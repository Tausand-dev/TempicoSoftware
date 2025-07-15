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
                 statusLabel: QLabel,colorLabel:QLabel, saveDataComplete:QCheckBox,tabNormalMeasurement: QWidget, tabScheduleMeasurement: QWidget, tabLimitedMeasurement: QWidget, saveDataButton:QPushButton, tabs:QTabWidget,parent,device):
        #Define the elements from the class
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
        pass
    
    def stopNormalMeasurement(self):
        self.worker.stop()
        self.changeStatusColor(0)
        self.changeStatusLabel("No measurement running")
        self.startNormalButton.setEnabled(True)
        self.pauseNormalButton.setEnabled(False)
        self.stopNormalButton.setEnabled(False)
        self.tabs.setTabEnabled(1,True)
        self.tabs.setTabEnabled(2,True)
    
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
    
    def captureMeasurement(self):
        pass


class WorkerThreadCountsEstimated(QThread):
    newMeasurement=Signal()
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
        #Sentinel for running
        self.running=True
        #Enable and disable the channels
        self.enableDisableChannels()
    
    
    def run(self):
        #Sync the time with the device before measurement
        self.syncTime()
        if self.normalMeasurementSentinel:
            while self.running:
                self.changeStatusColor.emit(1)
                self.changeStatusText.emit("Running measurement")
                print("Se realiza una medición normal")
                time.sleep(1)
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
        else:
            self.device.ch1.disableChannel()
            
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
        else:
            self.device.ch2.disableChannel()
            
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
        else:
            self.device.ch3.disableChannel()
            
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
        else:
            self.device.ch4.disableChannel()
    
    def syncTime(self):
        self.device.setDateTime()


    @Slot()   
    def stop(self):
        self.running=False      
            
        
        
        
    
    
    