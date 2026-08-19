# -*- coding: utf-8 -*-

import os
import datetime

import numpy as np
import pyqtgraph as pg
from PySide2.QtCore  import QMetaObject, Qt
from PySide2.QtGui   import QPixmap, QPainter, QColor
from PySide2.QtWidgets import (QTableWidget,
    QTableWidgetItem, QGridLayout, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QMessageBox
)

import pyTempico as Tempico
from Utils.createsavefile import createsavefile as savefile
from Threads.ThreadFCS import WorkerThreadFCS
from scipy.optimize import curve_fit


class FCSLogAxis(pg.AxisItem):
    """
    Custom logarithmic AxisItem for FCS.
    Only labels decade boundary ticks (e.g. 10^-6, 10^-5) to prevent overlapping labels.
    If zoomed in very closely (less than a decade visible), labels intermediate ticks with units.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the axis item and disables automatic SI-prefix scaling.

        :param args: Positional arguments forwarded to ``pg.AxisItem``.
        :param kwargs: Keyword arguments forwarded to ``pg.AxisItem``.
        :return: None
        """
        super().__init__(*args, **kwargs)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        Formats tick labels for the logarithmic τ axis.

        When not in log mode, delegates to the base class implementation. In
        log mode, if any of the given tick ``values`` sit on an integer decade
        boundary, only those decades are labeled (as ``10^n``) and all other
        ticks are left blank to avoid overlapping text. If no decade boundary
        is visible (i.e. the view is zoomed in to less than one decade),
        every tick is instead labeled with its time value converted to the
        most readable unit (ns, µs, ms, or s).

        :param values: Tick positions, expressed as ``log10`` of the
            underlying value.
        :param scale: Axis scale factor, as provided by pyqtgraph.
        :param spacing: Spacing between major ticks, as provided by
            pyqtgraph.
        :return: List of formatted tick label strings, one per value.
        """
        if not self.logMode:
            return super().tickStrings(values, scale, spacing)

        # Count how many integer decades are in values
        major_count = sum(1 for val in values if abs(val - round(val)) < 1e-9)

        if major_count > 0:
            strings = []
            for val in values:
                if abs(val - round(val)) < 1e-9:
                    exponent = int(round(val))
                    strings.append(f"10^{exponent}")
                else:
                    strings.append("")
            return strings
        else:
            strings = []
            for val in values:
                t_s = 10**val
                if t_s < 9.9e-7:
                    strings.append(f"{t_s * 1e9:.1f} ns")
                elif t_s < 9.9e-4:
                    strings.append(f"{t_s * 1e6:.1f} µs")
                elif t_s < 0.99:
                    strings.append(f"{t_s * 1e3:.1f} ms")
                elif t_s < 99.0:
                    strings.append(f"{t_s:.1f} s")
                else:
                    strings.append(f"{t_s:.1e} s")
            return strings


class FCSLogic():
    """
    Orchestration layer for the FCS measurement tab.

    Creates and manages a single pyqtgraph ``PlotWidget`` that displays the
    normalized autocorrelation function G(τ) in real time. Instantiates and
    controls a ``WorkerThreadFCS`` during acquisition, and provides save
    (data + plot) functionality after the measurement finishes.

    Parameters
    ----------
    parent : QWidget
        The ``QFrame`` / ``QWidget`` inside the FCS tab where the plot is
        injected (equivalent to ``Graph3`` in ``StartStopLogic``).
    disconnectButton : QPushButton
        Main-window Disconnect button – disabled while measuring.
    device : Tempico.TempicoDevice
        Open Tempico device instance.
    startButton : QPushButton
        Starts the acquisition.
    stopButton : QPushButton
        Stops the acquisition.
    saveDataButton : QPushButton
        Saves the raw G(τ) curve to a text/csv/dat file.
    savePlotButton : QPushButton
        Saves the plot as an image file.
    clearButton : QPushButton
        Clears the accumulated curve without restarting the device.
    connectButton : QPushButton
        Main-window Connect button – re-enabled when disconnected.
    mainWindow : QMainWindow
        Reference to the application's main window (for tab management and
        ``activeMeasurement`` / ``noMeasurement`` coordination).
    statusValue : QLabel
        Label that shows the current acquisition status text.
    statusPoint : QLabel
        Small label used as a coloured status indicator (traffic-light dot).
    timerStatus : QTimer
        Shared timer that polls the device connection; stopped during
        measurement and restarted when idle.
    tau_0 : int, optional
        Base bin size in picoseconds. Default: 1 000 000 ps (1 ms).
    """

    def __init__(
        self,
        parent,
        disconnectButton,
        device: Tempico.TempicoDevice,
        startButton,
        stopButton,
        saveDataButton,
        savePlotButton,
        clearButton,
        connectButton,
        mainWindow,
        statusValue,
        statusPoint,
        timerStatus,
        callsLabel,
        eventsLabel,
        elapsedLabel,
        fitButton,
        fitModelCombo,
        fitEquationLabel,
        fitResultLabel,
        fitResultsFrame,
        fitTable,
        fitOffsetCheckBox,
        stopChannelComboBox,
        fitResetParamsButton=None,
        tau_0 = 1_000_000_000,   # 1000 µs = 1 ms in picoseconds
    ):
        """
        Initializes the FCS logic layer and wires up the tab's widgets.

        Stores references to the device and every widget used by the FCS tab
        (start/stop/save/clear buttons, status labels, live-count labels,
        fitting controls, and the stop-channel selector), sets the initial
        enabled/disabled state of each button, and connects each control's
        signal to its corresponding handler (start/stop measurement, save
        data, save plot, clear curve, run fit, update fit equation preview,
        repopulate the "Initial value" guesses, sync manual edits to the
        per-model cache, reset those guesses to "Auto", apply offset). It
        also initializes the correlator parameters (``tau_0``, number of
        multi-tau levels, and grouping factor ``m``) and the internal
        sentinels used to track thread lifecycle and measurement state.

        :param parent: The widget where the pyqtgraph plot is injected.
        :param disconnectButton: Main-window Disconnect button.
        :param device: Open ``Tempico.TempicoDevice`` instance.
        :param startButton: Button that starts the acquisition.
        :param stopButton: Button that stops the acquisition.
        :param saveDataButton: Button that saves the G(τ) data.
        :param savePlotButton: Button that saves the plot image.
        :param clearButton: Button that clears the accumulated curve.
        :param connectButton: Main-window Connect button.
        :param mainWindow: Reference to the application's main window.
        :param statusValue: Label showing the current status text.
        :param statusPoint: Label used as a coloured status dot.
        :param timerStatus: Shared connection-polling timer.
        :param callsLabel: Label showing the number of calls received.
        :param eventsLabel: Label showing the number of events detected.
        :param elapsedLabel: Label showing the elapsed measurement time.
        :param fitButton: Button that runs the correlation curve fit.
        :param fitModelCombo: Combo box to select the fit model.
        :param fitEquationLabel: Label displaying the fit equation.
        :param fitResultLabel: Label displaying the fit result summary.
        :param fitResultsFrame: Frame containing the fit results widgets.
        :param fitTable: Three-column table ("Parameter" | "Initial value" |
            "Fit result"); the middle column is user-editable and seeds
            ``curve_fit``'s ``p0`` the next time "Fit" is pressed.
        :param fitOffsetCheckBox: Checkbox to toggle the G(∞) offset in the fit.
        :param stopChannelComboBox: Combo box to select the stop channel.
        :param fitResetParamsButton: Optional button ("Auto") that discards
            manual edits to the "Initial value" column for the current model
            and restores the automatically computed guess.
        :param tau_0: Base bin size in picoseconds. Defaults to
            ``1_000_000_000`` ps (1 ms).
        :type tau_0: int, optional
        :return: None
        """
        super().__init__()

        # ── Utility ──────────────────────────────────────────────────────────
        self.savefile = savefile()

        # ── Measurement window (used when saving data) ─────────────────────
        self.initialDate = ""
        self.finalDate   = ""

        # ── Device ───────────────────────────────────────────────────────────
        self.device = device

        # ── Correlator parameters ─────────────────────────────────────────
        # tau_0 in ps; num_levels and m are fixed internally (not user-facing)
        self.tau_0      = tau_0
        self.num_levels = 16   # fixed: covers ~1 ms to ~32 s at tau_0=1ms
        self.m          = 16   # fixed: standard multi-tau value

        # ── Widget references ─────────────────────────────────────────────
        self.parent           = parent
        self.disconnectButton = disconnectButton
        self.connectButton    = connectButton
        self.mainWindow       = mainWindow
        self.statusValue      = statusValue
        self.statusPoint      = statusPoint
        self.timerConnection  = timerStatus
        self.callsLabel       = callsLabel
        self.eventsLabel      = eventsLabel
        self.elapsedLabel     = elapsedLabel
        self.fitButton        = fitButton
        self.fitModelCombo    = fitModelCombo
        self.fitEquationLabel  = fitEquationLabel
        self.fitResultLabel    = fitResultLabel
        self.fitResultsFrame   = fitResultsFrame
        self.fitTable          = fitTable
        self.fitOffsetCheckBox     = fitOffsetCheckBox
        self.stopChannelComboBox   = stopChannelComboBox
        self.fitResetParamsButton  = fitResetParamsButton

        # Cache of user-edited initial guesses, keyed by fit-model index, so
        # switching models back and forth doesn't lose what was typed in.
        self._initial_params_cache = {}
        # Records the p0 actually used / model index for the last successful
        # fit, so it can be included in the saved-data header for
        # reproducibility.
        self.last_p0_used = None
        self.last_fit_idx = None

        self.startButton    = startButton
        self.stopButton     = stopButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.clearButton    = clearButton

        # Stored as None until main.py sets them after constructing this object.
        # main.py calls set_parameter_widgets() right after instantiation.
        self.tau0SpinBox        = None
        self.durationSpinBox    = None
        self.indefiniteCheckBox = None

        # ── Button initial states ─────────────────────────────────────────
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(True)
        # ── Button connections ────────────────────────────────────────────
        self.startButton.clicked.connect(self.start_graphic)
        self.stopButton.clicked.connect(self.stop_graphic)
        self.saveDataButton.clicked.connect(self.save_data)
        self.savePlotButton.clicked.connect(self.save_plot)
        self.clearButton.clicked.connect(self.clear_curve)
        self.fitButton.clicked.connect(self.run_fit)
        self.fitModelCombo.currentIndexChanged.connect(self._update_equation_label_preview)
        self.fitModelCombo.currentIndexChanged.connect(
            self._populate_initial_params_table
        )
        if self.fitTable is not None:
            self.fitTable.cellChanged.connect(
                self._on_initial_param_edited
            )
        if self.fitResetParamsButton is not None:
            self.fitResetParamsButton.clicked.connect(
                self._reset_initial_params_to_auto
            )
        self.fitOffsetCheckBox.stateChanged.connect(self._apply_offset_to_plot)
        # ── Internal state ────────────────────────────────────────────────
        # Sentinel: True while the worker thread is alive
        self.threadCreatedSentinel = False
        # Set to True once the first measurement finishes (enables Save)
        self.hasMeasurementData    = False
        # Set to True when device disconnects mid-measurement
        self.withoutMeasurement    = False

        self.isStopping            = False
        # Save-format sentinels (prevent re-saving the same data twice)
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0

        # Last emitted G(τ) arrays – kept so save works after stop
        self.last_taus_s      = np.array([])
        self.last_g           = np.array([])
        self.last_stop_times_ps = np.array([])   # raw stop times in ps

        # Show sensible starting guesses and the equation right away for the
        # currently selected model (mirrors G2Logic).
        self._populate_initial_params_table()
        self._update_equation_label_preview()

        # ── Build the plot ────────────────────────────────────────────────
        self._build_plot()

    # ── Plot construction ─────────────────────────────────────────────────────

    def _build_plot(self):
        """
        Create and inject the pyqtgraph plot widget into ``self.parent``.

        Sets up a logarithmic x-axis (standard FCS presentation), a dashed
        reference line at G = 1, and an empty scatter curve that will be
        updated in real time by ``update_plot``.

        :return: None
        """
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('w')
        custom_axis = FCSLogAxis(orientation='bottom')
        self.plot = self.win.addPlot(axisItems={'bottom': custom_axis})

        self.plot.setTitle('Autocorrelation Function — FCS')
        self.plot.setLabel('left',   'G(τ)')
        self.plot.setLabel('bottom', 'Lag time τ (s)')
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        # Logarithmic x-axis: standard for FCS curves (ns to ms range)
        self.plot.setLogMode(x=True, y=False)
        legend = self.plot.addLegend(offset=(-10, 10))
        legend.anchor(itemPos=(1, 0), parentPos=(1, 0), offset=(-10, 10))

        # Dashed reference line at G = 1 (uncorrelated baseline)
        ref_line = pg.InfiniteLine(
            pos=1.0, angle=0,
            pen=pg.mkPen('gray', width=1,
                         style=pg.QtCore.Qt.DashLine)
        )
        self.plot.addItem(ref_line)

        # Fit curve – drawn after the user clicks Fit
        self.fit_curve = self.plot.plot(
            [], [],
            pen=pg.mkPen('red', width=2),
            name='Fit',
        )

        # Scatter curve updated in real time
        self.curve = self.plot.plot(
            [], [],
            pen=None,
            symbol='o',
            symbolSize=5,
            symbolBrush='steelblue',
            symbolPen=None,
            name='G(τ) measured',
        )

        # Reuse the existing layout on graphicFrame if it already has one
        # (set by setupUi), otherwise create a new QGridLayout.
        existing_layout = self.parent.layout()
        if existing_layout is not None:
            self.gridlayout = existing_layout
        else:
            self.gridlayout = QGridLayout(self.parent)

        # Safely remove any widgets already in the layout
        while self.gridlayout.count():
            item = self.gridlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        self.gridlayout.addWidget(self.win, 0, 0)

    # ── Duration widget injection (called from main.py) ───────────────────────

    def set_parameter_widgets(self, tau0SpinBox, durationSpinBox, indefiniteCheckBox):
        """
        Provide references to the parameter widgets.

        Called by ``main.py`` immediately after constructing ``FCSLogic`` so
        that ``start_graphic`` can read the user-configured values at the
        moment the measurement starts — not at construction time.

        This is critical for ``tau0SpinBox``: if the user changes τ₀ after
        the tab is first opened, the new value must be picked up when
        "Begin measurement" is pressed.

        :param tau0SpinBox: QSpinBox with τ₀ in µs.
        :param durationSpinBox: QSpinBox with duration in seconds.
        :param indefiniteCheckBox: QCheckBox; when checked the measurement
            runs until the user presses Stop.
        :return: None
        """
        self.tau0SpinBox        = tau0SpinBox
        self.durationSpinBox    = durationSpinBox
        self.indefiniteCheckBox = indefiniteCheckBox


    def _get_stop_channel_index(self):
        """Returns 1-4 based on the selected stop-channel combo box index."""
        return self.stopChannelComboBox.currentIndex() + 1
    
    def _restore_buttons_after_stop(self):
        """Re-enable UI after a failed or aborted start."""
        self.mainWindow.tabs.setTabEnabled(0, True)
        self.mainWindow.tabs.setTabEnabled(1, True)
        self.mainWindow.tabs.setTabEnabled(2, True)
        self.mainWindow.tabs.setTabEnabled(3, True)
        self.mainWindow.tabs.setTabEnabled(5, True)
        self.tau0SpinBox.setEnabled(True) 
        self.durationSpinBox.setEnabled(True)
        self.fitOffsetCheckBox.setEnabled(True)
        self.disconnectButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(True)
        
        self.startTimerConnection()
        if hasattr(self.mainWindow, 'noMeasurement'):
            self.mainWindow.noMeasurement()

    # ── Start / Stop ──────────────────────────────────────────────────────────

    def start_graphic(self):
        """
        Start the FCS acquisition.

        Resets the curve, disables buttons that must not be used during
        measurement, stops the connection-polling timer, notifies the main
        window, and launches the ``WorkerThreadFCS``.

        :return: None
        """
        if self.device is None:
            return

        # Reset save sentinels so new data can be saved after this run
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0
        self.hasMeasurementData = False
        self.isStopping = False
        self.initialDate = datetime.datetime.now()
        self.finalDate = ""
        self.last_taus_s = np.array([])
        self.last_g      = np.array([])

        # Clear the curve visually
        self.curve.setData([], [])

        # Disable other tabs while measuring (mirrors StartStopLogic)
        self.mainWindow.tabs.setTabEnabled(0, False)  # Start-stop tab
        self.mainWindow.tabs.setTabEnabled(1, False)  # Lifetime tab
        self.mainWindow.tabs.setTabEnabled(2, False)  # Counts tab
        self.mainWindow.tabs.setTabEnabled(3, False)  # Time stamp tab
        self.mainWindow.tabs.setTabEnabled(5, False)  # G2 tab
        self.disconnectButton.setEnabled(False)
        

        # Button states during measurement
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.tau0SpinBox.setEnabled(False) 
        self.durationSpinBox.setEnabled(False)
        self.fitOffsetCheckBox.setEnabled(False)
        self.stopChannelComboBox.setEnabled(False)
        

        self.statusValue.setText("Measurement running")
        self.changeStatusColor(1)

        # Reset counters so the previous measurement's values don't persist
        self.callsLabel.setText("0")
        self.eventsLabel.setText("0")
        self.elapsedLabel.setText("0 s")

        # Stop the connection-polling timer while the thread owns the device
        self.stopTimerConnection()

        # Determine acquisition duration:
        # None = run indefinitely until Stop is pressed.
        total_seconds = None
        if (self.indefiniteCheckBox is not None
                and not self.indefiniteCheckBox.isChecked()
                and self.durationSpinBox is not None):
            total_seconds = self.durationSpinBox.value()

        # Read tau_0 from the spinbox at start time so any change the user
        # made after the tab was first opened is picked up correctly.
        # spinbox value is in µs → convert to picoseconds.
        if self.tau0SpinBox is not None:
            tau_0 = self.tau0SpinBox.value() * 1_000_000  # µs → ps
        else:
            tau_0 = self.tau_0  # fallback to constructor value

        # Instantiate and start the worker thread
        num_runs  = self.device.getNumberOfRuns()
        num_stops = self.device.ch1.getNumberOfStops()   # same for all channels
        ch_mode   = self.device.ch1.getMode()

        if num_stops < 2:
            self._restore_buttons_after_stop()
            dlg = QDialog(self.parent)
            dlg.setWindowTitle("Not enough stops")
            dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            dlg.setMinimumWidth(420)
            outer = QVBoxLayout(dlg)

            # Fila superior: icono warning + texto (replica QMessageBox)
            top_row = QHBoxLayout()
            icon_label = QLabel()
            icon_label.setPixmap(
                dlg.style().standardIcon(dlg.style().SP_MessageBoxWarning)
                .pixmap(32, 32)
            )
            icon_label.setAlignment(Qt.AlignTop)
            top_row.addWidget(icon_label)
            top_row.addSpacing(10)
            text_label = QLabel(
                "You must set at least 2 stops to start the "
                "autocorrelation (FCS) measurement.\n\n"
                "Do you want to change the configuration to 2 stops?"
            )
            text_label.setWordWrap(True)
            top_row.addWidget(text_label, stretch=1)
            outer.addLayout(top_row)
            outer.addSpacing(12)

            # Fila de botones equiespaciados
            btn_row = QHBoxLayout()
            yes_btn      = QPushButton("Yes")
            no_btn       = QPushButton("No")
            settings_btn = QPushButton("Go to settings")
            for b in (yes_btn, no_btn, settings_btn):
                btn_row.addWidget(b, stretch=1)
            outer.addLayout(btn_row)

            clicked = [None]
            yes_btn.clicked.connect(
                lambda: (clicked.__setitem__(0, "yes"), dlg.accept()))
            no_btn.clicked.connect(
                lambda: (clicked.__setitem__(0, "no"),  dlg.accept()))
            settings_btn.clicked.connect(
                lambda: (clicked.__setitem__(0, "settings"), dlg.accept()))
            dlg.exec_()

            if clicked[0] == "yes":
                for ch in [self.device.ch1, self.device.ch2,
                           self.device.ch3, self.device.ch4]:
                    ch.setNumberOfStops(2)
                self.start_graphic()
            elif clicked[0] == "settings":
                self.mainWindow.settings_clicked()
            return
        
        self.mainWindow.saveSettings()
        self.mainWindow.activeMeasurement()
        self.worker = WorkerThreadFCS(
            parent        = self.parent,
            device        = self.device,
            tau_0         = tau_0,
            num_levels    = self.num_levels,
            m             = self.m,
            total_seconds = total_seconds,
            stop_channel  = self._get_stop_channel_index(),
            start_channel = None,
            num_runs      = num_runs,
            num_stops     = num_stops,
            channel_mode  = ch_mode,
        )
        self.worker.dataReady.connect(self.update_plot)
        self.worker.statusUpdate.connect(self.changeStatusThread)
        self.worker.colorValue.connect(self.changeColorThread)
        self.worker.stringValue.connect(self.changeStatusThread)
        self.worker.threadCreated.connect(self.threadRunning)
        self.worker.finished.connect(self.threadComplete)
        self.worker.start()

    def stop_graphic(self):
        """
        Stop the acquisition and restore the UI to idle state.

        :return: None
        """
        self.isStopping = True
        self.finalDate = datetime.datetime.now()
        if not self.withoutMeasurement:
            self.startTimerConnection()

        if self.threadCreatedSentinel:
            self.worker.stop()

        self.statusValue.setText("No measurement running")
        self.changeStatusColor(0)

        # Re-enable tabs
        self.mainWindow.tabs.setTabEnabled(0, True)
        self.mainWindow.tabs.setTabEnabled(1, True)
        self.mainWindow.tabs.setTabEnabled(2, True)
        self.mainWindow.tabs.setTabEnabled(3, True)
        self.mainWindow.tabs.setTabEnabled(4, True)
        self.mainWindow.tabs.setTabEnabled(5, True)
        self.disconnectButton.setEnabled(True)
        self.mainWindow.noMeasurement()

        self.stopButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(True)
        self.tau0SpinBox.setEnabled(True)
        self.durationSpinBox.setEnabled(True)
        self.fitOffsetCheckBox.setEnabled(True)
        
        if not self.withoutMeasurement:
            self.startButton.setEnabled(True)

        if self.hasMeasurementData:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
            self.clearButton.setEnabled(True)
            self.fitButton.setEnabled(True)
    # ── Thread signal handlers ─────────────────────────────────────────────────

    def threadRunning(self, status):
        """
        Update ``threadCreatedSentinel`` from the ``threadCreated`` signal.

        Parameters
        ----------
        status : int
            0 → thread just started; 1 → thread just stopped.

        :return: None
        """
        if status == 0:
            self.threadCreatedSentinel = True
        elif status == 1:
            self.threadCreatedSentinel = False

    def threadComplete(self):
        """
        Called when the worker thread finishes naturally (``finished`` signal).

        :return: None
        """
        self.threadCreatedSentinel = False
        self.stop_graphic()

    def update_plot(self, taus_ps, g, stop_times_ps):
        """
        Update the G(τ) scatter plot with the latest correlation data.

        Converts lag times from picoseconds to seconds before plotting.
        Keeps a copy of the last arrays for the save functions.

        Parameters
        ----------
        taus_ps : numpy.ndarray
            Lag times in picoseconds (emitted by the thread).
        g : numpy.ndarray
            Normalized autocorrelation values G(τ).
        stop_times_ps : numpy.ndarray
            All raw stop times collected so far, in picoseconds.

        :return: None
        """
        taus_s = taus_ps * 1e-12
        mask = taus_s > 0
        self.curve.setData(taus_s[mask], g[mask])

        # Cache for saving
        self.last_taus_s        = taus_s[mask]
        self.last_g             = g[mask]
        self.last_stop_times_ps = stop_times_ps
        self.hasMeasurementData = True

    def changeStatusThread(self, new_text):
        """
        Update the status label text from a thread signal.

        :param new_text: Text to display (str).
        :return: None
        """
        if self.isStopping:
            return
        self.statusValue.setText("Measurement running")
        if self.isStopping:
            return
        try:
            parts = new_text.split("|")
            self.callsLabel.setText(parts[0].split(":")[1].strip())
            self.eventsLabel.setText(parts[1].split(":")[1].strip())
            self.elapsedLabel.setText(parts[2].split(":")[1].strip())
            self.statusValue.setText("Measurement running")
        except (IndexError, AttributeError):
            self.statusValue.setText(new_text)

    def changeColorThread(self, color):
        """
        Update the status-indicator dot colour from a thread signal.

        Uses the same colour code as ``StartStopLogic``:
        0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    # ── Clear ─────────────────────────────────────────────────────────────────

    def clear_curve(self):
        """
        Clear the G(τ) curve and cached data without stopping the device.

        :return: None
        """
        self.last_taus_s        = np.array([])
        self.last_g             = np.array([])
        self.last_stop_times_ps = np.array([])
        self.hasMeasurementData = False
        self.curve.setData([], [])
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.fit_curve.setData([], [])
        self._clear_fit_results()
        self.fitResultsFrame.setVisible(False)

    # ── Save data ─────────────────────────────────────────────────────────────
    def _get_fit_header_lines(self):
        """
        Builds header lines describing the current curve fit, for saved files.

        Returns an empty string if no fit results are currently shown
        (``fitResultsFrame`` is hidden). Otherwise, builds a multi-line
        string with the selected fit model's name, its equation (including
        the optional G(∞) offset term), one "Initial <param>" line per
        guess actually used for the last successful fit of this same model
        (from ``last_p0_used``/``last_fit_idx``), and one line per fitted
        parameter/derived quantity read from ``fitTable``.

        :return: Tab-separated header lines describing the fit, or an empty
            string if no fit is currently displayed.
        :rtype: str
        """
        if not self.fitResultsFrame.isVisible():
            return ""

        idx = self.fitModelCombo.currentIndex()
        pre = "G(∞) + " if self.fitOffsetCheckBox.isChecked() else ""

        model_names = {
            0: "3D Gaussian diffusion",
            1: "Anomalous diffusion",
            2: "Chemical relaxation",
            3: "Diffusion with flow",
            4: "Triplet state correction",
            5: "Two-component diffusion",
        }
        equations = {
            0: f"{pre}(1/N)·(1 + tau/tD)^-1·(1 + a^-2·tau/tD)^-0.5",
            1: f"{pre}(1/N)·(1 + (tau/tD)^alpha)^-1·(1 + a^-2·(tau/tD)^alpha)^-0.5",
            2: f"{pre}(K/N)·exp(-tau/tB),  G(0)=K/N, K=kon/koff",
            3: f"{pre}(1/N)·(1+tau/tD)^-1·(1+a^-2·tau/tD)^-0.5·exp[-(tau/tv)^2/(1+tau/tD)]",
            4: f"{pre}(1/N)·[(1-F+F·exp(-tau/tF))/(1-F)]·(1+tau/tD)^-1·(1+a^-2·tau/tD)^-0.5",
            5: f"{pre}(1/N)·(a1·GD1 + a2·GD2),  GDi=(1+tau/tDi)^-1·(1+a^-2·tau/tDi)^-0.5",
        }

        lines = [
            f"Fit model:\t{model_names.get(idx, 'Unknown')}",
            f"Fit equation:\t{equations.get(idx, '')}",
        ]

        if self.last_p0_used is not None and self.last_fit_idx == idx:
            labels = self.PARAM_LABELS.get(idx, [])
            for (name, unit, scale), value in zip(labels, self.last_p0_used):
                unit_suffix = f" {unit}" if unit else ""
                lines.append(f"Initial {name}:\t{value * scale:.4f}{unit_suffix}")

        if self.fitTable is not None and self.last_fit_idx == idx:
            for row in range(self.fitTable.rowCount()):
                name_item  = self.fitTable.item(row, 0)
                value_item = self.fitTable.item(row, 2)
                if name_item and value_item and value_item.text():
                    lines.append(f"{name_item.text()}:\t{value_item.text()}")

        return "\n".join(lines)
    
    
    def save_data(self):
        """
        Prompts for a file format and saves the current G(τ) curve and photon times.

        Does nothing if there is no measurement data cached. Otherwise, shows
        a small dialog to let the user choose the output format (txt, csv, or
        dat), then writes two files into the configured save folder: one with
        the ``tau_s`` / ``G(tau)`` pairs of the autocorrelation curve, and
        another with the raw stop timestamps in picoseconds. Both files share
        a header with the measurement window, device model, correlator
        parameters, selected stop channel, and — if a fit was run — the fit
        model, equation, and fitted parameter values. Shows a confirmation or
        error message box depending on the outcome.

        :return: None
        """
        if len(self.last_taus_s) == 0:
            return

        dataFolderPrefix = self.savefile.getDataFolderPrefix()
        folder_path      = dataFolderPrefix["saveFolder"]

        now               = datetime.datetime.now()
        current_date_str  = now.strftime("%Y%m%d%H%M%S")

        # Stop channel name used for the output file name
        ch_names  = ["A", "B", "C", "D"]
        ch_index  = self.stopChannelComboBox.currentIndex()
        ch_label  = ch_names[ch_index] if ch_index < len(ch_names) else "A"

        # ── Format selection dialog ───────────────────────────────────────
        dialog = QDialog(self.parent)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setWindowTitle("Save")
        dialog.setMinimumWidth(260)
        vlay = QVBoxLayout(dialog)
        vlay.setContentsMargins(20, 20, 20, 20)
        vlay.setSpacing(10)
        vlay.addWidget(QLabel("Select the text format:"))
        fmt_box = QComboBox(dialog)
        fmt_box.addItem("txt")
        fmt_box.addItem("csv")
        fmt_box.addItem("dat")
        vlay.addWidget(fmt_box)
        accept_btn = QPushButton("Accept", dialog)
        accept_btn.clicked.connect(dialog.accept)
        vlay.addWidget(accept_btn)

        if dialog.exec_() != QDialog.Accepted:
            return

        selected_format = fmt_box.currentText()

        

        prefix   = dataFolderPrefix['fcsPrefix']
        filename = f"{prefix}_{current_date_str}_Channel{ch_label}"

        # ── Header: correlator parameters ─────────────────────────────────
        tau_0_us = self.tau0SpinBox.value() if self.tau0SpinBox is not None else self.tau_0 // 1_000_000

        setting = (
            f"Tab:\tAutocorrelation (FCS)\n"
            f"Initial date:\t{self.initialDate}\n"
            f"Final date:\t{self.finalDate}\n"
            f"Device model:\t{self.device.getModelIdn()}\n"
            f"Base bin width τ₀ (µs):\t{tau_0_us}\n"
            f"num_levels:\t{self.num_levels}\n"
            f"m:\t{self.m}\n"
            f"Stop Channel:\tChannel {ch_label}"
        )

        # ── Add fit info if present ────────────────────────────────────────
        fit_header = self._get_fit_header_lines()
        if fit_header:
            setting += "\n" + fit_header

        try:
            filename_acf  = f"{prefix}_{current_date_str}_Channel{ch_label}_GtauCurve"
            filename_phot = f"{prefix}_{current_date_str}_Channel{ch_label}_StopTimes"

            sep = ";" if selected_format == "csv" else "\t"

            # --- ACF file ---
            acf_path = os.path.join(folder_path, f"{filename_acf}.{selected_format}")
            with open(acf_path, 'w', encoding='utf-8') as f:
                f.write(setting + '\n')
                f.write(f"tau_s{sep}G(tau)\n")
                for t, g in zip(self.last_taus_s, self.last_g):
                    f.write(f"{t}{sep}{g}\n")

            # --- Photon times file ---
            phot_path = os.path.join(folder_path, f"{filename_phot}.{selected_format}")
            with open(phot_path, 'w', encoding='utf-8') as f:
                f.write(setting + '\n')
                f.write(f"stop_stop_time_ps\n")
                for t in self.last_stop_times_ps:
                    f.write(f"{t}\n")

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"The files have been saved successfully in path folder:\n\n"
                f"{folder_path} with the following names:\n\n"
                f"File1: {filename_acf}.{selected_format}\n"
                f"File2: {filename_phot}.{selected_format}"
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        except Exception:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error saving")
            msg.setText("The file could not be saved.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    # ── Save plot ─────────────────────────────────────────────────────────────

    def save_plot(self):
        """
        Prompts for an image format and exports the current plot to a file.

        Shows a small dialog to let the user choose the output image format
        (png, tiff, or jpg), builds the destination file name from the
        configured file prefix, the current timestamp, and the selected stop
        channel, then exports the plot at 800x600 pixels using pyqtgraph's
        ``ImageExporter``. The destination folder is created if it does not
        already exist. Shows a confirmation or error message box depending on
        the outcome.

        :return: None
        """
        try:
            dataFolderPrefix = self.savefile.getDataFolderPrefix()
            folder_path      = dataFolderPrefix["saveFolder"]

            dialog = QDialog(self.parent)
            dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            dialog.setWindowTitle("Save plot")
            dialog.setMinimumWidth(260)
            vlay = QVBoxLayout(dialog)
            vlay.setContentsMargins(20, 20, 20, 20)
            vlay.setSpacing(10)
            vlay.addWidget(QLabel("Select the image format:"))
            fmt_box = QComboBox(dialog)
            fmt_box.addItem("png")
            fmt_box.addItem("tiff")
            fmt_box.addItem("jpg")
            vlay.addWidget(fmt_box)
            accept_btn = QPushButton("Accept", dialog)
            accept_btn.clicked.connect(dialog.accept)
            vlay.addWidget(accept_btn)

            if dialog.exec_() != QDialog.Accepted:
                return

            selected_format  = fmt_box.currentText()
            current_date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            ch_names = ["A", "B", "C", "D"]
            ch_index = self.stopChannelComboBox.currentIndex()
            ch_label = ch_names[ch_index] if ch_index < len(ch_names) else "A"

            prefix    = dataFolderPrefix.get("fcsPrefix", "Autocorrelation")
            filename  = f"{prefix}_{current_date_str}_Channel{ch_label}"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            sep       = '/' if os.name == 'posix' else '\\'
            full_path = folder_path + sep + filename + '.' + selected_format

            exporter = pg.exporters.ImageExporter(self.plot)
            exporter.parameters()['width']  = 800
            exporter.parameters()['height'] = 600
            exporter.export(full_path)

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"Plot saved in:\n\n{folder_path}\n\n"
                f"File: {filename}.{selected_format}"
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        except Exception:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error saving")
            msg.setText(
                "The plot could not be saved. "
                "Check the folder path or system files."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    # ── Status dot helpers ────────────────────────────────────────────────────

    def changeStatusColor(self, color):
        """
        Set the status-indicator dot colour from Logic-layer code.

        Colour codes: 0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    def _draw_status_dot(self, color):
        """
        Draw a filled circle on ``statusPoint`` with the given colour.

        Internal helper shared by ``changeStatusColor`` and
        ``changeColorThread`` to avoid code duplication.

        :param color: Colour code (int). 0=grey, 1=green, 2=yellow, 3=orange.
        :return: None
        """
        pixmap = QPixmap(self.statusPoint.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if color == 0:
            painter.setBrush(QColor(128, 128, 128))
        elif color == 1:
            painter.setBrush(QColor(0, 255, 0))
        elif color == 2:
            painter.setBrush(QColor(255, 255, 0))
        elif color == 3:
            painter.setBrush(QColor(255, 165, 0))
        painter.setPen(Qt.NoPen)
        point_size = min(
            self.statusPoint.width(), self.statusPoint.height()
        ) // 2
        x = (self.statusPoint.width()  - point_size) // 2
        y = (self.statusPoint.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusPoint.setPixmap(pixmap)

    # ── Timer helpers ─────────────────────────────────────────────────────────

    def stopTimerConnection(self):
        """
        Stop the shared connection-polling timer.

        Called when measurement starts so the timer does not interfere with
        the thread's exclusive use of the device.

        :return: None
        """
        self.timerConnection.stop()

    def startTimerConnection(self):
        """
        Restart the shared connection-polling timer at 500 ms.

        Called when the measurement finishes or is stopped.

        :return: None
        """
        self.timerConnection.start(500)

    # ── Device connect / disconnect (called from main.py) ─────────────────────

    def connectedDevice(self, device_new):
        """
        Update the device reference after a reconnection.

        Called by ``MainWindow.open_dialog`` when the user reconnects.

        :param device_new: New open ``TempicoDevice`` instance.
        :return: None
        """
        self.device = device_new
        self.withoutMeasurement = False
        self.startButton.setEnabled(True)
    # ── Fit logic ─────────────────────────────────────────────────────────────

    @staticmethod
    def _model_3d(tau, N, tau_D, kappa, offset=1.0):
        """3D Gaussian diffusion model — free structural parameter κ."""
        return offset + (1.0 / N) * (1.0 / (1.0 + tau / tau_D)) * (
            1.0 / np.sqrt(1.0 + tau / (kappa**2 * tau_D))
        )

    @staticmethod
    def _model_anomalous(tau, N, tau_D, alpha, kappa, offset=1.0):
        """3D anomalous diffusion model — free structural parameter κ."""
        return offset + (1.0 / N) * (
            1.0 / (
                (1.0 + (tau / tau_D)**alpha) *
                np.sqrt(1.0 + (kappa**-2) * (tau / tau_D)**alpha)
            )
        )

    @staticmethod
    def _model_chemical(tau, N, tau_B, K, offset=1.0):
        """Pure chemical relaxation (fast diffusion limit). G(0) = (1/N)·K"""
        G0 = (1.0 / N) * K
        return offset + G0 * np.exp(-tau / tau_B)

    @staticmethod
    def _model_flow(tau, N, tau_D, kappa, tau_v, offset=1.0):
        """3D diffusion with uniform lateral flow (τᵥ = ωxy/v)."""
        diff = (1.0 / (1.0 + tau / tau_D)) * (1.0 / np.sqrt(1.0 + (kappa**-2) * (tau / tau_D)))
        flow = np.exp(-(tau / tau_v)**2 / (1.0 + tau / tau_D))
        return offset + (1.0 / N) * diff * flow

    @staticmethod
    def _model_triplet(tau, N, tau_D, kappa, F, tau_F, offset=1.0):
        """Triplet state correction for normal 3D diffusion."""
        triplet = (1.0 - F + F * np.exp(-tau / tau_F)) / (1.0 - F)
        diff    = (1.0 / (1.0 + tau / tau_D)) * (1.0 / np.sqrt(1.0 + (kappa**-2) * (tau / tau_D)))
        return offset + (1.0 / N) * triplet * diff

    @staticmethod
    def _model_two_component(tau, N, tau_D1, tau_D2, alpha_1, kappa, offset=1.0):
        """Two-component 3D diffusion: weighted sum of two species."""
        alpha_2 = 1.0 - alpha_1
        d1 = (1.0 / (1.0 + tau / tau_D1)) * (1.0 / np.sqrt(1.0 + (kappa**-2) * (tau / tau_D1)))
        d2 = (1.0 / (1.0 + tau / tau_D2)) * (1.0 / np.sqrt(1.0 + (kappa**-2) * (tau / tau_D2)))
        return offset + (1.0 / N) * (alpha_1 * d1 + alpha_2 * d2)

    # Parameter names, display units, and unit-scale factors per fit model,
    # in curve_fit argument order (the fixed G(∞) offset is controlled by
    # ``fitOffsetCheckBox`` and is never part of this list). "Scale" converts
    # curve_fit's internal value (always in seconds for any tau-like
    # parameter) into the human-friendly unit shown in the table:
    # display_value = internal_value * scale. Shared by the editable
    # "Initial value" column, the "Fit result" column, and the saved-data
    # header.
    PARAM_LABELS = {
        0: [(u"N", "", 1.0), (u"τD", "ms", 1e3), (u"κ", "", 1.0)],
        1: [(u"N", "", 1.0), (u"τD", "ms", 1e3), (u"α", "", 1.0), (u"κ", "", 1.0)],
        2: [(u"N", "", 1.0), (u"τB", "ms", 1e3), (u"K", "", 1.0)],
        3: [(u"N", "", 1.0), (u"τD", "ms", 1e3), (u"a", "", 1.0), (u"τv", "ms", 1e3)],
        4: [(u"N", "", 1.0), (u"τD", "ms", 1e3), (u"a", "", 1.0),
            (u"F", "", 1.0), (u"τF", "µs", 1e6)],
        5: [(u"N", "", 1.0), (u"τD1", "ms", 1e3), (u"τD2", "ms", 1e3),
            (u"α1", "", 1.0), (u"a", "", 1.0)],
    }

    def _default_p0(self, idx):
        """
        Automatically suggested initial guesses (p0) for model ``idx``, in
        curve_fit's own internal units (seconds for any tau-like parameter),
        based on the currently displayed G(τ) data when available, or on a
        generic placeholder (used to pre-fill the table before any data has
        been collected).

        :param idx: Selected fit-model index (``fitModelCombo.currentIndex()``).
        :type idx: int
        :return: Initial guesses, in curve_fit argument order.
        :rtype: list[float]
        """
        taus = self.last_taus_s
        if taus is not None and len(taus) > 0:
            positive = taus[taus > 0]
            tau_med  = float(np.median(positive)) if len(positive) > 0 else 1e-3
        else:
            tau_med = 1e-3  # 1 ms placeholder before any data is collected

        if idx == 0:      # 3D Gaussian
            return [1.0, tau_med, 5.0]
        elif idx == 1:    # Anomalous
            return [1.0, tau_med, 1.0, 5.0]
        elif idx == 2:    # Chemical
            return [1.0, tau_med * 0.1, 1.0]
        elif idx == 3:    # Flow
            return [1.0, tau_med, 5.0, tau_med]
        elif idx == 4:    # Triplet
            return [1.0, tau_med, 5.0, 0.1, 1e-5]
        elif idx == 5:    # Two-component
            return [1.0, tau_med * 0.5, tau_med * 2.0, 0.5, 5.0]
        return [1.0, tau_med, 5.0]

    @staticmethod
    def _get_bounds(idx):
        """
        Lower/upper ``curve_fit`` bounds for model ``idx``, in the same
        internal units and argument order as ``PARAM_LABELS[idx]`` and
        ``_default_p0(idx)``. Used both to constrain the fit itself and to
        clip a user-entered "Initial value" back into a valid range before
        it is passed to ``curve_fit`` as ``p0``.

        :param idx: Selected fit-model index (``fitModelCombo.currentIndex()``).
        :type idx: int
        :return: ``(lower, upper)`` bounds tuple, each a list of floats in
            curve_fit argument order.
        :rtype: tuple[list[float], list[float]]
        """
        if idx == 0:
            return ([0, 0, 0.01], [np.inf, np.inf, np.inf])
        elif idx == 1:
            return ([0, 0, 0.1, 0.01], [np.inf, np.inf, 2.0, np.inf])
        elif idx == 2:
            return ([0, 0, 0], [np.inf, np.inf, np.inf])
        elif idx == 3:
            return ([0, 0, 0.01, 0], [np.inf, np.inf, np.inf, np.inf])
        elif idx == 4:
            return ([0, 0, 0.01, 0, 0], [np.inf, np.inf, np.inf, 0.99, np.inf])
        elif idx == 5:
            return ([0, 0, 0, 0, 0.01], [np.inf, np.inf, np.inf, 1.0, np.inf])
        return ([0, 0, 0], [np.inf, np.inf, np.inf])

    def _populate_initial_params_table(self, *_args):
        """
        (Re)fill the "Parameter" and "Initial value" columns of the merged
        fit table for the currently selected fit model. Called on startup,
        whenever ``fitModelCombo`` changes, and by the "Auto" button.

        Values shown come from ``_initial_params_cache`` only once the user
        has actually edited that model's guesses (or reset them) in this
        session. Until then, the guess is recomputed fresh from the live
        G(τ) data every time this is called, so it keeps tracking the
        current measurement instead of freezing on whatever was on screen
        the first time (e.g. before any data existed).

        The "Fit result" column is always cleared here: changing the model
        or the initial guess invalidates whatever result was previously
        shown, so the user is prompted to press "Fit" again.

        :param _args: Ignored. Accepts and discards whatever arguments the
            triggering signal passes (e.g. ``fitModelCombo``'s new index),
            so this can be connected directly as a slot.
        :return: None
        """
        if self.fitTable is None:
            return

        idx    = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
        labels = self.PARAM_LABELS.get(idx, self.PARAM_LABELS[0])

        values = self._initial_params_cache.get(idx)
        if values is None:
            values = self._default_p0(idx)

        table = self.fitTable
        table.blockSignals(True)
        table.setRowCount(len(labels))
        for row, (name, unit, scale) in enumerate(labels):
            display_name = f"{name} ({unit})" if unit else name
            item_name = QTableWidgetItem(display_name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, item_name)

            item_value = QTableWidgetItem(f"{values[row] * scale:.4f}")
            item_value.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, item_value)

            item_result = QTableWidgetItem("")
            item_result.setFlags(item_result.flags() & ~Qt.ItemIsEditable)
            item_result.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, item_result)
        table.resizeRowsToContents()
        h = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            h += table.rowHeight(row)
        table.setFixedHeight(h + 4)
        table.blockSignals(False)

        # A model/guess change invalidates any previously displayed result.
        self.last_p0_used = None
        self.last_fit_idx = None

    def _on_initial_param_edited(self, row, column):
        """
        Slot for ``fitTable.cellChanged``: keep the per-model initial-guess
        cache in sync whenever the user edits the "Initial value" column.

        Ignores edits to any other column. An entry that can't be parsed
        as a number is reverted to its last known-good value (either the
        cached edit or the auto-computed default) rather than left invalid.

        :param row: Row index of the edited cell (one parameter per row).
        :type row: int
        :param column: Column index of the edited cell; only ``1``
            ("Initial value") is handled.
        :type column: int
        :return: None
        """
        if column != 1 or self.fitTable is None:
            return
        idx    = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
        labels = self.PARAM_LABELS.get(idx, self.PARAM_LABELS[0])
        if row >= len(labels):
            return
        item = self.fitTable.item(row, column)
        if item is None:
            return
        scale = labels[row][2]
        try:
            display_value = float(item.text())
        except ValueError:
            # Invalid entry — revert to the last known-good value.
            cached = self._initial_params_cache.get(idx, self._default_p0(idx))
            self.fitTable.blockSignals(True)
            item.setText(f"{cached[row] * scale:.4f}")
            self.fitTable.blockSignals(False)
            return

        cached = self._initial_params_cache.setdefault(idx, self._default_p0(idx))
        cached[row] = display_value / scale

    def _reset_initial_params_to_auto(self):
        """
        "Auto" button — discard any manual edits for the current model and
        go back to tracking the automatically computed guess (which itself
        keeps following the live G(τ) data on every subsequent repaint).

        :return: None
        """
        idx = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
        self._initial_params_cache.pop(idx, None)
        self._populate_initial_params_table()

    def _clear_fit_results(self):
        """
        Blank the "Fit result" column and forget the last successful fit,
        without touching the editable "Initial value" guesses or hiding the
        equation/table — so the panel stays ready for editing.

        Also drops any extra derived-quantity rows (e.g. α2, G(0), G(∞))
        appended by a previous fit, shrinking the table back to just the
        base parameters for the currently selected model.

        :return: None
        """
        if self.fitResultLabel is not None:
            self.fitResultLabel.setVisible(False)
        if self.fitTable is not None:
            idx    = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
            n_base = len(self.PARAM_LABELS.get(idx, []))
            self.fitTable.blockSignals(True)
            if self.fitTable.rowCount() > n_base:
                self.fitTable.setRowCount(n_base)
            for row in range(self.fitTable.rowCount()):
                item_result = QTableWidgetItem("")
                item_result.setFlags(item_result.flags() & ~Qt.ItemIsEditable)
                item_result.setTextAlignment(Qt.AlignCenter)
                self.fitTable.setItem(row, 2, item_result)
            self.fitTable.blockSignals(False)
        self.last_p0_used = None
        self.last_fit_idx = None

    def _read_initial_params(self, idx, bounds=None):
        """
        Read the editable p0 guesses for model ``idx`` (converting from the
        table's display units back into curve_fit's internal units),
        falling back to the auto-computed defaults for any missing/invalid
        entry, then clip them into ``bounds`` so a user-entered value
        outside the allowed range can't make curve_fit raise.

        Reads directly from ``fitTable`` column 1 ("Initial value"; the
        table always reflects the currently selected model, since it is
        repopulated on every ``fitModelCombo`` change) so whatever is on
        screen at the moment "Fit" is pressed is what gets used — no
        reliance on the edit signal having already fired. Falls back to the
        per-model cache, then to the computed defaults, if the table isn't
        available.

        :param idx: Selected fit-model index (``fitModelCombo.currentIndex()``).
        :type idx: int
        :param bounds: Optional ``(lower, upper)`` bounds tuple, as returned
            by ``_get_bounds(idx)``, used to clip the returned guesses so
            they satisfy ``curve_fit``'s constraints.
        :type bounds: tuple[list[float], list[float]], optional
        :return: p0 guesses, in curve_fit argument order.
        :rtype: list[float]
        """
        defaults = self._default_p0(idx)
        labels   = self.PARAM_LABELS.get(idx, self.PARAM_LABELS[0])
        p0 = list(defaults)

        table = self.fitTable
        if table is not None and table.rowCount() >= len(defaults):
            for row in range(len(defaults)):
                item = table.item(row, 1)
                if item is None:
                    continue
                try:
                    display_value = float(item.text())
                    scale         = labels[row][2] if row < len(labels) else 1.0
                    p0[row] = display_value / scale
                except ValueError:
                    pass  # keep the default for this entry
        else:
            cached = self._initial_params_cache.get(idx)
            if cached is not None:
                p0 = list(cached)

        if bounds is not None:
            lower, upper = bounds
            p0 = [min(max(v, lo), hi) for v, lo, hi in zip(p0, lower, upper)]

        return p0

    def _apply_offset_to_plot(self):
        """
        Redraws the plotted curve shifted by -1 when the G(∞) offset is unchecked.

        If the G(∞) offset checkbox is checked, the curve is plotted with
        its original values; otherwise, the curve is shifted down by 1 so it
        matches the convention where G(∞) = 0. Since changing the offset
        invalidates any previous fit, the fit curve is cleared, the fit
        results panel is hidden, and the equation preview label is
        refreshed.

        :return: None
        """
        if len(self.last_g) == 0:
            return
        if self.fitOffsetCheckBox.isChecked():
            self.curve.setData(self.last_taus_s, self.last_g)
        else:
            self.curve.setData(self.last_taus_s, self.last_g - 1.0)
        # Clear the previous fit since the offset changed
        self.fit_curve.setData([], [])
        self._clear_fit_results()
        self.fitResultsFrame.setVisible(False)
        self._update_equation_label_preview()

    def _update_equation_label_preview(self):
        """
        Shows the HTML-formatted equation for the currently selected fit model.

        Builds an HTML string with the mathematical expression of the model
        selected in ``fitModelCombo``, including the optional G(∞) offset
        term when ``fitOffsetCheckBox`` is checked, and displays it in
        ``fitEquationLabel``. Also makes the fit results panel visible so
        the equation is shown even before a fit has been run.

        :return: None
        """
        offset = 1.0 if self.fitOffsetCheckBox.isChecked() else 0.0
        idx    = self.fitModelCombo.currentIndex()
        pre    = "G(∞) + " if offset == 1.0 else ""
        d      = "(1 + τ/τ<sub>D</sub>)<sup>−1</sup>(1 + a<sup>−2</sup>τ/τ<sub>D</sub>)<sup>−½</sup>"

        if idx == 0:
            html = f"<center>G(τ) = {pre}<sup>1</sup>/<sub>N</sub> · {d}</center>"
        elif idx == 1:
            html = (f"<center>G(τ) = {pre}<sup>1</sup>/<sub>N</sub> · "
                    f"(1 + (τ/τ<sub>D</sub>)<sup>α</sup>)<sup>−1</sup>"
                    f"(1 + a<sup>−2</sup>(τ/τ<sub>D</sub>)<sup>α</sup>)<sup>−½</sup></center>")
        elif idx == 2:
            html = (f"<center>G(τ) = {pre}"
                    f"<sup>1</sup>/<sub>N</sub> · K · exp(−τ/τ<sub>B</sub>)"
                    f"&nbsp;&nbsp;[G(0) = K/N, K = k<sub>on</sub>/k<sub>off</sub>]</center>")
        elif idx == 3:
            html = (f"<center>G(τ) = {pre}<sup>1</sup>/<sub>N</sub> · {d} · "
                    f"exp[−(τ/τ<sub>v</sub>)<sup>2</sup>/(1 + τ/τ<sub>D</sub>)]</center>")
        elif idx == 4:
            html = (f"<center>G(τ) = {pre}<sup>1</sup>/<sub>N</sub> · "
                    f"(1 − F + F·e<sup>−τ/τ<sub>F</sub></sup>)/(1 − F) · {d}</center>")
        elif idx == 5:
            html = (f"<center>G(τ) = {pre}<sup>1</sup>/<sub>N</sub> · "
                    f"(α<sub>1</sub>·(1+τ/τ<sub>D1</sub>)<sup>−1</sup>(1+a<sup>−2</sup>τ/τ<sub>D1</sub>)<sup>−½</sup> + "
                    f"α<sub>2</sub>·(1+τ/τ<sub>D2</sub>)<sup>−1</sup>(1+a<sup>−2</sup>τ/τ<sub>D2</sub>)<sup>−½</sup>)</center>")
        else:
            html = ""
        self.fitEquationLabel.setText(html)
        self.fitResultsFrame.setVisible(True)

    def _update_equation_label(self, N, tD_ms, kappa, alpha=None, offset=1.0,
                                T=None, tau_T=None, tau_F=None,
                                tD2_ms=None, f1=None, tau_R=None, A=None):
        """
        Shows the HTML-formatted equation for the 3D or anomalous diffusion model.

        Refreshes the generic preview first (via
        `_update_equation_label_preview`), then overwrites `fitEquationLabel`
        with the specific equation for the normal 3D diffusion model (when
        `alpha` is ``None``) or the anomalous diffusion model (when `alpha`
        is provided), including the G(∞) offset term when `offset` equals 1.0.

        :param N: Fitted average number of particles in the observation volume.
        :param tD_ms: Fitted diffusion time, in milliseconds.
        :param kappa: Fitted structural parameter (κ).
        :param alpha: Fitted anomalous diffusion exponent (α); if ``None``,
            the normal (non-anomalous) diffusion equation is shown.
        :param offset: 1.0 to include the G(∞) offset term, 0.0 otherwise.
        :param T: Unused placeholder for the triplet-state fraction, kept for
            interface consistency with other fit models.
        :param tau_T: Unused placeholder for the triplet relaxation time.
        :param tau_F: Unused placeholder for the flow time.
        :param tD2_ms: Unused placeholder for the second diffusion time
            (two-component model).
        :param f1: Unused placeholder for the first-species fraction
            (two-component model).
        :param tau_R: Unused placeholder for the chemical relaxation time.
        :param A: Unused placeholder for the chemical relaxation amplitude.
        :return: None
        """
        self._update_equation_label_preview()
        prefix = "G(∞) + " if offset == 1.0 else ""
        if alpha is None:
            html = (
                f"<center>"
                f"G(τ) = {prefix}"
                f"<sup>1</sup>/<sub>N</sub> · "
                f"(1 + τ/τ<sub>D</sub>)<sup>−1</sup> · "
                f"(1 + τ/(κ<sup>2</sup>·τ<sub>D</sub>))<sup>−½</sup>"
                f"</center>"
            )
        else:
            html = (
                f"<center>"
                f"G(τ) = {prefix}"
                f"<sup>1</sup>/<sub>N</sub> · "
                f"[(1 + (τ/τ<sub>D</sub>)<sup>α</sup>) · "
                f"(1 + κ<sup>−2</sup>·(τ/τ<sub>D</sub>)<sup>α</sup>)<sup>½</sup>]<sup>−1</sup>"
                f"</center>"
            )
        self.fitEquationLabel.setText(html)

    def _fill_fit_results(self, idx, popt, extra_rows=None):
        """
        Write the fit result values into the "Fit result" column (index 2)
        of the merged table, aligned row-by-row with the "Initial value"
        column already shown for model ``idx`` (the table rows/labels were
        already set by ``_populate_initial_params_table`` for this same
        model).

        Any derived quantities that aren't direct curve_fit parameters
        (e.g. α2 = 1-α1, G(0) = K/N, or the fixed G(∞) offset flag) can be
        appended as additional read-only rows via ``extra_rows``.

        :param idx: Selected fit-model index.
        :param popt: Fitted parameter values, in curve_fit argument order
            (matching ``PARAM_LABELS[idx]``).
        :param extra_rows: Optional list of ``(name, formatted_value)``
            tuples for derived/fixed quantities with no editable initial
            guess.
        :return: None
        """
        if self.fitTable is None:
            return
        labels      = self.PARAM_LABELS.get(idx, self.PARAM_LABELS[0])
        extra_rows  = extra_rows or []
        table       = self.fitTable
        table.blockSignals(True)
        table.setRowCount(len(labels) + len(extra_rows))

        for row, ((name, unit, scale), value) in enumerate(zip(labels, popt)):
            item_result = QTableWidgetItem(f"{value * scale:.4f}")
            item_result.setTextAlignment(Qt.AlignCenter)
            item_result.setFlags(item_result.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, item_result)

        for i, (name, value_str) in enumerate(extra_rows):
            row = len(labels) + i
            item_name = QTableWidgetItem(name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, item_name)

            item_value = QTableWidgetItem("")
            item_value.setFlags(item_value.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 1, item_value)

            item_result = QTableWidgetItem(value_str)
            item_result.setTextAlignment(Qt.AlignCenter)
            item_result.setFlags(item_result.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, item_result)

        table.resizeRowsToContents()
        h = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            h += table.rowHeight(row)
        table.setFixedHeight(h + 4)
        table.blockSignals(False)

    def run_fit(self):
        """
        Fit the current G(τ) curve with the model selected in ``fitModelCombo``.

        The initial guess (``p0``) comes from the editable "Initial value"
        column of ``fitTable`` (``_read_initial_params``), falling back to
        the auto-computed guess for anything left blank/invalid, and is
        clipped into the model's ``curve_fit`` bounds (``_get_bounds``) so
        an out-of-range entry can't make the fit raise. On success, the
        "Fit result" column is filled in (``_fill_fit_results``), the fit
        curve is redrawn, and ``last_p0_used``/``last_fit_idx`` are recorded
        so the saved-data header can report exactly what guess produced the
        displayed result.

        :return: None
        """
        self.fitResultLabel.setVisible(False)
        self.fitResultsFrame.setVisible(False)

        if self.last_taus_s is None or len(self.last_taus_s) < 5:
            self.fitResultLabel.setText("No hay suficientes datos para ajustar.")
            self.fitResultLabel.setVisible(True)
            self.fitResultsFrame.setVisible(True)
            return

        taus = self.last_taus_s
        g    = self.last_g
        mask = (taus > 0) & np.isfinite(g)
        taus = taus[mask]
        g    = g[mask]

        offset = 1.0 if self.fitOffsetCheckBox.isChecked() else 0.0
        # Si G(∞)→0, desplazar los datos restando 1 antes de fitear
        g_fit = g if offset == 1.0 else g - 1.0

        idx    = self.fitModelCombo.currentIndex()
        bounds = self._get_bounds(idx)
        # p0 comes from the editable "Initial value" column (falling back
        # to the auto-computed guess for anything left blank/invalid),
        # clipped into the fit bounds so an out-of-range guess can't make
        # curve_fit raise.
        p0 = self._read_initial_params(idx, bounds=bounds)
        g_inf_row = ("G(∞)", "1" if offset == 1.0 else "0")

        try:
            if idx == 0:  # 3D Gaussian
                popt, _ = curve_fit(
                    lambda t, N, tD, k: self._model_3d(t, N, tD, k, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tD_fit, kappa_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[g_inf_row])
                fit_g = self._model_3d(taus, N_fit, tD_fit, kappa_fit, offset)

            elif idx == 1:  # Anomalous
                popt, _ = curve_fit(
                    lambda t, N, tD, a, k: self._model_anomalous(t, N, tD, a, k, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tD_fit, alpha_fit, kappa_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[g_inf_row])
                fit_g = self._model_anomalous(taus, N_fit, tD_fit, alpha_fit, kappa_fit, offset)

            elif idx == 2:  # Chemical
                popt, _ = curve_fit(
                    lambda t, N, tB, K: self._model_chemical(t, N, tB, K, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tB_fit, K_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[
                    ("G(0)", f"{K_fit/N_fit:.4f}"),
                    g_inf_row,
                ])
                fit_g = self._model_chemical(taus, N_fit, tB_fit, K_fit, offset)

            elif idx == 3:  # Flow
                popt, _ = curve_fit(
                    lambda t, N, tD, k, tv: self._model_flow(t, N, tD, k, tv, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tD_fit, kappa_fit, tv_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[g_inf_row])
                fit_g = self._model_flow(taus, N_fit, tD_fit, kappa_fit, tv_fit, offset)

            elif idx == 4:  # Triplet
                popt, _ = curve_fit(
                    lambda t, N, tD, k, F, tF: self._model_triplet(t, N, tD, k, F, tF, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tD_fit, kappa_fit, F_fit, tF_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[g_inf_row])
                fit_g = self._model_triplet(taus, N_fit, tD_fit, kappa_fit, F_fit, tF_fit, offset)

            elif idx == 5:  # Two-component
                popt, _ = curve_fit(
                    lambda t, N, tD1, tD2, a1, k: self._model_two_component(t, N, tD1, tD2, a1, k, offset),
                    taus, g_fit, p0=p0, bounds=bounds, maxfev=10000
                )
                N_fit, tD1_fit, tD2_fit, a1_fit, kappa_fit = popt
                self._fill_fit_results(idx, popt, extra_rows=[
                    ("α2", f"{1-a1_fit:.4f}"),
                    g_inf_row,
                ])
                fit_g = self._model_two_component(taus, N_fit, tD1_fit, tD2_fit, a1_fit, kappa_fit, offset)

            else:
                return

            # Remember the p0 actually used, for the saved-data header.
            self.last_p0_used = list(p0)
            self.last_fit_idx = idx

            self._update_equation_label_preview()
            self.fit_curve.setData(taus, fit_g)
            self.fitResultsFrame.setVisible(True)

        except RuntimeError:
            self.fitResultLabel.setText("El ajuste no convergió.")
            self.fitResultLabel.setVisible(True)
            self.fitResultsFrame.setVisible(True)
        except Exception as e:
            self.fitResultLabel.setText(f"Error en el ajuste: {e}")
            self.fitResultLabel.setVisible(True)
            self.fitResultsFrame.setVisible(True)

    def disconnectedDevice(self):
        """
        Handle a device disconnection event.

        Stops any running measurement, disables the start button, and resets
        the status indicator to grey.

        :return: None
        """
        self.withoutMeasurement = True
        if self.threadCreatedSentinel:
            self.worker.stop()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectButton.setEnabled(True)
        self.statusValue.setText("Device disconnected")
        self.changeStatusColor(0)

    def hide_graphic2(self):
        """
        Disable start and stop buttons (called on disconnect from main.py).

        :return: None
        """
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)

    def show_graphic(self, device_new):
        """
        Re-enable the start button after a reconnection.

        :param device_new: New open ``TempicoDevice`` instance.
        :return: None
        """
        self.device = device_new
        self.startButton.setEnabled(True)

    # ── Save sentinel reset (called from main.py) ─────────────────────────────

    def resetSaveSentinels(self):
        """
        Reset the per-format save sentinels.

        Called by ``MainWindow.resetSaveSentinelsAllWindows`` so the user can
        re-save data in the same format after a new measurement.

        :return: None
        """
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0