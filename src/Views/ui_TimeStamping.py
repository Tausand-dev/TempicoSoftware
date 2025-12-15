# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeStampPagecePyeP.ui'
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
        Form.resize(1076, 726)
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
        self.verticalLayout_5.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_5.setSpacing(0)
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
        self.verticalLayout_2.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_2.setSpacing(0)
        self.EnableChannelsFrame = QFrame(self.SettingsFrame)
        self.EnableChannelsFrame.setObjectName(u"EnableChannelsFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.EnableChannelsFrame.sizePolicy().hasHeightForWidth())
        self.EnableChannelsFrame.setSizePolicy(sizePolicy2)
        self.EnableChannelsFrame.setFrameShape(QFrame.StyledPanel)
        self.EnableChannelsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.EnableChannelsFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 7, 10, 0)
        self.verticalLayout_3.setSpacing(0)
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

        self.frameStartStop = QFrame(self.SettingsFrame)
        self.frameStartStop.setObjectName(u"frameStartStop")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(6)
        sizePolicy4.setHeightForWidth(self.frameStartStop.sizePolicy().hasHeightForWidth())
        self.frameStartStop.setSizePolicy(sizePolicy4)
        self.frameStartStop.setFrameShape(QFrame.StyledPanel)
        self.frameStartStop.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frameStartStop)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_8.setSpacing(0)
        self.showTableCheckBox = QCheckBox(self.frameStartStop)
        self.showTableCheckBox.setObjectName(u"showTableCheckBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.showTableCheckBox.sizePolicy().hasHeightForWidth())
        self.showTableCheckBox.setSizePolicy(sizePolicy5)

        self.verticalLayout_8.addWidget(self.showTableCheckBox)

        self.tabStartStopTypes = QTabWidget(self.frameStartStop)
        self.tabStartStopTypes.setObjectName(u"tabStartStopTypes")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(9)
        sizePolicy6.setHeightForWidth(self.tabStartStopTypes.sizePolicy().hasHeightForWidth())
        self.tabStartStopTypes.setSizePolicy(sizePolicy6)
        self.tabStartStopTypes.setAutoFillBackground(True)
        self.tabStartStopTypes.setInputMethodHints(Qt.ImhNone)
        self.tabStartStopTypes.setDocumentMode(False)
        self.tabStartStopTypes.setTabsClosable(False)
        self.tabStartStopTypes.setMovable(False)
        self.tabStartStopTypes.setTabBarAutoHide(False)
        self.tabNormalMeasurement = QWidget()
        self.tabNormalMeasurement.setObjectName(u"tabNormalMeasurement")
        self.tabNormalMeasurement.setAutoFillBackground(True)
        self.verticalLayout_10 = QVBoxLayout(self.tabNormalMeasurement)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.startNormalButton = QPushButton(self.tabNormalMeasurement)
        self.startNormalButton.setObjectName(u"startNormalButton")

        self.verticalLayout_10.addWidget(self.startNormalButton)

        self.pauseNormalButton = QPushButton(self.tabNormalMeasurement)
        self.pauseNormalButton.setObjectName(u"pauseNormalButton")

        self.verticalLayout_10.addWidget(self.pauseNormalButton)

        self.stopNormalButton = QPushButton(self.tabNormalMeasurement)
        self.stopNormalButton.setObjectName(u"stopNormalButton")

        self.verticalLayout_10.addWidget(self.stopNormalButton)

        self.tabStartStopTypes.addTab(self.tabNormalMeasurement, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        
        self.scrollScheduled=QScrollArea()
        self.scrollScheduled.setWidgetResizable(True)
        self.scrollContent=QWidget()
        self.verticalLayout_11 = QVBoxLayout(self.scrollContent)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.labelStartSchedule = QLabel(self.scrollContent)
        self.labelStartSchedule.setObjectName(u"labelStartSchedule")

        self.verticalLayout_11.addWidget(self.labelStartSchedule)

        self.frameStartDateTime = QFrame(self.scrollContent)
        self.frameStartDateTime.setObjectName(u"frameStartDateTime")
        self.frameStartDateTime.setFrameShape(QFrame.StyledPanel)
        self.frameStartDateTime.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frameStartDateTime)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.startDate = QDateEdit(self.frameStartDateTime)
        self.startDate.setObjectName(u"startDate")
        self.startDate.setCalendarPopup(True)
        self.scrollContent.setAutoFillBackground(True)

        self.horizontalLayout_5.addWidget(self.startDate)

        self.startTime = QTimeEdit(self.frameStartDateTime)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setCalendarPopup(False)

        self.horizontalLayout_5.addWidget(self.startTime)


        self.verticalLayout_11.addWidget(self.frameStartDateTime)

        self.labelStopSchedule = QLabel(self.scrollContent)
        self.labelStopSchedule.setObjectName(u"labelStopSchedule")

        self.verticalLayout_11.addWidget(self.labelStopSchedule)

        self.frameStopDateTime = QFrame(self.scrollContent)
        self.frameStopDateTime.setObjectName(u"frameStopDateTime")
        self.frameStopDateTime.setFrameShape(QFrame.StyledPanel)
        self.frameStopDateTime.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frameStopDateTime)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.stopDate = QDateEdit(self.frameStopDateTime)
        self.stopDate.setObjectName(u"stopDate")
        self.stopDate.setCalendarPopup(True)

        self.horizontalLayout_6.addWidget(self.stopDate)

        self.stopTime = QTimeEdit(self.frameStopDateTime)
        self.stopTime.setObjectName(u"stopTime")

        self.horizontalLayout_6.addWidget(self.stopTime)


        self.verticalLayout_11.addWidget(self.frameStopDateTime)

        self.frameStartStopPauseButtons = QFrame(self.scrollContent)
        self.frameStartStopPauseButtons.setObjectName(u"frameStartStopPauseButtons")
        self.frameStartStopPauseButtons.setFrameShape(QFrame.StyledPanel)
        self.frameStartStopPauseButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameStartStopPauseButtons)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.startScheduleButton = QPushButton(self.frameStartStopPauseButtons)
        self.startScheduleButton.setObjectName(u"startScheduleButton")

        self.horizontalLayout_3.addWidget(self.startScheduleButton)

        self.pauseScheduleButton = QPushButton(self.frameStartStopPauseButtons)
        self.pauseScheduleButton.setObjectName(u"pauseScheduleButton")

        self.horizontalLayout_3.addWidget(self.pauseScheduleButton)

        self.stopScheduleButton = QPushButton(self.frameStartStopPauseButtons)
        self.stopScheduleButton.setObjectName(u"stopScheduleButton")

        self.horizontalLayout_3.addWidget(self.stopScheduleButton)


        self.verticalLayout_11.addWidget(self.frameStartStopPauseButtons)
        self.scrollScheduled.setWidget(self.scrollContent)
        self.verticalLayoutScroll=QVBoxLayout(self.tab_2)
        self.verticalLayoutScroll.addWidget(self.scrollScheduled)
        self.verticalLayoutScroll.setContentsMargins(0, 0, 0, 0)
        self.scrollScheduled.setFrameShape(QFrame.NoFrame)
        self.tabStartStopTypes.addTab(self.tab_2, "")
        self.limitedMeasurementsFrame = QWidget()
        self.limitedMeasurementsFrame.setObjectName(u"limitedMeasurementsFrame")
        self.verticalLayout_12 = QVBoxLayout(self.limitedMeasurementsFrame)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.numberMeasurementsLabel = QLabel(self.limitedMeasurementsFrame)
        self.numberMeasurementsLabel.setObjectName(u"numberMeasurementsLabel")

        self.verticalLayout_12.addWidget(self.numberMeasurementsLabel)

        self.numberMeasurementsSpinBox = QSpinBox(self.limitedMeasurementsFrame)
        self.numberMeasurementsSpinBox.setObjectName(u"numberMeasurementsSpinBox")

        self.verticalLayout_12.addWidget(self.numberMeasurementsSpinBox)

        self.frame_6 = QFrame(self.limitedMeasurementsFrame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.startLimitedMeasurementsButton = QPushButton(self.frame_6)
        self.startLimitedMeasurementsButton.setObjectName(u"startLimitedMeasurementsButton")

        self.horizontalLayout_7.addWidget(self.startLimitedMeasurementsButton)
        self.limitedMeasurementsFrame.setAutoFillBackground(True)
        self.pausetLimitedMeasurementsButton = QPushButton(self.frame_6)
        self.pausetLimitedMeasurementsButton.setObjectName(u"pausetLimitedMeasurementsButton")

        self.horizontalLayout_7.addWidget(self.pausetLimitedMeasurementsButton)

        self.stoptLimitedMeasurementsButton = QPushButton(self.frame_6)
        self.stoptLimitedMeasurementsButton.setObjectName(u"stoptLimitedMeasurementsButton")

        self.horizontalLayout_7.addWidget(self.stoptLimitedMeasurementsButton)


        self.verticalLayout_12.addWidget(self.frame_6)

        self.tabStartStopTypes.addTab(self.limitedMeasurementsFrame, "")

        self.verticalLayout_8.addWidget(self.tabStartStopTypes)


        self.verticalLayout_2.addWidget(self.frameStartStop)

        self.SaveDataFrame = QFrame(self.SettingsFrame)
        self.SaveDataFrame.setObjectName(u"SaveDataFrame")
        sizePolicy2.setHeightForWidth(self.SaveDataFrame.sizePolicy().hasHeightForWidth())
        self.SaveDataFrame.setSizePolicy(sizePolicy2)
        self.SaveDataFrame.setFrameShape(QFrame.StyledPanel)
        self.SaveDataFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.SaveDataFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(10, 0, 10, 8)
        self.verticalLayout_4.setSpacing(0)
        self.saveDataAfterCompleteCheckBox = QCheckBox(self.SaveDataFrame)
        self.saveDataAfterCompleteCheckBox.setObjectName(u"saveDataAfterCompleteCheckBox")

        self.verticalLayout_4.addWidget(self.saveDataAfterCompleteCheckBox)

        self.AutoSaveFrame = QFrame(self.SaveDataFrame)
        self.AutoSaveFrame.setObjectName(u"AutoSaveFrame")
        self.AutoSaveFrame.setFrameShape(QFrame.StyledPanel)
        self.AutoSaveFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.AutoSaveFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.everyLabel = QLabel(self.AutoSaveFrame)
        self.everyLabel.setObjectName(u"everyLabel")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(45)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.everyLabel.sizePolicy().hasHeightForWidth())
        self.everyLabel.setSizePolicy(sizePolicy7)

        self.horizontalLayout_8.addWidget(self.everyLabel)

        self.timeAutoSaveComboBox = QComboBox(self.AutoSaveFrame)
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.addItem("")
        self.timeAutoSaveComboBox.setObjectName(u"timeAutoSaveComboBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(60)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.timeAutoSaveComboBox.sizePolicy().hasHeightForWidth())
        self.timeAutoSaveComboBox.setSizePolicy(sizePolicy8)

        self.horizontalLayout_8.addWidget(self.timeAutoSaveComboBox)

        self.helpSaveButton = QPushButton(self.AutoSaveFrame)
        self.helpSaveButton.setObjectName(u"helpSaveButton")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(5)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.helpSaveButton.sizePolicy().hasHeightForWidth())
        self.helpSaveButton.setSizePolicy(sizePolicy9)

        self.horizontalLayout_8.addWidget(self.helpSaveButton)


        self.verticalLayout_4.addWidget(self.AutoSaveFrame)

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
        self.measurementsChannelALabel = QLabel(self.MeasurementsChannelsFrame)
        self.measurementsChannelALabel.setObjectName(u"measurementsChannelALabel")

        self.verticalLayout_6.addWidget(self.measurementsChannelALabel)

        self.measurementsChannelBLabel = QLabel(self.MeasurementsChannelsFrame)
        self.measurementsChannelBLabel.setObjectName(u"measurementsChannelBLabel")

        self.verticalLayout_6.addWidget(self.measurementsChannelBLabel)

        self.measurementsChannelCLabel = QLabel(self.MeasurementsChannelsFrame)
        self.measurementsChannelCLabel.setObjectName(u"measurementsChannelCLabel")

        self.verticalLayout_6.addWidget(self.measurementsChannelCLabel)

        self.measurementsChannelDLabel = QLabel(self.MeasurementsChannelsFrame)
        self.measurementsChannelDLabel.setObjectName(u"measurementsChannelDLabel")

        self.verticalLayout_6.addWidget(self.measurementsChannelDLabel)

        self.totalMeasurementsLabel = QLabel(self.MeasurementsChannelsFrame)
        self.totalMeasurementsLabel.setObjectName(u"totalMeasurementsLabel")

        self.verticalLayout_6.addWidget(self.totalMeasurementsLabel)
        self.verticalLayout_6.setAlignment(Qt.AlignRight)


        self.horizontalLayout_4.addWidget(self.MeasurementsChannelsFrame)

        self.MeasurementsValuesFrame = QFrame(self.MeasurementsFrame)
        self.MeasurementsValuesFrame.setObjectName(u"MeasurementsValuesFrame")
        self.MeasurementsValuesFrame.setFrameShape(QFrame.StyledPanel)
        self.MeasurementsValuesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.MeasurementsValuesFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.valueChannelALabel = QLabel(self.MeasurementsValuesFrame)
        self.valueChannelALabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.valueChannelALabel.setObjectName(u"valueChannelALabel")

        self.verticalLayout_7.addWidget(self.valueChannelALabel)

        self.valueChannelBLabel = QLabel(self.MeasurementsValuesFrame)
        self.valueChannelBLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.valueChannelBLabel.setObjectName(u"valueChannelBLabel")

        self.verticalLayout_7.addWidget(self.valueChannelBLabel)

        self.valueChannelCLabel = QLabel(self.MeasurementsValuesFrame)
        self.valueChannelCLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.valueChannelCLabel.setObjectName(u"valueChannelCLabel")

        self.verticalLayout_7.addWidget(self.valueChannelCLabel)

        self.valueChannelDLabel = QLabel(self.MeasurementsValuesFrame)
        self.valueChannelDLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.valueChannelDLabel.setObjectName(u"valueChannelDLabel")

        self.verticalLayout_7.addWidget(self.valueChannelDLabel)

        self.valueTotalLabel = QLabel(self.MeasurementsValuesFrame)
        self.valueTotalLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.valueTotalLabel.setObjectName(u"valueTotalLabel")

        self.verticalLayout_7.addWidget(self.valueTotalLabel)
        self.verticalLayout_7.setAlignment(Qt.AlignRight)


        self.horizontalLayout_4.addWidget(self.MeasurementsValuesFrame)


        self.verticalLayout_5.addWidget(self.MeasurementsFrame)


        self.horizontalLayout_2.addWidget(self.SettingsMeasurementsFrame)

        self.TableStatusFrame = QFrame(self.TimeStampPage)
        self.TableStatusFrame.setObjectName(u"TableStatusFrame")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(6)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.TableStatusFrame.sizePolicy().hasHeightForWidth())
        self.TableStatusFrame.setSizePolicy(sizePolicy10)
        self.TableStatusFrame.setFrameShape(QFrame.Panel)
        self.TableStatusFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout = QVBoxLayout(self.TableStatusFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TableFrame = QFrame(self.TableStatusFrame)
        self.TableFrame.setObjectName(u"TableFrame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(9)
        sizePolicy11.setHeightForWidth(self.TableFrame.sizePolicy().hasHeightForWidth())
        self.TableFrame.setSizePolicy(sizePolicy11)
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
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(1)
        sizePolicy12.setHeightForWidth(self.StatusFrame.sizePolicy().hasHeightForWidth())
        self.StatusFrame.setSizePolicy(sizePolicy12)
        self.StatusFrame.setFrameShape(QFrame.Panel)
        self.StatusFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_10 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.stateLabe = QLabel(self.StatusFrame)
        self.stateLabe.setObjectName(u"stateLabe")
        sizePolicy7.setHeightForWidth(self.stateLabe.sizePolicy().hasHeightForWidth())
        self.stateLabe.setSizePolicy(sizePolicy7)

        self.horizontalLayout_10.addWidget(self.stateLabe)

        self.valueStateLabel = QLabel(self.StatusFrame)
        self.valueStateLabel.setObjectName(u"valueStateLabel")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(55)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.valueStateLabel.sizePolicy().hasHeightForWidth())
        self.valueStateLabel.setSizePolicy(sizePolicy13)

        self.horizontalLayout_10.addWidget(self.valueStateLabel)

        self.labelColor = QLabel(self.StatusFrame)
        self.labelColor.setObjectName(u"labelColor")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(5)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.labelColor.sizePolicy().hasHeightForWidth())
        self.labelColor.setSizePolicy(sizePolicy14)

        self.horizontalLayout_10.addWidget(self.labelColor)


        self.verticalLayout.addWidget(self.StatusFrame)


        self.horizontalLayout_2.addWidget(self.TableStatusFrame)


        self.horizontalLayout.addWidget(self.TimeStampPage)


        self.retranslateUi(Form)

        self.drawColorPoint()
        

        header = self.tableTimeStamp.horizontalHeader()
        header.setStretchLastSection(False)

        # Primero: calcular tamaño mínimo necesario
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableTimeStamp.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableTimeStamp.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        

        

        self.tabStartStopTypes.setCurrentIndex(0)
        self.settingsForSpinBox()
        self.tableTimeStamp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.enableChannelsLabel.setText(QCoreApplication.translate("Form", u"Enable Channels:", None))
        self.enableChannelACheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel A", None))
        self.enableChannelBCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel B", None))
        self.enableChannelCCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel C", None))
        self.enableChannelDCheckBox.setText(QCoreApplication.translate("Form", u"Enable Channel D", None))
        self.showTableCheckBox.setText(QCoreApplication.translate("Form", u"Show table", None))
        self.saveDataAfterCompleteCheckBox.setText(QCoreApplication.translate("Form", u"Auto save data", None))
        self.startNormalButton.setText(QCoreApplication.translate("Form", u"Start acquisition", None))
        self.pauseNormalButton.setText(QCoreApplication.translate("Form", u"Pause acquisition", None))
        self.stopNormalButton.setText(QCoreApplication.translate("Form", u"Stop acquisition", None))
        self.tabStartStopTypes.setTabText(self.tabStartStopTypes.indexOf(self.tabNormalMeasurement), QCoreApplication.translate("Form", u"Manual", None))
        self.labelStartSchedule.setText(QCoreApplication.translate("Form", u"Schedule date time start measurement", None))
        self.labelStopSchedule.setText(QCoreApplication.translate("Form", u"Schedule date time finish measurement", None))
        self.startScheduleButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.pauseScheduleButton.setText(QCoreApplication.translate("Form", u"Pause", None))
        self.stopScheduleButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.tabStartStopTypes.setTabText(self.tabStartStopTypes.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Scheduled", None))
        self.numberMeasurementsLabel.setText(QCoreApplication.translate("Form", u"Number of measurements:", None))
        self.startLimitedMeasurementsButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.pausetLimitedMeasurementsButton.setText(QCoreApplication.translate("Form", u"Pause", None))
        self.stoptLimitedMeasurementsButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.tabStartStopTypes.setTabText(self.tabStartStopTypes.indexOf(self.limitedMeasurementsFrame), QCoreApplication.translate("Form", u"By sample size", None))
        self.saveDataButton.setText(QCoreApplication.translate("Form", u"Save Data", None))
        self.measurementsChannelALabel.setText(QCoreApplication.translate("Form", u"Measurements Channel A", None))
        self.measurementsChannelBLabel.setText(QCoreApplication.translate("Form", u"Measurements Channel B", None))
        self.measurementsChannelCLabel.setText(QCoreApplication.translate("Form", u"Measurements Channel C", None))
        self.measurementsChannelDLabel.setText(QCoreApplication.translate("Form", u"Measurements Channel D", None))
        self.totalMeasurementsLabel.setText(QCoreApplication.translate("Form", u"Total measurements", None))
        self.everyLabel.setText(QCoreApplication.translate("Form", u"Every:", None))
        self.timeAutoSaveComboBox.setItemText(0, QCoreApplication.translate("Form", u"5 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(1, QCoreApplication.translate("Form", u"10 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(2, QCoreApplication.translate("Form", u"15 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(3, QCoreApplication.translate("Form", u"20 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(4, QCoreApplication.translate("Form", u"30 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(5, QCoreApplication.translate("Form", u"45 Minutes", None))
        self.timeAutoSaveComboBox.setItemText(6, QCoreApplication.translate("Form", u"1 Hour", None))
        self.helpSaveButton.setText(QCoreApplication.translate("Form", u"Help", None))
        self.valueChannelALabel.setText(QCoreApplication.translate("Form", u"No measured", None))
        self.valueChannelBLabel.setText(QCoreApplication.translate("Form", u"No measured", None))
        self.valueChannelCLabel.setText(QCoreApplication.translate("Form", u"No measured", None))
        self.valueChannelDLabel.setText(QCoreApplication.translate("Form", u"No measured", None))
        self.valueTotalLabel.setText(QCoreApplication.translate("Form", u"No measured", None))
        ___qtablewidgetitem = self.tableTimeStamp.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Start Time (Y-M-D H:M:S)", None))
        font = ___qtablewidgetitem.font()
        font.setBold(True)
        ___qtablewidgetitem.setFont(font)
        ___qtablewidgetitem1 = self.tableTimeStamp.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Stop time (ps)", None))
        font = ___qtablewidgetitem1.font()
        font.setBold(True)
        ___qtablewidgetitem1.setFont(font)
        ___qtablewidgetitem2 = self.tableTimeStamp.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Channel", None))
        font = ___qtablewidgetitem2.font()
        font.setBold(True)
        ___qtablewidgetitem2.setFont(font)
        self.stateLabe.setText(QCoreApplication.translate("Form", u"State:", None))
        self.valueStateLabel.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.labelColor.setText(QCoreApplication.translate("Form",u"N",None))
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
    
    def settingsForSpinBox(self):
        self.numberMeasurementsSpinBox.setMinimum(1)
        self.numberMeasurementsSpinBox.setMaximum(2**28)
        self.numberMeasurementsSpinBox.setValue(1000)

