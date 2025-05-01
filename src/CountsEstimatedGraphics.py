from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace
from numpy import append as appnd
from createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
import time
class CountEstimatedLogic():
    def __init__(self,channelACheckBox: QCheckBox, channelBCheckBox: QCheckBox, channelCCheckBox: QCheckBox, channelDCheckBox: QCheckBox,startButton: QPushButton, stopButton: QPushButton,
                 mergeRadio: QRadioButton, separateGraphics: QRadioButton, timeRangeComboBox: QComboBox, clearButtonChannelA:QPushButton, clearButtonChannelB:QPushButton, clearButtonChannelC:QPushButton, 
                 clearButtonChannelD:QPushButton, saveDataButton: QPushButton, savePlotButton: QPushButton, countChannelAValue: QLabel,countChannelBValue: QLabel,countChannelCValue: QLabel,
                 countChannelDValue: QLabel, countChannelAUncertainty: QLabel, countChannelBUncertainty: QLabel, countChannelCUncertainty: QLabel, countChannelDUncertainty: QLabel,
                 tableCounts:QTableWidget, graphicsFrame: QFrame,channelAFrameLabel: QFrame,channelBFrameLabel: QFrame,channelCFrameLabel: QFrame,channelDFrameLabel: QFrame, device, parent):
        #Get the parameters
        self.channelACheckBox = channelACheckBox
        self.channelBCheckBox = channelBCheckBox
        self.channelCCheckBox = channelCCheckBox
        self.channelDCheckBox = channelDCheckBox
        self.startButton = startButton
        self.stopButton = stopButton
        self.mergeRadio = mergeRadio
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
        winCountsGraph=pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')
        #Add the plot to the window
        plotCounts=winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        #Add Labels
        plotCounts.setLabel('left',f'Counts channel {channel}')
        plotCounts.setLabel('bottom','Time')
        plotCounts.addLegend()
        curve = plotCounts.plot(pen='b',  name='Counts Estimated')
        return winCountsGraph, plotCounts, curve
        
    def constructGraphicA(self):
        self.winCountsGraphA, self.plotCountsA, self.curveCountsA = self.factoryGraphChannels('A')
        
    
    def constructGraphicB(self):
        self.winCountsGraphB, self.plotCountsB, self.curveCountsB = self.factoryGraphChannels('B')
        
    
    def constructGraphicC(self):
        self.winCountsGraphC, self.plotCountsC, self.curveCountsC = self.factoryGraphChannels('C')
        
    
    def constructGraphicD(self):
        self.winCountsGraphD, self.plotCountsD, self.curveCountsD = self.factoryGraphChannels('D')
        


    #Function to update wich graphics are shown
    def updateGraphicsLayout(self):
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
        for channel, label in zip(
            [self.channelACheckBox, self.channelBCheckBox, self.channelCCheckBox, self.channelDCheckBox],
            ["A", "B", "C", "D"]
        ):
            if channel.isChecked():
                graph, _, _ = self.factoryGraphChannels(label)
                graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                selected_graphs.append(graph)

        count = len(selected_graphs)

        if count == 0:
            return  # No ocultamos el frame, solo no añadimos nada

        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        if count == 1:
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
        self.getChannelsMeasure()
        self.worker=WorkerThreadCountsEstimated(self.selectChannelA,self.selectChannelB,self.selectChannelC,self.selectChannelD, self.device)
        self.worker.finished.connect(self.finishedThread)
        self.worker.createdSignal.connect(self.getCreatedEvent)
        self.worker.updateLabel.connect(self.updateLabels)
        self.worker.start()
    
    def getChannelsMeasure(self):
        if self.channelACheckBox.isChecked():
            self.selectChannelA=True
        if self.channelBCheckBox.isChecked():
            self.selectChannelB=True
        if self.channelCCheckBox.isChecked():
            self.selectChannelC=True
        if self.channelDCheckBox.isChecked():
            self.selectChannelD=True
    
        
    
    def captureMeasurement(self):
        
        pass
    
    def updateLabels(self, channel, value, uncertainty):
        if channel=="A":
            self.countChannelAValue.setText(f"Channel A: {value}")
            self.countChannelAUncertainty.setText(f"Uncertainty A: {uncertainty}")
        elif channel=="B":
            self.countChannelBValue.setText(f"Channel B: {value}")
            self.countChannelBUncertainty.setText(f"Uncertainty B: {uncertainty}")
        elif channel=="C":
            self.countChannelCValue.setText(f"Channel C: {value}")
            self.countChannelCUncertainty.setText(f"Uncertainty C: {uncertainty}")
        elif channel=="D":
            self.countChannelDValue.setText(f"Channel D: {value}")
            self.countChannelDUncertainty.setText(f"Uncertainty D: {uncertainty}")
    
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
    


class WorkerThreadCountsEstimated(QThread):
    #One value is for the count estimated and the other is for the uncertainty
    createdSignal=Signal()
    newValue=Signal(str,float,float)
    updateLabel= Signal(str,float,float)
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel,channelDSentinel, device):
        super().__init__()
        #Set the values for the  thread
        self.channelASentinel= channelASentinel
        self.channelBSentinel= channelBSentinel
        self.channelCSentinel= channelCSentinel
        self.channelDSentinel= channelDSentinel
        self.device= device
        #Set the settings for the device
        #for the moment the stops number will be set to 5
        self.enableDisableChannels()
        self.device.setNumberOfRuns(25)
        
    
    #Main function
    def run(self):
        self.createdSignal.emit()
        for i in range(10):
            self.getMeasurements()
            time.sleep(1)
            
        
    def getMeasurements(self):
        values=[]
        measure=self.device.measure()
        if measure:
            if len(measure)!=0:
                for run in measure:
                    if self.channelASentinel:
                        if run:
                            if run[0]==1 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run)
                                values=values+intervalValues
        if len(values)>0:
            meanValue=mean(values)
            uncertaintyValue=0
            #Send the signal to the main window
            if self.channelASentinel:
                self.updateLabel.emit("A",meanValue,uncertaintyValue)
            if self.channelBSentinel:
                self.updateLabel.emit("B",meanValue,uncertaintyValue)
            if self.channelCSentinel:
                self.updateLabel.emit("C",meanValue,uncertaintyValue)
            if self.channelDSentinel:
                self.updateLabel.emit("D",meanValue,uncertaintyValue)

    
    def calculateIntervalWithStops(self, currentMeasure):
        #TODO: CHANGE RECALCULATING NUMBER OF STOPS
        tempValues=[]
   
        for i in range(4):
            if currentMeasure[i+3]!=-1 and currentMeasure[i+4]!=-1:
                differenceValue=currentMeasure[i+4]-currentMeasure[i+3]
                realValueSeconds=(10**12)/(differenceValue)
                tempValues.append(realValueSeconds)
        
        return tempValues
    
    #TODO: DETERMINE THE NUMBER OF STOPS TO PERFORM THE MEASUREMENTS
    def determineStopsNumber(self):
        pass
    
    def enableDisableChannels(self):
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.channelASentinel:
            self.device.ch1.enableChannel()
            self.device.ch1.setNumberOfStops(5)
            self.device.ch1.setStopMask(0)
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
            self.device.ch2.setNumberOfStops(5)
            self.device.ch2.setStopMask(0)
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
            self.device.ch3.setNumberOfStops(5)
            self.device.ch3.setStopMask(0)
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
            self.device.ch4.setNumberOfStops(5)
            self.device.ch4.setStopMask(0)
        self.device.ch1.setMode(2)
        self.device.ch2.setMode(2)
        self.device.ch3.setMode(2)
        self.device.ch4.setMode(2)
        