from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor, QFont
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QWidget, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QHeaderView,QAbstractItemView, QApplication, QHBoxLayout, QDateEdit, QTimeEdit, QSpinBox, QTabWidget, QProgressBar
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace, std
from numpy import append as appnd
from createsavefile import createsavefile as savefile
from datetime import datetime, date, timedelta
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
import time
import random
import threading
from pyqtgraph import mkPen
from datetime import time as dtime
import os
import numpy as np
import sys
import io
class TimeStampLogic():
    """
    Class responsible for managing the logic and interface of the TimeStamp measurement tab.

    This class handles long-duration timestamp measurements across different operational modes, including:
    - **Normal** mode: Starts and stops measurements manually.
    - **Scheduled** mode: Automatically starts/stops measurements based on configured start and end date-times.
    - **Limited** mode: Runs measurements until a predefined number of events is recorded.

    It provides real-time updates of the measurement status, displays results in a table, and supports manual and automatic data saving in multiple formats. It also offers visual feedback, per-channel control, and user configuration for saving behaviors.

    The main responsibilities include:
    - Managing three measurement modes: normal, scheduled, and limited.
    - Displaying measurement data in a table, including per-channel and total counts.
    - Handling delayed start and stop based on date and time settings.
    - Enabling saving of data manually or automatically in `.txt`, `.csv`, and `.dat` formats.
    - Tracking system and measurement status through visual and textual indicators.
    - Controlling visibility and behavior of measurement labels and checkboxes.
    - Providing help dialogs and UI feedback during configuration.

    :param enableCheckBoxA: Checkbox to enable/disable channel A (QCheckBox).
    :param enableCheckBoxB: Checkbox to enable/disable channel B (QCheckBox).
    :param enableCheckBoxC: Checkbox to enable/disable channel C (QCheckBox).
    :param enableCheckBoxD: Checkbox to enable/disable channel D (QCheckBox).
    :param startNormalButton: Button to start normal measurement mode (QPushButton).
    :param pauseNormalButton: Button to pause normal measurement mode (QPushButton).
    :param stopNormalButton: Button to stop normal measurement mode (QPushButton).
    :param startScheduleButton: Button to start scheduled measurement mode (QPushButton).
    :param pauseScheduleButton: Button to pause scheduled measurement mode (QPushButton).
    :param stopScheduleButton: Button to stop scheduled measurement mode (QPushButton).
    :param startLimitedButton: Button to start limited measurement mode (QPushButton).
    :param pauseLimitedButton: Button to pause limited measurement mode (QPushButton).
    :param stopLimitedButton: Button to stop limited measurement mode (QPushButton).
    :param startDate: Date selector for scheduled start date (QDateEdit).
    :param startTime: Time selector for scheduled start time (QTimeEdit).
    :param finishDate: Date selector for scheduled end date (QDateEdit).
    :param finishTime: Time selector for scheduled end time (QTimeEdit).
    :param numberMeasurementsSpinBox: Spin box to configure number of measurements in limited mode (QSpinBox).
    :param showTableCheckBox: Checkbox to show/hide the measurement table (QCheckBox).
    :param measurementLabelA: Label title for channel A measurement (QLabel).
    :param measurementLabelB: Label title for channel B measurement (QLabel).
    :param measurementLabelC: Label title for channel C measurement (QLabel).
    :param measurementLabelD: Label title for channel D measurement (QLabel).
    :param valueMeasurementA: Label showing count value for channel A (QLabel).
    :param valueMeasurementB: Label showing count value for channel B (QLabel).
    :param valueMeasurementC: Label showing count value for channel C (QLabel).
    :param valueMeasurementD: Label showing count value for channel D (QLabel).
    :param valueTotalMeasurement: Label showing total count value (QLabel).
    :param tableTimeStamp: Table displaying recorded timestamp data (QTableWidget).
    :param statusLabel: Label showing current system status (QLabel).
    :param colorLabel: Color-coded label to indicate measurement state (QLabel).
    :param saveDataComplete: Checkbox to toggle full data saving after measurement (QCheckBox).
    :param tabNormalMeasurement: Tab widget for normal measurement UI (QWidget).
    :param tabScheduleMeasurement: Tab widget for scheduled measurement UI (QWidget).
    :param tabLimitedMeasurement: Tab widget for limited measurement UI (QWidget).
    :param saveDataButton: Button to manually save timestamp data (QPushButton).
    :param tabs: Main tab widget that hosts all measurement tabs (QTabWidget).
    :param autoSaveComboBox: Combo box to select preferred format for automatic saving (QComboBox).
    :param helpSaveButton: Button to show help dialog for save options (QPushButton).
    :param parent: The parent UI element containing this tab (usually QMainWindow).
    :param device: The connected TempicoDevice used for timestamp acquisition.
    :param timerConnection: Timer object for device connection polling (QTimer).
    :return: None
    """
    def __init__(self,enableCheckBoxA: QCheckBox,enableCheckBoxB: QCheckBox,enableCheckBoxC: QCheckBox,enableCheckBoxD: QCheckBox, startNormalButton: QPushButton, pauseNormalButton: QPushButton, stopNormalButton: QPushButton ,
                 startScheduleButton: QPushButton, pauseScheduleButton: QPushButton, stopScheduleButton: QPushButton,startLimitedButton: QPushButton, pauseLimitedButton: QPushButton, stopLimitedButton: QPushButton
                 ,startDate: QDateEdit,startTime: QTimeEdit,finishDate: QDateEdit,finishTime: QTimeEdit, numberMeasurementsSpinBox: QSpinBox, showTableCheckBox: QCheckBox,measurementLabelA: QLabel,measurementLabelB: QLabel,
                 measurementLabelC: QLabel, measurementLabelD: QLabel,valueMeasurementA: QLabel,valueMeasurementB: QLabel,valueMeasurementC: QLabel,valueMeasurementD: QLabel,valueTotalMeasurement: QLabel, tableTimeStamp: QTableWidget,
                 statusLabel: QLabel,colorLabel:QLabel, saveDataComplete:QCheckBox,tabNormalMeasurement: QWidget, tabScheduleMeasurement: QWidget, tabLimitedMeasurement: QWidget, saveDataButton:QPushButton, tabs:QTabWidget,autoSaveComboBox: QComboBox, helpSaveButton: QPushButton,parent,device: tempico.TempicoDevice, timerConnection: QTimer):
        #Define the elements from the class
        #Timer for connection
        self.timerConnection=timerConnection
        #Checkbox for the channels
        self.enableCheckBoxA=enableCheckBoxA
        self.enableCheckBoxB=enableCheckBoxB
        self.enableCheckBoxC=enableCheckBoxC
        self.enableCheckBoxD=enableCheckBoxD
        #Save data and show table
        self.saveDataComplete= saveDataComplete
        self.showTableCheckBox=showTableCheckBox
        #Tab and buttons for normal measurement
        self.startNormalButton= startNormalButton
        self.pauseNormalButton= pauseNormalButton
        self.stopNormalButton= stopNormalButton
        self.tabNormalMeasurement=tabNormalMeasurement
        #Tab and buttons for scheduled measurement
        self.startScheduleButton= startScheduleButton
        self.pauseScheduleButton= pauseScheduleButton
        self.stopScheduleButton= stopScheduleButton
        self.startDate=startDate
        self.startTime=startTime
        self.finishDate=finishDate
        self.finishTime=finishTime
        self.tabScheduleMeasurement=tabScheduleMeasurement
        #Tab and buttons for limited measurement
        self.startLimitedButton= startLimitedButton
        self.pauseLimitedButton= pauseLimitedButton
        self.stopLimitedButton= stopLimitedButton
        self.numberMeasurementsSpinBox=numberMeasurementsSpinBox
        self.tabLimitedMeasurement=tabLimitedMeasurement
        #Save data panel
        self.saveDataButton=saveDataButton
        self.autoSaveComboBox= autoSaveComboBox
        self.helpSaveButton=helpSaveButton
        self.valueMeasurementA=valueMeasurementA
        self.valueMeasurementB=valueMeasurementB
        self.valueMeasurementC=valueMeasurementC
        self.valueMeasurementD=valueMeasurementD
        self.valueTotalMeasurement=valueTotalMeasurement
        self.measurementLabelA=measurementLabelA
        self.measurementLabelB=measurementLabelB
        self.measurementLabelC=measurementLabelC
        self.measurementLabelD=measurementLabelD
        self.tableTimeStamp=tableTimeStamp
        self.statusLabel=statusLabel
        self.colorLabel=colorLabel
        self.mainWindow= parent
        self.tabs=tabs
        #Connect checkBox
        self.showTableCheckBox.stateChanged.connect(self.updateShowTable)
        self.enableCheckBoxA.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxB.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxC.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxD.stateChanged.connect(self.updateCheckBoxLabels)
        self.saveDataComplete.stateChanged.connect(self.checkBoxSaveData)
        #Set default states
        self.valueMeasurementA.setVisible(False)
        self.measurementLabelA.setVisible(False)
        self.valueMeasurementB.setVisible(False)
        self.measurementLabelB.setVisible(False)
        self.valueMeasurementC.setVisible(False)
        self.measurementLabelC.setVisible(False)
        self.valueMeasurementD.setVisible(False)
        self.measurementLabelD.setVisible(False)
        self.showTableCheckBox.setChecked(True)
        self.saveDataComplete.setChecked(True)
        self.saveDataButton.setEnabled(False)
        #Connect buttons
        self.startNormalButton.clicked.connect(self.startNormalMeasurement)
        self.pauseNormalButton.clicked.connect(self.pauseNormalMeasurement)
        self.stopNormalButton.clicked.connect(self.stopNormalButtonAction)
        self.startScheduleButton.clicked.connect(self.startScheduledMeasurement)
        self.pauseScheduleButton.clicked.connect(self.pauseScheduledMeasurement)
        self.stopScheduleButton.clicked.connect(self.stopScyheduledButtonAction)
        self.startLimitedButton.clicked.connect(self.startLimitedMeasurement)
        self.pauseLimitedButton.clicked.connect(self.pauseLimitedMeasurement)
        self.stopLimitedButton.clicked.connect(self.stopLimitedButtonAction)
        self.helpSaveButton.clicked.connect(self.dialogHelpSaveButton)
        self.saveDataButton.clicked.connect(self.saveDataButtonAction)
        #Sentinels
        self.channelASentinel=False
        self.channelBSentinel=False
        self.channelCSentinel=False
        self.channelDSentinel=False
        self.isWaiting=False
        #Sentinel to know if a measurement was made in order to enable the save data button
        self.measurementMade=False
        #Sentinel to know if data is already saved
        self.dataAutoSavedTxt=False
        self.dataAutoSavedCsv=False
        self.dataAutoSavedDat=False
        #Sentinel to know if data is saved with any specific format
        self.dataTxtSaved=False
        self.dataCsvSaved=False
        self.dataDatSaved=False
        self.dateTxtSaved=""
        self.dateCsvSaved=""
        self.dateDatSaved=""
        self.changedFolder=False
        #Sentinels to know if data needs to be re saved
        self.dataNeedResaved=False
        
        #Sentinel to know if the software is saving
        self.currenSaving=False
        #Set the current date to date time and hour
        self.currentDateTimeSet=datetime.now()
        self.currentDateSet=self.currentDateTimeSet.date()
        self.currentTimeSet=self.currentDateTimeSet.time()
        self.startDate.setDate(self.currentDateSet)
        self.startTime.setTime(self.currentTimeSet)
        self.finishDate.setDate(self.currentDateSet)
        self.finishTime.setTime(self.currentTimeSet)
        
        #Status value for scheduled measurements
        self.statusValueMeasurements="Running measurement"
        #Device
        self.device=device
        #Save data structures
        self.dateTimeData=[]
        self.stopData=[]
        #This data will be saved as index 0-Start 1-A 2-B 3-C 4-D
        self.channelData=[]
        #savefile object
        self.savefile=savefile()
        #timer for autosave
        self.autoSaveTimer=QTimer()
        #Deafault format
        self.selectedFormat="txt"
        #File name
        self.fileName=""
        #Buttons disabled if there is not device
        if device==None:
            #Normal Buttons
            self.startNormalButton.setEnabled(False)
            self.pauseNormalButton.setEnabled(False)
            self.stopNormalButton.setEnabled(False)
            #Schedule Buttons
            self.startScheduleButton.setEnabled(False)
            self.pauseScheduleButton.setEnabled(False)
            self.stopScheduleButton.setEnabled(False)
            #Limited Buttons
            self.startLimitedButton.setEnabled(False)
            self.pauseLimitedButton.setEnabled(False)
            self.stopLimitedButton.setEnabled(False)
        else:
            #Normal Buttons
            self.startNormalButton.setEnabled(True)
            self.pauseNormalButton.setEnabled(False)
            self.stopNormalButton.setEnabled(False)
            #Schedule Buttons
            self.startScheduleButton.setEnabled(True)
            self.pauseScheduleButton.setEnabled(False)
            self.stopScheduleButton.setEnabled(False)
            #Limited Buttons
            self.startLimitedButton.setEnabled(True)
            self.pauseLimitedButton.setEnabled(False)
            self.stopLimitedButton.setEnabled(False)
    
    # Functions to connect and disconnect device
    def connectedDevice(self,device):
        """
        Handles UI and internal state updates when the device is connected in the TimeStamp logic tab.

        This function performs the following actions:
        - Enables the disconnect button and disables the connect button in the main window.
        - Updates the internal sentinel to indicate the device is now connected.
        - Stores the reference to the connected device instance.
        - Enables the start buttons for normal, scheduled, and limited measurement modes.

        :param device: The connected device instance.
        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.disconnectedMeasurement=False
        self.device=device
        self.startNormalButton.setEnabled(True)
        self.startScheduleButton.setEnabled(True)
        self.startLimitedButton.setEnabled(True)
    
    def disconnectedDevice(self):
        """
        Handles UI and internal state updates when the device is disconnected.

        This function performs the following actions:
        - Resets the internal sentinel indicating whether data is currently being saved.
        - Updates the status label and color to reflect that no measurement is running.
        - Disables the disconnect button and enables the connect button in the main window.
        - Disables the start buttons for normal, scheduled, and limited measurement modes.

        :return: None
        """
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startNormalButton.setEnabled(False)
        self.startScheduleButton.setEnabled(False)
        self.startLimitedButton.setEnabled(False)
    
    #Functions graphic interface
    def updateShowTable(self):
        """
        Toggles the visibility of the timestamp data table based on the checkbox state.

        This function performs the following actions:
        - If the "Show Table" checkbox is checked, the timestamp data table is displayed.
        - If the checkbox is unchecked, the table is hidden.

        :return: None
        """
        if self.showTableCheckBox.isChecked():
            self.tableTimeStamp.setVisible(True)
        else:
            self.tableTimeStamp.setVisible(False)
            
    
    def updateCheckBoxLabels(self):
        """
        Updates the visibility of measurement labels and values based on each channel's checkbox state.

        This function performs the following actions:
        - For each channel (A, B, C, D), if its corresponding checkbox is checked:
        - The label and value indicator showing the number of measurements for that channel are made visible.
        - If unchecked, both elements are hidden.

        This allows dynamic feedback on active channels during timestamp measurements.

        :return: None
        """
        if self.enableCheckBoxA.isChecked():
            self.valueMeasurementA.setVisible(True)
            self.measurementLabelA.setVisible(True)
        else:
            self.valueMeasurementA.setVisible(False)
            self.measurementLabelA.setVisible(False)
            
        if self.enableCheckBoxB.isChecked():
            self.valueMeasurementB.setVisible(True)
            self.measurementLabelB.setVisible(True)
        else:
            self.valueMeasurementB.setVisible(False)
            self.measurementLabelB.setVisible(False)
            
        if self.enableCheckBoxC.isChecked():
            self.valueMeasurementC.setVisible(True)
            self.measurementLabelC.setVisible(True)
        else:
            self.valueMeasurementC.setVisible(False)
            self.measurementLabelC.setVisible(False)
            
        if self.enableCheckBoxD.isChecked():
            self.valueMeasurementD.setVisible(True)
            self.measurementLabelD.setVisible(True)
        else:
            self.valueMeasurementD.setVisible(False)
            self.measurementLabelD.setVisible(False)
    
    
    def startNormalMeasurement(self):
        """
        Starts a normal timestamp measurement.

        Normal measurements begin immediately when the user presses "Start" and continue until manually stopped. 
        This function performs the following actions:
        - Validates that at least one channel (A, B, C, or D) is selected.
        - If no channels are selected, an alert dialog is displayed and the measurement is not started.
        - If valid:
            - Disables the start button and enables pause/stop controls.
            - Disables other measurement tabs to prevent mode changes mid-measurement.
            - Saves pre-measurement settings and prepares auto-save behavior if selected.
            - Updates UI labels and status indicators to reflect active measurement.
            - Creates and starts a background thread (`WorkerThreadTimeStamping`) to handle the measurement process.
            - Connects worker signals to UI update slots.

        :return: None
        """
        self.resetValuesSentinels()
        if self.enableCheckBoxA.isChecked() or self.enableCheckBoxB.isChecked() or self.enableCheckBoxC.isChecked() or self.enableCheckBoxD.isChecked():
            #Disable enable buttons
            self.isSelectedFormat=True
            self.startNormalButton.setEnabled(False)
            self.pauseNormalButton.setEnabled(True)
            self.stopNormalButton.setEnabled(True)
            self.tabs.setTabEnabled(1,False)
            self.tabs.setTabEnabled(2,False)
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            #Set values 
            self.setValuesBeforeMeasurement()
            self.stopTimerConnection()
            #Auto save settings
            self.settingsBeforeMeasurement()
            #Save settings and beggin measurements for main window
            self.mainWindow.saveSettings()
            self.mainWindow.activeMeasurement()
            autoSaved=False
            if self.saveDataComplete.isChecked():
                autoSaved=True
                self.autoSaveSettings("Normal")
            if self.isSelectedFormat:
                self.clearData()
                self.changeStatusLabel("Running measurement")
                self.changeStatusColor(1)
                if self.saveDataComplete.isChecked():
                    self.fileNameAutoSave()
                #Init thread
                self.saveSettings()
                self.worker= WorkerThreadTimeStamping(self.channelASentinel,self.channelBSentinel, self.channelCSentinel, self.channelDSentinel,True,False,False, self.device, self.savefile, self.fileName, autoSaved)
                self.worker.finished.connect(self.finishedThread)
                self.worker.newMeasurement.connect(self.captureMeasurement)
                self.worker.changeStatusColor.connect(self.changeStatusColor)
                self.worker.changeStatusText.connect(self.changeStatusLabel)
                self.worker.finishedMeasurements.connect(self.finishedMeasurements)
                self.isWaiting=True
                self.worker.start()
        else:
            self.showDialogNoChannels()      
    
    def pauseNormalMeasurement(self):
        """
        Toggles the pause/resume state of a normal measurement.

        This function allows the user to pause and later resume an ongoing normal measurement.
        It interacts with the background worker thread to suspend or resume data acquisition accordingly.

        The function performs the following actions:
        - If the current state is "Pause acquisition":
        - Sends a signal to the worker thread to pause the measurement.
        - Updates the button text to "Continue acquisition".
        - If the current state is "Continue acquisition":
        - Temporarily disables the button to avoid duplicate clicks.
        - Sends a signal to the worker thread to resume the measurement.
        - Restores the button text to "Pause acquisition" and re-enables it.

        :return: None
        """   
        if self.pauseNormalButton.text()=="Pause adquisition":
            self.worker.changeIsPauseTrue()
            self.pauseNormalButton.setText("Continue adquisition")
        elif self.pauseNormalButton.text()=="Continue adquisition":
            self.pauseNormalButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseNormalButton.setText("Pause adquisition")
            self.pauseNormalButton.setEnabled(True)
            
            
        
    
    def stopNormalMeasurement(self):
        """
        Stops an ongoing normal measurement and resets the interface to its default state.

        This function performs the following actions:
        - Marks the measurement as completed by setting the corresponding sentinel.
        - Sends a stop signal to the background worker thread.
        - Updates the UI to reflect that no measurement is running (label, color, buttons).
        - If the measurement was paused, resets the pause button text to "Pause acquisition".
        - Re-enables tab switching and restores the initial measurement configuration.
        - Restarts the timer for checking device connection.
        - Notifies the main window to reflect the updated system state and re-enable settings.

        :return: None
        """
        self.measurementMade=True
        self.worker.stop()
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        if self.pauseNormalButton.text()=="Continue adquisition":
            self.pauseNormalButton.setText("Pause adquisition")
        self.startNormalButton.setEnabled(True)
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(2,True)
        self.startTimerConnection()
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.settingsAfterMeasurement()
        self.mainWindow.noMeasurement()
        self.mainWindow.enableSettings()
        
    def notSelectedFormatNormalStop(self):
        """
        Cancels the normal measurement initialization when no save format is selected while auto-save is enabled.

        This function is triggered when the user attempts to start a normal measurement with auto-save enabled
        but closes the format selection dialog without choosing any format (e.g., pressing the X).

        It performs the following actions:
        - Stops any saving process and resets saving state.
        - Updates UI labels and colors to indicate no measurement is running.
        - Re-enables the start button and disables pause/stop buttons.
        - Re-enables all measurement tabs and resumes connection monitoring.
        - Restores main window tab interactivity.

        :return: None
        """
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.startNormalButton.setEnabled(True)
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(2,True)
        self.startTimerConnection()
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        
      
    
    def startScheduledMeasurement(self):
        """
        Initiates a scheduled timestamp measurement with start and end times defined by the user.

        Scheduled measurements begin at a future time and automatically stop at the configured end time.
        This function performs the following actions:
        - Verifies that at least one channel is selected for measurement.
        - Disables tab navigation to prevent mode switching.
        - Retrieves and converts the start and end date-time values from the UI fields.
        - Validates:
            - That the start time is not in the past.
            - That the end time is after the start time.
        - If validation fails, corresponding alert dialogs are shown.
        - If validation passes:
            - Initializes auto-save format selection if enabled.
            - Configures a countdown timer (`timerBeginMeasurement`) to wait until the scheduled start time.
            - Updates the UI to reflect the waiting state with remaining time.
            - Begins measurement immediately if the scheduled start time is now or has passed.

        :return: None
        """
        self.resetValuesSentinels()
        if self.enableCheckBoxA.isChecked() or self.enableCheckBoxB.isChecked() or self.enableCheckBoxC.isChecked() or self.enableCheckBoxD.isChecked():
            
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            dateInit = self.startDate.date()
            hourInit = self.startTime.time()
            dateInitDateFormat = dateInit.toPython()
            hourInitTimeFormat = dtime(hourInit.hour(), hourInit.minute(), 0)
            self.dateTimeInit = datetime.combine(dateInitDateFormat, hourInitTimeFormat)
            dateFinal = self.finishDate.date()
            hourFinal = self.finishTime.time()
            dateFinalDateFormat = dateFinal.toPython()
            hourFinalTimeFormat = dtime(hourFinal.hour(), hourFinal.minute(), 0)
            self.dateTimeFinal = datetime.combine(dateFinalDateFormat, hourFinalTimeFormat)
            currentDate=datetime.now()
            correctInit=False
            if currentDate>self.dateTimeInit:
                self.showDialogIncorrectInitDate()
            else:
                correctInit=True
            correctFinal=False
            if correctInit: 
                if self.dateTimeFinal<self.dateTimeInit:
                    self.showDialogIncorrectDates()
                else:
                    correctFinal=True
            
            if correctInit and correctFinal:
                self.isSelectedFormat=True 
                self.tabs.setTabEnabled(0,False)
                self.tabs.setTabEnabled(2,False)
                self.startScheduleButton.setEnabled(False)
                self.pauseScheduleButton.setEnabled(False)
                self.stopScheduleButton.setEnabled(True)
                self.settingsBeforeMeasurement()
                if self.saveDataComplete.isChecked():
                    self.dialogFormatStart("Scheduled")
                if self.isSelectedFormat:
                    self.timerBeginMeasurement=QTimer()
                    self.timerBeginMeasurement.timeout.connect(self.countToBegin)
                    timerTimeSeconds=int((self.dateTimeInit-currentDate).total_seconds())
                    print(self.dateTimeInit)
                    print(currentDate)
                    if timerTimeSeconds>0:
                        self.isWaiting=True
                        self.changeStatusColor(2)
                        formattedTime = self.formatWaitingTime(timerTimeSeconds)
                        self.mainWindow.saveSettings()
                        self.mainWindow.activeMeasurement()
                        self.changeStatusLabel(f"Waiting to start in {formattedTime}")
                        self.timerBeginMeasurement.start(1000)
                    else:
                        self.beginMeasurementTime()
            else:
                pass
            
        else:
            self.showDialogNoChannels()
    
    
    def formatWaitingTime(self,secondsTotal):
        """
        Formats a time duration (in seconds) into a human-readable string for countdown display.

        This function is used to show the remaining time before a scheduled measurement starts or ends.
        The format adapts depending on the total duration:
        - If more than one day: `"Xd HH:MM:SS"`
        - If more than one hour: `"H:MM:SS"`
        - If less than one hour: `"M:SS"`

        :param secondsTotal: Total time in seconds to format.
        :return: A formatted string representing the remaining time.
        :rtype: str
        """
        days = secondsTotal // 86400
        hours = (secondsTotal % 86400) // 3600
        minutes = (secondsTotal % 3600) // 60
        seconds = secondsTotal % 60

        if days > 0:
            return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
        elif hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
        
    def beginMeasurementTime(self):
        """
        Starts the scheduled timestamp measurement when the countdown timer reaches zero.

        This function is automatically called after the waiting period in a scheduled measurement.
        It performs the following actions:
        - Clears previous data and resets internal sentinels.
        - Sets up pre-measurement values and stops the device connection timer.
        - Applies auto-save settings and generates the file name if needed.
        - Initializes the measurement worker thread in "scheduled" mode.
        - Starts a timer to monitor when the measurement should stop automatically.
        - Updates the UI to reflect that the measurement is now running.

        :return: None
        """
        self.isReordering=False
        self.isWaiting=False
        self.pauseScheduleButton.setEnabled(True)
        self.changeStatusColor(1)
        self.changeStatusLabel("Running measurement")
        self.clearData()
        self.resetValuesSentinels()
        self.setValuesBeforeMeasurement()
        self.stopTimerConnection()
        
        #Auto save settings
        autoSaved=False
        if self.saveDataComplete.isChecked():
            self.autoSaveSettings("Scheduled")
            autoSaved=True
        if self.saveDataComplete.isChecked():
            self.fileNameAutoSave()
        
        #Init thread
        self.saveSettings()
        self.timerToStopMeasurement=QTimer()
        self.timerToStopMeasurement.timeout.connect(self.countToStop)
        self.worker= WorkerThreadTimeStamping(self.channelASentinel,self.channelBSentinel, self.channelCSentinel, self.channelDSentinel,False,True,False, self.device, self.savefile, self.fileName, autoSaved)
        self.worker.finished.connect(self.finishedThreadSchedule)
        self.worker.newMeasurement.connect(self.captureMeasurement)
        self.worker.changeStatusColor.connect(self.changeStatusColor)
        self.worker.changeStatusText.connect(self.changeLabelToUpdate)
        self.worker.finishedMeasurements.connect(self.finishedMeasurements)
        self.worker.start()
        self.timerToStopMeasurement.start(1000)
        
    
    
    
    
    def countToBegin(self):
        """
        Updates the countdown status before the scheduled measurement begins.

        This function is called periodically by a QTimer during the waiting period before a scheduled measurement starts.
        It performs the following actions:
        - Calculates the remaining time until the scheduled start.
        - If time is still remaining:
        - Updates the status label and color with a formatted countdown.
        - If the start time has been reached or passed:
        - Stops the timer.
        - Calls the function to begin the actual measurement (`beginMeasurementTime`).

        :return: None
        """
        currentDate=datetime.now()
        timerTimeSeconds=int((self.dateTimeInit-currentDate).total_seconds())
        if timerTimeSeconds>0:
            self.changeStatusColor(2)
            formattedTime = self.formatWaitingTime(timerTimeSeconds)
            self.changeStatusLabel(f"Waiting to start in {formattedTime}")
        else:
            self.timerBeginMeasurement.stop()
            self.beginMeasurementTime()
            
    
    def countToStop(self):
        """
        Updates the countdown status until the scheduled measurement ends.

        This function is called periodically by a QTimer during an active scheduled measurement.
        It performs the following actions:
        - Calculates the remaining time until the configured end time.
        - If time is still remaining:
        - Updates the status label with the current measurement state and formatted time.
        - If the end time has been reached or passed:
        - Automatically stops the scheduled measurement by calling `stopScheduledMeasurement()`.

        :return: None
        """
        currentText=self.statusValueMeasurements
        currentDate=datetime.now()
        timerTimeSeconds=int((self.dateTimeFinal-currentDate).total_seconds())
        if timerTimeSeconds>0:
            formattedTime = self.formatWaitingTime(timerTimeSeconds)
            newText =f"{currentText} {formattedTime}"
            self.changeStatusLabel(newText)
        else:
            self.stopScheduledMeasurement()
    
    def pauseScheduledMeasurement(self):
        """
        Toggles the pause/resume state of a scheduled measurement.

        This function allows the user to pause or resume an ongoing scheduled measurement.
        It communicates with the background worker thread to suspend or resume the acquisition process.

        The function performs the following actions:
        - If the current button text is "Pause":
        - Sends a pause signal to the worker thread.
        - Updates the button text to "Continue".
        - If the current button text is "Continue":
        - Temporarily disables the button to prevent multiple clicks.
        - Sends a resume signal to the worker thread.
        - Updates the button text back to "Pause" and re-enables the button.

        :return: None
        """
        if self.pauseScheduleButton.text()=="Pause":
            self.worker.changeIsPauseTrue()
            self.pauseScheduleButton.setText("Continue")
        elif self.pauseScheduleButton.text()=="Continue":
            self.pauseScheduleButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseScheduleButton.setText("Pause")
            self.pauseScheduleButton.setEnabled(True)
        
    
    def stopScheduledMeasurement(self):
        """
        Stops a scheduled measurement at any point — before it starts (waiting phase) or during execution.

        This function handles both scenarios:
        - If the measurement hasn't started yet and is waiting for the scheduled start time:
            - Cancels the countdown timer and resets all UI elements to their default state.
        - If the measurement is already running:
            - Stops the data acquisition thread and the timer responsible for countdown to the end.
            - Updates the internal state and UI accordingly.

        In both cases, the function:
        - Resets saving state and UI labels.
        - Restores tab and button availability.
        - Notifies the main window to re-enable configuration options.
        - Calls post-measurement cleanup logic.

        :return: None
        """
        if self.isWaiting:
            self.currenSaving=False
            self.changeStatusColor(0)
            self.changeStatusLabel("No measurement running")
            self.timerBeginMeasurement.stop()
            if self.pauseScheduleButton.text()=="Continue":
                self.pauseScheduleButton.setText("Pause")
            self.startScheduleButton.setEnabled(True)
            self.stopScheduleButton.setEnabled(False)
            self.pauseScheduleButton.setEnabled(False)
            self.tabs.setTabEnabled(0,True)
            self.tabs.setTabEnabled(2,True)
            self.mainWindow.tabs.setTabEnabled(0,True)
            self.mainWindow.tabs.setTabEnabled(1,True)
            self.mainWindow.tabs.setTabEnabled(2,True)
            self.mainWindow.noMeasurement()
            self.mainWindow.enableSettings()
            self.settingsAfterMeasurement()
        else:
            self.measurementMade=True
            self.currenSaving=False
            self.changeStatusColor(0)
            self.changeStatusLabel("No measurement running")
            self.timerToStopMeasurement.stop()
            self.worker.stop()
            if self.pauseScheduleButton.text()=="Continue":
                self.pauseScheduleButton.setText("Pause")
            self.startScheduleButton.setEnabled(True)
            self.stopScheduleButton.setEnabled(False)
            self.pauseScheduleButton.setEnabled(False)
            self.tabs.setTabEnabled(0,True)
            self.tabs.setTabEnabled(2,True)
            self.mainWindow.tabs.setTabEnabled(0,True)
            self.mainWindow.tabs.setTabEnabled(1,True)
            self.mainWindow.tabs.setTabEnabled(2,True)
            self.mainWindow.noMeasurement()
            self.mainWindow.enableSettings()
            self.settingsAfterMeasurement()
        self.startTimerConnection()
    
    def notSelectedFormatScheduledStop(self):
        """
        Cancels the scheduled measurement setup when no save format is selected while auto-save is enabled.

        This function is triggered when the user attempts to start a scheduled measurement with auto-save enabled
        but closes the format selection dialog without choosing a format (e.g., presses the close [X] button).

        It performs the following actions:
        - Stops any saving operation and resets saving state.
        - Updates UI status and color to indicate no measurement is running.
        - Re-enables the start button and disables pause/stop buttons.
        - Restores tab interactivity for other measurement modes and the main window.
        - Resumes the timer for monitoring device connection.

        :return: None
        """
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.startScheduleButton.setEnabled(True)
        self.stopScheduleButton.setEnabled(False)
        self.pauseScheduleButton.setEnabled(False)
        self.tabs.setTabEnabled(0,True)
        self.tabs.setTabEnabled(2,True)
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.startTimerConnection()
            
    
    def startLimitedMeasurement(self):
        """
        Starts a limited timestamp measurement based on a fixed number of measurement cycles.

        This mode runs the acquisition process until the user-defined number of measurements is reached.
        The function performs the following actions:
        - Verifies that at least one channel (A, B, C, or D) is selected.
        - If none are selected, shows an alert and aborts the start.
        - If valid:
        - Disables other measurement tabs to prevent mode switching.
        - Disables the start button and enables pause/stop controls.
        - Prepares measurement parameters and auto-save options.
        - Generates the filename if auto-save is active.
        - Initializes the worker thread in "limited" mode, passing the number of desired measurements.
        - Connects thread signals to appropriate UI update handlers.
        - Starts the background thread and updates the UI to reflect the running state.

        :return: None
        """
        self.resetValuesSentinels()
        if self.enableCheckBoxA.isChecked() or self.enableCheckBoxB.isChecked() or self.enableCheckBoxC.isChecked() or self.enableCheckBoxD.isChecked():
            #Disable enable buttons
            self.isSelectedFormat=True
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            self.startLimitedButton.setEnabled(False)
            self.pauseLimitedButton.setEnabled(True)
            self.stopLimitedButton.setEnabled(True)
            self.tabs.setTabEnabled(0,False)
            self.tabs.setTabEnabled(1,False)
            #Set values 
            self.setValuesBeforeMeasurement()
            
            self.stopTimerConnection()
            #Auto save settings
            autoSaved=False
            self.settingsBeforeMeasurement()
            if self.saveDataComplete.isChecked():
                self.autoSaveSettings("Limited")
                autoSaved=True
            if self.isSelectedFormat:
                self.clearData()
                #Set the filename to save
                self.changeStatusLabel("Running measurement")
                self.changeStatusColor(1)
                if self.saveDataComplete.isChecked():
                    self.fileNameAutoSave()
                self.mainWindow.saveSettings()
                self.mainWindow.activeMeasurement()
                #Init thread
                self.saveSettings()
                numberMeasurementsValue=self.numberMeasurementsSpinBox.value()
                self.numberMeasurementsSpinBox.setEnabled(False)
                self.worker= WorkerThreadTimeStamping(self.channelASentinel,self.channelBSentinel, self.channelCSentinel, self.channelDSentinel,False,False,True, self.device, self.savefile, self.fileName, autoSaved,numberMeasurementsValue)
                self.worker.finished.connect(self.finishedThreadLimited)
                self.worker.newMeasurement.connect(self.captureMeasurement)
                self.worker.changeStatusColor.connect(self.changeStatusColor)
                self.worker.changeStatusText.connect(self.changeStatusLabel)
                self.worker.finishedMeasurements.connect(self.finishedMeasurements)
                self.isWaiting=True
                self.worker.start()
        else:
            self.showDialogNoChannels()  
            
    def stopLimitedMeasurement(self):
        """
        Stops the limited measurement process, regardless of whether the target number of measurements has been reached.

        This function can be used by the user to interrupt the measurement at any point.
        It performs the following actions:
        - Marks the measurement as completed (even if prematurely).
        - Stops the background worker thread.
        - Updates the UI status and color to reflect that no measurement is running.
        - Resets the pause button state (if previously in "Continue" mode).
        - Re-enables the start button and disables pause/stop buttons.
        - Re-enables the measurement count spinbox for further configuration.
        - Restores tab navigation for both the local interface and main window.
        - Signals the main window to re-enable settings and perform cleanup.
        - Restarts the timer that monitors device connection.

        :return: None
        """
        self.measurementMade=True
        self.worker.stop()
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        if self.pauseLimitedButton.text()=="Continue":
            self.pauseLimitedButton.setText("Pause")
        self.startLimitedButton.setEnabled(True)
        self.pauseLimitedButton.setEnabled(False)
        self.stopLimitedButton.setEnabled(False)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.tabs.setTabEnabled(0,True)
        self.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.mainWindow.noMeasurement()
        self.mainWindow.enableSettings()
        self.settingsAfterMeasurement()
        self.startTimerConnection()
    
    def notSelectedFormatLimitedStop(self):
        """
        Cancels the limited measurement setup when no save format is selected while auto-save is enabled.

        This function is triggered when the user initiates a limited measurement with auto-save enabled
        but closes the format selection dialog without choosing a file format.

        It performs the following actions:
        - Aborts the measurement setup and resets saving state.
        - Updates the status label and color to indicate no measurement is running.
        - Re-enables the start button and disables pause/stop controls.
        - Re-enables the measurement count spinbox.
        - Restores tab access for the local interface and main window.
        - Resumes the device connection timer.

        :return: None
        """
        self.currenSaving=False
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.startLimitedButton.setEnabled(True)
        self.pauseLimitedButton.setEnabled(False)
        self.stopLimitedButton.setEnabled(False)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.tabs.setTabEnabled(0,True)
        self.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.startTimerConnection()
    
        
    
    def pauseLimitedMeasurement(self):
        """
        Toggles the pause/resume state of a limited measurement based on number of events.

        This function allows the user to temporarily pause or resume a limited measurement in progress.
        It communicates with the background worker thread to suspend or resume data acquisition accordingly.

        The function performs the following actions:
        - If the current button text is "Pause":
        - Sends a pause signal to the worker thread.
        - Updates the button text to "Continue".
        - If the current button text is "Continue":
        - Temporarily disables the button to avoid duplicate clicks.
        - Sends a resume signal to the worker thread.
        - Updates the button text back to "Pause" and re-enables it.

        :return: None
        """
        if self.pauseLimitedButton.text()=="Pause":
            self.worker.changeIsPauseTrue()
            self.pauseLimitedButton.setText("Continue")
        elif self.pauseLimitedButton.text()=="Continue":
            self.pauseLimitedButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseLimitedButton.setText("Pause")
            self.pauseLimitedButton.setEnabled(True)
        
    def checkBoxSaveData(self):
        """
        Handles the behavior of the "Save Data" checkbox for enabling or disabling auto-save options.

        This function performs the following actions:
        - If the checkbox is checked (auto-save enabled):
        - Enables the combo box to allow the user to select the auto-save interval.
        - Disables the manual save button.
        - If the checkbox is unchecked (manual save mode):
        - Disables the auto-save interval combo box.
        - Enables the manual save button only if a measurement has already been completed.

        :return: None
        """
        if self.saveDataComplete.isChecked():
            self.autoSaveComboBox.setEnabled(True)
            self.saveDataButton.setEnabled(False)
        else:
            self.autoSaveComboBox.setEnabled(False)
            if self.measurementMade:
                self.saveDataButton.setEnabled(True)
            
            
    def dialogHelpSaveButton(self):
        """
        Opens a help dialog explaining how autosave works.

        :return: None
        """
        QMessageBox.information(
            self.mainWindow,
            "What does autosave do?",
            (
                "The autosave system stores data automatically at regular intervals. "
                "Since a high volume of measurements is expected, it is essential to configure short save intervals "
                "to avoid excessive data accumulation.\n\n"
                "If data is not saved frequently enough, the software may be affected by the available system resources. "
                "This can lead to low performance and even data loss before it can be saved properly.\n\n"
                "However, during the autosave process, acquisition may be paused.\n\n"
                "For these reasons, we recommend keeping autosave enabled and setting a short save interval, "
                "especially during long sessions or when working with high-frequency data acquisition."
            )
        )
        
    
    def setValuesBeforeMeasurement(self):
        """
        Activates channel sentinels based on the selected checkboxes.

        :return: None
        """
        if self.enableCheckBoxA.isChecked():
            self.channelASentinel=True
        if self.enableCheckBoxB.isChecked():
            self.channelBSentinel=True
        if self.enableCheckBoxC.isChecked():
            self.channelCSentinel=True
        if self.enableCheckBoxD.isChecked():
            self.channelDSentinel=True
        
    def resetValuesSentinels(self):
        """
        Resets all channel sentinels to False.

        :return: None
        """
        self.channelASentinel=False
        self.channelBSentinel=False
        self.channelCSentinel=False
        self.channelDSentinel=False
    
    def resetSaveSentinels(self):
        """
        Resets all save-related sentinels when the save folder is changed.

        This ensures that previously saved or autosaved data is marked as outdated,
        so it can be saved again in the new location if necessary.

        :return: None
        """
        self.changedFolder=True
        self.dataCsvSaved=False
        self.dataTxtSaved=False
        self.dataDatSaved=False
        if (self.dataAutoSavedCsv or self.dataAutoSavedTxt or self.dataAutoSavedDat):
            self.dataAutoSavedCsv= False
            self.dataAutoSavedTxt= False
            self.dataAutoSavedDat= False
            self.dataNeedResaved=True
        
    
    def settingsBeforeMeasurement(self):
        """
        Applies common UI settings before starting any type of measurement.

        Disables save options and channel checkboxes to prevent changes during acquisition.

        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(False)
        self.saveDataComplete.setEnabled(False)
        self.autoSaveComboBox.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.enableCheckBoxA.setEnabled(False)
        self.enableCheckBoxB.setEnabled(False)
        self.enableCheckBoxC.setEnabled(False)
        self.enableCheckBoxD.setEnabled(False)
        
    
    def clearData(self):
        """
        Clears all data and resets save-related sentinels from the previous measurement.

        This includes:
        - Resetting autosave and manual save flags.
        - Clearing stored measurement data and timestamps.
        - Resetting the display table.
        - Clearing internal autosave buffer via `savefile`.

        :return: None
        """
        self.dataNeedResaved=False
        self.dataAutoSavedTxt=False
        self.dataAutoSavedCsv=False
        self.dataAutoSavedDat=False
        self.dataTxtSaved=False
        self.dataCsvSaved=False
        self.dataDatSaved=False
        self.dateTxtSaved=""
        self.dateCsvSaved=""
        self.dateDatSaved=""
        self.tableTimeStamp.clearContents()
        self.tableTimeStamp.setRowCount(0)
        self.dateTimeData=[]
        self.stopData=[]
        self.channelData=[]
        self.savefile.clearDataAutoSave()
        
    
    def settingsAfterMeasurement(self):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.saveDataComplete.setEnabled(True)
        self.checkBoxSaveData()
        self.enableCheckBoxA.setEnabled(True)
        self.enableCheckBoxB.setEnabled(True)
        self.enableCheckBoxC.setEnabled(True)
        self.enableCheckBoxD.setEnabled(True)
        
        
        
    
    def autoSaveSettings(self,currentTab):
        #Execute window to select the format
        if currentTab!="Scheduled":
            self.dialogFormatStart(currentTab)
        self.startDateToSave=datetime.now()
        #Get the miliseconds to init timer
        if self.autoSaveComboBox.currentText()=="30 Minutes":
            milisecondsToInit=1800000
        elif self.autoSaveComboBox.currentText()=="1 Hour":
            milisecondsToInit=3600000
        elif self.autoSaveComboBox.currentText()=="2 Hours":
            milisecondsToInit=7200000
        elif self.autoSaveComboBox.currentText()=="3 Hours":
            milisecondsToInit=7200000
        elif self.autoSaveComboBox.currentText()=="4 Hours":
            milisecondsToInit=10800000
        elif self.autoSaveComboBox.currentText()=="5 Hours":
            milisecondsToInit=14400000
        elif self.autoSaveComboBox.currentText()=="6 Hours":
            milisecondsToInit=18000000
        #Set the timer to save
        self.autoSaveTimer.timeout.connect(self.autoSaveAction)
        self.autoSaveTimer.start(milisecondsToInit)
            
        
        
    
    def showDialogNoChannels(self):
        QMessageBox.warning(
            self.mainWindow,  
            "Not selected channels",
            "You must select at least one channel to start measurement"
        )
    
    
    def showDialogIncorrectDates(self):
        QMessageBox.warning(
            self.mainWindow,
            "Invalid Date Range",
            "The end date must be later than the start date."
        )
    
    def showDialogIncorrectInitDate(self):
        QMessageBox.warning(
            self.mainWindow,
            "Invalid Start Date",
            "The start date must be later than the current date and time."
        )
    
    
    def stopTimerConnection(self):
        """
        Stops the connection monitoring timer during an active measurement.

        This function is called when a measurement begins to prevent interference from the periodic connection checks. It halts the `timerConnection`, which normally runs in the background to monitor the status of the Tempico device.

        :return: None
        """
        #Stop timer when a measurement begins
        self.timerConnection.stop()
            
    def startTimerConnection(self):
        """
        Starts the connection monitoring timer to periodically check the device status.

        This function activates the `timerConnection`, which verifies the connection with the Tempico device every 500 milliseconds. It is typically called after a measurement has ended or when the device is reconnected, ensuring continuous monitoring of the device’s availability.

        :return: None
        """
        #Start timer when a measurement begins
        self.timerConnection.start(500)
    
    def updateValuesMeasurementA(self,text):
        self.valueMeasurementA.setText(text)
    
    def updateValuesMeasurementB(self,text):
        self.valueMeasurementB.setText(text)
    
    def updateValuesMeasurementC(self,text):
        self.valueMeasurementC.setText(text)
    
    def updateValuesMeasurementD(self,text):
        self.valueMeasurementD.setText(text)
    
    def updateValueTotalMeasurements(self,text):
        self.valueTotalMeasurement.setText(text)
        
    def changeStatusColor(self, color):
        """
        Changes the color of the point in the status bar. Each color is assigned a specific numeric value.

        :param color: The numeric value corresponding to the desired color (int).
                    - 0: Gray
                    - 1: Green
                    - 2: Yellow
                    - 3: Orange
        :return: None
        """
        if not self.currenSaving:
            color=color
        else:
            color=2
        pixmap = QPixmap(self.colorLabel.size())
        pixmap.fill(Qt.transparent)  
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        if color==0:
            painter.setBrush(QColor(128, 128, 128))  
        elif color==1:
            painter.setBrush(QColor(0, 255, 0))  
        elif color==2:
            painter.setBrush(QColor(255, 255, 0))  
        elif color==3:
            painter.setBrush(QColor(255, 165, 0))  
        painter.setPen(Qt.NoPen)
        point_size = min(self.colorLabel.width(), self.colorLabel.height()) // 2
        x = (self.colorLabel.width() - point_size) // 2
        y = (self.colorLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.colorLabel.setPixmap(pixmap)

    def changeStatusLabel(self, textValue):
        if not self.currenSaving:
            self.statusLabel.setText(textValue)
        else:
            self.statusLabel.setText("Saving Data")
            

    def changeLabelToUpdate(self, textValue):
        if not self.isReordering:
            self.statusValueMeasurements=textValue
        else:
            self.statusLabel.setText(textValue)
    
    #Function to know settings of device
    def saveSettings(self):
        header = "Channels in measurement: "
        channelsList = []
        channelASettings = ""
        channelBSettings = ""
        channelCSettings = ""
        channelDSettings = ""

        generalSettings = (
            f"General Device configurations:\n"
            f"Number of runs\t{self.device.getNumberOfRuns()}\t"
            f"Threshold voltage\t{self.device.getThresholdVoltage()}"
        )

        if self.channelASentinel:
            channelsList.append("A")
            channelASettings = (
                f"Channel A:\t"
                f"Average cycles\t{self.device.ch1.getAverageCycles()}\t"
                f"number of stops\t{self.device.ch1.getNumberOfStops()}\t"
                f"stop mask\t{self.device.ch1.getStopMask()}\t"
                f"mode\t{self.device.ch1.getMode()}\t"
                f"stop edge\t{self.device.ch1.getStopEdge()}\t"
                f"start edge\t{self.device.ch1.getStartEdge()}"
            )

        if self.channelBSentinel:
            channelsList.append("B")
            channelBSettings = (
                f"Channel B:\t"
                f"Average cycles\t{self.device.ch2.getAverageCycles()}\t"
                f"number of stops\t{self.device.ch2.getNumberOfStops()}\t"
                f"stop mask\t{self.device.ch2.getStopMask()}\t"
                f"mode\t{self.device.ch2.getMode()}\t"
                f"stop edge\t{self.device.ch2.getStopEdge()}\t"
                f"start edge\t{self.device.ch2.getStartEdge()}"
            )

        if self.channelCSentinel:
            channelsList.append("C")
            channelCSettings = (
                f"Channel C:\t"
                f"Average cycles\t{self.device.ch3.getAverageCycles()}\t"
                f"number of stops\t{self.device.ch3.getNumberOfStops()}\t"
                f"stop mask\t{self.device.ch3.getStopMask()}\t"
                f"mode\t{self.device.ch3.getMode()}\t"
                f"stop edge\t{self.device.ch3.getStopEdge()}\t"
                f"start edge\t{self.device.ch3.getStartEdge()}"
            )

        if self.channelDSentinel:
            channelsList.append("D")
            channelDSettings = (
                f"Channel D:\t"
                f"Average cycles\t{self.device.ch4.getAverageCycles()}\t"
                f"number of stops\t{self.device.ch4.getNumberOfStops()}\t"
                f"stop mask\t{self.device.ch4.getStopMask()}\t"
                f"mode\t{self.device.ch4.getMode()}\t"
                f"stop edge\t{self.device.ch4.getStopEdge()}\t"
                f"start edge\t{self.device.ch4.getStartEdge()}"
            )

        stringChannel = ", ".join(channelsList)
        header += stringChannel + "\n"
        header += generalSettings + "\n"
        header += channelASettings + "\n"
        header += channelBSettings + "\n"
        header += channelCSettings + "\n"
        header += channelDSettings + "\n"

        self.header = header
        
        
    def finishedThread(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.currenSaving=False
        self.stopNormalMeasurement()
    
    def finishedThreadSchedule(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.currenSaving=False
        self.stopScheduledMeasurement()
    
    def finishedThreadLimited(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.currenSaving=False
        self.stopLimitedMeasurement()
    
    def finishedMeasurements(self):
        self.autoSaveTimer.stop()
        if self.saveDataComplete.isChecked():
            self.autoSaveActionRoute()
        
        
    
    def captureMeasurement(self, valuesA, valuesB,valuesC,valuesD, valuesStart, totalMeasurementsChannelA,totalMeasurementsChannelB,totalMeasurementsChannelC,totalMeasurementsChannelD,totalMeasurements):
        moreThan50000=False
        #Get the channel index
        #Update table
        if totalMeasurements>50000:
            moreThan50000=True
        for tupleValueA in valuesA:
            self.tableTimeStamp.insertRow(0)
            item0=QTableWidgetItem(tupleValueA[0])
            item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1=QTableWidgetItem(str(tupleValueA[1]))
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item2=QTableWidgetItem("A")
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableTimeStamp.setItem(0,0,item0)
            self.tableTimeStamp.setItem(0,1,item1)
            self.tableTimeStamp.setItem(0,2,item2)
            self.dateTimeData.append(tupleValueA[0])
            self.stopData.append(tupleValueA[1])
            self.channelData.append(1)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)   
            
        for tupleValueB in valuesB:
            self.tableTimeStamp.insertRow(0)
            item0=QTableWidgetItem(tupleValueB[0])
            item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1=QTableWidgetItem(str(tupleValueB[1]))
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item2=QTableWidgetItem("B")
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableTimeStamp.setItem(0,0,item0)
            self.tableTimeStamp.setItem(0,1,item1)
            self.tableTimeStamp.setItem(0,2,item2)
            self.dateTimeData.append(tupleValueB[0])
            self.stopData.append(tupleValueB[1])
            self.channelData.append(2)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueC in valuesC:
            self.tableTimeStamp.insertRow(0)
            item0=QTableWidgetItem(tupleValueC[0])
            item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1=QTableWidgetItem(str(tupleValueC[1]))
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item2=QTableWidgetItem("C")
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableTimeStamp.setItem(0,0,item0)
            self.tableTimeStamp.setItem(0,1,item1)
            self.tableTimeStamp.setItem(0,2,item2)
            self.dateTimeData.append(tupleValueC[0])
            self.stopData.append(tupleValueC[1])
            self.channelData.append(3)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueD in valuesD:
            self.tableTimeStamp.insertRow(0)
            item0=QTableWidgetItem(tupleValueD[0])
            item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1=QTableWidgetItem(str(tupleValueD[1]))
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item2=QTableWidgetItem("D")
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableTimeStamp.setItem(0,0,item0)
            self.tableTimeStamp.setItem(0,1,item1)
            self.tableTimeStamp.setItem(0,2,item2)
            self.dateTimeData.append(tupleValueD[0])
            self.stopData.append(tupleValueD[1])
            self.channelData.append(4)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueStart in valuesStart:
            self.tableTimeStamp.insertRow(0)
            item0=QTableWidgetItem(tupleValueStart)
            item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item1=QTableWidgetItem("-1")
            item1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item2=QTableWidgetItem("Start")
            item2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableTimeStamp.setItem(0,0,item0)
            self.tableTimeStamp.setItem(0,1,item1)
            self.tableTimeStamp.setItem(0,2,item2)
            self.dateTimeData.append(tupleValueStart)
            self.stopData.append(-1)
            self.channelData.append(0)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        
        #Update labels
        if self.channelASentinel:
            self.updateValuesMeasurementA(str(int(totalMeasurementsChannelA)))
        if self.channelBSentinel:
            self.updateValuesMeasurementB(str(int(totalMeasurementsChannelB)))
        if self.channelCSentinel:
            self.updateValuesMeasurementC(str(int(totalMeasurementsChannelC)))
        if self.channelDSentinel:
            self.updateValuesMeasurementA(str(int(totalMeasurementsChannelD)))
        self.updateValueTotalMeasurements(str(int(totalMeasurements)))
    
    #Dialog to select the format before measurement when auto save is selected}
    def dialogFormatStart(self,currentTab):
        #Open select the format
        self.isSelectedFormat=False
        dialog = QDialog(self.mainWindow)
        dialog.setObjectName("TextFormat")
        dialog.resize(282, 105)
        dialog.setWindowTitle("Save")
        verticalLayout_2 = QVBoxLayout(dialog)
        verticalLayout_2.setObjectName("verticalLayout_2")
        VerticalImage = QVBoxLayout()
        VerticalImage.setObjectName("VerticalImage")
        SelectLabel = QLabel(dialog)
        SelectLabel.setObjectName("SelectLabel")
        SelectLabel.setText("Select the file format for autosave data:")
        VerticalImage.addWidget(SelectLabel)
        FormatBox = QComboBox(dialog)
        FormatBox.addItem("txt")
        FormatBox.addItem("csv")
        FormatBox.addItem("dat")
        FormatBox.setObjectName("FormatBox")
        VerticalImage.addWidget(FormatBox)
        verticalLayout_2.addLayout(VerticalImage)
        accepButton = QPushButton(dialog)
        accepButton.setObjectName("accepButton")
        accepButton.setText("Begin measurement")
        verticalLayout_2.addWidget(accepButton)
        QMetaObject.connectSlotsByName(dialog)  
        # Connect the accept button with real accept
        accepButton.clicked.connect(dialog.accept)
        if dialog.exec_() == QDialog.Accepted:
            self.selectedFormat = FormatBox.currentText()
            self.isSelectedFormat=True
        else:
            if currentTab=="Normal":
                self.notSelectedFormatNormalStop()
                self.settingsAfterMeasurement()
            elif currentTab=="Scheduled":
                self.notSelectedFormatScheduledStop()
                self.settingsAfterMeasurement()
            elif currentTab=="Limited":
                self.notSelectedFormatLimitedStop()
                self.settingsAfterMeasurement()
    
    
        
        
    
    #This function will activate the window when save data button is clicked
    def saveDataButtonAction(self):
        #Open select the format
        dialog = QDialog(self.mainWindow)
        dialog.setObjectName("TextFormat")
        dialog.resize(282, 105)
        dialog.setWindowTitle("Save")
        verticalLayout_2 = QVBoxLayout(dialog)
        verticalLayout_2.setObjectName("verticalLayout_2")
        VerticalImage = QVBoxLayout()
        VerticalImage.setObjectName("VerticalImage")
        SelectLabel = QLabel(dialog)
        SelectLabel.setObjectName("SelectLabel")
        SelectLabel.setText("Select the text format:")
        VerticalImage.addWidget(SelectLabel)
        FormatBox = QComboBox(dialog)
        FormatBox.addItem("txt")
        FormatBox.addItem("csv")
        FormatBox.addItem("dat")
        FormatBox.setObjectName("FormatBox")
        VerticalImage.addWidget(FormatBox)
        verticalLayout_2.addLayout(VerticalImage)
        accepButton = QPushButton(dialog)
        accepButton.setObjectName("accepButton")
        accepButton.setText("Accept")
        verticalLayout_2.addWidget(accepButton)
        QMetaObject.connectSlotsByName(dialog)  
        # Connect the accept button with real accept
        accepButton.clicked.connect(dialog.accept)
        if dialog.exec_() == QDialog.Accepted:
            selected_format = FormatBox.currentText()
            currentDate=datetime.now()
            self.saveDataAction(selected_format,currentDate)
    
    


        
        
    
    #This function will save data in txt file (TO DO: Put other formats)
    def saveDataAction(self,format,date): 
        try:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Information)
            dataFolderPrefix=self.savefile.getDataFolderPrefix()
            folder_path=dataFolderPrefix["saveFolder"]
            data_prefix=dataFolderPrefix["timeStampingPrefix"]
            #If exits and autosaved version with txt format
            if self.dataNeedResaved:
                dateAutoSaved=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                self.fileName=os.path.join(folder_path, f"{data_prefix}{currentDateStr}.{self.selectedFormat}")
                self.savefile.convertFileFormat(self.fileName,format,True)
                inital_text=f"The files have been saved with {format} format in path folder: "
                text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                name= f"\n\n{data_prefix}{dateAutoSaved}.{format}"
                message_box.setText(inital_text+text_route+name)
                message_box.setWindowTitle("Data Saved")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
                self.dataNeedResaved=False
                if format=="txt":
                    self.dataAutoSavedTxt=True
                elif format=="csv":
                    self.dataAutoSavedCsv=True
                elif format=="dat":
                    self.dataAutoSavedDat=True
                
            elif self.dataAutoSavedTxt or self.dataAutoSavedCsv or self.dataAutoSavedDat:
                if self.dataAutoSavedTxt and format=="txt":
                    inital_text = (
                        "The autosave feature has already preserved your data.\n"
                        "Additionally, if you selected a different format, the data may have already been converted accordingly.\n\n"
                    )
                    autosave_info = (
                        "This system periodically saves data during the measurement process to avoid memory loss or crashes.\n"
                        "As a result, no manual save is required.\n\n"
                    )
                    text_route = "Files were saved in the following path:\n\n" + str(folder_path) + "\n\nwith the following name:"
                    currentDateStr = self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    onlyFileName = f"{data_prefix}{currentDateStr}.txt"

                    message_box.setText(inital_text + autosave_info + text_route + onlyFileName)
                    message_box.setWindowTitle("Data Already Saved or Converted")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif self.dataAutoSavedCsv and format=="csv":
                    inital_text = (
                        "The autosave feature has already preserved your data.\n"
                        "Additionally, if you selected a different format, the data may have already been converted accordingly.\n\n"
                    )
                    autosave_info = (
                        "This system periodically saves data during the measurement process to avoid memory loss or crashes.\n"
                        "As a result, no manual save is required.\n\n"
                    )
                    text_route = "Files were saved in the following path:\n\n" + str(folder_path) + "\n\nwith the following name:"
                    currentDateStr = self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    onlyFileName = f"{data_prefix}{currentDateStr}.csv"

                    message_box.setText(inital_text + autosave_info + text_route + onlyFileName)
                    message_box.setWindowTitle("Data Already Saved or Converted")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif self.dataAutoSavedDat and format=="dat":
                    inital_text = (
                        "The autosave feature has already preserved your data.\n"
                        "Additionally, if you selected a different format, the data may have already been converted accordingly.\n\n"
                    )
                    autosave_info = (
                        "This system periodically saves data during the measurement process to avoid memory loss or crashes.\n"
                        "As a result, no manual save is required.\n\n"
                    )
                    text_route = "Files were saved in the following path:\n\n" + str(folder_path) + "\n\nwith the following name:"
                    currentDateStr = self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    onlyFileName = f"{data_prefix}{currentDateStr}.dat"

                    message_box.setText(inital_text + autosave_info + text_route + onlyFileName)
                    message_box.setWindowTitle("Data Already Saved or Converted")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif (self.dataAutoSavedTxt and format!="txt") or (self.dataAutoSavedCsv and format!="csv") or (self.dataAutoSavedDat and format!="dat"):
                    dateAutoSaved=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    self.savefile.convertFileFormat(self.fileName,format,False)
                    inital_text=f"The files have been saved with {format} format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\n{data_prefix}{dateAutoSaved}.{format}"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    if format=="txt":
                        self.dataAutoSavedTxt=True
                    elif format=="csv":
                        self.dataAutoSavedCsv=True
                    elif format=="dat":
                        self.dataAutoSavedDat=True
            else:
                if format=="txt" and self.dataTxtSaved:
                    inital_text="The files have been already saved with txt format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\n{data_prefix}{self.dateTxtSaved}.txt"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif format=="csv" and self.dataCsvSaved:
                    inital_text="The files have been already saved with csv format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\n{data_prefix}{self.dateCsvSaved}.csv"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif format=="dat" and self.dataDatSaved:
                    inital_text="The files have been already saved with dat format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\n{data_prefix}{self.dateDatSaved}.dat"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                else:
                    current_date_str=date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    filename=data_prefix+current_date_str
                    self.savefile.save_time_stamp(self.dateTimeData,self.stopData,self.channelData,filename,folder_path,format, self.header)
                    inital_text="The files have been saved successfully in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\n{filename}.{format}"
                    allFileName=f"{folder_path}\\{filename}.{format}"
                    self.saveFinalText=inital_text+text_route+name
                    self.showProgressDialog(allFileName)
                    if format=="txt":
                        self.dataTxtSaved=True
                        self.dateTxtSaved=current_date_str
                    elif format=="csv":
                        self.dataCsvSaved=True
                        self.dateCsvSaved=current_date_str
                    elif format=="dat":
                        self.dataDatSaved=True
                        self.dateDatSaved=current_date_str        
                    
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The changes could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
    def showProgressDialog(self,filename):
        
        self.progressDialog = QDialog(self.mainWindow)
        self.progressDialog.setWindowTitle("Progress")
        self.progressDialog.setWindowModality(Qt.ApplicationModal)
        self.progressDialog.setFixedSize(300, 100)

        layout = QVBoxLayout(self.progressDialog)
        self.progressLabel = QLabel("Processing...", self.progressDialog)
        self.progressBar = QProgressBar(self.progressDialog)
        self.progressBar.setRange(0, 100)

        layout.addWidget(self.progressLabel)
        layout.addWidget(self.progressBar)
        self.progressDialog.setLayout(layout)
        self.progressDialog.show()

        # Conectar la señal
        self.workerUpdate=ProcessingDataSaved(filename)
        self.workerUpdate.changeProgress.connect(self.updateProgressDialog)
        self.workerUpdate.finished.connect(self.finalMessageAfterSave)
        self.workerUpdate.start()
        
    def finalMessageAfterSave(self):
        message_box = QMessageBox(self.mainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(self.saveFinalText)
        message_box.setWindowTitle("Successful save")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
        
    
    def updateProgressDialog(self, percent):
        self.progressBar.setValue(percent)
        self.progressLabel.setText(f"Processing data {percent}%")
        QApplication.processEvents()
        
        if percent >= 100:
            self.progressDialog.close()
    

    def autoSaveActionRoute(self):
        self.isReordering=True
        self.currenSaving=True
        self.changeStatusLabel("Saving data")
        self.changeStatusColor(2)
        QApplication.processEvents() 
        try:
            totalLenData=len(self.dateTimeData)
            self.savefile.save_time_stamp_autosave(self.dateTimeData[:totalLenData],self.stopData[:totalLenData],self.channelData[:totalLenData], self.header)
            self.dateTimeData=self.dateTimeData[totalLenData:]
            self.stopData=self.stopData[totalLenData:]
            self.channelData=self.channelData[totalLenData:]
            self.currenSaving=False
            self.worker.changeReadyToReorder()
            if self.selectedFormat=="txt":
                self.dataAutoSavedTxt=True
            elif self.selectedFormat=="csv":
                self.dataAutoSavedCsv=True
            elif self.selectedFormat=="dat":
                self.dataAutoSavedDat=True
        except NameError as e:
            print(e)

        
    
    def autoSaveAction(self):
        self.currenSaving=True
        self.changeStatusLabel("Saving data")
        self.changeStatusColor(2)
        QApplication.processEvents() 
        try:
            totalLenData=len(self.dateTimeData)
            self.savefile.save_time_stamp_autosave(self.dateTimeData[:totalLenData],self.stopData[:totalLenData],self.channelData[:totalLenData], self.header)
            self.dateTimeData=self.dateTimeData[totalLenData:]
            self.stopData=self.stopData[totalLenData:]
            self.channelData=self.channelData[totalLenData:]
            self.currenSaving=False
        except NameError as e:
            print(e)
    
    def fileNameAutoSave(self):
        dataFolderPrefix=self.savefile.getDataFolderPrefix()
        folderpath=dataFolderPrefix["saveFolder"]
        data_prefix=dataFolderPrefix["timeStampingPrefix"]
        currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        self.fileName = os.path.join(folderpath, f"{data_prefix}{currentDateStr}.{self.selectedFormat}")
    
    def dialogToShowSave(self):
        message_box = QMessageBox(self.mainWindow)
        message_box.setIcon(QMessageBox.Information)
        inital_text="The files have been saved successfully in path folder: "
        dataFolderPrefix=self.savefile.getDataFolderPrefix()
        folderPath=dataFolderPrefix["saveFolder"]
        data_prefix=dataFolderPrefix["timeStampingPrefix"]
        text_route="\n\n"+ str(folderPath)+"\n\n"+"with the following name:"
        currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        onlyFileName=f"{data_prefix}{currentDateStr}.{self.selectedFormat}"
        name= f"\n\n{onlyFileName}"
        message_box.setText(inital_text+text_route+name)
        message_box.setWindowTitle("Successful save")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
    
    def stopNormalButtonAction(self):
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.worker.stop()
        

    def stopScyheduledButtonAction(self):
        if self.isWaiting:
            self.stopScheduledMeasurement()
        else:
            self.timerToStopMeasurement.stop()
            self.pauseScheduleButton.setEnabled(False)
            self.stopScheduleButton.setEnabled(False)
            self.worker.stop()
    
    def stopLimitedButtonAction(self):
        self.pauseLimitedButton.setEnabled(False)
        self.stopLimitedButton.setEnabled(False)
        self.worker.stop()

        
     
        


class WorkerThreadTimeStamping(QThread):
    newMeasurement=Signal(tuple,tuple,tuple,tuple,tuple,float,float,float,float,float)
    changeStatusText=Signal(str)
    changeStatusColor=Signal(int)
    finishedMeasurements=Signal()
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel, channelDSentinel,normalMeasurementSentinel, scheduleMeasurementSentinel,limitMeasurementSentinel,
                 device: tempico.TempicoDevice,savefile,filename,isAutoSave,maximumMeasurements=0):
        super().__init__()
        #init the parameters
        self.channelASentinel= channelASentinel
        self.channelBSentinel= channelBSentinel
        self.channelCSentinel= channelCSentinel
        self.channelDSentinel= channelDSentinel
        self.normalMeasurementSentinel=normalMeasurementSentinel
        self.scheduleMeasurementSentinel=scheduleMeasurementSentinel
        self.limitMeasurementSentinel=limitMeasurementSentinel
        self.device= device
        #Init the counters
        self.totalMeasurements=0
        self.totalMeasurementsChannelA=0
        self.totalMeasurementsChannelB=0
        self.totalMeasurementsChannelC=0
        self.totalMeasurementsChannelD=0
        #Getting the number of stops 
        self.numberStopsA=0
        self.numberStopsB=0
        self.numberStopsC=0
        self.numberStopsD=0
        #Value for limited measurements
        self.maximumMeasurements=maximumMeasurements
        print(self.maximumMeasurements)
        self.allMeasurementsComplete=False
        #Sentinel to pause thread
        self.isPause=False
        #Sentinel for running
        self.running=True
        #Class to save the file and file name
        self.savefile=savefile
        self.filename=filename
        self.isAutosave=isAutoSave
        #Enable and disable the channels
        self.readyToReOrder=False
        self.enableDisableChannels()
        #Sentinel to know how many measurements are registered
        self.noMeasurementsSequent=0
        self.noAbortsSequent=0
        self.consecutiveErrors=0
        self.saveCurrentMeasurements()
        
        
    
    
    def run(self):
        #Sync the time with the device before measurement
        self.syncTime()
        if self.normalMeasurementSentinel:
            while self.running:
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:    
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
                
        elif self.scheduleMeasurementSentinel:
            while self.running:
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
        if self.limitMeasurementSentinel:
            while self.running and (not self.allMeasurementsComplete):
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:
                    percentage=round((self.totalMeasurements/self.maximumMeasurements)*100,2)
                    message=f"Paused measurement {percentage} %"
                    self.changeStatusText.emit(message)
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getLimitedMeasurements()
        #Enable channels again after finished measurements
        self.enableChannelsAfterFinishedMeasurement()
        if self.isAutosave:
            self.finishedMeasurements.emit()
            while not self.readyToReOrder:
                time.sleep(0.5)
            self.changeStatusText.emit("Processing data")
            self.changeStatusColor.emit(2)
            self.sortTimeStamps(self.filename)
                
    def enableDisableChannels(self):
        self.totalDataPerMeasurement=0
        if self.channelASentinel:
            self.device.ch1.enableChannel()
            self.numberStopsA=self.device.ch1.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch1.disableChannel()
            
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
            self.numberStopsB=self.device.ch2.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch2.disableChannel()
            
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
            self.numberStopsC=self.device.ch3.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch3.disableChannel()
            
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
            self.numberStopsD=self.device.ch4.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch4.disableChannel()
    
    def enableChannelsAfterFinishedMeasurement(self):
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
    
    def syncTime(self):
        self.device.setDateTime()
    
    def sortMeasurementByStart(self, measurement):
        dataFiltered=[]
        for run in measurement:
            if run:
                dataFiltered.append(run)
        dataFiltered.sort(key=lambda x: x[2])
        return dataFiltered
    
            
    
    def getLimitedMeasurements(self):
        try:
            valueA=[]
            valueB=[]
            valueC=[]
            valueD=[]
            onlyStartMeasurements=[]
            startValues={}
            originalConsole=sys.stdout
            sys.stdout=io.StringIO()
            measure=self.device.measure()
            printedDeviceCommunication=sys.stdout.getvalue()
            sys.stdout=originalConsole
            finishedMeasurement=False
            if "Timeout reached" in printedDeviceCommunication:
                while not finishedMeasurement:
                    newFetch=self.device.fetch()
                    if (newFetch==measure):
                        finishedMeasurement=True
                        measure=newFetch
                        self.device.abort()
                        QThread.msleep(20)
                    else:
                        measure=newFetch
            
            if not measure and self.noMeasurementsSequent <3:
                #Counter to know how many not measurements are registered
                self.noMeasurementsSequent+=1
                
            elif not measure and self.noAbortsSequent>=10:
                self.device.reset()
                #Wait at least 20 ms
                QThread.msleep(20)
                self.applyCurrentSettings()
                print("Entra al reset de la medición")
                #Wait at least 20 ms 
                QThread.msleep(20)
            elif not measure and self.noMeasurementsSequent >=3:
                #Set timeout to finish abort
                self.noAbortsSequent+=1
                self.device.abort()
                QThread.msleep(20)
                print("Entra al abort por que no hay medicion")
                #Wait at least 10 ms
                
            
            if self.totalDataPerMeasurement+self.totalMeasurements>=self.maximumMeasurements:
                if measure:
                    measure=self.sortMeasurementByStart(measure)
            startValues={}
            totalNoStarts=0
            StartChannelRegister=True
            if measure:
                for channelMeasure in measure:
                    if channelMeasure:
                        startValue=channelMeasure[2]
                        startValue= str(datetime.fromtimestamp(startValue))
                        startValues[startValue]=0  
                        if self.channelASentinel:
                            if channelMeasure[0]==1:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueA.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                                    if self.totalMeasurements>=self.maximumMeasurements:
                                        self.allMeasurementsComplete=True
                                        break
                                if self.numberStopsA>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsA>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsA>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsA>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                
                                    
                        if self.channelBSentinel:
                            if channelMeasure[0]==2:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueB.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                                    if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsB>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsB>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsB>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsB>4: 
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                        if self.channelCSentinel:
                            if channelMeasure[0]==3:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueC.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                                    if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsC>1: 
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsC>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsC>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsC>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                        if self.channelDSentinel:
                            if channelMeasure[0]==4:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueD.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
                                    if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsD>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsD>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsD>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if self.numberStopsD>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                    else:
                        totalNoStarts+=1
            else:
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)
            if totalNoStarts==len(measure):
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)  
            for key, value in startValues.items():
                if self.totalMeasurements>= self.maximumMeasurements:
                    self.allMeasurementsComplete=True
                    break
                else:
                    if value==0:
                        onlyStartMeasurements.append(key)
                        self.totalMeasurements+=1
            channelStringList=[]
            if self.channelASentinel and not valueA and StartChannelRegister:
                channelStringList.append("A")
            if self.channelBSentinel and not valueB and StartChannelRegister:
                channelStringList.append("B")
            if self.channelCSentinel and not valueC and StartChannelRegister:
                channelStringList.append("C")
            if self.channelDSentinel and not valueD and StartChannelRegister:
                channelStringList.append("D")
            percentage=round((self.totalMeasurements/self.maximumMeasurements)*100,2)
            if channelStringList:
                channelErrorString=", ".join(channelStringList)
                if len(channelStringList)==1:
                    errorMessage=f"The channnel {channelErrorString} is not taking measurements {percentage} %"
                else:
                    errorMessage=f"The channnels {channelErrorString} are not taking measurements {percentage} %"
                
                self.changeStatusText.emit(errorMessage)
                self.changeStatusColor.emit(3)
            elif not StartChannelRegister:
                pass
            else:
                message=f"Running measurement {percentage} %"
                
                self.changeStatusText.emit(message)
                self.changeStatusColor.emit(1)  
            #Emitir lista de tuplas de valores
            self.newMeasurement.emit(valueA,valueB,valueC,valueD,onlyStartMeasurements, self.totalMeasurementsChannelA,
                                    self.totalMeasurementsChannelB,self.totalMeasurementsChannelC, self.totalMeasurementsChannelD, self.totalMeasurements)
        except Exception as e:
            # If this happen corrupted data was found
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors+=1
                
        
    
    def getMeasurement(self):
        try:
            valueA=[]
            valueB=[]
            valueC=[]
            valueD=[]
            onlyStartMeasurements=[]
            startValues={}
            originalConsole=sys.stdout
            sys.stdout=io.StringIO()
            measure=self.device.measure()
            printedDeviceCommunication=sys.stdout.getvalue()
            sys.stdout=originalConsole
            finishedMeasurement=False
            if "Timeout reached" in printedDeviceCommunication:
                while not finishedMeasurement:
                    newFetch=self.device.fetch()
                    if (newFetch==measure):
                        finishedMeasurement=True
                        measure=newFetch
                        self.device.abort()
                        QThread.msleep(20)
                    else:
                        measure=newFetch
            
            if not measure and self.noMeasurementsSequent <3:
                #Counter to know how many not measurements are registered
                self.noMeasurementsSequent+=1
                
            elif not measure and self.noAbortsSequent>=10:
                self.device.reset()
                #Wait at leat 20 ms
                QThread.msleep(20)
                self.applyCurrentSettings()
                print("Entra al reset de la medición")
                #Wait at leat 20 ms 
                QThread.msleep(20)
            elif not measure and self.noMeasurementsSequent >=3:
                #Set timeout to finish abort
                self.noAbortsSequent+=1
                self.device.abort()
                QThread.msleep(20)
                print("Entra al abort por que no hay medicion")
                #Wait at leat 10 ms
                
            
                
            
            if self.totalDataPerMeasurement+self.totalMeasurements>=self.maximumMeasurements:
                if measure:
                    measure=self.sortMeasurementByStart(measure)
            totalNoStarts=0
            StartChannelRegister=True
            if measure:
                self.noMeasurementsSequent=0
                self.noAbortsSequent=0
                for channelMeasure in measure:
                    if channelMeasure:
                        #New start algo
                        startValue=channelMeasure[2]
                        startValue= str(datetime.fromtimestamp(startValue))
                        startValues[startValue]=0
                        if self.channelASentinel:
                            if channelMeasure[0]==1:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueA.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                                if self.numberStopsA>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if self.numberStopsA>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if self.numberStopsA>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if self.numberStopsA>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                
                                    
                        if self.channelBSentinel:
                            if channelMeasure[0]==2:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueB.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                                if self.numberStopsB>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if self.numberStopsB>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if self.numberStopsB>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if self.numberStopsB>4: 
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                        if self.channelCSentinel:
                            if channelMeasure[0]==3:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueC.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                                if self.numberStopsC>1: 
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if self.numberStopsC>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if self.numberStopsC>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if self.numberStopsC>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                        if self.channelDSentinel:
                            if channelMeasure[0]==4:
                                if channelMeasure[3]!=-1:
                                    startValues[startValue]+=1
                                    valueD.append((startValue,channelMeasure[3]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
                                if self.numberStopsD>1:
                                    if channelMeasure[4]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if self.numberStopsD>2:
                                    if channelMeasure[5]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if self.numberStopsD>3:
                                    if channelMeasure[6]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if self.numberStopsD>4:
                                    if channelMeasure[7]!=-1:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                    else:
                        totalNoStarts+=1
            else:
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)
            if measure:
                if totalNoStarts==len(measure):
                    errorMessageInput=f"The start channel is not taking measurements"
                    StartChannelRegister=False
                    self.changeStatusText.emit(errorMessageInput)
                    self.changeStatusColor.emit(3)
            onlyStartsValues = [key for key, value in startValues.items() if value == 0]
            onlyStartMeasurements=onlyStartsValues
            self.totalMeasurements+=len(onlyStartMeasurements)
            channelStringList=[]
            if self.channelASentinel and (not valueA) and StartChannelRegister: 
                channelStringList.append("A")
            if self.channelBSentinel and (not valueB) and StartChannelRegister:
                channelStringList.append("B")
            if self.channelCSentinel and (not valueC) and StartChannelRegister:
                channelStringList.append("C")
            if self.channelDSentinel and (not valueD) and StartChannelRegister:
                channelStringList.append("D")
            if channelStringList:
                channelErrorString=", ".join(channelStringList)
                if len(channelStringList)==1:
                    errorMessage=f"The channnel {channelErrorString} is not taking measurements"
                else:
                    errorMessage=f"The channnels {channelErrorString} are not taking measurements"
                
                self.changeStatusText.emit(errorMessage)
                self.changeStatusColor.emit(3)
            elif not StartChannelRegister:
                pass
            else:
                self.changeStatusText.emit("Running measurement")
                self.changeStatusColor.emit(1)  
            #Emitir lista de tuplas de valores
            self.consecutiveErrors=0
            self.newMeasurement.emit(valueA,valueB,valueC,valueD,onlyStartMeasurements, self.totalMeasurementsChannelA,
                                    self.totalMeasurementsChannelB,self.totalMeasurementsChannelC, self.totalMeasurementsChannelD, self.totalMeasurements)
        except Exception as e:
            # If this happen corrupted data was found
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors+=1
                
            
        
    
    
    def changeIsPauseTrue(self):
        self.isPause= True
    
    def changeIsPauseFalse(self):
        self.isPause= False
    
    def changeReadyToReorder(self):
        self.readyToReOrder=True
    
    
       
    # Function to reorder data
    def sortTimeStamps(self, file_path):
        tempDataPath = os.path.join("./TempData", f"AutoSaveData.txt")
        with open(tempDataPath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            return

        header = lines[:8]
        data_lines = lines[8:]
        total_lines = len(data_lines)
        parsed_data = []
        selectedFormat=file_path.split(".")[-1]
        if selectedFormat=="csv":
            separator=";"
        else:
            separator="\t"
        #Change the header
        newHeader=[]
        for lineSettings in header:
            newLineSetting= lineSettings.replace("\t",separator)
            newHeader.append(newLineSetting)
        header=newHeader
            
        for idx, line in enumerate(data_lines):
            parts = line.strip().split("\t")
            if len(parts) == 3:
                start_time_str, stop_time, channel = parts
                try:
                    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
                    parsed_data.append((start_time, stop_time, channel))
                except ValueError:
                    continue

            if idx % max(1, total_lines // 30) == 0:
                percent = int((idx + 1) / total_lines * 30)
                self.changeStatusText.emit(f"Processing data {percent}%")

        self.changeStatusText.emit("Processing timestamps 70%")
        sorted_data = sorted(parsed_data, key=lambda x: x[0])

        self.changeStatusText.emit("Processing data 70%...")
        with open(tempDataPath, 'w', encoding='utf-8') as file:
            for headerValue in header:
                file.write(headerValue)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\t{stop_time}\t{channel}\n")
                if idx % max(1, len(sorted_data) // 15) == 0:
                    percent = 70 + int((idx + 1) / len(sorted_data) * 15)
                    self.changeStatusText.emit(f"Processing data {percent}%")
        
        
        
        self.changeStatusText.emit("Processing data 85%...")
        with open(file_path, 'w', encoding='utf-8') as file:
            for headerValue in header:
                file.write(headerValue)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}{separator}{stop_time}{separator}{channel}\n")

                if idx % max(1, len(sorted_data) // 15) == 0:
                    percent = 85 + int((idx + 1) / len(sorted_data) * 15)
                    self.changeStatusText.emit(f"Processing data {percent}%")

        self.changeStatusText.emit("Processing complete.")
    
    def saveCurrentMeasurements(self):
        #General settings
        self.numberRunsSetting=self.device.getNumberOfRuns()
        self.thresholdVoltage=self.device.getThresholdVoltage()
        #Channel A
        self.averageCyclesChannelA= self.device.ch1.getAverageCycles()
        self.modeChannelA= self.device.ch1.getMode()
        self.numberStopsChannelA = self.device.ch1.getNumberOfStops()
        self.stopEdgeTypeChannelA= self.device.ch1.getStopEdge()
        self.stopMaskChannelA=self.device.ch1.getStopMask()
        #ChannelB
        self.averageCyclesChannelB= self.device.ch2.getAverageCycles()
        self.modeChannelB= self.device.ch2.getMode()
        self.numberStopsChannelB = self.device.ch2.getNumberOfStops()
        self.stopEdgeTypeChannelB= self.device.ch2.getStopEdge()
        self.stopMaskChannelB=self.device.ch2.getStopMask()
        #ChannelC
        self.averageCyclesChannelC= self.device.ch3.getAverageCycles()
        self.modeChannelC= self.device.ch3.getMode()
        self.numberStopsChannelC = self.device.ch3.getNumberOfStops()
        self.stopEdgeTypeChannelC= self.device.ch3.getStopEdge()
        self.stopMaskChannelC=self.device.ch3.getStopMask()
        #ChannelD
        self.averageCyclesChannelD= self.device.ch4.getAverageCycles()
        self.modeChannelD= self.device.ch4.getMode()
        self.numberStopsChannelD = self.device.ch4.getNumberOfStops()
        self.stopEdgeTypeChannelD= self.device.ch4.getStopEdge()
        self.stopMaskChannelD=self.device.ch4.getStopMask()
    
    def applyCurrentSettings(self):
        #Settings to general device
        self.device.setNumberOfRuns(self.numberRunsSetting)
        self.device.setThresholdVoltage(self.thresholdVoltage)
        #Settings to channelA
        self.device.ch1.setAverageCycles(self.averageCyclesChannelA)
        self.device.ch1.setMode(self.modeChannelA)
        self.device.ch1.setNumberOfStops(self.numberStopsChannelA)
        self.device.ch1.setStopEdge(self.stopEdgeTypeChannelA)
        self.device.ch1.setStopMask(self.stopMaskChannelA)
        #Settings to channelB
        self.device.ch2.setAverageCycles(self.averageCyclesChannelB)
        self.device.ch2.setMode(self.modeChannelB)
        self.device.ch2.setNumberOfStops(self.numberStopsChannelB)
        self.device.ch2.setStopEdge(self.stopEdgeTypeChannelB)
        self.device.ch2.setStopMask(self.stopMaskChannelB)
        #Settings to channelC
        self.device.ch3.setAverageCycles(self.averageCyclesChannelC)
        self.device.ch3.setMode(self.modeChannelC)
        self.device.ch3.setNumberOfStops(self.numberStopsChannelC)
        self.device.ch3.setStopEdge(self.stopEdgeTypeChannelC)
        self.device.ch3.setStopMask(self.stopMaskChannelC)
        #Settings to channelD
        self.device.ch4.setAverageCycles(self.averageCyclesChannelD)
        self.device.ch4.setMode(self.modeChannelD)
        self.device.ch4.setNumberOfStops(self.numberStopsChannelD)
        self.device.ch4.setStopEdge(self.stopEdgeTypeChannelD)
        self.device.ch4.setStopMask(self.stopMaskChannelD)
        #Enable disable channels to continue measurements
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.channelASentinel:
            self.device.ch1.enableChannel()
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
        
        
    @Slot()   
    def stop(self):
        self.running=False    


class ProcessingDataSaved(QThread):
    changeProgress=Signal(float)
    def __init__(self, filename):
        super().__init__()
        self.filename=filename
    
    def run(self):
        self.sortTimeStamps(self.filename)
    
    def sortTimeStamps(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            self.changeProgress.emit(100)
            return

        header = lines[:8]
        data_lines = lines[7:]
        total_lines = len(data_lines)
        parsed_data = []
        selectedFormat=file_path.split(".")[-1]
        if selectedFormat=="csv":
            separator=";"
        else:
            separator="\t"

        for idx, line in enumerate(data_lines):
            parts = line.strip().split(separator)
            if len(parts) == 3:
                start_time_str, stop_time, channel = parts
                try:
                    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
                    parsed_data.append((start_time, stop_time, channel))
                except ValueError:
                    continue

            if idx % max(1, total_lines // 30) == 0:
                percent = int((idx + 1) / total_lines * 30)
                self.changeProgress.emit(percent)

        self.changeProgress.emit(70)

        sorted_data = sorted(parsed_data, key=lambda x: x[0])

        self.changeProgress.emit(70)  

        with open(file_path, 'w', encoding='utf-8') as file:
            for headerValue in header:
                file.write(headerValue)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}{separator}{stop_time}{separator}{channel}\n")

                if idx % max(1, len(sorted_data) // 30) == 0:
                    percent = 70 + int((idx + 1) / len(sorted_data) * 30)
                    self.changeProgress.emit(percent)

        self.changeProgress.emit(100)
    
    

        
        
            
        
        
        
    
    
    