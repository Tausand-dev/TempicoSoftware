from PySide2.QtCore import QTimer, Qt, QMetaObject
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QPushButton, QCheckBox,QLabel, QWidget, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QApplication, QDateEdit, QTimeEdit, QSpinBox, QTabWidget, QProgressBar
from Utils.createsavefile import createsavefile as savefile
from datetime import datetime
import pyTempico as tempico
from datetime import time as dtime
import os
from Threads.ThreadTimeStamping import WorkerThreadTimeStamping
from Threads.ThreadProccessData import ProcessingDataSaved
import platform
import struct
import psutil
import Utils.constants as constants
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
        self.oldIndex=0
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
        self.autoSaveComboBox.currentIndexChanged.connect(self.onAutoSaveIntervalChanged)
        #Sentinels
        self.channelASentinel=False
        self.channelBSentinel=False
        self.channelCSentinel=False
        self.channelDSentinel=False
        self.isWaiting=False
        #Sentinel to know if a measurement was made in order to enable the save data button
        self.measurementMade=False
        self.errorSaving=False
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
                # timestamps = [
                #     datetime.fromtimestamp(
                #         random.randint(946684800, 1735689600)  # Año 2000 a 2025
                #     ).strftime("%Y-%m-%d %H:%M:%S.%f")
                #     for _ in range(9_000_000)
                # ]
                # stopDataTest=[810702361]*9_000_000
                # channels=[1]*9_000_000
                # self.dateTimeData=timestamps
                # self.stopData=stopDataTest
                # self.channelData=channels
                self.mainWindow.saveSettings()
                self.mainWindow.activeMeasurement()
                self.worker= WorkerThreadTimeStamping(self.channelASentinel,self.channelBSentinel, self.channelCSentinel, self.channelDSentinel,True,False,False, self.device, self.savefile, self.fileName, autoSaved)
                self.worker.finished.connect(self.finishedThread)
                self.worker.newMeasurement.connect(self.captureMeasurement)
                self.worker.changeStatusColor.connect(self.changeStatusColor)
                self.worker.changeStatusText.connect(self.changeStatusLabel)
                self.worker.detectedErrorSaving.connect(self.setErrorAutoSaving)
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
        if self.pauseNormalButton.text()=="Pause acquisition":
            self.worker.changeIsPauseTrue()
            self.pauseNormalButton.setText("Continue acquisition")
        elif self.pauseNormalButton.text()=="Continue acquisition":
            self.pauseNormalButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseNormalButton.setText("Pause acquisition")
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
        if self.pauseNormalButton.text()=="Continue acquisition":
            self.pauseNormalButton.setText("Pause acquisition")
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
                if self.dateTimeFinal<=self.dateTimeInit:
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
        self.worker.detectedErrorSaving.connect(self.setErrorAutoSaving)
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
                self.worker.detectedErrorSaving.connect(self.setErrorAutoSaving)
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
        
    def checkBoxSaveDataAfterMeasurement(self):
        """
        Handles the behavior of the "Save Data" checkbox for enabling or disabling auto-save options.
        Includes a confirmation dialog when disabling auto-save.
        """
        if self.saveDataComplete.isChecked():
            self.autoSaveComboBox.setEnabled(True)
            self.saveDataButton.setEnabled(False)
        else:           
            self.autoSaveComboBox.setEnabled(False)
            if self.measurementMade:
                self.saveDataButton.setEnabled(True)


    
    def checkBoxSaveData(self):
        """
        Handles the behavior of the "Save Data" checkbox for enabling or disabling auto-save options.
        Includes a confirmation dialog when disabling auto-save.
        """
        if self.saveDataComplete.isChecked():
            self.autoSaveComboBox.setEnabled(True)
            self.saveDataButton.setEnabled(False)
        else:
            available_ram_mb = self.getAvailableRam()
            approx_measurements = self.getAproxTotalData(available_ram_mb)

            msg = QMessageBox(self.mainWindow)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Confirm Disable Auto-Save")
            msg.setText(
                f"Do you want to disable auto-save?\n\n"
                f"Please note that this feature is intended to prevent the program from crashing "
                f"due to insufficient memory. We recommend keeping it enabled with the lowest possible interval.\n\n"
                f"If you still wish to disable it, be aware that you currently have available to the process "
                f"{available_ram_mb:.2f} MB of RAM memory, which can store approximately "
                f"{approx_measurements} measurements."
            )
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)

            choice = msg.exec_()

            if choice == QMessageBox.Yes:
                self.autoSaveComboBox.setEnabled(False)
                if self.measurementMade:
                    self.saveDataButton.setEnabled(True)
            else:
                self.saveDataComplete.setChecked(True)
    def onAutoSaveIntervalChanged(self):
        """
        Warns the user if they change the auto-save interval from index 0 to any other value.
        """
        current_index = self.autoSaveComboBox.currentIndex()
        
        if current_index > self.oldIndex:
            msg = QMessageBox(self.mainWindow)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Auto-Save Interval Warning")
            msg.setText(
                "It is recommended to keep this value at the minimum.\n\n"
                "Increasing the interval means more data will be stored in RAM before saving, "
                "which may cause the system to run out of memory.\n\n"
                "Do you still want to proceed?"
            )
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)

            choice = msg.exec_()

            if choice == QMessageBox.No:
                # Revert back to index 0
                self.autoSaveComboBox.blockSignals(True)  # Evitar que se dispare de nuevo el evento
                self.autoSaveComboBox.setCurrentIndex(self.oldIndex)
                self.autoSaveComboBox.blockSignals(False)
            else:
                self.oldIndex=current_index        
        self.oldIndex=current_index
    
    def getAvailableRam(self):
        if platform.machine().endswith('64'):
            system_bits = "64bit"
        else:
            system_bits = "32bit"
        python_bits = struct.calcsize("P") * 8  
        proc = psutil.Process(os.getpid())
        used_by_process = proc.memory_info().rss
        if system_bits == '32bit' and python_bits == 32:
            PROCESS_LIMIT = 2 * 1024 ** 3
        elif system_bits == '64bit' and python_bits == 32:
            PROCESS_LIMIT = 4 * 1024 ** 3
        else:
            PROCESS_LIMIT = psutil.virtual_memory().total
        system_available = psutil.virtual_memory().available
        available_for_process = min(PROCESS_LIMIT - used_by_process, system_available)
        available_for_process_mb = available_for_process / (1024 ** 2)
        return available_for_process_mb

    def getAproxTotalData(self, availableRamMb):
        totalValuesMemory = int((22000000 * availableRamMb) / 4000)
        potencia = 10 ** (len(str(totalValuesMemory)) - 1)
        totalValuesMemory = (totalValuesMemory // potencia) * potencia

        return totalValuesMemory

        
        
            
            
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
        if "TP12" in constants.VERSION_PARAMETER:
            self.calibrateDeviceDelay()
        self.saveDataComplete.setEnabled(False)
        self.autoSaveComboBox.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.enableCheckBoxA.setEnabled(False)
        self.enableCheckBoxB.setEnabled(False)
        self.enableCheckBoxC.setEnabled(False)
        self.enableCheckBoxD.setEnabled(False)
    
    
    def calibrateDeviceDelay(self):
        self.device.calibrateDelay()
        
    
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
        self.errorSaving=False
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
        """
        Restores common UI controls after completing any measurement type.

        Re-enables connection, save options, and channel selection checkboxes.
        """
        self.mainWindow.disconnectButton.setEnabled(True)
        self.saveDataComplete.setEnabled(True)
        self.checkBoxSaveDataAfterMeasurement()
        self.enableCheckBoxA.setEnabled(True)
        self.enableCheckBoxB.setEnabled(True)
        self.enableCheckBoxC.setEnabled(True)
        self.enableCheckBoxD.setEnabled(True)
        
        
        
    
    def autoSaveSettings(self,currentTab):
        """
        Configures and starts the autosave timer based on the user's interval selection.

        If not in the "Scheduled" tab, prompts the user to select the save format.
        """
        #Execute window to select the format
        if currentTab!="Scheduled":
            self.dialogFormatStart(currentTab)
        self.startDateToSave=datetime.now()
        #Get the miliseconds to init timer
        if self.autoSaveComboBox.currentText()=="5 Minutes":
            milisecondsToInit=300000
        elif self.autoSaveComboBox.currentText()=="10 Minutes":
            milisecondsToInit=600000
        elif self.autoSaveComboBox.currentText()=="15 Minutes":
            milisecondsToInit=900000
        elif self.autoSaveComboBox.currentText()=="20 Minutes":
            milisecondsToInit=1200000
        elif self.autoSaveComboBox.currentText()=="30 Minutes":
            milisecondsToInit=1800000
        elif self.autoSaveComboBox.currentText()=="45 Minutes":
            milisecondsToInit=2700000
        elif self.autoSaveComboBox.currentText()=="1 Hour":
            milisecondsToInit=3600000
        #Set the timer to save
        self.autoSaveTimer.timeout.connect(self.autoSaveAction)
        self.autoSaveTimer.start(milisecondsToInit)
            
        
        
    
    def showDialogNoChannels(self):
        """
        Shows a warning dialog if no channels are selected for measurement.
        """
        QMessageBox.warning(
            self.mainWindow,  
            "Not selected channels",
            "You must select at least one channel to start measurement"
        )
    
    
    def showDialogIncorrectDates(self):
        """
        Shows a warning dialog if the end date is earlier than the start date in a scheduled measurement.
        """
        QMessageBox.warning(
            self.mainWindow,
            "Invalid Date Range",
            "The end date must be later than the start date."
        )
    
    def showDialogIncorrectInitDate(self):
        """
        Shows a warning dialog if the start date is earlier than the current date and time.
        """
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
        """
        Updates the label showing the measurement value for channel A.
        """
        self.valueMeasurementA.setText(text)
    
    def updateValuesMeasurementB(self,text):
        """
        Updates the label showing the measurement value for channel B.
        """
        self.valueMeasurementB.setText(text)
    
    def updateValuesMeasurementC(self,text):
        """
        Updates the label showing the measurement value for channel C.
        """
        self.valueMeasurementC.setText(text)
    
    def updateValuesMeasurementD(self,text):
        """
        Updates the label showing the measurement value for channel D.
        """
        self.valueMeasurementD.setText(text)
    
    def updateValueTotalMeasurements(self,text):
        """
        Updates the label showing the total measurements.
        """
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
        """
        Updates the status label text unless a save operation is in progress.

        If a save is occurring, the label is set to "Saving Data" instead.

        :param textValue: The text to display if not currently saving.
        :type textValue: str
        :return: None
        """
        if not self.currenSaving:
            self.statusLabel.setText(textValue)
        else:
            self.statusLabel.setText("Saving Data")
            

    def changeLabelToUpdate(self, textValue):
        """
        Updates the status label or measurement status value depending on the reordering state.

        If not currently reordering, updates `statusValueMeasurements`.
        If reordering, updates the `statusLabel` text directly.

        :param textValue: The text to display.
        :type textValue: str
        :return: None
        """
        if not self.isReordering:
            self.statusValueMeasurements=textValue
        else:
            self.statusLabel.setText(textValue)
    
    #Function to know settings of device
    def saveSettings(self):
        """
        Builds and stores the header for the data file, including device and active channel settings.

        The header contains:
        - Active channels in the measurement.
        - General device configurations.
        - Per-channel settings for each active channel.
        """
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
        """
        Handles post-measurement actions after the normal measurement thread finishes.

        If autosave is enabled, prompts the user to save.
        Then resets saving state and stops the normal measurement.
        """
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
        """
        Inserts new measurement data into the table, updates the internal data structures,
        and refreshes channel/total measurement labels.

        Called when the worker thread emits new measurement values for each channel.

        - Adds rows for each measurement (A, B, C, D, and Start events) at the top of the table.
        - Stores timestamps, stop values, and channel IDs in internal lists.
        - Limits table size to 50,000 rows.
        - Updates labels showing total measurements per channel and overall.
        """
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
            self.updateValuesMeasurementD(str(int(totalMeasurementsChannelD)))
        self.updateValueTotalMeasurements(str(int(totalMeasurements)))
    
    #Dialog to select the format before measurement when auto save is selected}
    def dialogFormatStart(self,currentTab):
        """
        Displays a dialog for selecting the file format when autosave is enabled.

        This function is called at the start of a measurement to let the user choose 
        the file format (`txt`, `csv`, or `dat`) for automatic data saving.
        If the user accepts, the selection is stored and measurement continues.
        If the user cancels, the measurement is stopped according to the current tab 
        (`Normal`, `Scheduled`, or `Limited`) and common post-measurement settings 
        are restored.

        :param currentTab: The tab where the measurement was started ("Normal", "Scheduled", or "Limited").
        :type currentTab: str
        """
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
        """
        Opens a dialog for selecting the file format when saving data manually.

        This function is triggered when the user clicks the manual "Save" button.
        It displays a dialog with available formats (`txt`, `csv`, `dat`) and, 
        upon acceptance, calls `saveDataAction` with the selected format and the 
        current date and time.

        :return: None
        """
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
        """
        Handles the logic for saving measurement data, either from autosave 
        or manual save.

        This function determines if the data has already been saved in the 
        requested format. If so, it notifies the user without duplicating the file. 
        If the data was autosaved in a different format, it converts the temporary 
        file to the selected format and saves it. If the data has not been saved yet, 
        it creates a new file with the current measurement data.

        Additionally, it displays informational dialogs to confirm the save 
        or alert the user if the process fails.

        :param format: The desired file format to save (`"txt"`, `"csv"`, or `"dat"`).
        :type format: str
        :param date: The date and time used to generate the filename for saving.
        :type date: datetime
        """
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
        """
        Displays a modal dialog showing the progress of the file saving process.

        This function creates and shows a progress dialog with a label and a 
        progress bar. It starts a background worker (`ProcessingDataSaved`) to 
        process the file saving and updates the progress bar in real time via 
        signals. When the process finishes, it triggers the final confirmation 
        message.

        :param filename: The full path of the file being saved.
        :type filename: str
        """
        
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
        """
        Displays a confirmation dialog indicating that the file was saved successfully.

        This function shows an information message box with the final save message 
        (`self.saveFinalText`), informing the user of the file's location and name.

        :return: None
        """
        if not self.errorSaving:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Information)
            message_box.setText(self.saveFinalText)
            message_box.setWindowTitle("Successful save")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
        else:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Data Processing Error")
            message_box.setText(
                f"An error occurred while processing the data. "
                f"The saved file may be incomplete:\n\n"
                f"{self.fileName}\n\n"
                f"However, the unprocessed raw data is still available here:\n"
                f"TempData/AutoSavedData.txt\n\n"
                f"Before starting a new measurement, please copy this file to a safe location "
                f"to prevent it from being overwritten."
            )
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
        
    
    def updateProgressDialog(self, percent):
        """
        Updates the progress dialog during the save process.

        This function updates the progress bar and label to reflect the current 
        progress percentage. If the progress reaches or exceeds 100%, the dialog 
        is automatically closed.

        :param percent: The current progress percentage (0 to 100).
        :type percent: int
        :return: None
        """
        self.progressBar.setValue(percent)
        self.progressLabel.setText(f"Processing data {percent}%")
        QApplication.processEvents()
        
        if percent >= 100:
            self.progressDialog.close()
    

    def autoSaveActionRoute(self):
        """
        Performs the final autosave when a measurement ends.

        This function is executed as the last step of a measurement when either the 
        user stops it manually or the scheduled time finishes. It saves all remaining 
        measurement data to a file using the selected autosave format (`txt`, `csv`, 
        or `dat`), clears the in-memory data lists, and updates the corresponding 
        flags indicating that the data has been saved.

        :return: None
        """
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
        """
        Performs periodic autosave during a measurement.

        This function is triggered automatically at regular intervals while a 
        measurement is running. It saves the current batch of measurement data 
        to a file using the predefined autosave format, then clears the saved 
        data from memory to free resources.

        :return: None
        """
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
        """
        Generates and stores the autosave file name.

        This function builds the complete file path for the autosave operation 
        based on the save folder, file prefix, measurement start date, and 
        selected file format. The resulting path is stored in the `fileName` 
        class attribute for later use.

        :return: None
        """
        dataFolderPrefix=self.savefile.getDataFolderPrefix()
        folderpath=dataFolderPrefix["saveFolder"]
        data_prefix=dataFolderPrefix["timeStampingPrefix"]
        currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        self.fileName = os.path.join(folderpath, f"{data_prefix}{currentDateStr}.{self.selectedFormat}")
    
    def dialogToShowSave(self):
        """
        Displays a confirmation dialog for a successful save operation.

        This function shows an information dialog indicating that the files have 
        been saved successfully. It includes the save folder path and the generated 
        file name based on the measurement start date and selected format.

        :return: None
        """
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
        """
        Stops an ongoing normal measurement.

        This function disables the pause and stop buttons for the normal 
        measurement mode and sends a stop signal to the worker thread.

        :return: None
        """
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.worker.stop()
        

    def stopScyheduledButtonAction(self):
        """
        Stops an ongoing scheduled measurement.

        If the measurement is still in the waiting state, it calls 
        `stopScheduledMeasurement()` directly. Otherwise, it stops the 
        scheduled timer, disables the pause and stop buttons, and sends 
        a stop signal to the worker thread.

        :return: None
        """
        if self.isWaiting:
            self.stopScheduledMeasurement()
        else:
            self.timerToStopMeasurement.stop()
            self.pauseScheduleButton.setEnabled(False)
            self.stopScheduleButton.setEnabled(False)
            self.worker.stop()
    
    def stopLimitedButtonAction(self):
        """
        Stops an ongoing limited measurement.

        This function disables the pause and stop buttons for the limited 
        measurement mode and sends a stop signal to the worker thread.

        :return: None
        """
        self.pauseLimitedButton.setEnabled(False)
        self.stopLimitedButton.setEnabled(False)
        self.worker.stop()
    
    def setErrorAutoSaving(self):
        self.errorSaving=True