from PySide2.QtCore import QThread, Signal, Slot
from numpy import arange, histogram
from numpy import append as appnd
import Utils.constants as constants

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
    disconectedSignal=Signal()
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
                        sentinelStart=len(currentStartMeasurement)==4 and currentStartMeasurement[3]!=constants.OVERFLOW_PARAMETER
                        sentinelStop=len(currentStopMeasurement)==4 and currentStopMeasurement[3]!=constants.OVERFLOW_PARAMETER
                        if sentinelStart:
                            self.totalStarts+=1
                        if sentinelStart and sentinelStop:
                            if currentStopMeasurement[3]>=currentStartMeasurement[3]:
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
                            self.noMeasurementsCounter+=1
                        
                                
                    else:
                        currentStopMeasurement=measurement[i]
                        sentinelStop=len(currentStopMeasurement)==4 and currentStopMeasurement[3]>=0
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