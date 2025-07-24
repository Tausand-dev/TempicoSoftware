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
class TimeStampLogic():
    def __init__(self,enableCheckBoxA: QCheckBox,enableCheckBoxB: QCheckBox,enableCheckBoxC: QCheckBox,enableCheckBoxD: QCheckBox, startNormalButton: QPushButton, pauseNormalButton: QPushButton, stopNormalButton: QPushButton ,
                 startScheduleButton: QPushButton, pauseScheduleButton: QPushButton, stopScheduleButton: QPushButton,startLimitedButton: QPushButton, pauseLimitedButton: QPushButton, stopLimitedButton: QPushButton
                 ,startDate: QDateEdit,startTime: QTimeEdit,finishDate: QDateEdit,finishTime: QTimeEdit, numberMeasurementsSpinBox: QSpinBox, showTableCheckBox: QCheckBox,measurementLabelA: QLabel,measurementLabelB: QLabel,
                 measurementLabelC: QLabel, measurementLabelD: QLabel,valueMeasurementA: QLabel,valueMeasurementB: QLabel,valueMeasurementC: QLabel,valueMeasurementD: QLabel,valueTotalMeasurement: QLabel, tableTimeStamp: QTableWidget,
                 statusLabel: QLabel,colorLabel:QLabel, saveDataComplete:QCheckBox,tabNormalMeasurement: QWidget, tabScheduleMeasurement: QWidget, tabLimitedMeasurement: QWidget, saveDataButton:QPushButton, tabs:QTabWidget,autoSaveComboBox: QComboBox, helpSaveButton: QPushButton,parent,device, timerConnection: QTimer):
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
        self.dataAutoSaved=False
        #Sentinel to know if data is saved with any specific format
        self.dataTxtSaved=False
        self.dataCsvSaved=False
        self.dataDatSaved=False
        self.dateTxtSaved=""
        self.dateCsvSaved=""
        self.dateDatSaved=""
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
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.disconnectedMeasurement=False
        self.device=device
        self.startNormalButton.setEnabled(True)
        self.startScheduleButton.setEnabled(True)
        self.startLimitedButton.setEnabled(True)
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startNormalButton.setEnabled(False)
        self.startScheduleButton.setEnabled(False)
        self.startLimitedButton.setEnabled(False)
    
    #Functions graphic interface
    def updateShowTable(self):
        if self.showTableCheckBox.isChecked():
            self.tableTimeStamp.setVisible(True)
        else:
            self.tableTimeStamp.setVisible(False)
            
    
    def updateCheckBoxLabels(self):
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
            #Test performance in saving data
            N = 2_000_000  # 2 millones
            if self.isSelectedFormat:
                self.clearData()
                self.changeStatusLabel("Running measurement")
                self.changeStatusColor(1)
                # start_date = datetime(2024, 1, 1)
                # end_date = datetime.now()
                # delta_seconds = int((end_date - start_date).total_seconds())

                # # Generar datetimes aleatorios y convertirlos a string con milisegundos
                # self.dateTimeData = [
                #     (start_date + timedelta(seconds=random.randint(0, delta_seconds), milliseconds=random.randint(0, 999)))
                #     .strftime('%Y-%m-%d %H:%M:%S.') + f"{random.randint(0, 999):03d}"
                #     for _ in range(N)
                # ]
                # self.stopData = [1] * N
                # self.channelData = [1] * N
                #Set the name for the file
                if self.saveDataComplete.isChecked():
                    self.fileNameAutoSave()
                #Init thread
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
        if self.pauseNormalButton.text()=="Pause adquisition":
            self.worker.changeIsPauseTrue()
            self.pauseNormalButton.setText("Continue adquisition")
        elif self.pauseNormalButton.text()=="Continue adquisition":
            self.pauseNormalButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseNormalButton.setText("Pause adquisition")
            self.pauseNormalButton.setEnabled(True)
            
            
        
    
    def stopNormalMeasurement(self):
        self.measurementMade=True
        self.worker.stop()
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
        #Check if any channel is selected 
        self.resetValuesSentinels()
        if self.enableCheckBoxA.isChecked() or self.enableCheckBoxB.isChecked() or self.enableCheckBoxC.isChecked() or self.enableCheckBoxD.isChecked():
            
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            self.mainWindow.activeMeasurement()
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
                print("Try again")
            
        else:
            self.showDialogNoChannels()
    
    def formatWaitingTime(self,secondsTotal):
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
        # N=2_000_000
        # start_date = datetime(2024, 1, 1)
        # end_date = datetime.now()
        # delta_seconds = int((end_date - start_date).total_seconds())

        # # Generar datetimes aleatorios y convertirlos a string con milisegundos
        # self.dateTimeData = [
        #     (start_date + timedelta(seconds=random.randint(0, delta_seconds), milliseconds=random.randint(0, 999)))
        #     .strftime('%Y-%m-%d %H:%M:%S.') + f"{random.randint(0, 999):03d}"
        #     for _ in range(N)
        # ]
        # self.stopData = [1] * N
        # self.channelData = [1] * N
        #Set the file name for auto save
        if self.saveDataComplete.isChecked():
            self.fileNameAutoSave()
        
        #Init thread
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
        if self.pauseScheduleButton.text()=="Pause":
            self.worker.changeIsPauseTrue()
            self.pauseScheduleButton.setText("Continue")
        elif self.pauseScheduleButton.text()=="Continue":
            self.pauseScheduleButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseScheduleButton.setText("Pause")
            self.pauseScheduleButton.setEnabled(True)
        
    
    def stopScheduledMeasurement(self):
         
        if self.isWaiting:
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
            self.mainWindow.enableSettings()
            self.mainWindow.noMeasurement()
            self.mainWindow.enableSettings()
            self.settingsAfterMeasurement()
        self.startTimerConnection()
    
    def notSelectedFormatScheduledStop(self):
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
        self.resetValuesSentinels()
        if self.enableCheckBoxA.isChecked() or self.enableCheckBoxB.isChecked() or self.enableCheckBoxC.isChecked() or self.enableCheckBoxD.isChecked():
            #Disable enable buttons
            self.isSelectedFormat=True
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            self.mainWindow.activeMeasurement()
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
        self.measurementMade=True
        self.worker.stop()
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
        self.mainWindow.enableSettings()
        self.mainWindow.noMeasurement()
        self.mainWindow.enableSettings()
        self.settingsAfterMeasurement()
        self.startTimerConnection()
    
    def notSelectedFormatLimitedStop(self):
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
        if self.pauseLimitedButton.text()=="Pause":
            self.worker.changeIsPauseTrue()
            self.pauseLimitedButton.setText("Continue")
        elif self.pauseLimitedButton.text()=="Continue":
            self.pauseLimitedButton.setEnabled(False)
            self.worker.changeIsPauseFalse()
            self.pauseLimitedButton.setText("Pause")
            self.pauseLimitedButton.setEnabled(True)
        
    def checkBoxSaveData(self):
        if self.saveDataComplete.isChecked():
            self.autoSaveComboBox.setEnabled(True)
            self.saveDataButton.setEnabled(False)
        else:
            self.autoSaveComboBox.setEnabled(False)
            if self.measurementMade:
                self.saveDataButton.setEnabled(True)
            
            
    def dialogHelpSaveButton(self):
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
        if self.enableCheckBoxA.isChecked():
            self.channelASentinel=True
        if self.enableCheckBoxB.isChecked():
            self.channelBSentinel=True
        if self.enableCheckBoxC.isChecked():
            self.channelCSentinel=True
        if self.enableCheckBoxD.isChecked():
            self.channelDSentinel=True
        
    def resetValuesSentinels(self):
        self.channelASentinel=False
        self.channelBSentinel=False
        self.channelCSentinel=False
        self.channelDSentinel=False
        
    
    def settingsBeforeMeasurement(self):
        self.saveDataComplete.setEnabled(False)
        self.autoSaveComboBox.setEnabled(False)
        self.saveDataButton.setEnabled(False)
    
    def clearData(self):
        self.dataAutoSaved=False
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
        
    
    def settingsAfterMeasurement(self):
        self.saveDataComplete.setEnabled(True)
        self.checkBoxSaveData()
        
        
        
    
    def autoSaveSettings(self,currentTab):
        #Execute window to select the format
        if currentTab!="Scheduled":
            self.dialogFormatStart(currentTab)
        self.startDateToSave=datetime.now()
        #Get the miliseconds to init timer
        if self.autoSaveComboBox.currentText()=="30 Minutes":
            milisecondsToInit=60000
            # milisecondsToInit=1800000
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
            
        
        
    def finishedThread(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.stopNormalMeasurement()
    
    def finishedThreadSchedule(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.stopScheduledMeasurement()
    
    def finishedThreadLimited(self):
        if self.saveDataComplete.isChecked():
            self.dialogToShowSave()
        self.stopLimitedMeasurement()
    
    def finishedMeasurements(self):
        self.autoSaveTimer.stop()
        if self.saveDataComplete.isChecked():
            self.autoSaveActionRoute()
        
        
    
    def captureMeasurement(self, valuesA, valuesB,valuesC,valuesD, valuesStart, totalMeasurementsChannelA,totalMeasurementsChannelB,totalMeasurementsChannelC,totalMeasurementsChannelD,totalMeasurements):
        moreThan50000=False
        #Get the channel index
        #Update table
        if self.tableTimeStamp.rowCount()>50000:
            moreThan50000=True
        for tupleValueA in valuesA:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueA[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueA[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("A"))
            self.dateTimeData.append(tupleValueA[0])
            self.stopData.append(tupleValueA[1])
            self.channelData.append(1)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)   
        for tupleValueB in valuesB:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueB[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueB[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("B"))
            self.dateTimeData.append(tupleValueB[0])
            self.stopData.append(tupleValueB[1])
            self.channelData.append(2)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueC in valuesC:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueC[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueC[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("C"))
            self.dateTimeData.append(tupleValueC[0])
            self.stopData.append(tupleValueC[1])
            self.channelData.append(3)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueD in valuesD:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueD[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueD[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("D"))
            self.dateTimeData.append(tupleValueD[0])
            self.stopData.append(tupleValueD[1])
            self.channelData.append(4)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueStart in valuesStart:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueStart))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem("-1"))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("Start"))
            self.dateTimeData.append(tupleValueStart)
            self.stopData.append(-1)
            self.channelData.append(0)
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        
        #Update labels
        if self.channelASentinel:
            self.updateValuesMeasurementA(str(totalMeasurementsChannelA))
        if self.channelBSentinel:
            self.updateValuesMeasurementB(str(totalMeasurementsChannelB))
        if self.channelCSentinel:
            self.updateValuesMeasurementC(str(totalMeasurementsChannelC))
        if self.channelDSentinel:
            self.updateValuesMeasurementA(str(totalMeasurementsChannelD))
        self.updateValueTotalMeasurements(str(totalMeasurements))
    
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
            folder_path=self.savefile.read_default_data()['Folder path']
            if self.dataAutoSaved:
                inital_text = "The data has already been saved automatically due to the autosave feature.\n\n"
                autosave_info = (
                    "This system periodically saves data during the measurement process to prevent memory issues.\n"
                    "Therefore, no manual save is necessary.\n\n"
                )
                text_route = "Files were saved in the following path:\n\n" + str(folder_path) + "\n\nwith the following name:"
                currentDateStr = self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                onlyFileName = f"TimeStamping{currentDateStr}.{self.selectedFormat}"

                message_box.setText(inital_text + autosave_info + text_route + onlyFileName)
                message_box.setWindowTitle("Data Already Saved")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_() 
            else:
                if format=="txt" and self.dataTxtSaved:
                    inital_text="The files have been already saved with txt format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\nTimeStamping{self.dateTxtSaved}.txt"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif format=="csv" and self.dataCsvSaved:
                    inital_text="The files have been already saved with csv format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\nTimeStamping{self.dateCsvSaved}.csv"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                elif format=="dat" and self.dataDatSaved:
                    inital_text="The files have been already saved with dat format in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following name:"
                    name= f"\n\nTimeStamping{self.dateDatSaved}.dat"
                    message_box.setText(inital_text+text_route+name)
                    message_box.setWindowTitle("Data Already Saved")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                else:
                    data_prefix="TimeStamping"
                    current_date_str=date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    filename=data_prefix+current_date_str
                    self.savefile.save_time_stamp(self.dateTimeData,self.stopData,self.channelData,filename,folder_path,format)
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
                    
        except NameError as e:
            print(e)
            
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
            folder_path=self.savefile.read_default_data()['Folder path']
            data_prefix="TimeStamping"
            current_date_str=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            filename=data_prefix+current_date_str
            self.savefile.save_time_stamp(self.dateTimeData[:totalLenData],self.stopData[:totalLenData],self.channelData[:totalLenData],filename,folder_path,self.selectedFormat)
            self.dateTimeData=self.dateTimeData[totalLenData:]
            self.stopData=self.stopData[totalLenData:]
            self.channelData=self.channelData[totalLenData:]
            self.currenSaving=False
            self.worker.changeReadyToReorder()
            self.dataAutoSaved=True
        except NameError as e:
            print(e)

        
    
    def autoSaveAction(self):
        self.currenSaving=True
        self.changeStatusLabel("Saving data")
        self.changeStatusColor(2)
        QApplication.processEvents() 
        try:
            totalLenData=len(self.dateTimeData)
            folder_path=self.savefile.read_default_data()['Folder path']
            data_prefix="TimeStamping"
            current_date_str=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            filename=data_prefix+current_date_str
            self.savefile.save_time_stamp(self.dateTimeData[:totalLenData],self.stopData[:totalLenData],self.channelData[:totalLenData],filename,folder_path,self.selectedFormat)
            self.dateTimeData=self.dateTimeData[totalLenData:]
            self.stopData=self.stopData[totalLenData:]
            self.channelData=self.channelData[totalLenData:]
            self.currenSaving=False
        except NameError as e:
            print(e)
    
    def fileNameAutoSave(self):
        folderpath=self.savefile.read_default_data()['Folder path']
        data_prefix="TimeStamping"
        currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        self.fileName = os.path.join(folderpath, f"{data_prefix}{currentDateStr}.{self.selectedFormat}")
    
    def dialogToShowSave(self):
        message_box = QMessageBox(self.mainWindow)
        message_box.setIcon(QMessageBox.Information)
        inital_text="The files have been saved successfully in path folder: "
        folderPath=self.savefile.read_default_data()['Folder path']
        text_route="\n\n"+ str(folderPath)+"\n\n"+"with the following name:"
        currentDateStr=self.startDateToSave.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        onlyFileName=f"TimeStamping{currentDateStr}.{self.selectedFormat}"
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
    
    
    def run(self):
        #Sync the time with the device before measurement
        self.syncTime()
        if self.normalMeasurementSentinel:
            while self.running:
                if self.isPause:    
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
                
        elif self.scheduleMeasurementSentinel:
            while self.running:
                if self.isPause:
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
        if self.limitMeasurementSentinel:
            while self.running and (not self.allMeasurementsComplete):
                if self.isPause:
                    percentage=round((self.totalMeasurements/self.maximumMeasurements)*100,2)
                    message=f"Paused measurement {percentage} %"
                    self.changeStatusText.emit(message)
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getLimitedMeasurements()
        
        if self.isAutosave:
            self.finishedMeasurements.emit()
            while not self.readyToReOrder:
                time.sleep(0.5)
            self.changeStatusText.emit("Processing data")
            self.changeStatusColor.emit(2)
            self.sortTimeStamps(self.filename)
                
    def enableDisableChannels(self):
        if self.channelASentinel:
            self.device.ch1.enableChannel()
            self.numberStopsA=self.device.ch1.getNumberOfStops()
        else:
            self.device.ch1.disableChannel()
            
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
            self.numberStopsB=self.device.ch2.getNumberOfStops()
        else:
            self.device.ch2.disableChannel()
            
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
            self.numberStopsC=self.device.ch3.getNumberOfStops()
        else:
            self.device.ch3.disableChannel()
            
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
            self.numberStopsD=self.device.ch4.getNumberOfStops()
        else:
            self.device.ch4.disableChannel()
    
    def syncTime(self):
        self.device.setDateTime()
    
    #Function to get the measurements
    
    def getLimitedMeasurements(self):
        valueA=[]
        valueB=[]
        valueC=[]
        valueD=[]
        onlyStartMeasurements=[]
        measure=self.device.measure()
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
        
    
    def getMeasurement(self):
        valueA=[]
        valueB=[]
        valueC=[]
        valueD=[]
        onlyStartMeasurements=[]
        startValues={}
        measure=self.device.measure()
        totalNoStarts=0
        StartChannelRegister=True
        if measure:
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
        self.newMeasurement.emit(valueA,valueB,valueC,valueD,onlyStartMeasurements, self.totalMeasurementsChannelA,
                                 self.totalMeasurementsChannelB,self.totalMeasurementsChannelC, self.totalMeasurementsChannelD, self.totalMeasurements)
        
    
    def changeIsPauseTrue(self):
        self.isPause= True
    
    def changeIsPauseFalse(self):
        self.isPause= False
    
    def changeReadyToReorder(self):
        self.readyToReOrder=True
        
    # Function to reorder data
    def sortTimeStamps(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            return

        header = lines[0]
        data_lines = lines[1:]
        total_lines = len(data_lines)
        parsed_data = []

        for idx, line in enumerate(data_lines):
            parts = line.strip().split('\t')
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
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(header)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}\t{stop_time}\t{channel}\n")

                if idx % max(1, len(sorted_data) // 30) == 0:
                    percent = 70 + int((idx + 1) / len(sorted_data) * 30)
                    self.changeStatusText.emit(f"Processing data {percent}%")

        self.changeStatusText.emit("Processing complete.")
    
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

        header = lines[0]
        data_lines = lines[1:]
        total_lines = len(data_lines)
        parsed_data = []

        for idx, line in enumerate(data_lines):
            parts = line.strip().split('\t')
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
            file.write(header)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}\t{stop_time}\t{channel}\n")

                if idx % max(1, len(sorted_data) // 30) == 0:
                    percent = 70 + int((idx + 1) / len(sorted_data) * 30)
                    self.changeProgress.emit(percent)

        self.changeProgress.emit(100)

        
        
            
        
        
        
    
    
    