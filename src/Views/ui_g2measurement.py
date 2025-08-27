# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'g2NewUieISktS.ui'
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
        G2.resize(893, 735)
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
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.totalStartsLabel = QLabel(self.ParametersMeasurementFrame)
        self.totalStartsLabel.setObjectName(u"totalStartsLabel")

        self.horizontalLayout_6.addWidget(self.totalStartsLabel)

        self.totalStartsValue = QLabel(self.ParametersMeasurementFrame)
        self.totalStartsValue.setObjectName(u"totalStartsValue")

        self.horizontalLayout_6.addWidget(self.totalStartsValue)

        self.totalStopsLabel = QLabel(self.ParametersMeasurementFrame)
        self.totalStopsLabel.setObjectName(u"totalStopsLabel")

        self.horizontalLayout_6.addWidget(self.totalStopsLabel)

        self.totalStopsValue = QLabel(self.ParametersMeasurementFrame)
        self.totalStopsValue.setObjectName(u"totalStopsValue")

        self.horizontalLayout_6.addWidget(self.totalStopsValue)

        self.estimatedLabel = QLabel(self.ParametersMeasurementFrame)
        self.estimatedLabel.setObjectName(u"estimatedLabel")

        self.horizontalLayout_6.addWidget(self.estimatedLabel)

        self.estimateValueLabel = QLabel(self.ParametersMeasurementFrame)
        self.estimateValueLabel.setObjectName(u"estimateValueLabel")

        self.horizontalLayout_6.addWidget(self.estimateValueLabel)

        self.helpButton = QPushButton(self.ParametersMeasurementFrame)
        self.helpButton.setObjectName(u"helpButton")

        self.horizontalLayout_6.addWidget(self.helpButton)


        self.verticalLayout_2.addWidget(self.ParametersMeasurementFrame)


        self.verticalLayout.addWidget(self.GraphicStatusFrame)

        self.SettingsFitFrame = QFrame(G2)
        self.SettingsFitFrame.setObjectName(u"SettingsFitFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(4)
        sizePolicy3.setHeightForWidth(self.SettingsFitFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFitFrame.setSizePolicy(sizePolicy3)
        self.SettingsFitFrame.setAutoFillBackground(True)
        self.SettingsFitFrame.setFrameShape(QFrame.NoFrame)
        self.SettingsFitFrame.setFrameShadow(QFrame.Sunken)
        self.SettingsFitFrame.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.SettingsFitFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.SettingsFrame = QFrame(self.SettingsFitFrame)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(3)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy4)
        self.SettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.SettingsFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stopChannelLabel = QLabel(self.SettingsFrame)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")

        self.verticalLayout_3.addWidget(self.stopChannelLabel)

        self.stopChannelComboBox = QComboBox(self.SettingsFrame)
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.setObjectName(u"stopChannelComboBox")

        self.verticalLayout_3.addWidget(self.stopChannelComboBox)

        self.coincidenceWindowLabel = QLabel(self.SettingsFrame)
        self.coincidenceWindowLabel.setObjectName(u"coincidenceWindowLabel")

        self.verticalLayout_3.addWidget(self.coincidenceWindowLabel)

        self.coincidenceWindowSpinBox = QDoubleSpinBox(self.SettingsFrame)
        self.coincidenceWindowSpinBox.setObjectName(u"coincidenceWindowSpinBox")
        self.coincidenceWindowSpinBox.setDecimals(2)
        self.coincidenceWindowSpinBox.setMaximum(100.000000000000000)
        self.coincidenceWindowSpinBox.setSingleStep(1.000000000000000)

        self.verticalLayout_3.addWidget(self.coincidenceWindowSpinBox)

        self.numberMeasurementsLabel = QLabel(self.SettingsFrame)
        self.numberMeasurementsLabel.setObjectName(u"numberMeasurementsLabel")

        self.verticalLayout_3.addWidget(self.numberMeasurementsLabel)

        self.numberMeasurementsSpinBox = QSpinBox(self.SettingsFrame)
        self.numberMeasurementsSpinBox.setObjectName(u"numberMeasurementsSpinBox")
        self.numberMeasurementsSpinBox.setMinimum(1)
        self.numberMeasurementsSpinBox.setMaximum(999999999)

        self.verticalLayout_3.addWidget(self.numberMeasurementsSpinBox)

        self.timeRangeLabel = QLabel(self.SettingsFrame)
        self.timeRangeLabel.setObjectName(u"timeRangeLabel")

        self.verticalLayout_3.addWidget(self.timeRangeLabel)

        self.timeRangeSpinBox = QSpinBox(self.SettingsFrame)
        self.timeRangeSpinBox.setObjectName(u"timeRangeSpinBox")
        self.timeRangeSpinBox.setMinimum(100)
        self.timeRangeSpinBox.setMaximum(4000)

        self.verticalLayout_3.addWidget(self.timeRangeSpinBox)

        self.StartStopFrame = QFrame(self.SettingsFrame)
        self.StartStopFrame.setObjectName(u"StartStopFrame")
        self.StartStopFrame.setFrameShape(QFrame.NoFrame)
        self.StartStopFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.StartStopFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.startButton = QPushButton(self.StartStopFrame)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_2.addWidget(self.startButton)

        self.stopButton = QPushButton(self.StartStopFrame)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.clearButton = QPushButton(self.StartStopFrame)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout_2.addWidget(self.clearButton)


        self.verticalLayout_3.addWidget(self.StartStopFrame)

        self.SaveFrame = QFrame(self.SettingsFrame)
        self.SaveFrame.setObjectName(u"SaveFrame")
        self.SaveFrame.setFrameShape(QFrame.NoFrame)
        self.SaveFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.SaveFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
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
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(7)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.FitFrame.sizePolicy().hasHeightForWidth())
        self.FitFrame.setSizePolicy(sizePolicy5)
        self.FitFrame.setFrameShape(QFrame.NoFrame)
        self.FitFrame.setFrameShadow(QFrame.Plain)
        self.FitFrame.setLineWidth(0)
        self.verticalLayout_6 = QVBoxLayout(self.FitFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.FitFrame)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(9)
        sizePolicy6.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy6)
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Sunken)
        self.frame_11.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.TunningGraphicFrame = QFrame(self.frame_11)
        self.TunningGraphicFrame.setObjectName(u"TunningGraphicFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(5)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.TunningGraphicFrame.sizePolicy().hasHeightForWidth())
        self.TunningGraphicFrame.setSizePolicy(sizePolicy7)
        self.TunningGraphicFrame.setFrameShape(QFrame.NoFrame)
        self.TunningGraphicFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.TunningGraphicFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.ApplyFitFrame = QFrame(self.TunningGraphicFrame)
        self.ApplyFitFrame.setObjectName(u"ApplyFitFrame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(7)
        sizePolicy8.setHeightForWidth(self.ApplyFitFrame.sizePolicy().hasHeightForWidth())
        self.ApplyFitFrame.setSizePolicy(sizePolicy8)
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
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(1)
        sizePolicy9.setHeightForWidth(self.fitEquationLabel.sizePolicy().hasHeightForWidth())
        self.fitEquationLabel.setSizePolicy(sizePolicy9)

        self.horizontalLayout_7.addWidget(self.fitEquationLabel)

        self.equationComboBox = QComboBox(self.SelectFitFrame)
        self.equationComboBox.addItem("")
        self.equationComboBox.addItem("")
        self.equationComboBox.addItem("")
        self.equationComboBox.setObjectName(u"equationComboBox")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(1)
        sizePolicy10.setHeightForWidth(self.equationComboBox.sizePolicy().hasHeightForWidth())
        self.equationComboBox.setSizePolicy(sizePolicy10)

        self.horizontalLayout_7.addWidget(self.equationComboBox)


        self.verticalLayout_7.addWidget(self.SelectFitFrame)

        self.equationLabel = QLabel(self.ApplyFitFrame)
        self.equationLabel.setObjectName(u"equationLabel")
        sizePolicy8.setHeightForWidth(self.equationLabel.sizePolicy().hasHeightForWidth())
        self.equationLabel.setSizePolicy(sizePolicy8)
        font = QFont()
        font.setPointSize(14)
        self.equationLabel.setFont(font)
        self.equationLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.equationLabel)

        self.applyFitButton = QPushButton(self.ApplyFitFrame)
        self.applyFitButton.setObjectName(u"applyFitButton")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(1)
        sizePolicy11.setHeightForWidth(self.applyFitButton.sizePolicy().hasHeightForWidth())
        self.applyFitButton.setSizePolicy(sizePolicy11)

        self.verticalLayout_7.addWidget(self.applyFitButton)


        self.verticalLayout_4.addWidget(self.ApplyFitFrame)

        self.ExternalDelayFrame = QFrame(self.TunningGraphicFrame)
        self.ExternalDelayFrame.setObjectName(u"ExternalDelayFrame")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(3)
        sizePolicy12.setHeightForWidth(self.ExternalDelayFrame.sizePolicy().hasHeightForWidth())
        self.ExternalDelayFrame.setSizePolicy(sizePolicy12)
        self.ExternalDelayFrame.setFrameShape(QFrame.StyledPanel)
        self.ExternalDelayFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.ExternalDelayFrame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.externalDelayLabel = QLabel(self.ExternalDelayFrame)
        self.externalDelayLabel.setObjectName(u"externalDelayLabel")

        self.verticalLayout_8.addWidget(self.externalDelayLabel)

        self.externalDelaySpinBox = QSpinBox(self.ExternalDelayFrame)
        self.externalDelaySpinBox.setObjectName(u"externalDelaySpinBox")

        self.verticalLayout_8.addWidget(self.externalDelaySpinBox)

        self.applyDelayButton = QPushButton(self.ExternalDelayFrame)
        self.applyDelayButton.setObjectName(u"applyDelayButton")

        self.verticalLayout_8.addWidget(self.applyDelayButton)


        self.verticalLayout_4.addWidget(self.ExternalDelayFrame)


        self.horizontalLayout_5.addWidget(self.TunningGraphicFrame)

        self.ParametersFrame = QFrame(self.frame_11)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        sizePolicy7.setHeightForWidth(self.ParametersFrame.sizePolicy().hasHeightForWidth())
        self.ParametersFrame.setSizePolicy(sizePolicy7)
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
        sizePolicy9.setHeightForWidth(self.StatusFrame.sizePolicy().hasHeightForWidth())
        self.StatusFrame.setSizePolicy(sizePolicy9)
        self.StatusFrame.setFrameShape(QFrame.StyledPanel)
        self.StatusFrame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.stateLabel = QLabel(self.StatusFrame)
        self.stateLabel.setObjectName(u"stateLabel")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(1)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.stateLabel.sizePolicy().hasHeightForWidth())
        self.stateLabel.setSizePolicy(sizePolicy13)

        self.horizontalLayout_4.addWidget(self.stateLabel)

        self.stateValueLabel = QLabel(self.StatusFrame)
        self.stateValueLabel.setObjectName(u"stateValueLabel")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(8)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.stateValueLabel.sizePolicy().hasHeightForWidth())
        self.stateValueLabel.setSizePolicy(sizePolicy14)

        self.horizontalLayout_4.addWidget(self.stateValueLabel)

        self.colorLabel = QLabel(self.StatusFrame)
        self.colorLabel.setObjectName(u"colorLabel")
        sizePolicy13.setHeightForWidth(self.colorLabel.sizePolicy().hasHeightForWidth())
        self.colorLabel.setSizePolicy(sizePolicy13)
        self.colorLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.colorLabel)


        self.verticalLayout_6.addWidget(self.StatusFrame)


        self.horizontalLayout.addWidget(self.FitFrame)


        self.verticalLayout.addWidget(self.SettingsFitFrame)

        self.retranslateUi(G2)
        self.guiChanges()

        QMetaObject.connectSlotsByName(G2)
    # setupUi

    def retranslateUi(self, G2):
        G2.setWindowTitle(QCoreApplication.translate("G2", u"Form", None))
        self.totalStartsLabel.setText(QCoreApplication.translate("G2", u"Total Starts", None))
        self.totalStartsValue.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.totalStopsLabel.setText(QCoreApplication.translate("G2", u"Total Stops:", None))
        self.totalStopsValue.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.estimatedLabel.setText(QCoreApplication.translate("G2", u"N1/T1:", None))
        self.estimateValueLabel.setText(QCoreApplication.translate("G2", u"Not determined yet", None))
        self.helpButton.setText(QCoreApplication.translate("G2", u"Help", None))
        self.stopChannelLabel.setText(QCoreApplication.translate("G2", u"Stop Channel:", None))
        self.stopChannelComboBox.setItemText(0, QCoreApplication.translate("G2", u"Channel A", None))
        self.stopChannelComboBox.setItemText(1, QCoreApplication.translate("G2", u"Channel B", None))
        self.stopChannelComboBox.setItemText(2, QCoreApplication.translate("G2", u"Channel C", None))
        self.stopChannelComboBox.setItemText(3, QCoreApplication.translate("G2", u"Channel D", None))

        self.coincidenceWindowLabel.setText(QCoreApplication.translate("G2", u"Coincidence window:", None))
        self.coincidenceWindowSpinBox.setSuffix(QCoreApplication.translate("G2", u" \u03bcs", None))
        self.numberMeasurementsLabel.setText(QCoreApplication.translate("G2", u"Number of measurements:", None))
        self.timeRangeLabel.setText(QCoreApplication.translate("G2", u"Time range:", None))
        self.timeRangeSpinBox.setSuffix(QCoreApplication.translate("G2", u" \u03bcs", None))
        self.startButton.setText(QCoreApplication.translate("G2", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("G2", u"Stop", None))
        self.clearButton.setText(QCoreApplication.translate("G2", u"Clear", None))
        self.saveDataButton.setText(QCoreApplication.translate("G2", u"Save Data", None))
        self.savePlotButton.setText(QCoreApplication.translate("G2", u"Save Plot", None))
        self.fitEquationLabel.setText(QCoreApplication.translate("G2", u"Fit equation:", None))
        self.equationComboBox.setItemText(0, QCoreApplication.translate("G2", u"Thermal", None))
        self.equationComboBox.setItemText(1, QCoreApplication.translate("G2", u"Antibunching", None))
        self.equationComboBox.setItemText(2, QCoreApplication.translate("G2", u"Three level system", None))

        self.equationLabel.setText(QCoreApplication.translate("G2", u"Equation", None))
        self.applyFitButton.setText(QCoreApplication.translate("G2", u"Apply", None))
        self.externalDelayLabel.setText(QCoreApplication.translate("G2", u"External delay:", None))
        self.applyDelayButton.setText(QCoreApplication.translate("G2", u"Apply", None))
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
        self.setLabelEquation("Thermal")

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
            #self.equationLabel.setText("Ae<sup>-(τ)<sup>2</sup>/(2c<sup>2</sup>)</sup> + B")
            self.equationLabel.setPixmap(self.pixMapThermal)
        elif equation=="Antibunching":
            #self.equationLabel.setText("1- e<sup>-|τ|/t<sub>α</sub></sup>")
            self.equationLabel.setPixmap(self.pixMapAntiBunching)
        elif equation=="Three level system":
            #self.equationLabel.setText("1+p<sub>f</sub><sup>2</sup>(ce<sup>-|τ|/(τ<sub>b</sub>)</sup>-(1+c)e<sup>-|τ|/(τ<sub>a</sub>)</sup>)")
            self.equationLabel.setPixmap(self.pixMapThreeLevel)