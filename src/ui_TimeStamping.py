# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeStampPagekilvzV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TimeStamping(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(934, 643)
        Form.setAutoFillBackground(True)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TimeStampPage = QFrame(Form)
        self.TimeStampPage.setObjectName(u"TimeStampPage")
        self.TimeStampPage.setAutoFillBackground(True)
        self.TimeStampPage.setFrameShape(QFrame.Panel)
        self.TimeStampPage.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.TimeStampPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SettingsMeasurementsFrame = QFrame(self.TimeStampPage)
        self.SettingsMeasurementsFrame.setObjectName(u"SettingsMeasurementsFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SettingsMeasurementsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsMeasurementsFrame.setSizePolicy(sizePolicy)
        self.SettingsMeasurementsFrame.setFrameShape(QFrame.StyledPanel)
        self.SettingsMeasurementsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.SettingsMeasurementsFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.SettingsFrame = QFrame(self.SettingsMeasurementsFrame)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(8)
        sizePolicy1.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.SettingsFrame.setFont(font)
        self.SettingsFrame.setMouseTracking(False)
        self.SettingsFrame.setAcceptDrops(False)
        self.SettingsFrame.setFrameShape(QFrame.Panel)
        self.SettingsFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.SettingsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.EnableChannelsFrame = QFrame(self.SettingsFrame)
        self.EnableChannelsFrame.setObjectName(u"EnableChannelsFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.EnableChannelsFrame.sizePolicy().hasHeightForWidth())
        self.EnableChannelsFrame.setSizePolicy(sizePolicy2)
        self.EnableChannelsFrame.setFrameShape(QFrame.StyledPanel)
        self.EnableChannelsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.EnableChannelsFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.enableChannelsLabel = QLabel(self.EnableChannelsFrame)
        self.enableChannelsLabel.setObjectName(u"enableChannelsLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.enableChannelsLabel.sizePolicy().hasHeightForWidth())
        self.enableChannelsLabel.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.enableChannelsLabel)

        self.enableChannelACheckBox = QCheckBox(self.EnableChannelsFrame)
        self.enableChannelACheckBox.setObjectName(u"enableChannelACheckBox")

        self.verticalLayout_3.addWidget(self.enableChannelACheckBox)

        self.enableChannelBCheckBox = QCheckBox(self.EnableChannelsFrame)
        self.enableChannelBCheckBox.setObjectName(u"enableChannelBCheckBox")

        self.verticalLayout_3.addWidget(self.enableChannelBCheckBox)

        self.enableChannelCCheckBox = QCheckBox(self.EnableChannelsFrame)
        self.enableChannelCCheckBox.setObjectName(u"enableChannelCCheckBox")

        self.verticalLayout_3.addWidget(self.enableChannelCCheckBox)

        self.enableChannelDCheckBox = QCheckBox(self.EnableChannelsFrame)
        self.enableChannelDCheckBox.setObjectName(u"enableChannelDCheckBox")

        self.verticalLayout_3.addWidget(self.enableChannelDCheckBox)


        self.verticalLayout_2.addWidget(self.EnableChannelsFrame)

        self.ScheduleFrame = QFrame(self.SettingsFrame)
        self.ScheduleFrame.setObjectName(u"ScheduleFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(4)
        sizePolicy4.setHeightForWidth(self.ScheduleFrame.sizePolicy().hasHeightForWidth())
        self.ScheduleFrame.setSizePolicy(sizePolicy4)
        self.ScheduleFrame.setFrameShape(QFrame.StyledPanel)
        self.ScheduleFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.ScheduleFrame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.ScheduleMeasurementCheckBox = QCheckBox(self.ScheduleFrame)
        self.ScheduleMeasurementCheckBox.setObjectName(u"ScheduleMeasurementCheckBox")

        self.verticalLayout_8.addWidget(self.ScheduleMeasurementCheckBox)

        self.scheduleDateTime = QDateTimeEdit(self.ScheduleFrame)
        self.scheduleDateTime.setObjectName(u"scheduleDateTime")

        self.verticalLayout_8.addWidget(self.scheduleDateTime)

        self.limitMeasurementsCheckBox = QCheckBox(self.ScheduleFrame)
        self.limitMeasurementsCheckBox.setObjectName(u"limitMeasurementsCheckBox")

        self.verticalLayout_8.addWidget(self.limitMeasurementsCheckBox)

        self.measurementsSpinBox = QSpinBox(self.ScheduleFrame)
        self.measurementsSpinBox.setObjectName(u"measurementsSpinBox")

        self.verticalLayout_8.addWidget(self.measurementsSpinBox)

        self.showTableCheckBox = QCheckBox(self.ScheduleFrame)
        self.showTableCheckBox.setObjectName(u"showTableCheckBox")

        self.verticalLayout_8.addWidget(self.showTableCheckBox)


        self.verticalLayout_2.addWidget(self.ScheduleFrame)

        self.SyncFrame = QFrame(self.SettingsFrame)
        self.SyncFrame.setObjectName(u"SyncFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.SyncFrame.sizePolicy().hasHeightForWidth())
        self.SyncFrame.setSizePolicy(sizePolicy5)
        self.SyncFrame.setFrameShape(QFrame.StyledPanel)
        self.SyncFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.SyncFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.syncLabel = QLabel(self.SyncFrame)
        self.syncLabel.setObjectName(u"syncLabel")

        self.horizontalLayout_5.addWidget(self.syncLabel)

        self.syncComboBox = QComboBox(self.SyncFrame)
        self.syncComboBox.addItem("")
        self.syncComboBox.addItem("")
        self.syncComboBox.addItem("")
        self.syncComboBox.addItem("")
        self.syncComboBox.addItem("")
        self.syncComboBox.addItem("")
        self.syncComboBox.setObjectName(u"syncComboBox")

        self.horizontalLayout_5.addWidget(self.syncComboBox)


        self.verticalLayout_2.addWidget(self.SyncFrame)

        self.StartStopPauseFrame = QFrame(self.SettingsFrame)
        self.StartStopPauseFrame.setObjectName(u"StartStopPauseFrame")
        sizePolicy5.setHeightForWidth(self.StartStopPauseFrame.sizePolicy().hasHeightForWidth())
        self.StartStopPauseFrame.setSizePolicy(sizePolicy5)
        self.StartStopPauseFrame.setFrameShape(QFrame.StyledPanel)
        self.StartStopPauseFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.StartStopPauseFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.startButton = QPushButton(self.StartStopPauseFrame)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_3.addWidget(self.startButton)

        self.pauseButton = QPushButton(self.StartStopPauseFrame)
        self.pauseButton.setObjectName(u"pauseButton")

        self.horizontalLayout_3.addWidget(self.pauseButton)

        self.stopButton = QPushButton(self.StartStopPauseFrame)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_3.addWidget(self.stopButton)


        self.verticalLayout_2.addWidget(self.StartStopPauseFrame)

        self.SaveDataFrame = QFrame(self.SettingsFrame)
        self.SaveDataFrame.setObjectName(u"SaveDataFrame")
        sizePolicy5.setHeightForWidth(self.SaveDataFrame.sizePolicy().hasHeightForWidth())
        self.SaveDataFrame.setSizePolicy(sizePolicy5)
        self.SaveDataFrame.setFrameShape(QFrame.StyledPanel)
        self.SaveDataFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.SaveDataFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.saveDataButton = QPushButton(self.SaveDataFrame)
        self.saveDataButton.setObjectName(u"saveDataButton")

        self.verticalLayout_4.addWidget(self.saveDataButton)


        self.verticalLayout_2.addWidget(self.SaveDataFrame)


        self.verticalLayout_5.addWidget(self.SettingsFrame)

        self.MeasurementsFrame = QFrame(self.SettingsMeasurementsFrame)
        self.MeasurementsFrame.setObjectName(u"MeasurementsFrame")
        sizePolicy2.setHeightForWidth(self.MeasurementsFrame.sizePolicy().hasHeightForWidth())
        self.MeasurementsFrame.setSizePolicy(sizePolicy2)
        self.MeasurementsFrame.setFrameShape(QFrame.Panel)
        self.MeasurementsFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_4 = QHBoxLayout(self.MeasurementsFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.MeasurementsChannelsFrame = QFrame(self.MeasurementsFrame)
        self.MeasurementsChannelsFrame.setObjectName(u"MeasurementsChannelsFrame")
        self.MeasurementsChannelsFrame.setFrameShape(QFrame.StyledPanel)
        self.MeasurementsChannelsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.MeasurementsChannelsFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(self.MeasurementsChannelsFrame)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_6.addWidget(self.label_4)

        self.label_2 = QLabel(self.MeasurementsChannelsFrame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.label_5 = QLabel(self.MeasurementsChannelsFrame)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_6.addWidget(self.label_5)

        self.label_3 = QLabel(self.MeasurementsChannelsFrame)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_6.addWidget(self.label_3)

        self.label_6 = QLabel(self.MeasurementsChannelsFrame)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_6.addWidget(self.label_6)


        self.horizontalLayout_4.addWidget(self.MeasurementsChannelsFrame)

        self.MeasurementsValuesFrame = QFrame(self.MeasurementsFrame)
        self.MeasurementsValuesFrame.setObjectName(u"MeasurementsValuesFrame")
        self.MeasurementsValuesFrame.setFrameShape(QFrame.StyledPanel)
        self.MeasurementsValuesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.MeasurementsValuesFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_7 = QLabel(self.MeasurementsValuesFrame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_7.addWidget(self.label_7)

        self.label_8 = QLabel(self.MeasurementsValuesFrame)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_7.addWidget(self.label_8)

        self.label_9 = QLabel(self.MeasurementsValuesFrame)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_7.addWidget(self.label_9)

        self.label_11 = QLabel(self.MeasurementsValuesFrame)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_7.addWidget(self.label_11)

        self.label_10 = QLabel(self.MeasurementsValuesFrame)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_7.addWidget(self.label_10)


        self.horizontalLayout_4.addWidget(self.MeasurementsValuesFrame)


        self.verticalLayout_5.addWidget(self.MeasurementsFrame)


        self.horizontalLayout_2.addWidget(self.SettingsMeasurementsFrame)

        self.TableStatusFrame = QFrame(self.TimeStampPage)
        self.TableStatusFrame.setObjectName(u"TableStatusFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(6)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.TableStatusFrame.sizePolicy().hasHeightForWidth())
        self.TableStatusFrame.setSizePolicy(sizePolicy6)
        self.TableStatusFrame.setFrameShape(QFrame.Panel)
        self.TableStatusFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout = QVBoxLayout(self.TableStatusFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TableFrame = QFrame(self.TableStatusFrame)
        self.TableFrame.setObjectName(u"TableFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(9)
        sizePolicy7.setHeightForWidth(self.TableFrame.sizePolicy().hasHeightForWidth())
        self.TableFrame.setSizePolicy(sizePolicy7)
        self.TableFrame.setFrameShape(QFrame.StyledPanel)
        self.TableFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.TableFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.tableTimeStamp = QTableWidget(self.TableFrame)
        if (self.tableTimeStamp.columnCount() < 3):
            self.tableTimeStamp.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableTimeStamp.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableTimeStamp.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableTimeStamp.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableTimeStamp.setObjectName(u"tableTimeStamp")
        self.tableTimeStamp.horizontalHeader().setCascadingSectionResizes(False)
        self.tableTimeStamp.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableTimeStamp.horizontalHeader().setStretchLastSection(True)
        self.tableTimeStamp.verticalHeader().setCascadingSectionResizes(False)
        self.tableTimeStamp.verticalHeader().setProperty("showSortIndicator", False)
        self.tableTimeStamp.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_9.addWidget(self.tableTimeStamp)


        self.verticalLayout.addWidget(self.TableFrame)

        self.StatusFrame = QFrame(self.TableStatusFrame)
        self.StatusFrame.setObjectName(u"StatusFrame")
        sizePolicy5.setHeightForWidth(self.StatusFrame.sizePolicy().hasHeightForWidth())
        self.StatusFrame.setSizePolicy(sizePolicy5)
        self.StatusFrame.setFrameShape(QFrame.Panel)
        self.StatusFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_10 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.stateLabe = QLabel(self.StatusFrame)
        self.stateLabe.setObjectName(u"stateLabe")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(45)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.stateLabe.sizePolicy().hasHeightForWidth())
        self.stateLabe.setSizePolicy(sizePolicy8)

        self.horizontalLayout_10.addWidget(self.stateLabe)

        self.valueStateLabel = QLabel(self.StatusFrame)
        self.valueStateLabel.setObjectName(u"valueStateLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(55)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.valueStateLabel.sizePolicy().hasHeightForWidth())
        self.valueStateLabel.setSizePolicy(sizePolicy9)

        self.horizontalLayout_10.addWidget(self.valueStateLabel)

        self.labelColor = QLabel(self.StatusFrame)
        self.labelColor.setObjectName(u"labelColor")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(5)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.labelColor.sizePolicy().hasHeightForWidth())
        self.labelColor.setSizePolicy(sizePolicy10)

        self.horizontalLayout_10.addWidget(self.labelColor)


        self.verticalLayout.addWidget(self.StatusFrame)


        self.horizontalLayout_2.addWidget(self.TableStatusFrame)


        self.horizontalLayout.addWidget(self.TimeStampPage)

        
        self.showTableCheckBox.setChecked(True)
        self.retranslateUi(Form)
        self.drawColorPoint()
        self.tableTimeStamp.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.enableChannelsLabel.setText(QCoreApplication.translate("Form", u"Enable Channels:", None))
        self.enableChannelACheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel A", None))
        self.enableChannelBCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel B", None))
        self.enableChannelCCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel C", None))
        self.enableChannelDCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel D", None))
        self.ScheduleMeasurementCheckBox.setText(QCoreApplication.translate("Form", u"Schedule measurement completion", None))
        self.limitMeasurementsCheckBox.setText(QCoreApplication.translate("Form", u"Limit measurements", None))
        self.showTableCheckBox.setText(QCoreApplication.translate("Form", u"Show table", None))
        self.syncLabel.setText(QCoreApplication.translate("Form", u"Synchronize:", None))
        self.syncComboBox.setItemText(0, QCoreApplication.translate("Form", u"Only with start", None))
        self.syncComboBox.setItemText(1, QCoreApplication.translate("Form", u"30 seconds", None))
        self.syncComboBox.setItemText(2, QCoreApplication.translate("Form", u"1 minute", None))
        self.syncComboBox.setItemText(3, QCoreApplication.translate("Form", u"5 minute", None))
        self.syncComboBox.setItemText(4, QCoreApplication.translate("Form", u"10 minute", None))
        self.syncComboBox.setItemText(5, QCoreApplication.translate("Form", u"1 hour", None))

        self.startButton.setText(QCoreApplication.translate("Form", u"Start adquisition", None))
        self.pauseButton.setText(QCoreApplication.translate("Form", u"Pause adquisiton", None))
        self.stopButton.setText(QCoreApplication.translate("Form", u"Stop adquisition", None))
        self.saveDataButton.setText(QCoreApplication.translate("Form", u"Save Data", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Measurements Channel A", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Measurements Channel B", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Measurements Channel C", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Measurements Channel D", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Total measurements", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"No running measurement", None))
        ___qtablewidgetitem = self.tableTimeStamp.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Stop time", None));
        ___qtablewidgetitem1 = self.tableTimeStamp.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Start time", None));
        ___qtablewidgetitem2 = self.tableTimeStamp.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Channel", None));
        self.stateLabe.setText(QCoreApplication.translate("Form", u"State:", None))
        self.valueStateLabel.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.labelColor.setText(QCoreApplication.translate("Form", u"N", None))
    # retranslateUi













    def drawColorPoint(self):
        pixmap = QPixmap(self.labelColor.size())
        pixmap.fill(Qt.transparent)  

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        painter.setBrush(QColor(128, 128, 128))  
        painter.setPen(Qt.NoPen)

        # Definir el tamaño del punto (círculo)
        point_size = min(self.labelColor.width(), self.labelColor.height()) // 2

        # Calcular la posición del círculo para que quede centrado
        x = (self.labelColor.width() - point_size) // 2
        y = (self.labelColor.height() - point_size) // 2

        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.labelColor.setPixmap(pixmap)
    
    def setFontSizeToLabels(self,size, *labels):
        font = QFont()
        font.setPointSize(size)
        for label in labels:
            label.setFont(font)
