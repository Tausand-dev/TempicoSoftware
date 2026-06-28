# -*- coding: utf-8 -*-
"""G2Logic

    Orchestration layer for the g²(τ) HBT measurement tab.  Manages the
    pyqtgraph plot widget, button states, thread lifecycle, data saving, and
    status indicators.

    Architecture mirrors FCSLogic exactly:
    - Same constructor parameter order and naming conventions.
    - Same signal-slot wiring pattern (dataReady → update_plot,
      statusUpdate → changeStatusThread, colorValue → changeColorThread,
      threadCreated → threadRunning, finished → threadComplete).
    - Same tab-disable / re-enable pattern during acquisition.
    - Same _draw_status_dot / startTimerConnection / stopTimerConnection helpers.

    Color classification and "light type" labels are deliberately excluded
    per project requirements.  The plot is a step-mode bar histogram of g²(τ)
    with a dashed reference line at g² = 1.

    | @author: Miguelangel García Castillo, Tausand Electronics
    | mgarcia@tausand.com
    | https://www.tausand.com
"""

import os
import time
import datetime

import numpy as np
import pyqtgraph as pg
from PySide2.QtCore  import Qt
from PySide2.QtGui   import QPixmap, QPainter, QColor
from PySide2.QtWidgets import (
    QGridLayout, QDialog, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QTableWidgetItem,
)
from scipy.optimize import curve_fit

import pyTempico as Tempico
from Utils.createsavefile import createsavefile as savefile
from Threads.ThreadG2 import WorkerThreadG2


