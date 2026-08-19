# -*- coding: utf-8 -*-

from PySide2.QtCore    import QMetaObject, QCoreApplication, Qt
from PySide2.QtGui     import QPixmap, QPainter, QColor
from PySide2.QtWidgets import (
    QSizePolicy, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QPushButton, QGridLayout,
    QApplication, QWidget, QSpinBox, QDoubleSpinBox,
    QCheckBox, QComboBox, QMainWindow, QTableWidget,
    QTableWidgetItem, QAbstractItemView,
)
# QDoubleSpinBox already imported above; listed explicitly for clarity
import sys
import types


class Ui_G2(object):
    """
    Pure layout class for the g²(τ) HBT measurement tab.

    Mirrors ``Ui_FCSMeasurement`` in structure: a two-column horizontal
    layout with a configuration panel on the left (stretch 3) and a
    graphic/status panel on the right (stretch 7).

    All widget references required by ``G2Logic`` are public attributes
    set up by ``setupUi``.
    """

    def setupUi(self, G2Measurement):
        """
        Builds and lays out every widget of the g²(τ) HBT measurement tab.

        Constructs the two-column layout described in the class docstring:
        the left ``ConfigurationArea`` (measurement controls, correlator
        parameters, cursor/fit widgets, and measurement stats panels) and the
        right ``TotalGraphicArea`` (the empty ``graphicFrame`` where
        ``G2Logic`` injects the live plot, plus the status bar). Also sets
        the initial enabled/disabled state of the action buttons, draws the
        initial grey status dot, and calls ``retranslateUi`` to set every
        widget's display text.

        :param G2Measurement: The widget (typically a ``QWidget`` tab page)
            that this UI class will populate.
        :return: None
        """
        if not G2Measurement.objectName():
            G2Measurement.setObjectName(u"G2Measurement")
        G2Measurement.setEnabled(True)
        G2Measurement.resize(1108, 874)

        # ── Root size policy ──────────────────────────────────────────────
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            G2Measurement.sizePolicy().hasHeightForWidth()
        )
        G2Measurement.setSizePolicy(sizePolicy)
        G2Measurement.setAcceptDrops(False)
        G2Measurement.setAutoFillBackground(False)

        # ── Root horizontal layout ────────────────────────────────────────
        self.horizontalLayout = QHBoxLayout(G2Measurement)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # ─────────────────────────────────────────────────────────────────
        # LEFT COLUMN – ConfigurationArea  (stretch 3)
        # ─────────────────────────────────────────────────────────────────
        self.ConfigurationArea = QWidget(G2Measurement)
        self.ConfigurationArea.setObjectName(u"ConfigurationArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.ConfigurationArea.sizePolicy().hasHeightForWidth()
        )
        self.ConfigurationArea.setSizePolicy(sizePolicy1)
        self.ConfigurationArea.setAutoFillBackground(True)

        self.verticalLayout = QVBoxLayout(self.ConfigurationArea)
        self.verticalLayout.setObjectName(u"verticalLayout")

        # ── Panel: Measurement controls ───────────────────────────────────
        self.MeasurementControlsFrame = QFrame(self.ConfigurationArea)
        self.MeasurementControlsFrame.setObjectName(u"MeasurementControlsFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(
            self.MeasurementControlsFrame.sizePolicy().hasHeightForWidth()
        )
        self.MeasurementControlsFrame.setSizePolicy(sizePolicy3)
        self.MeasurementControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.MeasurementControlsFrame.setFrameShadow(QFrame.Plain)

        self.verticalLayout_controls = QVBoxLayout(self.MeasurementControlsFrame)
        self.verticalLayout_controls.setObjectName(u"verticalLayout_controls")

        # Title label
        self.LabelControlsFrame = QFrame(self.MeasurementControlsFrame)
        self.LabelControlsFrame.setObjectName(u"LabelControlsFrame")
        self.LabelControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.LabelControlsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_label = QVBoxLayout(self.LabelControlsFrame)
        self.verticalLayout_label.setObjectName(u"verticalLayout_label")
        self.controlsLabel = QLabel(self.LabelControlsFrame)
        self.controlsLabel.setObjectName(u"controlsLabel")
        self.verticalLayout_label.addWidget(self.controlsLabel)
        self.verticalLayout_controls.addWidget(self.LabelControlsFrame)

        # Start / Stop / Clear buttons row
        self.StartStopFrame = QFrame(self.MeasurementControlsFrame)
        self.StartStopFrame.setObjectName(u"StartStopFrame")
        self.StartStopFrame.setFrameShape(QFrame.StyledPanel)
        self.StartStopFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_startstop = QHBoxLayout(self.StartStopFrame)
        self.horizontalLayout_startstop.setObjectName(u"horizontalLayout_startstop")

        self.startButton = QPushButton(self.StartStopFrame)
        self.startButton.setObjectName(u"startButton")
        self.horizontalLayout_startstop.addWidget(self.startButton)

        self.stopButton = QPushButton(self.StartStopFrame)
        self.stopButton.setObjectName(u"stopButton")
        self.horizontalLayout_startstop.addWidget(self.stopButton)

        self.clearButton = QPushButton(self.StartStopFrame)
        self.clearButton.setObjectName(u"clearButton")
        self.horizontalLayout_startstop.addWidget(self.clearButton)

        self.verticalLayout_controls.addWidget(self.StartStopFrame)

        # Save data / Save plot buttons row
        self.SaveFrame = QFrame(self.MeasurementControlsFrame)
        self.SaveFrame.setObjectName(u"SaveFrame")
        self.SaveFrame.setFrameShape(QFrame.StyledPanel)
        self.SaveFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_save = QHBoxLayout(self.SaveFrame)
        self.horizontalLayout_save.setObjectName(u"horizontalLayout_save")

        self.saveDataButton = QPushButton(self.SaveFrame)
        self.saveDataButton.setObjectName(u"saveDataButton")
        self.horizontalLayout_save.addWidget(self.saveDataButton)

        self.savePlotButton = QPushButton(self.SaveFrame)
        self.savePlotButton.setObjectName(u"savePlotButton")
        self.horizontalLayout_save.addWidget(self.savePlotButton)

        self.verticalLayout_controls.addWidget(self.SaveFrame)

        # ── Panel: Measurement stats ──────────────────────────────────────
        self.InfoFrame = QFrame(self.ConfigurationArea)
        self.InfoFrame.setObjectName(u"InfoFrame")
        self.InfoFrame.setFrameShape(QFrame.StyledPanel)
        self.InfoFrame.setFrameShadow(QFrame.Plain)

        self.verticalLayout_info = QVBoxLayout(self.InfoFrame)
        self.verticalLayout_info.setObjectName(u"verticalLayout_info")
        self.verticalLayout_info.setContentsMargins(6, 4, 6, 4)
        # Events row
        self.eventsRowFrame = QFrame(self.InfoFrame)
        self.eventsRowLayout = QHBoxLayout(self.eventsRowFrame)
        self.eventsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.eventsKeyLabel = QLabel("Events:", self.eventsRowFrame)
        self.eventsKeyLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.eventsLabel = QLabel("0", self.eventsRowFrame)
        self.eventsLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.eventsRowLayout.addWidget(self.eventsKeyLabel)
        self.eventsRowLayout.addWidget(self.eventsLabel)
        self.verticalLayout_info.addWidget(self.eventsRowFrame)

        # Elapsed row
        self.elapsedRowFrame = QFrame(self.InfoFrame)
        self.elapsedRowLayout = QHBoxLayout(self.elapsedRowFrame)
        self.elapsedRowLayout.setContentsMargins(0, 0, 0, 0)
        self.elapsedKeyLabel = QLabel("Elapsed:", self.elapsedRowFrame)
        self.elapsedKeyLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.elapsedLabel = QLabel("0 s", self.elapsedRowFrame)
        self.elapsedLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.elapsedRowLayout.addWidget(self.elapsedKeyLabel)
        self.elapsedRowLayout.addWidget(self.elapsedLabel)
        self.verticalLayout_info.addWidget(self.elapsedRowFrame)

        # g²(0) row
        self.g2ZeroRowFrame = QFrame(self.InfoFrame)
        self.g2ZeroRowLayout = QHBoxLayout(self.g2ZeroRowFrame)
        self.g2ZeroRowLayout.setContentsMargins(0, 0, 0, 0)
        self.g2ZeroKeyLabel = QLabel("g²(τ=0):", self.g2ZeroRowFrame)
        self.g2ZeroKeyLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.g2ZeroLabel = QLabel("—", self.g2ZeroRowFrame)
        self.g2ZeroLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.g2ZeroRowLayout.addWidget(self.g2ZeroKeyLabel)
        self.g2ZeroRowLayout.addWidget(self.g2ZeroLabel)
        self.verticalLayout_info.addWidget(self.g2ZeroRowFrame)

        # Count Estimation row (formerly "Rate (stop-stop)").
        # The checkbox itself is labelled "Count Estimation" and doubles as
        # the "Enable" toggle: checking it lets the user opt into a
        # stop-stop rate estimate even when the selected channel is
        # configured for a single stop — G2Logic bumps the request to 2
        # stops for the run in that case only. If the channel already has
        # 2+ stops configured, checking it changes nothing (that count is
        # kept as-is). The checkbox is disabled while a measurement is
        # running (see G2Logic.start_graphic / stop_graphic), so it can't
        # be toggled mid-measurement.
        self.countEstimationRowFrame = QFrame(self.InfoFrame)
        self.countEstimationRowLayout = QHBoxLayout(self.countEstimationRowFrame)
        self.countEstimationRowLayout.setContentsMargins(0, 0, 0, 0)

        self.countEstimationEnableCheckBox = QCheckBox(self.countEstimationRowFrame)
        self.countEstimationEnableCheckBox.setObjectName(u"countEstimationEnableCheckBox")
        self.countEstimationEnableCheckBox.setToolTip(
            "If the stop channel has a single stop configured, forces 2 "
            "stops per run so a Count Estimation can be shown. Has no "
            "effect if 2 or more stops are already configured."
        )
        self.countEstimationRowLayout.addWidget(self.countEstimationEnableCheckBox)

        self.countEstimationLabel = QLabel("—", self.countEstimationRowFrame)
        self.countEstimationLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.countEstimationRowLayout.addWidget(self.countEstimationLabel)
        self.verticalLayout_info.addWidget(self.countEstimationRowFrame)

        # ── Cursor / τ query row ──────────────────────────────────────────
        # Thin separator
        self.cursorSepFrame = QFrame(self.InfoFrame)
        self.cursorSepFrame.setFrameShape(QFrame.HLine)
        self.cursorSepFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_info.addWidget(self.cursorSepFrame)

        # τ spinbox row
        self.tauQueryRowFrame = QFrame(self.InfoFrame)
        self.tauQueryRowLayout = QHBoxLayout(self.tauQueryRowFrame)
        self.tauQueryRowLayout.setContentsMargins(0, 0, 0, 0)
        self.tauQueryKeyLabel = QLabel("Cursor τ:", self.tauQueryRowFrame)
        self.tauQueryKeyLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tauQuerySpinBox = QDoubleSpinBox(self.tauQueryRowFrame)
        self.tauQuerySpinBox.setObjectName(u"tauQuerySpinBox")
        self.tauQuerySpinBox.setMinimumHeight(22)
        self.tauQuerySpinBox.setRange(-1_000_000.0, 1_000_000.0)
        self.tauQuerySpinBox.setDecimals(3)
        self.tauQuerySpinBox.setSuffix(" ns")
        self.tauQuerySpinBox.setSingleStep(1.0)
        self.tauQuerySpinBox.setValue(0.0)
        # IMPORTANT: by default QAbstractSpinBox has keyboardTracking=True,
        # which fires valueChanged on EVERY keystroke while typing. Since
        # G2Logic._query_tau() reacts to valueChanged by snapping the value
        # to the nearest bin centre (and calling setValue() again), the box
        # would overwrite itself mid-typing — the number you type gets
        # replaced before you finish entering it. Disabling keyboard
        # tracking makes valueChanged fire only once editing is committed
        # (Enter/Tab/focus-out), so the snap-to-bin behaviour still happens,
        # but only against the final value you intended to enter.
        self.tauQuerySpinBox.setKeyboardTracking(False)
        self.tauQuerySpinBox.setToolTip(
            "Enter a τ value manually, or left-click on the plot."
        )

        # ── Make the up/down arrows step bin-by-bin ─────────────────────
        # By default, clicking the arrows (or pressing Up/Down) adds/
        # subtracts a fixed ``singleStep`` (1.0 ns), which almost never
        # lines up with an actual bin centre — so the arrows looked like
        # they "didn't do anything" (the value moved, but the displayed
        # g²(τ) and cursor line didn't change, since _query_tau always
        # snaps back to the nearest bin, i.e. the *same* bin).
        #
        # Instead, we override stepBy() on this specific spinbox instance
        # so that "up" advances to the next bin centre (higher τ) and
        # "down" moves to the previous bin centre (lower τ). The actual
        # bin data lives in G2Logic, not here, so the real work is
        # delegated to an optional hook — ``_on_tau_step`` — that G2Logic
        # attaches onto the spinbox itself via ``set_cursor_widgets``.
        # If no hook is attached yet (e.g. before a measurement has ever
        # produced data), we fall back to Qt's normal stepBy behaviour.
        def _tau_step_by(spinbox_self, steps):
            """
            Overridden ``stepBy`` that moves the τ cursor by whole bins.

            Delegates the actual bin-stepping logic to the ``_on_tau_step``
            hook attached by ``G2Logic`` (via ``set_cursor_widgets``), so the
            arrows/Up-Down keys land on the next or previous bin centre
            instead of an arbitrary fixed step. Falls back to Qt's default
            ``QDoubleSpinBox.stepBy`` behaviour if no hook has been attached
            yet.

            :param spinbox_self: The spin box instance this method is bound
                to (passed explicitly since it is assigned as an unbound
                function via ``types.MethodType``).
            :param steps: Number of steps to move; positive to increase τ,
                negative to decrease it.
            :type steps: int
            :return: None
            """
            hook = getattr(spinbox_self, "_on_tau_step", None)
            if callable(hook):
                hook(steps)
            else:
                QDoubleSpinBox.stepBy(spinbox_self, steps)

        self.tauQuerySpinBox._on_tau_step = None
        self.tauQuerySpinBox.stepBy = types.MethodType(
            _tau_step_by, self.tauQuerySpinBox
        )

        self.tauQueryRowLayout.addWidget(self.tauQueryKeyLabel)
        self.tauQueryRowLayout.addWidget(self.tauQuerySpinBox)
        self.verticalLayout_info.addWidget(self.tauQueryRowFrame)

        # Keep the cursor spinbox range tied to the current half-window
        # (±Window value). Without this, the cursor's allowed range stays
        # fixed at ±1,000,000 ns forever, completely disconnected from
        # whatever the user sets in "Window (±)". This is wired up later
        # in setupUi, right after ``windowSpinBox`` is created — see
        # ``_sync_tau_cursor_range`` below.

        # g²(τ) cursor result row
        self.g2CursorRowFrame = QFrame(self.InfoFrame)
        self.g2CursorRowLayout = QHBoxLayout(self.g2CursorRowFrame)
        self.g2CursorRowLayout.setContentsMargins(0, 0, 0, 0)
        self.g2CursorKeyLabel = QLabel("g²(τ) cursor:", self.g2CursorRowFrame)
        self.g2CursorKeyLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.g2CursorLabel = QLabel("—", self.g2CursorRowFrame)
        self.g2CursorLabel.setObjectName(u"g2CursorLabel")
        self.g2CursorLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.g2CursorLabel.setStyleSheet(u"font-weight: bold; color: #16a085;")
        self.g2CursorRowLayout.addWidget(self.g2CursorKeyLabel)
        self.g2CursorRowLayout.addWidget(self.g2CursorLabel)
        self.verticalLayout_info.addWidget(self.g2CursorRowFrame)

        # ── Panel: Correlator parameters ──────────────────────────────────
        self.ParametersFrame = QFrame(self.ConfigurationArea)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        sizePolicy3.setHeightForWidth(
            self.ParametersFrame.sizePolicy().hasHeightForWidth()
        )
        self.ParametersFrame.setSizePolicy(sizePolicy3)
        self.ParametersFrame.setFrameShape(QFrame.StyledPanel)
        self.ParametersFrame.setFrameShadow(QFrame.Plain)

        self.verticalLayout_params = QVBoxLayout(self.ParametersFrame)
        self.verticalLayout_params.setObjectName(u"verticalLayout_params")
        # Slightly tighter spacing between Stop Channel / Bin width / Window /
        # Duration / Continuous-measurement rows (default was 6px).
        self.verticalLayout_params.setSpacing(2)

        # Parameters title label
        self.LabelParametersFrame = QFrame(self.ParametersFrame)
        self.LabelParametersFrame.setObjectName(u"LabelParametersFrame")
        self.LabelParametersFrame.setFrameShape(QFrame.StyledPanel)
        self.LabelParametersFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_plabel = QHBoxLayout(self.LabelParametersFrame)
        self.horizontalLayout_plabel.setObjectName(u"horizontalLayout_plabel")
        self.horizontalLayout_plabel.setContentsMargins(4, 4, 4, 4)

        self.parametersLabel = QLabel(self.LabelParametersFrame)
        self.parametersLabel.setObjectName(u"parametersLabel")
        self.horizontalLayout_plabel.addWidget(self.parametersLabel)
        self.horizontalLayout_plabel.addStretch(1)

        self.verticalLayout_params.addWidget(self.LabelParametersFrame)

        # Stop channel row
        self.StopChannelFrame = QFrame(self.ParametersFrame)
        self.StopChannelFrame.setObjectName(u"StopChannelFrame")
        self.StopChannelFrame.setFrameShape(QFrame.StyledPanel)
        self.StopChannelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_stopchannel = QHBoxLayout(self.StopChannelFrame)
        self.horizontalLayout_stopchannel.setContentsMargins(6, 0.75, 6, 0.75)

        self.stopChannelLabel = QLabel(self.StopChannelFrame)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")
        self.horizontalLayout_stopchannel.addWidget(self.stopChannelLabel)

        self.stopChannelComboBox = QComboBox(self.StopChannelFrame)
        self.stopChannelComboBox.setObjectName(u"stopChannelComboBox")
        self.stopChannelComboBox.addItem(u"Channel A")
        self.stopChannelComboBox.addItem(u"Channel B")
        self.stopChannelComboBox.addItem(u"Channel C")
        self.stopChannelComboBox.addItem(u"Channel D")
        # Force a comfortable minimum width based on content (not just the
        # currently-selected item) so neither the closed box nor the dropdown
        # popup ever clip/truncate "Channel X" text.
        self.stopChannelComboBox.setSizeAdjustPolicy(
            QComboBox.AdjustToMinimumContentsLengthWithIcon
        )
        self.stopChannelComboBox.setMinimumContentsLength(11)
        self.stopChannelComboBox.setMinimumWidth(110)
        self.horizontalLayout_stopchannel.addWidget(self.stopChannelComboBox)

        self.verticalLayout_params.addWidget(self.StopChannelFrame)

        # Bin width row (unit: ns)
        self.BinWidthFrame = QFrame(self.ParametersFrame)
        self.BinWidthFrame.setObjectName(u"BinWidthFrame")
        self.BinWidthFrame.setFrameShape(QFrame.StyledPanel)
        self.BinWidthFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_binwidth = QHBoxLayout(self.BinWidthFrame)
        self.horizontalLayout_binwidth.setContentsMargins(6, 0.75, 6, 0.75)
        self.horizontalLayout_binwidth.setObjectName(u"horizontalLayout_binwidth")

        self.binWidthLabel = QLabel(self.BinWidthFrame)
        self.binWidthLabel.setObjectName(u"binWidthLabel")
        self.horizontalLayout_binwidth.addWidget(self.binWidthLabel)

        self.binWidthSpinBox = QDoubleSpinBox(self.BinWidthFrame)
        self.binWidthSpinBox.setObjectName(u"binWidthSpinBox")
        self.binWidthSpinBox.setMinimum(0.1)        # 0.1 ns minimum
        self.binWidthSpinBox.setMaximum(10_000.0)   # 10 µs maximum
        self.binWidthSpinBox.setSingleStep(0.5)
        self.binWidthSpinBox.setDecimals(1)
        self.binWidthSpinBox.setValue(2.0)           # default: 2 ns
        self.binWidthSpinBox.setSuffix(" ns")
        self.horizontalLayout_binwidth.addWidget(self.binWidthSpinBox)

        self.verticalLayout_params.addWidget(self.BinWidthFrame)

        # Window row (unit: ns)
        self.WindowFrame = QFrame(self.ParametersFrame)
        self.WindowFrame.setObjectName(u"WindowFrame")
        self.WindowFrame.setFrameShape(QFrame.StyledPanel)
        self.WindowFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_window = QHBoxLayout(self.WindowFrame)
        self.horizontalLayout_window.setContentsMargins(6, 0.75, 6, 0.75)
        self.horizontalLayout_window.setObjectName(u"horizontalLayout_window")

        self.windowLabel = QLabel(self.WindowFrame)
        self.windowLabel.setObjectName(u"windowLabel")
        self.horizontalLayout_window.addWidget(self.windowLabel)

        self.windowSpinBox = QSpinBox(self.WindowFrame)
        self.windowSpinBox.setObjectName(u"windowSpinBox")
        self.windowSpinBox.setMinimum(10)         # minimum: 10 ns
        self.windowSpinBox.setMaximum(100_000)    # maximum: 100 µs
        self.windowSpinBox.setValue(200)           # default: 200 ns (±200 ns window)
        self.windowSpinBox.setSuffix(" ns")
        self.horizontalLayout_window.addWidget(self.windowSpinBox)

        self.verticalLayout_params.addWidget(self.WindowFrame)

        # ── Tie the cursor-τ spinbox range to ±Window ───────────────────
        self._on_tau_cursor_reset = None

        def _sync_tau_cursor_range(half_window_ns):
            """
            Resets the τ-cursor spin box range to match ``±half_window_ns``.

            Blocks signals while updating the range and resetting the value
            to 0 ns, to avoid Qt's implicit clamping from producing a
            surprising jump to the new range's edge. Since blocking signals
            skips the normal ``valueChanged`` → ``_query_tau`` connection,
            the optional ``_on_tau_cursor_reset`` hook is called afterward so
            the plot's cursor line and g²(τ) readout stay in sync.

            :param half_window_ns: New half-window value, in nanoseconds,
                taken from ``windowSpinBox``.
            :return: None
            """
            self.tauQuerySpinBox.blockSignals(True)
            self.tauQuerySpinBox.setRange(
                -float(half_window_ns), float(half_window_ns)
            )
            self.tauQuerySpinBox.setValue(0.0)
            self.tauQuerySpinBox.blockSignals(False)
            if callable(self._on_tau_cursor_reset):
                self._on_tau_cursor_reset()

        # Exposed publicly so other modules (e.g. G2Logic.start_graphic)
        # can re-apply it on demand, e.g. right before a measurement starts.
        self.syncTauCursorRange = _sync_tau_cursor_range

        # Apply once immediately so the initial range matches the default
        # Window value (200 ns) instead of the old ±1,000,000 ns default.
        self.syncTauCursorRange(self.windowSpinBox.value())
        self.windowSpinBox.valueChanged.connect(self.syncTauCursorRange)

        # Duration row (unit: seconds)
        self.DurationFrame = QFrame(self.ParametersFrame)
        self.DurationFrame.setObjectName(u"DurationFrame")
        self.DurationFrame.setFrameShape(QFrame.StyledPanel)
        self.DurationFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_duration = QHBoxLayout(self.DurationFrame)
        self.horizontalLayout_duration.setContentsMargins(6, 0.75, 6, 0.75)
        self.horizontalLayout_duration.setObjectName(u"horizontalLayout_duration")

        self.durationLabel = QLabel(self.DurationFrame)
        self.durationLabel.setObjectName(u"durationLabel")
        self.horizontalLayout_duration.addWidget(self.durationLabel)

        self.durationSpinBox = QSpinBox(self.DurationFrame)
        self.durationSpinBox.setObjectName(u"durationSpinBox")
        self.durationSpinBox.setMinimum(1)      # minimum: 1 second
        self.durationSpinBox.setMaximum(86400)  # maximum: 24 hours
        self.durationSpinBox.setValue(60)        # default: 60 seconds
        self.horizontalLayout_duration.addWidget(self.durationSpinBox)

        self.verticalLayout_params.addWidget(self.DurationFrame)

        # Indefinite measurement checkbox row
        self.IndefiniteFrame = QFrame(self.ParametersFrame)
        self.IndefiniteFrame.setObjectName(u"IndefiniteFrame")
        self.IndefiniteFrame.setFrameShape(QFrame.StyledPanel)
        self.IndefiniteFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_indefinite = QHBoxLayout(self.IndefiniteFrame)
        self.horizontalLayout_indefinite.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_indefinite.setObjectName(u"horizontalLayout_indefinite")

        self.indefiniteCheckBox = QCheckBox(self.IndefiniteFrame)
        self.indefiniteCheckBox.setObjectName(u"indefiniteCheckBox")
        self.horizontalLayout_indefinite.addWidget(self.indefiniteCheckBox)

        self.verticalLayout_params.addWidget(self.IndefiniteFrame)

        # When indefinite is checked, disable the duration spinbox
        self.indefiniteCheckBox.toggled.connect(
            lambda checked: self.durationSpinBox.setEnabled(not checked)
        )

        # ── Assemble panels in the requested order ──────────────────────
        # 1) Measurement parameters (top)
        # 2) Measurement controls (middle)
        # 3) Statistics / info (bottom)
        self.verticalLayout.addWidget(self.ParametersFrame)
        self.verticalLayout.addWidget(self.MeasurementControlsFrame)
        self.verticalLayout.addWidget(self.InfoFrame)

        # Vertical spacer so panels hug the top
        self.verticalLayout.addStretch(1)

        self.horizontalLayout.addWidget(self.ConfigurationArea)

        # ─────────────────────────────────────────────────────────────────
        # RIGHT COLUMN – TotalGraphicArea  (stretch 7)
        # ─────────────────────────────────────────────────────────────────
        self.TotalGraphicArea = QWidget(G2Measurement)
        self.TotalGraphicArea.setObjectName(u"TotalGraphicArea")
        self.TotalGraphicArea.setEnabled(True)

        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(7)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.TotalGraphicArea.sizePolicy().hasHeightForWidth()
        )
        self.TotalGraphicArea.setSizePolicy(sizePolicy4)

        self.verticalLayoutGraph = QVBoxLayout(self.TotalGraphicArea)
        self.verticalLayoutGraph.setObjectName(u"verticalLayoutGraph")

        # ── Fit controls row ──────────────────────────────────────────────
        self.fitFrame = QFrame(self.TotalGraphicArea)
        self.fitFrame.setObjectName(u"fitFrame")
        self.fitFrame.setFrameShape(QFrame.StyledPanel)
        self.fitFrame.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_fit = QHBoxLayout(self.fitFrame)
        self.horizontalLayout_fit.setContentsMargins(8, 4, 8, 4)
        self.horizontalLayout_fit.setSpacing(10)

        self.fitModelCombo = QComboBox(self.fitFrame)
        self.fitModelCombo.setObjectName(u"fitModelCombo")
        self.fitModelCombo.addItem(u"Antibunched Gaussian")
        self.fitModelCombo.addItem(u"Antibunched Lorentzian")
        self.fitModelCombo.addItem(u"Bunched Gaussian")
        self.fitModelCombo.addItem(u"Bunched Lorentzian")
        self.fitModelCombo.addItem(u"Three-level system")
        self.fitModelCombo.setMinimumWidth(230)
        self.fitModelCombo.setMinimumHeight(28)
        self.horizontalLayout_fit.addWidget(self.fitModelCombo)

        self.fitButton = QPushButton(self.fitFrame)
        self.fitButton.setObjectName(u"fitButton")
        self.fitButton.setMinimumWidth(60)
        self.fitButton.setMinimumHeight(28)
        self.horizontalLayout_fit.addWidget(self.fitButton)

        self.horizontalLayout_fit.addStretch(1)

        self.verticalLayoutGraph.addWidget(self.fitFrame)

        # ── Fit parameters & results panel (equation + single merged table) ─
        # Replaces the old pair of duplicate-looking boxes ("Initial
        # parameters" table + "Fit results" table) with one panel: the
        # equation on top, and one 3-column table where the user edits the
        # initial guess right next to where the fit result will appear.
        self.fitResultsFrame = QFrame(self.TotalGraphicArea)
        self.fitResultsFrame.setObjectName(u"fitResultsFrame")
        self.fitResultsFrame.setFrameShape(QFrame.StyledPanel)
        self.fitResultsFrame.setFrameShadow(QFrame.Plain)

        self.verticalLayout_fitResults = QVBoxLayout(self.fitResultsFrame)
        self.verticalLayout_fitResults.setContentsMargins(10, 6, 10, 6)
        self.verticalLayout_fitResults.setSpacing(6)

        # Header row: equation (centered, renders HTML for super/subscripts)
        # plus the "Auto" button that resets the "Valor inicial" column.
        self.horizontalLayout_fitHeader = QHBoxLayout()
        self.horizontalLayout_fitHeader.setSpacing(10)

        self.fitEquationLabel = QLabel(self.fitResultsFrame)
        self.fitEquationLabel.setObjectName(u"fitEquationLabel")
        self.fitEquationLabel.setStyleSheet(u"font-size: 13px; color: #333333;")
        self.fitEquationLabel.setAlignment(Qt.AlignCenter)
        self.fitEquationLabel.setTextFormat(Qt.RichText)
        self.fitEquationLabel.setWordWrap(True)
        self.horizontalLayout_fitHeader.addWidget(self.fitEquationLabel, 1)

        # "Auto" button resets the "Valor inicial" column back to the
        # automatically suggested guesses (computed from the live data).
        self.fitResetParamsButton = QPushButton(self.fitResultsFrame)
        self.fitResetParamsButton.setObjectName(u"fitResetParamsButton")
        self.fitResetParamsButton.setMinimumWidth(60)
        self.fitResetParamsButton.setMinimumHeight(24)
        self.horizontalLayout_fitHeader.addWidget(
            self.fitResetParamsButton, 0, Qt.AlignTop
        )

        self.verticalLayout_fitResults.addLayout(self.horizontalLayout_fitHeader)

        # Merged parameter table: Parámetro | Valor inicial (editable) |
        # Resultado del fit (read-only, filled in after pressing "Fit").
        self.fitTable = QTableWidget(self.fitResultsFrame)
        self.fitTable.setObjectName(u"fitTable")
        self.fitTable.setColumnCount(3)
        self.fitTable.setHorizontalHeaderLabels(
            [u"Parameter", u"Initial Value", u"Fit Result"]
        )
        self.fitTable.horizontalHeader().setStretchLastSection(True)
        self.fitTable.verticalHeader().setVisible(False)
        # Only the "Valor inicial" column (index 1) is editable; the
        # parameter names and the fit result stay fixed. G2Logic enforces
        # this per-item, but default triggers are kept broad (double-click /
        # edit key) for a smooth UX.
        self.fitTable.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )
        self.fitTable.setSelectionMode(QTableWidget.SingleSelection)
        self.fitTable.setShowGrid(True)
        self.fitTable.setMinimumHeight(120)
        self.fitTable.setStyleSheet(u"font-size: 11px;")
        self.verticalLayout_fitResults.addWidget(self.fitTable)

        # Hidden label for G2Logic error messages (e.g. "Fit did not converge.")
        self.fitResultLabel = QLabel(self.fitResultsFrame)
        self.fitResultLabel.setObjectName(u"fitResultLabel")
        self.fitResultLabel.setStyleSheet(u"color: #cc0000; font-size: 11px;")
        self.fitResultLabel.setAlignment(Qt.AlignCenter)
        self.fitResultLabel.setVisible(False)
        self.verticalLayout_fitResults.addWidget(self.fitResultLabel)

        self.verticalLayoutGraph.addWidget(self.fitResultsFrame)

        # ── Graphic area – G2Logic injects the plot here ──────────────────
        self.GraphicArea = QWidget(self.TotalGraphicArea)
        self.GraphicArea.setObjectName(u"GraphicArea")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(7)
        sizePolicy5.setVerticalStretch(95)
        sizePolicy5.setHeightForWidth(
            self.GraphicArea.sizePolicy().hasHeightForWidth()
        )
        self.GraphicArea.setSizePolicy(sizePolicy5)
        self.GraphicArea.setAutoFillBackground(True)

        self.gridLayout = QGridLayout(self.GraphicArea)
        self.gridLayout.setObjectName(u"gridLayout")

        # graphicFrame: the QFrame that G2Logic uses as its parent widget.
        # Equivalent to graphicFrame in Ui_FCSMeasurement.
        self.graphicFrame = QFrame(self.GraphicArea)
        self.graphicFrame.setObjectName(u"graphicFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(5)
        sizePolicy6.setVerticalStretch(5)
        sizePolicy6.setHeightForWidth(
            self.graphicFrame.sizePolicy().hasHeightForWidth()
        )
        self.graphicFrame.setSizePolicy(sizePolicy6)
        self.graphicFrame.setFrameShape(QFrame.StyledPanel)
        self.graphicFrame.setFrameShadow(QFrame.Plain)
        self.gridLayout.addWidget(self.graphicFrame, 0, 0, 1, 1)

        self.verticalLayoutGraph.addWidget(self.GraphicArea)

        # ── Status bar ────────────────────────────────────────────────────
        self.widgetStatus = QWidget(self.TotalGraphicArea)
        self.widgetStatus.setObjectName(u"widgetStatus")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(5)
        sizePolicy7.setHeightForWidth(
            self.widgetStatus.sizePolicy().hasHeightForWidth()
        )
        self.widgetStatus.setSizePolicy(sizePolicy7)

        self.verticalLayout_status = QVBoxLayout(self.widgetStatus)
        self.verticalLayout_status.setObjectName(u"verticalLayout_status")

        self.statusFrame = QFrame(self.widgetStatus)
        self.statusFrame.setObjectName(u"statusFrame")
        self.statusFrame.setFrameShape(QFrame.StyledPanel)
        self.statusFrame.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_status = QHBoxLayout(self.statusFrame)
        self.horizontalLayout_status.setObjectName(u"horizontalLayout_status")

        # "Status:" fixed label
        self.statusLabel = QLabel(self.statusFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(10)
        sizePolicy8.setVerticalStretch(0)
        self.statusLabel.setSizePolicy(sizePolicy8)
        self.horizontalLayout_status.addWidget(self.statusLabel)

        # Dynamic status text – updated by G2Logic
        self.valueStatusLabel = QLabel(self.statusFrame)
        self.valueStatusLabel.setObjectName(u"valueStatusLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(45)
        sizePolicy9.setVerticalStretch(0)
        self.valueStatusLabel.setSizePolicy(sizePolicy9)
        self.horizontalLayout_status.addWidget(self.valueStatusLabel)

        # Coloured dot – updated by G2Logic._draw_status_dot()
        self.pointLabel = QLabel(self.statusFrame)
        self.pointLabel.setObjectName(u"pointLabel")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(5)
        sizePolicy10.setVerticalStretch(0)
        self.pointLabel.setSizePolicy(sizePolicy10)
        self.horizontalLayout_status.addWidget(self.pointLabel)

        self.verticalLayout_status.addWidget(self.statusFrame)
        self.verticalLayoutGraph.addWidget(self.widgetStatus)

        self.horizontalLayout.addWidget(self.TotalGraphicArea)

        # ── Finalise ──────────────────────────────────────────────────────
        self.retranslateUi(G2Measurement)
        QMetaObject.connectSlotsByName(G2Measurement)

        # Initial button states (mirrors Ui_FCSMeasurement)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.fitButton.setEnabled(False)

        # Draw the initial grey dot
        self.drawColorPoint()

        # ── Explicit Tab order ───────────────────────────────────────────
        # Qt's default focus chain follows widget *creation* order, not the
        # order panels were later added to ``verticalLayout``. Here
        # ParametersFrame (stopChannel/binWidth/window/duration/indefinite)
        # is constructed *after* MeasurementControlsFrame and InfoFrame,
        # even though it's placed visually on top — so Tab used to jump
        # controls -> stats -> parameters instead of following the panels
        # top-to-bottom. Chain the widgets explicitly, matching the actual
        # on-screen order (Parameters -> Controls -> Info -> Fit area).
        QWidget.setTabOrder(self.stopChannelComboBox, self.binWidthSpinBox)
        QWidget.setTabOrder(self.binWidthSpinBox, self.windowSpinBox)
        QWidget.setTabOrder(self.windowSpinBox, self.durationSpinBox)
        QWidget.setTabOrder(self.durationSpinBox, self.indefiniteCheckBox)
        QWidget.setTabOrder(self.indefiniteCheckBox, self.startButton)
        QWidget.setTabOrder(self.startButton, self.stopButton)
        QWidget.setTabOrder(self.stopButton, self.clearButton)
        QWidget.setTabOrder(self.clearButton, self.saveDataButton)
        QWidget.setTabOrder(self.saveDataButton, self.savePlotButton)
        QWidget.setTabOrder(self.savePlotButton, self.countEstimationEnableCheckBox)
        QWidget.setTabOrder(self.countEstimationEnableCheckBox, self.tauQuerySpinBox)
        QWidget.setTabOrder(self.tauQuerySpinBox, self.fitModelCombo)
        QWidget.setTabOrder(self.fitModelCombo, self.fitButton)
        QWidget.setTabOrder(self.fitButton, self.fitResetParamsButton)
        QWidget.setTabOrder(self.fitResetParamsButton, self.fitTable)

    # setupUi

    def retranslateUi(self, G2Measurement):
        """
        Sets the translatable display text of every widget built in ``setupUi``.

        Assigns the window title and the text of every label and button
        using ``QCoreApplication.translate``, so the UI can be localized
        through Qt's translation mechanism without touching the layout code
        in ``setupUi``.

        :param G2Measurement: The widget whose window title is set.
        :return: None
        """
        G2Measurement.setWindowTitle(
            QCoreApplication.translate("G2Measurement", u"Form", None)
        )
        # Controls panel
        self.controlsLabel.setText(
            QCoreApplication.translate(
                "G2Measurement", u"Measurement controls:", None
            )
        )
        self.startButton.setText(
            QCoreApplication.translate("G2Measurement", u"Start", None)
        )
        self.stopButton.setText(
            QCoreApplication.translate("G2Measurement", u"Stop", None)
        )
        self.saveDataButton.setText(
            QCoreApplication.translate("G2Measurement", u"Save Data File", None)
        )
        self.savePlotButton.setText(
            QCoreApplication.translate("G2Measurement", u"Save Plot", None)
        )
        self.clearButton.setText(
            QCoreApplication.translate("G2Measurement", u"Clear", None)
        )
        # Parameters panel
        self.parametersLabel.setText(
            QCoreApplication.translate(
                "G2Measurement", u"Measurement parameters:", None
            )
        )
        self.stopChannelLabel.setText(
            QCoreApplication.translate("G2Measurement", u"Stop Channel:", None)
        )
        self.binWidthLabel.setText(
            QCoreApplication.translate("G2Measurement", u"Bin width:", None)
        )
        self.windowLabel.setText(
            QCoreApplication.translate("G2Measurement", u"Window (±):", None)
        )
        self.durationLabel.setText(
            QCoreApplication.translate("G2Measurement", u"Duration (s):", None)
        )
        self.indefiniteCheckBox.setText(
            QCoreApplication.translate(
                "G2Measurement", u"Continuous measurement", None
            )
        )
        # Info panel
        self.countEstimationEnableCheckBox.setText(
            QCoreApplication.translate("G2Measurement", u"Count Estimation", None)
        )
        # Status bar
        self.statusLabel.setText(
            QCoreApplication.translate("G2Measurement", u"Status:", None)
        )
        self.valueStatusLabel.setText(
            QCoreApplication.translate(
                "G2Measurement", u"No measurement running", None
            )
        )
        self.pointLabel.setText(
            QCoreApplication.translate("G2Measurement", u"", None)
        )
        self.fitButton.setText(
            QCoreApplication.translate("G2Measurement", u"Fit", None)
        )
        self.fitResetParamsButton.setText(
            QCoreApplication.translate("G2Measurement", u"Auto", None)
        )
        self.fitEquationLabel.setText(
            QCoreApplication.translate("G2Measurement", u"", None)
        )
        self.fitResultLabel.setText(
            QCoreApplication.translate("G2Measurement", u"", None)
        )

    # retranslateUi

    def drawColorPoint(self):
        """
        Draw the initial grey status dot on ``pointLabel``.

        Called once at the end of ``setupUi`` so the dot is visible before
        any measurement starts. Mirrors ``Ui_FCSMeasurement.drawColorPoint``.
        """
        pixmap = QPixmap(self.pointLabel.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(128, 128, 128))
        painter.setPen(Qt.NoPen)
        point_size = min(
            self.pointLabel.width(), self.pointLabel.height()
        ) // 2
        x = (self.pointLabel.width()  - point_size) // 2
        y = (self.pointLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.pointLabel.setPixmap(pixmap)


# ── Quick preview ────────────────────────────────────

class _PreviewWindow(QMainWindow):
    """
    Standalone preview window used to visually inspect the G2 tab layout.

    Only used when this module is run directly (``python
    ui_g2measurement.py``); not imported or used by the rest of the
    application.
    """
    def __init__(self):
        """
        Builds the G2 UI inside a bare `QMainWindow` for quick visual review.

        Instantiates `Ui_G2`, runs its `setupUi`, expands the configuration
        area horizontally, and places both columns in the window's central
        widget.

        :return: None
        """
        super().__init__()
        self.ui = Ui_G2()
        self.ui.setupUi(self)
        self.ui.ConfigurationArea.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )
        central = QWidget()
        layout  = QHBoxLayout(central)
        layout.addWidget(self.ui.ConfigurationArea)
        layout.addWidget(self.ui.TotalGraphicArea)
        self.setCentralWidget(central)
        # Enable buttons so they are visible in the preview
        self.ui.startButton.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = _PreviewWindow()
    win.setWindowTitle("g²(τ) HBT Measurement – UI preview")
    win.resize(1108, 874)
    win.show()
    app.exec_()