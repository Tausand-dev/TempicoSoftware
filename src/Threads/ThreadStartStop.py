from PySide2.QtCore import QThread, Signal, Slot
import time
import time
import io
import pyTempico as tempico
import sys
import Utils.constants as constants
class WorkerThreadStartStopHistogram(QThread):
    """
    Worker thread for processing Start-Stop measurements without blocking the main UI.

    This class extends `QThread` to handle the acquisition and processing of 
    Start-Stop measurement data from a `TempicoDevice` in the background. It 
    collects data from up to four channels (A–D), applies range validation, 
    detects out-of-range measurements, and emits signals to update the GUI 
    with processed results, status messages, and visual indicators.

    Main responsibilities:
    - Acquire Start-Stop measurements for each enabled channel.
    - Track total and out-of-range counts per channel.
    - Manage sentinels for detecting missing measurements or channels requiring mode changes.
    - Maintain and emit maximum measurement values for updating histogram ranges.
    - Save device configuration before measurement and determine if batch mode should be used.
    - Handle dialog prompts when channels exceed acceptable out-of-range limits.

    Signals:
        dataSignal (float, str):
            Emitted with the processed measurement value and its channel ID.
        dataPureSignal (float, str):
            Emitted with the raw measurement value and its channel ID.
        threadCreated (int):
            Emitted when the thread is initialized and ready.
        dialogInit ():
            Emitted to initialize a measurement-related dialog in the UI.
        colorValue (int):
            Emitted to update the UI status color (e.g., normal, warning, error).
        stringValue (str):
            Emitted to update the UI status text.
        dialogSignal (str):
            Emitted to request opening a dialog for a specific channel.
        newMaxValueSignal (float, str):
            Emitted when a new maximum value is detected for a channel.
        dataBashSignal (list, list, list, list):
            Emitted with batched processed measurements for all channels.
        dataPureBashSignal (list, list, list, list):
            Emitted with batched raw measurements for all channels.

    :param parent: The parent widget or window managing this thread.
    :param device: Instance of `tempico.TempicoDevice` used to acquire measurements.
    :param sentinelSaveA: Boolean indicating if channel A measurements should be saved.
    :param sentinelSaveB: Boolean indicating if channel B measurements should be saved.
    :param sentinelSaveC: Boolean indicating if channel C measurements should be saved.
    :param sentinelSaveD: Boolean indicating if channel D measurements should be saved.
    :param checkA: Boolean indicating if channel A should be checked for measurement validity.
    :param checkB: Boolean indicating if channel B should be checked for measurement validity.
    :param checkC: Boolean indicating if channel C should be checked for measurement validity.
    :param checkD: Boolean indicating if channel D should be checked for measurement validity.
    """
    dataSignal=Signal(float,str)
    dataPureSignal=Signal(float,str)
    threadCreated=Signal(int)
    dialogInit=Signal()
    colorValue=Signal(int)
    stringValue=Signal(str)
    dialogSignal=Signal(str)
    newMaxValueSignal=Signal(float,str)
    dataBashSignal=Signal(list,list,list,list)
    dataPureBashSignal=Signal(list,list,list,list)
    
    
    def __init__(self,parent,device: tempico.TempicoDevice,sentinelSaveA,sentinelSaveB,sentinelSaveC,sentinelSaveD,checkA,checkB,checkC,checkD):
        super().__init__()
        self.totalA=0
        self.outOfRangeA=0
        self.totalB=0
        self.outOfRangeB=0
        self.totalC=0
        self.outOfRangeC=0
        self.totalD=0
        self.outOfRangeD=0
        self.parent=parent
        self.device=device
        self.setinelSaveA=sentinelSaveA
        self.setinelSaveB=sentinelSaveB
        self.setinelSaveC=sentinelSaveC
        self.setinelSaveD=sentinelSaveD
        #Sentinel to know if the thread stil running
        self.itsRunning=True
        self.checkA=checkA
        self.checkB=checkB
        self.checkC=checkC
        self.checkD=checkD
        self.enableDisableChannels()
        #Check if the dialog was opened before
        self.sentinelDialogA=False
        self.sentinelDialogB=False
        self.sentinelDialogC=False
        self.sentinelDialogD=False
        self.currentMaxValueA=0
        self.currentMaxValueB=0
        self.currentMaxValueC=0
        self.currentMaxValueD=0
        #Sentinel to know if dialog is open
        self.openDialog=False
        #List of channels to change
        self.channelsToChange=[]
        #sentinel for the starts
        self.totalStarts=0
        #List of channels witouth measurement
        self.channelsNM=[]
        #String with the state of the device
        self.currentState=""
        #String with NM
        self.currentNM=""
        #Sentinels to know if there is not a measurement
        self.noMeasurementA=0
        self.noMeasurementB=0
        self.noMeasurementC=0
        self.noMeasurementD=0
        self.noMeasurementsSequent=0
        self.noAbortsSequent=0
        self.consecutiveErrors=0
        self.saveCurrentSettings()
        self.isBashedMeasurement()
        


        
    #Main function
    def run(self):
        """
        Executes the thread's main loop to update the graph based on measurements.

        The function emits a signal indicating that the thread has been created. It then enters a 
        loop that continues as long as the thread is running. Inside the loop, it calls the update 
        method to refresh the graph and pauses for 0.5 seconds before the next iteration.

        :return: None
        """
        self.threadCreated.emit(0)
        while self.itsRunning:
             self.getMeasurements()
             time.sleep(0.1)
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
    
    def enableDisableChannels(self):
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.checkA:
            self.device.ch1.enableChannel()
        if self.checkB:
            self.device.ch2.enableChannel()
        if self.checkC:
            self.device.ch3.enableChannel()
        if self.checkD:
            self.device.ch4.enableChannel()
    ##---------------------------------##
    ##---------------------------------##
    ##----Get measurements function----##
    ##---------------------------------##
    ##---------------------------------## 
    
    def getMeasurements(self):
        """
        Acquires and processes timestamp measurements from each active channel.

        This function retrieves measurement data from the connected device, 
        validates it, and processes it channel by channel (A–D). It checks the 
        number of stops for each channel, determines whether to emit the 
        measurement immediately or wait based on the configured number of runs, 
        and detects potential corruption in the measurement sequence.

        Additional checks are performed to:
        - Identify channels that are not recording measurements correctly.
        - Detect if the problem is due to missing Start signals.
        - Prompt the user to change the mode of channels if a high proportion of 
            out-of-range values is detected.
        - Capture potential disconnection errors and stop the measurement if they 
            persist.

        This method also emits status messages, channel problem notifications, and 
        measurement values for both normal and batched data modes.

        :return: None
        """
        
        valuesA=[]
        dataPureValuesA=[]
        valuesB=[]
        dataPureValuesB=[]
        valuesC=[]
        dataPureValuesC=[]
        valuesD=[]
        dataPureValuesD=[]
        try:
            originalConsole=sys.stdout
            sys.stdout=io.StringIO()
            measurement=self.device.measure()
            printedDeviceCommunication=sys.stdout.getvalue()
            sys.stdout=originalConsole
            finishedMeasurement=False
            if "Timeout reached" in printedDeviceCommunication:
                while not finishedMeasurement:
                    time.sleep(1)
                    newFetch=self.device.fetch()
                    if (newFetch==measurement):
                        finishedMeasurement=True
                        measurement=newFetch
                    else:
                        measurement=newFetch
            if not measurement and self.noMeasurementsSequent <3:
                self.noMeasurementsSequent+=1
                
            elif not measurement and self.noAbortsSequent>=10:
                self.device.reset()
                self.applyCurrentSettings()
                QThread.msleep(20)
            elif not measurement and self.noMeasurementsSequent >=3:
                self.noAbortsSequent+=1
                self.device.abort()
                
            # valuesToSkip=0
            
            if measurement:
                totalLenMeasurement= len(measurement)
                self.noAbortsSequent=0
                for indexRun in range(totalLenMeasurement):
                    run=measurement[indexRun]
                    # TODO: Test if this is not neccesary
                    # if indexRun<(totalLenMeasurement-2) and valuesToSkip<1:
                    #     nextRun=measurement[indexRun+1]
                    #     valuesToSkip=self.checkCorruptData(run,nextRun)
                    # if valuesToSkip>0:
                    #     valuesToSkip-=1
                    #     continue
                    if run:
                        if "Start" in self.channelsNM:
                            self.channelsNM.remove("Start")
                        #Channel A
                        if run[0]==1:
                            totalRangeA=self.getRange(run,self.numberStopsChannelA)
                            for i in range(totalRangeA):
                                if run[3+i]!=constants.OVERFLOW_PARAMETER:
                                    if "A" in self.channelsNM:
                                        self.channelsNM.remove("A")
                                    self.totalA+=1
                                    if self.modeChannelA==2:
                                        correctedUnitsMeasurement=run[3+i]/(10**9)
                                        self.emitOrSaveMeasurement(valuesA,correctedUnitsMeasurement,run[3+i],dataPureValuesA,"A")
                                    else:
                                        correctedUnitsMeasurement=run[3+i]/(10**3)
                                        if run[3+i]>800000:
                                            self.outOfRangeA+=1
                                        if self.totalA>10 and (self.outOfRangeA/self.totalA)>0.6:
                                            if not self.sentinelDialogA:
                                                self.openDialog=True
                                                self.sentinelDialogA=True
                                                self.dialogSignal.emit("channel A")
                                                while (self.openDialog):
                                                    time.sleep(1)
                                                self.modeChannelA=self.device.ch1.getMode()
                                                if self.modeChannelA==1:
                                                    self.emitOrSaveMeasurement(valuesA,correctedUnitsMeasurement,run[3+i],dataPureValuesA,"A")
                                                    
                                            else:
                                                self.emitOrSaveMeasurement(valuesA,correctedUnitsMeasurement,run[3+i],dataPureValuesA,"A")
                                                
                                        else:
                                            self.emitOrSaveMeasurement(valuesA,correctedUnitsMeasurement,run[3+i],dataPureValuesA,"A")
                                            
                                            if "A" in self.channelsToChange:
                                                self.channelsToChange.remove("A")
                                else:
                                    if "A" not in self.channelsNM:
                                        self.channelsNM.append("A")
                                                
                        #Channel B
                        elif run[0]==2:
                            totalRangeB=self.getRange(run,self.numberStopsChannelB)
                            for i in range(totalRangeB):
                                if run[3+i]!=constants.OVERFLOW_PARAMETER:
                                    if "B" in self.channelsNM:
                                        self.channelsNM.remove("B")
                                    self.totalB+=1
                                    if self.modeChannelB==2:
                                        correctedUnitsMeasurement=run[3+i]/(10**9)
                                        self.emitOrSaveMeasurement(valuesB,correctedUnitsMeasurement,run[3+i],dataPureValuesB,"B")
                                    else:
                                        correctedUnitsMeasurement=run[3+i]/(10**3)
                                        if run[3+i]>800000:
                                            self.outOfRangeB+=1
                                        if self.totalB>10 and (self.outOfRangeB/self.totalB)>0.6:
                                            if not self.sentinelDialogB:
                                                self.openDialog=True
                                                self.sentinelDialogB=True
                                                self.dialogSignal.emit("channel B")
                                                while (self.openDialog):
                                                    time.sleep(1)
                                                self.modeChannelB=self.device.ch2.getMode()
                                                if self.modeChannelB==1:
                                                    self.emitOrSaveMeasurement(valuesB,correctedUnitsMeasurement,run[3+i],dataPureValuesB,"B")
                                            else:
                                                self.emitOrSaveMeasurement(valuesB,correctedUnitsMeasurement,run[3+i],dataPureValuesB,"B")
                                        else:
                                            self.emitOrSaveMeasurement(valuesB,correctedUnitsMeasurement,run[3+i],dataPureValuesB,"B")
                                            if "B" in self.channelsToChange:
                                                self.channelsToChange.remove("B")
                                else:
                                    if "B" not in self.channelsNM:
                                        self.channelsNM.append("B")
                        #Channel C
                        elif run[0]==3:
                            totalRangeC=self.getRange(run,self.numberStopsChannelC)
                            for i in range(totalRangeC):
                                if run[3+i]!=constants.OVERFLOW_PARAMETER:
                                    if "C" in self.channelsNM:
                                        self.channelsNM.remove("C")
                                    self.totalC+=1
                                    if self.modeChannelC==2:
                                        correctedUnitsMeasurement=run[3+i]/(10**9)
                                        self.emitOrSaveMeasurement(valuesC,correctedUnitsMeasurement,run[3+i],dataPureValuesC,"C")
                                    else:
                                        correctedUnitsMeasurement=run[3+i]/(10**3)
                                        if run[3+i]>800000:
                                            self.outOfRangeC+=1
                                        if self.totalC>10 and (self.outOfRangeC/self.totalC)>0.6:
                                            if not self.sentinelDialogC:
                                                self.openDialog=True
                                                self.sentinelDialogC=True
                                                self.dialogSignal.emit("channel C")
                                                while (self.openDialog):
                                                    time.sleep(1)
                                                self.modeChannelC=self.device.ch3.getMode()
                                                if self.modeChannelC==1:
                                                    self.emitOrSaveMeasurement(valuesC,correctedUnitsMeasurement,run[3+i],dataPureValuesC,"C")
                                            else:
                                                self.emitOrSaveMeasurement(valuesC,correctedUnitsMeasurement,run[3+i],dataPureValuesC,"C")
                                        else:
                                            self.emitOrSaveMeasurement(valuesC,correctedUnitsMeasurement,run[3+i],dataPureValuesC,"C")
                                            if "C" in self.channelsToChange:
                                                self.channelsToChange.remove("C")
                                else:
                                    if "C" not in self.channelsNM:
                                        self.channelsNM.append("C")
                        #Channel D
                        elif run[0]==4:
                            totalRangeD=self.getRange(run,self.numberStopsChannelD)
                            for i in range(totalRangeD):
                                if run[3+i]!=constants.OVERFLOW_PARAMETER:
                                    if "D" in self.channelsNM:
                                        self.channelsNM.remove("D")
                                    self.totalD+=1
                                    if self.modeChannelD==2:
                                        correctedUnitsMeasurement=run[3+i]/(10**9)
                                        self.emitOrSaveMeasurement(valuesD,correctedUnitsMeasurement,run[3+i],dataPureValuesD,"D")
                                    else:
                                        correctedUnitsMeasurement=run[3+i]/(10**3)
                                        if run[3+i]>800000:
                                            self.outOfRangeD+=1
                                        if self.totalD>10 and (self.outOfRangeD/self.totalD)>0.6:
                                            if not self.sentinelDialogD:
                                                self.openDialog=True
                                                self.sentinelDialogD=True
                                                self.dialogSignal.emit("channel D")
                                                while (self.openDialog):
                                                    time.sleep(1)
                                                self.modeChannelD=self.device.ch4.getMode()
                                                if self.modeChannelD==1:
                                                    self.emitOrSaveMeasurement(valuesD,correctedUnitsMeasurement,run[3+i],dataPureValuesD,"D")
                                            else:
                                                self.emitOrSaveMeasurement(valuesD,correctedUnitsMeasurement,run[3+i],dataPureValuesD,"D")
                                        else:
                                            self.emitOrSaveMeasurement(valuesD,correctedUnitsMeasurement,run[3+i],dataPureValuesD,"D")
                                            if "D" in self.channelsToChange:
                                                self.channelsToChange.remove("D")
                                else:
                                    if "D" not in self.channelsNM:
                                        self.channelsNM.append("D")
                    else:
                        if "Start" not in self.channelsNM:
                            self.channelsNM=[]
                            self.channelsNM.append("Start")    
            else:
                if "Start" not in self.channelsNM:
                    self.channelsNM=[]
                    self.channelsNM.append("Start")
               
            if self.isBashed:
                if valuesA:
                    self.newMaxValueSignal.emit(self.currentMaxValueA,"A")
                if valuesB:
                    self.newMaxValueSignal.emit(self.currentMaxValueB,"B")
                if valuesC:
                    self.newMaxValueSignal.emit(self.currentMaxValueC,"C")
                if valuesD:
                    self.newMaxValueSignal.emit(self.currentMaxValueD,"D")
                self.dataPureBashSignal.emit(dataPureValuesA,dataPureValuesB,dataPureValuesC,dataPureValuesD)
                self.dataBashSignal.emit(valuesA,valuesB,valuesC,valuesD)
                
            if len(self.channelsToChange)>0 and len(self.channelsNM)==0:
                stringEmit="Consider changing mode of the channels:"
                for i in range(len(self.channelsToChange)):
                    if i==0:
                        stringEmit+=" "+self.channelsToChange[i]
                    else:
                        stringEmit+=", "+self.channelsToChange[i]
                self.currentState= stringEmit
                self.colorValue.emit(3)
                self.stringValue.emit(self.currentState)
            elif len(self.channelsNM)>0:
                stringEmit="No measurements in channels: "
                for i in range(len(self.channelsNM)):
                    if i==0:
                        stringEmit+=" "+self.channelsNM[i] 
                    else:
                        stringEmit+=", "+self.channelsNM[i] 
                self.currentNM=stringEmit
                emitStringProblems=self.currentNM
                self.colorValue.emit(3)
                self.stringValue.emit(emitStringProblems)
            elif len(self.channelsNM)==0 and len(self.channelsToChange)==0:
                self.colorValue.emit(1)
                self.stringValue.emit("Measurement running")
            self.consecutiveErrors=0
        except Exception as e:
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors+=1
            if self.consecutiveErrors>10:
                self.stop()


    def emitOrSaveMeasurement(self,listValues,measurement,pureMeasurement,pureList,channel):
        """
        Determines whether a measurement should be saved or emitted, filtering out values
        that exceed the device's maximum limit.

        If the measurement is below the predefined limit, it is either stored for batch 
        processing or emitted immediately depending on the operating mode. In batched mode, 
        the measurement and its raw value are appended to the provided lists. In normal mode, 
        the measurement is compared against the current maximum value and emitted through 
        the corresponding signals.

        :param listValues: List to store processed measurement values in batched mode.
        :param measurement: Processed measurement value.
        :param pureMeasurement: Raw measurement value from the device.
        :param pureList: List to store raw measurement values in batched mode.
        :param channel: Channel identifier for the measurement.
        :return: None
        """
        if self.isBashed:
            listValues.append(measurement)
            pureList.append(pureMeasurement)
            if channel=="A" and measurement>self.currentMaxValueA:
                self.currentMaxValueA=measurement
            if channel=="B" and measurement>self.currentMaxValueB:
                self.currentMaxValueB=measurement
            if channel=="C" and measurement>self.currentMaxValueC:
                self.currentMaxValueC=measurement
            if channel=="D" and measurement>self.currentMaxValueD:
                self.currentMaxValueD=measurement
        else:
            self.compareMaxValue(measurement,channel)
            self.dataSignal.emit(measurement,channel)
            self.dataPureSignal.emit(pureMeasurement,channel)
            
            
    def checkCorruptData(self, currentMeasurement, nextMeasurement):
        """
        Checks if a measurement is corrupt by comparing it to the next measurement.

        The function verifies whether the sequence number of the next measurement 
        is either the same or exactly one greater than the current one. If it is 
        neither, the current measurement is considered corrupt and should be skipped.

        :param currentMeasurement: Current measurement data.
        :param nextMeasurement: Next measurement data to compare against.
        :return: 1 if the current measurement is corrupt, 0 otherwise.
        """
        finalToSkip=0
        if nextMeasurement:
            if (currentMeasurement[1]+1)!=nextMeasurement[1] and ((currentMeasurement[1])!=nextMeasurement[1]):
                finalToSkip=1
        return finalToSkip

    def getRange(self, currentMeasurement,stopNumber):
        """
        Determines the valid range of stops to process for a measurement.

        This function calculates the maximum valid index range based on the expected 
        number of stops and the actual length of the measurement data. It ensures that 
        the processing does not exceed available data, which helps prevent errors in 
        cases where measurements are incomplete or corrupted.

        :param currentMeasurement: Current measurement data as a list.
        :param stopNumber: Expected number of stops for the measurement.
        :return: The validated number of stops to process.
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
            
            
    
    def isBashedMeasurement(self):
        """
        Determines whether measurements should be processed in batches.

        If the configured number of runs is greater than 50, the measurement mode 
        is set to batched; otherwise, it is set to normal.

        :return: None
        """
        if self.numberRunsSetting>50:
            self.isBashed=True
        else:
            self.isBashed=False
        
    def compareMaxValue(self,newValue,channel):
        """
        Checks if a new measurement value exceeds the current maximum for the given channel.

        If the new value is greater than the stored maximum for that channel, the 
        maximum is updated and a signal is emitted to notify that the histogram's 
        X-axis range should be adjusted.

        :param newValue: The new measurement value to compare.
        :param channel: The channel identifier ("A", "B", "C", or "D").
        :return: None
        """
        if channel=="A": 
            if newValue>self.currentMaxValueA:
                self.currentMaxValueA=newValue
                self.newMaxValueSignal.emit(newValue,"A")
        elif channel=="B": 
            if newValue>self.currentMaxValueB:
                self.currentMaxValueB=newValue
                self.newMaxValueSignal.emit(newValue,"B")
        elif channel=="C":
            if newValue>self.currentMaxValueC:
                self.currentMaxValueC=newValue
                self.newMaxValueSignal.emit(newValue,"C")
        elif channel=="D": 
            if newValue>self.currentMaxValueD:
                self.currentMaxValueD=newValue
                self.newMaxValueSignal.emit(newValue,"D")
    #Function to know if a dialog is open
    def dialogIsOpen(self):
        """
        Sets the 'openDialog' sentinel to False, indicating that no dialog is open.

        :return: None
        """
        self.openDialog=False 
    
    #Change the max Value if the mode is changed
    def changeMaxValue(self,channel,valueMax):
        """
        Changes the maximum value for the specified channel.

        :param channel: The channel for which the maximum value is to be changed (str).
        :param valueMax: The new maximum value to be set (float).
        :return: None
        """
        if channel=='A':
            self.currentMaxValueA=valueMax
        elif channel=='B':
            self.currentMaxValueB=valueMax
        elif channel=='C':
            self.currentMaxValueC=valueMax
        elif channel=='D':
            self.currentMaxValueD=valueMax

    #Add to the list if the mode is not changed
    def addChannelWarning(self,channel):
        """
        Adds the specified channel to the list of channels that need to change mode.

        :param channel: The channel to be added to the warning list (str).
        :return: None
        """
        if channel=='A':
            self.channelsToChange.append('A')
        elif channel=='B':
            self.channelsToChange.append('B')
        elif channel=='C':
            self.channelsToChange.append('C')
        elif channel=='D':
            self.channelsToChange.append('D')

    def saveCurrentSettings(self):
        """
        Saves the current configuration settings of the device.

        This function retrieves the general and per-channel configuration parameters 
        from the connected device and stores them in the corresponding instance variables. 
        These values include run counts, thresholds, modes, number of stops, stop edge 
        types, and stop masks for each channel.

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
        Applies the stored configuration settings to the device.

        This function sends the previously saved general and per-channel 
        configuration parameters back to the connected device. These include 
        run counts, thresholds, average cycles, modes, number of stops, 
        stop edge types, and stop masks for each channel. After applying the 
        settings, it enables or disables the channels according to the stored 
        configuration.

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
        self.enableDisableChannels()
        
        

    @Slot()
    def stop(self):
        """
        Stops the measurement process and closes the thread.

        This method emits a signal to indicate that the thread has been stopped
        and sets the running flag to False.

        :return: None
        """
        self.threadCreated.emit(1)
        self.itsRunning=False