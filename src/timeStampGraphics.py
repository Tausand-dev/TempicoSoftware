from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor, QFont
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QWidget, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QHeaderView,QAbstractItemView, QApplication, QHBoxLayout, QDateEdit, QTimeEdit, QSpinBox, QTabWidget
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace, std
from numpy import append as appnd
from createsavefile import createsavefile as savefile
from datetime import datetime, date
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
import time
import random
import threading
from pyqtgraph import mkPen
import os
import numpy as np
class TimeStampLogic():
    def __init__(self,enableCheckBoxA: QCheckBox,enableCheckBoxB: QCheckBox,enableCheckBoxC: QCheckBox,enableCheckBoxD: QCheckBox, startNormalButton: QPushButton, pauseNormalButton: QPushButton, stopNormalButton: QPushButton ,
                 startScheduleButton: QPushButton, pauseScheduleButton: QPushButton, stopScheduleButton: QPushButton,startLimitedButton: QPushButton, pauseLimitedButton: QPushButton, stopLimitedButton: QPushButton
                 ,startDate: QDateEdit,startTime: QTimeEdit,finishDate: QDateEdit,finishTime: QTimeEdit, numberMeasurementsSpinBox: QSpinBox, showTableCheckBox: QCheckBox,measurementLabelA: QLabel,measurementLabelB: QLabel,
                 measurementLabelC: QLabel, measurementLabelD: QLabel,valueMeasurementA: QLabel,valueMeasurementB: QLabel,valueMeasurementC: QLabel,valueMeasurementD: QLabel,valueTotalMeasurement: QLabel, tableTimeStamp: QTableWidget,
                 statusLabel: QLabel,colorLabel:QLabel, saveDataComplete:QCheckBox,tabNormalMeasurement: QWidget, tabScheduleMeasurement: QWidget, tabLimitedMeasurement: QWidget, saveDataButton:QPushButton, tabs:QTabWidget,parent,device, timerConnection: QTimer):
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
        #Save data button
        self.saveDataButton=saveDataButton
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
        #Connect buttons
        self.startNormalButton.clicked.connect(self.startNormalMeasurement)
        self.pauseNormalButton.clicked.connect(self.pauseNormalMeasurement)
        self.stopNormalButton.clicked.connect(self.stopNormalMeasurement)
        #Sentinels
        self.channelASentinel=False
        self.channelBSentinel=False
        self.channelCSentinel=False
        self.channelDSentinel=False
        #Device
        self.device=device
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
            self.startNormalButton.setEnabled(False)
            self.pauseNormalButton.setEnabled(True)
            self.stopNormalButton.setEnabled(True)
            self.tabs.setTabEnabled(1,False)
            self.tabs.setTabEnabled(2,False)
            #Set values 
            self.setValuesBeforeMeasurement()
            self.changeStatusColor(1)
            self.stopTimerConnection()
            self.mainWindow.activeMeasurement()
            #Init thread
            self.worker= WorkerThreadCountsEstimated(self.channelASentinel,self.channelBSentinel, self.channelCSentinel, self.channelDSentinel,True,False,False, self.device)
            self.worker.finished.connect(self.finishedThread)
            self.worker.newMeasurement.connect(self.captureMeasurement)
            self.worker.changeStatusColor.connect(self.changeStatusColor)
            self.worker.changeStatusText.connect(self.changeStatusLabel)
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
        self.worker.stop()
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.startNormalButton.setEnabled(True)
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(2,True)
        self.startTimerConnection()
    
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
        
    
    def showDialogNoChannels(self):
        QMessageBox.warning(
            self.mainWindow,  
            "Not selected channels",
            "You must select at least one channel to start measurement"
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
        self.statusLabel.setText(textValue)
        
        
    def finishedThread(self):
        
        self.stopNormalMeasurement()
    
    def captureMeasurement(self, valuesA, valuesB,valuesC,valuesD, valuesStart, totalMeasurementsChannelA,totalMeasurementsChannelB,totalMeasurementsChannelC,totalMeasurementsChannelD,totalMeasurements):
        moreThan50000=False
        #Update table
        if self.tableTimeStamp.rowCount()>50000:
            moreThan50000=True
        for tupleValueA in valuesA:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueA[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueA[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("A"))
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)   
        for tupleValueB in valuesB:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueB[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueB[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("B"))
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueC in valuesC:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueC[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueC[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("C"))
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueD in valuesD:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueD[0]))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem(str(tupleValueD[1])))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("D"))
            if moreThan50000:
                 self.tableTimeStamp.removeRow(self.tableTimeStamp.rowCount() - 1)
        for tupleValueStart in valuesStart:
            self.tableTimeStamp.insertRow(0)
            self.tableTimeStamp.setItem(0,0,QTableWidgetItem(tupleValueStart))
            self.tableTimeStamp.setItem(0,1,QTableWidgetItem("-1"))
            self.tableTimeStamp.setItem(0,2,QTableWidgetItem("Start"))
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
        
        


