# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'g2NewUihmkJGV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_G2(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(893, 735)
        Form.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GraphicStatusFrame = QFrame(Form)
        self.GraphicStatusFrame.setObjectName(u"GraphicStatusFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.GraphicStatusFrame.sizePolicy().hasHeightForWidth())
        self.GraphicStatusFrame.setSizePolicy(sizePolicy)
        self.GraphicStatusFrame.setAutoFillBackground(True)
        self.GraphicStatusFrame.setFrameShape(QFrame.StyledPanel)
        self.GraphicStatusFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.GraphicStatusFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.GraphicFrame = QFrame(self.GraphicStatusFrame)
        self.GraphicFrame.setObjectName(u"GraphicFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(95)
        sizePolicy1.setHeightForWidth(self.GraphicFrame.sizePolicy().hasHeightForWidth())
        self.GraphicFrame.setSizePolicy(sizePolicy1)
        self.GraphicFrame.setFrameShape(QFrame.StyledPanel)
        self.GraphicFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.GraphicFrame)

        self.StatusFrame = QFrame(self.GraphicStatusFrame)
        self.StatusFrame.setObjectName(u"StatusFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(5)
        sizePolicy2.setHeightForWidth(self.StatusFrame.sizePolicy().hasHeightForWidth())
        self.StatusFrame.setSizePolicy(sizePolicy2)
        self.StatusFrame.setFrameShape(QFrame.StyledPanel)
        self.StatusFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.totalStartsLabel = QLabel(self.StatusFrame)
        self.totalStartsLabel.setObjectName(u"totalStartsLabel")

        self.horizontalLayout_6.addWidget(self.totalStartsLabel)

        self.totalStartsValue = QLabel(self.StatusFrame)
        self.totalStartsValue.setObjectName(u"totalStartsValue")

        self.horizontalLayout_6.addWidget(self.totalStartsValue)

        self.totalStopsLabel = QLabel(self.StatusFrame)
        self.totalStopsLabel.setObjectName(u"totalStopsLabel")

        self.horizontalLayout_6.addWidget(self.totalStopsLabel)

        self.totalStopsValue = QLabel(self.StatusFrame)
        self.totalStopsValue.setObjectName(u"totalStopsValue")

        self.horizontalLayout_6.addWidget(self.totalStopsValue)

        self.helpButton = QPushButton(self.StatusFrame)
        self.helpButton.setObjectName(u"helpButton")

        self.horizontalLayout_6.addWidget(self.helpButton)


        self.verticalLayout_2.addWidget(self.StatusFrame)


        self.verticalLayout.addWidget(self.GraphicStatusFrame)

        self.SettingsFitFrame = QFrame(Form)
        self.SettingsFitFrame.setObjectName(u"SettingsFitFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(4)
        sizePolicy3.setHeightForWidth(self.SettingsFitFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFitFrame.setSizePolicy(sizePolicy3)
        self.SettingsFitFrame.setAutoFillBackground(True)
        self.SettingsFitFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsFitFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout = QHBoxLayout(self.SettingsFitFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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

        self.coincidenceWindowComboBox = QComboBox(self.SettingsFrame)
        self.coincidenceWindowComboBox.setObjectName(u"coincidenceWindowComboBox")

        self.verticalLayout_3.addWidget(self.coincidenceWindowComboBox)

        self.numberMeasurementsLabel = QLabel(self.SettingsFrame)
        self.numberMeasurementsLabel.setObjectName(u"numberMeasurementsLabel")

        self.verticalLayout_3.addWidget(self.numberMeasurementsLabel)

        self.numberMeasurementsSpinBox = QSpinBox(self.SettingsFrame)
        self.numberMeasurementsSpinBox.setObjectName(u"numberMeasurementsSpinBox")

        self.verticalLayout_3.addWidget(self.numberMeasurementsSpinBox)

        self.timeRangeLabel = QLabel(self.SettingsFrame)
        self.timeRangeLabel.setObjectName(u"timeRangeLabel")

        self.verticalLayout_3.addWidget(self.timeRangeLabel)

        self.timeRangeComboBox = QComboBox(self.SettingsFrame)
        self.timeRangeComboBox.setObjectName(u"timeRangeComboBox")

        self.verticalLayout_3.addWidget(self.timeRangeComboBox)

        self.StartStopFrame = QFrame(self.SettingsFrame)
        self.StartStopFrame.setObjectName(u"StartStopFrame")
        self.StartStopFrame.setFrameShape(QFrame.StyledPanel)
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
        self.SaveFrame.setFrameShape(QFrame.StyledPanel)
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
        self.FitFrame.setFrameShape(QFrame.StyledPanel)
        self.FitFrame.setFrameShadow(QFrame.Raised)
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
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.EquationFrame = QFrame(self.frame_11)
        self.EquationFrame.setObjectName(u"EquationFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(5)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.EquationFrame.sizePolicy().hasHeightForWidth())
        self.EquationFrame.setSizePolicy(sizePolicy7)
        self.EquationFrame.setFrameShape(QFrame.StyledPanel)
        self.EquationFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.EquationFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.fitEquationLabel = QLabel(self.EquationFrame)
        self.fitEquationLabel.setObjectName(u"fitEquationLabel")

        self.verticalLayout_4.addWidget(self.fitEquationLabel)

        self.equationComboBox = QComboBox(self.EquationFrame)
        self.equationComboBox.setObjectName(u"equationComboBox")

        self.verticalLayout_4.addWidget(self.equationComboBox)

        self.equationLabel = QLabel(self.EquationFrame)
        self.equationLabel.setObjectName(u"equationLabel")

        self.verticalLayout_4.addWidget(self.equationLabel)

        self.applyButton = QPushButton(self.EquationFrame)
        self.applyButton.setObjectName(u"applyButton")

        self.verticalLayout_4.addWidget(self.applyButton)


        self.horizontalLayout_5.addWidget(self.EquationFrame)

        self.ParametersFrame = QFrame(self.frame_11)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        sizePolicy7.setHeightForWidth(self.ParametersFrame.sizePolicy().hasHeightForWidth())
        self.ParametersFrame.setSizePolicy(sizePolicy7)
        self.ParametersFrame.setFrameShape(QFrame.StyledPanel)
        self.ParametersFrame.setFrameShadow(QFrame.Plain)
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

        self.StatusFrame_2 = QFrame(self.FitFrame)
        self.StatusFrame_2.setObjectName(u"StatusFrame_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(1)
        sizePolicy8.setHeightForWidth(self.StatusFrame_2.sizePolicy().hasHeightForWidth())
        self.StatusFrame_2.setSizePolicy(sizePolicy8)
        self.StatusFrame_2.setFrameShape(QFrame.StyledPanel)
        self.StatusFrame_2.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.StatusFrame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.stateLabel = QLabel(self.StatusFrame_2)
        self.stateLabel.setObjectName(u"stateLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(1)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.stateLabel.sizePolicy().hasHeightForWidth())
        self.stateLabel.setSizePolicy(sizePolicy9)

        self.horizontalLayout_4.addWidget(self.stateLabel)

        self.stateValueLabel = QLabel(self.StatusFrame_2)
        self.stateValueLabel.setObjectName(u"stateValueLabel")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(8)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.stateValueLabel.sizePolicy().hasHeightForWidth())
        self.stateValueLabel.setSizePolicy(sizePolicy10)

        self.horizontalLayout_4.addWidget(self.stateValueLabel)

        self.colorLabel = QLabel(self.StatusFrame_2)
        self.colorLabel.setObjectName(u"colorLabel")
        sizePolicy9.setHeightForWidth(self.colorLabel.sizePolicy().hasHeightForWidth())
        self.colorLabel.setSizePolicy(sizePolicy9)
        self.colorLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.colorLabel)


        self.verticalLayout_6.addWidget(self.StatusFrame_2)


        self.horizontalLayout.addWidget(self.FitFrame)


        self.verticalLayout.addWidget(self.SettingsFitFrame)


        self.retranslateUi(Form)
        self.drawColorPoint()
        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.totalStartsLabel.setText(QCoreApplication.translate("Form", u"Total Starts", None))
        self.totalStartsValue.setText(QCoreApplication.translate("Form", u"NumberStarts#", None))
        self.totalStopsLabel.setText(QCoreApplication.translate("Form", u"Total Stops", None))
        self.totalStopsValue.setText(QCoreApplication.translate("Form", u"NumberStops#", None))
        self.helpButton.setText(QCoreApplication.translate("Form", u"Help", None))
        self.stopChannelLabel.setText(QCoreApplication.translate("Form", u"Channel", None))
        self.stopChannelComboBox.setItemText(0, QCoreApplication.translate("Form", u"Channel A", None))
        self.stopChannelComboBox.setItemText(1, QCoreApplication.translate("Form", u"Channel B", None))
        self.stopChannelComboBox.setItemText(2, QCoreApplication.translate("Form", u"Channel C", None))
        self.stopChannelComboBox.setItemText(3, QCoreApplication.translate("Form", u"Channel D", None))

        self.coincidenceWindowLabel.setText(QCoreApplication.translate("Form", u"Coincidence window:", None))
        self.numberMeasurementsLabel.setText(QCoreApplication.translate("Form", u"Number of measurements", None))
        self.timeRangeLabel.setText(QCoreApplication.translate("Form", u"Time range:", None))
        self.startButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.clearButton.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.saveDataButton.setText(QCoreApplication.translate("Form", u"Save Data", None))
        self.savePlotButton.setText(QCoreApplication.translate("Form", u"Save Plot", None))
        self.fitEquationLabel.setText(QCoreApplication.translate("Form", u"Fit equation:", None))
        self.equationLabel.setText(QCoreApplication.translate("Form", u"Equation", None))
        self.applyButton.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.fitParametersLabel.setText(QCoreApplication.translate("Form", u"Fit parameters", None))
        ___qtablewidgetitem = self.parametersTable.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Value", None));
        ___qtablewidgetitem1 = self.parametersTable.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Std Dev", None));
        ___qtablewidgetitem2 = self.parametersTable.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Units", None));
        self.initialParametersButton.setText(QCoreApplication.translate("Form", u"Set initial parameters", None))
        self.stateLabel.setText(QCoreApplication.translate("Form", u"State", None))
        self.stateValueLabel.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        self.colorLabel.setText(QCoreApplication.translate("Form", u"Color", None))
    # retranslateUi


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

