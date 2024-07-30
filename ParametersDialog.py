from PySide2.QtCore import *
from PySide2.QtCore import QObject
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import time

class CountParameters():
    def __init__(self,channelComboBox: QComboBox, device, measurementLabel: QLabel, statusLabel: QLabel, informationLabel: QLabel,
                 startButton:QPushButton,stopButton:QPushButton,dialog: QDialog, g2Graphic, mainWindow):
        super().__init__()
        self.mainWindow=mainWindow
        self.dialog=dialog
        self.g2Graphic=g2Graphic
        self.channelComboBox=channelComboBox
        self.device=device
        self.measurementLabel=measurementLabel
        self.statusLabel=statusLabel
        self.informationLabel=informationLabel
        self.startButton=startButton
        self.stopButton=stopButton
        #Init the buttons
        self.stopButton.setEnabled(False)
        #Connect the ComboBox change function
        self.channelComboBox.currentIndexChanged.connect(self.changeComboBox)
        #Connect the startstopButtons
        self.startButton.clicked.connect(self.startMeasurement)
        self.stopButton.clicked.connect(self.stopMeasurement)
        #Connect the dialog close
        self.dialog.finished.connect(self.dialogClosed)
        #Sentinel in order to know if there is a current measurement
        self.currentMeasurement=False
        
    def startMeasurement(self):
        self.startButton.setEnabled(False)
        self.channelComboBox.setEnabled(False)
        self.determineChannel()
        self.oldSettings()
        
        self.worker=WorkerThreadParameters(self.device,self.selectedChannel,self.currentChannelLabel)
        self.worker.finished.connect(self.evt_worker_finished)
        self.worker.updateLabel.connect(self.updateMeasuredLabel)
        self.worker.updateStatus.connect(self.updateStatusLabel)
        self.worker.start()
        self.currentMeasurement=True
        self.stopButton.setEnabled(True)
        
    def evt_worker_finished(self):
        self.afterStop()
        
    def afterStop(self):
        self.currentMeasurement=False
        self.statusLabel.setText("Not running")
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.channelComboBox.setEnabled(True)
        self.changeOldSettings()
        
    
    def determineChannel(self):
        self.currentChannelLabel=self.channelComboBox.currentText()
        if self.channelComboBox.currentIndex()==0:
            self.selectedChannel=self.device.ch1
            self.device.ch1.enableChannel()
            self.device.ch2.disableChannel()
            self.device.ch3.disableChannel()
            self.device.ch4.disableChannel()
        elif self.channelComboBox.currentIndex()==1:
            self.selectedChannel=self.device.ch2
            self.device.ch1.disableChannel()
            self.device.ch2.enableChannel()
            self.device.ch3.disableChannel()
            self.device.ch4.disableChannel()
        elif self.channelComboBox.currentIndex()==2:
            self.selectedChannel=self.device.ch3
            self.device.ch1.disableChannel()
            self.device.ch2.disableChannel()
            self.device.ch3.enableChannel()
            self.device.ch4.disableChannel()
        elif self.channelComboBox.currentIndex()==3:
            self.selectedChannel=self.device.ch4
            self.device.ch1.disableChannel()
            self.device.ch2.disableChannel()
            self.device.ch3.disableChannel()
            self.device.ch4.enableChannel()
    
    def stopMeasurement(self):
        self.worker.stop()
        self.afterStop()
    
    def changeOldSettings(self):
        self.device.setNumberOfRuns(self.oldNumberRuns)
        self.selectedChannel.setNumberOfStops(self.oldStopsNumber)
        self.selectedChannel.setStopMask(self.oldStopMask)
        self.selectedChannel.setAverageCycles(self.oldAverageCycles)
        
        
    
    def changeComboBox(self):
        self.informationLabel.setText("Mean time between events of "+ self.channelComboBox.currentText()+":")
        
    #Function to get all the current settings 
    def oldSettings(self):
        self.oldNumberRuns=self.device.getNumberOfRuns()
        self.oldStopsNumber=self.selectedChannel.getNumberOfStops()
        self.oldStopMask=self.selectedChannel.getStopMask()
        self.oldAverageCycles=self.selectedChannel.getAverageCycles()
        
    def updateMeasuredLabel(self,labelText):
        self.measurementLabel.setText(labelText)
    def updateStatusLabel(self,labelText):
        self.statusLabel.setText(labelText)
    
    def dialogClosed(self):
        if self.g2Graphic!=None:
            self.g2Graphic.timerStatus.start(500)
            print("Se reinicia el timer de g2 measurements")
        if self.currentMeasurement:
            reply = QMessageBox.question(self.mainWindow, 'Measurement Running',
                                         "There is a measurement running. Do you really want to close?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.worker.stop()
                while self.currentMeasurement:
                    time.sleep(0.5)
                self.dialog.event.accept()
            else:
                self.dialog.event.ignore()
        else:
            self.dialog.event.accept()

class WorkerThreadParameters(QThread):
    updateLabel = Signal(str)
    updateStatus = Signal(str)
    def __init__(self,device,selectedChannel,channelLabel):
        super().__init__()
        self._is_running=True
        self.device=device
        self.channelLabel=channelLabel
        self.selectedChannel=selectedChannel
        self.measurements=[]
        self.currentProgres=""
        self.currentProblems=""
    
    def run(self):
        j=1
        self.updateStatus.emit("Se ejecuta")
        while j<21 and self._is_running:
            
            self.currentProgres="Running: "+str(round(j*5))+"%"
            self.takeMeasurement()
            self.getAverage()
            j+=1
            
    
    def takeMeasurement(self):
        self.device.setNumberOfRuns(100)
        self.selectedChannel.setNumberOfStops(2)
        self.selectedChannel.setStopMask(0)
        self.selectedChannel.setAverageCycles(1)
        measure=self.device.measure()
        countNoStarts=0
        countNoAnyMeasurementsChannel=0
        countNoTwoMeasurementsChannel=0
        if len(measure)==0:
            self.currentProblems=" Start Channel is not taking measurements"
            self.updateStatus.emit(self.currentProgres+self.currentProblems)
        else:
            for i in measure:
                if len(i)==0:
                    countNoStarts+=1
                elif len(i)==5:
                    if i[3]==-1 and i[4]==-1:
                        countNoAnyMeasurementsChannel+=1
                    elif i[3]==-1 or  i[4]==-1:
                        countNoTwoMeasurementsChannel+=1
                    else:
                        stopStopDifference=i[4]-i[3]
                        self.measurements.append(stopStopDifference)
            if countNoAnyMeasurementsChannel>=70:
                self.currentProblems=" "+self.channelLabel+" is not taking measurements"
                self.updateStatus.emit(self.currentProgres+self.currentProblems)
            elif countNoTwoMeasurementsChannel>=70:
                self.currentProblems="Can not get two stops from "+self.channelLabel
                self.updateStatus.emit(self.currentProgres+self.currentProblems)
            else:
                self.currentProblems=""
                self.updateStatus.emit(self.currentProgres+self.currentProblems)
    
    def getAverage(self):
        if len(self.measurements)==0:
            self.updateLabel.emit("Undefined")
        else:
            total=len(self.measurements)
            totalSum=sum(self.measurements)
            average=totalSum/total
            unitsDivFacList=self.getUnits(average)
            units=unitsDivFacList[0]
            divisionFactor=unitsDivFacList[1]
            newAverage=round(average/divisionFactor,2)
            self.updateLabel.emit(str(newAverage)+" "+units)
            
    def getUnits(self,average):
        if average < 1e3:
            return ["ps",1]
        elif average < 1e6:
            return ["ns",10**3]
        elif average < 1e9:
            return ["µs",10**6]
        elif average < 1e12:
            return ["ms",10**9]
        
        pass
            
    def stop(self):
        self._is_running=False
        self.updateStatus.emit("Ending measurement")
                
                        
                
                        
                    
        
        
        