# -*- coding: utf-8 -*-

from PySide2.QtCore import QMetaObject, QCoreApplication, Qt
from PySide2.QtGui  import QPixmap, QPainter, QColor
from PySide2.QtWidgets import (
    QSizePolicy, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QPushButton, QGridLayout,
    QMainWindow, QApplication, QWidget, QSpinBox, QCheckBox, QComboBox,
    QTableWidget, QTableWidgetItem, QToolButton,
)
import sys


class Ui_FCSMeasurement(object):
    """
    Pure layout class for the FCS measurement tab.

    Follows the same structure as ``Ui_HistogramaStartStop``:
    - Left column  (``ConfigurationArea``): all controls and parameters,
      stretch factor 3.
    - Right column (``TotalGraphicArea``):  empty ``graphicFrame`` where
      ``FCSLogic`` injects the pyqtgraph plot, plus the status bar at the
      bottom, stretch factor 7.

    Widget names exposed to ``FCSLogic`` (and to ``main.py``)
    ----------------------------------------------------------
    startButton       QPushButton   Begin measurement
    stopButton        QPushButton   End measurement
    saveDataButton    QPushButton   Save G(τ) data
    savePlotButton    QPushButton   Save plot image
    clearButton       QPushButton   Clear curve
    tau0SpinBox       QSpinBox      Base bin τ₀ in µs  (1–10 000 000)
    durationSpinBox   QSpinBox      Measurement duration in seconds (1–86400)
    indefiniteCheckBox QCheckBox    When checked, duration is ignored (run until Stop)
    graphicFrame      QFrame        Container for the live plot (Graph3)
    valueStatusLabel  QLabel        Status text
    pointLabel        QLabel        Coloured status dot
    """

    def setupUi(self, FCSMeasurement):
        if not FCSMeasurement.objectName():
            FCSMeasurement.setObjectName(u"FCSMeasurement")
        FCSMeasurement.setEnabled(True)
        FCSMeasurement.resize(1108, 874)

        # ── Root size policy ──────────────────────────────────────────────
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            FCSMeasurement.sizePolicy().hasHeightForWidth()
        )
        FCSMeasurement.setSizePolicy(sizePolicy)
        FCSMeasurement.setAcceptDrops(False)
        FCSMeasurement.setAutoFillBackground(False)

        # ── Root horizontal layout ────────────────────────────────────────
        self.horizontalLayout = QHBoxLayout(FCSMeasurement)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # ─────────────────────────────────────────────────────────────────
        # LEFT COLUMN – ConfigurationArea  (stretch 3)
        # ─────────────────────────────────────────────────────────────────
        self.ConfigurationArea = QWidget(FCSMeasurement)
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
        self.MeasurementControlsFrame.setFrameShape(QFrame.Panel)
        self.MeasurementControlsFrame.setFrameShadow(QFrame.Sunken)

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

        # Start / Stop buttons row
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
        self.InfoFrame.setFrameShape(QFrame.Panel)
        self.InfoFrame.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_info = QVBoxLayout(self.InfoFrame)
        self.verticalLayout_info.setObjectName(u"verticalLayout_info")

        self.statusLabel  = QLabel(self.InfoFrame)
        self.valueStatusLabel = QLabel(self.InfoFrame)
        self.pointLabel   = QLabel(self.InfoFrame)
        self.callsLabel   = QLabel(self.InfoFrame)
        self.eventsLabel  = QLabel(self.InfoFrame)
        self.elapsedLabel = QLabel(self.InfoFrame)

        # Status row: dot + text side by side
        self.statusRowFrame = QFrame(self.InfoFrame)
        self.horizontalLayout_statusrow = QHBoxLayout(self.statusRowFrame)
        self.horizontalLayout_statusrow.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_statusrow.addWidget(self.statusLabel)
        self.horizontalLayout_statusrow.addWidget(self.valueStatusLabel)
        self.horizontalLayout_statusrow.addWidget(self.pointLabel)
        self.horizontalLayout_statusrow.addStretch(1)

        self.verticalLayout_info.addWidget(self.statusRowFrame)
        self.verticalLayout_info.addWidget(self.callsLabel)
        self.verticalLayout_info.addWidget(self.eventsLabel)
        self.verticalLayout_info.addWidget(self.elapsedLabel)
        

        # ── Panel: Correlator parameters ──────────────────────────────────
        self.ParametersFrame = QFrame(self.ConfigurationArea)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        sizePolicy3.setHeightForWidth(
            self.ParametersFrame.sizePolicy().hasHeightForWidth()
        )
        self.ParametersFrame.setSizePolicy(sizePolicy3)
        self.ParametersFrame.setFrameShape(QFrame.Panel)
        self.ParametersFrame.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_params = QVBoxLayout(self.ParametersFrame)
        self.verticalLayout_params.setObjectName(u"verticalLayout_params")

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

        self.parametersHelpButton = QToolButton(self.LabelParametersFrame)
        self.parametersHelpButton.setObjectName(u"parametersHelpButton")
        self.parametersHelpButton.setText(u"?")
        self.parametersHelpButton.setFixedSize(22, 22)
        self.parametersHelpButton.setStyleSheet(
            u"QToolButton {"
            u"  font-weight: bold; font-size: 13px; color: #444444;"
            u"  border: 1px solid #888888; border-radius: 11px;"
            u"  background-color: #f0f0f0;"
            u"}"
            u"QToolButton:hover { background-color: #ddeeff; border-color: #1a5fa8; color: #1a5fa8; }"
            u"QToolButton:pressed { background-color: #c0d8f0; }"
        )
        self.horizontalLayout_plabel.addWidget(self.parametersHelpButton)
        self.horizontalLayout_plabel.addStretch(1)

        self.verticalLayout_params.addWidget(self.LabelParametersFrame)

        # Start channel row
        self.StartChannelFrame = QFrame(self.ParametersFrame)
        self.StartChannelFrame.setObjectName(u"StartChannelFrame")
        self.StartChannelFrame.setFrameShape(QFrame.StyledPanel)
        self.StartChannelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_startchannel = QHBoxLayout(self.StartChannelFrame)

        self.startChannelLabel = QLabel(self.StartChannelFrame)
        self.startChannelLabel.setObjectName(u"startChannelLabel")
        self.horizontalLayout_startchannel.addWidget(self.startChannelLabel)

        self.startChannelComboBox = QComboBox(self.StartChannelFrame)
        self.startChannelComboBox.setObjectName(u"startChannelComboBox")
        self.startChannelComboBox.addItem(u"Start channel")
        self.startChannelComboBox.addItem(u"Channel A")
        self.startChannelComboBox.addItem(u"Channel B")
        self.startChannelComboBox.addItem(u"Channel C")
        self.startChannelComboBox.addItem(u"Channel D")
        self.horizontalLayout_startchannel.addWidget(self.startChannelComboBox)

        self.verticalLayout_params.addWidget(self.StartChannelFrame)

        # Stop channel row
        self.StopChannelFrame = QFrame(self.ParametersFrame)
        self.StopChannelFrame.setObjectName(u"ChannelFrame")
        self.StopChannelFrame.setFrameShape(QFrame.StyledPanel)
        self.StopChannelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_stopchannel = QHBoxLayout(self.StopChannelFrame)

        self.stopChannelLabel = QLabel(self.StopChannelFrame)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")
        self.horizontalLayout_stopchannel.addWidget(self.stopChannelLabel)

        self.stopChannelComboBox = QComboBox(self.StopChannelFrame)
        self.stopChannelComboBox.setObjectName(u"stopChannelComboBox")
        self.stopChannelComboBox.addItem(u"Channel A")
        self.stopChannelComboBox.addItem(u"Channel B")
        self.stopChannelComboBox.addItem(u"Channel C")
        self.stopChannelComboBox.addItem(u"Channel D")
        self.horizontalLayout_stopchannel.addWidget(self.stopChannelComboBox)

        self.verticalLayout_params.addWidget(self.StopChannelFrame)

        # tau_0 row  (unit: ms, minimum 1 ms)
        self.Tau0Frame = QFrame(self.ParametersFrame)
        self.Tau0Frame.setObjectName(u"Tau0Frame")
        self.Tau0Frame.setFrameShape(QFrame.StyledPanel)
        self.Tau0Frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_tau0 = QHBoxLayout(self.Tau0Frame)
        self.horizontalLayout_tau0.setObjectName(u"horizontalLayout_tau0")

        self.tau0Label = QLabel(self.Tau0Frame)
        self.tau0Label.setObjectName(u"tau0Label")
        self.horizontalLayout_tau0.addWidget(self.tau0Label)

        self.tau0SpinBox = QSpinBox(self.Tau0Frame)
        self.tau0SpinBox.setObjectName(u"tau0SpinBox")
        self.tau0SpinBox.setMinimum(1)           # minimum: 1 µs
        self.tau0SpinBox.setMaximum(10_000_000)  # maximum: 10 s in µs
        self.tau0SpinBox.setValue(5)             # default: 5 µs 
        self.horizontalLayout_tau0.addWidget(self.tau0SpinBox)

        self.verticalLayout_params.addWidget(self.Tau0Frame)

        # Duration row (unit: seconds)
        self.DurationFrame = QFrame(self.ParametersFrame)
        self.DurationFrame.setObjectName(u"DurationFrame")
        self.DurationFrame.setFrameShape(QFrame.StyledPanel)
        self.DurationFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_duration = QHBoxLayout(self.DurationFrame)
        self.horizontalLayout_duration.setObjectName(u"horizontalLayout_duration")

        self.durationLabel = QLabel(self.DurationFrame)
        self.durationLabel.setObjectName(u"durationLabel")
        self.horizontalLayout_duration.addWidget(self.durationLabel)

        self.durationSpinBox = QSpinBox(self.DurationFrame)
        self.durationSpinBox.setObjectName(u"durationSpinBox")
        self.durationSpinBox.setMinimum(1)     # minimum: 1 second
        self.durationSpinBox.setMaximum(86400) # maximum: 24 hours
        self.durationSpinBox.setValue(60)      # default: 60 seconds
        self.horizontalLayout_duration.addWidget(self.durationSpinBox)

        self.verticalLayout_params.addWidget(self.DurationFrame)

        # Indefinite measurement checkbox row
        self.IndefiniteFrame = QFrame(self.ParametersFrame)
        self.IndefiniteFrame.setObjectName(u"IndefiniteFrame")
        self.IndefiniteFrame.setFrameShape(QFrame.StyledPanel)
        self.IndefiniteFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_indefinite = QHBoxLayout(self.IndefiniteFrame)
        self.horizontalLayout_indefinite.setObjectName(u"horizontalLayout_indefinite")

        self.indefiniteCheckBox = QCheckBox(self.IndefiniteFrame)
        self.indefiniteCheckBox.setObjectName(u"indefiniteCheckBox")
        self.horizontalLayout_indefinite.addWidget(self.indefiniteCheckBox)

        self.verticalLayout_params.addWidget(self.IndefiniteFrame)

        # When indefinite is checked, disable the duration spinbox
        self.indefiniteCheckBox.toggled.connect(
            lambda checked: self.durationSpinBox.setEnabled(not checked)
        )
        
        self.verticalLayout.addWidget(self.ParametersFrame)

        self.verticalLayout.addWidget(self.MeasurementControlsFrame)

        self.verticalLayout.addWidget(self.InfoFrame)

        # Vertical spacer so panels hug the top
        self.verticalLayout.addStretch(1)

        self.horizontalLayout.addWidget(self.ConfigurationArea)

        # ─────────────────────────────────────────────────────────────────
        # RIGHT COLUMN – TotalGraphicArea  (stretch 7)
        # ─────────────────────────────────────────────────────────────────
        self.TotalGraphicArea = QWidget(FCSMeasurement)
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
        self.fitFrame.setFrameShape(QFrame.Panel)
        self.fitFrame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_fit = QHBoxLayout(self.fitFrame)
        self.horizontalLayout_fit.setContentsMargins(8, 4, 8, 4)
        self.horizontalLayout_fit.setSpacing(10)

        self.fitModelCombo = QComboBox(self.fitFrame)
        self.fitModelCombo.setObjectName(u"fitModelCombo")
        self.fitModelCombo.addItem(u"3D Gaussian diffusion")
        self.fitModelCombo.addItem(u"Anomalous diffusion")
        self.fitModelCombo.setFixedWidth(200)
        self.fitModelCombo.setFixedHeight(28)
        self.horizontalLayout_fit.addWidget(self.fitModelCombo)

        self.fitButton = QPushButton(self.fitFrame)
        self.fitButton.setObjectName(u"fitButton")
        self.fitButton.setFixedWidth(60)
        self.fitButton.setFixedHeight(28)
        self.horizontalLayout_fit.addWidget(self.fitButton)

        self.fitOffsetCheckBox = QCheckBox(self.fitFrame)
        self.fitOffsetCheckBox.setObjectName(u"fitOffsetCheckBox")
        self.fitOffsetCheckBox.setChecked(True)
        self.horizontalLayout_fit.addWidget(self.fitOffsetCheckBox)

        self.horizontalLayout_fit.addStretch(1)

        self.verticalLayoutGraph.addWidget(self.fitFrame)

        # ── Fit results panel (equation + parameter table) ────────────────
        self.fitResultsFrame = QFrame(self.TotalGraphicArea)
        self.fitResultsFrame.setObjectName(u"fitResultsFrame")
        self.fitResultsFrame.setFrameShape(QFrame.Panel)
        self.fitResultsFrame.setFrameShadow(QFrame.Sunken)
        self.fitResultsFrame.setVisible(False)

        self.verticalLayout_fitResults = QVBoxLayout(self.fitResultsFrame)
        self.verticalLayout_fitResults.setContentsMargins(10, 6, 10, 6)
        self.verticalLayout_fitResults.setSpacing(6)

        # Equation label – renders HTML for super/subscripts
        self.fitEquationLabel = QLabel(self.fitResultsFrame)
        self.fitEquationLabel.setObjectName(u"fitEquationLabel")
        self.fitEquationLabel.setStyleSheet(
            u"font-size: 13px; color: #333333;"
        )
        self.fitEquationLabel.setAlignment(Qt.AlignCenter)
        self.fitEquationLabel.setTextFormat(Qt.RichText)
        self.fitEquationLabel.setWordWrap(True)
        self.verticalLayout_fitResults.addWidget(self.fitEquationLabel)

        # Parameter table
        self.fitTable = QTableWidget(self.fitResultsFrame)
        self.fitTable.setObjectName(u"fitTable")
        self.fitTable.setColumnCount(2)
        self.fitTable.setHorizontalHeaderLabels([u"Parameter", u"Value"])
        self.fitTable.horizontalHeader().setStretchLastSection(True)
        self.fitTable.verticalHeader().setVisible(False)
        self.fitTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.fitTable.setSelectionMode(QTableWidget.NoSelection)
        self.fitTable.setShowGrid(True)
        self.fitTable.setFixedHeight(100)
        self.fitTable.setStyleSheet(
            u"font-size: 11px;"
        )
        self.verticalLayout_fitResults.addWidget(self.fitTable)

        # Hidden label kept for FCSLogic error messages
        self.fitResultLabel = QLabel(self.fitResultsFrame)
        self.fitResultLabel.setObjectName(u"fitResultLabel")
        self.fitResultLabel.setStyleSheet(
            u"color: #cc0000; font-size: 11px;"
        )
        self.fitResultLabel.setAlignment(Qt.AlignCenter)
        self.fitResultLabel.setVisible(False)
        self.verticalLayout_fitResults.addWidget(self.fitResultLabel)

        self.verticalLayoutGraph.addWidget(self.fitResultsFrame)

        # ── Graphic area – FCSLogic injects the plot here ─────────────────
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

        # graphicFrame: the QFrame that FCSLogic uses as its parent widget.
        # Equivalent to Graph3 in Ui_HistogramaStartStop.
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
        self.statusFrame.setFrameShape(QFrame.Panel)
        self.statusFrame.setFrameShadow(QFrame.Sunken)

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

        # Dynamic status text – updated by FCSLogic
        self.valueStatusLabel = QLabel(self.statusFrame)
        self.valueStatusLabel.setObjectName(u"valueStatusLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(45)
        sizePolicy9.setVerticalStretch(0)
        self.valueStatusLabel.setSizePolicy(sizePolicy9)
        self.horizontalLayout_status.addWidget(self.valueStatusLabel)

        # Coloured dot – updated by FCSLogic._draw_status_dot()
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
        self.retranslateUi(FCSMeasurement)
        QMetaObject.connectSlotsByName(FCSMeasurement)

        # Initial button states (mirrors Ui_HistogramaStartStop)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.fitButton.setEnabled(False)

        # Draw the initial grey dot
        self.drawColorPoint()

    # setupUi

    def retranslateUi(self, FCSMeasurement):
        FCSMeasurement.setWindowTitle(
            QCoreApplication.translate("FCSMeasurement", u"Form", None)
        )
        # Controls panel
        self.controlsLabel.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Measurement controls:", None
            )
        )
        self.startButton.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Start", None
            )
        )
        self.stopButton.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Stop", None
            )
        )
        self.saveDataButton.setText(
            QCoreApplication.translate("FCSMeasurement", u"Save Data File", None)
        )
        self.savePlotButton.setText(
            QCoreApplication.translate("FCSMeasurement", u"Save Plot", None)
        )
        self.clearButton.setText(
            QCoreApplication.translate("FCSMeasurement", u"Clear", None)
        )
        # Parameters panel
        self.parametersLabel.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Correlator parameters:", None
            )
        )
        self.tau0Label.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Base bin width τ₀ (µs):", None
            )
        )
        self.durationLabel.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Duration (s):", None
            )
        )
        self.indefiniteCheckBox.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"Continuous measurement", None
            )
        )
        # Status bar
        self.statusLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Status:", None)
        )
        self.valueStatusLabel.setText(
            QCoreApplication.translate(
                "FCSMeasurement", u"No measurement running", None
            )
        )
        self.pointLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"", None)
        )
        self.callsLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Calls: 0", None)
            )
        self.eventsLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Events: 0", None)
            )
        self.elapsedLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Elapsed: 0 s", None)
            )
        self.statusLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Status:", None)
        )
        self.valueStatusLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"No measurement running", None)
        )
        self.pointLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"", None)
        )
        self.fitButton.setText(
            QCoreApplication.translate("FCSMeasurement", u"Fit", None)
        )
        self.fitEquationLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"", None)
        )
        self.fitResultLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"", None)
        )
        self.fitOffsetCheckBox.setText(
            QCoreApplication.translate("FCSMeasurement", u"G(∞) offset", None)
        )
        self.stopChannelLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Stop Channel:", None)
        )
        self.stopChannelComboBox.setItemText(
            0, QCoreApplication.translate("FCSMeasurement", u"Channel A", None)
        )
        self.stopChannelComboBox.setItemText(
            1, QCoreApplication.translate("FCSMeasurement", u"Channel B", None)
        )
        self.stopChannelComboBox.setItemText(
            2, QCoreApplication.translate("FCSMeasurement", u"Channel C", None)
        )
        self.stopChannelComboBox.setItemText(
            3, QCoreApplication.translate("FCSMeasurement", u"Channel D", None)
        )
        self.startChannelLabel.setText(
            QCoreApplication.translate("FCSMeasurement", u"Start Channel:", None)
        )
        self.startChannelComboBox.setItemText(
            0, QCoreApplication.translate("FCSMeasurement", u"Start channel", None)
        )
        self.startChannelComboBox.setItemText(
            1, QCoreApplication.translate("FCSMeasurement", u"Channel A", None)
        )
        self.startChannelComboBox.setItemText(
            2, QCoreApplication.translate("FCSMeasurement", u"Channel B", None)
        )
        self.startChannelComboBox.setItemText(
            3, QCoreApplication.translate("FCSMeasurement", u"Channel C", None)
        )
        self.startChannelComboBox.setItemText(
            4, QCoreApplication.translate("FCSMeasurement", u"Channel D", None)
        )
        

    # retranslateUi

    def drawColorPoint(self):
        """
        Draw the initial grey status dot on ``pointLabel``.

        Called once at the end of ``setupUi`` so the dot is visible before
        any measurement starts (mirrors ``Ui_HistogramaStartStop``).
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
    def __init__(self):
        super().__init__()
        self.ui = Ui_FCSMeasurement()
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
    win.setWindowTitle("FCS Measurement – UI preview")
    win.resize(1108, 874)
    win.show()
    app.exec_()