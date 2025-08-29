# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'g2NewUiqcDdDx.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_G2(object):
    def setupUi(self, G2):
        if not G2.objectName():
            G2.setObjectName(u"G2")
        G2.resize(904, 735)
        G2.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(G2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GraphicStatusFrame = QFrame(G2)
        self.GraphicStatusFrame.setObjectName(u"GraphicStatusFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.GraphicStatusFrame.sizePolicy().hasHeightForWidth())
        self.GraphicStatusFrame.setSizePolicy(sizePolicy)
        self.GraphicStatusFrame.setAutoFillBackground(True)
        self.GraphicStatusFrame.setFrameShape(QFrame.NoFrame)
        self.GraphicStatusFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.GraphicStatusFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.GraphicFrame = QFrame(self.GraphicStatusFrame)
        self.GraphicFrame.setObjectName(u"GraphicFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(95)
        sizePolicy1.setHeightForWidth(self.GraphicFrame.sizePolicy().hasHeightForWidth())
        self.GraphicFrame.setSizePolicy(sizePolicy1)
        self.GraphicFrame.setFrameShape(QFrame.StyledPanel)
        self.GraphicFrame.setFrameShadow(QFrame.Plain)

        self.verticalLayout_2.addWidget(self.GraphicFrame)

        self.ParametersMeasurementFrame = QFrame(self.GraphicStatusFrame)
        self.ParametersMeasurementFrame.setObjectName(u"ParametersMeasurementFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(5)
        sizePolicy2.setHeightForWidth(self.ParametersMeasurementFrame.sizePolicy().hasHeightForWidth())
        self.ParametersMeasurementFrame.setSizePolicy(sizePolicy2)
        self.ParametersMeasurementFrame.setFrameShape(QFrame.StyledPanel)
        self.ParametersMeasurementFrame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.ParametersMeasurementFrame)
        self.horizontalLayout_6.setSpacing(11)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.totalStartsLabel = QLabel(self.ParametersMeasurementFrame)
        self.totalStartsLabel.setObjectName(u"totalStartsLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.totalStartsLabel.sizePolicy().hasHeightForWidth())
        self.totalStartsLabel.setSizePolicy(sizePolicy3)
        self.totalStartsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.totalStartsLabel)

        self.totalStartsValue = QLabel(self.ParametersMeasurementFrame)
        self.totalStartsValue.setObjectName(u"totalStartsValue")
        sizePolicy3.setHeightForWidth(self.totalStartsValue.sizePolicy().hasHeightForWidth())
        self.totalStartsValue.setSizePolicy(sizePolicy3)

        self.horizontalLayout_6.addWidget(self.totalStartsValue)

        self.totalStopsLabel = QLabel(self.ParametersMeasurementFrame)
        self.totalStopsLabel.setObjectName(u"totalStopsLabel")
        sizePolicy3.setHeightForWidth(self.totalStopsLabel.sizePolicy().hasHeightForWidth())
        self.totalStopsLabel.setSizePolicy(sizePolicy3)
        self.totalStopsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.totalStopsLabel)

        self.totalStopsValue = QLabel(self.ParametersMeasurementFrame)
        self.totalStopsValue.setObjectName(u"totalStopsValue")
        sizePolicy3.setHeightForWidth(self.totalStopsValue.sizePolicy().hasHeightForWidth())
        self.totalStopsValue.setSizePolicy(sizePolicy3)

        self.horizontalLayout_6.addWidget(self.totalStopsValue)

        self.estimatedLabel = QLabel(self.ParametersMeasurementFrame)
        self.estimatedLabel.setObjectName(u"estimatedLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(2)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.estimatedLabel.sizePolicy().hasHeightForWidth())
        self.estimatedLabel.setSizePolicy(sizePolicy4)
        self.estimatedLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.estimatedLabel)

        self.estimateValueLabel = QLabel(self.ParametersMeasurementFrame)
        self.estimateValueLabel.setObjectName(u"estimateValueLabel")
        sizePolicy4.setHeightForWidth(self.estimateValueLabel.sizePolicy().hasHeightForWidth())
        self.estimateValueLabel.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.estimateValueLabel)

        self.helpButton = QPushButton(self.ParametersMeasurementFrame)
        self.helpButton.setObjectName(u"helpButton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.helpButton)


        self.verticalLayout_2.addWidget(self.ParametersMeasurementFrame)


        self.verticalLayout.addWidget(self.GraphicStatusFrame)

        self.SettingsFitFrame = QFrame(G2)
        self.SettingsFitFrame.setObjectName(u"SettingsFitFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(4)
        sizePolicy6.setHeightForWidth(self.SettingsFitFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFitFrame.setSizePolicy(sizePolicy6)
        self.SettingsFitFrame.setAutoFillBackground(True)
        self.SettingsFitFrame.setFrameShape(QFrame.NoFrame)
        self.SettingsFitFrame.setFrameShadow(QFrame.Sunken)
        self.SettingsFitFrame.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.SettingsFitFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.SettingsFrame = QFrame(self.SettingsFitFrame)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(3)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy7)
        self.SettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.SettingsFrame)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.StopChannelFrame = QFrame(self.SettingsFrame)
        self.StopChannelFrame.setObjectName(u"StopChannelFrame")
        self.StopChannelFrame.setFrameShape(QFrame.StyledPanel)
        self.StopChannelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.StopChannelFrame)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.stopChannelLabel = QLabel(self.StopChannelFrame)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")

        self.horizontalLayout_10.addWidget(self.stopChannelLabel)

        self.stopChannelComboBox = QComboBox(self.StopChannelFrame)
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.setObjectName(u"stopChannelComboBox")

        self.horizontalLayout_10.addWidget(self.stopChannelComboBox)


        self.verticalLayout_3.addWidget(self.StopChannelFrame)

        self.CoincidenceWindowFrame = QFrame(self.SettingsFrame)
        self.CoincidenceWindowFrame.setObjectName(u"CoincidenceWindowFrame")
        self.CoincidenceWindowFrame.setFrameShape(QFrame.StyledPanel)
        self.CoincidenceWindowFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.CoincidenceWindowFrame)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.coincidenceWindowLabel = QLabel(self.CoincidenceWindowFrame)
        self.coincidenceWindowLabel.setObjectName(u"coincidenceWindowLabel")

        self.horizontalLayout_11.addWidget(self.coincidenceWindowLabel)

        self.coincidenceWindowComboBox = QComboBox(self.CoincidenceWindowFrame)
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.addItem("")
        self.coincidenceWindowComboBox.setObjectName(u"coincidenceWindowComboBox")

        self.horizontalLayout_11.addWidget(self.coincidenceWindowComboBox)


        self.verticalLayout_3.addWidget(self.CoincidenceWindowFrame)

        self.NumberBinsFrame = QFrame(self.SettingsFrame)
        self.NumberBinsFrame.setObjectName(u"NumberBinsFrame")
        self.NumberBinsFrame.setFrameShape(QFrame.StyledPanel)
        self.NumberBinsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.NumberBinsFrame)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.timeRangeLabel = QLabel(self.NumberBinsFrame)
        self.timeRangeLabel.setObjectName(u"timeRangeLabel")

        self.horizontalLayout_12.addWidget(self.timeRangeLabel)

        self.numberBinsComboBox = QComboBox(self.NumberBinsFrame)
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.addItem("")
        self.numberBinsComboBox.setObjectName(u"numberBinsComboBox")

        self.horizontalLayout_12.addWidget(self.numberBinsComboBox)


        self.verticalLayout_3.addWidget(self.NumberBinsFrame)

        self.ExternalDelayFrame = QFrame(self.SettingsFrame)
        self.ExternalDelayFrame.setObjectName(u"ExternalDelayFrame")
        self.ExternalDelayFrame.setFrameShape(QFrame.StyledPanel)
        self.ExternalDelayFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.ExternalDelayFrame)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.externalDelayLabel = QLabel(self.ExternalDelayFrame)
        self.externalDelayLabel.setObjectName(u"externalDelayLabel")

        self.horizontalLayout_13.addWidget(self.externalDelayLabel)

        self.externalDelaySpinBox = QDoubleSpinBox(self.ExternalDelayFrame)
        self.externalDelaySpinBox.setObjectName(u"externalDelaySpinBox")
        self.externalDelaySpinBox.setDecimals(3)
        self.externalDelaySpinBox.setMaximum(4000.000000000000000)

        self.horizontalLayout_13.addWidget(self.externalDelaySpinBox)


        self.verticalLayout_3.addWidget(self.ExternalDelayFrame)

        self.MaximumTimeFrame = QFrame(self.SettingsFrame)
        self.MaximumTimeFrame.setObjectName(u"MaximumTimeFrame")
        self.MaximumTimeFrame.setFrameShape(QFrame.StyledPanel)
        self.MaximumTimeFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.MaximumTimeFrame)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.maximumTimeLabel = QLabel(self.MaximumTimeFrame)
        self.maximumTimeLabel.setObjectName(u"maximumTimeLabel")

        self.horizontalLayout_16.addWidget(self.maximumTimeLabel)

        self.maximumTimeValue = QLabel(self.MaximumTimeFrame)
        self.maximumTimeValue.setObjectName(u"maximumTimeValue")

        self.horizontalLayout_16.addWidget(self.maximumTimeValue)


        self.verticalLayout_3.addWidget(self.MaximumTimeFrame)

        self.tabWidget = QTabWidget(self.SettingsFrame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(True)
        self.Manual = QWidget()
        self.Manual.setObjectName(u"Manual")
        self.verticalLayout_9 = QVBoxLayout(self.Manual)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.StartStopFrame = QFrame(self.Manual)
        self.StartStopFrame.setObjectName(u"StartStopFrame")
        self.StartStopFrame.setEnabled(True)
        self.StartStopFrame.setFrameShape(QFrame.NoFrame)
        self.StartStopFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.StartStopFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.startButton = QPushButton(self.StartStopFrame)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_2.addWidget(self.startButton)

        self.stopButton = QPushButton(self.StartStopFrame)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.clearButton = QPushButton(self.StartStopFrame)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout_2.addWidget(self.clearButton)


        self.verticalLayout_9.addWidget(self.StartStopFrame)

        self.tabWidget.addTab(self.Manual, "")
        self.BySize = QWidget()
        self.BySize.setObjectName(u"BySize")
        self.verticalLayout_10 = QVBoxLayout(self.BySize)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame = QFrame(self.BySize)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.numberMeasurementsLabel = QLabel(self.frame)
        self.numberMeasurementsLabel.setObjectName(u"numberMeasurementsLabel")

        self.horizontalLayout_14.addWidget(self.numberMeasurementsLabel)

        self.numberMeasurementsSpinBox = QSpinBox(self.frame)
        self.numberMeasurementsSpinBox.setObjectName(u"numberMeasurementsSpinBox")
        self.numberMeasurementsSpinBox.setMinimum(1000)
        self.numberMeasurementsSpinBox.setMaximum(999999999)

        self.horizontalLayout_14.addWidget(self.numberMeasurementsSpinBox)


        self.verticalLayout_10.addWidget(self.frame)

        self.FrameMeasurement = QFrame(self.BySize)
        self.FrameMeasurement.setObjectName(u"FrameMeasurement")
        self.FrameMeasurement.setFrameShape(QFrame.StyledPanel)
        self.FrameMeasurement.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.FrameMeasurement)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.startLimitedButton = QPushButton(self.FrameMeasurement)
        self.startLimitedButton.setObjectName(u"startLimitedButton")

        self.horizontalLayout_8.addWidget(self.startLimitedButton)

        self.stopLimitedButton = QPushButton(self.FrameMeasurement)
        self.stopLimitedButton.setObjectName(u"stopLimitedButton")

        self.horizontalLayout_8.addWidget(self.stopLimitedButton)

        self.clearLimitedButton = QPushButton(self.FrameMeasurement)
        self.clearLimitedButton.setObjectName(u"clearLimitedButton")

        self.horizontalLayout_8.addWidget(self.clearLimitedButton)


        self.verticalLayout_10.addWidget(self.FrameMeasurement)

        self.tabWidget.addTab(self.BySize, "")
        self.AutoClear = QWidget()
        self.AutoClear.setObjectName(u"AutoClear")
        self.verticalLayout_11 = QVBoxLayout(self.AutoClear)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_2 = QFrame(self.AutoClear)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.everyClearLabel = QLabel(self.frame_2)
        self.everyClearLabel.setObjectName(u"everyClearLabel")

        self.horizontalLayout_15.addWidget(self.everyClearLabel)

        self.autoClearSpinBox = QSpinBox(self.frame_2)
        self.autoClearSpinBox.setObjectName(u"autoClearSpinBox")
        self.autoClearSpinBox.setMinimum(1)
        self.autoClearSpinBox.setMaximum(999999999)

        self.horizontalLayout_15.addWidget(self.autoClearSpinBox)


        self.verticalLayout_11.addWidget(self.frame_2)

        self.FrameStartStopClear = QFrame(self.AutoClear)
        self.FrameStartStopClear.setObjectName(u"FrameStartStopClear")
        self.FrameStartStopClear.setFrameShape(QFrame.StyledPanel)
        self.FrameStartStopClear.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.FrameStartStopClear)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.startAutoClearButton = QPushButton(self.FrameStartStopClear)
        self.startAutoClearButton.setObjectName(u"startAutoClearButton")

        self.horizontalLayout_9.addWidget(self.startAutoClearButton)

        self.stopAutoClearButton = QPushButton(self.FrameStartStopClear)
        self.stopAutoClearButton.setObjectName(u"stopAutoClearButton")

        self.horizontalLayout_9.addWidget(self.stopAutoClearButton)

        self.cleanAutoClearButton = QPushButton(self.FrameStartStopClear)
        self.cleanAutoClearButton.setObjectName(u"cleanAutoClearButton")

        self.horizontalLayout_9.addWidget(self.cleanAutoClearButton)


        self.verticalLayout_11.addWidget(self.FrameStartStopClear)

        self.tabWidget.addTab(self.AutoClear, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.SaveFrame = QFrame(self.SettingsFrame)
        self.SaveFrame.setObjectName(u"SaveFrame")
        self.SaveFrame.setFrameShape(QFrame.NoFrame)
        self.SaveFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.SaveFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.saveDataButton = QPushButton(self.SaveFrame)
        self.saveDataButton.setObjectName(u"saveDataButton")

        self.horizontalLayout_3.addWidget(self.saveDataButton)

        self.savePlotButton = QPushButton(self.SaveFrame)
        self.savePlotButton.setObjectName(u"savePlotButton")

        self.horizontalLayout_3.addWidget(self.savePlotButton)


        self.verticalLayout_3.addWidget(self.SaveFrame)


        self.horizontalLayout.addWidget(self.SettingsFrame)

        self.FitFrame = QFrame(self.SettingsFitFrame)
        self.FitFrame.setObjectName(u"FitFrame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(7)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.FitFrame.sizePolicy().hasHeightForWidth())
        self.FitFrame.setSizePolicy(sizePolicy8)
        self.FitFrame.setFrameShape(QFrame.NoFrame)
        self.FitFrame.setFrameShadow(QFrame.Plain)
        self.FitFrame.setLineWidth(0)
        self.verticalLayout_6 = QVBoxLayout(self.FitFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.FitFrame)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(9)
        sizePolicy9.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy9)
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Sunken)
        self.frame_11.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.TunningGraphicFrame = QFrame(self.frame_11)
        self.TunningGraphicFrame.setObjectName(u"TunningGraphicFrame")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(5)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.TunningGraphicFrame.sizePolicy().hasHeightForWidth())
        self.TunningGraphicFrame.setSizePolicy(sizePolicy10)
        self.TunningGraphicFrame.setFrameShape(QFrame.NoFrame)
        self.TunningGraphicFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.TunningGraphicFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.ApplyFitFrame = QFrame(self.TunningGraphicFrame)
        self.ApplyFitFrame.setObjectName(u"ApplyFitFrame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(7)
        sizePolicy11.setHeightForWidth(self.ApplyFitFrame.sizePolicy().hasHeightForWidth())
        self.ApplyFitFrame.setSizePolicy(sizePolicy11)
        self.ApplyFitFrame.setFrameShape(QFrame.StyledPanel)
        self.ApplyFitFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_7 = QVBoxLayout(self.ApplyFitFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.SelectFitFrame = QFrame(self.ApplyFitFrame)
        self.SelectFitFrame.setObjectName(u"SelectFitFrame")
        self.SelectFitFrame.setFrameShape(QFrame.NoFrame)
        self.SelectFitFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.SelectFitFrame)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.fitEquationLabel = QLabel(self.SelectFitFrame)
        self.fitEquationLabel.setObjectName(u"fitEquationLabel")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(1)
        sizePolicy12.setHeightForWidth(self.fitEquationLabel.sizePolicy().hasHeightForWidth())
        self.fitEquationLabel.setSizePolicy(sizePolicy12)

        self.horizontalLayout_7.addWidget(self.fitEquationLabel)

        self.equationComboBox = QComboBox(self.SelectFitFrame)
        self.equationComboBox.addItem("")
        self.equationComboBox.addItem("")
        self.equationComboBox.addItem("")
        self.equationComboBox.setObjectName(u"equationComboBox")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(1)
        sizePolicy13.setHeightForWidth(self.equationComboBox.sizePolicy().hasHeightForWidth())
        self.equationComboBox.setSizePolicy(sizePolicy13)

        self.horizontalLayout_7.addWidget(self.equationComboBox)


        self.verticalLayout_7.addWidget(self.SelectFitFrame)

        self.equationLabel = QLabel(self.ApplyFitFrame)
        self.equationLabel.setObjectName(u"equationLabel")
        sizePolicy11.setHeightForWidth(self.equationLabel.sizePolicy().hasHeightForWidth())
        self.equationLabel.setSizePolicy(sizePolicy11)
        font = QFont()
        font.setPointSize(22)
        self.equationLabel.setFont(font)
        self.equationLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.equationLabel)

        self.applyFitButton = QPushButton(self.ApplyFitFrame)
        self.applyFitButton.setObjectName(u"applyFitButton")
        sizePolicy14 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(1)
        sizePolicy14.setHeightForWidth(self.applyFitButton.sizePolicy().hasHeightForWidth())
        self.applyFitButton.setSizePolicy(sizePolicy14)

        self.verticalLayout_7.addWidget(self.applyFitButton)


        self.verticalLayout_4.addWidget(self.ApplyFitFrame)


        self.horizontalLayout_5.addWidget(self.TunningGraphicFrame)

        self.ParametersFrame = QFrame(self.frame_11)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        sizePolicy10.setHeightForWidth(self.ParametersFrame.sizePolicy().hasHeightForWidth())
        self.ParametersFrame.setSizePolicy(sizePolicy10)
        self.ParametersFrame.setFrameShape(QFrame.StyledPanel)
        self.ParametersFrame.setFrameShadow(QFrame.Sunken)
        self.ParametersFrame.setLineWidth(0)
        self.verticalLayout_5 = QVBoxLayout(self.ParametersFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.fitParametersLabel = QLabel(self.ParametersFrame)
        self.fitParametersLabel.setObjectName(u"fitParametersLabel")

        self.verticalLayout_5.addWidget(self.fitParametersLabel)

        self.parametersTable = QTableWidget(self.ParametersFrame)
        if (self.parametersTable.columnCount() < 4):
            self.parametersTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.parametersTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.parametersTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.parametersTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.parametersTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.parametersTable.setObjectName(u"parametersTable")

        self.verticalLayout_5.addWidget(self.parametersTable)

        self.initialParametersButton = QPushButton(self.ParametersFrame)
        self.initialParametersButton.setObjectName(u"initialParametersButton")

        self.verticalLayout_5.addWidget(self.initialParametersButton)


        self.horizontalLayout_5.addWidget(self.ParametersFrame)


        self.verticalLayout_6.addWidget(self.frame_11)

        self.StatusFrame = QFrame(self.FitFrame)
        self.StatusFrame.setObjectName(u"StatusFrame")
        sizePolicy12.setHeightForWidth(self.StatusFrame.sizePolicy().hasHeightForWidth())
        self.StatusFrame.setSizePolicy(sizePolicy12)
        self.StatusFrame.setFrameShape(QFrame.StyledPanel)
        self.StatusFrame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.stateLabel = QLabel(self.StatusFrame)
        self.stateLabel.setObjectName(u"stateLabel")
        sizePolicy3.setHeightForWidth(self.stateLabel.sizePolicy().hasHeightForWidth())
        self.stateLabel.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.stateLabel)

        self.stateValueLabel = QLabel(self.StatusFrame)
        self.stateValueLabel.setObjectName(u"stateValueLabel")
        sizePolicy15 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy15.setHorizontalStretch(8)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.stateValueLabel.sizePolicy().hasHeightForWidth())
        self.stateValueLabel.setSizePolicy(sizePolicy15)

        self.horizontalLayout_4.addWidget(self.stateValueLabel)

        self.colorLabel = QLabel(self.StatusFrame)
        self.colorLabel.setObjectName(u"colorLabel")
        sizePolicy3.setHeightForWidth(self.colorLabel.sizePolicy().hasHeightForWidth())
        self.colorLabel.setSizePolicy(sizePolicy3)
        self.colorLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.colorLabel)


        self.verticalLayout_6.addWidget(self.StatusFrame)


        self.horizontalLayout.addWidget(self.FitFrame)


        self.verticalLayout.addWidget(self.SettingsFitFrame)


        self.retranslateUi(G2)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(G2)
        self.guiChanges()
    # setupUi

    def retranslateUi(self, G2):
        G2.setWindowTitle(QCoreApplication.translate("G2", u"Form", None))
        self.totalStartsLabel.setText(QCoreApplication.translate("G2", u"Total Starts:", None))
        self.totalStartsValue.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.totalStopsLabel.setText(QCoreApplication.translate("G2", u"Total Stops:", None))
        self.totalStopsValue.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.estimatedLabel.setText(QCoreApplication.translate("G2", u"Counts per second:", None))
        self.estimateValueLabel.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.helpButton.setText(QCoreApplication.translate("G2", u"Help", None))
        self.stopChannelLabel.setText(QCoreApplication.translate("G2", u"Stop Channel:", None))
        self.stopChannelComboBox.setItemText(0, QCoreApplication.translate("G2", u"Channel A", None))
        self.stopChannelComboBox.setItemText(1, QCoreApplication.translate("G2", u"Channel B", None))
        self.stopChannelComboBox.setItemText(2, QCoreApplication.translate("G2", u"Channel C", None))
        self.stopChannelComboBox.setItemText(3, QCoreApplication.translate("G2", u"Channel D", None))

        self.coincidenceWindowLabel.setText(QCoreApplication.translate("G2", u"Coincidence window:", None))
        self.coincidenceWindowComboBox.setItemText(0, QCoreApplication.translate("G2", u"480 ps", None))
        self.coincidenceWindowComboBox.setItemText(1, QCoreApplication.translate("G2", u"960 ps", None))
        self.coincidenceWindowComboBox.setItemText(2, QCoreApplication.translate("G2", u"2 ns", None))
        self.coincidenceWindowComboBox.setItemText(3, QCoreApplication.translate("G2", u"4 ns", None))
        self.coincidenceWindowComboBox.setItemText(4, QCoreApplication.translate("G2", u"8 ns", None))
        self.coincidenceWindowComboBox.setItemText(5, QCoreApplication.translate("G2", u"16 ns", None))
        self.coincidenceWindowComboBox.setItemText(6, QCoreApplication.translate("G2", u"32 ns", None))
        self.coincidenceWindowComboBox.setItemText(7, QCoreApplication.translate("G2", u"64 ns", None))
        self.coincidenceWindowComboBox.setItemText(8, QCoreApplication.translate("G2", u"128 ns", None))
        self.coincidenceWindowComboBox.setItemText(9, QCoreApplication.translate("G2", u"256 ns", None))
        self.coincidenceWindowComboBox.setItemText(10, QCoreApplication.translate("G2", u"512 ns", None))
        self.coincidenceWindowComboBox.setItemText(11, QCoreApplication.translate("G2", u"1 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(12, QCoreApplication.translate("G2", u"2 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(13, QCoreApplication.translate("G2", u"4 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(14, QCoreApplication.translate("G2", u"8 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(15, QCoreApplication.translate("G2", u"16 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(16, QCoreApplication.translate("G2", u"32 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(17, QCoreApplication.translate("G2", u"64 \u00b5s", None))
        self.coincidenceWindowComboBox.setItemText(18, QCoreApplication.translate("G2", u"100 \u00b5s", None))

        self.timeRangeLabel.setText(QCoreApplication.translate("G2", u"Number of bins:", None))
        self.numberBinsComboBox.setItemText(0, QCoreApplication.translate("G2", u"10", None))
        self.numberBinsComboBox.setItemText(1, QCoreApplication.translate("G2", u"20", None))
        self.numberBinsComboBox.setItemText(2, QCoreApplication.translate("G2", u"30", None))
        self.numberBinsComboBox.setItemText(3, QCoreApplication.translate("G2", u"40", None))
        self.numberBinsComboBox.setItemText(4, QCoreApplication.translate("G2", u"50", None))
        self.numberBinsComboBox.setItemText(5, QCoreApplication.translate("G2", u"60", None))
        self.numberBinsComboBox.setItemText(6, QCoreApplication.translate("G2", u"70", None))
        self.numberBinsComboBox.setItemText(7, QCoreApplication.translate("G2", u"80", None))
        self.numberBinsComboBox.setItemText(8, QCoreApplication.translate("G2", u"90", None))
        self.numberBinsComboBox.setItemText(9, QCoreApplication.translate("G2", u"100", None))
        self.numberBinsComboBox.setItemText(10, QCoreApplication.translate("G2", u"200", None))
        self.numberBinsComboBox.setItemText(11, QCoreApplication.translate("G2", u"300", None))
        self.numberBinsComboBox.setItemText(12, QCoreApplication.translate("G2", u"400", None))
        self.numberBinsComboBox.setItemText(13, QCoreApplication.translate("G2", u"500", None))
        self.numberBinsComboBox.setItemText(14, QCoreApplication.translate("G2", u"600", None))
        self.numberBinsComboBox.setItemText(15, QCoreApplication.translate("G2", u"700", None))
        self.numberBinsComboBox.setItemText(16, QCoreApplication.translate("G2", u"800", None))
        self.numberBinsComboBox.setItemText(17, QCoreApplication.translate("G2", u"900", None))
        self.numberBinsComboBox.setItemText(18, QCoreApplication.translate("G2", u"1000", None))
        self.numberBinsComboBox.setItemText(19, QCoreApplication.translate("G2", u"2000", None))
        self.numberBinsComboBox.setItemText(20, QCoreApplication.translate("G2", u"3000", None))
        self.numberBinsComboBox.setItemText(21, QCoreApplication.translate("G2", u"4000", None))
        self.numberBinsComboBox.setItemText(22, QCoreApplication.translate("G2", u"5000", None))
        self.numberBinsComboBox.setItemText(23, QCoreApplication.translate("G2", u"6000", None))
        self.numberBinsComboBox.setItemText(24, QCoreApplication.translate("G2", u"7000", None))
        self.numberBinsComboBox.setItemText(25, QCoreApplication.translate("G2", u"8000", None))
        self.numberBinsComboBox.setItemText(26, QCoreApplication.translate("G2", u"9000", None))
        self.numberBinsComboBox.setItemText(27, QCoreApplication.translate("G2", u"10000", None))

        self.externalDelayLabel.setText(QCoreApplication.translate("G2", u"External delay:", None))
        self.externalDelaySpinBox.setPrefix("")
        self.externalDelaySpinBox.setSuffix(QCoreApplication.translate("G2", u" \u03bcs", None))
        self.maximumTimeLabel.setText(QCoreApplication.translate("G2", u"Maximum time:", None))
        self.maximumTimeValue.setText(QCoreApplication.translate("G2", u"value", None))
        self.startButton.setText(QCoreApplication.translate("G2", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("G2", u"Stop", None))
        self.clearButton.setText(QCoreApplication.translate("G2", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Manual), QCoreApplication.translate("G2", u"Manual", None))
        self.numberMeasurementsLabel.setText(QCoreApplication.translate("G2", u"Number of measurements:", None))
        self.startLimitedButton.setText(QCoreApplication.translate("G2", u"Start", None))
        self.stopLimitedButton.setText(QCoreApplication.translate("G2", u"Stop", None))
        self.clearLimitedButton.setText(QCoreApplication.translate("G2", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BySize), QCoreApplication.translate("G2", u"By size", None))
        self.everyClearLabel.setText(QCoreApplication.translate("G2", u"Every:", None))
        self.autoClearSpinBox.setSuffix(QCoreApplication.translate("G2", u" s", None))
        self.startAutoClearButton.setText(QCoreApplication.translate("G2", u"Start", None))
        self.stopAutoClearButton.setText(QCoreApplication.translate("G2", u"Stop", None))
        self.cleanAutoClearButton.setText(QCoreApplication.translate("G2", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AutoClear), QCoreApplication.translate("G2", u"Auto clear", None))
        self.saveDataButton.setText(QCoreApplication.translate("G2", u"Save Data", None))
        self.savePlotButton.setText(QCoreApplication.translate("G2", u"Save Plot", None))
        self.fitEquationLabel.setText(QCoreApplication.translate("G2", u"Fit equation:", None))
        self.equationComboBox.setItemText(0, QCoreApplication.translate("G2", u"Thermal", None))
        self.equationComboBox.setItemText(1, QCoreApplication.translate("G2", u"Antibunching", None))
        self.equationComboBox.setItemText(2, QCoreApplication.translate("G2", u"Three level system", None))

        self.equationLabel.setText(QCoreApplication.translate("G2", u"Equation", None))
        self.applyFitButton.setText(QCoreApplication.translate("G2", u"Apply", None))
        self.fitParametersLabel.setText(QCoreApplication.translate("G2", u"Fit parameters", None))
        ___qtablewidgetitem = self.parametersTable.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("G2", u"Value", None));
        ___qtablewidgetitem1 = self.parametersTable.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("G2", u"Std Dev", None));
        ___qtablewidgetitem2 = self.parametersTable.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("G2", u"Units", None));
        self.initialParametersButton.setText(QCoreApplication.translate("G2", u"Set initial parameters", None))
        self.stateLabel.setText(QCoreApplication.translate("G2", u"State", None))
        self.stateValueLabel.setText(QCoreApplication.translate("G2", u"No running measurement", None))
        self.colorLabel.setText(QCoreApplication.translate("G2", u"Color", None))
    # retranslateUi


    def guiChanges(self):
        self.drawColorPoint()
        self.equationComboBox.currentIndexChanged.connect(self.setChangeComboBox)
        self.pixMapThermal=QPixmap("./Sources/ThermalEquation.png")
        self.pixMapAntiBunching=QPixmap("./Sources/AntibunchingEquation.png")
        self.pixMapThreeLevel=QPixmap("./Sources/ThreeLevelSystemEquation.png")
        self.coincidenceWindowComboBox.currentIndexChanged.connect(self.setNumberBins)
        self.numberBinsComboBox.currentIndexChanged.connect(self.setMaximumTimeValue)
        self.setLabelEquation("Thermal")
        self.defineValuesBinsComboBox()

    def defineValuesBinsComboBox(self):
        self.numberOfBinsValues = [ "10","20","30","40","50","60","70","80","90","100"
                                   ,"200","300","400","500","600","700","800","900","1000",
                                   "2000","3000","4000","5000","6000","7000","8000","9000","10000"]
        initialValues=["50","60","70","80","90","100"
                        ,"200","300","400","500","600","700","800","900","1000",
                        "2000","3000","4000","5000","6000","7000","8000","9000","10000"]
        self.numberBinsComboBox.clear()
        self.numberBinsComboBox.addItems(initialValues)
        self.numberBinsComboBox.setCurrentIndex(0)
    
    def drawColorPoint(self):
        pixmap = QPixmap(self.colorLabel.size())
        pixmap.fill(Qt.transparent)  

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        painter.setBrush(QColor(128, 128, 128))  
        painter.setPen(Qt.NoPen)

        # Definir el tamaño del punto (círculo)
        point_size = min(self.colorLabel.width(), self.colorLabel.height()) // 2

        # Calcular la posición del círculo para que quede centrado
        x = (self.colorLabel.width() - point_size) // 2
        y = (self.colorLabel.height() - point_size) // 2

        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.colorLabel.setPixmap(pixmap)
    
    def setChangeComboBox(self):
        equation=self.equationComboBox.currentText()
        self.setLabelEquation(equation)
    
    def setLabelEquation(self, equation):
        if equation=="Thermal":
            self.equationLabel.setPixmap(self.pixMapThermal)
        elif equation=="Antibunching":
            self.equationLabel.setPixmap(self.pixMapAntiBunching)
        elif equation=="Three level system":
            self.equationLabel.setPixmap(self.pixMapThreeLevel)
    
    def setNumberBins(self):
        binsToAdd=[]
        currentCoincidence=self.coincidenceWindowComboBox.currentText()
        valuePs=self.getNumberPs(currentCoincidence)
        minimumValue=int(self.numberOfBinsValues[0])
        if minimumValue*valuePs<24000:
            minimumBinsNumber=round(24000/valuePs)
            binsToAdd.append(str(minimumBinsNumber))
        else:
            minimumBinsNumber=int(self.numberOfBinsValues[0])
            binsToAdd.append(str(minimumBinsNumber))
        for valueToAddStr in self.numberOfBinsValues:
            valueToAdd=int(valueToAddStr)
            currentRange=valueToAdd*valuePs
            if valueToAdd>minimumBinsNumber and currentRange<=4000000000:
                binsToAdd.append(valueToAddStr)
        self.numberBinsComboBox.clear()
        self.numberBinsComboBox.addItems(binsToAdd)
        self.numberBinsComboBox.setCurrentIndex(0)
        
            
    
    def setMaximumTimeValue(self):
        if self.numberBinsComboBox.currentText()!="":
            currentCoincidence=self.coincidenceWindowComboBox.currentText()
            valuePs=self.getNumberPs(currentCoincidence)
            currentNumberBins=int(self.numberBinsComboBox.currentText())
        
            currentRange=valuePs*currentNumberBins
            currentRangeStr=self.getNumberStr(currentRange)
            self.maximumTimeValue.setText(currentRangeStr)
        
    
    def getNumberPs(self, valueStr):
        units=valueStr.split(" ")
        if units[1]=="ps":
            value=float(units[0])
        elif units[1]=="ns":
            value=float(units[0])*(10**(3))
        elif units[1]=="µs":
            value=float(units[0])*(10**(6))
        return value
    
    def getNumberStr(self, valuePs):
        if valuePs//(10**9)>0:
            valueStr=str(round(valuePs/(10**9),2))+" ms"
        elif valuePs//(10**6)>0:
            valueStr=str(round(valuePs/(10**6),2))+" µs"
        elif valuePs//(10**3)>0:
            valueStr=str(round(valuePs/(10**3),2))+" ns"
        else:
            valueStr=str(valuePs)+" ps"
        return valueStr
        
        
            
    
    def changeCoincidenceSpinBox(self):
        if self.coincidenceWindowSpinBox.value()==1000:
            self.coincidenceWindowSpinBox.setValue(1)
            self.coincidenceWindowSpinBox.setSuffix(" \u03bcs")
            self.coincidenceWindowSpinBox.setMinimum(0)
            self.coincidenceWindowSpinBox.setMaximum(100)
            self.coincidenceWindowSpinBox.setDecimals(3)
            self.coincidenceWindowSpinBox.setSingleStep(0.001)
        if self.coincidenceWindowSpinBox.value()==0.999:
            self.coincidenceWindowSpinBox.setMinimum(1)
            self.coincidenceWindowSpinBox.setMaximum(1001)
            self.coincidenceWindowSpinBox.setValue(999)
            self.coincidenceWindowSpinBox.setSuffix(" ns")
            self.coincidenceWindowSpinBox.setDecimals(0)
            self.coincidenceWindowSpinBox.setSingleStep(1)
            
            
    