# -*- coding: utf-8 -*-

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
    rateStopStopLabel : QLabel
        Label that displays the Rate (stop-stop), i.e. 1 / mean(delta_stop)
        computed from the time between one stop and the next (cps).
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
        rateStopStopLabel,
        stopChannelComboBox,
        tauQuerySpinBox=None,
        g2CursorLabel=None,
        fitButton=None,
        fitModelCombo=None,
        fitEquationLabel=None,
        fitResultLabel=None,
        fitResultsFrame=None,
        fitTable=None,
        fitResetParamsButton=None,
    ):
        """
        Initializes the g²(τ) logic layer and wires up the tab's widgets.

        Stores references to the device and every widget used by the G2 tab
        (start/stop/save/clear buttons, status labels, live-count labels,
        cursor/τ-query widgets, and the optional fitting controls), sets the
        initial enabled/disabled state of each button, and connects each
        control's signal to its corresponding handler. Fit-related widgets
        (``fitButton``, ``fitModelCombo``, etc.) may be provided here or set
        later via ``set_fit_widgets``; cursor widgets may likewise be set
        later via ``set_cursor_widgets``.

        :param parent: The ``QFrame`` where the pyqtgraph plot is injected.
        :param disconnectButton: Main-window Disconnect button.
        :param device: Open ``Tempico.TempicoDevice`` instance.
        :param startButton: Button that starts the acquisition.
        :param stopButton: Button that stops the acquisition.
        :param saveDataButton: Button that saves the g²(τ) data.
        :param savePlotButton: Button that saves the plot image.
        :param clearButton: Button that clears the accumulated curve.
        :param connectButton: Main-window Connect button.
        :param mainWindow: Reference to the application's main window.
        :param statusValue: Label showing the current status text.
        :param statusPoint: Label used as a coloured status dot.
        :param timerStatus: Shared connection-polling timer.
        :param eventsLabel: Label showing the total number of photon events.
        :param elapsedLabel: Label showing the elapsed measurement time.
        :param g2ZeroLabel: Label showing the g²(τ=0) value.
        :param rateStopStopLabel: Label showing the Rate (stop-stop), i.e.
            1 / mean(delta_stop) computed from the time between one stop
            and the next.
        :param stopChannelComboBox: Combo box to select the stop channel.
        :param tauQuerySpinBox: Optional spin box to query g²(τ) at a
            specific τ value.
        :param g2CursorLabel: Optional label showing g²(τ) at the queried τ.
        :param fitButton: Optional button that runs the correlation curve fit.
        :param fitModelCombo: Optional combo box to select the fit model.
        :param fitEquationLabel: Optional label displaying the fit equation.
        :param fitResultLabel: Optional label displaying the fit result summary.
        :param fitResultsFrame: Optional frame containing the fit results widgets.
        :param fitTable: Optional table widget showing fitted parameter values.
        :param fitResetParamsButton: Optional button to reset fit parameters.
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
        self.rateStopStopLabel  = rateStopStopLabel
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
        self.fitResetParamsButton  = fitResetParamsButton

        # Cache of user-edited initial guesses, keyed by fit-model index, so
        # switching models back and forth doesn't lose what was typed in.
        self._initial_params_cache = {}
        # Records the p0 actually used / model index for the last successful
        # fit, so it can be included in the saved-data header for
        # reproducibility.
        self.last_p0_used = None
        self.last_fit_idx = None

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
        # Show sensible starting guesses and the equation right away (model index 0)
        self._populate_initial_params_table()
        self._update_equation_label_preview()

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

        # Re-enable pyqtgraph's built-in "A" auto-range button.
        #
        # It was previously hidden because ViewBox.autoRange() fits the
        # view to childrenBoundingRect() of EVERYTHING added to the plot —
        # including the decorative InfiniteLines (the g²=1 reference line,
        # the τ=0 dotted line, and _cursor_line). The earlier attempt to
        # exclude them called ``item.setIgnoreBounds(True)``, but stock
        # pyqtgraph's InfiniteLine has no such method — the ``hasattr``
        # guard silently no-op'd, so those lines were still included, and
        # that's what made the range (and therefore the cursor's apparent
        # position within the view) jump around.
        #
        # The correct way to exclude an item from auto-range is to tell
        # the ViewBox at the moment it's added, via the ``ignoreBounds``
        # keyword on ``addItem()`` (see below). With that actually applied,
        # autoRange() only ever measures the real histogram/fit curves, so
        # pressing "A" now gives a sane fit and never moves the τ cursor
        # line off its real bin position.
        self.plot.showButtons()

        # Even with the cursor line excluded from the fit above, clicking
        # "A" still rescales the x/y axes to whatever the histogram/fit
        # curves currently span. Since the cursor's on-screen spot depends
        # on the axis range, that rescale reads as "the cursor jumped
        # left" — and if it happens repeatedly (e.g. during a running
        # measurement, as the histogram keeps growing) it looks like it
        # keeps drifting further left each time it's pressed.
        #
        # Rather than leave that side-effect unpredictable, make it
        # deterministic: every "A" click also snaps the τ cursor back to
        # 0 ns, exactly like changing "Window (±)" already does (see
        # ``_sync_tau_cursor_range`` in ui_g2measurement.py). The cursor
        # never ends up somewhere arbitrary; it always lands on tau_0 = 0.
        self.plot.autoBtn.clicked.connect(self._on_autorange_clicked)

        # Dashed reference line at g² = 1 (uncorrelated baseline)
        ref_line = pg.InfiniteLine(
            pos=1.0, angle=0,
            pen=pg.mkPen('gray', width=1, style=Qt.DashLine)
        )
        # Decorative line — excluded from autoRange()/childrenBoundingRect()
        # via ignoreBounds, not the (non-existent) setIgnoreBounds() method.
        self.plot.addItem(ref_line, ignoreBounds=True)

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
        # Decorative line — excluded from autoRange()/childrenBoundingRect()
        # via ignoreBounds, so pressing "A" never repositions the cursor.
        self.plot.addItem(self._cursor_line, ignoreBounds=True)
        zero_line = pg.InfiniteLine(
            pos=0.0, angle=90,
            pen=pg.mkPen('gray', width=1, style=Qt.DotLine)
        )
        self.plot.addItem(zero_line, ignoreBounds=True)

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

        # Wire up the bin-by-bin stepping hook (see the ``stepBy`` override
        # in ``Ui_G2.setupUi``). Clicking the spinbox's up/down arrows, or
        # pressing the Up/Down keys while it has focus, now calls
        # ``_step_tau_by_bin`` instead of Qt's default fixed-increment step.
        self.tauQuerySpinBox._on_tau_step = self._step_tau_by_bin

        # Connect plot click → τ query
        self.plot.scene().sigMouseClicked.connect(self._on_plot_clicked)

    # ── Cursor helpers ────────────────────────────────────────────────────────

    def _on_autorange_clicked(self, *_args):
        """
        Handle a click on pyqtgraph's built-in auto-range "A" button.

        The button's own default handler (connected by pyqtgraph itself)
        rescales the plot's axes to fit the histogram/fit curves. That
        rescale doesn't change the τ cursor's underlying value, but it
        does change where the cursor line *appears* relative to the new
        axes — which looks like the cursor jumping to the left, and can
        look like it keeps drifting further left with repeated clicks.

        To make this predictable, every "A" click also snaps the τ
        cursor back to 0 ns (same behaviour already used when "Window
        (±)" changes, in ``ui_g2measurement.py``'s
        ``_sync_tau_cursor_range``), so the cursor always lands on a
        known reference point instead of an arbitrary spot.

        :param _args: Ignored. pyqtgraph's ButtonItem.clicked emits the
            button instance itself; this handler doesn't need it.
        :return: None
        """
        if self.tauQuerySpinBox is not None:
            self.tauQuerySpinBox.blockSignals(True)
            self.tauQuerySpinBox.setValue(0.0)
            self.tauQuerySpinBox.blockSignals(False)
        self._query_tau(0.0)

    def _step_tau_by_bin(self, steps):
        """
        Move the τ cursor to the next/previous histogram bin.

        Called from the ``stepBy`` override installed on ``tauQuerySpinBox``
        (see ``Ui_G2.setupUi``) whenever the spinbox's up/down arrows are
        clicked or the Up/Down keys are pressed while it has focus.

        Finds the bin closest to the spinbox's current value, then moves
        ``steps`` bins away from it (``steps`` is positive for "up" /
        higher τ, negative for "down" / lower τ — this is exactly what Qt
        passes into ``stepBy``). The move is clamped to stay within the
        available bin range, and the usual ``_query_tau`` update (g² label,
        cursor line, spinbox value) is triggered so everything stays in
        sync — exactly as if the user had clicked that bin directly.

        :param steps: Number of bins to move; positive = next bin(s)
            (increasing τ), negative = previous bin(s) (decreasing τ).
        :return: None
        """
        if len(self.last_centres_ns) == 0 or self.tauQuerySpinBox is None:
            return

        current  = self.tauQuerySpinBox.value()
        idx      = int(np.argmin(np.abs(self.last_centres_ns - current)))
        new_idx  = idx + int(steps)
        new_idx  = max(0, min(new_idx, len(self.last_centres_ns) - 1))
        tau_next = float(self.last_centres_ns[new_idx])

        self._query_tau(tau_next)

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
        fitResetParamsButton=None,
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
        self.fitResetParamsButton  = fitResetParamsButton

        self.fitButton.clicked.connect(self.run_fit)
        self.fitModelCombo.currentIndexChanged.connect(
            self._update_equation_label_preview
        )
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
        # Show sensible starting guesses and the equation right away for the
        # current model
        self._populate_initial_params_table()
        self._update_equation_label_preview()

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
        window, and launches the ``WorkerThreadG2``. The number of stops
        requested per run is read directly from the selected stop
        channel's current device configuration (``getNumberOfStops()``),
        so the measurement always matches what the Channels settings
        dialog shows — no internal default is silently substituted.

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
        self.initialDate = datetime.datetime.now()
        self.finalDate = ""

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
        self.rateStopStopLabel.setText("—")

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

        # Read the number of stops actually configured for the selected
        # stop channel (set via the Channels settings dialog) so the
        # measurement uses exactly what the UI shows, instead of an
        # internal default that could silently disagree with it.
        _channels  = [self.device.ch1, self.device.ch2,
                      self.device.ch3, self.device.ch4]
        num_stops  = _channels[stop_ch - 1].getNumberOfStops()

        self.mainWindow.saveSettings()
        self.mainWindow.activeMeasurement()

        self.worker = WorkerThreadG2(
            parent        = self.parent,
            device        = self.device,
            stop_channel  = stop_ch,
            bin_ns        = bin_ns,
            window_ns     = window_ns,
            num_stops     = num_stops,
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
        self.finalDate = datetime.datetime.now()
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
        rate_stop_stop: float,
    ):
        """
        Update the g²(τ) step-histogram with the latest correlation data.

        Also refreshes the g²(0), rate, and event-count stat labels.
        Does NOT apply any color-coding or light-type classification.

        :param centres_ns: Bin-centre positions in nanoseconds (ndarray).
        :param g2: Normalized g²(τ) values (ndarray).
        :param total_events: Total photon events accumulated so far.
        :param rate_stop_stop: Rate (stop-stop) in counts per second, i.e.
            1 / mean(delta_stop) computed from the time between one stop
            and the next (dead-time-safe; see ``WorkerThreadG2``).
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
        if rate_stop_stop and rate_stop_stop > 0:
            self.rateStopStopLabel.setText(f"{rate_stop_stop:,.0f} cps")
        else:
            self.rateStopStopLabel.setText("—")

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
        self.rateStopStopLabel.setText("—")
        self.eventsLabel.setText("0")
        self.elapsedLabel.setText("0 s")
        # Reset cursor
        self._cursor_line.setVisible(False)
        if self.g2CursorLabel is not None:
            self.g2CursorLabel.setText("—")
        # Reset fit — blank the "Resultado del fit" column only; the
        # equation and the editable "Valor inicial" guesses stay visible
        # and untouched.
        self.fit_curve.setData([], [])
        self._clear_fit_results()
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

    # Parameter names (and units) per fit model, in curve_fit argument order.
    # Shared by the editable "initial parameters" table, the results table,
    # and the saved-data header.
    PARAM_LABELS = {
        0: [(u"y₀", ""), (u"V", ""), (u"τ₀", "ns"), (u"σ", "ns")],
        1: [(u"y₀", ""), (u"V", ""), (u"τ₀", "ns"), (u"Γ", "ns")],
        2: [(u"y₀", ""), (u"α", ""), (u"τ₀", "ns"), (u"τ_c", "ns")],
        3: [(u"y₀", ""), (u"α", ""), (u"τ₀", "ns"), (u"τ_c", "ns")],
        4: [(u"a", ""),  (u"τ₀", "ns"), (u"τ₁", "ns"), (u"τ₂", "ns")],
    }

    def _default_p0(self, idx):
        """
        Automatically suggested initial guesses (p0) for model ``idx``,
        based on the currently displayed g²(τ) data when available, or on
        generic placeholders (used to pre-fill the table before any data
        has been collected).

        :return: list of 4 floats, in curve_fit argument order.
        """
        tau_arr = np.array([])
        g2_arr  = np.array([])
        if (self.last_centres_ns is not None and self.last_g2 is not None
                and len(self.last_centres_ns) == len(self.last_g2)):
            tau_arr = self.last_centres_ns.copy()
            g2_arr  = self.last_g2.copy()
            mask    = np.isfinite(g2_arr)
            tau_arr = tau_arr[mask]
            g2_arr  = g2_arr[mask]

        hw        = float(np.max(np.abs(tau_arr))) if len(tau_arr) > 0 else 200.0
        tau_scale = hw / 4.0

        if idx == 0:      # Antibunched Gaussian
            return [1.0, 0.5, 0.0, tau_scale]
        elif idx == 1:    # Antibunched Lorentzian
            y0_guess = float(np.max(g2_arr)) if len(g2_arr) > 0 else 1.0
            return [y0_guess, 0.5, 0.0, tau_scale]
        elif idx == 2:    # Bunched Gaussian
            return [1.0, 0.5, 0.0, tau_scale]
        elif idx == 3:    # Bunched Lorentzian
            return [1.0, 0.5, 0.0, tau_scale]
        elif idx == 4:    # Three-level system
            return [0.5, 0.0, tau_scale * 0.5, tau_scale * 2.0]
        return [1.0, 0.5, 0.0, tau_scale]

    @staticmethod
    def _get_bounds(idx, hw):
        """Return the (lower, upper) curve_fit bounds tuple for model ``idx``."""
        if idx == 4:
            return ([0, -hw, 0.01, 0.01], [np.inf, hw, np.inf, np.inf])
        return ([0, 0, -hw, 0.01], [np.inf, np.inf, hw, np.inf])

    def _populate_initial_params_table(self, *_args):
        """
        (Re)fill the "Parámetro" and "Valor inicial" columns of the merged
        fit table for the currently selected fit model. Called on startup,
        whenever ``fitModelCombo`` changes, and by the "Auto" button.

        Values shown come from ``_initial_params_cache`` only once the user
        has actually edited that model's guesses (or reset them) in this
        session. Until then, the guess is recomputed fresh from the live
        g²(τ) data every time this is called, so it keeps tracking the
        current measurement window instead of freezing on whatever was on
        screen the first time (e.g. before any data existed).

        The "Resultado del fit" column is always cleared here: changing the
        model or the initial guess invalidates whatever result was
        previously shown, so the user is prompted to press "Fit" again.
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
        for row, (name, unit) in enumerate(labels):
            display_name = f"{name} ({unit})" if unit else name
            item_name = QTableWidgetItem(display_name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, item_name)

            item_value = QTableWidgetItem(f"{values[row]:.4f}")
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
        """Keep the per-model cache in sync when the user edits a guess."""
        if column != 1 or self.fitTable is None:
            return
        idx = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
        item = self.fitTable.item(row, column)
        if item is None:
            return
        try:
            value = float(item.text())
        except ValueError:
            # Invalid entry — revert to the last known-good value.
            cached = self._initial_params_cache.get(idx, self._default_p0(idx))
            self.fitTable.blockSignals(True)
            item.setText(f"{cached[row]:.4f}")
            self.fitTable.blockSignals(False)
            return

        cached = self._initial_params_cache.setdefault(idx, self._default_p0(idx))
        cached[row] = value

    def _reset_initial_params_to_auto(self):
        """
        "Auto" button — discard any manual edits for the current model and
        go back to tracking the automatically computed guess (which itself
        keeps following the live g²(τ) data on every subsequent repaint).
        """
        idx = self.fitModelCombo.currentIndex() if self.fitModelCombo is not None else 0
        self._initial_params_cache.pop(idx, None)
        self._populate_initial_params_table()

    def _clear_fit_results(self):
        """
        Blank the "Resultado del fit" column and forget the last successful
        fit, without touching the editable "Valor inicial" guesses or
        hiding the equation/table — so the panel stays ready for editing.
        """
        if self.fitResultLabel is not None:
            self.fitResultLabel.setVisible(False)
        if self.fitTable is not None:
            self.fitTable.blockSignals(True)
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
        Read the editable p0 guesses for model ``idx``, falling back to the
        auto-computed defaults for any missing/invalid entry, then clip them
        into ``bounds`` so a user-entered value outside the allowed range
        can't make curve_fit raise.

        Reads directly from ``fitTable`` column 1 ("Valor inicial"; the
        table always reflects the currently selected model, since it is
        repopulated on every ``fitModelCombo`` change) so whatever is on
        screen at the moment "Fit" is pressed is what gets used — no
        reliance on the edit signal having already fired. Falls back to the
        per-model cache, then to the computed defaults, if the table isn't
        available.
        """
        defaults = self._default_p0(idx)
        p0 = list(defaults)

        table = self.fitTable
        if table is not None and table.rowCount() == len(defaults):
            for row in range(table.rowCount()):
                item = table.item(row, 1)
                if item is None:
                    continue
                try:
                    p0[row] = float(item.text())
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

    def _fill_fit_results(self, idx, popt):
        """
        Write the fit result values into the "Resultado del fit" column
        (index 2) of the merged table, aligned row-by-row with the
        "Valor inicial" column already shown for model ``idx`` (the table
        rows/labels were already set by ``_populate_initial_params_table``
        for this same model).
        """
        if self.fitTable is None:
            return
        labels = self.PARAM_LABELS.get(idx, self.PARAM_LABELS[0])
        table = self.fitTable
        table.blockSignals(True)
        for row, ((name, unit), value) in enumerate(zip(labels, popt)):
            unit_suffix = f" {unit}" if unit else ""
            item_result = QTableWidgetItem(f"{value:.4f}{unit_suffix}")
            item_result.setTextAlignment(Qt.AlignCenter)
            item_result.setFlags(item_result.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, item_result)
        table.blockSignals(False)

    def _get_fit_header_lines(self):
        """
        Return fit result lines for the save header, or an empty string if
        no fit has been run yet.
        """
        if self.fitModelCombo is None or self.last_fit_idx is None:
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
        if self.last_p0_used is not None and self.last_fit_idx == idx:
            labels = self.PARAM_LABELS.get(idx, [])
            for (name, unit), value in zip(labels, self.last_p0_used):
                unit_suffix = f" {unit}" if unit else ""
                lines.append(f"Initial {name}:\t{value:.4f}{unit_suffix}")
        if self.fitTable is not None and self.last_fit_idx == idx:
            for row in range(self.fitTable.rowCount()):
                n = self.fitTable.item(row, 0)
                v = self.fitTable.item(row, 2)
                if n and v and v.text():
                    lines.append(f"{n.text()}:\t{v.text()}")
        return "\n".join(lines)

    def run_fit(self):
        """Fit the current g²(τ) histogram with the selected model."""
        if self.fitResultLabel is not None:
            self.fitResultLabel.setVisible(False)

        if self.last_centres_ns is None or len(self.last_centres_ns) < 5:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText("Not enough data to fit.")
                self.fitResultLabel.setVisible(True)
            return

        tau  = self.last_centres_ns.copy()
        g2   = self.last_g2.copy()
        mask = np.isfinite(g2)
        tau  = tau[mask]
        g2   = g2[mask]

        idx = self.fitModelCombo.currentIndex() if self.fitModelCombo else 0
        hw  = float(np.max(np.abs(tau))) if len(tau) > 0 else 200.0

        bounds = self._get_bounds(idx, hw)
        # p0 comes from the editable "Valor inicial" column (falling back
        # to the auto-computed guess for anything left blank/invalid),
        # clipped into the fit bounds so an out-of-range guess can't make
        # curve_fit raise.
        p0 = self._read_initial_params(idx, bounds=bounds)

        try:
            if idx == 0:  # Antibunched Gaussian
                popt, _ = curve_fit(self._model_antibunched_gaussian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                fit_g2 = self._model_antibunched_gaussian(tau, *popt)

            elif idx == 1:  # Antibunched Lorentzian
                popt, _ = curve_fit(self._model_antibunched_lorentzian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                fit_g2 = self._model_antibunched_lorentzian(tau, *popt)

            elif idx == 2:  # Bunched Gaussian
                popt, _ = curve_fit(self._model_bunched_gaussian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                fit_g2 = self._model_bunched_gaussian(tau, *popt)

            elif idx == 3:  # Bunched Lorentzian
                popt, _ = curve_fit(self._model_bunched_lorentzian,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                fit_g2 = self._model_bunched_lorentzian(tau, *popt)

            elif idx == 4:  # Three-level system
                popt, _ = curve_fit(self._model_three_level,
                                    tau, g2, p0=p0, bounds=bounds, maxfev=10000)
                fit_g2 = self._model_three_level(tau, *popt)

            else:
                return

            # Write the results into the "Resultado del fit" column, right
            # next to the "Valor inicial" guesses that produced them.
            self._fill_fit_results(idx, popt)

            # Remember the p0 actually used, for the saved-data header.
            self.last_p0_used = list(p0)
            self.last_fit_idx = idx

            self._update_equation_label_preview()
            self.fit_curve.setData(tau, fit_g2)

        except RuntimeError:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText("Fit did not converge.")
                self.fitResultLabel.setVisible(True)
        except Exception as e:
            if self.fitResultLabel is not None:
                self.fitResultLabel.setText(f"Fit error: {e}")
                self.fitResultLabel.setVisible(True)

    # ── Save data ─────────────────────────────────────────────────────────────

    def save_data(self):
        """
        Save the current g²(τ) measurement to two text files.

        Opens a format-selection dialog (txt / csv / dat) and writes:

        - ``..._StartStopTimes``: the raw (unbinned) stop times recorded
          during the acquisition, one row per detected event — the raw
          start-stop data behind the measurement.
        - ``..._G2Curve``: the analyzed data, i.e. the g²(τ) curve itself
          (τ in ns and the corresponding normalized g²(τ) value).

        Both files share the same header with the measurement parameters
        (bin width, window, TDC mode, stop channel).

        :return: None
        """
        if len(self.last_centres_ns) == 0:
            return

        dataFolderPrefix = self.savefile.getDataFolderPrefix()
        folder_path      = dataFolderPrefix["saveFolder"]

        now               = datetime.datetime.now()
        current_date_str  = now.strftime("%Y%m%d%H%M%S")

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
            f"Tab:\tg2 (HBT)\n"
            f"Initial date:\t{self.initialDate}\n"
            f"Final date:\t{self.finalDate}\n"
            f"Device model:\t{self.device.getModelIdn()}\n"
            f"Bin width (ns):\t{bin_ns_val}\n"
            f"Window (ns):\t{window_ns_val}\n"
            f"Stop channel:\tChannel {ch_label}"
        )

        fit_header = self._get_fit_header_lines()
        if fit_header:
            setting += "\n" + fit_header

        prefix = dataFolderPrefix.get("g2Prefix", "G2")

        # Two files: raw start-stop data and the analyzed g²(τ) curve
        filename_raw   = f"{prefix}_{current_date_str}_Channel{ch_label}_StartStopTimes"
        filename_curve = f"{prefix}_{current_date_str}_Channel{ch_label}_G2Curve"

        # Raw stop times accumulated by the worker thread during acquisition
        raw_stop_ps = list(getattr(self.worker, "raw_stop_ps", []))

        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            self.savefile.save_g2_start_stop_times(
                raw_stop_ps, filename_raw, folder_path, setting, selected_format
            )
            self.savefile.save_g2Hbt_data(
                (self.last_centres_ns, self.last_g2), filename_curve,
                folder_path, setting, selected_format, "tau_ns"
            )

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"The files have been saved successfully in path folder:\n\n"
                f"{folder_path} with the following names:\n\n"
                f"File1: {filename_curve}.{selected_format}\n"
                f"File2: {filename_raw}.{selected_format}"
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

            # Hide the tau cursor line just for the export so it doesn't end
            # up in the saved image, then restore its on-screen state
            # (visible/hidden) exactly as it was, whether the export
            # succeeds or fails.
            cursor_was_visible = self._cursor_line.isVisible()
            self._cursor_line.setVisible(False)
            try:
                exporter = pg.exporters.ImageExporter(self.plot)
                exporter.parameters()['width']  = 800
                exporter.parameters()['height'] = 600
                exporter.export(full_path)
            finally:
                self._cursor_line.setVisible(cursor_was_visible)

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