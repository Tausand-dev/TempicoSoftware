from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget, QTableWidgetItem
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
        self.stopButton.clicked.connect(self.stopMeasure)
        self.clearButtonChannelA.clicked.connect(self.clearChannelA)
        self.clearButtonChannelB.clicked.connect(self.clearChannelB)
        self.clearButtonChannelC.clicked.connect(self.clearChannelC)
        self.clearButtonChannelD.clicked.connect(self.clearChannelD)
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
            top_row.addStretch()
            top_row.addWidget(selected_graphs[0])
            top_row.addStretch()
            layout.addLayout(top_row)
        elif count == 2:
            top_row.addWidget(selected_graphs[0])
            bottom_row.addWidget(selected_graphs[1])
            layout.addLayout(top_row)
            layout.addLayout(bottom_row)
        elif count == 3:
            top_row.addWidget(selected_graphs[0])
            top_row.addWidget(selected_graphs[1])
            bottom_row.addStretch()
            bottom_row.addWidget(selected_graphs[2])
            bottom_row.addStretch()
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
        self.worker.newMeasurement.connect(self.captureMeasurement)
        self.worker.updateLabel.connect(self.updateLabels)
        self.worker.start()
    
    def stopMeasure(self):
        self.resetSentinels()
    
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
        
        
    
        
    
    def captureMeasurement(self,dateTime,channelAValue,channelAUncertainty,channelBValue,channelBUncertainty,channelCValue,channelCUncertainty,channelDValue,channelDUncertainty):
        
        #Add values in table
        channelAValue=round(channelAValue,2)
        channelAUncertainty= round(channelAUncertainty,5)
        channelBValue=round(channelBValue,2)
        channelBUncertainty= round(channelBUncertainty,5)
        channelCValue=round(channelCValue,2)
        channelCUncertainty= round(channelCUncertainty,5)
        channelDValue=round(channelDValue,2)
        channelDUncertainty= round(channelDUncertainty,5)
        newData=[dateTime,channelAValue,channelBValue,channelCValue,channelDValue]
        posRow=self.tableCounts.rowCount()
        self.tableCounts.insertRow(posRow)
        for col, value in enumerate(newData):
            self.tableCounts.setItem(posRow, col,QTableWidgetItem(str(value)))
        #Update values to label
        if self.channelACheckBox.isChecked():
            self.updateLabels("A",channelAValue, channelAUncertainty)
        if self.channelBCheckBox.isChecked():
            self.updateLabels("B",channelBValue, channelBUncertainty)
        if self.channelCCheckBox.isChecked():
            self.updateLabels("C",channelCValue, channelCUncertainty)
        if self.channelDCheckBox.isChecked():
            self.updateLabels("D",channelDValue, channelDUncertainty)
        #Update graphics value 
        today_str = date.today().strftime("%Y-%m-%d")
        full_str = f"{today_str} {dateTime}"  
        dateObject = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
        timeStampNumeric = dateObject.timestamp()
        self.timestampsChannelA.append(timeStampNumeric)
        self.timestampsChannelB.append(timeStampNumeric)
        self.timestampsChannelC.append(timeStampNumeric)
        self.timestampsChannelD.append(timeStampNumeric)
        self.channelAValues.append(channelAValue)
        self.channelBValues.append(channelBValue)
        self.channelCValues.append(channelCValue)
        self.channelDValues.append(channelDValue)
        self.curveCountsA.setData(self.timestampsChannelA, self.channelAValues)
        self.curveCountsB.setData(self.timestampsChannelB, self.channelBValues)
        self.curveCountsC.setData(self.timestampsChannelC, self.channelCValues)
        self.curveCountsD.setData(self.timestampsChannelD, self.channelDValues)
    
    def updateLabels(self, channel, value, uncertainty):
        roundedValue=round(value,2)
        roundedUncertainty=round(uncertainty,5)
        if channel=="A":
            
            self.countChannelAValue.setText(f"Channel A: {roundedValue}")
            self.countChannelAUncertainty.setText(f"Uncertainty A: {roundedUncertainty}")
        elif channel=="B":
            self.countChannelBValue.setText(f"Channel B: {roundedValue}")
            self.countChannelBUncertainty.setText(f"Uncertainty B: {roundedUncertainty}")
        elif channel=="C":
            self.countChannelCValue.setText(f"Channel C: {roundedValue}")
            self.countChannelCUncertainty.setText(f"Uncertainty C: {roundedUncertainty}")
        elif channel=="D":
            self.countChannelDValue.setText(f"Channel D: {roundedValue}")
            self.countChannelDUncertainty.setText(f"Uncertainty D: {roundedUncertainty}")
    
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
        #actions for stop button
        self.stopMeasure()
    


class WorkerThreadCountsEstimated(QThread):
    #One value is for the count estimated and the other is for the uncertainty
    createdSignal=Signal()
    newValue=Signal(str,float,float)
    updateLabel= Signal(str,float,float)
    #Represents date, channelAValue, channelAUncertainty, channelBValue, channelBUncertainty,channelCValue, channelCUncertainty,channelDValue, channelDUncertainty
    newMeasurement=Signal(datetime,float,float,float,float,float,float,float,float)
    
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
            uncertaintyValue=std(values)
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelASentinel:
                valueChannelA=meanValue
                uncertaintyChannelA=uncertaintyValue
            else:
                valueChannelA=0
                uncertaintyChannelA=0
                
                
            if self.channelBSentinel:
                valueChannelB=meanValue
                uncertaintyChannelB=uncertaintyValue
            else:
                valueChannelB=0
                uncertaintyChannelB=0
            
            
            if self.channelCSentinel:
                valueChannelC=meanValue
                uncertaintyChannelC=uncertaintyValue
            else:
                valueChannelC=0
                uncertaintyChannelC=0
            
            
            if self.channelDSentinel:
                valueChannelD=meanValue
                uncertaintyChannelD=uncertaintyValue
            else:
                valueChannelD=0
                uncertaintyChannelD=0    
            
            currentTime = datetime.now().strftime("%H:%M:%S")
            self.newMeasurement.emit(currentTime, valueChannelA, uncertaintyChannelA, valueChannelB, uncertaintyChannelB, valueChannelC, uncertaintyChannelC, valueChannelD, uncertaintyChannelD)


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
        