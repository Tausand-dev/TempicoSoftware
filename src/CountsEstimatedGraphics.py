from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QHeaderView,QAbstractItemView, QApplication
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
class CountEstimatedLogic():
    def __init__(self,channelACheckBox: QCheckBox, channelBCheckBox: QCheckBox, channelCCheckBox: QCheckBox, channelDCheckBox: QCheckBox,startButton: QPushButton, stopButton: QPushButton,
                 mergeRadio: QRadioButton, separateGraphics: QRadioButton, deatachedGraphics:QRadioButton, timeRangeComboBox: QComboBox, clearButtonChannelA:QPushButton, clearButtonChannelB:QPushButton, clearButtonChannelC:QPushButton, 
                 clearButtonChannelD:QPushButton, saveDataButton: QPushButton, savePlotButton: QPushButton, countChannelAValue: QLabel,countChannelBValue: QLabel,countChannelCValue: QLabel,
                 countChannelDValue: QLabel, countChannelAUncertainty: QLabel, countChannelBUncertainty: QLabel, countChannelCUncertainty: QLabel, countChannelDUncertainty: QLabel,
                 tableCounts:QTableWidget, graphicsFrame: QFrame,channelAFrameLabel: QFrame,channelBFrameLabel: QFrame,channelCFrameLabel: QFrame,channelDFrameLabel: QFrame, statusLabel: QLabel, pointStatusLabel: QLabel, deatachedCheckBox: QCheckBox, device, parent, timerConnection):
        #Get the parameters
        self.savefile=savefile()
        self.channelACheckBox = channelACheckBox
        self.channelCCheckBox = channelBCheckBox
        self.channelBCheckBox = channelCCheckBox
        self.channelDCheckBox = channelDCheckBox
        self.startButton = startButton
        self.stopButton = stopButton
        self.mergeGraphics = mergeRadio
        self.deatachedGraphics = deatachedGraphics
        self.separateGraphics = separateGraphics
        self.timeRangeComboBox = timeRangeComboBox
        self.clearButtonChannelA = clearButtonChannelA
        self.clearButtonChannelB = clearButtonChannelB
        self.clearButtonChannelC = clearButtonChannelC
        self.clearButtonChannelD = clearButtonChannelD
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.countChannelAValue = countChannelAValue
        self.countChannelBValue = countChannelBValue
        self.countChannelCValue = countChannelCValue
        self.countChannelDValue = countChannelDValue
        self.countChannelAUncertainty = countChannelAUncertainty
        self.countChannelBUncertainty = countChannelBUncertainty
        self.countChannelCUncertainty = countChannelCUncertainty
        self.countChannelDUncertainty = countChannelDUncertainty
        self.tableCounts = tableCounts
        self.graphicsFrame= graphicsFrame
        self.device = device
        self.mainWindow = parent
        self.timerConnection=timerConnection
        self.channelAFrameLabel=channelAFrameLabel
        self.channelBFrameLabel=channelBFrameLabel
        self.channelCFrameLabel=channelCFrameLabel
        self.channelDFrameLabel=channelDFrameLabel
        self.statusLabel=statusLabel
        self.pointStatusLabel=pointStatusLabel
        self.deatachedCheckBox= deatachedCheckBox
        #Init for the buttons
        self.stopButton.setEnabled(False)
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        #Construct the graphics
        self.constructGraphicA()
        self.constructGraphicB()
        self.constructGraphicC()
        self.constructGraphicD()
        #Connection for the checkbox
        self.channelACheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelBCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelCCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelDCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.deatachedCheckBox.stateChanged.connect(self.deatachedTable)
        #Connection for the radio button
        self.separateGraphics.toggled.connect(self.updateGraphicsLayout)
        self.mergeGraphics.toggled.connect(self.updateGraphicsLayout)
        #Activate sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Sentinels to know wich graphic was selected in measurement
        self.measurementChannelA=False
        self.measurementChannelB=False
        self.measurementChannelC=False
        self.measurementChannelD=False
        #Sentinel to know if the device was disconnected in measurement
        self.disconnectedMeasurement=False
        #Sentinel to detect that a measurement begin was created
        self.treadCreated=False
        #variables for dialogs
        self.dialogACreated=None
        self.dialogBCreated=None
        self.dialogCCreated=None
        self.dialogDCreated=None
        self.dialogTableOpen=None
        #Configure labels
        self.countChannelAValue.setText("Channel A: No running")
        self.countChannelBValue.setText("Channel B: No running")
        self.countChannelCValue.setText("Channel C: No running")
        self.countChannelDValue.setText("Channel D: No running")
        #Connection for the buttons
        self.startButton.clicked.connect(self.startMeasure)
        self.stopButton.clicked.connect(self.stopMeasure)
        self.clearButtonChannelA.clicked.connect(self.clearChannelA)
        self.clearButtonChannelB.clicked.connect(self.clearChannelB)
        self.clearButtonChannelC.clicked.connect(self.clearChannelC)
        self.clearButtonChannelD.clicked.connect(self.clearChannelD)
        self.savePlotButton.clicked.connect(self.savePlots)
        self.saveDataButton.clicked.connect(self.saveData)
        #Connection for the combo Box
        self.timeRangeComboBox.currentIndexChanged.connect(self.updateGraphic)
        #Creation data list for measurements
        #TODO: improve querys with deque, add uncertainties
        self.timestampsChannelA=[]
        self.timestampsChannelB=[]
        self.timestampsChannelC=[]
        self.timestampsChannelD=[]
        self.channelAValues=[]
        self.channelBValues=[]
        self.channelCValues=[]
        self.channelDValues=[]
        #Values for save data
        self.timestampsDateChannelA=[]
        self.timestampsDateChannelB=[]
        self.timestampsDateChannelC=[]
        self.timestampsDateChannelD=[]
        #End connection for the checkbox
        
        #Create the sentinels for connection
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        #Create Clone Table
        self.createCloneTable()
        
        
        
        if device==None:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.clearButtonChannelA.setEnabled(False)
            self.clearButtonChannelB.setEnabled(False)
            self.clearButtonChannelC.setEnabled(False)
            self.clearButtonChannelD.setEnabled(False)
            self.saveDataButton.setEnabled(False)
            self.savePlotButton.setEnabled(False)
            
        
    def verifyConnection(self):
        
        pass
    
    #Funcion to dinamically changes the interface
    def checkBoxListenerChannels(self):
        self.hideColumns()
        if self.channelACheckBox.isChecked():
            self.channelAFrameLabel.setVisible(True)
        else:
            self.channelAFrameLabel.setVisible(False)
        
        
        if self.channelBCheckBox.isChecked():
            self.channelBFrameLabel.setVisible(True)
        else:
            self.channelBFrameLabel.setVisible(False)

        
        if self.channelCCheckBox.isChecked():
            self.channelCFrameLabel.setVisible(True)
        else:
            self.channelCFrameLabel.setVisible(False)

        if self.channelDCheckBox.isChecked():
            self.channelDFrameLabel.setVisible(True)
        else:
            self.channelDFrameLabel.setVisible(False)
        #Here we update the graphics that are shown in the interface
        self.updateGraphicsLayout()
    
    def factoryGraphChannels(self, channel):
        colors = {
            "A": (0, 114, 189),    # azul
            "B": (217, 83, 25),    # rojo-naranja
            "C": (237, 177, 32),   # amarillo
            "D": (126, 47, 142),   # púrpura
        }

        color = colors.get(channel, "k")

        winCountsGraph = pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')

        plotCounts = winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        plotCounts.setLabel('left', f'Counts channel {channel}')
        plotCounts.setLabel('bottom', 'Time (s)')
        plotCounts.addLegend()

        pen = mkPen(color=color, width=2.5)

      
        curve = plotCounts.plot(
            pen=pen,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=color,
            name='Counts Estimated'
        )

        return winCountsGraph, plotCounts, curve

    def factoryGraphsAllChannels(self):
        colors = {
            "A": (0, 114, 189),    # azul
            "B": (217, 83, 25),    # rojo-naranja
            "C": (237, 177, 32),   # amarillo
            "D": (126, 47, 142),   # púrpura
        }

        colorA = colors.get("A", "k")
        colorB = colors.get("B", "k")
        colorC = colors.get("C", "k")
        colorD = colors.get("D", "k")

        winCountsGraph = pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')

        plotCounts = winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        plotCounts.setLabel('left', f'Counts channels')
        plotCounts.setLabel('bottom', 'Time (s)')
        plotCounts.addLegend()

        penA = mkPen(color=colorA, width=2.5)
        penB = mkPen(color=colorB, width=2.5)
        penC = mkPen(color=colorC, width=2.5)
        penD = mkPen(color=colorD, width=2.5)

      
        curveA = plotCounts.plot(
            pen=penA,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorA,
            name='Counts Estimated A'  if self.channelACheckBox.isChecked() else None
        )
        
        curveB = plotCounts.plot(
            pen=penB,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorB,
            name='Counts Estimated B' if self.channelBCheckBox.isChecked() else None
        )
        
        curveC = plotCounts.plot(
            pen=penC,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorC,
            name='Counts Estimated C' if self.channelCCheckBox.isChecked() else None
        )
        
        curveD = plotCounts.plot(
            pen=penD,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorD,
            name='Counts Estimated D' if self.channelDCheckBox.isChecked() else None
        )

        return winCountsGraph, plotCounts, curveA, curveB, curveC, curveD
    

    def constructGraphicA(self):
        self.winCountsGraphA, self.plotCountsA, self.curveCountsA = self.factoryGraphChannels('A')
        
    
    def constructGraphicB(self):
        self.winCountsGraphB, self.plotCountsB, self.curveCountsB = self.factoryGraphChannels('B')
        
    
    def constructGraphicC(self):
        self.winCountsGraphC, self.plotCountsC, self.curveCountsC = self.factoryGraphChannels('C')
        
    
    def constructGraphicD(self):
        self.winCountsGraphD, self.plotCountsD, self.curveCountsD = self.factoryGraphChannels('D')
    
    def constructAllGraphics(self):
        self.winCountsAllGraph, self.plotCountsAllC, self.cuveCountsAllA, self.cuveCountsAllB, self.cuveCountsAllC,self.cuveCountsAllD =self.factoryGraphsAllChannels()
        

    def createCloneTable(self):
        self.cloneTable=QTableWidget()
        self.cloneTable.setColumnCount(5)
        self.cloneTable.setHorizontalHeaderLabels(['Date','A','B','C','D'])
        self.cloneTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cloneTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        
        

    #Function to update wich graphics are shown
    def updateGraphicsLayout(self):
        if self.separateGraphics.isChecked():
            if self.dialogACreated:
                self.dialogACreated.close()
                self.dialogACreated=None
                self.channelACheckBox.setChecked(True)
            if self.dialogBCreated:
                self.dialogBCreated.close()
                self.dialogBCreated=None
                self.channelBCheckBox.setChecked(True)
            if self.dialogCCreated:
                self.dialogCCreated.close()
                self.dialogCCreated=None
                self.channelCCheckBox.setChecked(True)
            if self.dialogDCreated:
                self.dialogDCreated.close()
                self.dialogDCreated=None
                self.channelDCheckBox.setChecked(True)
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy

            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)

            selected_graphs = []

            for checkbox, label in zip(
                [self.channelACheckBox, self.channelBCheckBox, self.channelCCheckBox, self.channelDCheckBox],
                ["A", "B", "C", "D"]
            ):
                if checkbox.isChecked():
                    graph, plot, curve = self.factoryGraphChannels(label)
                    graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    selected_graphs.append(graph)

                    # Copiar los datos antiguos a las nuevas curvas
                    if label == "A":
                        curve.setData(self.timestampsChannelA, self.channelAValues)
                        self.curveCountsA = curve
                        self.winCountsGraphA = graph
                        self.plotCountsA = plot
                    elif label == "B":
                        curve.setData(self.timestampsChannelB, self.channelBValues)
                        self.curveCountsB = curve
                        self.winCountsGraphB = graph
                        self.plotCountsB = plot
                    elif label == "C":
                        curve.setData(self.timestampsChannelC, self.channelCValues)
                        self.curveCountsC = curve
                        self.winCountsGraphC = graph
                        self.plotCountsC = plot
                    elif label == "D":
                        curve.setData(self.timestampsChannelD, self.channelDValues)
                        self.curveCountsD = curve
                        self.winCountsGraphD = graph
                        self.plotCountsD = plot

            count = len(selected_graphs)
            if count == 0:
                return

            top_row = QHBoxLayout()
            bottom_row = QHBoxLayout()

            if count == 1:
                
                selected_graphs[0].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                top_row.addWidget(selected_graphs[0])
                layout.addLayout(top_row)

            elif count == 2:
                top_row.addWidget(selected_graphs[0])
                bottom_row.addWidget(selected_graphs[1])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
            elif count == 3:
                top_row.addWidget(selected_graphs[0])
                top_row.addWidget(selected_graphs[1])
                selected_graphs[2].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                bottom_row.addWidget(selected_graphs[2])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
            elif count == 4:
                top_row.addWidget(selected_graphs[0])
                top_row.addWidget(selected_graphs[1])
                bottom_row.addWidget(selected_graphs[2])
                bottom_row.addWidget(selected_graphs[3])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
        elif self.mergeGraphics.isChecked():
            if self.dialogACreated:
                self.dialogACreated.close()
                self.dialogACreated=None
                self.channelACheckBox.setChecked(True)
            if self.dialogBCreated:
                self.dialogBCreated.close()
                self.dialogBCreated=None
                self.channelBCheckBox.setChecked(True)
            if self.dialogCCreated:
                self.dialogCCreated.close()
                self.dialogCCreated=None
                self.channelCCheckBox.setChecked(True)
            if self.dialogDCreated:
                self.dialogDCreated.close()
                self.dialogDCreated=None
                self.channelDCheckBox.setChecked(True)
            
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy

            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)
            
            graph, plot, curveA, curveB, curveC,curveD = self.factoryGraphsAllChannels()
            graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            curveA.setData(self.timestampsChannelA, self.channelAValues)
            curveB.setData(self.timestampsChannelB, self.channelBValues)
            curveC.setData(self.timestampsChannelC, self.channelCValues)
            curveD.setData(self.timestampsChannelD, self.channelDValues)
            self.curveCountsA= curveA
            self.curveCountsB= curveB
            self.curveCountsC= curveC
            self.curveCountsD= curveD
            self.winCountsGraphA = graph
            self.winCountsGraphB = graph
            self.winCountsGraphC = graph
            self.winCountsGraphD = graph
            self.plotCountsA = plot
            self.plotCountsB = plot
            self.plotCountsC = plot
            self.plotCountsD = plot
            top_row = QHBoxLayout()
            if self.channelACheckBox.isChecked() or self.channelBCheckBox.isChecked() or self.channelCCheckBox.isChecked() or self.channelDCheckBox.isChecked():
                top_row.addWidget(graph)
                layout.addLayout(top_row)
            if not self.channelACheckBox.isChecked():
                self.curveCountsA.hide()
            if not self.channelBCheckBox.isChecked():
                self.curveCountsB.hide()
            if not self.channelCCheckBox.isChecked():
                self.curveCountsC.hide()
            if not self.channelDCheckBox.isChecked():
                self.curveCountsD.hide()
        elif self.deatachedGraphics.isChecked():  
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
            #Delete layout
            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)
            #Check the selected graphics
            if not self.dialogACreated and self.channelACheckBox.isChecked():
                self.dialogACreated= self.createDialogFactory("A")
                self.winCountsGraphA, self.plotCountsA, self.curveCountsA= self.factoryGraphChannels("A")
                layoutChannelA=QVBoxLayout(self.dialogACreated)
                layoutChannelA.addWidget(self.winCountsGraphA)
                self.curveCountsA.setData(self.timestampsChannelA, self.channelAValues)
                self.dialogACreated.show()
            elif self.dialogACreated and not self.channelACheckBox.isChecked():
                self.dialogACreated.close()
                self.dialogACreated=None
            if not self.dialogBCreated and self.channelBCheckBox.isChecked():
                self.dialogBCreated= self.createDialogFactory("B")
                self.winCountsGraphB, self.plotCountsB, self.curveCountsB= self.factoryGraphChannels("B")
                layoutChannelB=QVBoxLayout(self.dialogBCreated)
                layoutChannelB.addWidget(self.winCountsGraphB)
                self.curveCountsB.setData(self.timestampsChannelB, self.channelBValues)
                self.dialogBCreated.show()
            elif self.dialogBCreated and not self.channelBCheckBox.isChecked():
                self.dialogBCreated.close()
                self.dialogBCreated=None
            if not self.dialogCCreated and self.channelCCheckBox.isChecked():
                self.dialogCCreated= self.createDialogFactory("C")
                self.winCountsGraphC, self.plotCountsC, self.curveCountsC= self.factoryGraphChannels("C")
                layoutChannelC=QVBoxLayout(self.dialogCCreated)
                layoutChannelC.addWidget(self.winCountsGraphC)
                self.curveCountsC.setData(self.timestampsChannelC, self.channelCValues)
                self.dialogCCreated.show()
            elif self.dialogCCreated and not self.channelCCheckBox.isChecked():
                self.dialogCCreated.close()
                self.dialogCCreated=None
            if not self.dialogDCreated and self.channelDCheckBox.isChecked():
                self.dialogDCreated= self.createDialogFactory("D")
                self.winCountsGraphD, self.plotCountsD, self.curveCountsD= self.factoryGraphChannels("D")
                layoutChannelD=QVBoxLayout(self.dialogDCreated)
                layoutChannelD.addWidget(self.winCountsGraphD)
                self.curveCountsD.setData(self.timestampsChannelD, self.channelDValues)
                self.dialogDCreated.show()
            elif self.dialogDCreated and not self.channelDCheckBox.isChecked():
                self.dialogDCreated.close()
                self.dialogDCreated=None
                
        self.updateGraphic()
    
    
    def connectedDevice(self,device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.disconnectedMeasurement=False
        #TODO: SET THE TIMER OF MEASUREMENTS
        #self.timerStatus.start(500)
        self.device=device
        self.startButton.setEnabled(True)
    
    
    
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        #TODO: SET THE TIMER OF MEASUREMENTS
        #self.timerStatus.start(500)
        self.startButton.setEnabled(False)

    def startMeasure(self):
        if self.channelACheckBox.isChecked() or self.channelBCheckBox.isChecked() or self.channelCCheckBox.isChecked() or self.channelDCheckBox.isChecked():
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            #Disable save buttons
            self.saveDataButton.setEnabled(False)
            self.savePlotButton.setEnabled(False)
            #Disable other tabs while the software is taking measurements
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.saveSettings()
            self.stopTimerConnection()
            self.resetValues()
            self.getChannelsMeasure()
            self.enableButtons()
            self.changeStatusColor(1)
            self.mainWindow.activeMeasurement()
            self.worker=WorkerThreadCountsEstimated(self.selectChannelA,self.selectChannelB,self.selectChannelC,self.selectChannelD, self.device)
            self.worker.finished.connect(self.finishedThread)
            self.worker.createdSignal.connect(self.getCreatedEvent)
            self.worker.newMeasurement.connect(self.captureMeasurement)
            self.worker.updateLabel.connect(self.updateLabels)
            self.worker.noTotalMeasurements.connect(self.noMeasurementsFounded)
            self.worker.noPartialMeasurements.connect(self.eliminateCheckBoxChannels)
            self.worker.changeStatusText.connect(self.changeStatusLabel)
            self.worker.changeStatusColor.connect(self.changeStatusColor)
            self.worker.disconnectedDevice.connect(self.lostConnection)
            self.worker.start()
        else:
            self.noChannelsSelected()
    
    def stopMeasure(self):
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.resetSentinels()
        self.stopButton.setEnabled(False)
        self.worker.stop()
        
        if not self.disconnectedMeasurement:
            self.startTimerConnection()
            self.mainWindow.disconnectButton.setEnabled(True)        
        else:
            self.mainWindow.disconnectedDevice()
        self.mainWindow.noMeasurement()
        self.returnSettings()
        
        
    
    def stopTimerConnection(self):
        #Stop timer when a measurement begins
        self.timerConnection.stop()
    
    def startTimerConnection(self):
        #Start timer when a measurement begins
        self.timerConnection.start(500)
    
    def clearChannelA(self):
        self.timestampsChannelA=[]
        self.timestampsDateChannelA=[]
        self.channelAValues=[]
        self.curveCountsA.setData(self.timestampsChannelA,self.channelAValues)
    
    def clearChannelB(self):
        self.timestampsChannelB=[]
        self.timestampsDateChannelB=[]
        self.channelBValues=[]
        self.curveCountsB.setData(self.timestampsChannelB,self.channelBValues)
    
    def clearChannelC(self):
        self.timestampsChannelC=[]
        self.timestampsDateChannelC=[]
        self.channelCValues=[]
        self.curveCountsC.setData(self.timestampsChannelC,self.channelCValues)
    
    def clearChannelD(self):
        self.timestampsChannelD=[]
        self.timestampsDateChannelD=[]
        self.channelDValues=[]
        self.curveCountsD.setData(self.timestampsChannelD,self.channelDValues)
        
    #Functions to create all the dialogs for each graphic
    def createDialogFactory(self, channel):
        dialog = QDialog(self.mainWindow)
        dialog.setWindowTitle(f"Detached Graphics {channel}")
        dialog.resize(400, 300)
        dialog.setModal(False)
        dialog.finished.connect(lambda _: self.closeDialogChannels(channel))

        # Asignar posición para evitar superposición
        offsets = {
            "A": (100, 100),
            "B": (550, 100),
            "C": (100, 450),
            "D": (550, 450)
        }
        if channel in offsets:
            x, y = offsets[channel]
            dialog.move(x, y)

        return dialog
        
    def updateGraphic(self):
        if not self.timestampsChannelA:
            return
        # Apply seconds filter to the list
        try:
            segundosValue= int(self.timeRangeComboBox.currentText().split()[0])
        except ValueError:
            segundosValue = 10  # fallback
        x_max = self.timestampsChannelA[-1]
        x_min = x_max - segundosValue
        self.plotCountsA.setXRange(x_min, x_max, padding=0)
        self.plotCountsB.setXRange(x_min, x_max, padding=0)
        self.plotCountsC.setXRange(x_min, x_max, padding=0)
        self.plotCountsD.setXRange(x_min, x_max, padding=0)
        
    
    def getChannelsMeasure(self):
        self.selectChannelA=True
        self.selectChannelB=True
        self.selectChannelC=True
        self.selectChannelD=True
        self.measurementChannelA=True
        self.measurementChannelB=True
        self.measurementChannelC=True
        self.measurementChannelD=True
        if not self.channelACheckBox.isChecked():
            self.selectChannelA=False
            self.measurementChannelA=False
            self.channelACheckBox.setEnabled(False)
        if not self.channelBCheckBox.isChecked():
            self.selectChannelB=False
            self.measurementChannelB=False
            self.channelBCheckBox.setEnabled(False)
        if not self.channelCCheckBox.isChecked():
            self.selectChannelC=False
            self.measurementChannelC=False
            self.channelCCheckBox.setEnabled(False)
        if not self.channelDCheckBox.isChecked():
            self.selectChannelD=False
            self.measurementChannelD=False
            self.channelDCheckBox.setEnabled(False)
    
    def resetSentinels(self):
        #Reset selected sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Reset enable checkbox
        self.channelACheckBox.setEnabled(True)
        self.channelBCheckBox.setEnabled(True)
        self.channelCCheckBox.setEnabled(True)
        self.channelDCheckBox.setEnabled(True)
    
    def saveSettings(self):
        try:
            self.numberRunsSetting=self.device.getNumberOfRuns()
            #Number of stops
            self.numberStopsChannelASetting=self.device.ch1.getNumberOfStops()
            self.numberStopsChannelBSetting=self.device.ch2.getNumberOfStops()
            self.numberStopsChannelCSetting=self.device.ch3.getNumberOfStops()
            self.numberStopsChannelDSetting=self.device.ch4.getNumberOfStops()
            #Mode
            self.modeChannelASetting=self.device.ch1.getMode()
            self.modeChannelBSetting=self.device.ch2.getMode()
            self.modeChannelCSetting=self.device.ch3.getMode()
            self.modeChannelDSetting=self.device.ch4.getMode()
            #AverageCycles
            self.averageCyclesChannelASetting=self.device.ch1.getAverageCycles()
            self.averageCyclesChannelBSetting=self.device.ch2.getAverageCycles()
            self.averageCyclesChannelCSetting=self.device.ch3.getAverageCycles()
            self.averageCyclesChannelDSetting=self.device.ch4.getAverageCycles()
            #StopMask
            self.stopMaskChannelASetting=self.device.ch1.getStopMask()
            self.stopMaskChannelBSetting=self.device.ch2.getStopMask()
            self.stopMaskChannelCSetting=self.device.ch3.getStopMask()
            self.stopMaskChannelDSetting=self.device.ch4.getStopMask()
        except:
            pass
        
    
    
    
    def returnSettings(self):
        try:
            
            #Return number of runs
            self.device.setNumberOfRuns(self.numberRunsSetting)
            #Return average cycles
            self.device.ch1.setAverageCycles(self.averageCyclesChannelASetting)
            self.device.ch2.setAverageCycles(self.averageCyclesChannelBSetting)
            self.device.ch1.setAverageCycles(self.averageCyclesChannelCSetting)
            self.device.ch1.setAverageCycles(self.averageCyclesChannelDSetting)
            #Return number of stops
            self.device.ch1.setNumberOfStops(self.numberStopsChannelASetting)
            self.device.ch2.setNumberOfStops(self.numberStopsChannelBSetting)
            self.device.ch3.setNumberOfStops(self.numberStopsChannelCSetting)
            self.device.ch4.setNumberOfStops(self.numberStopsChannelDSetting)
            #Return mode
            self.device.ch1.setMode(self.modeChannelASetting)
            self.device.ch2.setMode(self.modeChannelBSetting)
            self.device.ch3.setMode(self.modeChannelCSetting)
            self.device.ch4.setMode(self.modeChannelDSetting)
            
            #Return stop mask
            self.device.ch1.setStopMask(self.stopMaskChannelASetting)
            self.device.ch2.setStopMask(self.stopMaskChannelBSetting)
            self.device.ch3.setStopMask(self.stopMaskChannelCSetting)
            self.device.ch4.setStopMask(self.stopMaskChannelDSetting)   
        except NameError as e:
            print(e)
        
    def resetValues(self):
        #Delete the values
        self.channelAValues=[]
        self.channelBValues=[]
        self.channelCValues=[]
        self.channelDValues=[]
        #Delete the timestamps
        self.timestampsChannelA=[]
        self.timestampsChannelB=[]
        self.timestampsChannelC=[]
        self.timestampsChannelD=[]
        #Delete date time stamps
        self.timestampsDateChannelA=[]
        self.timestampsDateChannelB=[]
        self.timestampsDateChannelC=[]
        self.timestampsDateChannelD=[]
        #Reset table rows
        self.tableCounts.setRowCount(0)
        self.cloneTable.setRowCount(0)
        #Reset graphics
        self.curveCountsA.setData(self.timestampsChannelA,self.channelAValues)
        self.curveCountsB.setData(self.timestampsChannelB,self.channelBValues)
        self.curveCountsC.setData(self.timestampsChannelC,self.channelCValues)
        self.curveCountsD.setData(self.timestampsChannelD,self.channelDValues)
        #Reset sentinels to save data
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        

    
    def enableButtons(self):
        if not self.selectChannelA:
            self.clearButtonChannelA.setEnabled(False)
        else:
            self.clearButtonChannelA.setEnabled(True)
        
        if not self.selectChannelB:
            self.clearButtonChannelB.setEnabled(False)
        else:
            self.clearButtonChannelB.setEnabled(True)
        
        if not self.selectChannelC:
            self.clearButtonChannelC.setEnabled(False)
        else:
            self.clearButtonChannelC.setEnabled(True)
        
        if not self.selectChannelD:
            self.clearButtonChannelD.setEnabled(False)
        else:
            self.clearButtonChannelD.setEnabled(True)
        self.mainWindow.disconnectButton.setEnabled(False)
            
    
    #Hide and show column for channels measurement
    def hideColumns(self):
        #First show all columns
        self.tableCounts.showColumn(1);
        self.tableCounts.showColumn(2);
        self.tableCounts.showColumn(3);
        self.tableCounts.showColumn(4);
        #Show all columns for clone table
        self.cloneTable.showColumn(1);
        self.cloneTable.showColumn(2);
        self.cloneTable.showColumn(3);
        self.cloneTable.showColumn(4);
        #Hide columns according sentinels
        if not self.channelACheckBox.isChecked():
            self.tableCounts.hideColumn(1)
            self.cloneTable.hideColumn(1)
        if not self.channelBCheckBox.isChecked():
            self.tableCounts.hideColumn(2)
            self.cloneTable.hideColumn(2)
        if not self.channelCCheckBox.isChecked():
            self.tableCounts.hideColumn(3)
            self.cloneTable.hideColumn(3)
        if not self.channelDCheckBox.isChecked():
            self.tableCounts.hideColumn(4)
            self.cloneTable.hideColumn(4)
        
        
    
        
    
    def captureMeasurement(self,secondsTime,dateTime,channelAValue,channelAUncertainty,channelBValue,channelBUncertainty,channelCValue,channelCUncertainty,channelDValue,channelDUncertainty):
        channelsWithoutMeasurements=[]
        #Manage status
        if channelAValue==0:
            channelsWithoutMeasurements.append("A")
        if channelBValue==0:
            channelsWithoutMeasurements.append("B")
        if channelCValue==0:
            channelsWithoutMeasurements.append("C")
        if channelDValue==0:
            channelsWithoutMeasurements.append("D")
        
        if len(channelsWithoutMeasurements)==0:
            self.changeStatusColor(1)
            self.changeStatusLabel("Running measurement")
        else:
            channelString=', '.join(channelsWithoutMeasurements)
            self.changeStatusColor(3)
            if len(channelsWithoutMeasurements)==1:
                self.changeStatusLabel(f"The channnel {channelString} is not taking measurements")
            else:
                self.changeStatusLabel(f"The channnels {channelString} are not taking measurements")
                
            
            
        #Add values in table
        #Channel A
        
        if channelAValue!=0 and channelAValue!=-1:
            channelAValue=round(channelAValue,2)
            channelAUncertainty= round(channelAUncertainty,5)
            self.timestampsChannelA.append(secondsTime)
            self.timestampsDateChannelA.append(dateTime)
            self.channelAValues.append(channelAValue)
            self.curveCountsA.setData(self.timestampsChannelA, self.channelAValues)
        elif channelAValue==0:
            channelAValue="Low Counts"
            channelAUncertainty="Low Counts"
        elif channelAValue == -1:
            channelAValue="Not Selected"
            channelAUncertainty="Not Selected"
        #Channel B
        if channelBValue!=0 and channelBValue!=-1:
            channelBValue=round(channelBValue,2)
            channelBUncertainty= round(channelBUncertainty,5)
            self.timestampsChannelB.append(secondsTime)
            self.timestampsDateChannelB.append(dateTime)
            self.channelBValues.append(channelBValue)
            self.curveCountsB.setData(self.timestampsChannelB, self.channelBValues)
        elif channelBValue==0:
            channelBValue="Low Counts"
            channelBUncertainty="Low Counts"
        elif channelBValue == -1:
            channelBValue="Not Selected"
            channelBUncertainty="Not Selected"
        #Channel C
        if channelCValue!=0 and channelCValue!=-1:
            channelCValue=round(channelCValue,2)
            channelCUncertainty= round(channelCUncertainty,5)
            self.timestampsChannelC.append(secondsTime)
            self.timestampsDateChannelC.append(dateTime)
            self.channelCValues.append(channelCValue)
            self.curveCountsC.setData(self.timestampsChannelC, self.channelCValues)
        elif channelCValue==0:
            channelCValue="Low Counts"
            channelCUncertainty="Low Counts"
        elif channelCValue == -1:
            channelCValue="Not Selected"
            channelCUncertainty="Not Selected"
        #Channel D
        if channelDValue!=0 and channelDValue!=-1:
            channelDValue=round(channelDValue,2)
            channelDUncertainty= round(channelDUncertainty,5)
            self.timestampsChannelD.append(secondsTime)
            self.timestampsDateChannelD.append(dateTime)
            self.channelDValues.append(channelDValue)
            self.curveCountsD.setData(self.timestampsChannelD, self.channelDValues)
        elif channelDValue==0:
            channelDValue="Low Counts"
            channelDUncertainty="Low Counts"
        elif channelDValue == -1:
            channelDValue="Not Selected"
            channelDUncertainty="Not Selected"
        
        
        newData=[dateTime,channelAValue,channelBValue,channelCValue,channelDValue]
        self.tableCounts.insertRow(0)
        self.cloneTable.insertRow(0)
        for col, value in enumerate(newData):
            self.tableCounts.setItem(0, col,QTableWidgetItem(str(value)))
            self.cloneTable.setItem(0, col,QTableWidgetItem(str(value)))
        #Update values to label
        if self.channelACheckBox.isChecked():
            self.updateLabels("A",channelAValue, channelAUncertainty)
        if self.channelBCheckBox.isChecked():
            self.updateLabels("B",channelBValue, channelBUncertainty)
        if self.channelCCheckBox.isChecked():
            self.updateLabels("C",channelCValue, channelCUncertainty)
        if self.channelDCheckBox.isChecked():
            self.updateLabels("D",channelDValue, channelDUncertainty)
        
        self.updateGraphic()
            
        
    
    def updateLabels(self, channel, value, uncertainty):
        if value=="Low Counts":
            finalValue=value
            finalUncertainty=uncertainty
        elif value=="Not Selected":
            finalValue=value
            finalUncertainty=uncertainty
        else:    
            finalValue=round(value,2)
            finalUncertainty=round(uncertainty,5)
        if channel=="A":    
            self.countChannelAValue.setText(f"Channel A: {finalValue}")
            self.countChannelAUncertainty.setText(f"Uncertainty A: {finalUncertainty}")
        elif channel=="B":
            self.countChannelBValue.setText(f"Channel B: {finalValue}")
            self.countChannelBUncertainty.setText(f"Uncertainty B: {finalUncertainty}")
        elif channel=="C":
            self.countChannelCValue.setText(f"Channel C: {finalValue}")
            self.countChannelCUncertainty.setText(f"Uncertainty C: {finalUncertainty}")
        elif channel=="D":
            self.countChannelDValue.setText(f"Channel D: {finalValue}")
            self.countChannelDUncertainty.setText(f"Uncertainty D: {finalUncertainty}")
    
    def updateTableWidget(self):
        pass
    
    def getCreatedEvent(self):
        print("Thread created")
    
    
    def closeDialogChannels(self, channel):
        if channel == "A":
            self.dialogACreated=None
            self.channelACheckBox.setChecked(False)
        elif channel == "B":
            self.dialogBCreated=None
            self.channelBCheckBox.setChecked(False)
        elif channel == "C":
            self.dialogCCreated=None
            self.channelCCheckBox.setChecked(False)
        elif channel == "D":
            self.dialogDCreated=None
            self.channelDCheckBox.setChecked(False)
    
    def finishedThread(self):
        #Restart the sentinels
        
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Start button enabled and stop button disabled
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        if self.timestampsChannelA or self.timestampsChannelB or self.timestampsChannelC or self.timestampsChannelD:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
        #Disable clear channels
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        self.changeStatusColor(0)
        self.changeStatusLabel("No running")
        
        
        #actions for stop button
        self.stopMeasure()
    
    #No selected channels function
    def noChannelsSelected(self):
        QMessageBox.warning(
            self.mainWindow,  
            "Not selected channels",
            "You must select at least one channel to start measurement"
        )
        
        
    
    #Function to define that no measurements were founded
    def noMeasurementsFounded(self):
        QMessageBox.warning(
            self.mainWindow,  
            "No Measurements Found",
            "Unable to obtain a measurement in any of the selected channels: At least 500 pulses per second are required to estimate the counts in each channel. That is, two consecutive stops are needed after a start within a 4 ms window"
        )
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        #Reset measurements
        self.measurementChannelA=False
        self.measurementChannelB=False
        self.measurementChannelC=False
        self.measurementChannelD=False
    
    #Function to eliminate channels where there is no measurements
    def eliminateCheckBoxChannels(self, channelList):
        newChannelList=[]
        for i in channelList:
            newValues="Channel "+i
            newChannelList.append(newValues)
        if newChannelList:
            channelStr = ", ".join(newChannelList)
            message = (
                "Unable to obtain a measurement: At least 500 pulses per second are required to estimate the counts in each channel. That is, two consecutive stops are needed after a start within a 4 ms window "
                f"in the following channels:\n\n{channelStr}\n\n"
                "Do you want to continue with the measurement?"
            )

            reply = QMessageBox.question(
                self.mainWindow,                  # Parent
                "Estimation Warning",             # Title
                message,                          # Message
                QMessageBox.Yes | QMessageBox.No, # Buttons
                QMessageBox.Yes                   # Default
            )

            for channelValue in channelList:
                if channelValue == "A":
                    self.device.ch1.disableChannel()
                    self.channelACheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelACheckBox.setEnabled(False)
                    self.measurementChannelA=False
                    self.clearButtonChannelA.setEnabled(False)
                elif channelValue == "B":
                    self.device.ch2.disableChannel()
                    self.channelBCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelBCheckBox.setEnabled(False)
                    self.measurementChannelB=False
                    self.clearButtonChannelB.setEnabled(False)
                elif channelValue == "C":
                    self.device.ch3.disableChannel()
                    self.channelCCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelCCheckBox.setEnabled(False)
                    self.measurementChannelC=False
                    self.clearButtonChannelC.setEnabled(False)
                elif channelValue == "D":
                    self.device.ch4.disableChannel()
                    self.channelDCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelDCheckBox.setEnabled(False)
                    self.measurementChannelD=False
                    self.clearButtonChannelD.setEnabled(False)

            # Continuar o parar según respuesta
            self.worker.continueEvent.set()

            if reply == QMessageBox.No:
                self.worker.stop()
    
    def deatachedTable(self):
        if self.deatachedCheckBox.isChecked():
            self.dialogTableOpen = QDialog(self.mainWindow)
            self.dialogTableOpen.setWindowTitle(f"Estimated counts Table")
            self.dialogTableOpen.resize(530, 400)
            self.dialogTableOpen.setModal(False)
            layoutDialogTable= QVBoxLayout(self.dialogTableOpen)
            layoutDialogTable.addWidget(self.cloneTable)
            self.dialogTableOpen.show()
            self.dialogTableOpen.finished.connect(lambda _: self.closeTableDialog())
        else:
            if self.dialogTableOpen:
                self.dialogTableOpen.close()
                self.dialogTableOpen=None
                
            
        
        
    def closeTableDialog(self):
        if self.deatachedCheckBox.isChecked():
            self.dialogTableOpen=None
            self.deatachedCheckBox.setChecked(False)
           

    def changeStatusLabel(self,textValue):
        self.statusLabel.setText(textValue)
    

    
        #Function to change the color of point measurement
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
        pixmap = QPixmap(self.pointStatusLabel.size())
        pixmap.fill(Qt.transparent)  
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        #Define the colors
        #Number 0 is for gray
        #Number 1 is for green
        #Number 2 is for yellow
        #Number 3 is for orange
        if color==0:
            painter.setBrush(QColor(128, 128, 128))  
        elif color==1:
            painter.setBrush(QColor(0, 255, 0))  
        elif color==2:
            painter.setBrush(QColor(255, 255, 0))  
        elif color==3:
            painter.setBrush(QColor(255, 165, 0))  
        painter.setPen(Qt.NoPen)
        point_size = min(self.pointStatusLabel.width(), self.pointStatusLabel.height()) // 2
        x = (self.pointStatusLabel.width() - point_size) // 2
        y = (self.pointStatusLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.pointStatusLabel.setPixmap(pixmap)




#Save plots
    def savePlots(self):
        """
        Saves the current plots in the selected image format.

        This method opens a dialog for the user to select an image format (PNG, TIFF, or JPG) 
        and saves the plots for channels A, B, C, and D if their respective flags are set to True. 
        The plots are saved with a timestamp in the specified format in the default folder path.

        :return: None
        """
        try:
            graph_names=[]
            #Open select the format
            dialog = QDialog(self.mainWindow)
    
            dialog.setObjectName("ImageFormat")
            dialog.resize(282, 105)
            dialog.setWindowTitle("Save plots")
            
            #pixmap = QIcon("./Sources/tausand_small.ico")
            
            #dialog.setWindowIcon()
            
            verticalLayout_2 = QVBoxLayout(dialog)
            verticalLayout_2.setObjectName("verticalLayout_2")
            
            VerticalImage = QVBoxLayout()
            VerticalImage.setObjectName("VerticalImage")
            
            graphicsToSaveLabel=QLabel("Only the current plots with the current view will be saved.")

            VerticalImage.addWidget(graphicsToSaveLabel)
            
            SelectLabel = QLabel(dialog)
            SelectLabel.setObjectName("SelectLabel")
            SelectLabel.setText("Select the image format:")
            VerticalImage.addWidget(SelectLabel)
            
            FormatBox = QComboBox(dialog)
            FormatBox.addItem("png")
            FormatBox.addItem("tiff")
            FormatBox.addItem("jpg")
            FormatBox.setObjectName("FormatBox")
            VerticalImage.addWidget(FormatBox)
           

            
            
            verticalLayout_2.addLayout(VerticalImage)
            
            accepButton = QPushButton(dialog)
            accepButton.setObjectName("accepButton")
            accepButton.setText("Accept")
            verticalLayout_2.addWidget(accepButton)
            
            QMetaObject.connectSlotsByName(dialog)
            
            # Conectar el botón "Accept" al método accept del diálogo
            accepButton.clicked.connect(dialog.accept)
            
            # Mostrar el diálogo y esperar a que se cierre
            if dialog.exec_() == QDialog.Accepted:
                selected_format = FormatBox.currentText()
                
                if self.channelACheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    self.plotCountsA.setAspectLocked(False)
                    exporter= pg.exporters.ImageExporter(self.winCountsGraphA.scene())
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Counts_ChannelA'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.channelBCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    exporter= pg.exporters.ImageExporter(self.plotCountsB)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Counts_ChannelB'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.channelCCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    exporter= pg.exporters.ImageExporter(self.plotCountsC)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Counts_ChannelC'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.channelDCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    self.separateGraphics.setChecked(True)
                    exporter= pg.exporters.ImageExporter(self.plotCountsD)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Counts_ChannelD'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.mergeGraphics.isChecked():
                    exporter= pg.exporters.ImageExporter(self.plotCountsA)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Counts_MergeChannels'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Information)
                initial_text="The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+ "with the following names:"
                text_route=""
                index=1
                for i in graph_names:
                    text_route+="\n"+"File"+str(index)+": "+i+"."+selected_format
                    index+=1
                message_box.setText(initial_text+text_route)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                # show successful save
                message_box.exec_()
                
            
        except NameError as e:
            print(e)
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The graphics could not be saved, check the folder path or system files")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
    
    
    def saveData(self):
        """
        Saves the current data according to the selected format specified in the dialog box.

        The function starts by retrieving the default histogram name and the current 
        date, which is formatted to create a unique filename. It then initializes lists 
        to hold filenames, data, settings, and column names for the saved files.

        A dialog box is displayed for the user to select the desired file format 
        (txt, csv, or dat) for saving the data. Once the user accepts the selection, 
        the function checks if the selected format has already been saved before.

        If the selected format has not been saved, it collects data from the various 
        channels (A, B, C, D) if their corresponding sentinel variables indicate 
        they should be saved. It retrieves the average cycles, mode, number of stops, 
        stop edge, and stop mask for each channel to include in the settings. The 
        function then attempts to save the collected data in the specified format.

        If the save operation is successful, a message box is displayed, confirming 
        the successful save and showing the folder path and file names. If an error 
        occurs during the save process, an error message box is shown.

        If the selected format has already been saved, a message box is displayed 
        with the previous save information.

        :return: None
        """
        
        data_prefix="CountsEstimated"
        current_date=datetime.now()
        current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        #Init filenames and data list
        filenames=[]
        data=[]
        timeStamps=[]
        settings=[]
        channels=[]
        
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
            conditiontxt= FormatBox.currentText()=="txt" and self.sentinelsavetxt==1
            conditioncsv= FormatBox.currentText()=="csv" and self.sentinelsavecsv==1
            conditiondat= FormatBox.currentText()=="dat" and self.sentinelsavedat==1   
            total_condition= conditiontxt or conditioncsv or conditiondat
            if not total_condition:
                if self.measurementChannelA:
                    filename1=data_prefix+current_date_str+'channelA'
                    setting_A=""
                    settings.append(setting_A)
                    filenames.append(filename1)
                    timeStamps.append(self.timestampsDateChannelA)
                    channels.append("A")
                    data.append(self.channelAValues)
                if self.measurementChannelB:
                    filename2=data_prefix+current_date_str+'channelB'
                    setting_B=""
                    settings.append(setting_B)
                    filenames.append(filename2)
                    timeStamps.append(self.timestampsDateChannelB)
                    channels.append("B")
                    data.append(self.channelBValues)
                if self.measurementChannelC:
                    filename3=data_prefix+current_date_str+'channelC'
                    setting_C=""
                    settings.append(setting_C)
                    filenames.append(filename3)
                    timeStamps.append(self.timestampsDateChannelC)
                    channels.append("C")
                    data.append(self.channelCValues)
                if self.measurementChannelD:
                    filename4=data_prefix+current_date_str+'channelD'
                    setting_D=""
                    settings.append(setting_D)
                    filenames.append(filename4)
                    timeStamps.append(self.timestampsDateChannelD)
                    channels.append("D")
                    data.append(self.channelDValues)
                folder_path=self.savefile.read_default_data()['Folder path']
                
                try:
                    
                    self.savefile.save_counts_data(timeStamps,data,filenames,folder_path,settings,selected_format,channels)
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Information)
                    inital_text="The files have been saved successfully in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following names:"
                    index=1
                    for i in filenames:
                        filenumber="File" + str(index)+": "
                        text_route+="\n\n"+filenumber+i+"."+str(selected_format)
                        index+=1
                    message_box.setText(inital_text+text_route)
                    if selected_format=="txt":
                        self.oldroutetxt="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavetxt=1
                    elif selected_format=="csv":
                        self.oldroutecsv="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavecsv=1
                    elif selected_format=="dat":
                        self.oldroutedat="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavedat=1
                    message_box.setWindowTitle("Successful save")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    self.savebutton.setEnabled(True)
                except NameError as e:
                    #If an error occurs, an error message box will be displayed.
                    print(e)
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                
            else:
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Information)
                if conditiontxt:
                    message_box.setText(self.oldroutetxt)
                elif conditioncsv:
                    message_box.setText(self.oldroutecsv)
                elif conditiondat:
                    message_box.setText(self.oldroutedat)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    
    def lostConnection(self):
        self.disconnectedMeasurement=True
        msg_box = QMessageBox(self.mainWindow)
        msg_box.setText("Connection with the device has been lost")
        msg_box.setWindowTitle("Connection Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        
    
    
    
    
    

class WorkerThreadCountsEstimated(QThread):
    #One value is for the count estimated and the other is for the uncertainty
    createdSignal=Signal()
    newValue=Signal(str,float,float)
    updateLabel= Signal(str,float,float)
    #Represents date, channelAValue, channelAUncertainty, channelBValue, channelBUncertainty,channelCValue, channelCUncertainty,channelDValue, channelDUncertainty
    newMeasurement=Signal(float,datetime,float,float,float,float,float,float,float,float)
    #Signals to manage the total stops values
    noTotalMeasurements=Signal()
    noPartialMeasurements=Signal(list)
    changeStatusText=Signal(str)
    changeStatusColor=Signal(int)
    disconnectedDevice=Signal()
    
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel,channelDSentinel, device: tempico.TempicoDevice):
        super().__init__()
        #Set the values for the  thread
        self.channelASentinel= channelASentinel
        self.channelBSentinel= channelBSentinel
        self.channelCSentinel= channelCSentinel
        self.channelDSentinel= channelDSentinel
        self.device= device
        self.channelsMeasure=[]
        self.channelsWithoutMeasurements=[]
        #Set the settings for the device
        #for the moment the stops number will be set to 5
        self.enableDisableChannels()
        self.device.setNumberOfRuns(25)
        self.continueEvent=threading.Event()
        self.running=True
        self.numberStopsChannelA=0
        self.numberStopsChannelB=0
        self.numberStopsChannelC=0
        self.numberStopsChannelD=0
        
        
        
    
    #Main function
    def run(self):
        # self.createdSignal.emit()
        # for i in range(10):
        #     self.getMeasurements()
        #     time.sleep(1)
        
        
        #Test determine stops measurement
        for channel in self.channelsMeasure:
            self.changeStatusText.emit(f"Estimating number stops in channel {channel} 0%")
            self.changeStatusColor.emit(3)
            try:
                totalStops=self.determineStopsNumber(channel)
                if totalStops<2 and self.running:
                    if channel=="A":
                        self.channelASentinel=False
                    elif channel == "B":
                        self.channelBSentinel=False
                    elif channel == "C":
                        self.channelCSentinel=False
                    elif channel == "D":
                        self.channelDSentinel=False
                    self.channelsWithoutMeasurements.append(channel)
                else:
                    if self.running:
                        if channel=="A":
                            self.numberStopsChannelA=totalStops
                        elif channel=="B":
                            self.numberStopsChannelB=totalStops
                        elif channel=="C":
                            self.numberStopsChannelC=totalStops
                        elif channel=="D":
                            self.numberStopsChannelD=totalStops
            except:
                self.running=False
                

        if len(self.channelsWithoutMeasurements)== len(self.channelsMeasure) and self.running:
            self.noTotalMeasurements.emit()
            self.running=False
            print("No hay ninguna medicion en ningun canal")
        elif self.channelsWithoutMeasurements and self.running:
            self.noPartialMeasurements.emit(self.channelsWithoutMeasurements)
            self.continueEvent.wait()
            print("El hilo continua luego de que la pestana se cierra")
        if self.running:
            self.enableDisableChannels()
        if self.running:
            #Get the init time for measurement
            self.initialMeasurementTime = time.time()
        while self.running:
            try:
                self.device.readIdnFromDevice()
            except:
                self.running=False
                self.disconnectedDevice.emit()
            if self.running:
                print("Se ejecuta medicion")
                self.getMeasurements()
                time.sleep(1)
            
            
        
    def getMeasurements(self):
        values=[]
        valuesB=[]
        valuesC=[]
        valuesD=[]
        measure=self.device.measure()
        
        print(measure)
        if measure:
            if len(measure)!=0:
                for run in measure:
                    if self.channelASentinel:
                        if run:
                            if run[0]==1 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelA)
                               
                                values=values+intervalValues
                    if self.channelBSentinel:
                        if run:
                            if run[0]==2 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run,self.numberStopsChannelB)
                                valuesB=valuesB+intervalValues
                    
                    if self.channelCSentinel:
                        if run:
                            if run[0]==3 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelC)
                                valuesC=valuesC+intervalValues
                    
                    if self.channelDSentinel:
                        if run:
                            if run[0]==4 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelC)
                                valuesD=valuesD+intervalValues
        if len(values)>0:
            meanValue=mean(values)
            uncertaintyValue=std(values)
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelASentinel:
                valueChannelA=meanValue
                uncertaintyChannelA=uncertaintyValue
            else:
                valueChannelA=-1
                uncertaintyChannelA=-1
        else:
            if self.channelASentinel:
                valueChannelA=0
                uncertaintyChannelA=0
            else:
                valueChannelA=-1
                uncertaintyChannelA=-1
                
            
        
        
        if len(valuesB)>0:
            meanValueB=mean(valuesB)
            uncertaintyValueB=std(valuesB)
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelBSentinel:
                valueChannelB=meanValueB
                uncertaintyChannelB=uncertaintyValueB
            else:
                valueChannelB=-1
                uncertaintyChannelB=-1
        else:
            if self.channelBSentinel:
                valueChannelB=0
                uncertaintyChannelB=0
            else:
                valueChannelB=-1
                uncertaintyChannelB=-1

        if len(valuesC)>0:
            meanValueC=mean(valuesC)
            uncertaintyValueC=std(valuesC)
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelCSentinel:
                valueChannelC=meanValueC
                uncertaintyChannelC=uncertaintyValueC
            else:
                valueChannelC=-1
                uncertaintyChannelC=-1
        else:
            if self.channelCSentinel:
                valueChannelC=0
                uncertaintyChannelC=0
            else:
                valueChannelC=-1
                uncertaintyChannelC=-1
        
        if len(valuesD)>0:
            meanValueD=mean(valuesD)
            uncertaintyValueD=std(valuesD)
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelDSentinel:
                valueChannelD=meanValueD
                uncertaintyChannelD=uncertaintyValueD
            else:
                valueChannelD=-1
                uncertaintyChannelD=-1
        else:
            if self.channelDSentinel:
                valueChannelD=0
                uncertaintyChannelD=0
            else:
                valueChannelD=-1
                uncertaintyChannelD=-1 
            
        currentTime = time.time()-self.initialMeasurementTime
        currentDate= datetime.now().strftime("%H:%M:%S")
        self.newMeasurement.emit(currentTime,currentDate, valueChannelA, uncertaintyChannelA, valueChannelB, uncertaintyChannelB, valueChannelC, uncertaintyChannelC, valueChannelD, uncertaintyChannelD)


    def calculateIntervalWithStops(self, currentMeasure, numberStops):
        #TODO: CHANGE RECALCULATING NUMBER OF STOPS
        tempValues=[]
        for i in range(numberStops-1):
            if currentMeasure[i+3]!=-1 and currentMeasure[i+4]!=-1:
                differenceValue=currentMeasure[i+4]-currentMeasure[i+3]
                realValueSeconds=(10**12)/(differenceValue)
                tempValues.append(realValueSeconds)
        
        return tempValues
    
    
    #TODO: DETERMINE THE NUMBER OF STOPS TO PERFORM THE MEASUREMENTS
    def determineStopsNumber(self, channelTest):
        #Disable all channels
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        ##-------------------
        ##Enable only the tested channel
        if channelTest == "A":
            self.device.ch1.enableChannel()
            channel=self.device.ch1
        elif channelTest == "B":
            self.device.ch2.enableChannel()
            channel=self.device.ch2
        elif channelTest == "C":
            self.device.ch3.enableChannel()
            channel=self.device.ch3
        elif channelTest == "D":
            self.device.ch4.enableChannel()
            channel=self.device.ch4
        ##--------------------
            
        #Pre settings for determine stop number
        self.device.setNumberOfRuns(1)
        channel.setMode(2)
        ##-------------
        valuePercent=round(100/80,2)
        stopsInMeasure=5
        stopsFounded=False
        totalIterations=20
        #This number is arbitrary in order to determine how many measurements are necessary for determine the stop number
        while(stopsInMeasure>=2 and (not stopsFounded) and self.running):
            
            channel.setNumberOfStops(stopsInMeasure)
            totalMeasurements=0
            for i in range(totalIterations):
                try:
                    self.device.readIdnFromDevice()
                except:
                    self.running=False
                    self.disconnectedDevice.emit()
                if not self.running:
                    break
                self.changeStatusText.emit(f"Estimating number stops in channel {channelTest} {valuePercent}%")
                valuePercent+=100/80
                valuePercent=round(valuePercent,2)    
                measurements=self.device.measure()
                if measurements:
                    if measurements[0]:
                        if measurements[0][3] != -1:
                            totalMeasurements+=1
            if totalMeasurements>totalIterations/2:
                stopsFounded=True
            else:
                stopsInMeasure-=1
        if self.running:
            self.changeStatusText.emit(f"Estimating number stops in channel {channelTest} 100%")
            time.sleep(2)
        
        return stopsInMeasure
        
    
    def enableDisableChannels(self):
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.channelASentinel:
            self.channelsMeasure.append("A")
            self.device.ch1.enableChannel()
            self.device.ch1.setStopMask(0)
            self.device.ch1.setAverageCycles(1)
        if self.channelBSentinel:
            self.channelsMeasure.append("B")
            self.device.ch2.enableChannel()
            self.device.ch2.setStopMask(0)
            self.device.ch2.setAverageCycles(1)            
        if self.channelCSentinel:
            self.channelsMeasure.append("C")
            self.device.ch3.enableChannel()
            self.device.ch3.setStopMask(0)
            self.device.ch3.setAverageCycles(1)
        if self.channelDSentinel:
            self.channelsMeasure.append("D")
            self.device.ch4.enableChannel()
            self.device.ch4.setStopMask(0)
            self.device.ch4.setAverageCycles(1)
        self.device.ch1.setMode(2)
        self.device.ch2.setMode(2)
        self.device.ch3.setMode(2)
        self.device.ch4.setMode(2)
        
    @Slot()   
    def stop(self):
        self.running=False
        