class G2Logic:
    """
    Orchestration layer for the g²(τ) HBT measurement tab.

    Creates and manages a single pyqtgraph ``PlotWidget`` that displays the
    normalized second-order correlation function g²(τ) in real time.
    Instantiates and controls a ``WorkerThreadG2`` during acquisition, and
    provides save (data + plot) functionality after the measurement finishes.

    Parameters
    ----------
    parent : QWidget
        The ``QFrame`` inside the G2 tab where the plot is injected
        (equivalent to ``graphicFrame`` in ``Ui_G2Measurement``).
    disconnectButton : QPushButton
        Main-window Disconnect button — disabled while measuring.
    device : Tempico.TempicoDevice
        Open Tempico device instance.
    startButton : QPushButton
        Starts the acquisition.
    stopButton : QPushButton
        Stops the acquisition.
    saveDataButton : QPushButton
        Saves the raw g²(τ) curve to a text/csv/dat file.
    savePlotButton : QPushButton
        Saves the plot as an image file.
    clearButton : QPushButton
        Clears the accumulated curve without restarting the device.
    connectButton : QPushButton
        Main-window Connect button — re-enabled when disconnected.
    mainWindow : QMainWindow
        Reference to the application's main window.
    statusValue : QLabel
        Label that shows the current acquisition status text.
    statusPoint : QLabel
        Small label used as a coloured status indicator (traffic-light dot).
    timerStatus : QTimer
        Shared timer that polls the device connection; stopped during
        measurement and restarted when idle.
    eventsLabel : QLabel
        Label that displays the total number of photon events.
    elapsedLabel : QLabel
        Label that displays the elapsed measurement time.
    g2ZeroLabel : QLabel
        Label that displays the g²(τ=0) value.
    rateStartLabel : QLabel
        Label that displays the start-channel count rate (cps).
    rateStopLabel : QLabel
        Label that displays the stop-channel count rate (cps).
    stopChannelComboBox : QComboBox
        Combo box to select which TDC channel carries the stop signal (A–D).
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
        eventsLabel,
        elapsedLabel,
        g2ZeroLabel,
        rateStartLabel,
        rateStopLabel,
        stopChannelComboBox,
        tauQuerySpinBox=None,
        g2CursorLabel=None,
        fitButton=None,
        fitModelCombo=None,
        fitEquationLabel=None,
        fitResultLabel=None,
        fitResultsFrame=None,
        fitTable=None,
    ):
        super().__init__()

        # ── Utility ──────────────────────────────────────────────────────────
        self.savefile = savefile()

        # ── Device ───────────────────────────────────────────────────────────
        self.device = device

        # ── Widget references ─────────────────────────────────────────────
        self.parent              = parent
        self.disconnectButton    = disconnectButton
        self.connectButton       = connectButton
        self.mainWindow          = mainWindow
        self.statusValue         = statusValue
        self.statusPoint         = statusPoint
        self.timerConnection     = timerStatus
        self.eventsLabel         = eventsLabel
        self.elapsedLabel        = elapsedLabel
        self.g2ZeroLabel         = g2ZeroLabel
        self.rateStartLabel      = rateStartLabel
        self.rateStopLabel       = rateStopLabel
        self.stopChannelComboBox = stopChannelComboBox

        self.startButton    = startButton
        self.stopButton     = stopButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.clearButton    = clearButton

        # ── Cursor / τ-query widgets (optional, set by main.py) ───────────
        self.tauQuerySpinBox = tauQuerySpinBox
        self.g2CursorLabel   = g2CursorLabel

        # ── Fit widgets (optional – set here or via set_fit_widgets()) ────
        self.fitButton        = fitButton
        self.fitModelCombo    = fitModelCombo
        self.fitEquationLabel = fitEquationLabel
        self.fitResultLabel   = fitResultLabel
        self.fitResultsFrame  = fitResultsFrame
        self.fitTable         = fitTable

        # Parameter widgets — injected after construction via set_parameter_widgets()
        self.binWidthSpinBox    = None
        self.windowSpinBox      = None
        self.durationSpinBox    = None
        self.indefiniteCheckBox = None

        # ── Button initial states ─────────────────────────────────────────
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(True)

        # ── Button signal connections ─────────────────────────────────────
        self.startButton.clicked.connect(self.start_graphic)
        self.stopButton.clicked.connect(self.stop_graphic)
        self.saveDataButton.clicked.connect(self.save_data)
        self.savePlotButton.clicked.connect(self.save_plot)
        self.clearButton.clicked.connect(self.clear_curve)

        # ── Fit signal connections ────────────────────────────────────────
        if self.fitButton is not None:
            self.fitButton.clicked.connect(self.run_fit)
        if self.fitModelCombo is not None:
            self.fitModelCombo.currentIndexChanged.connect(
                self._update_equation_label_preview
            )

        # ── Internal state ────────────────────────────────────────────────
        # True while the worker thread is alive
        self.threadCreatedSentinel = False
        # True once the first measurement finishes (enables Save)
        self.hasMeasurementData    = False
        # True when device disconnects mid-measurement
        self.withoutMeasurement    = False
        self.isStopping            = False

        # Save-format sentinels (prevent re-saving the same data twice)
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0

        # Last emitted g²(τ) arrays — kept so save works after stop
        self.last_centres_ns = np.array([])
        self.last_g2         = np.array([])

        # ── Build the plot ────────────────────────────────────────────────
        self._build_plot()

    # ── Plot construction ─────────────────────────────────────────────────────

    def _build_plot(self):
        """
        Create and inject the pyqtgraph plot widget into ``self.parent``.

        Sets up a linear x-axis (τ in ns, can be negative), a dashed reference
        line at g² = 1, and an empty step-mode histogram curve that will be
        updated in real time by ``update_plot``.

        :return: None
        """
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('w')
        self.plot = self.win.addPlot()

        self.plot.setTitle('Second-Order Correlation Function g\u00b2(\u03c4)')
        self.plot.setLabel('left',   'g\u00b2(\u03c4)')
        self.plot.setLabel('bottom', 'Delay \u03c4 (ns)')
        self.plot.showGrid(x=True, y=True, alpha=0.3)

        # Disable pyqtgraph's built-in "A" auto-range button.
        #
        # That button calls ViewBox.autoRange(), which fits the view to
        # childrenBoundingRect() of EVERYTHING in the plot — including the
        # decorative InfiniteLines (_cursor_line, the g²=1 reference line,
        # the τ=0 dotted line). An InfiniteLine's bounding rect is not a
        # normal data bound, and mixing it into autoRange() is what made
        # the X-axis (and therefore the visual position of the cursor
        # relative to the view) snap to an unrelated, usually far-left,
        # range instead of respecting "Window (±)". Hiding the button
        # avoids the bug entirely; the X-range is instead kept in sync
        # with windowSpinBox from main.py.
        self.plot.hideButtons()

        # Dashed reference line at g² = 1 (uncorrelated baseline)
        ref_line = pg.InfiniteLine(
            pos=1.0, angle=0,
            pen=pg.mkPen('gray', width=1, style=Qt.DashLine)
        )
        # Decorative line — must never influence autoRange()/childrenBoundingRect().
        if hasattr(ref_line, "setIgnoreBounds"):
            ref_line.setIgnoreBounds(True)
        self.plot.addItem(ref_line)

        # Fit curve – drawn after the user clicks Fit
        self.fit_curve = self.plot.plot(
            [], [],
            pen=pg.mkPen('red', width=2),
            name='Fit',
        )

        # Step-mode histogram curve.
        # stepMode=True (bool) is supported by ALL pyqtgraph versions.
        # With stepMode=True the x array must have len(y)+1 elements (the bin
        # edges).  update_plot() always builds the edges array before calling
        # setData(), so the contract is satisfied during normal operation.
        #
        # IMPORTANT: PlotCurveItem.__init__ forwards all kwargs straight to
        # setData(). If no x/y are given here, pyqtgraph defaults BOTH to
        # empty (0,) arrays -- which immediately violates the stepMode
        # len(x) == len(y)+1 contract and raises:
        #   "len(X) must be len(Y)+1 since stepMode=True (got (0,) and (0,))"
        # right here in the constructor. That is the exact crash seen when
        # pressing Start (start_graphic()'s safety net retries _build_plot(),
        # which raised the very same exception again). Passing a valid
        # 1-bin placeholder ([0, 1] / [0]) avoids the issue entirely.
        self.curve = pg.PlotCurveItem(
            x=np.array([0.0, 1.0]),
            y=np.array([0.0]),
            stepMode=True,
            fillLevel=0,
            brush=pg.mkBrush(41, 128, 185, 100),
            pen=pg.mkPen('#2980b9', width=1.5),
        )
        self.plot.addItem(self.curve)

        # ── Cursor line (vertical dashed, teal) — hidden until first click ──
        self._cursor_line = pg.InfiniteLine(
            pos=0.0, angle=90,
            pen=pg.mkPen('#16a085', width=1.8, style=Qt.DashLine),
            label='τ cursor',
            labelOpts={'color': '#16a085', 'position': 0.75},
        )
        self._cursor_line.setVisible(False)
        # Decorative line — must never influence autoRange()/childrenBoundingRect().
        if hasattr(self._cursor_line, "setIgnoreBounds"):
            self._cursor_line.setIgnoreBounds(True)
        self.plot.addItem(self._cursor_line)
        zero_line = pg.InfiniteLine(
            pos=0.0, angle=90,
            pen=pg.mkPen('gray', width=1, style=Qt.DotLine)
        )
        if hasattr(zero_line, "setIgnoreBounds"):
            zero_line.setIgnoreBounds(True)
        self.plot.addItem(zero_line)

        # Reuse the existing layout on parent if it already has one
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

    # ── Cursor widget injection (called from main.py) ────────────────────────

    def set_cursor_widgets(self, tauQuerySpinBox, g2CursorLabel):
        """
        Provide references to the τ-cursor widgets.

        Called by ``main.py`` immediately after constructing ``G2Logic``.
        Connects the spinbox signal and enables click interaction on the plot.

        :param tauQuerySpinBox: QDoubleSpinBox for manual τ entry (ns).
        :param g2CursorLabel: QLabel that shows g²(τ) at the cursor position.
        :return: None
        """
        self.tauQuerySpinBox = tauQuerySpinBox
        self.g2CursorLabel   = g2CursorLabel

        # Connect spinbox → query update
        self.tauQuerySpinBox.valueChanged.connect(self._query_tau)

        # Connect plot click → τ query
        self.plot.scene().sigMouseClicked.connect(self._on_plot_clicked)

    # ── Cursor helpers ────────────────────────────────────────────────────────

    def _on_plot_clicked(self, event):
        """
        Handle a left-click on the plot: move the cursor to the clicked τ.

        Maps the scene position to data coordinates using the ViewBox, then
        delegates to ``_query_tau`` — exactly as in Prueba7.py.

        :param event: pyqtgraph mouse-click event.
        :return: None
        """
        from PySide2.QtCore import Qt as _Qt
        if event.button() != _Qt.LeftButton:
            return
        pos = event.scenePos()
        if self.plot.sceneBoundingRect().contains(pos):
            mouse_point = self.plot.vb.mapSceneToView(pos)
            tau_clicked = mouse_point.x()
            if self.tauQuerySpinBox is not None:
                self.tauQuerySpinBox.blockSignals(True)
                self.tauQuerySpinBox.setValue(tau_clicked)
                self.tauQuerySpinBox.blockSignals(False)
            self._query_tau(tau_clicked)

    def _query_tau(self, tau_val=None):
        """
        Update the g²(τ) cursor label and move the cursor line to ``tau_val``.

        Finds the histogram bin whose centre is closest to ``tau_val``, reads
        its g² value, updates ``g2CursorLabel``, and repositions
        ``_cursor_line``.  Mirrors ``HBTWindow._query_tau`` from Prueba7.py.

        :param tau_val: Lag time in nanoseconds to query.  If None, reads the
            current value of ``tauQuerySpinBox``.
        :return: None
        """
        if tau_val is None:
            if self.tauQuerySpinBox is not None:
                tau_val = self.tauQuerySpinBox.value()
            else:
                return

        if len(self.last_centres_ns) == 0 or len(self.last_g2) == 0:
            if self.g2CursorLabel is not None:
                self.g2CursorLabel.setText("— (no data)")
            return

        idx      = int(np.argmin(np.abs(self.last_centres_ns - tau_val)))
        tau_real = float(self.last_centres_ns[idx])
        g2_val   = float(self.last_g2[idx])

        if self.g2CursorLabel is not None:
            self.g2CursorLabel.setText(
                f"{g2_val:.4f}  @  τ = {tau_real:.3f} ns"
            )

        # Move cursor line to the real bin centre
        self._cursor_line.setValue(tau_real)
        self._cursor_line.setVisible(True)

        # Snap the spinbox to the nearest bin centre to avoid ambiguity
        if self.tauQuerySpinBox is not None:
            self.tauQuerySpinBox.blockSignals(True)
            self.tauQuerySpinBox.setValue(tau_real)
            self.tauQuerySpinBox.blockSignals(False)

    # ── Fit widget injection (called from main.py) ───────────────────────────

    def set_fit_widgets(
        self,
        fitButton,
        fitModelCombo,
        fitEquationLabel,
        fitResultLabel,
        fitResultsFrame,
        fitTable,
    ):
        """
        Provide references to the fit widgets from ``Ui_G2``.

        Called by ``main.py`` after constructing ``G2Logic``.
        Connects the fit button and model-combo signals.

        :return: None
        """
        self.fitButton        = fitButton
        self.fitModelCombo    = fitModelCombo
        self.fitEquationLabel = fitEquationLabel
        self.fitResultLabel   = fitResultLabel
        self.fitResultsFrame  = fitResultsFrame
        self.fitTable         = fitTable

        self.fitButton.clicked.connect(self.run_fit)
        self.fitModelCombo.currentIndexChanged.connect(
            self._update_equation_label_preview
        )

    # ── Parameter widget injection (called from main.py) ─────────────────────

    def set_parameter_widgets(
        self,
        binWidthSpinBox,
        windowSpinBox,
        durationSpinBox,
        indefiniteCheckBox,
    ):
        """
        Provide references to the parameter widgets.

        Called by ``main.py`` immediately after constructing ``G2Logic`` so
        that ``start_graphic`` can read the user-configured values at the
        moment the measurement starts — not at construction time.

        :param binWidthSpinBox: QDoubleSpinBox with bin width in ns.
        :param windowSpinBox: QSpinBox with half-window in ns.
        :param durationSpinBox: QSpinBox with duration in seconds.
        :param indefiniteCheckBox: QCheckBox; when checked the measurement runs
            until the user presses Stop.
        :return: None
        """
        self.binWidthSpinBox    = binWidthSpinBox
        self.windowSpinBox      = windowSpinBox
        self.durationSpinBox    = durationSpinBox
        self.indefiniteCheckBox = indefiniteCheckBox

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_stop_channel_index(self) -> int:
        """Return 1–4 for the selected stop channel."""
        return self.stopChannelComboBox.currentIndex() + 1

    def _restore_buttons_after_stop(self):
        """Re-enable UI controls after a failed or aborted start."""
        self.mainWindow.tabs.setTabEnabled(0, True)
        self.mainWindow.tabs.setTabEnabled(1, True)
        self.mainWindow.tabs.setTabEnabled(2, True)
        self.mainWindow.tabs.setTabEnabled(3, True)
        self.mainWindow.tabs.setTabEnabled(4, True)
        if self.binWidthSpinBox is not None:
            self.binWidthSpinBox.setEnabled(True)
        if self.windowSpinBox is not None:
            self.windowSpinBox.setEnabled(True)
        if self.durationSpinBox is not None:
            self.durationSpinBox.setEnabled(True)
        if self.indefiniteCheckBox is not None:
            self.indefiniteCheckBox.setEnabled(True)
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
        Start the g²(τ) acquisition.

        Resets the curve, disables controls that must not be used during
        measurement, stops the connection-polling timer, notifies the main
        window, and launches the ``WorkerThreadG2``.

        :return: None
        """
        if self.device is None:
            return

        # Safety net: if _build_plot() failed silently during __init__
        # (e.g. pyqtgraph raised an exception), retry it now before we
        # try to call self.curve.setData().
        if not hasattr(self, 'curve'):
            self._build_plot()
        if not hasattr(self, 'curve'):
            # Plot still could not be built — abort gracefully.
            return

        # Reset save sentinels so new data can be saved after this run
        self.sentinelsavetxt    = 0
        self.sentinelsavecsv    = 0
        self.sentinelsavedat    = 0
        self.hasMeasurementData = False
        self.isStopping         = False
        self.last_centres_ns    = np.array([])
        self.last_g2            = np.array([])

        # Clear the curve visually.
        # With stepMode=True, pyqtgraph requires len(x) == len(y)+1.
        # Passing a single zero-height bin is the safest cross-version reset.
        self.curve.setData([0, 1], [0])

        # Disable other tabs while measuring (mirrors FCSLogic)
        self.mainWindow.tabs.setTabEnabled(0, False)   # Start-stop tab
        self.mainWindow.tabs.setTabEnabled(1, False)   # Counts tab
        self.mainWindow.tabs.setTabEnabled(2, False)   # Time stamp tab
        self.mainWindow.tabs.setTabEnabled(3, False)   # Lifetime tab
        self.mainWindow.tabs.setTabEnabled(4, False)   # FCS tab
        self.disconnectButton.setEnabled(False)

        # Button states during measurement
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(False)

        # Disable parameter widgets while running
        if self.binWidthSpinBox is not None:
            self.binWidthSpinBox.setEnabled(False)
        if self.windowSpinBox is not None:
            self.windowSpinBox.setEnabled(False)
        if self.durationSpinBox is not None:
            self.durationSpinBox.setEnabled(False)
        if self.indefiniteCheckBox is not None:
            self.indefiniteCheckBox.setEnabled(False)

        self.statusValue.setText("Measurement running")
        self.changeStatusColor(1)

        # Reset stats display
        self.eventsLabel.setText("0")
        self.elapsedLabel.setText("0 s")
        self.g2ZeroLabel.setText("—")
        self.rateStartLabel.setText("—")
        self.rateStopLabel.setText("—")

        # Stop the connection-polling timer while the thread owns the device
        self.stopTimerConnection()

        # ── Read parameters ───────────────────────────────────────────────
        bin_ns    = self.binWidthSpinBox.value()  if self.binWidthSpinBox is not None else 2.0
        window_ns = self.windowSpinBox.value()    if self.windowSpinBox   is not None else 200.0

        total_seconds = None
        if (self.indefiniteCheckBox is not None
                and not self.indefiniteCheckBox.isChecked()
                and self.durationSpinBox is not None):
            total_seconds = self.durationSpinBox.value()

        stop_ch = self._get_stop_channel_index()

        self.mainWindow.saveSettings()
        self.mainWindow.activeMeasurement()

        self.worker = WorkerThreadG2(
            parent        = self.parent,
            device        = self.device,
            stop_channel  = stop_ch,
            bin_ns        = bin_ns,
            window_ns     = window_ns,
            total_seconds = total_seconds,
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
        if not self.withoutMeasurement:
            self.startTimerConnection()

        if self.threadCreatedSentinel:
            self.worker.stop()

        self.statusValue.setText("No measurement running")
        self.changeStatusColor(0)

        # Re-enable all tabs
        for i in range(6):
            self.mainWindow.tabs.setTabEnabled(i, True)

        self.disconnectButton.setEnabled(True)
        self.mainWindow.noMeasurement()

        self.stopButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(True)

        # Re-enable parameter widgets
        if self.binWidthSpinBox is not None:
            self.binWidthSpinBox.setEnabled(True)
        if self.windowSpinBox is not None:
            self.windowSpinBox.setEnabled(True)
        if self.durationSpinBox is not None:
            self.durationSpinBox.setEnabled(True)
        if self.indefiniteCheckBox is not None:
            self.indefiniteCheckBox.setEnabled(True)

        if not self.withoutMeasurement:
            self.startButton.setEnabled(True)

        if self.hasMeasurementData:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
            self.clearButton.setEnabled(True)
            if self.fitButton is not None:
                self.fitButton.setEnabled(True)

    # ── Thread signal handlers ─────────────────────────────────────────────────

    def threadRunning(self, status: int):
        """
        Update ``threadCreatedSentinel`` from the ``threadCreated`` signal.

        :param status: 0 → thread just started; 1 → thread just stopped.
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

    def update_plot(
        self,
        centres_ns,
        g2,
        total_events: int,
        rate_s: float,
        rate_p: float,
    ):
        """
        Update the g²(τ) step-histogram with the latest correlation data.

        Also refreshes the g²(0), rate, and event-count stat labels.
        Does NOT apply any color-coding or light-type classification.

        :param centres_ns: Bin-centre positions in nanoseconds (ndarray).
        :param g2: Normalized g²(τ) values (ndarray).
        :param total_events: Total photon events accumulated so far.
        :param rate_s: Start-channel count rate in counts per second.
        :param rate_p: Stop-channel count rate in counts per second.
        :return: None
        """
        centres_ns = np.asarray(centres_ns, dtype=np.float64)
        g2         = np.asarray(g2,         dtype=np.float64)

        if len(centres_ns) == 0 or len(g2) == 0:
            return

        # Build bin edges from centres.
        # With stepMode=True, setData expects n+1 edge values for n y values.
        # edges[i] is the left boundary of bin i; edges[n] is the right boundary
        # of the last bin.  This is exactly n+1 values for n bins.
        if len(centres_ns) > 1:
            bin_ns = float(centres_ns[1] - centres_ns[0])
        else:
            bin_ns = 1.0
        edges = np.concatenate(
            [[centres_ns[0] - bin_ns / 2.0],
              centres_ns + bin_ns / 2.0]
        )
        self.curve.setData(edges, g2)

        # Cache for saving
        self.last_centres_ns = centres_ns
        self.last_g2         = g2
        self.hasMeasurementData = True

        # Refresh cursor value with the latest data
        self._query_tau()

        # Update stats labels
        self.eventsLabel.setText(f"{total_events:,}")
        self.rateStartLabel.setText(f"{rate_s:,.0f} cps")
        self.rateStopLabel.setText(f"{rate_p:,.0f} cps")

        # g²(0): value in the bin whose centre is closest to τ = 0
        if len(centres_ns) > 0:
            z_idx   = int(np.argmin(np.abs(centres_ns)))
            g2_zero = float(g2[z_idx])
            self.g2ZeroLabel.setText(f"{g2_zero:.4f}")

        # Adjust Y-axis range with a small margin
        if len(g2) > 0:
            g2_max = max(float(np.nanmax(g2)) * 1.15, 1.5)
            self.plot.setYRange(0, g2_max)

    def changeStatusThread(self, new_text: str):
        """
        Update the status label and elapsed/events counters from a thread signal.

        Parses strings of the form ``"events: N | elapsed: T s"``
        or ``"events: N | elapsed: T s / D s"`` emitted by ``WorkerThreadG2``.

        :param new_text: Text to parse (str).
        :return: None
        """
        if self.isStopping:
            return
        self.statusValue.setText("Measurement running")
        try:
            parts = new_text.split("|")
            events_part  = parts[0].split(":")[1].strip()
            elapsed_part = parts[1].split(":")[1].strip()
            self.eventsLabel.setText(events_part.replace(",", ""))
            self.elapsedLabel.setText(elapsed_part)
        except (IndexError, AttributeError):
            self.statusValue.setText(new_text)

    def changeColorThread(self, color: int):
        """
        Update the status-indicator dot colour from a thread signal.

        Colour codes: 0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    # ── Clear ─────────────────────────────────────────────────────────────────

    def clear_curve(self):
        """
        Clear the g²(τ) curve and cached data without stopping the device.

        :return: None
        """
        self.last_centres_ns    = np.array([])
        self.last_g2            = np.array([])
        self.hasMeasurementData = False
        self.curve.setData([0, 1], [0])
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.g2ZeroLabel.setText("—")
        self.rateStartLabel.setText("—")
        self.rateStopLabel.setText("—")
        self.eventsLabel.setText("0")
        self.elapsedLabel.setText("0 s")
        # Reset cursor
        self._cursor_line.setVisible(False)
        if self.g2CursorLabel is not None:
            self.g2CursorLabel.setText("—")
        # Reset fit
        self.fit_curve.setData([], [])
        if self.fitResultsFrame is not None:
            self.fitResultsFrame.setVisible(False)
        if self.fitButton is not None:
            self.fitButton.setEnabled(False)

    # ── Fit logic ─────────────────────────────────────────────────────────────

    @staticmethod
    def _model_antibunched_gaussian(tau, y0, V, tau0, sigma):
        """g2(τ) = y₀ − V·exp(−(τ−τ₀)²/(2σ²))"""
        return y0 - V * np.exp(-((tau - tau0) ** 2) / (2.0 * sigma ** 2))

    @staticmethod
    def _model_antibunched_lorentzian(tau, y0, V, tau0, Gamma):
        """g2(τ) = y₀ − V·(Γ/2)²/((τ−τ₀)²+(Γ/2)²)"""
        half = Gamma / 2.0
        return y0 - V * half ** 2 / ((tau - tau0) ** 2 + half ** 2)

    @staticmethod
    def _model_bunched_gaussian(tau, y0, alpha, tau0, tau_c):
        """g2(τ) = y₀ + α·exp(−π·(|τ−τ₀|/τ_c)²)"""
        return y0 + alpha * np.exp(-np.pi * (np.abs(tau - tau0) / tau_c) ** 2)

    @staticmethod
    def _model_bunched_lorentzian(tau, y0, alpha, tau0, tau_c):
        """g2(τ) = y₀ + α·exp(−2·|τ−τ₀|/τ_c)"""
        return y0 + alpha * np.exp(-2.0 * np.abs(tau - tau0) / tau_c)

    @staticmethod
    def _model_three_level(tau, a, tau0, tau1, tau2):
        """g2(τ) = 1 − (1+a)·exp(−|τ−τ₀|/τ₁) + a·exp(−|τ−τ₀|/τ₂)"""
        dt = np.abs(tau - tau0)
        return 1.0 - (1.0 + a) * np.exp(-dt / tau1) + a * np.exp(-dt / tau2)

    def _update_equation_label_preview(self):
        """Show the equation for the currently selected model."""
        if self.fitEquationLabel is None or self.fitModelCombo is None:
            return
        idx = self.fitModelCombo.currentIndex()
        eqs = [
            # 0 Antibunched Gaussian
            u"<center>g²(τ) = y<sub>0</sub> − V · exp(−(τ−τ<sub>0</sub>)²/(2σ²))</center>",
            # 1 Antibunched Lorentzian
            u"<center>g²(τ) = y<sub>0</sub> − V · (Γ/2)² / ((τ−τ<sub>0</sub>)² + (Γ/2)²)</center>",
            # 2 Bunched Gaussian
            u"<center>g²(τ) = y<sub>0</sub> + α · exp(−π·(|τ−τ<sub>0</sub>|/τ<sub>c</sub>)²)</center>",
            # 3 Bunched Lorentzian
            u"<center>g²(τ) = y<sub>0</sub> + α · exp(−2·|τ−τ<sub>0</sub>|/τ<sub>c</sub>)</center>",
            # 4 Three-level system
            u"<center>g²(τ) = 1 − (1+a)·exp(−|τ−τ<sub>0</sub>|/τ<sub>1</sub>) + a·exp(−|τ−τ<sub>0</sub>|/τ<sub>2</sub>)</center>",
        ]
        self.fitEquationLabel.setText(eqs[idx] if idx < len(eqs) else "")
        if self.fitResultsFrame is not None:
            self.fitResultsFrame.setVisible(True)

    def _fill_fit_table(self, rows):
        """Fill fitTable with (name, value) rows."""
        table = self.fitTable
        table.setRowCount(len(rows))
        for i, (name, value) in enumerate(rows):
            item_name  = QTableWidgetItem(name)
            item_value = QTableWidgetItem(value)
            item_name.setTextAlignment(Qt.AlignCenter)
            item_value.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 0, item_name)
            table.setItem(i, 1, item_value)
        table.resizeRowsToContents()
        h = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            h += table.rowHeight(row)
        table.setFixedHeight(h + 4)

    def _get_fit_header_lines(self):
        """Return fit result lines for the save header, or empty string."""
        if self.fitResultsFrame is None or not self.fitResultsFrame.isVisible():
            return ""
        if self.fitModelCombo is None:
            return ""

        idx = self.fitModelCombo.currentIndex()
        model_names = {
            0: "Antibunched Gaussian",
            1: "Antibunched Lorentzian",
            2: "Bunched Gaussian",
            3: "Bunched Lorentzian",
            4: "Three-level system",
        }
        equations = {
            0: "y0 - V*exp(-(tau-tau0)^2/(2*sigma^2))",
            1: "y0 - V*(Gamma/2)^2/((tau-tau0)^2+(Gamma/2)^2)",
            2: "y0 + alpha*exp(-pi*(|tau-tau0|/tau_c)^2)",
            3: "y0 + alpha*exp(-2*|tau-tau0|/tau_c)",
            4: "1-(1+a)*exp(-|tau-tau0|/tau1)+a*exp(-|tau-tau0|/tau2)",
        }
        lines = [
            f"Fit model:\t{model_names.get(idx, 'Unknown')}",
            f"Fit equation:\t{equations.get(idx, '')}",
        ]
        if self.fitTable is not None:
            for row in range(self.fitTable.rowCount()):
                n = self.fitTable.item(row, 0)
                v = self.fitTable.item(row, 1)
                if n and v:
                    lines.append(f"{n.text()}:\t{v.text()}")
        return "\n".join(lines)

    def run_fit(self):
        """Fit the current g²(τ) histogram with the selected model."""
        if self.fitResultLabel is not None:
            self.fitResultLabel.setVisible(False)
        if self.fitResultsFrame is not None:
            self.fitResultsFrame.setVisible(False)

        if self.last_centres_ns is None or len(self.last_centres_ns) < 5:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText("Not enough data to fit.")
                self.fitResultLabel.setVisible(True)
            if self.fitResultsFrame is not None:
                self.fitResultsFrame.setVisible(True)
            return

        tau  = self.last_centres_ns.copy()
        g2   = self.last_g2.copy()
        mask = np.isfinite(g2)
        tau  = tau[mask]
        g2   = g2[mask]

        idx       = self.fitModelCombo.currentIndex() if self.fitModelCombo else 0
        hw        = float(np.max(np.abs(tau))) if len(tau) > 0 else 200.0
        tau_scale = hw / 4.0

        try:
            if idx == 0:  # Antibunched Gaussian
                p0     = [1.0, 0.5, 0.0, tau_scale]
                bounds = ([0, 0, -hw, 0.01], [np.inf, np.inf, hw, np.inf])
                popt, _ = curve_fit(self._model_antibunched_gaussian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                y0, V, tau0, sigma = popt
                self._fill_fit_table([
                    ("y₀",    f"{y0:.4f}"),
                    ("V",     f"{V:.4f}"),
                    ("τ₀",    f"{tau0:.4f} ns"),
                    ("σ",     f"{sigma:.4f} ns"),
                ])
                fit_g2 = self._model_antibunched_gaussian(tau, *popt)

            elif idx == 1:  # Antibunched Lorentzian
                p0     = [float(np.max(g2)), 0.5, 0.0, tau_scale]
                bounds = ([0, 0, -hw, 0.01], [np.inf, np.inf, hw, np.inf])
                popt, _ = curve_fit(self._model_antibunched_lorentzian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                y0, V, tau0, Gamma = popt
                self._fill_fit_table([
                    ("y₀",    f"{y0:.4f}"),
                    ("V",     f"{V:.4f}"),
                    ("τ₀",    f"{tau0:.4f} ns"),
                    ("Γ",     f"{Gamma:.4f} ns"),
                ])
                fit_g2 = self._model_antibunched_lorentzian(tau, *popt)

            elif idx == 2:  # Bunched Gaussian
                p0     = [1.0, 0.5, 0.0, tau_scale]
                bounds = ([0, 0, -hw, 0.01], [np.inf, np.inf, hw, np.inf])
                popt, _ = curve_fit(self._model_bunched_gaussian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                y0, alpha, tau0, tau_c = popt
                self._fill_fit_table([
                    ("y₀",    f"{y0:.4f}"),
                    ("α",     f"{alpha:.4f}"),
                    ("τ₀",    f"{tau0:.4f} ns"),
                    ("τ_c",   f"{tau_c:.4f} ns"),
                ])
                fit_g2 = self._model_bunched_gaussian(tau, *popt)

            elif idx == 3:  # Bunched Lorentzian
                p0     = [1.0, 0.5, 0.0, tau_scale]
                bounds = ([0, 0, -hw, 0.01], [np.inf, np.inf, hw, np.inf])
                popt, _ = curve_fit(self._model_bunched_lorentzian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                y0, alpha, tau0, tau_c = popt
                self._fill_fit_table([
                    ("y₀",    f"{y0:.4f}"),
                    ("α",     f"{alpha:.4f}"),
                    ("τ₀",    f"{tau0:.4f} ns"),
                    ("τ_c",   f"{tau_c:.4f} ns"),
                ])
                fit_g2 = self._model_bunched_lorentzian(tau, *popt)

            elif idx == 4:  # Three-level system
                p0     = [0.5, 0.0, tau_scale * 0.5, tau_scale * 2.0]
                bounds = ([0, -hw, 0.01, 0.01], [np.inf, hw, np.inf, np.inf])
                popt, _ = curve_fit(self._model_three_level,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                a, tau0, tau1, tau2 = popt
                self._fill_fit_table([
                    ("a",     f"{a:.4f}"),
                    ("τ₀",   f"{tau0:.4f} ns"),
                    ("τ₁",   f"{tau1:.4f} ns"),
                    ("τ₂",   f"{tau2:.4f} ns"),
                ])
                fit_g2 = self._model_three_level(tau, *popt)

            else:
                return

            self._update_equation_label_preview()
            self.fit_curve.setData(tau, fit_g2)
            if self.fitResultsFrame is not None:
                self.fitResultsFrame.setVisible(True)

        except RuntimeError:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText("Fit did not converge.")
                self.fitResultLabel.setVisible(True)
            if self.fitResultsFrame is not None:
                self.fitResultsFrame.setVisible(True)
        except Exception as e:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText(f"Fit error: {e}")
                self.fitResultLabel.setVisible(True)
            if self.fitResultsFrame is not None:
                self.fitResultsFrame.setVisible(True)

    # ── Save data ─────────────────────────────────────────────────────────────

    def save_data(self):
        """
        Save the current g²(τ) curve to a text file.

        Opens a format-selection dialog (txt / csv / dat) and writes two
        columns: τ (ns) and g²(τ).  The header records the measurement
        parameters (bin width, window, TDC mode, stop channel).

        :return: None
        """
        if len(self.last_centres_ns) == 0:
            return

        dataFolderPrefix = self.savefile.getDataFolderPrefix()
        folder_path      = dataFolderPrefix["saveFolder"]
        current_date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        ch_names  = ["A", "B", "C", "D"]
        ch_index  = self.stopChannelComboBox.currentIndex()
        ch_label  = ch_names[ch_index] if ch_index < len(ch_names) else "A"

        # Format selection dialog (same structure as FCSLogic)
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Save")
        vlay = QVBoxLayout(dialog)
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

        # Gather parameter values for the header
        bin_ns_val    = (self.binWidthSpinBox.value()
                         if self.binWidthSpinBox is not None else "—")
        window_ns_val = (self.windowSpinBox.value()
                         if self.windowSpinBox   is not None else "—")

        setting = (
            f"Bin width (ns):\t{bin_ns_val}\n"
            f"Window (ns):\t{window_ns_val}\n"
            f"Stop channel:\tChannel {ch_label}"
        )

        fit_header = self._get_fit_header_lines()
        if fit_header:
            setting += "\n" + fit_header

        prefix    = dataFolderPrefix.get("g2Prefix", "G2")
        filename  = f"{prefix}_{current_date_str}_Channel{ch_label}"
        sep       = ";" if selected_format == "csv" else "\t"

        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            full_path = os.path.join(folder_path, f"{filename}.{selected_format}")
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(setting + '\n')
                f.write(f"tau_ns{sep}g2\n")
                for t, g in zip(self.last_centres_ns, self.last_g2):
                    f.write(f"{t}{sep}{g}\n")

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"File saved successfully:\n\n"
                f"{folder_path}\n\n"
                f"File: {filename}.{selected_format}"
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
        Save the g²(τ) plot as an image file (png / tiff / jpg).

        Opens a format-selection dialog and exports the current pyqtgraph plot
        using ``pg.exporters.ImageExporter``.

        :return: None
        """
        try:
            dataFolderPrefix = self.savefile.getDataFolderPrefix()
            folder_path      = dataFolderPrefix["saveFolder"]

            dialog = QDialog(self.parent)
            dialog.setWindowTitle("Save plot")
            vlay = QVBoxLayout(dialog)
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

            ch_names  = ["A", "B", "C", "D"]
            ch_index  = self.stopChannelComboBox.currentIndex()
            ch_label  = ch_names[ch_index] if ch_index < len(ch_names) else "A"

            prefix   = dataFolderPrefix.get("g2Prefix", "G2")
            filename = f"{prefix}_{current_date_str}_Channel{ch_label}"

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

    def changeStatusColor(self, color: int):
        """
        Set the status-indicator dot colour from Logic-layer code.

        Colour codes: 0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    def _draw_status_dot(self, color: int):
        """
        Draw a filled circle on ``statusPoint`` with the given colour.

        Internal helper shared by ``changeStatusColor`` and
        ``changeColorThread`` to avoid code duplication.  Mirrors
        ``FCSLogic._draw_status_dot`` exactly.

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
        Stop the device-connection polling timer.

        Called at the start of a measurement so the timer does not interfere
        with the worker thread's device access.

        :return: None
        """
        if self.timerConnection is not None:
            self.timerConnection.stop()

    def startTimerConnection(self):
        """
        Start the device-connection polling timer with a 500 ms interval.

        Called when the measurement finishes or is stopped.

        :return: None
        """
        if self.timerConnection is not None:
            self.timerConnection.start(500)

    # ── Device connection lifecycle (called from main.py) ─────────────────────

    def disconnectedDevice(self):
        """
        Handle a device disconnection event.

        Stops any running measurement, disables the Start button, and resets
        the status indicator to grey.  Mirrors ``FCSLogic.disconnectedDevice``.

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
        Disable Start and Stop buttons (called on disconnect from main.py).

        :return: None
        """
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)

    def connectedDevice(self, device_new):
        """
        Re-enable the Start button after a reconnection.

        Mirrors ``FCSLogic.show_graphic`` in purpose; named ``connectedDevice``
        to match the calling convention already in use in main.py for all
        other Logic classes.

        :param device_new: New open ``TempicoDevice`` instance.
        :return: None
        """
        self.device = device_new
        self.withoutMeasurement = False
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