class WorkerThreadCountsEstimated(QThread):
    newMeasurement=Signal(tuple,tuple,tuple,tuple,tuple,float,float,float,float,float)
    changeStatusText=Signal(str)
    changeStatusColor=Signal(int)
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel, channelDSentinel,normalMeasurementSentinel, scheduleMeasurementSentinel,limitMeasurementSentinel,
                 device: tempico.TempicoDevice):
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
        #Sentinel to pause thread
        self.isPause=False
        #Sentinel for running
        self.running=True
        #Enable and disable the channels
        self.enableDisableChannels()
    
    
    def run(self):
        #Sync the time with the device before measurement
        self.syncTime()
        if self.normalMeasurementSentinel:
            while self.running:
                if self.isPause:
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
                
        elif self.scheduleMeasurementSentinel:
            for i in range(10):
                print("Se realiza una medición programada")
                time.sleep(1)
        if self.limitMeasurementSentinel:
            for i in range(10):
                print("Se realiza una medición limitada por mediciones")
                time.sleep(1)
                
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
    
    def getMeasurement(self):
        valueA=[]
        valueB=[]
        valueC=[]
        valueD=[]
        onlyStartMeasurements=[]
        measure=self.device.measure()
        numberRun=0
        if measure:
            for channelMeasure in measure:
                if channelMeasure:
                    if channelMeasure[1]!=numberRun:
                        #generar medición con solamente el start
                        if numberRun!=0:
                            if not measuresDetected:
                                self.totalMeasurements+=1
                                onlyStartMeasurements.append(startValue)
                        numberRun=channelMeasure[1]
                        startValue=channelMeasure[2]
                        startValue= str(datetime.fromtimestamp(startValue))
                        measuresDetected=False
                    if self.channelASentinel:
                        if channelMeasure[0]==1:
                            if channelMeasure[3]!=-1:
                                measuresDetected=True
                                valueA.append((startValue,channelMeasure[3]))
                                self.totalMeasurements+=1
                                self.totalMeasurementsChannelA+=1
                            if self.numberStopsA>1:
                                if channelMeasure[4]!=-1:
                                    measuresDetected=True
                                    valueA.append((startValue,channelMeasure[4]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                            if self.numberStopsA>2:
                                if channelMeasure[5]!=-1:
                                    measuresDetected=True
                                    valueA.append((startValue,channelMeasure[5]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                            if self.numberStopsA>3:
                                if channelMeasure[6]!=-1:
                                    measuresDetected=True
                                    valueA.append((startValue,channelMeasure[6]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                            if self.numberStopsA>4:
                                if channelMeasure[7]!=-1:
                                    measuresDetected=True
                                    valueA.append((startValue,channelMeasure[7]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelA+=1
                            
                                
                    if self.channelBSentinel:
                        if channelMeasure[0]==2:
                            if channelMeasure[3]!=-1:
                                measuresDetected=True
                                valueB.append((startValue,channelMeasure[3]))
                                self.totalMeasurements+=1
                                self.totalMeasurementsChannelB+=1
                            if self.numberStopsB>1:
                                if channelMeasure[4]!=-1:
                                    measuresDetected=True
                                    valueB.append((startValue,channelMeasure[4]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                            if self.numberStopsB>2:
                                if channelMeasure[5]!=-1:
                                    measuresDetected=True
                                    valueB.append((startValue,channelMeasure[5]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                            if self.numberStopsB>3:
                                if channelMeasure[6]!=-1:
                                    measuresDetected=True
                                    valueB.append((startValue,channelMeasure[6]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                            if self.numberStopsB>4: 
                                if channelMeasure[7]!=-1:
                                    measuresDetected=True
                                    valueB.append((startValue,channelMeasure[7]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelB+=1
                    if self.channelCSentinel:
                        if channelMeasure[0]==3:
                            if channelMeasure[3]!=-1:
                                measuresDetected=True
                                valueC.append((startValue,channelMeasure[3]))
                                self.totalMeasurements+=1
                                self.totalMeasurementsChannelB+=1
                            if self.numberStopsC>1: 
                                if channelMeasure[4]!=-1:
                                    measuresDetected=True
                                    valueC.append((startValue,channelMeasure[4]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelC+=1
                            if self.numberStopsC>2:
                                if channelMeasure[5]!=-1:
                                    measuresDetected=True
                                    valueC.append((startValue,channelMeasure[5]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelC+=1
                            if self.numberStopsC>3:
                                if channelMeasure[6]!=-1:
                                    measuresDetected=True
                                    valueC.append((startValue,channelMeasure[6]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelC+=1
                            if self.numberStopsC>4:
                                if channelMeasure[7]!=-1:
                                    measuresDetected=True
                                    valueC.append((startValue,channelMeasure[7]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelC+=1
                    if self.channelDSentinel:
                        if channelMeasure[0]==4:
                            if channelMeasure[3]!=-1:
                                measuresDetected=True
                                valueD.append((startValue,channelMeasure[3]))
                                self.totalMeasurements+=1
                                self.totalMeasurementsChannelD+=1
                            if self.numberStopsD>1:
                                if channelMeasure[4]!=-1:
                                    measuresDetected=True
                                    valueD.append((startValue,channelMeasure[4]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
                            if self.numberStopsD>2:
                                if channelMeasure[5]!=-1:
                                    measuresDetected=True
                                    valueD.append((startValue,channelMeasure[5]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
                            if self.numberStopsD>3:
                                if channelMeasure[6]!=-1:
                                    measuresDetected=True
                                    valueD.append((startValue,channelMeasure[6]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
                            if self.numberStopsD>4:
                                if channelMeasure[7]!=-1:
                                    measuresDetected=True
                                    valueD.append((startValue,channelMeasure[7]))
                                    self.totalMeasurements+=1
                                    self.totalMeasurementsChannelD+=1
        if not measuresDetected:
            self.totalMeasurements+=1
            onlyStartMeasurements.append(startValue)
        channelStringList=[]
        if self.channelASentinel and not valueA:
            channelStringList.append("A")
        if self.channelBSentinel and not valueB:
            channelStringList.append("B")
        if self.channelCSentinel and not valueC:
            channelStringList.append("C")
        if self.channelDSentinel and not valueD:
            channelStringList.append("D")
        if channelStringList:
            channelErrorString=", ".join(channelStringList)
            if len(channelStringList)==1:
                errorMessage=f"The channnel {channelErrorString} is not taking measurements"
            else:
                errorMessage=f"The channnels {channelErrorString} are not taking measurements"
            self.changeStatusText.emit(errorMessage)
            self.changeStatusColor.emit(3)
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
              
    
    @Slot()   
    def stop(self):
        self.running=False      
        
            
        
        
        
    
    
    