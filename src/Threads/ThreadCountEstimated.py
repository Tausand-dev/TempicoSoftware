from PySide2.QtCore import QThread, Signal, Slot
from numpy import mean, sqrt, std
from datetime import datetime
import pyTempico as tempico
import time
import threading
import numpy as np
import Utils.constants as constants
class WorkerThreadCountsEstimated(QThread):
    """
    This class represents a worker thread that processes Start-Stop measurements in a separate thread
    to avoid blocking the main GUI thread. It handles data acquisition from the Tempico device,
    determines the feasibility of performing measurements per channel, and continuously collects
    and emits measurement data while running.

    The thread evaluates which channels meet the minimum requirements for valid measurements
    (e.g., at least 2 stops within a defined time window), disables those that do not, and allows
    the user to decide whether to proceed with the remaining ones.

    Signals are extensively used to communicate with the GUI, updating labels, graphs, and table data
    in real time, or notifying when no valid measurements are available.

    Additional attributes track the number of stop events per channel and enable synchronization
    with the main interface using a `threading.Event()` object.

    :param channelASentinel: Boolean indicating if Channel A is initially selected for measurement.
    :param channelBSentinel: Boolean indicating if Channel B is initially selected for measurement.
    :param channelCSentinel: Boolean indicating if Channel C is initially selected for measurement.
    :param channelDSentinel: Boolean indicating if Channel D is initially selected for measurement.
    :param device: The TempicoDevice instance used to perform the measurement operations.

    Signals:
        - newValue(str, float, float): Emitted with updated values for display (label updates).
        - updateLabel(str, float, float): Updates the label values for each channel.
        - newMeasurement(float, datetime, float, float, float, float, float, float, float, float): 
          Emitted with measurement timestamp, and count/uncertainty data for each channel.
        - noTotalMeasurements(): Emitted when none of the channels provide valid stop data.
        - noPartialMeasurements(list): Emitted with a list of channels that failed the threshold.
        - changeStatusText(str): Updates the system status label with a custom message.
        - changeStatusColor(int): Updates the system status label color code.
        - disconnectedDevice(): Emitted when the Tempico device is no longer reachable.
        - initialDate(str): Emitted with the starting timestamp of the measurement session.
        - finalDate(str): Emitted with the ending timestamp of the measurement session.

    Attributes:
        - channelsMeasure: List of channels accepted for measurement after validation.
        - channelsWithoutMeasurements: List of channels that failed the validation criteria.
        - continueEvent: Event object used to pause/resume thread logic when user interaction is needed.
        - running: Boolean flag to control the thread's main loop.
        - numberStopsChannelA/B/C/D: Internal counters to track stop events for each channel.

    :return: None
    """
    
    #One value is for the count estimated and the other is for the uncertainty
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
    initialDate=Signal(str)
    finalDate=Signal(str)
    
    
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
        """
        Executes the thread's main loop to perform count estimations from the Tempico device.

        First, it evaluates each selected channel to determine whether valid measurements can be 
        obtained. If a channel does not meet the required threshold, it is disabled and removed 
        from the measurement process. If at least one channel is valid, the measurement process begins.

        The loop runs continuously while the thread is active, triggering measurements every second. 
        If the device becomes unresponsive or the user stops the measurement, the thread exits.

        :return: None
        """
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

        elif self.channelsWithoutMeasurements and self.running:
            self.noPartialMeasurements.emit(self.channelsWithoutMeasurements)
            self.continueEvent.wait()
        if self.running:
            self.enableDisableChannels()
        if self.running:
            #Get the init time for measurement
            self.initialDate.emit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.initialMeasurementTime = time.time()
        while self.running:
            try:
                self.device.readIdnFromDevice()
            except:
                self.running=False
                self.disconnectedDevice.emit()
            if self.running:
                self.getMeasurements()
                time.sleep(1)
        self.finalDate.emit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            
        
    def getMeasurements(self):
        """
        Retrieves and processes the latest measurement data from the Tempico device.

        For each enabled channel, it verifies that the received data is valid, calculates 
        stop intervals based on the number of pulses received, and computes both the mean 
        and standard deviation of the intervals. These values represent the estimated count 
        and its uncertainty.

        If valid data is found, the results are emitted via a signal along with the timestamp 
        of the measurement. If no data is available, default values are emitted depending 
        on the state of each channel.

        :return: None
        """
        values=[]
        valuesB=[]
        valuesC=[]
        valuesD=[]
        measure=self.device.measure()
        if measure:
            if len(measure)!=0:
                for run in measure:
                    if self.channelASentinel:
                        if run:
                            if run[0]==1 and run[3]!=constants.OVERFLOW_PARAMETER :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelA)
                               
                                values=values+intervalValues
                    if self.channelBSentinel:
                        if run:
                            if run[0]==2 and run[3]!=constants.OVERFLOW_PARAMETER :
                                intervalValues=self.calculateIntervalWithStops(run,self.numberStopsChannelB)
                                valuesB=valuesB+intervalValues
                    
                    if self.channelCSentinel:
                        if run:
                            if run[0]==3 and run[3]!=constants.OVERFLOW_PARAMETER :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelC)
                                valuesC=valuesC+intervalValues
                    
                    if self.channelDSentinel:
                        if run:
                            if run[0]==4 and run[3]!=constants.OVERFLOW_PARAMETER :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelD)
                                valuesD=valuesD+intervalValues
        if len(values)>0:
            meanValue=(10**12)/mean(values)
            desvestValues=std(values)/sqrt(len(values))
            meanValuePs=mean(values)
            if desvestValues == 0:
                uncertaintyValue = 0
            else:
                uncertaintyValue = (desvestValues / (meanValuePs ** 2))* 1e12
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
            meanValueB=(10**12)/mean(valuesB)
            desvestValuesB=std(valuesB)/sqrt(len(valuesB))
            meanValueBPs=mean(valuesB)
            if desvestValuesB == 0:
                uncertaintyValueB = 0
            else:
                uncertaintyValueB = (desvestValuesB / (meanValueBPs ** 2))* 1e12
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
            meanValueC=(10**12)/mean(valuesC)
            desvestValuesC=std(valuesC)/sqrt(len(valuesC))
            meanValuesCPs=mean(valuesC)
            if desvestValuesC == 0:
                uncertaintyValueC = 0
            else:
                uncertaintyValueC = (desvestValuesC / (meanValuesCPs ** 2))* 1e12
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
            meanValueD=(10**12)/mean(valuesD)
            desvestValuesD = np.std(valuesD)/sqrt(len(valuesD))
            meanValuesDPs=mean(valuesD)
            if desvestValuesD == 0:
                uncertaintyValueD = 0
            else:
                uncertaintyValueD = (desvestValuesD / (meanValuesDPs ** 2))* 1e12
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
        """
        Calculates stop time intervals based on pulse timestamps from the measurement.

        The function receives a raw measurement and the expected number of stops, 
        then iteratively computes the time differences between consecutive valid 
        pulse timestamps. Each interval is converted to a frequency in Hz by 
        dividing 10^12 by the difference in timestamp units (assuming picoseconds).

        :param currentMeasure: A list containing pulse data for a single run.
        :param numberStops: The number of stop intervals expected in the measurement.
        :return: A list of frequency values (in Hz) calculated from the stop intervals.
        """
        #TODO: CHANGE RECALCULATING NUMBER OF STOPS
        tempValues=[]
        for i in range(numberStops-1):
            if currentMeasure[i+3]!=constants.OVERFLOW_PARAMETER and currentMeasure[i+4]!=constants.OVERFLOW_PARAMETER:
                differenceValue=currentMeasure[i+4]-currentMeasure[i+3]
                tempValues.append(differenceValue)
        
        return tempValues
    
    
    #TODO: DETERMINE THE NUMBER OF STOPS TO PERFORM THE MEASUREMENTS
    def determineStopsNumber(self, channelTest):
        """
        Determines the optimal number of stop pulses for a given channel to ensure valid measurements.

        This function tests different stop configurations by progressively reducing the number of 
        required stop pulses (from 5 down to 2). For each configuration, it performs multiple test 
        measurements and checks if at least half of them return valid data. If a configuration with 
        sufficient measurements is found, it is returned. If none meet the condition, 1 is returned 
        by default. If the thread is stopped during execution, the process halts.

        :param channelTest: A string indicating the channel to test ("A", "B", "C", or "D").
        :return: An integer representing the number of stop pulses that reliably produce measurements.
        """
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
                        if measurements[0][3] != constants.OVERFLOW_PARAMETER:
                            totalMeasurements+=1
            if totalMeasurements>totalIterations/2:
                stopsFounded=True
            else:
                stopsInMeasure-=1
        if self.running:
            self.changeStatusText.emit(f"Estimating number stops in channel {channelTest} 100%")
            time.sleep(1)
        
        return stopsInMeasure
        
    
    def enableDisableChannels(self):
        """
        Enables or disables device channels based on active measurement sentinels.

        This function disables all channels initially, then enables only the selected ones based on 
        the sentinel flags. It configures each enabled channel with a default stop mask and averaging 
        settings, and adds them to the list of channels to be measured. This reduces processing time 
        by avoiding unnecessary measurements from inactive channels.

        :return: None
        """
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
        """
        Stops the measurement process by setting the running sentinel to False.

        This function is typically called from the GUI when the user requests to stop the measurement. 
        Once the sentinel is set to False, the running loop in the thread will exit, effectively 
        terminating the background measurement process.

        :return: None
        """
        self.running=False