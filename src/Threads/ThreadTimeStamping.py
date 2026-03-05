from PySide2.QtCore import QThread, Signal, Slot
from datetime import datetime
import pyTempico as tempico
import time
import os
import sys
import io
from itertools import islice
import shutil
from Utils.createsavefile import createsavefile 
import Utils.constants as constants
class WorkerThreadTimeStamping(QThread):
    """
    Thread class responsible for executing and managing timestamp measurements in the background.

    This class extends `QThread` to handle real-time acquisition of timestamp data from a
    `TempicoDevice` without blocking the main UI thread. It supports three operational modes:
    - **Normal**: Manual start/stop by the user.
    - **Scheduled**: Automatic start/stop based on configured start and end times.
    - **Limited**: Stops automatically after a predefined number of measurements.

    The class collects data from up to four independent channels (A–D), tracks total and per-channel
    counts, and emits signals to update the user interface with measurement data, status text, and
    status colors. It also handles autosaving of data to files in supported formats.

    Main responsibilities:
    - Continuously acquire timestamp measurements while the thread is running.
    - Track total measurements and per-channel statistics.
    - Handle sentinel flags for pausing, stopping, and controlling measurement flow.
    - Emit signals to update UI components with real-time measurement and status information.
    - Save measurement data automatically or manually based on user settings.
    - Enable or disable specific channels based on configuration.

    Signals:
        newMeasurement (tuple, tuple, tuple, tuple, tuple, float, float, float, float, float):
            Emitted when new measurement data is available, including per-channel and total counts.
        changeStatusText (str):
            Emitted to update the UI status text.
        changeStatusColor (int):
            Emitted to update the UI status color (e.g., ready, running, saving).
        finishedMeasurements ():
            Emitted when the measurement process is complete.

    :param channelASentinel: Flag to enable/disable channel A measurements.
    :param channelBSentinel: Flag to enable/disable channel B measurements.
    :param channelCSentinel: Flag to enable/disable channel C measurements.
    :param channelDSentinel: Flag to enable/disable channel D measurements.
    :param normalMeasurementSentinel: Flag to control normal mode execution.
    :param scheduleMeasurementSentinel: Flag to control scheduled mode execution.
    :param limitMeasurementSentinel: Flag to control limited mode execution.
    :param device: Instance of `tempico.TempicoDevice` used to acquire timestamp data.
    :param savefile: Object responsible for handling file-saving operations.
    :param filename: File path or name to save measurement data.
    :param isAutoSave: Boolean indicating whether autosave is enabled.
    :param maximumMeasurements: Maximum number of measurements in limited mode (default 0).
    """
    newMeasurement=Signal(tuple,tuple,tuple,tuple,tuple,float,float,float,float,float)
    changeStatusText=Signal(str)
    changeStatusColor=Signal(int)
    finishedMeasurements=Signal()
    detectedErrorSaving=Signal()
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel, channelDSentinel,normalMeasurementSentinel, scheduleMeasurementSentinel,limitMeasurementSentinel,
                 device: tempico.TempicoDevice,savefile,filename,isAutoSave,maximumMeasurements=0):
        super().__init__()
        #init the parameters
        self.channelASentinel= channelASentinel
        self.channelBSentinel= channelBSentinel
        self.channelCSentinel= channelCSentinel
        self.channelDSentinel= channelDSentinel
        self.normalMeasurementSentinel=normalMeasurementSentinel
        self.scheduleMeasurementSentinel=scheduleMeasurementSentinel
        self.limitMeasurementSentinel=limitMeasurementSentinel
        self.device= device
        #Init the counters
        self.totalMeasurements=0
        self.totalMeasurementsChannelA=0
        self.totalMeasurementsChannelB=0
        self.totalMeasurementsChannelC=0
        self.totalMeasurementsChannelD=0
        #Getting the number of stops 
        self.numberStopsA=0
        self.numberStopsB=0
        self.numberStopsC=0
        self.numberStopsD=0
        #Value for limited measurements
        self.maximumMeasurements=maximumMeasurements
        self.allMeasurementsComplete=False
        #Sentinel to pause thread
        self.isPause=False
        #Sentinel for running
        self.running=True
        #Class to save the file and file name
        self.savefile=savefile
        self.filename=filename
        self.isAutosave=isAutoSave
        #Enable and disable the channels
        self.readyToReOrder=False
        self.enableDisableChannels()
        #Sentinel to know how many measurements are registered
        self.noMeasurementsSequent=0
        self.noAbortsSequent=0
        self.consecutiveErrors=0
        self.saveCurrentMeasurements()
        #Maximum value
        self.maximumValueMeasurement=5000000000
        self.savefile=createsavefile()
        self.folderData=self.savefile.getAutoSaveFolderPath()
        
        
    
    
    def run(self):
        #Sync the time with the device before measurement
        self.syncTime()
        if self.normalMeasurementSentinel:
            while self.running:
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:    
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
                
        elif self.scheduleMeasurementSentinel:
            while self.running:
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:
                    self.changeStatusText.emit("Paused measurement")
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getMeasurement()
        if self.limitMeasurementSentinel:
            while self.running and (not self.allMeasurementsComplete):
                if self.consecutiveErrors>=50:
                    self.running=False
                if self.isPause:
                    percentage=round((self.totalMeasurements/self.maximumMeasurements)*100,2)
                    message=f"Paused measurement {percentage} %"
                    self.changeStatusText.emit(message)
                    self.changeStatusColor.emit(2)
                    time.sleep(0.5)
                else:
                    self.getLimitedMeasurements()
        #Enable channels again after finished measurements
        self.enableChannelsAfterFinishedMeasurement()
        if self.isAutosave:
            self.finishedMeasurements.emit()
            while not self.readyToReOrder:
                time.sleep(0.5)
            self.changeStatusText.emit("Processing data")
            self.changeStatusColor.emit(2)
            self.sortTimeStamps(self.filename)
                
    def enableDisableChannels(self):
        """
        Configures the device channels according to the user's selection.

        This function enables or disables each measurement channel (A–D) based on
        the sentinel values provided at initialization. It also retrieves the
        number of stops for each active channel and calculates the total possible
        measurements for a single run, storing it in `totalDataPerMeasurement`.
        """
        self.totalDataPerMeasurement=0
        if self.channelASentinel:
            self.device.ch1.enableChannel()
            self.numberStopsA=self.device.ch1.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch1.disableChannel()
            
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
            self.numberStopsB=self.device.ch2.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch2.disableChannel()
            
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
            self.numberStopsC=self.device.ch3.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch3.disableChannel()
            
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
            self.numberStopsD=self.device.ch4.getNumberOfStops()
            self.totalDataPerMeasurement+= self.device.getNumberOfRuns()*self.device.ch1.getNumberOfStops()
        else:
            self.device.ch4.disableChannel()
    
    def enableChannelsAfterFinishedMeasurement(self):
        """
        Enables all measurement channels on the device.

        """
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
    
    def syncTime(self):
        """
        Synchronizes the system time with the connected device.
        """
        self.device.setDateTime()
    
    def sortMeasurementByStart(self, measurement):
        """
        Sorts measurement records by their start time.

        Filters out empty runs from the provided measurement list and sorts the 
        remaining entries in ascending order based on the third element of each record 
        (start time).

        :param measurement: List of measurement records, where each record is an iterable 
                            containing at least three elements.
        :type measurement: list
        :return: A list of filtered and sorted measurement records.
        :rtype: list
        """
        dataFiltered=[]
        for run in measurement:
            if run:
                dataFiltered.append(run)
        dataFiltered.sort(key=lambda x: x[2])
        return dataFiltered
    
            
    
    def getLimitedMeasurements(self):
        """
        Acquires, processes, and validates measurements from the device in limited mode, 
        stopping once the configured maximum number of measurements is reached.

        This method:
        1. Solicits a measurement from the device and captures any console output.
        2. Handles timeouts by attempting additional fetches, aborting when data is stagnant, 
        or resetting the device after repeated failures.
        3. Sorts the retrieved measurements by start time when applicable.
        4. Iterates through the measurements and:
        - Detects and skips corrupt data sequences.
        - Assigns valid measurement values to their respective channels (A, B, C, D) based 
            on enabled channel sentinels.
        - Verifies that values fall within the allowed measurement range.
        - Updates total and per-channel measurement counters.
        - Stops processing immediately if the maximum limit is reached.
        5. Identifies active channels producing no valid data and emits user warnings.
        6. Detects and records start-only measurements (with no corresponding stop values).
        7. Emits the processed results to the main thread, including:
        - Tuples of `(start_time, value)` for each channel.
        - List of start-only measurement timestamps.
        - Per-channel totals and overall total.
        8. Sends progress updates and status messages to the GUI.

        If no measurements are available or a start channel is inactive, a warning is emitted 
        to the main thread.
        """
        
        try:
            valueA=[]
            valueB=[]
            valueC=[]
            valueD=[]
            onlyStartMeasurements=[]
            startValues={}
            originalConsole=sys.stdout
            sys.stdout=io.StringIO()
            measure=self.device.measure()
            printedDeviceCommunication=sys.stdout.getvalue()
            sys.stdout=originalConsole
            finishedMeasurement=False
            if "Timeout reached" in printedDeviceCommunication:
                while not finishedMeasurement:
                    time.sleep(1)
                    newFetch=self.device.fetch()
                    if (newFetch==measure):
                        finishedMeasurement=True
                        measure=newFetch
                        self.device.abort()
                    else:
                        measure=newFetch
            
            if not measure and self.noMeasurementsSequent <3:
                #Counter to know how many not measurements are registered
                self.noMeasurementsSequent+=1
                
            elif not measure and self.noAbortsSequent>=10:
                self.device.reset()
                self.applyCurrentSettings()
                #Wait at least 20 ms 
                QThread.msleep(20)
            elif not measure and self.noMeasurementsSequent >=3:
                #Set timeout to finish abort
                self.noAbortsSequent+=1
                self.device.abort()
                
            valuesToSkip=0
            if self.totalDataPerMeasurement+self.totalMeasurements>=self.maximumMeasurements:
                if measure:
                    measure=self.sortMeasurementByStart(measure)
            startValues={}
            totalNoStarts=0
            StartChannelRegister=True
            totalLenMeasure=len(measure)
            if measure:
                self.noMeasurementsSequent=0
                self.noAbortsSequent=0
                for measureIndex in range(totalLenMeasure):
                    channelMeasure=measure[measureIndex]
                    if channelMeasure:
                        # if measureIndex<totalLenMeasure-2 and valuesToSkip<1:
                        #     nextMeasure=measure[measureIndex+1]
                        #     valuesToSkip=self.checkCorruptData(channelMeasure,nextMeasure)
                        # if valuesToSkip>0:
                        #     valuesToSkip-=1
                        #     continue
                        startValue=channelMeasure[2]
                        startValue= str(datetime.fromtimestamp(startValue))
                        startValues[startValue]=0  
                        if self.channelASentinel:
                            if channelMeasure[0]==1:
                                totalRange=self.getRange(channelMeasure,self.numberStopsA)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                
                                    
                        if self.channelBSentinel:
                            if channelMeasure[0]==2:
                                totalRange=self.getRange(channelMeasure,self.numberStopsB)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                                self.allMeasurementsComplete=True
                                                break
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>4: 
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                        if self.channelCSentinel:
                            if channelMeasure[0]==3:
                                totalRange=self.getRange(channelMeasure,self.numberStopsC)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                                self.allMeasurementsComplete=True
                                                break
                                if totalRange>1: 
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                        if self.channelDSentinel:
                            if channelMeasure[0]==4:
                                totalRange=self.getRange(channelMeasure,self.numberStopsD)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                                self.allMeasurementsComplete=True
                                                break
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                        if self.totalMeasurements>=self.maximumMeasurements:
                                            self.allMeasurementsComplete=True
                                            break
                    else:
                        totalNoStarts+=1
            else:
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)
            if totalNoStarts==len(measure):
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)  
            for key, value in startValues.items():
                if self.totalMeasurements>= self.maximumMeasurements:
                    self.allMeasurementsComplete=True
                    break
                else:
                    if value==0:
                        onlyStartMeasurements.append(key)
                        self.totalMeasurements+=1
            channelStringList=[]
            if self.channelASentinel and not valueA and StartChannelRegister:
                channelStringList.append("A")
            if self.channelBSentinel and not valueB and StartChannelRegister:
                channelStringList.append("B")
            if self.channelCSentinel and not valueC and StartChannelRegister:
                channelStringList.append("C")
            if self.channelDSentinel and not valueD and StartChannelRegister:
                channelStringList.append("D")
            percentage=round((self.totalMeasurements/self.maximumMeasurements)*100,2)
            if channelStringList:
                channelErrorString=", ".join(channelStringList)
                if len(channelStringList)==1:
                    errorMessage=f"The channnel {channelErrorString} is not taking measurements {percentage} %"
                else:
                    errorMessage=f"The channnels {channelErrorString} are not taking measurements {percentage} %"
                
                self.changeStatusText.emit(errorMessage)
                self.changeStatusColor.emit(3)
            elif not StartChannelRegister:
                pass
            else:
                message=f"Running measurement {percentage} %"
                
                self.changeStatusText.emit(message)
                self.changeStatusColor.emit(1)  
            #Emitir lista de tuplas de valores
            self.newMeasurement.emit(valueA,valueB,valueC,valueD,onlyStartMeasurements, self.totalMeasurementsChannelA,
                                    self.totalMeasurementsChannelB,self.totalMeasurementsChannelC, self.totalMeasurementsChannelD, self.totalMeasurements)
        except Exception as e:
            # If this happen corrupted data was found
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors+=1
                
        
    
    def getMeasurement(self):
        """
        Acquires, processes, and validates measurements from the device, assigning 
        them to their corresponding channels and emitting results to the main thread.

        This method:
        1. Solicits a measurement from the device.
        2. Handles timeouts by attempting additional fetches and aborting if needed.
        3. Verifies measurement integrity:
        - Detects and skips corrupt data sequences.
        - Confirms that the device returns complete measurements.
        4. Organizes measurements by channel (A, B, C, D) according to the channel 
        sentinels enabled in the worker.
        5. Validates that each enabled channel is actually producing measurements, 
        generating user warnings if not.
        6. Detects and reports cases where only start values are recorded without 
        associated stop measurements.
        7. Updates internal counters for total and per-channel measurements.
        8. Emits the processed measurement data, including:
        - Tuples for each channel with `(start_time, value)`.
        - List of start-only measurements.
        - Totals per channel and global total.

        If no measurements are available or a start channel is inactive, a warning 
        is emitted to the main thread.
        """
        try:
            valueA=[]
            valueB=[]
            valueC=[]
            valueD=[]
            onlyStartMeasurements=[]
            startValues={}
            originalConsole=sys.stdout
            sys.stdout=io.StringIO()
            measure=self.device.measure()
            printedDeviceCommunication=sys.stdout.getvalue()
            sys.stdout=originalConsole
            finishedMeasurement=False
            if "Timeout reached" in printedDeviceCommunication:
                while not finishedMeasurement:
                    time.sleep(1)
                    newFetch=self.device.fetch()
                    if (newFetch==measure):
                        finishedMeasurement=True
                        measure=newFetch
                        self.device.abort()
                        QThread.msleep(20)
                    else:
                        measure=newFetch
            
            if not measure and self.noMeasurementsSequent <3:
                #Counter to know how many not measurements are registered
                self.noMeasurementsSequent+=1
                
            elif not measure and self.noAbortsSequent>=10:
                self.device.reset()
                self.applyCurrentSettings() 
                QThread.msleep(20)
            elif not measure and self.noMeasurementsSequent >=3:
                #Set timeout to finish abort
                self.noAbortsSequent+=1
                self.device.abort()
            valuesToSkip=0 
            totalNoStarts=0
            StartChannelRegister=True
            totalLenMeasure=len(measure)
            if measure:
                self.noMeasurementsSequent=0
                self.noAbortsSequent=0
                for measureIndex in range(totalLenMeasure):
                    channelMeasure=measure[measureIndex]                        
                    if channelMeasure:
                        # if measureIndex<totalLenMeasure-2 and valuesToSkip<1:
                        #     nextMeasure=measure[measureIndex+1]
                        #     valuesToSkip=self.checkCorruptData(channelMeasure,nextMeasure)
                        # if valuesToSkip>0:
                        #     valuesToSkip-=1
                        #     continue    
                        #New start algo
                        startValue=channelMeasure[2]
                        startValue= str(datetime.fromtimestamp(startValue))
                        startValues[startValue]=0
                        if self.channelASentinel:
                            if channelMeasure[0]==1:
                                totalRange=self.getRange(channelMeasure,self.numberStopsA)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueA.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelA+=1
                                
                                    
                        if self.channelBSentinel:
                            if channelMeasure[0]==2:
                                totalRange=self.getRange(channelMeasure,self.numberStopsB)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                                if totalRange>4: 
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueB.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelB+=1
                        if self.channelCSentinel:
                            if channelMeasure[0]==3:
                                totalRange=self.getRange(channelMeasure,self.numberStopsC)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if totalRange>1: 
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueC.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelC+=1
                        if self.channelDSentinel:
                            if channelMeasure[0]==4:
                                totalRange=self.getRange(channelMeasure,self.numberStopsD)
                                if totalRange>0:
                                    if channelMeasure[3]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[3]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if totalRange>1:
                                    if channelMeasure[4]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[4]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if totalRange>2:
                                    if channelMeasure[5]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[5]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if totalRange>3:
                                    if channelMeasure[6]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[6]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                                if totalRange>4:
                                    if channelMeasure[7]!=constants.OVERFLOW_PARAMETER:
                                        startValues[startValue]+=1
                                        valueD.append((startValue,channelMeasure[7]))
                                        self.totalMeasurements+=1
                                        self.totalMeasurementsChannelD+=1
                    else:
                        totalNoStarts+=1
            else:
                errorMessageInput=f"The start channel is not taking measurements"
                StartChannelRegister=False
                self.changeStatusText.emit(errorMessageInput)
                self.changeStatusColor.emit(3)
            if measure:
                if totalNoStarts==len(measure):
                    errorMessageInput=f"The start channel is not taking measurements"
                    StartChannelRegister=False
                    self.changeStatusText.emit(errorMessageInput)
                    self.changeStatusColor.emit(3)
            onlyStartsValues = [key for key, value in startValues.items() if value == 0]
            onlyStartMeasurements=onlyStartsValues
            self.totalMeasurements+=len(onlyStartMeasurements)
            channelStringList=[]
            if self.channelASentinel and (not valueA) and StartChannelRegister: 
                channelStringList.append("A")
            if self.channelBSentinel and (not valueB) and StartChannelRegister:
                channelStringList.append("B")
            if self.channelCSentinel and (not valueC) and StartChannelRegister:
                channelStringList.append("C")
            if self.channelDSentinel and (not valueD) and StartChannelRegister:
                channelStringList.append("D")
            if channelStringList:
                channelErrorString=", ".join(channelStringList)
                if len(channelStringList)==1:
                    errorMessage=f"The channnel {channelErrorString} is not taking measurements"
                else:
                    errorMessage=f"The channnels {channelErrorString} are not taking measurements"
                
                self.changeStatusText.emit(errorMessage)
                self.changeStatusColor.emit(3)
            elif not StartChannelRegister:
                pass
            else:
                self.changeStatusText.emit("Running measurement")
                self.changeStatusColor.emit(1)  
            #Emitir lista de tuplas de valores
            self.consecutiveErrors=0
            
            self.newMeasurement.emit(valueA,valueB,valueC,valueD,onlyStartMeasurements, self.totalMeasurementsChannelA,
                                    self.totalMeasurementsChannelB,self.totalMeasurementsChannelC, self.totalMeasurementsChannelD, self.totalMeasurements)
        except Exception as e:
            # If this happen corrupted data was found
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors+=1
                
            
        
    def getRange(self, currentMeasurement,stopNumber):
        """
        Determines the valid range of stops in a measurement.

        This function checks the length of the provided measurement list to ensure
        it is not corrupted. If the length is smaller than expected, the range is 
        adjusted to avoid out-of-bounds errors when processing the data.

        :param currentMeasurement: The current measurement data as a list.
        :param stopNumber: The expected number of stops.
        :return: The validated number of stops to iterate over.
        """
        totalRange=0
        correctRange=stopNumber
        totalLenMeasurement=len(currentMeasurement)
        if totalLenMeasurement>=4:
            if totalLenMeasurement-3<correctRange:
                totalRange=totalLenMeasurement-3
            else:
                totalRange=correctRange
        return totalRange

    
    def checkCorruptData(self, currentMeasurement, nextMeasurement):
        """
        Checks if the current measurement should be skipped due to data corruption.

        This function compares the sequence index of the current measurement with 
        the next one. If the sequence does not follow the expected order, it 
        determines that the current measurement is corrupt and should be skipped.

        :param currentMeasurement: The current measurement data as a list.
        :param nextMeasurement: The following measurement data as a list.
        :return: 1 if the current measurement should be skipped, 0 otherwise.
        """
        finalToSkip=0
        if nextMeasurement:
            if (currentMeasurement[1]+1)!=nextMeasurement[1] and ((currentMeasurement[1])!=nextMeasurement[1]):
                finalToSkip=1
        return finalToSkip
    
    
    def changeIsPauseTrue(self):
        """
        Sets the pause sentinel to True.

        :return: None
        """
        self.isPause= True
    
    def changeIsPauseFalse(self):
        """
        Sets the pause sentinel to False.

        :return: None
        """
        self.isPause= False
    
    def changeReadyToReorder(self):
        """
        Sets the ready-to-reorder sentinel to True.

        :return: None
        """
        self.readyToReOrder=True
    
    
    def sortTimeStamps(self,filePath):
        """
        Sorts a timestamp file by start times and moves the processed data to the user-selected folder.

        This function reads a temporary autosave file containing timestamp data,
        sorts the entries by their start time, and writes the sorted data both back
        to the temporary file and to the final file in the user-selected save
        location. The function also updates the processing progress via status
        signals.

        :param file_path: The destination file path where the sorted data will be saved.
        :return: None
        """
        tempDataPath = os.path.join(self.folderData, f"AutoSaveData.txt")
        tempDataOrder= os.path.join(self.folderData, f"AutoSaveDataSorted.txt")
        selectedFormat= filePath.split(".")[-1]
        newSeparator= ";" if selectedFormat == "csv" else "\t"
        chunkSize=30000
        #1000 Margin
        overlapSize=self.totalDataPerMeasurement+1000
        self.changeStatusText.emit(f"Processing data 0%")
        currentAdvance=0
        with open(tempDataPath, 'r', encoding='utf-8') as file:
            header = list(islice(file, 8))
            with open(tempDataOrder, 'w', encoding='utf-8') as out:
                for headLine in header:
                    newheadLine=headLine.replace("\t",newSeparator)
                    out.write(newheadLine)
            with open(tempDataOrder, 'a', encoding='utf-8') as outFile:
                isFinished=False
                currentOverlapValues=[]
                while not isFinished:
                    currentChunk=list(islice(file, chunkSize-len(currentOverlapValues)))
                    if not currentChunk and len(currentOverlapValues) == 0:
                        isFinished=True
                    else:
                        dataToOrder=currentOverlapValues
                        for line in currentChunk:
                            parts = line.strip().split("\t")
                            if len(parts) == 3:
                                start_time_str, stop_time, channel = parts
                                try:
                                    dataToOrder.append((start_time_str, stop_time, channel))
                                except ValueError:
                                    self.detectedErrorSaving.emit()
                                    continue
                        dataToOrder.sort(key=lambda x: x[0])
                        totalLenChunk=len(dataToOrder)
                        currentAdvance+=totalLenChunk-overlapSize
                        percent = int(currentAdvance / (self.totalMeasurements))
                        self.changeStatusText.emit(f"Processing data {percent}%")
                        if totalLenChunk < chunkSize:
                            currentOverlapValues=[]
                            for line in dataToOrder:
                                outFile.write(f"{line[0]}{newSeparator}{line[1]}{newSeparator}{line[2]}\n")
                        else:
                            #TO DO USE dataOrder
                            for line in dataToOrder[:-overlapSize]:
                                outFile.write(f"{line[0]}{newSeparator}{line[1]}{newSeparator}{line[2]}\n")
                            currentOverlapValues=dataToOrder[-overlapSize:]
        os.replace(tempDataOrder, tempDataPath)
        shutil.copy2(tempDataPath, filePath)
        self.changeStatusText.emit(f"Processing data 100%")
    
    def saveCurrentMeasurements(self):
        """
        Saves the current device configuration settings.

        This function retrieves the general and per-channel configuration 
        parameters from the connected device and stores them in the corresponding 
        instance variables. These values represent the active measurement 
        settings, such as run counts, thresholds, modes, and stop configurations.

        :return: None
        """
        #General settings
        self.numberRunsSetting=self.device.getNumberOfRuns()
        self.thresholdVoltage=self.device.getThresholdVoltage()
        #Channel A
        self.averageCyclesChannelA= self.device.ch1.getAverageCycles()
        self.modeChannelA= self.device.ch1.getMode()
        self.numberStopsChannelA = self.device.ch1.getNumberOfStops()
        self.stopEdgeTypeChannelA= self.device.ch1.getStopEdge()
        self.stopMaskChannelA=self.device.ch1.getStopMask()
        #ChannelB
        self.averageCyclesChannelB= self.device.ch2.getAverageCycles()
        self.modeChannelB= self.device.ch2.getMode()
        self.numberStopsChannelB = self.device.ch2.getNumberOfStops()
        self.stopEdgeTypeChannelB= self.device.ch2.getStopEdge()
        self.stopMaskChannelB=self.device.ch2.getStopMask()
        #ChannelC
        self.averageCyclesChannelC= self.device.ch3.getAverageCycles()
        self.modeChannelC= self.device.ch3.getMode()
        self.numberStopsChannelC = self.device.ch3.getNumberOfStops()
        self.stopEdgeTypeChannelC= self.device.ch3.getStopEdge()
        self.stopMaskChannelC=self.device.ch3.getStopMask()
        #ChannelD
        self.averageCyclesChannelD= self.device.ch4.getAverageCycles()
        self.modeChannelD= self.device.ch4.getMode()
        self.numberStopsChannelD = self.device.ch4.getNumberOfStops()
        self.stopEdgeTypeChannelD= self.device.ch4.getStopEdge()
        self.stopMaskChannelD=self.device.ch4.getStopMask()
    
    
    def applyCurrentSettings(self):
        """
        Applies the previously saved device configuration.

        This function restores the general and per-channel configuration 
        parameters that were saved from the device, and reconfigures the device 
        accordingly. It also enables or disables channels based on sentinel values 
        to continue measurements.

        :return: None
        """
        #Settings to general device
        self.device.setNumberOfRuns(self.numberRunsSetting)
        self.device.setThresholdVoltage(self.thresholdVoltage)
        #Settings to channelA
        self.device.ch1.setAverageCycles(self.averageCyclesChannelA)
        self.device.ch1.setMode(self.modeChannelA)
        self.device.ch1.setNumberOfStops(self.numberStopsChannelA)
        self.device.ch1.setStopEdge(self.stopEdgeTypeChannelA)
        self.device.ch1.setStopMask(self.stopMaskChannelA)
        #Settings to channelB
        self.device.ch2.setAverageCycles(self.averageCyclesChannelB)
        self.device.ch2.setMode(self.modeChannelB)
        self.device.ch2.setNumberOfStops(self.numberStopsChannelB)
        self.device.ch2.setStopEdge(self.stopEdgeTypeChannelB)
        self.device.ch2.setStopMask(self.stopMaskChannelB)
        #Settings to channelC
        self.device.ch3.setAverageCycles(self.averageCyclesChannelC)
        self.device.ch3.setMode(self.modeChannelC)
        self.device.ch3.setNumberOfStops(self.numberStopsChannelC)
        self.device.ch3.setStopEdge(self.stopEdgeTypeChannelC)
        self.device.ch3.setStopMask(self.stopMaskChannelC)
        #Settings to channelD
        self.device.ch4.setAverageCycles(self.averageCyclesChannelD)
        self.device.ch4.setMode(self.modeChannelD)
        self.device.ch4.setNumberOfStops(self.numberStopsChannelD)
        self.device.ch4.setStopEdge(self.stopEdgeTypeChannelD)
        self.device.ch4.setStopMask(self.stopMaskChannelD)
        #Enable disable channels to continue measurements
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.channelASentinel:
            self.device.ch1.enableChannel()
        if self.channelBSentinel:
            self.device.ch2.enableChannel()
        if self.channelCSentinel:
            self.device.ch3.enableChannel()
        if self.channelDSentinel:
            self.device.ch4.enableChannel()
        
        
    @Slot()   
    def stop(self):
        """
        Sets the running sentinel to False to indicate that the thread has finished.

        :return: None
        """
        self.running=False    