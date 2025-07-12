from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor, QFont
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QHeaderView,QAbstractItemView, QApplication, QHBoxLayout, QDateTimeEdit, QSpinBox
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
    def __init__(self,enableCheckBoxA: QCheckBox,enableCheckBoxB: QCheckBox,enableCheckBoxC: QCheckBox,enableCheckBoxD: QCheckBox,scheduleCheckBox:QCheckBox,scheduleTimeEdit: QDateTimeEdit,
                 limitMeasurementsCheckBox: QCheckBox, limitMeasurementsSpinBox: QSpinBox, showTableCheckBox: QCheckBox, syncComboBox: QComboBox, startButton: QPushButton, pauseButton: QPushButton,
                 stopButton: QPushButton, saveDataButton: QPushButton, valueMeasurementA: QLabel,valueMeasurementB: QLabel,valueMeasurementC: QLabel,valueMeasurementD: QLabel, valueTotalMeasurement: QLabel,
                 measurementLabelA: QLabel,measurementLabelB: QLabel,measurementLabelC: QLabel,measurementLabelD: QLabel,tableTimeStamp: QTableWidget,
                 statusLabel: QLabel, colorLabel: QLabel, parent, device):
        #Define the elements from the class
        self.enableCheckBoxA=enableCheckBoxA
        self.enableCheckBoxB=enableCheckBoxB
        self.enableCheckBoxC=enableCheckBoxC
        self.enableCheckBoxD=enableCheckBoxD
        self.scheduleCheckBox=scheduleCheckBox
        self.scheduleTimeEdit=scheduleTimeEdit
        self.limitMeasurementsCheckBox=limitMeasurementsCheckBox
        self.limitMeasurementsSpinBox=limitMeasurementsSpinBox
        self.showTableCheckBox=showTableCheckBox
        self.syncCheckBox=syncComboBox
        self.startButton=startButton
        self.pauseButton=pauseButton
        self.stopButton=stopButton
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
        #Connect checkBox
        self.showTableCheckBox.stateChanged.connect(self.updateShowTable)
        self.scheduleCheckBox.stateChanged.connect(self.updateScheduleTime)
        self.limitMeasurementsCheckBox.stateChanged.connect(self.updateLimitMeasurements)
        self.enableCheckBoxA.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxB.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxC.stateChanged.connect(self.updateCheckBoxLabels)
        self.enableCheckBoxD.stateChanged.connect(self.updateCheckBoxLabels)
        #Set default states
        self.scheduleTimeEdit.setEnabled(False)
        self.limitMeasurementsSpinBox.setEnabled(False)
        self.valueMeasurementA.setVisible(False)
        self.measurementLabelA.setVisible(False)
        self.valueMeasurementB.setVisible(False)
        self.measurementLabelB.setVisible(False)
        self.valueMeasurementC.setVisible(False)
        self.measurementLabelC.setVisible(False)
        self.valueMeasurementD.setVisible(False)
        self.measurementLabelD.setVisible(False)
        #Buttons disabled if there is not device
        if device==None:
            self.startButton.setEnabled(False)
            self.pauseButton.setEnabled(False)
            self.stopButton.setEnabled(False)
        else:
            self.startButton.setEnabled(True)
            self.pauseButton.setEnabled(False)
            self.stopButton.setEnabled(False)
    
    # Functions to connect and disconnect device
    def connectedDevice(self,device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.disconnectedMeasurement=False
        self.device=device
        self.startButton.setEnabled(True)
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startButton.setEnabled(False)
    
    #Functions graphic interface
    def updateShowTable(self):
        if self.showTableCheckBox.isChecked():
            self.tableTimeStamp.setVisible(True)
        else:
            self.tableTimeStamp.setVisible(False)
            
    
    def updateScheduleTime(self):
        if self.scheduleCheckBox.isChecked():
            self.scheduleTimeEdit.setEnabled(True)
        else:
            self.scheduleTimeEdit.setEnabled(False)
            
    
    def updateLimitMeasurements(self):
        if self.limitMeasurementsCheckBox.isChecked():
            self.limitMeasurementsSpinBox.setEnabled(True)
        else:
            self.limitMeasurementsSpinBox.setEnabled(False)
    
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
        