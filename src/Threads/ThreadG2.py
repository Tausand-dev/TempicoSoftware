import pyTempico as tempico
from PySide2.QtCore import QThread, Signal
import pyTempico as tempico
import numpy as np
from Utils.constants import *
class WorkerThreadG2(QThread):
    """
    Worker thread for handling g² (second-order correlation) measurements in a separate thread 
    to ensure that the GUI remains responsive during data acquisition.

    This class is responsible for running the correlation measurement in the background using 
    the Tempico device. It collects start-stop events, builds and normalizes the g² histogram, 
    estimates parameters such as counts per second, and communicates results and status updates 
    back to the GUI via signals.

    Signals:
        - updateMeasurement: Signal emitted to update the g² histogram, total starts, and total stops (list, int, int).
        - updateTauValues: Signal emitted to update tau values along with the total starts and stops (list, int, int).
        - updateStatusLabel: Signal emitted to update the measurement status message in the GUI (str).
        - updateColorLabel: Signal emitted to update the color indicator of the status label (int).
        - updateEstimatedParameter: Signal emitted to update the current estimated counts per second (str).
        - updateDeterminedParameters: Signal emitted when determined parameters are ready to be updated.
        - updateFirstParameter: Signal emitted with the first calculated parameter for display (str).

    :param stopChannel: The stop channel selected for the measurement ("A", "B", "C", or "D") (str).
    :param maximumTime: The maximum measurement time range (float, in picoseconds).
    :param numberBins: The number of bins used for building the histogram (int).
    :param coincidenceWindow: The coincidence window size (float, in picoseconds).
    :param device: The Tempico device used for data acquisition (tempico.TempicoDevice).
    :param mode: The mode setting that defines measurement configuration (int or str depending on GUI settings).
    :param units: The time units selected for display and processing (str).
    :param limitedMeasurement: Whether the measurement is limited to a fixed number of acquisitions (bool, default=False).
    :param numberOfMeasurements: The number of measurements when in limited mode (int, default=0).
    :param autoclearMeasure: Whether the measurement should periodically auto-clear accumulated histograms (bool, default=False).
    """
    updateMeasurement=Signal(list, int, int)
    updateTauValues=Signal(list,int,int)
    updateStatusLabel=Signal(str)
    updateColorLabel=Signal(int)
    updateEstimatedParameter=Signal(str)
    updateDeterminedParameters=Signal()
    updateFirstParameter=Signal(str)
    cannotEstimate=Signal()
    def __init__(self, stopChannel: str, maximumTime: float, numberBins:int, coincidenceWindow: float, device: tempico.TempicoDevice, 
                 mode,units,limitedMeasurement=False,numberOfMeasurements=0,autoclearMeasure=False):
        super().__init__()
        self.totalStarts=0
        self.totalStops=0
        self.running=True
        self.stopChannel=stopChannel
        self.maximumTime=maximumTime
        self.maximumTimeSeconds=self.psToS(maximumTime)
        self.modeSettings=mode
        self.units=units
        self.cumulatedEstimatedParameter=0
        self.totalEstimatedParameter=0
        self.numberBins=numberBins
        self.coincidenceWindow=self.psToS(coincidenceWindow)
        self.isLimitedMeasurement=limitedMeasurement
        self.numberMeasurements=numberOfMeasurements
        self.autoclearMeasure=autoclearMeasure
        self.device=device
        self.totalTimeIntegration=0
        self.bins=self.generateBinList()
        self.divisionFactor=self.getDivisionFactor()
        self.TauValues = (0.5 * (self.bins[:-1] + self.bins[1:])/self.divisionFactor)
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.baseg2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.saveSettings()
        self.settingsForEstimate()
        
    
    def run(self):
        self.estimatedParameter=self.estimatedParameterValue()
        if self.estimatedParameter==-1 and self.running:
            self.running=False
        elif self.estimatedParameter!=-1 and self.running:
            self.cumulatedEstimatedParameter+=self.estimatedParameter
            self.totalEstimatedParameter+=1
            if not self.autoclearMeasure:
                self.updateEstimatedParameter.emit(str(int(self.estimatedParameter)))
            else:
                self.updateFirstParameter.emit(str(int(self.estimatedParameter)))
            self.updateDeterminedParameters.emit()
            self.updateTauValues.emit(self.TauValues,self.divisionFactor,self.modeSettings)
        self.settingsForMeasurement()
        self.updateStatusLabel.emit("Running measurement")
        self.updateColorLabel.emit(1)
        while self.running:
            self.getMeasurement()
        self.recoverSettings()
    
    def getDivisionFactor(self):
        """
        Returns the normalization factor based on the selected time unit.

        :return: Factor for unit conversion (int).
        """
        factor=1
        if self.units=="ns":
            factor=10**3
        elif self.units=="us":
            factor=10**6
        elif self.units=="ms":
            factor=10**9
        return factor
            
    
    def settingsForEstimate(self):
        """
        Configures the device to estimate the photon arrival rate on the selected stop channel.

        The function sets the device to perform a single run, disables all channels,
        and then enables only the selected stop channel (A–D).  
        For the chosen channel, it configures the acquisition mode, stop mask, average cycles,  
        and ensures that two stop events are captured for pulse estimation.

        :return: None
        """
        self.device.setNumberOfRuns(1)
        self.device.disableChannel(1)
        self.device.disableChannel(2)
        self.device.disableChannel(3)
        self.device.disableChannel(4)
        if self.stopChannel=="A":
            self.device.enableChannel(1)
            self.device.setAverageCycles(1,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(1,2)
        elif self.stopChannel=="B":
            self.device.enableChannel(2)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(2,2)
        elif self.stopChannel=="C":
            self.device.enableChannel(3)
            self.device.setAverageCycles(3,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(3,2)
        elif self.stopChannel=="D":
            self.device.enableChannel(4)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(4,2)
    
    def settingsForMeasurement(self):
        """
        Applies the configuration required to perform the g² measurement.

        It sets the device to run 100 acquisitions, assigns one stop channel 
        (A–D), and configures its acquisition mode according to `self.modeSettings`.

        :return: None
        """
        self.device.setNumberOfRuns(100)
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,1)
            self.device.setMode(1,self.modeSettings)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,1)
            self.device.setMode(2,self.modeSettings)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,1)
            self.device.setMode(3,self.modeSettings)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,1)
            self.device.setMode(4,self.modeSettings)
    
    def settingsForEstimatedParameters(self):
        """
        Applies minimal configuration to the device for parameter estimation.

        Unlike the initial setup, this function only sets the number of stops 
        for the selected stop channel (A–D) and configures the acquisition mode.  
        It assumes that the general configuration has already been applied.

        :return: None
        """
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,2)
            self.device.setMode(1,2)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,2)
            self.device.setMode(1,2)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,2)
            self.device.setMode(1,2)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,2)
            self.device.setMode(1,2)
        
        
        
    def saveSettings(self):
        """
        Saves the current configuration of the device into instance variables.

        This includes number of runs, number of stops, stop masks, average cycles, 
        and acquisition modes for each channel (A–D).

        :return: None
        """
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
        """
        Restores the previously saved configuration to the device.

        This re-enables all channels (A–D) and applies the saved values for 
        number of runs, number of stops, stop masks, average cycles, 
        and acquisition modes.

        :return: None
        """
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
        """
        Estimates an initial parameter value based on device measurements.

        The method configures the device for estimation, collects up to 100 
        measurements, and computes the time differences between stop channels. 
        Progress updates are emitted through `updateStatusLabel` and 
        `updateColorLabel`. If too many measurements are invalid or no start 
        signals are detected, the function returns -1.

        :return: Estimated parameter value (float) or -1 if estimation fails.
        """
        self.settingsForEstimatedParameters()
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
        """
        Performs a measurement cycle to obtain data for g2 analysis.

        The method applies measurement settings, collects runs from the device, 
        processes stop events, and builds a g2 histogram from the detected time 
        differences. It also estimates an auxiliary parameter from stop differences 
        and updates status/measurement signals accordingly.

        If there are too many missing start events or stops, error messages are 
        emitted. Otherwise, the g2 values and estimated parameters are updated 
        in real time.

        :return: None
        """
        self.settingsForMeasurement()
        measurement = self.device.measure()
        totalStopPerMeasurement=0
        timeDifferences, stopDifferences = [], []
        notStartsMeasurement=0
        for run in measurement:
            if not run:
                notStartsMeasurement+=1
                continue
            totalStopPerMeasurement+=self.processRun(run, timeDifferences)
            if self.isLimitedMeasurement and self.totalStops>=self.numberMeasurements:
                self.updateDeterminedParameters.emit()
                self.running=False
                break
        stopDifferences=self.estimateParameterInMeasurement()
        if self.totalTimeIntegration>0:
            g2Values=self.buildG2Histogram(timeDifferences)
            self.updateMeasurement.emit(g2Values, self.totalStarts,self.totalStops)
        else:
            self.updateMeasurement.emit(self.g2Histogram, self.totalStarts,self.totalStops)
        if stopDifferences:
            self.cumulatedEstimatedParameter+=self.getCountPerSecondParameter(stopDifferences)
            self.totalEstimatedParameter+=1
            self.estimatedParameter=self.cumulatedEstimatedParameter/self.totalEstimatedParameter
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
            
    def estimateParameterInMeasurement(self):
        """
        Estimates differences between stop signals during a measurement.

        The method applies the settings for estimated parameters, performs a device
        measurement, and calculates the time difference between two stop channels 
        when valid data is detected.

        :return: A list of time differences between stop signals (list).
        """
        self.settingsForEstimatedParameters()
        estimatedDifferences=[]
        measure=self.device.measure()
        for run in measure:
            if not run:
                continue
            if len(run)==5:
                stop1=run[3]
                stop2=run[4]
                differenceEstimated=stop2-stop1
                estimatedDifferences.append(differenceEstimated)
        return estimatedDifferences
            
            
    
    
    def processRun(self, run, timeDifferences):
        """
        Processes a single run from the Tempico measurement.

        Adds stop values to the list of time differences if valid, updates the 
        total number of starts, stops, and the total integration time.

        :param run: A single measurement run from the Tempico device (list).
        :param timeDifferences: List where valid stop times are appended (list).
        :return: 1 if the stop value is invalid (-1), otherwise 0 (int).
        """
        self.totalStarts += 1
        if run[3] == OVERFLOW_PARAMETER:
            return 1
        if run[3]<self.maximumTime:
            timeDifferences.append(run[3])
            self.totalStops += 1
        self.totalTimeIntegration += run[3]
        return 0

 
    def getCountPerSecondParameter(self,estimatedDifferences):
        """
        Calculates the counts per second parameter from stop differences.

        It computes the mean of the given stop time differences and converts it 
        into counts per second, assuming values are in picoseconds.

        :param estimatedDifferences: List of stop time differences (list).
        :return: Estimated counts per second, rounded to the nearest integer (float).
        """
        meanDifferences=np.mean(estimatedDifferences)
        estimatedValue= (10**(12))/meanDifferences
        return round(estimatedValue,0)

    
    def buildG2Histogram(self,timeDifferences):
        """
        Builds and normalizes the g2 histogram from time differences.

        It computes a histogram of the given time differences, accumulates the results 
        with previous data, and normalizes the values using the estimated counts per second, 
        the total integration time, and the coincidence window.

        :param timeDifferences: List of stop time differences from the measurement (list).
        :return: Normalized g2 histogram as a NumPy array (ndarray).
        """
        g2TemporalHistogram,_=np.histogram(timeDifferences, bins=self.bins)
        if len(g2TemporalHistogram)==0:
            g2TemporalHistogram=self.baseg2Histogram
        if len(self.g2Histogram)!=0:
            self.g2Histogram=self.g2Histogram+ g2TemporalHistogram
        else:
            self.g2Histogram=g2TemporalHistogram
        integrationTimeS=self.psToS(self.totalTimeIntegration)
        normalizedParameter=1/((self.estimatedParameter**2)*integrationTimeS*self.coincidenceWindow)
        histogramToEmit=self.g2Histogram*normalizedParameter
        return histogramToEmit
        
    
    
    def generateBinList(self):
        """
        Generates the list of histogram bins based on the selected mode and user-defined parameters.

        If mode 1 is selected, bins start from 12,500 ps.  
        If mode 2 is selected, bins start from 125,000 ps.  
        The bins extend up to the maximum time with the number of bins specified.

        :return: Array of bin edges for the histogram (ndarray).
        """
        if self.modeSettings==1:
            histogramToBuild=np.linspace(12500, self.maximumTime, self.numberBins + 1)
        elif self.modeSettings==2:
            histogramToBuild=np.linspace(125000, self.maximumTime, self.numberBins + 1)
        return histogramToBuild
    
    
    def getG2Average(self,g2Histogram):
        """
        Calculates the average value of the given g2 histogram.

        :param g2Histogram: Histogram values to average (ndarray or list).
        :return: Average value of the histogram (float).
        """
        valueSum=np.sum(g2Histogram)
        return valueSum/len(g2Histogram)
    
    def sortByStart(self, measurement):
        """
        Sorts the measurement runs based on the start value.

        :param measurement: List of measurement runs (list).
        :return: Sorted list of runs by the start value (list).
        """
        dataFiltered=[]
        for run in measurement:
            if run:
                dataFiltered.append(run)
        dataFiltered.sort(key=lambda x: x[2])
        return dataFiltered
    
    def changeToOneStop(self):
        """
        Sets the selected stop channel to use only one stop.

        :return: None
        """
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,1)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,1)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,1)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,1)
    
    def psToS(self,picoseconds):
        """
        Converts a value from picoseconds (ps) to seconds (s).

        :param picoseconds: Time value in picoseconds (int or float).
        :return: Converted value in seconds (float).
        """
        return picoseconds * 1e-12

    def clearG2(self):
        """
        Resets all g2 measurement values to start a new measurement.

        :return: None
        """
        self.totalTimeIntegration=0
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.totalStarts=0
        self.totalStops=0
        self.cumulatedEstimatedParameter=0
        self.totalEstimatedParameter=0
        
    
    def stop(self):
        """
        Stops the execution thread by changing the sentinel flag and 
        emitting the signal to terminate all processes related to the thread.

        :return: None
        """
        self.updateDeterminedParameters.emit()
        self.running=False