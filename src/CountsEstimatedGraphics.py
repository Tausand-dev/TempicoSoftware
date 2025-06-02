from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox
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
class CountEstimatedLogic():
    def __init__(self,channelACheckBox: QCheckBox, channelBCheckBox: QCheckBox, channelCCheckBox: QCheckBox, channelDCheckBox: QCheckBox,startButton: QPushButton, stopButton: QPushButton,
                 mergeRadio: QRadioButton, separateGraphics: QRadioButton, timeRangeComboBox: QComboBox, clearButtonChannelA:QPushButton, clearButtonChannelB:QPushButton, clearButtonChannelC:QPushButton, 
                 clearButtonChannelD:QPushButton, saveDataButton: QPushButton, savePlotButton: QPushButton, countChannelAValue: QLabel,countChannelBValue: QLabel,countChannelCValue: QLabel,
                 countChannelDValue: QLabel, countChannelAUncertainty: QLabel, countChannelBUncertainty: QLabel, countChannelCUncertainty: QLabel, countChannelDUncertainty: QLabel,
                 tableCounts:QTableWidget, graphicsFrame: QFrame,channelAFrameLabel: QFrame,channelBFrameLabel: QFrame,channelCFrameLabel: QFrame,channelDFrameLabel: QFrame, device, parent):
        #Get the parameters
        self.channelACheckBox = channelACheckBox
        self.channelCCheckBox = channelBCheckBox
        self.channelBCheckBox = channelCCheckBox
        self.channelDCheckBox = channelDCheckBox
        self.startButton = startButton
        self.stopButton = stopButton
        self.mergeGraphics = mergeRadio
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
        self.channelAFrameLabel=channelAFrameLabel
        self.channelBFrameLabel=channelBFrameLabel
        self.channelCFrameLabel=channelCFrameLabel
        self.channelDFrameLabel=channelDFrameLabel
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
        #Connection for the radio button
        self.separateGraphics.toggled.connect(self.updateGraphicsLayout)
        self.mergeGraphics.toggled.connect(self.updateGraphicsLayout)
        #Activate sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
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
        #End connection for the checkbox
        
        
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
        


    #Function to update wich graphics are shown
    def updateGraphicsLayout(self):
        if self.separateGraphics.isChecked():
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
        else:
            
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
        self.updateGraphic()
    
    
    def connectedDevice(self,device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
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
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.resetValues()
        self.getChannelsMeasure()
        self.enableButtons()
        self.worker=WorkerThreadCountsEstimated(self.selectChannelA,self.selectChannelB,self.selectChannelC,self.selectChannelD, self.device)
        self.worker.finished.connect(self.finishedThread)
        self.worker.createdSignal.connect(self.getCreatedEvent)
        self.worker.newMeasurement.connect(self.captureMeasurement)
        self.worker.updateLabel.connect(self.updateLabels)
        self.worker.noTotalMeasurements.connect(self.noMeasurementsFounded)
        self.worker.noPartialMeasurements.connect(self.eliminateCheckBoxChannels)
        self.worker.start()
    
    def stopMeasure(self):
        self.resetSentinels()
        self.stopButton.setEnabled(False)
        self.worker.stop()
    
    def clearChannelA(self):
        self.timestampsChannelA=[]
        self.channelAValues=[]
    
    def clearChannelB(self):
        self.timestampsChannelB=[]
        self.channelBValues=[]
    
    def clearChannelC(self):
        self.timestampsChannelC=[]
        self.channelCValues=[]
    
    def clearChannelD(self):
        self.timestampsChannelD=[]
        self.channelDValues=[]
        
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
        if not self.channelACheckBox.isChecked():
            self.selectChannelA=False
            self.channelACheckBox.setEnabled(False)
        if not self.channelBCheckBox.isChecked():
            self.selectChannelB=False
            self.channelBCheckBox.setEnabled(False)
        if not self.channelCCheckBox.isChecked():
            self.selectChannelC=False
            self.channelCCheckBox.setEnabled(False)
        if not self.channelDCheckBox.isChecked():
            self.selectChannelD=False
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
        #Reset table rows
        self.tableCounts.setRowCount(0)

    
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
            
    
    #Hide and show column for channels measurement
    def hideColumns(self):
        #First show all columns
        self.tableCounts.showColumn(1);
        self.tableCounts.showColumn(2);
        self.tableCounts.showColumn(3);
        self.tableCounts.showColumn(4);
        #Hide columns according sentinels
        if not self.channelACheckBox.isChecked():
            self.tableCounts.hideColumn(1)
        if not self.channelBCheckBox.isChecked():
            self.tableCounts.hideColumn(2)
        if not self.channelCCheckBox.isChecked():
            self.tableCounts.hideColumn(3)
        if not self.channelDCheckBox.isChecked():
            self.tableCounts.hideColumn(4)
        
        
    
        
    
    def captureMeasurement(self,secondsTime,dateTime,channelAValue,channelAUncertainty,channelBValue,channelBUncertainty,channelCValue,channelCUncertainty,channelDValue,channelDUncertainty):
        
        #Add values in table
        #Channel A
        if channelAValue!=0 and channelAValue!=-1:
            channelAValue=round(channelAValue,2)
            channelAUncertainty= round(channelAUncertainty,5)
            self.timestampsChannelA.append(secondsTime)
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
        for col, value in enumerate(newData):
            self.tableCounts.setItem(0, col,QTableWidgetItem(str(value)))
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
    
    
    
    
    def finishedThread(self):
        #Restart the sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Start button enabled and stop button disabled
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.savePlotButton.setEnabled(True)
        self.saveDataButton.setEnabled(True)
        
        #actions for stop button
        self.stopMeasure()
    
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
                    self.channelACheckBox.setEnabled(False)
                    self.clearButtonChannelA.setEnabled(False)
                elif channelValue == "B":
                    self.device.ch2.disableChannel()
                    self.channelBCheckBox.setChecked(False)
                    self.channelBCheckBox.setEnabled(False)
                    self.clearButtonChannelB.setEnabled(False)
                elif channelValue == "C":
                    self.device.ch3.disableChannel()
                    self.channelCCheckBox.setChecked(False)
                    self.channelCCheckBox.setEnabled(False)
                    self.clearButtonChannelC.setEnabled(False)
                elif channelValue == "D":
                    self.device.ch4.disableChannel()
                    self.channelDCheckBox.setChecked(False)
                    self.channelDCheckBox.setEnabled(False)
                    self.clearButtonChannelD.setEnabled(False)

            # Continuar o parar según respuesta
            self.worker.continueEvent.set()

            if reply == QMessageBox.No:
                self.worker.stop()
        


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
            totalStops=self.determineStopsNumber(channel)
            if totalStops<2:
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
                if channel=="A":
                    self.numberStopsChannelA=totalStops
                elif channel=="B":
                    self.numberStopsChannelB=totalStops
                elif channel=="C":
                    self.numberStopsChannelC=totalStops
                elif channel=="D":
                    self.numberStopsChannelD=totalStops

        if len(self.channelsWithoutMeasurements)== len(self.channelsMeasure):
            self.noTotalMeasurements.emit()
            self.running=False
            print("No hay ninguna medicion en ningun canal")
        elif self.channelsWithoutMeasurements:
            self.noPartialMeasurements.emit(self.channelsWithoutMeasurements)
            self.continueEvent.wait()
            print("El hilo continua luego de que la pestana se cierra")
        self.enableDisableChannels()
        if self.running:
            #Get the init time for measurement
            self.initialMeasurementTime = time.time()
        while self.running:
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
        stopsInMeasure=5
        stopsFounded=False
        totalIterations=20
        #This number is arbitrary in order to determine how many measurements are necessary for determine the stop number
        while(stopsInMeasure>=2 and (not stopsFounded)):
            channel.setNumberOfStops(stopsInMeasure)
            totalMeasurements=0
            for i in range(totalIterations):
                measurements=self.device.measure()
                if measurements:
                    if measurements[0]:
                        if measurements[0][3] != -1:
                            totalMeasurements+=1
            if totalMeasurements>totalIterations/2:
                stopsFounded=True
            else:
                stopsInMeasure-=1
        
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
        if self.channelBSentinel:
            self.channelsMeasure.append("B")
            self.device.ch2.enableChannel()
            self.device.ch2.setStopMask(0)
        if self.channelCSentinel:
            self.channelsMeasure.append("C")
            self.device.ch3.enableChannel()
            self.device.ch3.setStopMask(0)
        if self.channelDSentinel:
            self.channelsMeasure.append("D")
            self.device.ch4.enableChannel()
            self.device.ch4.setStopMask(0)
        self.device.ch1.setMode(2)
        self.device.ch2.setMode(2)
        self.device.ch3.setMode(2)
        self.device.ch4.setMode(2)
        
    @Slot()   
    def stop(self):
        self.running=False
        