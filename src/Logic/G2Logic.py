from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox, QTabWidget
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
    def __init__(self,stopChannelComboBox: QComboBox, coincidenceWindowComboBox: QComboBox, numberMeasurementsSpinBox: QSpinBox, numberBinsComboBox: QComboBox,startManualButton: QPushButton, stopManualButton: QPushButton,
                 clearButton: QPushButton,saveDataButton: QPushButton, savePlotButton: QPushButton, comboBoxEquation: QComboBox, applyFitButton: QPushButton, externalDelaySpinBox: QDoubleSpinBox,
                 parametersTable: QTableWidget, initialParametersButton: QPushButton, statusValueLabel: QLabel, statusColorLabel: QLabel, totalStartsLabel: QLabel, totalStopsLabel: QLabel, calculatedParameter: QLabel, helpButton: QPushButton,
                 graphicFrame:QFrame, startLimitedButtonG2: QPushButton, stopLimitedButtonG2: QPushButton, clearLimitedButtonG2: QPushButton, autoClearSpinBox: QSpinBox, startAutoClearButton: QPushButton,
                 stopAutoClearButton: QPushButton, clearAutoClearButton: QPushButton,maximumTimeLabel: QLabel, tabSettings: QTabWidget,device: tempico.TempicoDevice, mainWindow, connectedTimer: QTimer):
        self.stopChannelComboBox= stopChannelComboBox
        self.coincidenceWindowComboBox = coincidenceWindowComboBox
        self.numberMeasurementsSpinBox= numberMeasurementsSpinBox
        self.numberBinsComboBox = numberBinsComboBox
        self.startManualButton = startManualButton
        self.stopManualButton = stopManualButton
        self.clearButton = clearButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.comboBoxEquation = comboBoxEquation
        self.applyFitButton = applyFitButton
        self.externalDelaySpinBox = externalDelaySpinBox
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
        self.startLimitedButtonG2=startLimitedButtonG2
        self.stopLimitedButtonG2=stopLimitedButtonG2
        self.clearLimitedButtonG2=clearLimitedButtonG2
        self.autoClearSpinBox=autoClearSpinBox
        self.startAutoClearButton=startAutoClearButton
        self.stopAutoClearButton=stopAutoClearButton
        self.clearAutoClearButton=clearAutoClearButton
        self.maximumTimeLabel=maximumTimeLabel
        self.tabSettings=tabSettings
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        self.currentMeasurement=False
        #Connect elements
        self.stopChannelComboBox.currentIndexChanged.connect(self.stopChannelChanged)
        self.comboBoxEquation.currentIndexChanged.connect(self.changeTableParameters)
        self.startManualButton.clicked.connect(self.startManualMeasurement)
        self.stopManualButton.clicked.connect(self.stopManualMeasurement)
        self.clearButton.clicked.connect(self.clearManualMeasurement)
        self.startLimitedButtonG2.clicked.connect(self.startLimitedMeasurement)
        self.stopLimitedButtonG2.clicked.connect(self.stopLimitedMeasurement)
        self.clearLimitedButtonG2.clicked.connect(self.clearManualMeasurement)
        self.clearAutoClearButton.clicked.connect(self.clearManualMeasurement)
        #self.externalDelaySpinBox.valueChanged.connect(self.changeExternalDelay)
        self.initialConfigs()
        self.createGraphic()
    
    
    def initialConfigs(self):
        if self.device==None:
            self.startManualButton.setEnabled(False)
        self.stopManualButton.setEnabled(False)
        self.clearButton.setEnabled(False)    
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.applyFitButton.setEnabled(False)
        self.initParametersEquationThermal()
        self.initParametersEquationAntiBunching()
        self.initParametersEquationThreeLevel()
        self.changeTermalTableParameters()
    
    def connectedDevice(self, device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.device=device
        self.startManualButton.setEnabled(True)
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startManualButton.setEnabled(False)
    
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
        self.plotG2.setLabel('left','g2(tau) Start-A')
        self.plotG2.setLabel('bottom','Tau')
        self.plotG2.addLegend()
        self.graphicLayout.addWidget(self.winG2)
        self.curveG2 = self.plotG2.plot(pen='b',  name='g2 Data')
        self.curveFit = self.plotG2.plot(pen='r', name='g2 fit')
    
    def stopChannelChanged(self):
        if self.stopChannelComboBox.currentIndex()==0:
            self.plotG2.setLabel('left','g2(tau) Start-A')
        elif self.stopChannelComboBox.currentIndex()==1:
            self.plotG2.setLabel('left','g2(tau) Start-B')
        elif self.stopChannelComboBox.currentIndex()==2:
            self.plotG2.setLabel('left','g2(tau) Start-C')
        elif self.stopChannelComboBox.currentIndex()==3:
            self.plotG2.setLabel('left','g2(tau) Start-D')
    
    
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
    
    #Manual measurement 
    def startManualMeasurement(self):
        self.stopManualButton.setEnabled(True)
        self.startManualButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.stopTimerConnection()
        self.applyFitButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(False)
        self.coincidenceWindowComboBox.setEnabled(False)
        self.numberBinsComboBox.setEnabled(False)
        self.tabSettings.setTabEnabled(1,False)
        self.tabSettings.setTabEnabled(2,False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.tauValues=[]
        self.determinedParameters=False
        self.currentMeasurement=True
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeLabel.text())
        numberBins=int(self.numberBinsComboBox.currentText())
        self.externalDelaySpinBox.setEnabled(False)
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device)
        self.worker.updateStatusLabel.connect(self.changeStatus)
        self.worker.updateColorLabel.connect(self.changeStatusColor)
        self.worker.updateEstimatedParameter.connect(self.changeEstimatedParameter)
        self.worker.updateDeterminedParameters.connect(self.changeDeterminedParameters)
        self.worker.updateTauValues.connect(self.captureTauValues)
        self.worker.updateMeasurement.connect(self.captureMeasurement)
        self.worker.finished.connect(self.finishManualMeasurement)
        self.worker.start()
    
    def stopManualMeasurement(self):
        self.worker.stop()
        self.stopManualButton.setEnabled(False)
        
    def getPicoSecondsValue(self, valueStr):
        units=valueStr.split(" ")
        print(units)
        if units[1]=="ps":
            value=float(units[0])
        elif units[1]=="ns":
            value=float(units[0])*(10**(3))
        elif units[1]=="µs":
            value=float(units[0])*(10**(6))
        elif units[1]=="ms":
            value=float(units[0])*(10**(9))
        return value
        
    
    def clearManualMeasurement(self):
        self.worker.clearG2()
        
     
    #By size measurement
    def startLimitedMeasurement(self):
        self.stopLimitedButtonG2.setEnabled(True)
        self.startLimitedButtonG2.setEnabled(False)
        self.clearLimitedButtonG2.setEnabled(True)
        self.numberMeasurementsSpinBox.setEnabled(False)
        self.stopTimerConnection()
        self.applyFitButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(False)
        self.coincidenceWindowComboBox.setEnabled(False)
        self.numberBinsComboBox.setEnabled(False)
        self.tabSettings.setTabEnabled(0,False)
        self.tabSettings.setTabEnabled(2,False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.tauValues=[]
        self.determinedParameters=False
        self.currentMeasurement=True
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeLabel.text())
        numberBins=int(self.numberBinsComboBox.currentText())
        numberMeasurements=int(self.numberMeasurementsSpinBox.value())
        self.timerAutoClear = QTimer()
        self.timerAutoClear.timeout.connect(self.clearManualMeasurement)
        self.externalDelaySpinBox.setEnabled(False)
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device, True, numberMeasurements)
        self.worker.updateStatusLabel.connect(self.changeStatus)
        self.worker.updateColorLabel.connect(self.changeStatusColor)
        self.worker.updateEstimatedParameter.connect(self.changeEstimatedParameter)
        self.worker.updateDeterminedParameters.connect(self.changeDeterminedParameters)
        self.worker.updateTauValues.connect(self.captureTauValues)
        self.worker.updateMeasurement.connect(self.captureMeasurement)
        self.worker.finished.connect(self.finishLimitedMeasurement)
        self.worker.start()
        
    
    def stopLimitedMeasurement(self):
        self.worker.stop()
        self.stopLimitedButtonG2.setEnabled(False)
    
    
    
    #Auto clear measurement
    def startAutoClearMeasurement(self):
        self.stopAutoClearButton.setEnabled(True)
        self.startAutoClearButton.setEnabled(False)
        self.clearAutoClearButton.setEnabled(True)
        self.stopTimerConnection()
        self.applyFitButton.setEnabled(False)
        self.stopChannelComboBox.setEnabled(False)
        self.coincidenceWindowComboBox.setEnabled(False)
        self.autoClearSpinBox.setEnabled(False)
        self.tabSettings.setTabEnabled(0,False)
        self.tabSettings.setTabEnabled(1,False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.tauValues=[]
        self.determinedParameters=False
        self.currentMeasurement=True
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeLabel.text())
        numberBins=int(self.numberBinsComboBox.currentText())
        self.externalDelaySpinBox.setEnabled(False)
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device)
        self.worker.updateStatusLabel.connect(self.changeStatus)
        self.worker.updateColorLabel.connect(self.changeStatusColor)
        self.worker.updateEstimatedParameter.connect(self.changeEstimatedParameter)
        self.worker.updateDeterminedParameters.connect(self.changeDeterminedParameters)
        self.worker.updateTauValues.connect(self.captureTauValues)
        self.worker.updateMeasurement.connect(self.captureMeasurement)
        self.worker.finished.connect(self.finishManualMeasurement)
        self.worker.start()
    
    
    def stopAutoClearMeasurement(self):
        pass
    
    
    def finishManualMeasurement(self):
        if not self.determinedParameters:
            self.showDialogNoParameters()
        self.stopManualButton.setEnabled(False)
        self.startManualButton.setEnabled(True)
        self.clearButton.setEnabled(False)
        self.startTimerConnection()
        self.applyFitButton.setEnabled(True)
        self.stopChannelComboBox.setEnabled(True)
        self.coincidenceWindowComboBox.setEnabled(True)
        self.numberBinsComboBox.setEnabled(True)
        self.tabSettings.setTabEnabled(1,True)
        self.tabSettings.setTabEnabled(2,True)
        self.saveDataButton.setEnabled(True)
        self.savePlotButton.setEnabled(True)
        self.changeStatus("No running measurement")
        self.changeStatusColor(0)
        self.currentMeasurement=False
    
    def finishLimitedMeasurement(self):
        if not self.determinedParameters:
            self.showDialogNoParameters()
        self.stopLimitedButtonG2.setEnabled(False)
        self.startLimitedButtonG2.setEnabled(True)
        self.clearLimitedButtonG2.setEnabled(False)
        self.startTimerConnection()
        self.applyFitButton.setEnabled(True)
        self.stopChannelComboBox.setEnabled(True)
        self.coincidenceWindowComboBox.setEnabled(True)
        self.numberBinsComboBox.setEnabled(True)
        self.tabSettings.setTabEnabled(0,True)
        self.tabSettings.setTabEnabled(2,True)
        self.saveDataButton.setEnabled(True)
        self.savePlotButton.setEnabled(True)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.changeStatus("No running measurement")
        self.changeStatusColor(0)
        self.currentMeasurement=False
    
    
    def showDialogNoParameters(self):
        QMessageBox.warning(
            self.mainWindow,
            "Insufficient Measurements",
            "Not enough measurements have been detected on the START or STOP channel.\n"
            "Therefore, it is not possible to determine the parameters required "
            "to correctly calculate g²."
        )
    
    def getChannelComboBox(self):
        if self.stopChannelComboBox.currentText()=="Channel A":
            return "A"
        elif self.stopChannelComboBox.currentText()=="Channel B":
            return "B"
        elif self.stopChannelComboBox.currentText()=="Channel C":
            return "C"
        elif self.stopChannelComboBox.currentText()=="Channel D":
            return "D"
    #Change status
    def changeStatus(self, text):
        self.statusValueLabel.setText(text)
    
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
        pixmap = QPixmap(self.statusColorLabel.size())
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
        point_size = min(self.statusColorLabel.width(), self.statusColorLabel.height()) // 2
        x = (self.statusColorLabel.width() - point_size) // 2
        y = (self.statusColorLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusColorLabel.setPixmap(pixmap)
    
    def changeEstimatedParameter(self, text):
        self.calculatedParameter.setText(text)
        
    def changeDeterminedParameters(self):
        self.determinedParameters=True
    
    def captureTauValues(self, tauValues):
        self.tauValues=tauValues
        self.externalDelaySpinBox.setEnabled(True)
    
    def changeExternalDelay(self):
        if self.currentMeasurement:
            externalDelayUs=self.externalDelaySpinBox.value()
            externalValueMs=externalDelayUs/(10**3)
            newTauValues=[]
            for tau in self.tauValues:
                newTau=tau-externalValueMs
                newTauValues.append(newTau)
            self.tauValues=np.array(newTauValues)
    
    def captureMeasurement(self, g2Values, totalStarts, totalStops):
        self.curveG2.setData(self.tauValues, g2Values)
        self.totalStartsLabel.setText(str(totalStarts))
        self.totalStopsLabel.setText(str(totalStops))
    
    
        
    
    
                
class WorkerThreadG2(QThread):
    updateMeasurement=Signal(list, int, int)
    updateTauValues=Signal(list)
    updateStatusLabel=Signal(str)
    updateColorLabel=Signal(int)
    updateEstimatedParameter=Signal(str)
    updateDeterminedParameters=Signal()
    def __init__(self, stopChannel: str, maximumTime: float, numberBins:int, coincidenceWindow: float, device: tempico.TempicoDevice,limitedMeasurement=False,numberOfMeasurements=0):
        super().__init__()
        self.totalStarts=0
        self.totalStops=0
        self.running=True
        self.stopChannel=stopChannel
        self.maximumTime=maximumTime
        self.numberBins=numberBins
        self.coincidenceWindow=self.psToS(coincidenceWindow)
        self.isLimitedMeasurement=limitedMeasurement
        self.numberMeasurements=numberOfMeasurements
        self.device=device
        self.totalTimeIntegration=0
        self.bins=self.generateBinList()
        self.TauValues = (0.5 * (self.bins[:-1] + self.bins[1:])/(10**9))
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.saveSettings()
        self.settingsForEstimate()
        
    
    def run(self):
        self.estimatedParameter=self.estimatedParameterValue()
        if self.estimatedParameter==-1 and self.running:
            print("Cannot estimated due to low number of values")
        elif self.estimatedParameter!=-1 and self.running:
            self.updateEstimatedParameter.emit(str(int(self.estimatedParameter)))
            self.updateDeterminedParameters.emit()
            self.updateTauValues.emit(self.TauValues)
        self.settingsForMeasurement()
        self.updateStatusLabel.emit("Running measurement")
        self.updateColorLabel.emit(1)
        while self.running:
            self.getMeasurement()
        self.recoverSettings()
    
    
    
    def settingsForEstimate(self):
        self.device.setNumberOfRuns(1)
        self.device.disableChannel(1)
        self.device.disableChannel(2)
        self.device.disableChannel(3)
        self.device.disableChannel(4)
        if self.stopChannel=="A":
            self.device.enableChannel(1)
            self.device.setAverageCycles(1,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
            self.device.setNumberOfStops(1,2)
        elif self.stopChannel=="B":
            self.device.enableChannel(2)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
            self.device.setNumberOfStops(2,2)
        elif self.stopChannel=="C":
            self.device.enableChannel(3)
            self.device.setAverageCycles(3,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
            self.device.setNumberOfStops(3,2)
        elif self.stopChannel=="D":
            self.device.enableChannel(4)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,2)
            self.device.setNumberOfStops(4,2)
    
    def settingsForMeasurement(self):
        self.device.setNumberOfRuns(100)
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,2)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,2)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,2)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,2)
        
        
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
    
    def estimatedParameterValue(self):
        notRegisteredMeasurements=0
        percentage=0
        self.updateStatusLabel.emit(f"Taking initial parameters {percentage}%")
        self.updateColorLabel.emit(2)
        estimatedDifferences=[]
        notStartsDetected=0
        for i in range(100):
            if not self.running:
                return -1
            measurement=self.device.measure()
            print(measurement)
            if notStartsDetected>=10:
                self.updateStatusLabel.emit(f"Taking initial parameters 100% (Waiting start 10/10)")
                return -1
            if not measurement:
                notRegisteredMeasurements+=1
                notStartsDetected+=1
                
            else:
                notStartsDetected=0
                if len(measurement[0])==5:
                    stop1=measurement[0][3]
                    stop2=measurement[0][4]
                    differenceEstimated=stop2-stop1
                    estimatedDifferences.append(differenceEstimated)
                else:
                    notRegisteredMeasurements+=1
            percentage=i+1
            if notRegisteredMeasurements>0:
                self.updateStatusLabel.emit(f"Taking initial parameters {percentage}% (Waiting start {notRegisteredMeasurements}/10)")
            else:
                self.updateStatusLabel.emit(f"Taking initial parameters {percentage}%")
                
        self.updateStatusLabel.emit(f"Taking initial parameters 100%")
        if notRegisteredMeasurements>700:
            return -1
        else:
            return self.getCountPerSecondParameter(estimatedDifferences)
    
    
    def getMeasurement(self):
        measurement = self.device.measure()
        totalStopPerMeasurement=0
        sortedMeasurement = self.sortByStart(measurement)
        timeDifferences, stopDifferences = [], []
        notStartsMeasurement=0
        for run in sortedMeasurement:
            if not run:
                notStartsMeasurement+=1
                continue
            totalStopPerMeasurement+=self.processRun(run, timeDifferences, stopDifferences)
            if self.isLimitedMeasurement and self.totalStops>=self.numberMeasurements:
                self.updateDeterminedParameters.emit()
                self.running=False
                break 
        if self.totalTimeIntegration>0:
            g2Values=self.buildG2Histogram(timeDifferences)
            self.updateMeasurement.emit(g2Values, self.totalStarts,self.totalStops)
        else:
            self.updateMeasurement.emit(self.g2Histogram, self.totalStarts,self.totalStops)
        if stopDifferences:
            self.estimatedParameter=self.getCountPerSecondParameter(stopDifferences)
            self.updateEstimatedParameter.emit(str(int(self.estimatedParameter)))
        if len(measurement)==0:
            self.updateStatusLabel.emit(f"No measurements in start channel")
            self.updateColorLabel.emit(3)
        elif notStartsMeasurement>70:
            self.updateStatusLabel.emit(f"No measurements in start channel")
            self.updateColorLabel.emit(3)
        elif totalStopPerMeasurement>70:
            self.updateStatusLabel.emit(f"No measurements in channels {self.stopChannel}")
            self.updateColorLabel.emit(3)
        else:
            self.updateStatusLabel.emit(f"Running measurement")
            self.updateColorLabel.emit(1)
            
        
            
    
    
    def processRun(self, run, timeDifferences, stopDifferences):
        self.totalStarts += 1
        if run[3] == -1:
            
            return 1
        self.totalStops += 1
        timeDifferences.append(run[3])
        self.totalTimeIntegration += run[3]

        if len(run) > 4 and run[4] != -1:
            stopDifferences.append(run[4] - run[3])
        return 0

 
    def getCountPerSecondParameter(self,estimatedDifferences):
        meanDifferences=np.mean(estimatedDifferences)
        estimatedValue= (10**(12))/meanDifferences
        return round(estimatedValue,0)

    
    def buildG2Histogram(self,timeDifferences):
        g2TemporalHistogram,_=np.histogram(timeDifferences, bins=self.bins)
        if len(self.g2Histogram)!=0:
            self.g2Histogram=self.g2Histogram+ g2TemporalHistogram
        else:
            self.g2Histogram=g2TemporalHistogram
        integrationTimeS=self.psToS(self.totalTimeIntegration)
        normalizedParameter=1/((self.estimatedParameter**2)*integrationTimeS*self.coincidenceWindow)
        histogramToEmit=self.g2Histogram*normalizedParameter
        return histogramToEmit
        
        
    def generateBinList(self):
        return np.linspace(0, self.maximumTime, self.numberBins + 1)
    
                    
    
    def sortByStart(self, measurement):
        dataFiltered=[]
        for run in measurement:
            if run:
                dataFiltered.append(run)
        dataFiltered.sort(key=lambda x: x[2])
        return dataFiltered
    
    def changeToOneStop(self):
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,1)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,1)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,1)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,1)
    
    def psToS(self,picoseconds):
        return picoseconds * 1e-12

    def clearG2(self):
        self.totalTimeIntegration=0
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.totalStarts=0
        self.totalStops=0
        
    
    def stop(self):
        self.updateDeterminedParameters.emit()
        self.running=False
            
    
        
        
    
    
        
    
    
    
    
    
    
        
        