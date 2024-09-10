from PySide2.QtCore import *
from PySide2.QtCore import QObject
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import createsavefile as savefile
import time
import datetime
from scipy.optimize import curve_fit
from pyTempico import TempicoDevice
import math
class FLIMGraphic():
    #TO DO: DELETE TEMPICO CLASS TYPE OF THE VARIABLE
    def __init__(self,comboBoxStartChannel: QComboBox, comboBoxStopChannel: QComboBox, graphicFrame:QFrame, startButton: QPushButton,stopButton: QPushButton, initialParametersButton: QPushButton,
                 clearButton: QPushButton,saveDataButton:QPushButton,savePlotButton:QPushButton,statusLabel: QLabel, pointLabel: QLabel,binWidthComboBox: QComboBox,numberBins:QComboBox,functionComboBox:QComboBox,
                 numberMeasurementsSpinBox: QSpinBox, totalMeasurements: QLabel,totalStart: QLabel,totalTime: QLabel,timeRange: QLabel,device,applyButton: QPushButton, tauParameter: QLabel,
                 i0Parameter: QLabel,thirdParameter: QLabel,fourthParameter: QLabel,MainWindow):
        super().__init__()
        #Initialize the main window
        self.mainWindow=MainWindow
        #Initialize the Tempico Device class
        self.device=device
        #Initialize comboBox
        self.comboBoxStartChannel=comboBoxStartChannel
        self.comboBoxStopChannel=comboBoxStopChannel
        self.binWidthComboBox=binWidthComboBox
        self.functionComboBox=functionComboBox
        self.numberBins=numberBins
        #Initialize Buttons
        self.startButton=startButton
        self.stopButton=stopButton
        self.clearButton=clearButton
        self.saveDataButton=saveDataButton
        self.savePlotButton=savePlotButton
        self.applyButton=applyButton
        self.initialParametersButton=initialParametersButton
        #Initialize the labels
        self.statusLabel=statusLabel
        self.pointLabel=pointLabel
        self.totalMeasurements=totalMeasurements
        self.totalStart=totalStart
        self.totalTime=totalTime
        self.tauParameter=tauParameter
        self.i0Parameter=i0Parameter
        self.thirdParameter=thirdParameter
        self.fourthParameter=fourthParameter
        self.timeRange=timeRange
        #Initialize the spinBox
        self.numberMeasurementsSpinBox=numberMeasurementsSpinBox
        #Fix the original value of Channels comboBox
        self.comboBoxStopChannel.setCurrentIndex(1)
        self.comboBoxStartChannel.currentIndexChanged.connect(self.indexChangeStartChannel)
        self.comboBoxStopChannel.currentIndexChanged.connect(self.indexChangeStopChannel)
        #Set the enable init Buttons
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.applyButton.setEnabled(False)
        self.initialParametersButton.setEnabled(False)
        #Get initial index for comboBoxChannels
        self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()
        self.oldStopChannelIndex=self.comboBoxStopChannel.currentIndex()
        #Create the timer for label with total Time
        self.time = QTime(0, 0, 0)
        self.timerMeasurements = QTimer()
        self.timerMeasurements.timeout.connect(self.update_timer)
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
        self.plotFLIM.addLegend()
        self.graphicLayout.addWidget(self.winFLIM)
        self.curve = self.plotFLIM.plot(pen='b',  name='Data')
        self.curveFit = self.plotFLIM.plot(pen='r', name='Data fit')
        #-----------------------------------#
        #-----------------------------------#
        #--------End Graphic Creation-------#
        #-----------------------------------#
        #-----------------------------------#
        
        #----------Buttons Connection-------#
        self.startButton.clicked.connect(self.startMeasurement)
        self.stopButton.clicked.connect(self.stopMeasurement)
        self.clearButton.clicked.connect(self.clearGraphic)
        self.applyButton.clicked.connect(self.applyAction)
        self.savePlotButton.clicked.connect(self.savePlotFLIM)
        self.functionComboBox.currentIndexChanged.connect(self.changeFunction)
        self.saveDataButton.clicked.connect(self.saveFLIMData)
        self.initialParametersButton.clicked.connect(self.initialParametersDialog)
        #--------End Buttons Connection-----#
        
        #----------Define other parameters and sentinels-------#
        
        #Sentinel to know if there is a current thread running
        self.threadCreated=False
        #List of measured  values
        self.measuredData=[]
        #List of time Values X axis
        self.measuredTime=[]
        #List of Fit Parameter
        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
        self.FitCov=["nan","nan","nan","nan"]
        #Sentinel to know what is the current fit
        self.currentFit=""
        #Sentiinels to check the files saved
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0  
        #Variables for save the graphic 
        self.ylabel='Counts'
        self.xlabel='Time'
        self.xDataFitCopy=[]
        self.yDataFitCopy=[]
        #InitialValuesFor exponential Fit
        self.initialI0=0
        self.initialTau0=0
        #InitialValuesFor kol Fit
        self.initialI0Kol=0
        self.initialTau0Kol=0
        self.initialBeta=0
        #InitialValuesFor shifted Exponential
        self.initialI0Shif=0
        self.initialTau0Shif=0
        self.initialAlpha=0
        self.initialB=0
        #InitialValuesFor double Exponential
        self.initialI0Doub=0
        self.initialTau0Doub=0
        self.initialTau1Doub=0
        self.initialAlphaDoub=0
        
        #Sentinel to check if there is a initial Parameters change
        self.changeInitialParametersExp=False
        self.changeInitialParametersKol=False
        self.changeInitialParametersDoub=False
        self.changeInitialParametersShif=False
        #Variables to define the mode of the old channels
        self.oldChannelA=1
        self.oldChannelB=1
        self.oldChannelC=1
        self.oldChannelD=1
        #--------End Define other parameters and sentinels-----#
        #--------Init the the timer to check the connection----#
        self.timerStatus=QTimer()
        self.timerStatus.timeout.connect(self.checkDeviceStatus)
        if self.device!=None:
            self.startButton.setEnabled(True)
            self.timerStatus.start(500)
            
            
    #Verify the connection of the function
    def checkDeviceStatus(self):
        try:
            self.device.readIdnFromDevice()
        except:
            
            if self.threadCreated:
                self.worker.stop()
            self.disconnectedDevice()
            msg_box = QMessageBox(self.mainWindow)
            msg_box.setText("Connection with the device has been lost")
            msg_box.setWindowTitle("Connection Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            
        
    # Functions to verify that start and stop will not be the same channels
    def indexChangeStartChannel(self):
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex()+1:
            self.comboBoxStartChannel.setCurrentIndex(self.oldStartChannelIndex)
        else:
            self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()
    
    def indexChangeStopChannel(self):
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex()+1:
            self.comboBoxStopChannel.setCurrentIndex(self.oldStopChannelIndex)
        else:
            self.oldStopChannelIndex=self.comboBoxStopChannel.currentIndex()
    #Function to catch the start button action
    def startMeasurement(self):
        #Disable or enable the necessary
        self.timerStatus.stop()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.clearButton.setEnabled(True)
        self.applyButton.setEnabled(False)
        self.initialParametersButton.setEnabled(False)
        self.comboBoxStartChannel.setEnabled(False)
        self.comboBoxStopChannel.setEnabled(False)
        self.binWidthComboBox.setEnabled(False)
        self.numberBins.setEnabled(False)
        self.mainWindow.tabs.setTabEnabled(0,False)
        self.numberMeasurementsSpinBox.setEnabled(False)
        self.plotFLIM.setLabel('left','Counts '+self.comboBoxStopChannel.currentText())
        self.ylabel='Counts '+self.comboBoxStopChannel.currentText()
        #Change the parameters labels to undefined
        self.resetParametersLabels()
        #Save the channels mode before measurement
        self.saveMode()
        #Reset save parameters
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        #Change status Values
        self.changeStatusLabel("Measurement running")
        self.changeStatusColor(1)
        self.updateLabels("0","0")
        #Reboot the list of measured values and time Data
        self.measuredData=[]
        self.measuredTime=[]
        self.curve.setData(self.measuredTime,self.measuredData)
        #Get the selected channels
        self.getTempicoChannel()
        timeRangeps=self.timeRangeValue()
        #Init the timer measurements
        self.time = QTime(0, 0, 0)
        self.startTimer()
        self.curveFit.setData([],[])
        #Create the thread object
        self.worker=WorkerThreadFLIM(self.currentStartChannel,self.currentStopChannel,self.binWidthComboBox.currentText(),self.numberMeasurementsSpinBox.value(),
                                     self.device,timeRangeps)
        
        #Create connections to main thread 
        self.worker.finished.connect(self.finishedThreadMeasurement)
        self.worker.createdSignal.connect(self.changeCreatedStatus)
        self.worker.statusSignal.connect(self.changeStatusLabel)
        self.worker.pointSignal.connect(self.changeStatusColor)
        self.worker.updateValues.connect(self.updateMeasurement)
        self.worker.updateLabel.connect(self.updateLabel)
        self.worker.updateMeasurementsLabel.connect(self.updateLabels)
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
        self.numberBins.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.savePlotButton.setEnabled(True)
        self.comboBoxStartChannel.setEnabled(True)
        self.comboBoxStopChannel.setEnabled(True)
        self.binWidthComboBox.setEnabled(True)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.changeStatusLabel("No measurement running")
        self.changeStatusColor(0)
        self.threadCreated=False
        self.stopTimer()
        self.timerStatus.start(500)
        self.setOldMode()
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
        if len(self.measuredTime)>0:
            self.applyButton.setEnabled(True)
            self.initialParametersButton.setEnabled(True)
            if not self.changeInitialParametersExp:
                self.initialI0=max(self.measuredData)
                self.initialTau0=np.mean(self.measuredTime)
            if not self.changeInitialParametersKol:
                self.initialI0Kol=max(self.measuredData)
                self.initialTau0Kol=np.mean(self.measuredTime)
                self.initialBeta=0
            if not self.changeInitialParametersShif:
                self.initialI0Shif=max(self.measuredData)
                self.initialTau0Shif=np.mean(self.measuredTime)
                self.initialAlpha=0
                self.initialB=0
            if not self.changeInitialParametersDoub:
                self.initialI0Doub=max(self.measuredData)
                self.initialTau0Doub=np.mean(self.measuredTime)
                self.initialTau1Doub=np.mean(self.measuredTime)
                self.initialAlphaDoub=0
        self.saveDataButton.setEnabled(True)
        
    
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
            self.currentStartChannel=None
        elif startChannelValue==1:
            self.device.ch1.enableChannel()
            self.currentStartChannel=self.device.ch1
        elif startChannelValue==2:
            self.device.ch2.enableChannel()
            self.currentStartChannel=self.device.ch2
        elif startChannelValue==3:
            self.device.ch3.enableChannel()
            self.currentStartChannel=self.device.ch3
        elif startChannelValue==4:
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
    
    
    #Get the mode of the channel to save in a variable before start measurement
    def saveMode(self):
        try:
            self.oldChannelA=self.device.ch1.getMode()
            self.oldChannelB=self.device.ch2.getMode()
            self.oldChannelC=self.device.ch3.getMode()
            self.oldChannelD=self.device.ch4.getMode()
        except:
            pass
    
    #Set the mode before measurement in every channel
    def setOldMode(self):
        try:
            self.device.ch1.setMode(self.oldChannelA)
            self.device.ch2.setMode(self.oldChannelB)
            self.device.ch3.setMode(self.oldChannelC)
            self.device.ch4.setMode(self.oldChannelD) 
        except:
            pass
        
        
    
    
    
        
    #Get the value of the time range label
    def timeRangeValue(self):
        unitsList=self.timeRange.text().split(" ")
        if unitsList[1]=='ps':
            multiplier=1
        elif unitsList[1]=='ns':
            multiplier=10**3
        elif unitsList[1]=='µs':
            multiplier=10**6
        elif unitsList[1]=='ms':
            multiplier=10**9
        valueRange=float(unitsList[0])
        picoSecondsValue=valueRange*multiplier
        return picoSecondsValue
            
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
        self.units=units
        self.unitsLabel='Time ('+units+')'
        self.plotFLIM.setLabel('bottom','Time ('+units+')')
        self.xlabel='Time ('+units+')'
    
    
    def updateLabels(self,totalMeasurements,totalStarts):
        self.totalMeasurements.setText(totalMeasurements)
        self.totalStart.setText(totalStarts)
    
    #Functions created for connect or disconnect the device
    def connectedDevice(self,device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.timerStatus.start(500)
        self.device=device
        self.startButton.setEnabled(True)
        
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.timerStatus.stop()
        self.startButton.setEnabled(False)
    
    #Functions to update the totalTime Label
    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.totalTime.setText(self.time.toString('hh:mm:ss'))
    
    def startTimer(self):
        self.timerMeasurements.start(1000)
    
    def stopTimer(self):
        self.timerMeasurements.stop()
        self.totalTime.setText("No measurement running")
    #Connection with change of comboBox
    def changeFunction(self):
        if self.currentFit=="ExpDecay" and self.functionComboBox.currentIndex()==0:
            if self.FitParameters[0]!="Undefined":
                self.i0Parameter.setText(str(self.FitParameters[0])+" Cov: "+self.FitCov[1])
                self.tauParameter.setText(str(self.FitParameters[1])+self.units+" Cov: "+self.FitCov[0])
            else:
                self.i0Parameter.setText(str(self.FitParameters[0]))
                self.tauParameter.setText(str(self.FitParameters[1]))
        elif self.currentFit=="Kohlrausch" and self.functionComboBox.currentIndex()==1:
            if self.FitParameters[0]!="Undefined":
                self.i0Parameter.setText(str(self.FitParameters[0])+" Cov: "+self.FitCov[1])
                self.tauParameter.setText(str(self.FitParameters[1])+self.units+" Cov: "+self.FitCov[0])
                self.thirdParameter.setText(str(self.FitParameters[2])+" Cov: "+self.FitCov[2])
            else:
                self.i0Parameter.setText(str(self.FitParameters[0]))
                self.tauParameter.setText(str(self.FitParameters[1]))
                self.thirdParameter.setText(str(self.FitParameters[2]))
        elif self.currentFit=="ShiftedExponential" and self.functionComboBox.currentIndex()==2:
            if self.FitParameters[0]!="Undefined":
                self.i0Parameter.setText(str(self.FitParameters[0])+" Cov: "+self.FitCov[1])
                self.tauParameter.setText(str(self.FitParameters[1])+self.units+" Cov: "+self.FitCov[0])
                self.thirdParameter.setText(str(self.FitParameters[2])+" Cov: "+self.FitCov[2])
                self.fourthParameter.setText(str(self.FitParameters[3])+" Cov: "+self.FitCov[3])
            else:
                self.i0Parameter.setText(str(self.FitParameters[0]))
                self.tauParameter.setText(str(self.FitParameters[1]))
                self.thirdParameter.setText(str(self.FitParameters[2]))
                self.fourthParameter.setText(str(self.FitParameters[3]))
        elif self.currentFit=="DoubleExponential" and self.functionComboBox.currentIndex()==3:
            if self.FitParameters[0]!="Undefined":
                self.i0Parameter.setText(str(self.FitParameters[0])+" Cov: "+self.FitCov[1])
                self.tauParameter.setText(str(self.FitParameters[1])+" "+self.units+" Cov: "+self.FitCov[0])
                self.thirdParameter.setText(str(self.FitParameters[2])+" "+self.units+" Cov: "+self.FitCov[2])
                self.fourthParameter.setText(str(self.FitParameters[3])+" Cov: "+self.FitCov[3])
            else:
                self.i0Parameter.setText(str(self.FitParameters[0]))
                self.tauParameter.setText(str(self.FitParameters[1]))
                self.thirdParameter.setText(str(self.FitParameters[2]))
                self.fourthParameter.setText(str(self.FitParameters[3]))
        else:
            self.i0Parameter.setText("Undefined")
            self.tauParameter.setText("Undefined")
            if self.functionComboBox.currentIndex()==1:
                self.thirdParameter.setText("Undefined")
            elif self.functionComboBox.currentIndex()==2:
                self.fourthParameter.setText("Undefined")
             
    #Connection with the ApplyButton
    def applyAction(self):
        if len(self.measuredData)>0:
            try:
                if self.functionComboBox.currentText()=="Exponential":
                    i0,tau0=self.fitExpDecay(self.measuredTime,self.measuredData)
                    if i0=="Undefined" or str(i0)=='nan':
                        self.currentFit=""
                        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
                    else:
                        self.currentFit="ExpDecay"
                        self.FitParameters[0]=round(i0,3)
                        self.FitParameters[1]=round(tau0,3)
                elif self.functionComboBox.currentText()=="Kohlrausch":
                    i0,tau0,beta=self.fitKohlrauschFit(self.measuredTime,self.measuredData)
                    print(str(i0)=='nan')
                    if i0=="Undefined" or str(i0)=='nan':
                        self.currentFit=""
                        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
                    else:
                        self.currentFit="fitKohlrausch"
                        self.FitParameters[0]=round(i0,3)
                        self.FitParameters[1]=round(tau0,3)
                        self.FitParameters[2]=round(beta,3)
                    
                elif self.functionComboBox.currentText()=="Shifted exponencial":
                    i0,tau0,alpha,b=self.fitShiiftedExponential(self.measuredTime,self.measuredData)
                    if i0=="Undefined" or str(i0)=='nan':
                        self.currentFit=""
                        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
                    else:   
                        self.currentFit="ShiftedExponential"
                        self.FitParameters[0]=round(i0,3)
                        self.FitParameters[1]=round(tau0,3)
                        self.FitParameters[2]=round(alpha,3)
                        self.FitParameters[3]=round(b,3)
                        
                elif self.functionComboBox.currentText()=="Double exponencial":
                    i0,tau0,tau1,alpha=self.fitDoubleExponential(self.measuredTime,self.measuredData)
                    if i0=="Undefined" or str(i0)=='nan':
                        self.currentFit=""
                        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
                    else:   
                        self.currentFit="DoubleExponential"
                        self.FitParameters[0]=round(i0,3)
                        self.FitParameters[1]=round(tau0,3)
                        self.FitParameters[2]=round(tau1,3)
                        self.FitParameters[3]=round(alpha,3)
                    
            except NameError:
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    
                    
    #Reset the labels when a measurement begins
    def resetParametersLabels(self):
        if self.currentFit=="DoubleExponential":
            self.tauParameter.setText("Undefined")
            self.i0Parameter.setText("Undefined")
            self.thirdParameter.setText("Undefined")
            self.fourthParameter.setText("Undefined")
        elif self.currentFit=="ShiftedExponential":
            self.tauParameter.setText("Undefined")
            self.i0Parameter.setText("Undefined")
            self.thirdParameter.setText("Undefined")
            self.fourthParameter.setText("Undefined")
        elif self.currentFit=="fitKohlrausch":
            self.tauParameter.setText("Undefined")
            self.i0Parameter.setText("Undefined")
            self.thirdParameter.setText("Undefined")
        elif self.currentFit=="ExpDecay":
            self.tauParameter.setText("Undefined")
            self.i0Parameter.setText("Undefined")
            
    #fit exponential curver
    def fitExpDecay(self,xData,yData):
        # Initial guess for the parameters
        try:
            initial_guess = [self.initialI0, self.initialTau0]
            # Curve fitting
            popt, pcov = curve_fit(self.exp_decay, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0 and tau0
            I0_opt, tau0_opt = popt
            yFit = self.exp_decay(xData, I0_opt, tau0_opt)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=pcov[0][0]
                tau_0Cov=pcov[1][1]
                I_0CovString=self.roundStringPCov(I_0Cov)
                tau_0CovString=self.roundStringPCov(tau_0Cov)
                self.FitCov[0]=I_0CovString
                self.FitCov[1]=tau_0CovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"         
            print("Covariance parameters")
            print("Covariance I_0")
            print(I_0CovString)
            print("Covariance tau_0")
            print(tau_0CovString) 
            #Graphic of the fit curve
            self.curveFit.setData(xData,yFit)
            if str(I0_opt)=='nan':
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                self.tauParameter.setText(str(round(I0_opt,3))+" Cov: "+I_0CovString)
                self.i0Parameter.setText(str(round(tau0_opt,3))+" "+self.units+" Cov: "+tau_0CovString)
            return I0_opt, tau0_opt
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined"
        

    #fit kohlrausch curver
    def fitKohlrauschFit(self,xData,yData):
        try:
            # Initial guess for the parameters
            initial_guess = [self.initialI0Kol, self.initialTau0Kol, self.initialBeta]
            # Curve fitting
            popt, pcov = curve_fit(self.kohl_decay, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0 and tau0
            I0_opt, tau0_opt, beta_opt = popt
            yFit = self.kohl_decay(xData, I0_opt, tau0_opt,beta_opt)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=pcov[0][0]
                tau_0Cov=pcov[1][1]
                betaCov=pcov[2][2]
                I_0CovString=self.roundStringPCov(I_0Cov)
                tau_0CovString=self.roundStringPCov(tau_0Cov)
                betaCovString=self.roundStringPCov(betaCov)
                self.FitCov[0]=I_0CovString
                self.FitCov[1]=tau_0CovString
                self.FitCov[2]=betaCovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"
                self.FitCov[2]="nan"
            #Graphic of the fit curve
            self.curveFit.setData(xData,yFit)
            if str(I0_opt)=='nan':
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                self.tauParameter.setText(str(round(I0_opt,3))+" "+self.units+" Cov: "+I_0CovString)
                self.i0Parameter.setText(str(round(tau0_opt,3))+" Cov: "+tau_0CovString)
                self.thirdParameter.setText(str(round(beta_opt,3))+" Cov: "+betaCovString)
            return I0_opt, tau0_opt, beta_opt
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()  
            return "Undefined","Undefined","Undefined"
    #Initial Parameters Dialog
    def initialParametersDialog(self):
        self.initialDialog = QDialog(self.mainWindow)
        self.initialDialog.setWindowTitle("Select Function Parameters")
        layout = QVBoxLayout(self.initialDialog)
        # ComboBox for selecting the function type
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Exponential fit", "Kohlrausch fit", "Shifted Exponential fit","Double Exponential fit"])
        layout.addWidget(self.combo_box)
        # Form layout for input fields
        form_layout = QFormLayout()
        layout.addLayout(form_layout)
        # Input fields for Exponential
        self.I_0_field = QDoubleSpinBox()
        self.I_0_field.setDecimals(2)
        self.I_0_field.setRange(-float('inf'), float('inf'))
        
        self.Tau_0_field = QDoubleSpinBox()
        self.Tau_0_field.setDecimals(2)
        self.Tau_0_field.setRange(-float('inf'), float('inf'))
        
        # Additional fields for Kolrausch
        self.Beta_field = QDoubleSpinBox()
        self.Beta_field.setDecimals(2)
        self.Beta_field.setRange(-float('inf'), float('inf'))
        
        # Additional fields for Shifted Exponential
        self.Alpha_field = QDoubleSpinBox()
        self.Alpha_field.setDecimals(2)
        self.Alpha_field.setRange(-float('inf'), float('inf'))
        
        self.B_field = QDoubleSpinBox()
        self.B_field.setDecimals(2)
        self.B_field.setRange(-float('inf'), float('inf'))
        # Function to update the form based on the selected function
        def update_form():
            # Clear the form
            for i in reversed(range(form_layout.count())):
                form_layout.itemAt(i).widget().setParent(None)
            if self.combo_box.currentText() == "Exponential fit":
                self.I_0_field.setValue(self.initialI0)
                self.Tau_0_field.setValue(self.initialTau0)
                form_layout.addRow("I<sub>0<\sub>:", self.I_0_field)
                form_layout.addRow("τ<sub>0<\sub>:", self.Tau_0_field)
            elif self.combo_box.currentText() == "Kohlrausch fit":
                self.I_0_field.setValue(self.initialI0Kol)
                self.Tau_0_field.setValue(self.initialTau0Kol)
                self.Beta_field.setValue(self.initialBeta)
                form_layout.addRow("I<sub>0<\sub>:", self.I_0_field)
                form_layout.addRow("τ<sub>0<\sub>:", self.Tau_0_field)
                form_layout.addRow("β:", self.Beta_field)
            elif self.combo_box.currentText() == "Shifted Exponential fit":
                self.I_0_field.setValue(self.initialI0Shif)
                self.Tau_0_field.setValue(self.initialTau0Shif)
                self.Alpha_field.setValue(self.initialAlpha)
                self.B_field.setValue(self.initialB)
                form_layout.addRow("I<sub>0<\sub>:", self.I_0_field)
                form_layout.addRow("τ<sub>0<\sub>:", self.Tau_0_field)
                form_layout.addRow("α:", self.Alpha_field)
                form_layout.addRow("b:", self.B_field)
            elif self.combo_box.currentText() == "Double Exponential fit":
                self.I_0_field.setValue(self.initialI0Doub)
                self.Tau_0_field.setValue(self.initialTau0Doub)
                self.Alpha_field.setValue(self.initialTau1Doub)
                self.B_field.setValue(self.initialAlphaDoub)
                form_layout.addRow("I<sub>0<\sub>:", self.I_0_field)
                form_layout.addRow("τ<sub>0<\sub>:", self.Tau_0_field)
                form_layout.addRow("τ<sub>1<\sub>:", self.Alpha_field)
                form_layout.addRow("α:", self.B_field)
        # Connect the ComboBox change signal to the update function
        self.combo_box.currentIndexChanged.connect(update_form)
        # Initialize the form
        update_form()
        # Apply and Reset buttons
        button_layout = QHBoxLayout()
        apply_button = QPushButton("Apply")
        reset_button = QPushButton("Default Values")
        button_layout.addWidget(apply_button)
        button_layout.addWidget(reset_button)
        apply_button.clicked.connect(self.applyInitialDialog)
        reset_button.clicked.connect(self.resetInitialDialog)
        layout.addLayout(button_layout)
        self.initialDialog.exec_()
    
    #Function to connect the apply button
    def applyInitialDialog(self):
        print("Se ejecuta")
        if self.combo_box.currentText()=="Exponential fit":
            self.initialI0=self.I_0_field.value()
            self.initialTau0=self.Tau_0_field.value()
            self.changeInitialParametersExp=True
        elif self.combo_box.currentText()=="Kohlrausch fit":
            self.initialI0Kol=self.I_0_field.value()
            self.initialTau0Kol=self.Tau_0_field.value()
            self.initialBeta=self.Beta_field.value()
            self.changeInitialParametersKol=True
        elif self.combo_box.currentText()=="Shifted Exponential fit":
            self.initialI0Shif=self.I_0_field.value()
            self.initialTau0Shif=self.Tau_0_field.value()
            self.initialAlpha=self.Alpha_field.value()
            self.initialB=self.B_field.value()
            self.changeInitialParametersShif=True
        elif self.combo_box.currentText()=="Double Exponential fit":
            self.initialI0Doub=self.I_0_field.value()
            self.initialTau0Doub=self.Tau_0_field.value()
            self.initialTau1Doub=self.Alpha_field.value()
            self.initialAlphaDoub=self.B_field.value()
            self.changeInitialParametersDoub=True
        self.initialDialog.accept()
    #Function to connect the reset button
    def resetInitialDialog(self):
        if len(self.measuredData)>0:
            if self.combo_box.currentText()=="Exponential fit":
                self.initialI0=max(self.measuredData)
                self.initialTau0=np.mean(self.measuredTime)
                self.I_0_field.setValue(self.initialI0)
                self.Tau_0_field.setValue(self.initialTau0)
                self.changeInitialParametersExp=False
            elif self.combo_box.currentText()=="Kohlrausch fit":
                self.initialI0Kol=max(self.measuredData)
                self.initialTau0Kol=np.mean(self.measuredTime)
                self.initialBeta=1.0
                self.Beta_field.setValue(self.initialBeta)
                self.I_0_field.setValue(self.initialI0Kol)
                self.Tau_0_field.setValue(self.initialTau0Kol)
                self.changeInitialParametersKol=False
            elif self.combo_box.currentText()=="Shifted Exponential fit":
                self.initialI0Shif=max(self.measuredData)
                self.initialTau0Shif=np.mean(self.measuredTime)
                self.initialAlpha=0
                self.initialB=0
                self.I_0_field.setValue(self.initialI0Shif)
                self.Tau_0_field.setValue(self.initialTau0Shif)
                self.Alpha_field.setValue(self.initialAlpha)
                self.B_field.setValue(self.initialB)
                self.changeInitialParametersShif=False
            elif self.combo_box.currentText()=="Double Exponential fit":
                self.initialI0Doub=max(self.measuredData)
                self.initialTau0Doub=np.mean(self.measuredTime)
                self.initialAlphaDoub=0
                self.initialTau1Doub=np.mean(self.measuredTime)
                self.I_0_field.setValue(self.initialI0Doub)
                self.Tau_0_field.setValue(self.initialTau0Doub)
                self.Alpha_field.setValue(self.initialTau1Doub)
                self.B_field.setValue(self.initialAlphaDoub)
                self.changeInitialParametersDoub=False
        

    
    #fit Shifted Exponential
    def fitShiiftedExponential(self, xData, yData):
        try:
            # Initial guess for the parameters: I0, tau0, alpha, b
            initial_guess = [self.initialI0Shif, self.initialTau0Shif, self.initialAlpha, self.initialB]
            # Curve fitting
            popt, pcov = curve_fit(self.shifted_decay_function, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0, tau0, alpha, and b
            I0_opt, tau0_opt, alpha_opt, b_opt = popt
            # Calculate the fitted curve
            yFit = self.shifted_decay_function(xData, I0_opt, tau0_opt, alpha_opt, b_opt)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=pcov[0][0]
                tau_0Cov=pcov[1][1]
                alphaCov=pcov[2][2]
                bCov=pcov[3][3]
                I_0CovString=self.roundStringPCov(I_0Cov)
                tau_0CovString=self.roundStringPCov(tau_0Cov)
                alphaCovString=self.roundStringPCov(alphaCov)
                bCovString=self.roundStringPCov(bCov)
                self.FitCov[0]=I_0CovString
                self.FitCov[1]=tau_0CovString
                self.FitCov[2]=alphaCovString
                self.FitCov[3]=bCovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"
                self.FitCov[2]="nan"
                self.FitCov[3]="nan"
            # Graphic of the fit curve
            self.curveFit.setData(xData, yFit)
            # Set the fitted parameters in the UI
            if str(I0_opt)=='nan':
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                self.tauParameter.setText(str(round(I0_opt, 3))+" Cov: "+I_0CovString)
                self.i0Parameter.setText(str(round(tau0_opt, 3))+" "+self.units+" Cov: "+tau_0CovString)
                self.thirdParameter.setText(str(round(alpha_opt, 3))+" Cov: "+alphaCovString)
                self.fourthParameter.setText(str(round(b_opt, 3))+" Cov: "+bCovString)
            return I0_opt, tau0_opt, alpha_opt, b_opt
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined","Undefined","Undefined"
    
    
    #fit Double exponential
    def fitDoubleExponential(self, xData, yData):
        try:
            # Initial guess for the parameters: I0, tau0, alpha, b
            initial_guess = [self.initialI0Doub, self.initialTau0Doub, self.initialTau1Doub, self.initialAlphaDoub]
            # Curve fitting
            popt, pcov = curve_fit(self.double_Exponential, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0, tau0, alpha, and b
            I0_opt, tau0_opt, tau1_opt, alpha_opt = popt
            # Calculate the fitted curve
            yFit = self.double_Exponential(xData, I0_opt, tau0_opt, tau1_opt, alpha_opt)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=pcov[0][0]
                tau_0Cov=pcov[1][1]
                tau_1Cov=pcov[2][2]
                alphaCov=pcov[3][3]
                I_0CovString=self.roundStringPCov(I_0Cov)
                tau_0CovString=self.roundStringPCov(tau_0Cov)
                tau_1CovString=self.roundStringPCov(tau_1Cov)
                alphaCovString=self.roundStringPCov(alphaCov)
                self.FitCov[0]=I_0CovString
                self.FitCov[1]=tau_0CovString
                self.FitCov[2]=tau_1CovString
                self.FitCov[3]=alphaCovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"
                self.FitCov[2]="nan"
                self.FitCov[3]="nan"
            # Graphic of the fit curve
            self.curveFit.setData(xData, yFit)
            # Set the fitted parameters in the UI
            if str(I0_opt)=='nan':
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                self.tauParameter.setText(str(round(I0_opt, 3))+" Cov: "+I_0CovString)
                self.i0Parameter.setText(str(round(tau0_opt, 3))+" "+self.units+" Cov: "+tau_0CovString)
                self.thirdParameter.setText(str(round(tau1_opt, 3))+" "+self.units+" Cov: "+tau_1CovString)
                self.fourthParameter.setText(str(round(alpha_opt, 3))+" Cov: "+alphaCovString)
            return I0_opt, tau0_opt, tau1_opt, alpha_opt
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined","Undefined","Undefined"
        
    
    
        
        
        
    #Exponential Decay Function
    def exp_decay(self,t, I0, tau0):
        return I0 * np.exp(-t / tau0)

    #Kohlrausch Decay Function
    def kohl_decay(self,t, I0, tau0,beta):
        return I0 * np.exp((-t / tau0)**beta)
    
    #Shifted Exponential Function
    def shifted_decay_function(self, t, I0, tau0, alpha, b):
        # Define the decay function with the new equation
        return I0 * np.exp(-(t - alpha) / tau0) + b
    #Double Exponential Function
    def double_Exponential(self,t, I0, tau0, tau1, alpha): 
        return I0*(alpha*np.exp(-t/tau0)+(1-alpha)*np.exp(-t/tau1))

    #Function to get the string of the pcov numbers
    
    def roundStringPCov(self, number):
        if number == 0:
            return "0.00"
        exponent = int(math.floor(math.log10(abs(number))))
        rounded_number = round(number / (10 ** exponent), 2)
        if exponent != 0:
            return f"{rounded_number:.2f}e{exponent:+d}"
        else:
            return f"{rounded_number:.2f}"
    
    #Save buttons
    #Save Plot Button
    def savePlotFLIM(self):
        try:
            graph_names=[]
            #Open select the format
            dialog =QDialog(self.mainWindow)    
            dialog.setObjectName("ImageFormat")
            dialog.resize(285,105)
            dialog.setWindowTitle("Save Plots")
            verticalLayout_2 = QVBoxLayout(dialog)
            verticalLayout_2.setObjectName("verticalLayout_2")
            VerticalImage = QVBoxLayout()
            VerticalImage.setObjectName("VerticalImage")
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
            
            # Connect the button "Accept" to the accept dialog method
            accepButton.clicked.connect(dialog.accept)
            if dialog.exec_()==QDialog.Accepted:
                selected_format=FormatBox.currentText()
                copyWin=pg.GraphicsLayoutWidget()
                copyWin.setBackground('w')
                copyPlot=copyWin.addPlot()
                copyPlot.showGrid(x=True, y=True)
                copyPlot.setLabel('left',self.ylabel)
                copyPlot.setLabel('bottom',self.xlabel)
                copyPlot.addLegend()
                copyCurve=copyPlot.plot(pen='b', name='Data')
                copyFit=copyPlot.plot(pen='r', name='Data fit')
                copyCurve.setData(self.measuredTime,self.measuredData)
                copyFit.setData(self.xDataFitCopy,self.yDataFitCopy)
                # Add a footer for the graphic
                if self.currentFit=="ExpDecay":
                    textFooter="Fit: I<sub>0</sub>*e^(-t/τ<sub>0</sub>) , Parameters: I<sub>0</sub>="+str(self.FitParameters[0])+" τ<sub>0</sub>:"+str(self.FitParameters[1])+" "+self.units
                elif self.currentFit=="fitKohlrausch":
                    textFooter="Fit: I<sub>0</sub>*e^((-t/τ<sub>0</sub>)^(β)) , Parameters: I<sub>0</sub>="+str(self.FitParameters[0])+" τ<sub>0</sub>:"+str(self.FitParameters[1])+" "+self.units+" 	β:"+str(self.FitParameters[2])
                elif self.currentFit=="ShiftedExponential":
                    textFooter="Fit: I<sub>0</sub>*e^((-t+α)/τ<sub>0</sub>))+b, Parameters: I<sub>0</sub>="+str(self.FitParameters[0])+" τ<sub>0</sub>:"+str(self.FitParameters[1])+" "+self.units+" α:"+str(self.FitParameters[2])+" b:"+str(self.FitParameters[3])
                elif self.currentFit=="DoubleExponential":
                    textFooter="Fit: I<sub>0</sub>*(α*e^(-t/τ<sub>0</sub>)+(1-α)*e^(-t/τ<sub>1</sub>)), Parameters: I<sub>0</sub>="+str(self.FitParameters[0])+" τ<sub>0</sub>:"+str(self.FitParameters[1])+" "+self.units+" τ<sub>1</sub>:"+str(self.FitParameters[2])+" "+self.units+" α:"+str(self.FitParameters[3])
                    
                else:
                    textFooter="No fit has been applied"
                    
                footer = pg.LabelItem(text=textFooter, justify='left')
                copyWin.addItem(footer, row=2, col=0)
                copyWin.ci.layout.setRowStretchFactor(0.4, 0.1)
                copyPlot.getViewBox().setState(self.plotFLIM.getViewBox().getState())
                exporter=pg.exporters.ImageExporter(copyWin.scene())
                exporter.parameters()['width'] = 1000
                exporter.parameters()['height'] = 700
                folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                current_date=datetime.datetime.now()
                current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                graph_name='FLIMMeasurement'+current_date_str
                exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                initial_text="The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+ "with the following names:"
                text_route="\n"+graph_name+"."+selected_format
                graph_names.append(graph_name)
                message_box = QMessageBox(self.mainWindow)
                message_box.setText(initial_text+text_route)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                # show successful save
                message_box.exec_()            
        except NameError:
            print(NameError)
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
    #Save Data Button
    def saveFLIMData(self):
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
            total_condition= conditiontxt or conditiondat or conditioncsv
            folder_path=savefile.read_default_data()['Folder path']
            if not total_condition:
                current_date=datetime.datetime.now()
                current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                fitSetting=""
                if self.currentFit=="ExpDecay":
                    fitSetting="Exponential Fit:"+'\t'+'I_0*e^(-t/tau_0)'+'\n'+'Tau_0:'+'\t'+str(self.FitParameters[0])+'\n'+'I_0:'+'\t'+str(self.FitParameters[1])
                elif self.currentFit=="Kohlrausch":
                    fitSetting="Kohlrausch Fit:"+'\t'+'I_0*e^((-t/tau_0)^(Beta))'+'\n'+'Tau_0:'+'\t'+str(self.FitParameters[0])+'\n'+'I_0:'+'\t'+str(self.FitParameters[1])+'\n'+'Beta: '+'\t'+ str(self.FitParameters[2])
                elif self.currentFit=="ShiftedExponential":
                    fitSetting="Shifted Exponential Fit"+'\t'+'I_0*e^((-t+alpha)/tau_0))+b'+'\n'+'Tau_0:'+'\t'+str(self.FitParameters[0])+'\n'+'I_0:'+'\t'+str(self.FitParameters[1])+'\n'+'alpha: '+'\t'+ str(self.FitParameters[2])+'\n'+'b: '+'\t'+ str(self.FitParameters[3])
                elif self.currentFit=="DoubleExponential":
                    fitSetting="Double Exponential Fit"+'\t'+'I0*(alpha*np.exp(-t/tau0)+(1-alpha)*np.exp(-t/tau1))'+'\n'+'Tau_0:'+'\t'+str(self.FitParameters[0])+'\n'+'I_0:'+'\t'+str(self.FitParameters[1])+'\n'+'Tau_1: '+'\t'+ str(self.FitParameters[2])+'\n'+'alpha: '+'\t'+ str(self.FitParameters[3])
                elif self.currentFit=="":
                    fitSetting=""
                    
                #Channel Setting
                fitSetting+='\n'+'Start Channel: '+'\t'+self.comboBoxStartChannel.currentText()
                fitSetting+='\n'+'Stop Channel: '+'\t'+self.comboBoxStopChannel.currentText()
                
                
                #Put the settings and fit
                filename="FLIMMeasurement"+current_date_str
                #Round the values in order to get a better txt files
                newMeasuredTime=[]
                for i in self.measuredTime:
                    newValue=round(i,5)
                    newMeasuredTime.append(newValue)
                data=[newMeasuredTime,self.measuredData ]
                try:
                    savefile.save_FLIM_data(data,filename,folder_path,fitSetting,selected_format, self.unitsLabel)
                    if selected_format=="txt":
                        self.oldtxtName=filename
                        self.sentinelsavetxt=1
                    elif selected_format=="csv":
                        self.oldcsvName=filename
                        self.sentinelsavecsv=1
                    elif selected_format=="dat":
                        self.olddatName=filename
                        self.sentinelsavedat=1
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Information)
                    if selected_format=="txt":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldtxtName+".txt"
                    elif selected_format=="csv":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldcsvName+".csv"
                    elif selected_format=="dat":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.olddatName+".dat"
                    message_box.setText(textRoute)
                    message_box.setWindowTitle("Successful save")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()   
                except NameError:
                    print(NameError)
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()         
            else:
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Information)
                if selected_format=="txt":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldtxtName+".txt"
                elif selected_format=="csv":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldcsvName+".csv"
                elif selected_format=="dat":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.olddatName+".dat"
                message_box.setText(textRoute)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()



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
    updateMeasurementsLabel=Signal(str,str)
    def __init__(self,deviceStartChannel,deviceStopChannel,binwidthText,numberMeasurements,device,TimeRange):
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
        self.TimeRange=TimeRange
        #Getting the value in picoSeconds of binWidtrh
        self.getBinWidthNumber()
        #Getting the mode of the device
        self.measurementMode()
        #Measurement List
        self.startStopDifferences=[]
        #Get the sequence of no measurements
        self.noMeasurementsCounter=0
        
    #Main Function
    def run(self):
        #Prueba: TO DO BORRAR
        self.createdSignal.emit()
        while self.totalMeasurements<self.numberMeasurements and self._is_running:
            
            percentage=round((self.totalMeasurements*100)/self.numberMeasurements,2)
            self.checkDeviceStatus()
            #Try in order to avoid the errors related to suddenly disconnect the device
            self.checkDeviceStatus()
            try:
                self.takeMeasurements(percentage)
                self.createFLIMData()
            except:
                pass
            
    #Functon to define the mode of the measurement
    def measurementMode(self):
        if self.TimeRange<=500000:
            self.device.ch1.setMode(1)
            self.device.ch2.setMode(1)
            self.device.ch3.setMode(1)
            self.device.ch4.setMode(1)
        else:
            self.device.ch1.setMode(2)
            self.device.ch2.setMode(2)
            self.device.ch3.setMode(2)
            self.device.ch4.setMode(2)
        
    #Take one measurement function
    def takeMeasurements(self, percentage):
        #Init the config to take measurement
        self.device.setNumberOfRuns(100)
        if self.deviceStartChannel!=None:
            self.deviceStartChannel.setStopMask(0)
            self.deviceStartChannel.setNumberOfStops(1)
        self.deviceStopChannel.setStopMask(0)
        self.deviceStopChannel.setNumberOfStops(1)
        measurement=self.device.measure()
        try:
            if len(measurement)==0:
                self.totalRuns+=100
                self.noMeasurementsCounter+=100
                self.statusSignal.emit("Measurement running: Input Channel is not taking measurements")
                self.pointSignal.emit(3)
            else:
                if self.noMeasurementsCounter>=100:
                    self.statusSignal.emit("Measurement running: Stop Channel is not taking measurements")
                    self.pointSignal.emit(3)
                else:
                    self.statusSignal.emit("Measurement running: "+str(percentage)+"%")
                for i in range(100):
                    if not self._is_running:
                        break
                    #TO DO: CHANGE THE VALUE ACCORDING TO THE CHANNEL
                    #TO DO: CHECK IF THE START VALUE IS THE SAME
                    if self.deviceStartChannel!=None:
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
                                if differenceValue<=self.TimeRange:
                                    self.noMeasurementsCounter=0
                                    self.startStopDifferences.append(differenceValue)
                                else:
                                    self.noMeasurementsCounter+=1
                            else:
                                self.noMeasurementsCounter+=1
                        else:
                            self.noMeasurementsCounter+=1
                        
                                
                    else:
                        currentStopMeasurement=measurement[i]
                        sentinelStop=len(currentStopMeasurement)==4 and currentStopMeasurement[3]!=-1
                        partialStop=len(currentStopMeasurement)==4 
                        if sentinelStop:
                            differenceValue=currentStopMeasurement[3]
                            if differenceValue>0:
                                self.totalMeasurements+=1
                                self.totalTime+=differenceValue
                                if differenceValue<=self.TimeRange:
                                    self.noMeasurementsCounter=0
                                    self.startStopDifferences.append(differenceValue)
                                else:
                                    self.noMeasurementsCounter+=1
                            else:
                                self.noMeasurementsCounter+=1
                        else:
                            self.noMeasurementsCounter+=1
                        if partialStop:
                            self.totalStarts+=1
                    if self.totalMeasurements>=self.numberMeasurements:
                        break
                if self.noMeasurementsCounter>=100:
                    self.statusSignal.emit("Measurement running: Stop Channel is not taking measurements")
                    self.pointSignal.emit(3)
                    
        except:
            self.totalRuns+=100
            self.noMeasurementsCounter+=100
            self.statusSignal.emit("Measurement running: Input Channel is not taking measurements")
            self.pointSignal.emit(3)
                
                
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
        self.updateMeasurementsLabel.emit(str(self.totalMeasurements),str(self.totalStarts))
            
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
        self.totalMeasurements=0
    
    #Check the connection of the device
    def checkDeviceStatus(self):
        try:
            self.device.readIdnFromDevice()
        except:
            self.stop()
    
    #Stop thread function
    @Slot()
    def stop(self):
        self._is_running=False
        self.statusSignal.emit("Ending measurement")
        self.pointSignal.emit(2)
    
    
        
        
    
    
    