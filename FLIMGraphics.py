from PySide2.QtCore import *
from PySide2.QtCore import QObject
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import createsavefile as savefile
import time
from pyTempico import TempicoDevice
class FLIMGraphic():
    #TO DO: DELETE TEMPICO CLASS TYPE OF THE VARIABLE
    def __init__(self,comboBoxStartChannel: QComboBox, comboBoxStopChannel: QComboBox, graphicFrame:QFrame, startButton: QPushButton,stopButton: QPushButton,
                 clearButton: QPushButton,saveDataButton:QPushButton,savePlotButton:QPushButton,statusLabel: QLabel, pointLabel: QLabel,binWidthComboBox: QComboBox,
                 numberMeasurementsSpinBox: QSpinBox, device: TempicoDevice):
        super().__init__()
        #Initialize the Tempico Device class
        self.device=device
        #Initialize comboBox
        self.comboBoxStartChannel=comboBoxStartChannel
        self.comboBoxStopChannel=comboBoxStopChannel
        self.binWidthComboBox=binWidthComboBox
        #Initialize Buttons
        self.startButton=startButton
        self.stopButton=stopButton
        self.clearButton=clearButton
        self.saveDataButton=saveDataButton
        self.savePlotButton=savePlotButton
        #Initialize the labels
        self.statusLabel=statusLabel
        self.pointLabel=pointLabel
        #Initialize the spinBox
        self.numberMeasurementsSpinBox=numberMeasurementsSpinBox
        #Fix the original value of Channels comboBox
        self.comboBoxStopChannel.setCurrentIndex(1)
        self.comboBoxStartChannel.currentIndexChanged.connect(self.indexChangeStartChannel)
        self.comboBoxStopChannel.currentIndexChanged.connect(self.indexChangeStopChannel)
        #Set the enable init Buttons
        self.stopButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        #Get initial index for comboBoxChannels
        self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()
        self.oldStopChannelIndex=self.comboBoxStopChannel.currentIndex()
        #-----------------------------------#
        #-----------------------------------#
        #----------Graphic Creation---------#
        #-----------------------------------#
        #-----------------------------------#
        self.graphicLayout=QHBoxLayout(graphicFrame)
        self.winFLIM=pg.GraphicsLayoutWidget()
        self.winFLIM.setBackground('w')
        #Add the plot to the window
        self.plotFLIM=self.winFLIM.addPlot()
        self.plotFLIM.showGrid(x=True, y=True)
        #Add Labels
        self.plotFLIM.setLabel('left','Counts')
        self.plotFLIM.setLabel('bottom','Time')
        self.graphicLayout.addWidget(self.winFLIM)
        self.curve = self.plotFLIM.plot(pen='b')
        #-----------------------------------#
        #-----------------------------------#
        #--------End Graphic Creation-------#
        #-----------------------------------#
        #-----------------------------------#
        
        #----------Buttons Connection-------#
        self.startButton.clicked.connect(self.startMeasurement)
        self.stopButton.clicked.connect(self.stopMeasurement)
        self.clearButton.clicked.connect(self.clearGraphic)
        #--------End Buttons Connection-----#
        
        #----------Define other parameters and sentinels-------#
        self.currentStartChannel=self.device.ch1
        self.currentStopChannel=self.device.ch2
        #Sentinel to know if there is a current thread running
        self.threadCreated=False
        #List of measured  values
        self.measuredData=[]
        #List of time Values X axis
        self.measuredTime=[]
        #--------End Define other parameters and sentinels-----#
        
        
        
    # Functions to verify that start and stop will not be the same channels
    def indexChangeStartChannel(self):
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex():
            self.comboBoxStartChannel.setCurrentIndex(self.oldStartChannelIndex)
        else:
            self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()
    
    def indexChangeStopChannel(self):
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex():
            self.comboBoxStopChannel.setCurrentIndex(self.oldStopChannelIndex)
        else:
            self.oldStopChannelIndex=self.comboBoxStopChannel.currentIndex()
    #Function to catch the start button action
    def startMeasurement(self):
        #Disable or enable the necessary
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.clearButton.setEnabled(True)
        self.comboBoxStartChannel.setEnabled(False)
        self.comboBoxStopChannel.setEnabled(False)
        self.binWidthComboBox.setEnabled(False)
        self.numberMeasurementsSpinBox.setEnabled(False)
        #Change status Values
        self.changeStatusLabel("Measurement running")
        self.changeStatusColor(1)
        #Reboot the list of measured values and time Data
        self.measuredData=[]
        self.measuredTime=[]
        #Get the selected channels
        self.getTempicoChannel()
        #Create the thread object
        self.worker=WorkerThreadFLIM(self.currentStartChannel,self.currentStopChannel,self.binWidthComboBox.currentText(),self.numberMeasurementsSpinBox.value(),
                                     self.device)
        #Create connections to main thread 
        self.worker.finished.connect(self.finishedThreadMeasurement)
        self.worker.createdSignal.connect(self.changeCreatedStatus)
        self.worker.statusSignal.connect(self.changeStatusLabel)
        self.worker.pointSignal.connect(self.changeStatusColor)
        self.worker.updateValues.connect(self.updateMeasurement)
        self.worker.updateLabel.connect(self.updateLabel)
        #Start the thread
        self.worker.start()
    def getUnits(self,value):
        if value < 1e3:
            return ["ps",1]
        elif value < 1e6:
            return ["ns",10**3]
        elif value < 1e9:
            return ["µs",10**6]
        elif value < 1e12:
            return ["ms",10**9]
        
        
    
    #Function to catch the stop button action
    def stopMeasurement(self):
        #Disable or enable the necessary
        if self.threadCreated:
            self.worker.stop()
        else:
            self.enableAfterFinisihThread()
    
    #Function to clear the graphic
    def clearGraphic(self):
        self.measuredData=[]
        self.measuredTime=[]
        if self.threadCreated:
            self.worker.clear()
        
    def enableAfterFinisihThread(self):
        self.stopButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.comboBoxStartChannel.setEnabled(True)
        self.comboBoxStopChannel.setEnabled(True)
        self.binWidthComboBox.setEnabled(True)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.changeStatusLabel("No measurement running")
        self.changeStatusColor(0)
        self.threadCreated=False
        
        
    #Function to change the status measurement
    def changeStatusLabel(self, textValue):
        self.statusLabel.setText(textValue)
        
    #Function to change the color of point measurement
    def changeStatusColor(self, color):
        pixmap = QPixmap(self.pointLabel.size())
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
        point_size = min(self.pointLabel.width(), self.pointLabel.height()) // 2
        x = (self.pointLabel.width() - point_size) // 2
        y = (self.pointLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.pointLabel.setPixmap(pixmap)
        
    #Function to get the tempico Channel from the comboBoxValue
    def getTempicoChannel(self):
        startChannelValue=self.comboBoxStartChannel.currentIndex()
        stopChannelValue=self.comboBoxStopChannel.currentIndex()
        #Init with all channels disabled
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        
        #Get the start channel before begin the measurement
        if startChannelValue==0:
            self.device.ch1.enableChannel()
            self.currentStartChannel=self.device.ch1
        elif startChannelValue==1:
            self.device.ch2.enableChannel()
            self.currentStartChannel=self.device.ch2
        elif startChannelValue==2:
            self.device.ch3.enableChannel()
            self.currentStartChannel=self.device.ch3
        elif startChannelValue==3:
            self.device.ch4.enableChannel()
            self.currentStartChannel=self.device.ch4
        
        #Get the stop channel before begin the measurement
        if stopChannelValue==0:
            self.device.ch1.enableChannel()
            self.currentStopChannel=self.device.ch1
        elif stopChannelValue==1:
            self.device.ch2.enableChannel()
            self.currentStopChannel=self.device.ch2
        elif stopChannelValue==2:
            self.device.ch3.enableChannel()
            self.currentStopChannel=self.device.ch3
        elif stopChannelValue==3:
            self.device.ch4.enableChannel()
            self.currentStopChannel=self.device.ch4
            
    #Function to execute when the thread is finished
    def finishedThreadMeasurement(self):
        #To do BORRAR EL PRINT
        print("Finalizo la ejecución del thread")
        self.enableAfterFinisihThread()
        
    #Function to connect the signal with created thread sentinel
    def changeCreatedStatus(self):
        self.threadCreated=True
    
    #Function to update the measured values
    def updateMeasurement(self,listOfNewValues,domainMeasurement):
        self.measuredData=listOfNewValues
        self.measuredTime=domainMeasurement
        self.curve.setData(self.measuredTime,self.measuredData)
    #Function to get the Label with the correct units
    def updateLabel(self,units):
        self.plotFLIM.setLabel('bottom','Time ('+units+')')
    
    def updateLabels(self,totalSampleTime,totalMeasurements,totalStarts):
        pass
        
        
    


#The measurement is created in a thread in order to avoid a low performance in the graphic interface
#AVOID TO CHANGE SOMETING OF THE GRAPHIC INTERFACE IN THE THREAD
#THREAD IS ONLY TO MANAGE, MEASURE AND CALCULATE DATA
#AVOID TO CLOSE THE THREAD WITH PYQT5 METHODS LIKE .CLOSE(), .EXIT(), .QUIT(), .STOP() 
#TO CLOSE THE THREAD LET RUN THE MAIN FUNCTION UNTIL FINAL
class WorkerThreadFLIM(QThread):
    createdSignal=Signal()
    statusSignal=Signal(str)
    pointSignal=Signal(int)
    updateValues=Signal(list,list)
    updateLabel=Signal(str)
    def __init__(self,deviceStartChannel,deviceStopChannel,binwidthText,numberMeasurements,device):
        super().__init__()
        #Parameters of the measurement
        self.totalTime=0
        self.totalMeasurements=0
        self.totalStarts=0
        self.totalRuns=0
        #Class parameters
        self._is_running=True
        self.deviceStartChannel=deviceStartChannel
        self.deviceStopChannel=deviceStopChannel
        self.binwidthText=binwidthText
        self.numberMeasurements=numberMeasurements
        self.device=device
        #Getting the value in picoSeconds of binWidtrh
        self.getBinWidthNumber()
        #Measurement List
        self.startStopDifferences=[]
    #Main Function
    def run(self):
        #Prueba: TO DO BORRAR
        self.createdSignal.emit()
        i=1
        while i<201 and self._is_running:
            percentage=round(i/2)
            self.takeMeasurements(percentage)
            self.createFLIMData()
            i+=1
            
    #Take one measurement function
    def takeMeasurements(self, percentage):
        #Init the config to take measurement
        self.device.setNumberOfRuns(100)
        self.deviceStartChannel.setStopMask(0)
        self.deviceStopChannel.setStopMask(0)
        self.deviceStartChannel.setNumberOfStops(1)
        self.deviceStopChannel.setNumberOfStops(1)
        measurement=self.device.measure()
        if len(measurement)==0:
            self.totalRuns+=100
            self.statusSignal.emit("Measurement running: Input Channel is not taking measurements")
            self.pointSignal.emit(3)
        else:
            self.statusSignal.emit("Measurement running: "+str(percentage)+"%")
        for i in range(100):
            if not self._is_running:
                break
            #TO DO: CHANGE THE VALUE ACCORDING TO THE CHANNEL
            #TO DO: CHECK IF THE START VALUE IS THE SAME
            currentStartMeasurement=measurement[i]
            currentStopMeasurement=measurement[i+100]
            sentinelStart=len(currentStartMeasurement)==4 and currentStartMeasurement[3]!=-1
            sentinelStop=len(currentStopMeasurement)==4 and currentStopMeasurement[3]!=-1
            if sentinelStart:
                self.totalStarts+=1
            if sentinelStart and sentinelStop:
                differenceValue=currentStopMeasurement[3]-currentStartMeasurement[3]
                if differenceValue>0:
                    self.totalMeasurements+=1
                    self.totalTime+=differenceValue
                    self.startStopDifferences.append(differenceValue)
    #Function to created the data to update the histogram graphic
    def createFLIMData(self):
        if len(self.startStopDifferences)>0:
            maximumValue=max(self.startStopDifferences)
            unitsDivisionFactor=self.getUnits(maximumValue)
            units=unitsDivisionFactor[0]
            divisionFactor=unitsDivisionFactor[1]
            newDifferences=[]
            #Normalizing the data according to the units
            if divisionFactor==1:
                newDifferences=self.startStopDifferences
                newBinWidth=self.binwidthPicoSeconds
            else:
                newBinWidth=self.binwidthPicoSeconds/divisionFactor
                for i in range(len(self.startStopDifferences)):
                    currentValue=self.startStopDifferences[i]
                    newValue=currentValue/divisionFactor
                    newDifferences.append(newValue)
            domainValues=np.arange(0,maximumValue/divisionFactor,newBinWidth)
            bin_edges = np.append(domainValues - newBinWidth / 2, domainValues[-1] + newBinWidth / 2)
            counts,_ = np.histogram(newDifferences, bins=bin_edges)
            self.updateValues.emit(counts,domainValues)
            self.updateLabel.emit(units)
            
    #Function to get the scale in time of the histogram
    def getUnits(self,picosecondsValue):
        if picosecondsValue < 1e3:
            return ["ps",1]
        elif picosecondsValue < 1e6:
            return ["ns",10**3]
        elif picosecondsValue < 1e9:
            return ["µs",10**6]
        elif picosecondsValue < 1e12:
            return ["ms",10**9]
    def getBinWidthNumber(self):
        splitList=self.binwidthText.split(' ')
        number=int(splitList[0])
        units=splitList[1].replace(' ','')
        if units=='ps':
            multiplier=1
        elif units=='ns':
            multiplier=10**3
        elif units=='µs':
            multiplier=10**6
        self.binwidthPicoSeconds=number*multiplier
    
    #Function to clear the graphic
    def clear(self):
        self.startStopDifferences=[]
        
    #Stop thread function
    @Slot()
    def stop(self):
        self._is_running=False
        self.statusSignal.emit("Ending measurement")
        self.pointSignal.emit(2)
    
    
        
        
    
    
    