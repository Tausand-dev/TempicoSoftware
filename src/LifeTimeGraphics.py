from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace
from numpy import append as appnd
from createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
class LifeTimeGraphic():
    """
    Class responsible for the logic and functionality of the LifeTime (Fluorescence Lifetime Measurement) window.

    This class manages the creation and updating of graphical plots related to LifeTime, controls user interactions with various 
    buttons, and ensures that measurements are taken from the specified channels. The class handles:
    - Initialization of the graphical interface elements.
    - Starting and stopping of measurements.
    - Saving of data and plots.
    - Displaying parameters of the measurements, such as the number of measurements taken, and the percentage of completion.

    :param comboBoxStartChannel: The combo box for selecting the start channel (QComboBox).
    :param comboBoxStopChannel: The combo box for selecting the stop channel (QComboBox).
    :param graphicFrame: The frame that holds the graphical plot (QFrame).
    :param startButton: The button to start the measurements (QPushButton).
    :param stopButton: The button to stop the measurements (QPushButton).
    :param initialParametersButton: The button to configure initial parameters (QPushButton).
    :param clearButton: The button to clear the graphs and data (QPushButton).
    :param saveDataButton: The button to save the measurement data (QPushButton).
    :param savePlotButton: The button to save the graph plot (QPushButton).
    :param statusLabel: The label showing the current status (QLabel).
    :param pointLabel: The label displaying the current point in the measurement (QLabel).
    :param binWidthComboBox: The combo box for selecting the bin width (QComboBox).
    :param numberBins: The combo box for selecting the number of bins (QComboBox).
    :param functionComboBox: The combo box for selecting a function (QComboBox).
    :param numberMeasurementsSpinBox: The spin box for specifying the number of measurements (QSpinBox).
    :param totalMeasurements: The label showing the total number of measurements (QLabel).
    :param totalStart: The label showing the number of measurements taken from the start channel (QLabel).
    :param totalTime: The label showing the total time of measurements (QLabel).
    :param timeRange: The label showing the time range for the measurements (QLabel).
    :param device: The connected Tempico device used for measurements.
    :param applyButton: The button for applying selected parameters (QPushButton).
    :param parameterTable: The table displaying the parameters of the measurements (QTableWidget).
    :param MainWindow: The main window that holds the application UI elements.
    :param timerStatus: The timer used for periodic updates (QTimer).
    :return: None
    """
    #TO DO: DELETE TEMPICO CLASS TYPE OF THE VARIABLE
    def __init__(self,comboBoxStartChannel: QComboBox, comboBoxStopChannel: QComboBox, graphicFrame:QFrame, startButton: QPushButton,stopButton: QPushButton, initialParametersButton: QPushButton,
                 clearButton: QPushButton,saveDataButton:QPushButton,savePlotButton:QPushButton,statusLabel: QLabel, pointLabel: QLabel,binWidthComboBox: QComboBox,numberBins:QComboBox,functionComboBox:QComboBox,
                 numberMeasurementsSpinBox: QSpinBox, totalMeasurements: QLabel,totalStart: QLabel,totalTime: QLabel,timeRange: QLabel,device,applyButton: QPushButton, parameterTable: QTableWidget,MainWindow, timerStatus: QTimer):
        super().__init__()
        self.savefile=savefile()
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
        self.winLifeTime=pg.GraphicsLayoutWidget()
        self.winLifeTime.setBackground('w')
        #Add the plot to the window
        self.plotLifeTime=self.winLifeTime.addPlot()
        self.plotLifeTime.showGrid(x=True, y=True)
        #Add Labels
        self.plotLifeTime.setLabel('left','Counts')
        self.plotLifeTime.setLabel('bottom','Time')
        self.plotLifeTime.addLegend()
        self.graphicLayout.addWidget(self.winLifeTime)
        self.curve = self.plotLifeTime.plot(pen='b',  name='Data')
        self.curveFit = self.plotLifeTime.plot(pen='r', name='Data fit')
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
        self.savePlotButton.clicked.connect(self.savePlotLifeTime)
        self.functionComboBox.currentIndexChanged.connect(self.changeFunction)
        self.saveDataButton.clicked.connect(self.saveLifeTimeData)
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
        self.initialBeta=1
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
        #Initialize Paramaters Table for fit
        self.parametersTable=parameterTable
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
        #Variable to define the old number of runs
        self.oldNumberRuns=0
        #--------End Define other parameters and sentinels-----#
        #--------Init the the timer to check the connection----#
        self.timerStatus=timerStatus
        self.timerStatus.timeout.connect(self.checkDeviceStatus)
        #Set the value of R^2
        self.R2="Undefined"
        if self.device!=None:
            self.startButton.setEnabled(True)
            self.timerStatus.start(500)
            
            
    #Verify the connection of the function
    def checkDeviceStatus(self):
        """
        Verifies the device's operational status by attempting to read its identification.

        This function performs the following actions:
        - Attempts to read the identification from the device to ensure it is functioning correctly.
        - If the read operation fails, it stops any running worker thread and disconnects the device from the serial port.
        - Displays an error message indicating that the connection with the device has been lost.

        :return: None
        """
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
        """
        Verifies that the options of the start and stop combo boxes are not the same 
        when the start combo box is changed. If they are the same, it reverts to 
        the previously selected option.

        :return: None
        """
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex()+1:
            self.comboBoxStartChannel.setCurrentIndex(self.oldStartChannelIndex)
        else:
            self.oldStartChannelIndex=self.comboBoxStartChannel.currentIndex()
    
    def indexChangeStopChannel(self):
        """
        Verifies that the options of the start and stop combo boxes are not the same 
        when the stop combo box is changed. If they are the same, it reverts to 
        the previously selected option.

        :return: None
        """
        if self.comboBoxStartChannel.currentIndex()==self.comboBoxStopChannel.currentIndex()+1:
            self.comboBoxStopChannel.setCurrentIndex(self.oldStopChannelIndex)
        else:
            self.oldStopChannelIndex=self.comboBoxStopChannel.currentIndex()
            
    #Function to catch the start button action
    def startMeasurement(self):
        """
        Initiates the measurement process by clearing previous data, resetting the UI, and starting a new measurement thread.

        This function performs several actions to prepare for and start a new measurement:
        - Stops the status timer and disables/enables relevant buttons.
        - Clears previous graph data and resets parameter labels.
        - Saves the current channel modes and resets save parameters.
        - Updates the status label and color to indicate a running measurement.
        - Clears previously measured data and time, resetting the plot.
        - Retrieves the selected channels and initializes a new measurement thread with the selected parameters.
        - Connects signals from the worker thread to corresponding slots in the main thread for UI updates.

        :return: None
        """
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
        if 'Start' in self.comboBoxStartChannel.currentText():
            self.plotLifeTime.setLabel('left','Counts '+self.comboBoxStopChannel.currentText())
            self.ylabel='Counts '+self.comboBoxStopChannel.currentText()
            
        else:
            self.plotLifeTime.setLabel('left','Counts Channels '+self.comboBoxStartChannel.currentText().replace("Channel ","")+'-'+self.comboBoxStopChannel.currentText().replace("Channel ",""))
            self.ylabel='Counts '+self.comboBoxStartChannel.currentText()+'-'+self.comboBoxStopChannel.currentText()
            
            
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
        self.xDataFitCopy=[]
        self.yDataFitCopy=[]
        #Create the thread object
        self.worker=WorkerThreadLifeTime(self.currentStartChannel,self.currentStopChannel,self.binWidthComboBox.currentText(),self.numberMeasurementsSpinBox.value(),
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
        """
        Receives a numerical value in picoseconds (ps) and returns a list with two values:
        the appropriate units for the value and a number indicating by how much to divide 
        the value for conversion.

        :param value: The numerical value in picoseconds to convert.
        :return: A list containing the appropriate unit as a string and a number indicating 
                the divisor for conversion.
        """
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
        """
        Stops the measurement thread if it is created and executes the 
        function enableAfterFinishedThread() if the thread is not created.

        :return: None
        """
        #Disable or enable the necessary
        if self.threadCreated:
            self.worker.stop()
        else:
            self.enableAfterFinisihThread()
    
    #Function to clear the graphic
    def clearGraphic(self):
        """
        Clears the measured data and time lists when a measurement is in progress 
        and also clears the graphic by executing the worker's clear function.

        :return: None
        """  
        self.measuredData=[]
        self.measuredTime=[]
        if self.threadCreated:
            self.worker.clear()
        
    def enableAfterFinisihThread(self):
        """
        Executes when a measurement ends, either by pressing the stop button 
        or when it has naturally finished. Re-enables the buttons, combo boxes, 
        and fields necessary for a new measurement or for saving data. 
        Resets the default parameters for the settings.

        :return: None
        """
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
                self.initialTau0=mean(self.measuredTime)
            if not self.changeInitialParametersKol:
                self.initialI0Kol=max(self.measuredData)
                self.initialTau0Kol=mean(self.measuredTime)
                self.initialBeta=1
            if not self.changeInitialParametersShif:
                self.initialI0Shif=max(self.measuredData)
                self.initialTau0Shif=mean(self.measuredTime)
                self.initialAlpha=0
                self.initialB=0
            if not self.changeInitialParametersDoub:
                self.initialI0Doub=max(self.measuredData)
                self.initialTau0Doub=mean(self.measuredTime)
                self.initialTau1Doub=mean(self.measuredTime)
                self.initialAlphaDoub=0
        self.saveDataButton.setEnabled(True)
        
    
    #Function to change the status measurement
    def changeStatusLabel(self, textValue):
        """
        Changes the text of the status label.

        :param textValue: The text to set for the status label (str).
        :return: None
        """
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
        """
        Assigns the Tempico device channels based on the selected values from the combo boxes.
        The selected start and stop channels are assigned to the variables `currentStartChannel` 
        and `currentStopChannel`, respectively. It also enables the corresponding channels.

        :return: None
        """
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
        """
        Saves the current modes of the channels before starting a measurement.
        The modes are stored in the variables `oldChannelA`, `oldChannelB`, 
        `oldChannelC`, and `oldChannelD`, allowing for restoration to the original settings after the measurement.

        :return: None
        """
        try:
            self.oldNumberRuns=self.device.getNumberOfRuns()
            self.oldChannelA=self.device.ch1.getMode()
            self.oldChannelB=self.device.ch2.getMode()
            self.oldChannelC=self.device.ch3.getMode()
            self.oldChannelD=self.device.ch4.getMode()
        except:
            pass
    
    #Set the mode before measurement in every channel
    def setOldMode(self):
        """
        Restores the modes of the channels after a measurement is completed.
        The channels are set to their previous modes stored in `oldChannelA`, 
        `oldChannelB`, `oldChannelC`, and `oldChannelD`.

        :return: None
        """
        try:     
            self.device.setNumberOfRuns(self.oldNumberRuns)
            self.device.ch1.setMode(self.oldChannelA)
            self.device.ch2.setMode(self.oldChannelB)
            self.device.ch3.setMode(self.oldChannelC)
            self.device.ch4.setMode(self.oldChannelD) 
        except:
            pass
        
        
    
    
    
        
    #Get the value of the time range label
    def timeRangeValue(self):
        """
        Converts the value from the timeRange label to picoseconds (ps).

        :return: float
            The value converted to picoseconds.
        """
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
        """
        Executes when the measurement thread finishes.

        This function enables the UI components related to new measurements 
        and resets the settings to default.

        :return: None
        """
        self.enableAfterFinisihThread()
        
    #Function to connect the signal with created thread sentinel
    def changeCreatedStatus(self):
        """
        Notifies that the measurement thread has been created.

        This function sets the status of thread creation to True.

        :return: None
        """
        self.threadCreated=True
    
    #Function to update the measured values
    def updateMeasurement(self,listOfNewValues,domainMeasurement):
        """
        Updates the measured data and time with new values and refreshes the graph.

        This function receives a new list of values representing counts and their corresponding
        update times, assigning them to the variables measuredData and measuredTime, and 
        updates the graph accordingly.

        :param listOfNewValues: The new list of measurement values (list).
        :param domainMeasurement: The list of times corresponding to the measurement values (list).
        :return: None
        """
        self.measuredData=listOfNewValues
        self.measuredTime=domainMeasurement
        self.curve.setData(self.measuredTime,self.measuredData)
        
    #Function to get the Label with the correct units
    def updateLabel(self,units):
        """
        Updates the label of the x-axis in the graph with the correct units for the data.

        This function takes the units as a string and updates the x-axis label accordingly.

        :param units: The units to be displayed on the x-axis label (str).
        :return: None
        """
        self.units=units
        self.unitsLabel='Time ('+units+')'
        self.plotLifeTime.setLabel('bottom','Time ('+units+')')
        self.xlabel='Time ('+units+')'
    
    
    def updateLabels(self,totalMeasurements,totalStarts):
        """
        Updates the labels for total measurements and total starts with the given values.

        This function sets the text of the totalMeasurements and totalStart labels 
        according to the parameters provided.

        :param totalMeasurements: The text to set for the total measurements label (str).
        :param totalStarts: The text to set for the total starts label (str).
        :return: None
        """
        self.totalMeasurements.setText(totalMeasurements)
        self.totalStart.setText(totalStarts)
    
    #Functions created for connect or disconnect the device
    def connectedDevice(self,device):
        """
        Configures the UI options when the Tempico device is connected.

        This function enables and disables the appropriate buttons and starts the timer to monitor the device status.
        - Enables the disconnect button and disables the connect button.
        - Starts a status timer with a 500 ms interval.
        - Assigns the connected device to the class attribute and enables the start button.

        :param device: The connected Tempico device.
        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.timerStatus.start(500)
        self.device=device
        self.startButton.setEnabled(True)
        
    def disconnectedDevice(self):
        """
        Configures the UI options when the Tempico device is disconnected.

        This function disables and enables the appropriate buttons and stops the timer that monitors the device status.
        - Disables the disconnect button and enables the connect button.
        - Stops the status timer.
        - Disables the start button.

        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.timerStatus.stop()
        self.startButton.setEnabled(False)
    
    #Functions to update the totalTime Label
    def update_timer(self):
        """
        Updates the timer for the ongoing measurement by adding one second.

        This function increments the time variable by one second and updates the 
        totalTime label to reflect the new time.

        :return: None
        """
        self.time = self.time.addSecs(1)
        self.totalTime.setText(self.time.toString('hh:mm:ss'))
    
    def startTimer(self):
        """
        Starts the timer that triggers the update_timer function every second.

        This function initiates the timer for the ongoing measurement, allowing
        the update_timer function to be executed at one-second intervals.

        :return: None
        """
        self.timerMeasurements.start(1000)
    
    def stopTimer(self):
        """
        Stops the timer that triggers the update_timer function.

        This function halts the timer responsible for updating the measurement time
        and sets the totalTime label to indicate that no measurement is currently running.

        :return: None
        """
        self.timerMeasurements.stop()
        self.totalTime.setText("No measurement running")
    
    #Connection with change of comboBox
    def changeFunction(self):
        """
        Updates the parameter values in the UI based on the selected function in the functionComboBox.

        This function checks the current fitting function (e.g., "ExpDecay", "Kohlrausch", "ShiftedExponential", or 
        "DoubleExponential") and updates the parameter labels accordingly. If the parameters have already been calculated,
        it will display the values along with their uncertainties and units. If the parameters are not available, it sets 
        the values to "Undefined".

        Variables assignment:
        - Parameters like "I0", "tau0", "Beta", "alpha", "b", "R^2", and their respective uncertainties are assigned using 
        `insertParameters()` based on the fitting model.
        - Units are assigned through the `self.units` attribute for certain parameters (e.g., tau0).
        
        Behavior by function:
        - ExpDecay: Updates `I0`, `tau0`, and `R^2`.
        - Kohlrausch: Updates `I0`, `tau0`, `Beta`, and `R^2`.
        - ShiftedExponential: Updates `I0`, `tau0`, `alpha`, `b`, and `R^2`.
        - DoubleExponential: Updates `I0`, `tau0`, `tau1`, `alpha`, and `R^2`.

        :return: None
        """
        if self.currentFit=="ExpDecay" and self.functionComboBox.currentIndex()==0:
            if self.FitParameters[0]!="Undefined":

                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),str(float(self.FitCov[0])),"")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),str(float(self.FitCov[1])),self.units)
                ####################
                #Change R^2 parameter
                self.insertParameters(2,"R^2",str(self.R2),"","")
                ####################
                
            else:
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),"","")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),"","")
                ####################
                #Change R^2 parameter
                self.insertParameters(2,"R^2",str(self.R2),"","")
                ####################

        elif self.currentFit=="Kohlrausch" and self.functionComboBox.currentIndex()==1:
            if self.FitParameters[0]!="Undefined":
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),str(float(self.FitCov[0])),"")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),str(float(self.FitCov[1])),self.units)
                ####################
                #Change the Beta parameter values
                self.insertParameters(2,"β",str(self.FitParameters[2]),str(float(self.FitCov[2])),"")
                ####################
                #Change R^2 parameter
                self.insertParameters(3,"R^2",str(self.R2),"","")
                ####################

            else:
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),"","")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),"","")
                ####################
                #Change the Beta parameter values
                self.insertParameters(2,"β",str(self.FitParameters[2]),"","")
                ####################
                #Change R^2 parameter
                self.insertParameters(3,"R^2",str(self.R2),"","")
                ####################

        elif self.currentFit=="ShiftedExponential" and self.functionComboBox.currentIndex()==2:
            if self.FitParameters[0]!="Undefined":
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),str(float(self.FitCov[0])),"")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),str(float(self.FitCov[1])),self.units)
                ####################
                #Change the alpha parameter values
                self.insertParameters(2,"α",str(self.FitParameters[2]),str(float(self.FitCov[2])),"")
                ####################
                #Change the b parameter values
                self.insertParameters(3,"b",str(self.FitParameters[3]),str(float(self.FitCov[3])),"")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")
                ####################
                
            else:
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),"","")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),"","")
                ####################
                #Change the alpha parameter values
                self.insertParameters(2,"α",str(self.FitParameters[2]),"","")
                ####################
                #Change the b parameter values
                self.insertParameters(3,"b",str(self.FitParameters[3]),"","")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")
                ####################

        elif self.currentFit=="DoubleExponential" and self.functionComboBox.currentIndex()==3:
            if self.FitParameters[0]!="Undefined":
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),str(float(self.FitCov[0])),"")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),str(float(self.FitCov[1])),self.units)
                ####################
                #Change the tau1 parameter values
                self.insertParameters(2,"τ1",str(self.FitParameters[2]),str(float(self.FitCov[2])),self.units)
                ####################
                #Change the alpha parameter values
                self.insertParameters(3,"α",str(self.FitParameters[3]),str(float(self.FitCov[3])),"")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")
                ####################
                
            else:
                #Change the I0 parameter values
                self.insertParameters(0,"I0",str(self.FitParameters[0]),"","")
                ####################
                #Change the tau parameter values
                self.insertParameters(1,"τ0",str(self.FitParameters[1]),"","")
                ####################
                #Change the tau1 parameter values
                self.insertParameters(2,"τ1",str(self.FitParameters[2]),"","")
                ####################   
                #Change the alpha parameter values
                self.insertParameters(3,"α",str(self.FitParameters[3]),"","")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")
                ####################

        else:
            #Change the I0 parameter values
            self.insertParameters(0,"I0","Undefined","","")
            ####################
            #Change the tau parameter values
            self.insertParameters(1,"τ0","Undefined","","")
            ####################
            if self.functionComboBox.currentIndex()==0:
                #Change R^2 parameter
                self.insertParameters(2,"R^2","Undefined","","")
                ####################
            elif self.functionComboBox.currentIndex()==1:
                #Change the Beta parameter values
                self.insertParameters(2,"β","Undefined","","")
                ####################
                #Change R^2 parameter
                self.insertParameters(3,"R^2","Undefined","","")
                ####################
            elif self.functionComboBox.currentIndex()==2:
                #Change the alpha parameter values
                self.insertParameters(2,"α","Undefined","","")
                ####################
                #Change the b parameter values
                self.insertParameters(3,"b","Undefined","","")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2","Undefined","","")
                ####################
            elif self.functionComboBox.currentIndex()==3:
                #Change the tau1 parameter values
                self.insertParameters(2,"τ1","Undefined","","")
                ####################
                #Change the alpha parameter values
                self.insertParameters(3,"α","Undefined","","")
                ####################
                #Change R^2 parameter
                self.insertParameters(4,"R^2","Undefined","","")
                ####################
        
    def insertParameters(self,index,Parameter,Value,Cov,Units):
        """
        Inserts the parameter values into the fitting table at the specified row.

        This function updates the table used for displaying the fitted parameters by inserting the parameter name, its 
        value, the covariance (uncertainty), and the units in the specified row of the table.

        Variables assignment:
        - The parameter name is assigned to the first column of the specified row (`index`).
        - The value of the parameter is assigned to the second column.
        - The covariance of the parameter is assigned to the third column.
        - The units of the parameter are assigned to the fourth column.

        :param index: The row index where the values will be inserted (int).
        :param Parameter: The name of the parameter to be displayed (str).
        :param Value: The value of the parameter to be displayed (str).
        :param Cov: The covariance (uncertainty) of the parameter (str).
        :param Units: The units of the parameter (str).
        :return: None
        """
        #Change parameter values
        self.parametersTable.setItem(index,0,QTableWidgetItem(Parameter))
        self.parametersTable.setItem(index,1,QTableWidgetItem(Value))
        self.parametersTable.setItem(index,2,QTableWidgetItem(Cov))
        self.parametersTable.setItem(index,3,QTableWidgetItem(Units))
        ####################
             
    #Connection with the ApplyButton
    def applyAction(self):
        """
        Captures the action of the 'apply' button, calculates the selected fit, and stores the resulting parameters.

        This function determines which fitting function is selected from `functionComboBox` and attempts to calculate
        the fit using the measured time and data. If the parameters can be determined, they are stored in `FitParameters`.
        If not, a dialog informs the user that the parameters could not be determined.

        Variables assignment:
        - The parameters `i0`, `tau0`, and other fit-specific variables are calculated using the corresponding fit function.
        - If the fit is successful, the rounded parameters are stored in `FitParameters`.
        - If the fit fails or returns "Undefined", a message box is shown to inform the user of the error.

        :return: None
        """
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
                    if i0=="Undefined" or str(i0)=='nan':
                        self.currentFit=""
                        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
                    else:
                        self.currentFit="fitKohlrausch"
                        self.FitParameters[0]=round(i0,3)
                        self.FitParameters[1]=round(tau0,3)
                        self.FitParameters[2]=round(beta,3)
                    
                elif self.functionComboBox.currentText()=="Shifted exponential":
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
                        
                elif self.functionComboBox.currentText()=="Double exponential":
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
        """
        Resets all the fit parameters to 'Undefined' and clears the current fit type.

        This function sets the list `FitParameters` to contain "Undefined" values for all parameters and clears `currentFit`.
        Additionally, it resets the `R2` value to "Undefined". Depending on the selected fit type in `functionComboBox`,
        the respective parameter labels in the table are updated to reflect "Undefined" values.

        Variables assignment:
        - `FitParameters` is reset to a list of "Undefined".
        - `currentFit` is cleared to an empty string.
        - `R2` is reset to "Undefined".
        - The `insertParameters` method is used to update the table with "Undefined" values for each parameter
        based on the selected function in `functionComboBox`.

        :return: None
        """
        self.FitParameters=["Undefined","Undefined","Undefined","Undefined"]
        self.currentFit=""
        self.R2="Undefined"
        if self.functionComboBox.currentText()=="Double exponential":
            self.insertParameters(0,"I0","Undefined","","")
            self.insertParameters(1,"τ0","Undefined","","")
            self.insertParameters(2,"τ1","Undefined","","")
            self.insertParameters(3,"α","Undefined","","")
            self.insertParameters(4,"R^2","Undefined","","")
                
            
        elif self.functionComboBox.currentText()=="Shifted exponential":
            self.insertParameters(0,"I0","Undefined","","")
            self.insertParameters(1,"τ0","Undefined","","")
            self.insertParameters(2,"α","Undefined","","")
            self.insertParameters(3,"b","Undefined","","")
            self.insertParameters(4,"R^2","Undefined","","")
            
        elif self.functionComboBox.currentText()=="Kohlrausch":
            self.insertParameters(0,"I0","Undefined","","")
            self.insertParameters(1,"τ0","Undefined","","")
            self.insertParameters(2,"β","Undefined","","")
            self.insertParameters(3,"R^2","Undefined","","")
            
        elif self.functionComboBox.currentText()=="Exponential":
            self.insertParameters(0,"I0","Undefined","","")
            self.insertParameters(1,"τ0","Undefined","","")
            self.insertParameters(2,"R^2","Undefined","","")
            
            
    #fit exponential curver
    def fitExpDecay(self,xData,yData):
        """
        Calculates the exponential decay fit for the given data.

        This function attempts to fit an exponential decay model to the provided `xData` and `yData`. If successful,
        the optimal parameters (I0, tau0) are used to update the respective labels in the parameters table along with
        their uncertainties (covariance), and the fitted curve is plotted. If the fit cannot be performed, it alerts
        the user via a message box.

        Variables assignment:
        - `self.FitCov`: Contains the covariance values for I0 and tau0, or "nan" if not calculable.
        - `self.xDataFitCopy`: Stores a copy of the `xData` for the fitted curve.
        - `self.yDataFitCopy`: Stores the computed y-values for the fitted curve.
        - `self.R2`: Stores the calculated R² value for the fit.
        - `self.curveFit`: Updates the plot with the fitted curve data.

        :param xData: The x-axis data points (array-like).
        :param yData: The y-axis data points (array-like).
        :return: Tuple (I0_opt, tau0_opt) containing the fitted values of I0 and tau0, or ("Undefined", "Undefined") if fitting fails.
        :rtype: tuple(float, float) or tuple(str, str)
        """
        # Initial guess for the parameters
        try:
            initial_guess = [self.initialI0, self.initialTau0]
            # Curve fitting
            popt, pcov = curve_fit(self.exp_decay, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0 and tau0
            I0_opt, tau0_opt = popt
            self.xDataFitCopy=xData
            yFit=[]
            for i in xData:
                value=self.exp_decay(i, I0_opt, tau0_opt)
                yFit.append(value)
            self.yDataFitCopy=yFit
            try:
                I_0Cov=sqrt(pcov[0][0])
                tau_0Cov=sqrt(pcov[1][1])
                if I_0Cov>I0_opt:
                    self.FitCov[0]="nan"
                    I_0CovString="nan"
                else:
                    I_0CovString=self.roundStringPCov(I_0Cov)
                    self.FitCov[0]=I_0CovString
                if tau_0Cov>tau_0Cov:
                    self.FitCov[1]="nan"
                    tau_0CovString="nan"
                else:
                    tau_0CovString=self.roundStringPCov(tau_0Cov)    
                    self.FitCov[1]=tau_0CovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"         
            #Graphic of the fit curve
            self.curveFit.setData(xData,yFit)
            if str(I0_opt)=='nan':
                self.curveFit.setData([],[])
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                r2Parameter=self.calculateR2(yData,yFit)
                self.R2=round(r2Parameter,3)
                maxRoundTau0=self.maxRound(I_0CovString)
                maxRoundI0=self.maxRound(tau_0CovString)
                #Change I0 parameter
                self.insertParameters(0,"I0",str(round(I0_opt,maxRoundTau0)),str(float(I_0CovString)),"")
                #Change tau0 parameter
                self.insertParameters(1,"τ0",str(round(tau0_opt,maxRoundI0)),str(float(tau_0CovString)),self.units)
                #Change R^2 parameter
                self.insertParameters(2,"R^2",str(self.R2),"","")


            return I0_opt, tau0_opt
        except:
            self.curveFit.setData([],[])
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined"
        

    #fit kohlrausch curver
    def fitKohlrauschFit(self,xData,yData):
        """
        Calculates the Kohlrausch fit for the given data.

        This function attempts to fit a Kohlrausch (stretched exponential) model to the provided `xData` and `yData`.
        If successful, the optimal parameters (I0, tau0, Beta) are used to update the respective labels in the parameters
        table along with their uncertainties (covariance), and the fitted curve is plotted. If the fit cannot be performed,
        it alerts the user via a message box.

        Variables assignment:
        - `self.FitCov`: Contains the covariance values for I0, tau0, and Beta, or "nan" if not calculable.
        - `self.xDataFitCopy`: Stores a copy of the `xData` for the fitted curve.
        - `self.yDataFitCopy`: Stores the computed y-values for the fitted curve.
        - `self.R2`: Stores the calculated R² value for the fit.
        - `self.curveFit`: Updates the plot with the fitted curve data.

        :param xData: The x-axis data points (array-like).
        :param yData: The y-axis data points (array-like).
        :return: Tuple (I0_opt, tau0_opt, beta_opt) containing the fitted values of I0, tau0, and Beta, or ("Undefined", "Undefined", "Undefined") if fitting fails.
        :rtype: tuple(float, float, float) or tuple(str, str, str)
        """
        try:
            # Initial guess for the parameters
            initial_guess = [self.initialI0Kol, self.initialTau0Kol, self.initialBeta]
            # Curve fitting
            popt, pcov = curve_fit(self.kohl_decay, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0 and tau0
            I0_opt, tau0_opt, beta_opt = popt
            yFit=[]
            for i in xData:
                value=self.kohl_decay(i, I0_opt, tau0_opt,beta_opt)
                yFit.append(value)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=sqrt(pcov[0][0])
                tau_0Cov=sqrt(pcov[1][1])
                betaCov=sqrt(pcov[2][2])
                #Try to get the first parameter
                if I_0Cov>I0_opt:
                    self.FitCov[0]="nan"    
                    I_0CovString="nan"
                else:
                    I_0CovString=self.roundStringPCov(I_0Cov)
                    self.FitCov[0]=I_0CovString
                #Try to get the second parameter
                if tau_0Cov>tau0_opt:
                    self.FitCov[1]="nan"    
                    tau_0CovString="nan"
                else:
                    tau_0CovString=self.roundStringPCov(tau_0Cov)
                    self.FitCov[1]=tau_0CovString
                    
                #Try to get the third parameter
                
                if betaCov>beta_opt:
                    self.FitCov[2]="nan"    
                    betaCovString="nan"
                else:
                    betaCovString=self.roundStringPCov(betaCov)
                    self.FitCov[2]=betaCovString
            except:
                self.FitCov[0]="nan"
                self.FitCov[1]="nan"
                self.FitCov[2]="nan"
            #Graphic of the fit curve
            self.curveFit.setData(xData,yFit)
            if str(I0_opt)=='nan':
                self.curveFit.setData([],[])
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                r2Parameter=self.calculateR2(yData,yFit)
                self.R2=round(r2Parameter,3)
                maxRoundTau0=self.maxRound(I_0CovString)
                maxRoundI0=self.maxRound(tau_0CovString)
                maxRoundBeta=self.maxRound(betaCovString)
                #Change I0 parameter
                self.insertParameters(0,"I0",str(round(tau0_opt,maxRoundI0)),str(float(tau_0CovString)),"")
                #Change tau0 parameter
                self.insertParameters(1,"τ0",str(round(I0_opt,maxRoundTau0)),str(float(I_0CovString)),self.units)
                #Change Beta parameter
                self.insertParameters(2,"β",str(round(beta_opt,maxRoundBeta)),str(float(betaCovString)),"")
                #Change R^2 parameter
                self.insertParameters(3,"R^2",str(self.R2),"","")
            return I0_opt, tau0_opt, beta_opt
        except:
            self.curveFit.setData([],[])
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()  
            return "Undefined","Undefined","Undefined"
    #Initial Parameters Dialog
    def initialParametersDialog(self):
        """
        Displays a dialog for selecting initial parameters for fitting functions.

        This dialog allows the user to select a type of fitting function and input the corresponding parameters.
        The parameters that can be set include:
        - I0 (initial value)
        - tau0 (decay constant)
        - beta (for Kohlrausch fit)
        - alpha (for Shifted Exponential fit)
        - b (for Shifted Exponential fit)
        
        The dialog contains a ComboBox to select the function type, and the input fields dynamically update based on
        the selected function. It includes "Apply" and "Reset" buttons to apply changes or revert to default values.

        Variables assignment:
        - The input values from the dialog are assigned to respective attributes, but are not directly returned.

        :return: None
        """
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
        """
        Updates the initial parameters based on user input from the parameter dialog.

        This function is called when the user clicks the "Apply" button in the parameter dialog. 
        It retrieves the values from the input fields corresponding to the selected fitting function 
        and assigns them to the appropriate instance variables. 

        The following parameters are updated based on the selected fit type:
        - For Exponential fit:
        - I0 (initial value)
        - tau0 (decay constant)
        - For Kohlrausch fit:
        - I0 (initial value)
        - tau0 (decay constant)
        - beta (exponent)
        - For Shifted Exponential fit:
        - I0 (initial value)
        - tau0 (decay constant)
        - alpha (shift parameter)
        - b (baseline value)
        - For Double Exponential fit:
        - I0 (initial value)
        - tau0 (first decay constant)
        - tau1 (second decay constant)
        - alpha (mixing coefficient)

        Variables assignment:
        - The updated values are assigned to their respective initial parameter variables.
        - A boolean flag indicating that initial parameters have changed is set to True for the relevant fit type.

        :return: None
        """
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
        """
        Resets the initial parameters in the dialog based on the measured data.

        This function is called when the user clicks the "Default Values" button in the parameter dialog. 
        It resets the initial parameters to sensible defaults derived from the measured data. 
        The following resets occur based on the selected fitting function:
        
        - For Exponential fit:
            - I0 is set to the maximum value of measured data.
            - tau0 is set to the mean of measured time.
        - For Kohlrausch fit:
            - I0 is set to the maximum value of measured data.
            - tau0 is set to the mean of measured time.
            - beta is set to 1.0 (default value).
        - For Shifted Exponential fit:
            - I0 is set to the maximum value of measured data.
            - tau0 is set to the mean of measured time.
            - alpha is set to 0 (default value).
            - b is set to 0 (default value).
        - For Double Exponential fit:
            - I0 is set to the maximum value of measured data.
            - tau0 is set to the mean of measured time.
            - alpha is set to 0 (default value).
            - tau1 is set to the mean of measured time.

        The corresponding input fields in the dialog are updated with these new values. 
        Flags indicating that the initial parameters have not changed are also reset to False for the relevant fit type.

        :return: None
        """
        if len(self.measuredData)>0:
            if self.combo_box.currentText()=="Exponential fit":
                self.initialI0=max(self.measuredData)
                self.initialTau0=mean(self.measuredTime)
                self.I_0_field.setValue(self.initialI0)
                self.Tau_0_field.setValue(self.initialTau0)
                self.changeInitialParametersExp=False
            elif self.combo_box.currentText()=="Kohlrausch fit":
                self.initialI0Kol=max(self.measuredData)
                self.initialTau0Kol=mean(self.measuredTime)
                self.initialBeta=1.0
                self.Beta_field.setValue(self.initialBeta)
                self.I_0_field.setValue(self.initialI0Kol)
                self.Tau_0_field.setValue(self.initialTau0Kol)
                self.changeInitialParametersKol=False
            elif self.combo_box.currentText()=="Shifted Exponential fit":
                self.initialI0Shif=max(self.measuredData)
                self.initialTau0Shif=mean(self.measuredTime)
                self.initialAlpha=0
                self.initialB=0
                self.I_0_field.setValue(self.initialI0Shif)
                self.Tau_0_field.setValue(self.initialTau0Shif)
                self.Alpha_field.setValue(self.initialAlpha)
                self.B_field.setValue(self.initialB)
                self.changeInitialParametersShif=False
            elif self.combo_box.currentText()=="Double Exponential fit":
                self.initialI0Doub=max(self.measuredData)
                self.initialTau0Doub=mean(self.measuredTime)
                self.initialAlphaDoub=0
                self.initialTau1Doub=mean(self.measuredTime)
                self.I_0_field.setValue(self.initialI0Doub)
                self.Tau_0_field.setValue(self.initialTau0Doub)
                self.Alpha_field.setValue(self.initialTau1Doub)
                self.B_field.setValue(self.initialAlphaDoub)
                self.changeInitialParametersDoub=False
        

    
    #fit Shifted Exponential
    def fitShiiftedExponential(self, xData, yData):
        """
        Fits a shifted exponential decay model to the provided data.

        This function fits a shifted exponential decay model to the given `xData` and `yData` using the initial guesses for 
        the parameters (I0, tau0, alpha, b). If the fit is successful, it updates the corresponding values for each parameter 
        and plots the fitted curve. If the fit fails, a warning message is displayed to the user.

        Variables assignment:
        - `self.FitCov`: Stores the covariance values for I0, tau0, alpha, and b, or "nan" if not calculable.
        - `self.xDataFitCopy`: Stores a copy of the `xData` for the fitted curve.
        - `self.yDataFitCopy`: Stores the computed y-values for the fitted curve.
        - `self.R2`: Stores the calculated R² value for the fit.
        - `self.curveFit`: Updates the plot with the fitted curve data.

        :param xData: The x-axis data points (array-like).
        :param yData: The y-axis data points (array-like).
        :return: Tuple (I0_opt, tau0_opt, alpha_opt, b_opt) containing the fitted values of I0, tau0, alpha, and b, or 
                ("Undefined", "Undefined", "Undefined", "Undefined") if fitting fails.
        :rtype: tuple(float, float, float, float) or tuple(str, str, str, str)
        """
        try:
            # Initial guess for the parameters: I0, tau0, alpha, b
            initial_guess = [self.initialI0Shif, self.initialTau0Shif, self.initialAlpha, self.initialB]
            # Curve fitting
            popt, pcov = curve_fit(self.shifted_decay_function, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0, tau0, alpha, and b
            I0_opt, tau0_opt, alpha_opt, b_opt = popt
            # Calculate the fitted curve
            yFit=[]
            for i in xData:
                value=self.shifted_decay_function(i, I0_opt, tau0_opt, alpha_opt, b_opt)
                yFit.append(value)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=sqrt(pcov[0][0])
                tau_0Cov=sqrt(pcov[1][1])
                alphaCov=sqrt(pcov[2][2])
                bCov=sqrt(pcov[3][3])
                
                #Get I0 parameter
                if I_0Cov>I0_opt:
                    self.FitCov[0]="nan"
                    I_0CovString="nan"
                else:
                    I_0CovString=self.roundStringPCov(I_0Cov)
                    self.FitCov[0]=I_0CovString
        
                #Get tau parameter
                if tau_0Cov>tau0_opt:
                    self.FitCov[1]="nan"
                    tau_0CovString="nan"
                else:
                    tau_0CovString=self.roundStringPCov(tau_0Cov)
                    self.FitCov[1]=tau_0CovString
               
               #Get alpha parameter
                if alphaCov>alpha_opt:
                    self.FitCov[2]="nan"
                    alphaCovString="nan"
                else:
                    alphaCovString=self.roundStringPCov(alphaCov)
                    self.FitCov[2]=alphaCovString
                
                
                #Get b parameter
                if bCov>b_opt:
                    self.FitCov[3]="nan"
                    bCovString="nan"
                else:
                    bCovString=self.roundStringPCov(bCov)
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
                self.curveFit.setData([],[])
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                r2Parameter=self.calculateR2(yData,yFit)
                self.R2=round(r2Parameter,3)
                maxRoundTau0=self.maxRound(I_0CovString)
                maxRoundI0=self.maxRound(tau_0CovString)
                maxRoundAlpha=self.maxRound(alphaCovString)
                maxRoundB=self.maxRound(bCovString)
                #Change I0 parameter
                self.insertParameters(0,"I0",str(round(I0_opt, maxRoundTau0)),str(float(I_0CovString)),"")
                #Change tau0 parameter
                self.insertParameters(1,"τ0",str(round(tau0_opt, maxRoundI0)),str(float(tau_0CovString)),self.units)
                #Change alpha parameter
                self.insertParameters(2,"α",str(round(alpha_opt, maxRoundAlpha)),str(float(alphaCovString)),"")
                #Change b parameter
                self.insertParameters(3,"b",str(round(b_opt, maxRoundB)),str(float(bCovString)),"")
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")

            return I0_opt, tau0_opt, alpha_opt, b_opt
        except:
            self.curveFit.setData([],[])
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined","Undefined","Undefined"
    
    
    #fit Double exponential
    def fitDoubleExponential(self, xData, yData):
        """
        Fits a double exponential decay model to the provided data.

        This function fits a double exponential decay model to the given `xData` and `yData` using the initial guesses for 
        the parameters (I0, tau0, tau1, alpha). If the fit is successful, it updates the corresponding values for each 
        parameter and plots the fitted curve. If the fit fails, a warning message is displayed to the user.

        Variables assignment:
        - `self.FitCov`: Stores the covariance values for I0, tau0, tau1, and alpha, or "nan" if not calculable.
        - `self.xDataFitCopy`: Stores a copy of the `xData` for the fitted curve.
        - `self.yDataFitCopy`: Stores the computed y-values for the fitted curve.
        - `self.R2`: Stores the calculated R² value for the fit.
        - `self.curveFit`: Updates the plot with the fitted curve data.

        :param xData: The x-axis data points (array-like).
        :param yData: The y-axis data points (array-like).
        :return: Tuple (I0_opt, tau0_opt, tau1_opt, alpha_opt) containing the fitted values of I0, tau0, tau1, and alpha, 
                or ("Undefined", "Undefined", "Undefined", "Undefined") if fitting fails.
        :rtype: tuple(float, float, float, float) or tuple(str, str, str, str)
        """
        try:
            # Initial guess for the parameters: I0, tau0, alpha, b
            initial_guess = [self.initialI0Doub, self.initialTau0Doub, self.initialTau1Doub, self.initialAlphaDoub]
            # Curve fitting
            popt, pcov = curve_fit(self.double_Exponential, xData, yData, p0=initial_guess)
            # Extracting the optimal values of I0, tau0, alpha, and b
            I0_opt, tau0_opt, tau1_opt, alpha_opt = popt
            # Calculate the fitted curve
            yFit=[]
            for i in xData:
                value=self.double_Exponential(i, I0_opt, tau0_opt, tau1_opt, alpha_opt)
                yFit.append(value)
            self.xDataFitCopy=xData
            self.yDataFitCopy=yFit
            try:
                I_0Cov=sqrt(pcov[0][0])
                tau_0Cov=sqrt(pcov[1][1])
                tau_1Cov=sqrt(pcov[2][2])
                alphaCov=sqrt(pcov[3][3])
                
                #Get I0 parameter
                if I_0Cov>I0_opt:
                    self.FitCov[0]="nan"
                    I_0CovString="nan"
                else:
                    I_0CovString=self.roundStringPCov(I_0Cov)
                    self.FitCov[0]=I_0CovString
        
                #Get tau parameter
                if tau_0Cov>tau0_opt:
                    self.FitCov[1]="nan"
                    tau_0CovString="nan"
                else:
                    tau_0CovString=self.roundStringPCov(tau_0Cov)
                    self.FitCov[1]=tau_0CovString
               
               #Get tau1 parameter
                if tau_1Cov>tau1_opt:
                    self.FitCov[2]="nan"
                    tau_1CovString="nan"
                else:
                    tau_1CovString=self.roundStringPCov(tau_1Cov)
                    self.FitCov[2]=tau_1CovString
                
                
                #Get alpha parameter
                if alphaCov>alpha_opt:
                    self.FitCov[3]="nan"
                    alphaCovString="nan"
                else:
                    alphaCovString=self.roundStringPCov(alphaCov)
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
                self.curveFit.setData([],[])
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("The parameters for the graph could not be determined.")
                message_box.setWindowTitle("Error generating the fit")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            else:
                r2Parameter=self.calculateR2(yData,yFit)
                self.R2=round(r2Parameter,3)
                maxRoundTau0=self.maxRound(I_0CovString)
                maxRoundI0=self.maxRound(tau_0CovString)
                maxRoundTau1=self.maxRound(tau_1CovString)
                maxRoundalpha=self.maxRound(alphaCovString)
                #Change I0 parameter
                self.insertParameters(0,"I0",str(round(I0_opt, maxRoundTau0)),str(float(I_0CovString)),"")
                #Change tau0 parameter
                self.insertParameters(1,"τ0",str(round(tau0_opt, maxRoundI0)),str(float(tau_0CovString)),self.units)
                #Change alpha parameter
                self.insertParameters(2,"τ1",str(round(tau1_opt, maxRoundTau1)),str(float(tau_1CovString)),self.units)
                #Change b parameter
                self.insertParameters(3,"α",str(round(alpha_opt, maxRoundalpha)),str(float(alphaCovString)),"")
                #Change R^2 parameter
                self.insertParameters(4,"R^2",str(self.R2),"","")
            return I0_opt, tau0_opt, tau1_opt, alpha_opt
        except:
            self.curveFit.setData([],[])
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("The parameters for the graph could not be determined.")
            message_box.setWindowTitle("Error generating the fit")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return "Undefined","Undefined","Undefined","Undefined"
        
    
    
        
        
        
    #Exponential Decay Function
    def exp_decay(self,t, I0, tau0):
        """
        Computes the value of an exponential decay function.

        This function calculates the value of the exponential decay function using the given parameters for time `t`, 
        initial value `I0`, and decay constant `tau0`.

        Variables assignment:
        - The computed value is returned directly and not assigned to any variable within the function.

        :param t: The time at which to evaluate the function (float).
        :param I0: The initial value of the exponential function (float).
        :param tau0: The decay constant (float).
        :return: The value of the exponential decay function at time `t`.
        :rtype: float
        """
        return I0 * exp(-t / tau0)

    #Kohlrausch Decay Function
    def kohl_decay(self,t, I0, tau0,beta):
        """
        Computes the value of a Kohlrausch (stretched exponential) decay function.

        This function calculates the value of the stretched exponential (Kohlrausch) decay function using the given parameters: 
        time `t`, initial value `I0`, decay constant `tau0`, and stretching parameter `beta`.

        Variables assignment:
        - The computed value is returned directly and not assigned to any variable within the function.

        :param t: The time at which to evaluate the function (float).
        :param I0: The initial value of the exponential function (float).
        :param tau0: The decay constant (float).
        :param beta: The stretching exponent, controlling the deviation from a simple exponential decay (float).
        :return: The value of the stretched exponential decay function at time `t`.
        :rtype: float
        """
        return I0 * exp((-t / tau0)**beta)
    
    #Shifted Exponential Function
    def shifted_decay_function(self, t, I0, tau0, alpha, b):
        """
        Computes the value of a shifted exponential decay function.

        This function calculates the value of a shifted exponential decay function using the given parameters: 
        time `t`, initial value `I0`, decay constant `tau0`, shift parameter `alpha`, and constant offset `b`.

        Variables assignment:
        - The computed value is returned directly and not assigned to any variable within the function.

        :param t: The time at which to evaluate the function (float).
        :param I0: The initial value of the exponential function (float).
        :param tau0: The decay constant (float).
        :param alpha: The shift parameter, determining the horizontal shift of the decay function (float).
        :param b: The constant offset added to the decay function (float).
        :return: The value of the shifted exponential decay function at time `t`.
        :rtype: float
        """
        # Define the decay function with the new equation
        return I0 * exp(-(t - alpha) / tau0) + b
    #Double Exponential Function
    def double_Exponential(self,t, I0, tau0, tau1, alpha): 
        """
        Computes the value of a double exponential decay function.

        This function calculates the value of a double exponential decay function using the given parameters: 
        time `t`, initial value `I0`, decay constants `tau0` and `tau1`, and mixing parameter `alpha`.

        Variables assignment:
        - The computed value is returned directly and not assigned to any variable within the function.

        :param t: The time at which to evaluate the function (float).
        :param I0: The initial value of the exponential function (float).
        :param tau0: The first decay constant (float).
        :param tau1: The second decay constant (float).
        :param alpha: The mixing parameter that determines the contribution of the first decay (float).
        :return: The value of the double exponential decay function at time `t`.
        :rtype: float
        """
        return I0*(alpha*exp(-t/tau0)+(1-alpha)*exp(-t/tau1))

    #Function to get the maximum number of decimal numbers from sd (Standard Deviation)
    
    def maxRound(self,string):
        """
        Determines the number of decimal places needed for at least three significant figures.

        :param string: The number as a string (str).
        :return: Number of decimal places (int).
        """
        try:
            num = float(string)
            
            if '.' not in string and 'e' not in string:
                return 3
            
            parts = re.split('[eE]', string)
            base = parts[0]
            if '.' in base:
                base_decimals = len(base.split('.')[1])
            else:
                base_decimals = 0
            if len(parts) > 1:
                exponent = int(parts[1])
                total_decimals = max(0, base_decimals - exponent)
            else:
                total_decimals = base_decimals
            
            return total_decimals
        except:
            return 3
    

    #Function to get the string of the pcov numbers
    
    def roundStringPCov(self, number):
        """
        Converts a number to a string representation in scientific notation with two decimal places.

        :param number: The input number (float).
        :return: String representation in scientific notation (str).
        """
        if number == 0:
            return "0.00"
        exponent = int(math.floor(math.log10(abs(number))))
        rounded_number = round(number / (10 ** exponent), 2)
        if exponent != 0:
            return f"{rounded_number:.2f}e{exponent:+d}"
        else:
            return f"{rounded_number:.2f}"
    
    #Function to calculate the parameter R^2

    def calculateR2(self,data,fitData):
        """
        Calculates the R² value based on the observed and fitted data.

        :param data: The observed data points (array-like).
        :param fitData: The fitted data points (array-like).
        :return: The R² value indicating the goodness of fit (float).
        """
        #Get the array
        arrayData=array(data)
        arrayFit=array(fitData)
        #Mean data
        meanData=mean(arrayData)
        #Get the residue
        ssRes=sum((arrayData-arrayFit)**2)
        #Get the total sum squared
        ssTot=sum((arrayData-meanData)**2)
        #Get R^2
        R2=1-(ssRes/ssTot)
        return R2

        
    
    #Save buttons
    #Save Plot Button
    def savePlotLifeTime(self):
        """
        Saves the graph image in the specified format (PNG, TIFF, or JPG) based on the user's selection.
        :return: None
        """
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
                copyPlot.getViewBox().setState(self.plotLifeTime.getViewBox().getState())
                exporter=ImageExporter(copyWin.scene())
                exporter.parameters()['width'] = 1000
                exporter.parameters()['height'] = 700
                folder_path=self.savefile.read_default_data()['Folder path'].replace('\n', '')
                current_date=datetime.datetime.now()
                current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                graph_name='LifeTimeMeasurement'+current_date_str
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
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
    #Save Data Button
    def saveLifeTimeData(self):
        """
        Saves the data in the selected format (TXT, CSV, or DAT) based on the user's choice.

        :return: None
        """
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
            folder_path=self.savefile.read_default_data()['Folder path']
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
                filename="LifeTimeMeasurement"+current_date_str
                #Round the values in order to get a better txt files
                newMeasuredTime=[]
                for i in self.measuredTime:
                    newValue=round(i,5)
                    newMeasuredTime.append(newValue)
                data=[newMeasuredTime,self.measuredData ]
                try:
                    self.savefile.save_LifeTime_data(data,filename,folder_path,fitSetting,selected_format, self.unitsLabel)
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
                except:
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
class WorkerThreadLifeTime(QThread):
    """
    Worker thread for handling LifeTime (Fluorescence Lifetime Measurement) processing in a separate thread 
    to ensure that the GUI remains responsive during measurements.

    This class performs the measurement tasks in the background, processes the data, and communicates with 
    the main thread to update the GUI with the measurement status, results, and other relevant information.
    
    Signals:
        - createdSignal: Signal emitted when the worker thread is created.
        - statusSignal: Signal emitted to update the status message in the GUI.
        - pointSignal: Signal emitted to update the current measurement point.
        - updateValues: Signal emitted to update measurement values and corresponding times.
        - updateLabel: Signal emitted to update a specific label in the GUI.
        - updateMeasurementsLabel: Signal emitted to update the label showing the number of measurements taken.

    :param deviceStartChannel: The start channel of the Tempico device used for measurement (TempicoChannel).
    :param deviceStopChannel: The stop channel of the Tempico device used for measurement (TempicoChannel).
    :param binwidthText: The selected bin width for the measurement (str).
    :param numberMeasurements: The number of measurements to be taken (int).
    :param device: The Tempico device used for performing measurements (Tempico).
    :param TimeRange: The time range for the measurements (int).
    :return: None
    """
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
        """
        Runs the measurement thread, continuously taking measurements based on user-selected values
        and passing them to the graphs.

        :return: None
        """
        
        self.createdSignal.emit()
        while self.totalMeasurements<self.numberMeasurements and self._is_running:
            
            percentage=round((self.totalMeasurements*100)/self.numberMeasurements,2)
            self.checkDeviceStatus()
            #Try in order to avoid the errors related to suddenly disconnect the device
            self.checkDeviceStatus()
            try:
                self.takeMeasurements(percentage)
                self.createLifeTimeData()
            except:
                pass
            
    #Functon to define the mode of the measurement
    def measurementMode(self):
        """
        Sets the measurement mode for the device channels based on the specified time range.

        If the time range is less than or equal to 500000 ps , sets all channels to mode 1.
        Otherwise, sets all channels to mode 2.

        :param self: The instance of the class.
        :return: None
        """
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
        
        self.device.ch1.setMode(2)
        self.device.ch2.setMode(2)
        self.device.ch3.setMode(2)
        self.device.ch4.setMode(2)
        
    #Take one measurement function
    def takeMeasurements(self, percentage):
        """
        Takes measurements from the device and updates the start-stop differences list.

        Configures the device for measurement runs and checks the input and stop channels for data.
        If no measurements are detected, emits a status signal to update the main thread about the current measurement state.

        :param percentage: The percentage of measurement completion (float).
        :return: None
        """
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
                            self.totalMeasurements+=1
                            self.totalTime+=differenceValue
                            if abs(differenceValue)<=self.TimeRange:
                                self.noMeasurementsCounter=0
                                self.startStopDifferences.append(differenceValue)
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
    def createLifeTimeData(self):
        """
        Generates LifeTime data from the start-stop differences and emits the calculated results to the main thread.

        Processes the collected data to determine the number of counts within a given time based on the maximum value of start-stop differences.
        Normalizes the data according to the determined units and calculates the histogram counts.

        :return: None
        """
        if len(self.startStopDifferences)>0:
            maximumValue=max(self.startStopDifferences)
            minimunValue=min(self.startStopDifferences)
            if abs(maximumValue)>abs(minimunValue) and minimunValue<0:
                maximumValue=self.TimeRange
                minimunValue=-self.TimeRange
            elif abs(maximumValue)<=abs(minimunValue) and minimunValue<0:
                maximumValue=-self.TimeRange
                minimunValue=self.TimeRange
            elif minimunValue>0:
                maximumValue=self.TimeRange
                minimunValue=0
            
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
            domainValues=arange(minimunValue/divisionFactor,maximumValue/divisionFactor+newBinWidth,newBinWidth)
            bin_edges = appnd(domainValues - newBinWidth / 2, domainValues[-1] + newBinWidth / 2)
            counts,_ = histogram(newDifferences, bins=bin_edges)
            self.updateValues.emit(counts,domainValues)
            self.updateLabel.emit(units)
        self.updateMeasurementsLabel.emit(str(self.totalMeasurements),str(self.totalStarts))
            
    #Function to get the scale in time of the histogram
    def getUnits(self,picosecondsValue):
        """
        Determines the appropriate units for a given value in picoseconds.

        Converts a given value in picoseconds to the most suitable time unit (picoseconds, nanoseconds, microseconds, or milliseconds).

        :param picosecondsValue: The value in picoseconds (float).
        :return: A list containing the unit as a string and the factor by which to divide the value (list).
        """
        if picosecondsValue < 1e3:
            return ["ps",1]
        elif picosecondsValue < 1e6:
            return ["ns",10**3]
        elif picosecondsValue < 1e9:
            return ["µs",10**6]
        elif picosecondsValue < 1e12:
            return ["ms",10**9]
        
    def getBinWidthNumber(self):
        """
        Calculates the bin width in picoseconds based on user input in different units.

        Extracts the numerical value and its corresponding unit from the user-provided text,
        and converts it into picoseconds for further calculations.

        :return: None
        """
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
        """
        Clears the recorded start-stop differences and resets the total measurement count.

        This function empties the list that stores the differences between start and stop measurements,
        and sets the total number of measurements back to zero.

        :return: None
        """
        self.startStopDifferences=[]
        self.totalMeasurements=0
    
    #Check the connection of the device
    def checkDeviceStatus(self):
        """
        Checks the status of the device by attempting to read a parameter.

        If an error occurs during the read operation, the measurement process is stopped.

        :return: None
        """
        try:
            self.device.readIdnFromDevice()
        except:
            self.stop()
    
    #Stop thread function
    @Slot()
    def stop(self):
        """
        Stops the measurement process by setting the running flag to False.

        Emits a status message indicating that the measurement is ending and updates the status bar color to yellow.

        :return: None
        """
        self._is_running=False
        self.statusSignal.emit("Ending measurement")
        self.pointSignal.emit(2)
    
    
        
        
    
    
    