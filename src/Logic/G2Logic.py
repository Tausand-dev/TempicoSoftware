from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum
from Utils.createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
import math
import re
from Threads.ThreadLifeTime import WorkerThreadLifeTime
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
from PySide2.QtCore import QThread, Signal, Slot
from numpy import mean, sqrt, std
from datetime import datetime
import pyTempico as tempico
import time
import threading
import numpy as np
class G2Logic():
    def __init__(self,stopChannelComboBox: QComboBox, coincidenceWindowSpinBox: QDoubleSpinBox, numberMeasurementsSpinBox: QSpinBox, timeRangeSpinBox: QSpinBox,startButton: QPushButton, stopButton: QPushButton,
                 clearButton: QPushButton,saveDataButton: QPushButton, savePlotButton: QPushButton, comboBoxEquation: QComboBox, applyFitButton: QPushButton, externalDelaySpinBox: QDoubleSpinBox, applyExternalDelayButton: QPushButton,
                 parametersTable: QTableWidget, initialParametersButton: QPushButton, statusValueLabel: QLabel, statusColorLabel: QLabel, totalStartsLabel: QLabel, totalStopsLabel: QLabel, calculatedParameter: QLabel, helpButton: QPushButton,
                 graphicFrame:QFrame,device: tempico.TempicoDevice, mainWindow, connectedTimer: QTimer):
        self.stopChannelComboBox= stopChannelComboBox
        self.coincidenceWindowSpinBox = coincidenceWindowSpinBox
        self.numberMeasurementsSpinBox= numberMeasurementsSpinBox
        self.timeRangeSpinBox = timeRangeSpinBox
        self.startButton = startButton
        self.startButton = startButton
        self.stopButton = stopButton
        self.clearButton = clearButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.comboBoxEquation = comboBoxEquation
        self.applyFitButton = applyFitButton
        self.externalDelaySpinBox = externalDelaySpinBox
        self.applyExternalDelayButton = applyExternalDelayButton
        self.parametersTable = parametersTable
        self.initialParametersButton = initialParametersButton
        self.statusValueLabel = statusValueLabel
        self.statusColorLabel = statusColorLabel
        self.totalStartsLabel = totalStartsLabel
        self.totalStopsLabel = totalStopsLabel
        self.calculatedParameter = calculatedParameter
        self.helpButton = helpButton
        self.device = device
        self.mainWindow= mainWindow
        self.connectedTimer=connectedTimer
        self.graphicFrame=graphicFrame
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        #Connect elements
        self.stopChannelComboBox.currentIndexChanged.connect(self.stopChannelChanged)
        self.comboBoxEquation.currentIndexChanged.connect(self.changeTableParameters)
        self.initialConfigs()
        self.createGraphic()
    
    
    def initialConfigs(self):
        if self.device==None:
            self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.clearButton.setEnabled(False)    
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.applyExternalDelayButton.setEnabled(False)
        self.applyFitButton.setEnabled(False)
        self.initParametersEquationThermal()
        self.initParametersEquationAntiBunching()
        self.initParametersEquationThreeLevel()
        self.changeTermalTableParameters()
    
    def connectedDevice(self, device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.device=device
        self.startButton.setEnabled(True)
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startButton.setEnabled(False)
    
    def resetSaveSentinels(self):
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
    
    def createGraphic(self):
        self.graphicLayout=QHBoxLayout(self.graphicFrame)
        self.winG2=pg.GraphicsLayoutWidget()
        self.winG2.setBackground('w')
        #Add the plot to the window
        self.plotG2=self.winG2.addPlot()
        self.plotG2.showGrid(x=True, y=True)
        #Add Labels
        self.plotG2.setLabel('left','Coincidences Start-A')
        self.plotG2.setLabel('bottom','Time')
        self.plotG2.addLegend()
        self.graphicLayout.addWidget(self.winG2)
        self.curveG2 = self.plotG2.plot(pen='b',  name='g2 Data')
        self.curveFit = self.plotG2.plot(pen='r', name='g2 fit')
    
    def stopChannelChanged(self):
        if self.stopChannelComboBox.currentIndex()==0:
            self.plotG2.setLabel('left','Coincidences Start-A')
        elif self.stopChannelComboBox.currentIndex()==1:
            self.plotG2.setLabel('left','Coincidences Start-B')
        elif self.stopChannelComboBox.currentIndex()==2:
            self.plotG2.setLabel('left','Coincidences Start-C')
        elif self.stopChannelComboBox.currentIndex()==3:
            self.plotG2.setLabel('left','Coincidences Start-D')
    
    
    def startTimerConnection(self):
        self.connectedTimer.start(500)

    
    def stopTimerConnection(self):
        self.connectedTimer.stop()
    
    def initParametersEquationThermal(self):
        self.thermalParameterAValue="nan"
        self.thermalParameterAStd="nan"
        self.thermalParameterAUnits="nan"
        self.thermalParametercValue="nan"
        self.thermalParametercStd="nan"
        self.thermalParametercUnits="nan"
        self.thermalParameterBValue="nan"
        self.thermalParameterBStd="nan"
        self.thermalParameterBUnits="nan"
        self.thermalParameterR2="nan"
    
    def initParametersEquationAntiBunching(self):
        self.antiBunchingParameterTauAValue="nan"
        self.antiBunchingParameterTauAStd="nan"
        self.antiBunchingParameterTauAUnits="nan"
        self.antiBunchingParameterR2="nan"
    
    def initParametersEquationThreeLevel(self):
        self.threeLevelParameterPfSValue="nan"
        self.threeLevelParameterPfSStd="nan"
        self.threeLevelParameterPfSUnits="nan"
        self.threeLevelParameterCValue="nan"
        self.threeLevelParameterCStd="nan"
        self.threeLevelParameterCUnits="nan"
        self.threeLevelParameterTbValue="nan"
        self.threeLevelParameterTbStd="nan"
        self.threeLevelParameterTbUnits="nan"
        self.threeLevelParameterTaValue="nan"
        self.threeLevelParameterTaStd="nan"
        self.threeLevelParameterTaUnits="nan"
        self.threeLevelParameterR2="nan"
        
        
    
    def changeTableParameters(self):
        self.parametersTable.setRowCount(0)
        if self.comboBoxEquation.currentIndex()==0:
            self.changeTermalTableParameters()
        elif self.comboBoxEquation.currentIndex()==1:
            self.changeAntiBunchingTableParameters()
        elif self.comboBoxEquation.currentIndex()==2:
            self.changeThreeLevelTableParameters()
    
    def changeTermalTableParameters(self):
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        self.parametersTable.insertRow(2)
        self.parametersTable.insertRow(3)
        if self.thermalParameterAStd=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem("A"))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem("A"))
            self.parametersTable.setItem(0,1,QTableWidgetItem(str(self.thermalParameterAValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(str(self.thermalParameterAStd)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.thermalParameterAUnits)))
            
        if self.thermalParametercValue=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem("c"))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem("c"))
            self.parametersTable.setItem(1,0,QTableWidgetItem(str(self.thermalParametercValue)))
            self.parametersTable.setItem(1,1,QTableWidgetItem(str(self.thermalParametercStd)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(str(self.thermalParametercUnits)))
        
        if self.thermalParameterBValue=="nan":
            self.parametersTable.setItem(2,0,QTableWidgetItem("B"))
            self.parametersTable.setItem(2,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(2,2,QTableWidgetItem(""))
            self.parametersTable.setItem(2,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(2,0,QTableWidgetItem("B"))
            self.parametersTable.setItem(2,0,QTableWidgetItem(str(self.thermalParameterBValue)))
            self.parametersTable.setItem(2,1,QTableWidgetItem(str(self.thermalParameterBStd)))
            self.parametersTable.setItem(2,2,QTableWidgetItem(str(self.thermalParameterBUnits)))
        if self.thermalParameterR2=="nan":
            self.parametersTable.setItem(3,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(3,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(3,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(3,1,QTableWidgetItem(self.thermalParameterR2))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
            
    
    def changeAntiBunchingTableParameters(self):
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        if self.antiBunchingParameterTauAValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem("T_a"))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem("T_a"))
            self.parametersTable.setItem(0,1,QTableWidgetItem(str(self.antiBunchingParameterTauAValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(str(self.antiBunchingParameterTauAStd)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.antiBunchingParameterTauAUnits)))
            

        if self.antiBunchingParameterR2=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(1,1,QTableWidgetItem(self.antiBunchingParameterR2))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))

    def changeThreeLevelTableParameters(self):
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        self.parametersTable.insertRow(2)
        self.parametersTable.insertRow(3)
        self.parametersTable.insertRow(4)
        if self.threeLevelParameterPfSValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem("Pf^2"))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem("Pf^2"))
            self.parametersTable.setItem(0,1,QTableWidgetItem(str(self.threeLevelParameterPfSValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(str(self.threeLevelParameterPfSStd)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.threeLevelParameterPfSUnits)))
            
        if self.threeLevelParameterCValue=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem("c"))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem("c"))
            self.parametersTable.setItem(1,0,QTableWidgetItem(str(self.threeLevelParameterCValue)))
            self.parametersTable.setItem(1,1,QTableWidgetItem(str(self.threeLevelParameterCStd)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(str(self.threeLevelParameterCUnits)))
        
        if self.threeLevelParameterTbValue=="nan":
            self.parametersTable.setItem(2,0,QTableWidgetItem("T_b"))
            self.parametersTable.setItem(2,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(2,2,QTableWidgetItem(""))
            self.parametersTable.setItem(2,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(2,0,QTableWidgetItem("T_b"))
            self.parametersTable.setItem(2,0,QTableWidgetItem(str(self.threeLevelParameterTbValue)))
            self.parametersTable.setItem(2,1,QTableWidgetItem(str(self.threeLevelParameterTbStd)))
            self.parametersTable.setItem(2,2,QTableWidgetItem(str(self.threeLevelParameterTbUnits)))
        
        if self.threeLevelParameterTaValue=="nan":
            self.parametersTable.setItem(3,0,QTableWidgetItem("T_a"))
            self.parametersTable.setItem(3,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(3,0,QTableWidgetItem("T_a"))
            self.parametersTable.setItem(3,0,QTableWidgetItem(str(self.threeLevelParameterTaValue)))
            self.parametersTable.setItem(3,1,QTableWidgetItem(str(self.threeLevelParameterTaStd)))
            self.parametersTable.setItem(3,2,QTableWidgetItem(str(self.threeLevelParameterTaUnits)))
            
        if self.threeLevelParameterR2=="nan":
            self.parametersTable.setItem(4,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(4,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(4,2,QTableWidgetItem(""))
            self.parametersTable.setItem(4,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(4,0,QTableWidgetItem("R^2"))
            self.parametersTable.setItem(4,1,QTableWidgetItem(self.threeLevelParameterR2))
            self.parametersTable.setItem(4,2,QTableWidgetItem(""))
            self.parametersTable.setItem(4,3,QTableWidgetItem(""))
    
    def startMeasurement(self):
        
        pass
    
    def stopMeasurement(self):
        pass
    
    def cleanMeasurement(self):
        pass
        
                
class WorkerThreadG2(QThread):
    updateMeasurement=Signal(list,list)
    updateStatusLabel=Signal(str)
    updateMeasurementsLabels=Signal(int,int)
    updateEstimatedParameter=Signal(float)
    def __init__(self, stopChannel: str, coincidenceWindow: float, numberMeasurements:int, timeRange:float, device: tempico.TempicoDevice):
        super().__init__()
        self.totalStarts=0
        self.totalStops=0
        self.running=True
        self.stopChannel=stopChannel
        self.coincidenceWindow=coincidenceWindow
        self.numberMeasurements=numberMeasurements
        self.timeRange=timeRange
        self.device=device
        self.saveSettings()
        self.enableDisableChannels()
    
    def enableDisableChannels(self):
        self.device.disableChannel(1)
        self.device.disableChannel(2)
        self.device.disableChannel(3)
        self.device.disableChannel(4)
        if self.stopChannel=="A":
            self.device.enableChannel(1)
            self.device.setAverageCycles(1,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
        elif self.stopChannel=="B":
            self.device.enableChannel(2)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
        elif self.stopChannel=="C":
            self.device.enableChannel(3)
            self.device.setAverageCycles(3,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
        elif self.stopChannel=="D":
            self.device.enableChannel(4)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
    
    
    
    def saveSettings(self):
        self.numberRunsSaved=self.device.getNumberOfRuns()
        self.numberStopsChannelA=self.device.getNumberOfStops(1)
        self.numberStopsChannelB=self.device.getNumberOfStops(2)
        self.numberStopsChannelC=self.device.getNumberOfStops(3)
        self.numberStopsChannelD=self.device.getNumberOfStops(4)
        self.stopMaskChannelA=self.device.getStopMask(1)
        self.stopMaskChannelB=self.device.getStopMask(2)
        self.stopMaskChannelC=self.device.getStopMask(3)
        self.stopMaskChannelD=self.device.getStopMask(4)
        self.averageCyclesChannelA=self.device.getAverageCycles(1)
        self.averageCyclesChannelB=self.device.getAverageCycles(2)
        self.averageCyclesChannelC=self.device.getAverageCycles(3)
        self.averageCyclesChannelD=self.device.getAverageCycles(4)
        self.modeChannelA=self.device.getMode(1)
        self.modeChannelB=self.device.getMode(2)
        self.modeChannelC=self.device.getMode(3)
        self.modeChannelD=self.device.getMode(4)
    
    def recoverSettings(self):
        self.device.enableChannel(1)
        self.device.enableChannel(2)
        self.device.enableChannel(3)
        self.device.enableChannel(4)
        self.device.setNumberOfRuns(self.numberRunsSaved)
        self.device.setNumberOfStops(1,self.numberStopsChannelA)
        self.device.setNumberOfStops(2,self.numberStopsChannelB)
        self.device.setNumberOfStops(3,self.numberStopsChannelC)
        self.device.setNumberOfStops(4,self.numberStopsChannelD)
        self.device.setStopMask(1,self.stopMaskChannelA)
        self.device.setStopMask(2,self.stopMaskChannelB)
        self.device.setStopMask(3,self.stopMaskChannelC)
        self.device.setStopMask(4,self.stopMaskChannelD)
        self.device.setAverageCycles(1,self.averageCyclesChannelA)
        self.device.setAverageCycles(2,self.averageCyclesChannelB)
        self.device.setAverageCycles(3,self.averageCyclesChannelC)
        self.device.setAverageCycles(4,self.averageCyclesChannelD)
        self.device.setMode(1,self.modeChannelA)
        self.device.setMode(2,self.modeChannelB)
        self.device.setMode(3,self.modeChannelC)
        self.device.setMode(4,self.modeChannelD)
    
        
        
    
    
        
    
    
    
    
    
    
        
        