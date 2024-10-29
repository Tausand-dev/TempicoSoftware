from PySide2.QtCore import *
from PySide2.QtCore import QObject
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import bisect
import createsavefile as savefile
import datetime
import time
class g2Graphic():
    def __init__(self, parent, comboBoxChannel1: QComboBox, comboBoxChannel2:QComboBox, startButton:QPushButton,stopButton:QPushButton,
                 saveDataButton:QPushButton, savePlotButton: QPushButton,getDataLabelN1:QLabel,getDataLabelN2:QLabel, statusLabel:QLabel, pointLabel:QLabel,
                 init_sentinel,graphicFrame:QFrame, comboBoxBin: QComboBox,*args, **kwargs):
        super().__init__()
        #MainWindow
        self.parent=parent
        self.comboBoxBin=comboBoxBin
        #InitDevice
        self.device=self.parent.conectedDevice
        #Start Stop Buttons
        self.startButton=startButton
        self.stopButton=stopButton
        #Save Buttons
        self.saveDataButton=saveDataButton
        self.savePlotButton=savePlotButton
        #Init the buttons
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        #Labels
        self.getDataLabelN1=getDataLabelN1
        self.getDataLabelN2=getDataLabelN2
        self.statusLabel=statusLabel
        self.pointLabel=pointLabel
        
        #Channel1g2measurement
        self.comboBoxChannel1=comboBoxChannel1
        #Channel2g2measurement
        self.comboBoxChannel2=comboBoxChannel2
        if init_sentinel==0:
            self.comboBoxChannel1.setCurrentIndex(0)
            self.comboBoxChannel2.setCurrentIndex(1)
        #sentinel for thread
        self.threadSentinel=False
        self.oldIndexChannel1=self.comboBoxChannel1.currentIndex()
        self.oldIndexChannel2=self.comboBoxChannel2.currentIndex()
        #Init graphic widget
        #Create a horizonalLayout
        self.graphic_layout = QHBoxLayout(graphicFrame)
        self.win_g2=pg.GraphicsLayoutWidget()
        self.win_g2.setBackground('w')
        self.plotg2=self.win_g2.addPlot()
        self.plotg2.showGrid(x=True, y=True)
        #TO DO:Change labels
        currentTextA=self.comboBoxChannel1.currentText().replace("Channel ","")
        currentTextB=self.comboBoxChannel2.currentText().replace("Channel ","")
        self.plotg2.setLabel('left','g(2) '+currentTextA+currentTextB)
        self.plotg2.setLabel('bottom','tau')
        self.plotg2.setMouseEnabled(x=True, y=True)
        self.graphic_layout.addWidget(self.win_g2)
        #ChangeComboBoxAction
        self.comboBoxChannel1.currentIndexChanged.connect(self.on_combobox_changed1)
        self.comboBoxChannel2.currentIndexChanged.connect(self.on_combobox_changed2)
        #ConnectStartButton
        self.startButton.clicked.connect(self.startmeasurement)
        self.stopButton.clicked.connect(self.stopmeasurement)
        self.curve = self.plotg2.plot(pen='b')
        self.savePlotButton.clicked.connect(self.savePlotg2)
        self.sentinelParameter=False
        #Create the values for g2
        self.g2Values=[]
        #Create the time domain for g2 values
        self.tauValues=[]
        #Create the time differences len values
        self.totalTimeDifferenceValue=0
        self.threadCreated=False
        self.timerStatus=QTimer()
        self.timerStatus.timeout.connect(self.check_device_status)
        self.notStartMeasurements=False
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        self.saveDataButton.clicked.connect(self.saveg2Data)
        self.unitsLabel=''
        if self.device==None:
            self.disconnectDevice()
        else:
            self.timerStatus.start(500)
        
        
        
        
    #Two channels could not be the same, Change channel 1
    #Change the label of the graphic
    def comboBoxInitMeasurement(self):
        current_text1=self.comboBoxChannel1.currentText().replace("Channel ","")
        current_text2=self.comboBoxChannel2.currentText().replace("Channel ","")
        self.plotg2.setLabel('left','g(2) '+current_text1+current_text2)
    
    def on_combobox_changed1(self):
        if self.comboBoxChannel1.currentIndex()==self.comboBoxChannel2.currentIndex():
            self.comboBoxChannel1.setCurrentIndex(self.oldIndexChannel1)
        else:
            self.oldIndexChannel1=self.comboBoxChannel1.currentIndex()
                
    #Two channels could not be the same, changeChannel2
    #Change the label of the graphic
    def on_combobox_changed2(self):
        if self.comboBoxChannel2.currentIndex()==self.comboBoxChannel1.currentIndex():
            self.comboBoxChannel2.setCurrentIndex(self.oldIndexChannel2)
        else:
            self.oldIndexChannel2=self.comboBoxChannel2.currentIndex()
    
    #TO DO: Implement the actions of start-stop
    def startmeasurement(self):
        self.unitsLabel=''
        self.timerStatus.stop()
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        self.parent.disconnectButton.setEnabled(False)
        try:
            self.oldSettings()
        except:
            pass
        self.g2Sentinel=False
        self.notStartMeasurements=False
        self.totalTimeDifferenceValue=0
        self.threadCreated=False
        self.sentinelParameter=False
        self.threadSentinel=False
        self.channel1Selected=self.comboBoxChannel1.currentText()
        self.channel2Selected=self.comboBoxChannel2.currentText()
        self.updateg2Values([],[],0)
        self.comboBoxInitMeasurement()
        self.startButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.comboBoxChannel1.setEnabled(False)
        self.comboBoxChannel2.setEnabled(False)
        self.comboBoxBin.setEnabled(False)
        self.parent.tabs.setTabEnabled(0,False)
        self.statusLabel.setText("Running measurement 0%")
        self.drawPoint(0)
        self.worker=WorkerThread(self,self.statusLabel,self.device,
                                 self.comboBoxChannel1,self.comboBoxChannel2,self.oldIndexChannel1,self.oldIndexChannel2,self.getDataLabelN1,self.getDataLabelN2,self.comboBoxBin)
        self.worker.finished.connect(self.evt_worker_finished)
        self.worker.update_label.connect(self.update_plot_label)
        self.worker.updateg2.connect(self.updateg2Values)
        self.worker.ThrdFin.connect(self.CreatedFin)
        self.worker.dialogSignal.connect(self.BinWidthAcceptDialog)
        self.worker.start()
        self.stopButton.setEnabled(True)
    
    def changeNotStartMeasurements(self,sentinel):
        if sentinel==1:
            self.notStartMeasurements=True
        elif sentinel==0:
            self.notStartMeasurements=False
    
    
    #Function created to get old settings before measurement
    def oldSettings(self):
        try:
            oldSettings=self.device.getSettings()
            strNumberStops1=oldSettings[2]
            strNumberStops2=oldSettings[9]
            strNumberStops3=oldSettings[16]
            strNumberStops4=oldSettings[23]
            strStopMask1=oldSettings[6]
            strStopMask2=oldSettings[13]
            strStopMask3=oldSettings[20]
            strStopMask4=oldSettings[27]
            strNumberRuns=oldSettings[28]
            self.numberStops1=int(strNumberStops1.split(' ')[-1])
            self.numberStops2=int(strNumberStops2.split(' ')[-1])
            self.numberStops3=int(strNumberStops3.split(' ')[-1])
            self.numberStops4=int(strNumberStops4.split(' ')[-1])
            self.stopMask1=int(strStopMask1.split(' ')[-1])
            self.stopMask2=int(strStopMask2.split(' ')[-1])
            self.stopMask3=int(strStopMask3.split(' ')[-1])
            self.stopMask4=int(strStopMask4.split(' ')[-1])
            self.numberRuns=int(strNumberRuns.split(' ')[-1])
        except NameError:
            print(NameError)
    
    def changeToNewSettings(self):  
        try:
            self.device.ch1.setNumberOfStops(self.numberStops1)
            self.device.ch2.setNumberOfStops(self.numberStops2)
            self.device.ch3.setNumberOfStops(self.numberStops3)
            self.device.ch4.setNumberOfStops(self.numberStops4)
            self.device.ch1.setStopMask(self.stopMask1)
            self.device.ch2.setStopMask(self.stopMask2)
            self.device.ch3.setStopMask(self.stopMask3)
            self.device.ch4.setStopMask(self.stopMask4)
            self.device.setNumberOfRuns(self.numberRuns)
        except NameError:
            print(NameError)
        
    
    def stopmeasurement(self):
        self.stopButton.setEnabled(False)
        if not self.threadSentinel:
            if self.threadCreated:
                #self.worker.update_label.disconnect(self.update_plot_label)
                #self.worker.updateg2.disconnect(self.updateg2Values)
                #self.worker.ThrdFin.disconnect(self.CreatedFin)
                self.worker.stop()
            else:
                self.enableAfterStop()
    def enableAfterStop(self):
        if self.totalTimeDifferenceValue>0:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.comboBoxChannel1.setEnabled(True)
        self.comboBoxChannel2.setEnabled(True)
        self.comboBoxBin.setEnabled(True)
        self.parent.disconnectButton.setEnabled(True)
        try:
            self.changeToNewSettings()
        except:
            pass 
        self.statusLabel.setText("No measurement running")
        self.drawPoint(1)
    
    def disconnectDevice(self):
        self.timerStatus.stop()
        if self.threadCreated:
            self.worker.stop()
        self.parent.connectButton.setEnabled(True)
        self.parent.disconnectButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
    
    def connectDevice(self):
        self.timerStatus.start(500)
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.device=self.parent.conectedDevice
           
    
    def drawPoint(self,sentinel):
        pixmap = QPixmap(self.pointLabel.size())
        pixmap.fill(Qt.transparent)  
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if sentinel==1:
            painter.setBrush(QColor(128, 128, 128))  
        elif sentinel==0:
            painter.setBrush(QColor(0, 255, 0))
        elif sentinel==2:
            painter.setBrush(QColor(255, 255, 0))
        elif sentinel==3:
            painter.setBrush(QColor(255, 165, 0))
            
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.pointLabel.width(), self.pointLabel.height())  
        painter.end()
        self.pointLabel.setPixmap(pixmap)  
    def no_measurements_dialog(self,Channel1,Channel2):
        if not self.notStartMeasurements:
            message_box = QMessageBox(self.parent)
            message_box.setWindowTitle("Measurements Not Found")
            message_box.setText("Cannot get measurements from the start channel.\nCheck the Tempico connections or verify the input signal")
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
        else:
            
            channelsText=""
            sentinelChannel1=False
            if Channel1!=None:
                channelsText+=Channel1
                sentinelChannel1=True
            if Channel2!=None and sentinelChannel1:
                channelsText+=", "+Channel2
            elif Channel2!=None and not sentinelChannel1:
                channelsText+=Channel2
                
                
            message_box = QMessageBox(self.parent)
            message_box.setWindowTitle("Measurements Not Found")
            message_box.setText("Cannot get measurements from the selected channels.\nCheck the Tempico connections or verify the following channels: \n"+channelsText)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            self.getDataLabelN1.setText("Undefined")
            self.getDataLabelN2.setText("Undefined")
    
    def notTotalg2(self):
        message_box = QMessageBox(self.parent)
        message_box.setWindowTitle("g2 with insufficient data")
        message_box.setText("The obtained g2 does not have sufficient data, as it contains fewer than 5000 time differences. For a more accurate measurement, it is advisable to collect the data again.")
        pixmap= QPixmap('./Sources/abacus_small.ico')
        message_box.setIconPixmap(pixmap)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
        
    def evt_worker_finished(self):
        if self.totalTimeDifferenceValue<5000 and self.g2Sentinel and self.totalTimeDifferenceValue!=0:
            self.notTotalg2()
        if self.threadSentinel:
            self.parent.tabs.setTabEnabled(0,True)
        elif not self.threadSentinel and self.sentinelParameter:
            dataTimeDifference1=self.worker.timeDifferenceChannel1
            dataTimeDifference2=self.worker.timeDifferenceChannel2
            if len(dataTimeDifference1)>=1000 and len(dataTimeDifference2)>=1000:
                self.parent.tabs.setTabEnabled(0,True)
            elif len(dataTimeDifference1)>=1000 and len(dataTimeDifference2)<1000:
                self.no_measurements_dialog(None,self.comboBoxChannel2.currentText())
                self.parent.tabs.setTabEnabled(0,True)
            elif len(dataTimeDifference1)<1000 and len(dataTimeDifference2)>=1000:
                self.no_measurements_dialog(self.comboBoxChannel1.currentText(),None)
                self.parent.tabs.setTabEnabled(0,True)
            elif len(dataTimeDifference1)<1000 and len(dataTimeDifference2)<1000:
                self.no_measurements_dialog(self.comboBoxChannel1.currentText(),self.comboBoxChannel2.currentText())
                self.parent.tabs.setTabEnabled(0,True)
        self.parent.tabs.setTabEnabled(0,True)
        self.enableAfterStop()
        self.threadCreated=False
        self.timerStatus.start(500)
        
    
    def average_counts(self,channelArray):
        total_values=len(channelArray)
        total_sum=sum(channelArray)
        total_average=total_sum/total_values
        return total_average
    
    def changeTrheadSentinel(self):
        self.threadSentinel=True
        
    def changesentinelParameter(self):
        self.sentinelParameter=True
    
    def beging2Measurement(self):
        self.g2Sentinel=True
    
    def update_plot_label(self, text):
        self.unitsLabel='tau ('+text+')'
        self.plotg2.setLabel('bottom', 'tau ('+text+')')

    def updateg2Values(self,g2values,tauValues,lenCoincidences):
        self.g2Values=g2values
        self.tauValues=tauValues
        self.totalTimeDifferenceValue=lenCoincidences
        print("Se actualiza")
        self.curve.setData(self.tauValues,self.g2Values)
    
    def CreatedFin(self):
        self.threadCreated=True
    
    def BinWidthAcceptDialog(self):
        dialog = QDialog(self.parent)
        dialog.setObjectName("ConfirmationDialog")
        dialog.resize(300, 100)
        dialog.setWindowTitle("Confirm")
        verticalLayout_2 = QVBoxLayout(dialog)
        verticalLayout_2.setObjectName("verticalLayout_2")
        messageLabel = QLabel(dialog)
        messageLabel.setObjectName("messageLabel")
        font = messageLabel.font()
        font.setPointSize(10)
        messageLabel.setFont(font)
        messageLabel.setText("The chosen bin width generates a histogram with too much data,\n"
                             "which can result in the application having low performance or,\n"
                             "in the worst case, crashing. However, all of this will depend on\n"
                             "your system's specifications.\n\n"
                             "Would you like to continue the measurement with the chosen bin?")
        messageLabel.setAlignment(Qt.AlignJustify)
        verticalLayout_2.addWidget(messageLabel)
        # Layout for the buttons
        buttonLayout = QHBoxLayout()
        yesButton = QPushButton(dialog)
        yesButton.setObjectName("yesButton")
        yesButton.setText("Sí")
        buttonLayout.addWidget(yesButton)
        noButton = QPushButton(dialog)
        noButton.setObjectName("noButton")
        noButton.setText("No")
        buttonLayout.addWidget(noButton)
        verticalLayout_2.addLayout(buttonLayout)
        QMetaObject.connectSlotsByName(dialog)
        # Connect the buttons
        yesButton.clicked.connect(dialog.accept)
        noButton.clicked.connect(dialog.reject)
        dialog.accepted.connect(self.worker.accepted)
        dialog.rejected.connect(self.worker.rejected)
        dialog.exec_()
    #Function created to create a warning when the the device is disconnected
    def check_device_status(self):
        try:
            self.device.readIdnFromDevice()
        except:
            if self.threadCreated:
                self.worker.stop()
            self.disconnectDevice()
            msg_box = QMessageBox(self.parent)
            msg_box.setText("Connection with the device has been lost")
            msg_box.setWindowTitle("Connection Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
                
        
    def savePlotg2(self):
        #try:
            graph_names=[]
            #Open select the format
            dialog =QDialog(self.parent)    
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
            
            # Conectar el botón "Accept" al método accept del diálogo
            accepButton.clicked.connect(dialog.accept)
            if dialog.exec_()==QDialog.Accepted:
                selected_format=FormatBox.currentText()
                exporter=pg.exporters.ImageExporter(self.plotg2)
                exporter.parameters()['width'] = 800
                exporter.parameters()['height'] = 600
                folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                current_date=datetime.datetime.now()
                current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                graph_name='g2Measurement'+current_date_str
                exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                initial_text="The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+ "with the following names:"
                text_route="\n"+graph_name+"."+selected_format
                graph_names.append(graph_name)
                message_box = QMessageBox(self.parent)
                message_box.setText(initial_text+text_route)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                # show successful save
                message_box.exec_()
                
        # except:
        #     message_box = QMessageBox(self.parent)
        #     message_box.setIcon(QMessageBox.Critical)
        #     message_box.setText("The plots could not be saved.")
        #     message_box.setWindowTitle("Error saving")
        #     message_box.setStandardButtons(QMessageBox.Ok)
        #     message_box.exec_()
    
    def saveg2Data(self):
        #Open select the format
        dialog = QDialog(self.parent)
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
                #Settings Channel 1
                N1RecordTime=self.getDataLabelN1.text()
                N2RecordTime=self.getDataLabelN2.text()
                if self.channel1Selected=="Channel A":
                    setting1="Channel A: \n"+ "Mode: "+str(self.device.ch1.getMode())+"\nN1/T1: "+N1RecordTime+"\n"
                elif self.channel1Selected=="Channel B":
                    setting1="Channel B: \n"+ "Mode: "+str(self.device.ch2.getMode())+"\nN1/T1: "+N1RecordTime+"\n"
                elif self.channel1Selected=="Channel C":
                    setting1="Channel C: \n"+ "Mode: "+str(self.device.ch3.getMode())+"\nN1/T1: "+N1RecordTime+"\n"
                elif self.channel1Selected=="Channel D":
                    setting1="Channel D: \n"+ "Mode: "+str(self.device.ch4.getMode())+"\nN1/T1: "+N1RecordTime+"\n"
                    
                #Settings Channel 2
                if self.channel2Selected=="Channel A":
                    setting2="Channel A: \n"+ "Mode: "+str(self.device.ch1.getMode())+"\nN2/T2: "+N2RecordTime
                elif self.channel2Selected=="Channel B":
                    setting2="Channel B: \n"+ "Mode: "+str(self.device.ch2.getMode())+"\nN2/T2: "+N2RecordTime
                elif self.channel2Selected=="Channel C":
                    setting2="Channel C: \n"+ "Mode: "+str(self.device.ch3.getMode())+"\nN2/T2: "+N2RecordTime
                elif self.channel2Selected=="Channel D":
                    setting2="Channel D: \n"+ "Mode: "+str(self.device.ch4.getMode())+"\nN2/T2: "+N2RecordTime


                settings=setting1+setting2
                filename="g2Measurement"+current_date_str
                data=[self.tauValues, self.g2Values]
                try:
                    savefile.save_g2_data(data,filename,folder_path,settings,selected_format, self.unitsLabel)
                    if selected_format=="txt":
                        self.oldtxtName=filename
                        self.sentinelsavetxt=1
                    elif selected_format=="csv":
                        self.oldcsvName=filename
                        self.sentinelsavecsv=1
                    elif selected_format=="dat":
                        self.olddatName=filename
                        self.sentinelsavedat=1
                    message_box = QMessageBox(self.parent)
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
                    message_box = QMessageBox(self.parent)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()         
            else:
                message_box = QMessageBox(self.parent)
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
                
    

class WorkerThread(QThread):
    update_label = Signal(str)
    updateg2= Signal(list,list,int)
    ThrdFin=Signal()
    stop_signal=Signal()
    dialogSignal=Signal()
    
    def __init__(self,g2Graphic, statusLabel,device,comboBoxChannel1,comboBoxChannel2,oldIndexChannel1,oldIndexChannel2,N1dataLabel,N2dataLabel,binwidth):
        super().__init__()
        self._is_running=True
        self.stop_signal.connect(self.stop)
        strList=binwidth.currentText().split(' ')
        multiplier=self.multiplier(strList[1])
        value=int(strList[0])
        self.binwidth=value*multiplier
        #Init the variables to take measurements
        #g2Graphic connection
        self.g2Graphic=g2Graphic
        self.parentg2=self.g2Graphic.parent
        #Main script connection
        self.device=device
        self.comboBoxChannel1=comboBoxChannel1
        self.statusLabel=statusLabel
        self.comboBoxChannel2=comboBoxChannel2
        self.oldIndexChannel1=oldIndexChannel1
        self.oldIndexChannel2=oldIndexChannel2
        self.oldIndexChannel1=self.oldIndexChannel1+1
        self.oldIndexChannel2=self.oldIndexChannel2+1
        self.conditionDifference=self.oldIndexChannel2>self.oldIndexChannel1
        #Initial data channels
        self.timeDifferenceChannel1=[]
        self.timeDifferenceChannel2=[]
        self.totalTime=0
        self.data_coincidente=[]
        self.N1dataLabel=N1dataLabel
        self.N2dataLabel=N2dataLabel
        
        
    #Thread to take the measurement
    def run(self):
        while self._is_running:
            self.ThrdFin.emit()
            self.take_measurement()
            if len(self.timeDifferenceChannel1)>=1000 and len(self.timeDifferenceChannel2)>=1000 and self._is_running:
                self.g2PrepareMeasurement()
                self.continueMeasurement=True
                if self.warningBinData:
                    self.continueMeasurement=False
                    self.dialogClose=False
                    self.dialogSignal.emit()
                    while not self.dialogClose:
                        time.sleep(0.5)
                if self.continueMeasurement:        
                    self.g2Graphic.drawPoint(0)
                    self.g2Graphic.beging2Measurement()
                    self.determinate_N1_N2()
                    if len(self.data_coincidente)>0:
                        self.calculate_total_time()
                        self.create_g2_data()
                j=1 
                while j <601 and self._is_running and self.continueMeasurement:  
                    self.checkStatus()
                    if not self._is_running:
                        break
                    percentage=round(j/6,1)
                    self.statusLabel.setText("Running measurement "+str(percentage)+"%")
                    self.g2_measurement()
                    j+=1
                self.g2Graphic.changeTrheadSentinel()
                self.stop()
            self.stop()
    #Accept and reject buttons for the dialog
    def accepted(self):
        self.continueMeasurement=True
        self.dialogClose=True
    def rejected(self):
            self.continueMeasurement=False
            self.dialogClose=True
            
        
    def calculate_total_time(self):
        self.totalTime=0
        for i in self.data_coincidente:
            self.totalTime+=abs(i)
    
    #THis function take the measurement in order to get the g2 function
    def take_measurement(self): 
        # Set up the measurement
        self.indexChannel1=self.comboBoxChannel1.currentIndex()
        self.indexChannel2=self.comboBoxChannel2.currentIndex()
        #Disable all channels
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        
        #Channel1
        if self.indexChannel1==0:
            self.device.ch1.enableChannel()
            self.currentChannel1=self.device.ch1
        elif self.indexChannel1==1:
            self.device.ch2.enableChannel()
            self.currentChannel1=self.device.ch2
        elif self.indexChannel1==2:
            self.device.ch3.enableChannel()
            self.currentChannel1=self.device.ch3
        elif self.indexChannel1==3:
            self.device.ch4.enableChannel()
            self.currentChannel1=self.device.ch4
        #Channel2
        if self.indexChannel2==0:
            self.device.ch1.enableChannel()
            self.currentChannel2=self.device.ch1
        elif self.indexChannel2==1:
            self.device.ch2.enableChannel()
            self.currentChannel2=self.device.ch2
        elif self.indexChannel2==2:
            self.device.ch3.enableChannel()
            self.currentChannel2=self.device.ch3
        elif self.indexChannel2==3:
            self.device.ch4.enableChannel()
            self.currentChannel2=self.device.ch4
        #Init to get the data 
        i=0
        sentinelData=False
        while i<10 and not sentinelData and self._is_running:
            percentage=i*10
            if i==0:
                self.statusLabel.setText("Taking parameters "+"0"+"%")
            elif len(self.timeDifferenceChannel1)>=1000 and len(self.timeDifferenceChannel2)>=1000:
                self.g2Graphic.drawPoint(0)
                self.statusLabel.setText("Taking parameters: 100%")
                sentinelData=True
            elif not self.g2Graphic.notStartMeasurements:
                self.g2Graphic.drawPoint(3)
                self.statusLabel.setText("Taking parameters: "+str(percentage)+"%"+" (start channel" + " is not taking measurements)")
            elif len(self.timeDifferenceChannel1)>=1000 and len(self.timeDifferenceChannel2)<1000:
                self.g2Graphic.drawPoint(3)
                self.statusLabel.setText("Taking parameters: "+str(percentage)+"%"+" (" + self.comboBoxChannel2.currentText()+ " is not taking measurements)")
            elif len(self.timeDifferenceChannel1)<1000 and len(self.timeDifferenceChannel2)>=1000:
                self.g2Graphic.drawPoint(3)
                self.statusLabel.setText("Taking parameters: "+str(percentage)+"%"+" (" + self.comboBoxChannel1.currentText()+ " is not taking measurements)")
            elif len(self.timeDifferenceChannel1)<1000 and len(self.timeDifferenceChannel2)<1000:
                self.g2Graphic.drawPoint(3)
                self.statusLabel.setText("Taking parameters: "+str(percentage)+"%"+" (" + self.comboBoxChannel1.currentText()+" and "+ self.comboBoxChannel2.currentText()+ " are not taking measurements)")
            self.initial_measurement()
            
            i+=1
        if i==10:
            self.g2Graphic.changesentinelParameter()
        
        
        
    #Taking the parameters in order to get the number of counts
    def initial_measurement(self):
        self.currentChannel1.setStopMask(0)
        self.currentChannel2.setStopMask(0)
        self.device.setNumberOfRuns(100)
        self.currentChannel1.setNumberOfStops(2)
        self.currentChannel2.setNumberOfStops(2)
        countNoStarts=0
        for i in range(10):
            try:
                self.checkStatus()
                if not self._is_running:
                    break   
                medicion=self.device.measure()
                if len(medicion)==0:
                    countNoStarts+=1
                for i in range(round(len(medicion)/2)):
                    currentMeasurementch1=medicion[i]
                    currentMeasurementch2=medicion[i+100]
                    getMeasurech1=False
                    getMeasurech2=False
                    if len(currentMeasurementch1)==0:
                        countNoStarts+=1
                    if len(currentMeasurementch2)==0:
                        countNoStarts+=1
                    if len(currentMeasurementch1)==5:
                        ch1stop_1=currentMeasurementch1[3]
                        ch1stop_2=currentMeasurementch1[4]
                        if ch1stop_1!=-1 and ch1stop_2!=-1:
                            stopDifference=abs(ch1stop_2-ch1stop_1)
                            getMeasurech1=True
                            self.timeDifferenceChannel1.append(stopDifference)
                    if len(currentMeasurementch2)==5:
                        ch2stop_1=currentMeasurementch2[3]
                        ch2stop_2=currentMeasurementch2[4]
                        if ch2stop_1!=-1 and ch2stop_2!=-1:
                            stopDifference=abs(ch2stop_2-ch2stop_1)
                            getMeasurech2=True
                            self.timeDifferenceChannel2.append(stopDifference)
                    if getMeasurech1 and getMeasurech2:
                        if self.conditionDifference:
                            stopDifference1=ch2stop_1-ch1stop_1
                        else:    
                            stopDifference1=ch1stop_1-ch2stop_1
                        self.data_coincidente.append(stopDifference1)
            except:
                pass
        if countNoStarts>=5:
            self.g2Graphic.changeNotStartMeasurements(0)
        else:
            self.g2Graphic.changeNotStartMeasurements(1)
            
    
    
    
    def checkStatus(self):
        try:
            self.device.readIdnFromDevice()
        except:
            self.stop()
        
    
    def get_g2_measurement(self):
        numberOfStops=5
        self.currentChannel1.setNumberOfStops(1)
        self.currentChannel2.setNumberOfStops(numberOfStops)
        old_data_coincidence=self.data_coincidente
        medicion=self.device.measure()
        print(self.device.getSettings())
        print(medicion)
        data_tuple=[]
        try:
            for i in range(100):
                dataA=medicion[i]
                dataB=medicion[i+100]
                tupla=(dataA,dataB)
                data_tuple.append(tupla)
            for i in data_tuple:
                if len(i[0])>0 and len(i[1])>0:
                    for j in range(numberOfStops):
                        if i[0][3]!=-1 and i[1][3+j]!=-1:
                            #cambiar el nombre de coincidencia
                            if self.conditionDifference:
                                stop_diference= i[1][3+j]-i[0][3]    
                            else:
                                stop_diference= i[0][3]-i[1][3+j] 
                            if stop_diference<= 4000000000:    
                                self.data_coincidente.append(stop_diference)
                    # if i[0][4]!=-1 and i[1][4]!=-1:
                    #     #cambiar el nombre de coincidencia
                    #     if self.conditionDifference:
                    #         stop_diference= i[1][4]-i[0][4]    
                    #     else:
                    #         stop_diference= i[0][4]-i[1][4]    
                    #     self.data_coincidente.append(stop_diference)
        except:
            print("Error")
        
    
    #Count the elements in the array between lower and upper
    def count_elements_in_range(self,arr, lower, upper):
        left_index = bisect.bisect_left(arr, lower)
        right_index = bisect.bisect_right(arr, upper)
        return right_index - left_index
    
    def create_g2_data(self):
        min_value=round(min(self.data_coincidente))
        max_value=round(max(self.data_coincidente))
        #Determine the max absolute value
        if abs(min_value)>abs(max_value):
            results=self.format_time(min_value*(-1))
            units=results[0]
            division_factor=results[1]
            lower_bound=min_value/division_factor
            upper_bound=(min_value*(-1))/division_factor
        else:
            #Determine units
            results=self.format_time(max_value)
            units=results[0]
            division_factor=results[1]
            lower_bound=max_value*(-1)/division_factor
            upper_bound=max_value/division_factor
                
        #TO DO: Change binwidth with the combo box value
        self.update_label.emit(units)
        self.domain_values=np.arange(lower_bound,upper_bound,self.binwidth/division_factor)
        self.g2_values=[]
        self.data_coincidente.sort()
        new_coincidence=self.data_coincidente.copy()
        for i in range(len(new_coincidence)):
            currentValue=new_coincidence[i]
            newValue=currentValue/division_factor
            new_coincidence[i]=newValue
        new_averageN1=self.averageTimeN1/division_factor
        new_averageN2=self.averageTimeN2/division_factor
        N_1=1/new_averageN1
        N_2=1/new_averageN2
        newBinWidth=self.binwidth/division_factor
        newTotalTime=self.totalTime/division_factor
        inverse_ct=N_1*N_2*newTotalTime*newBinWidth
        constant=1/inverse_ct
        #TO DO: Discover error in g2 measurement
        bin_edges = np.append(self.domain_values - newBinWidth / 2, self.domain_values[-1] + newBinWidth / 2)
        counts, _ = np.histogram(new_coincidence, bins=bin_edges)
        self.g2_values=counts*constant
        self.updateg2.emit(self.g2_values,self.domain_values,len(self.data_coincidente))
            
    #Function created to determine the units of the measurement
    def format_time(self,picoseconds):
        if picoseconds < 1e3:
            return ["ps",1]
        elif picoseconds < 1e6:
            return ["ns",10**3]
        elif picoseconds < 1e9:
            return ["µs",10**6]
        elif picoseconds < 1e12:
            return ["ms",10**9]

            
    
    def determinate_N1_N2(self):
        lenN1=len(self.timeDifferenceChannel1)
        lenN2=len(self.timeDifferenceChannel2)
        sumN1=sum(self.timeDifferenceChannel1)
        sumN2=sum(self.timeDifferenceChannel2)
        self.averageTimeN1=sumN1/lenN1
        self.averageTimeN2=sumN2/lenN2
        resultsTime1=self.format_time(self.averageTimeN1)
        resultsTime2=self.format_time(self.averageTimeN2)
        units1=resultsTime1[0]
        units2=resultsTime2[0]
        divisionFactor1=resultsTime1[1]
        divisionFactor2=resultsTime2[1]
        self.N1dataLabel.setText(str(round(self.averageTimeN1/divisionFactor1,2))+" "+units1)
        self.N2dataLabel.setText(str(round(self.averageTimeN2/divisionFactor2,2))+" "+units2)
    
    #Get the graphic of g2 measurement
    def g2_measurement(self):
        try:
            self.get_g2_measurement()
            if len(self.data_coincidente)>0:
                self.calculate_total_time()
                self.create_g2_data()
        except NameError as e:
            print(e)
    
    def coincidence_normalization(self,array,divisionFactor):
        for i in range(len(array)):
            currenValue=array[i]
            newValue=currenValue/divisionFactor
            array[i]=newValue
    
    #Function created to get the ratio beetween the stops and binwidth and show a dialog to the user
    def g2PrepareMeasurement(self):
        self.statusLabel.setText("Preparing measurement")
        self.g2Graphic.drawPoint(2)
        self.warningBinData=False
        self.dataAvailable=False
        if len(self.data_coincidente)>20:
            self.dataAvailable=True
        if self.dataAvailable:
            StopDifAbs=[]
            for i in self.data_coincidente:
                StopDifAbs.append(abs(i))
            maximumDifference=max(StopDifAbs)
            ratio=maximumDifference/self.binwidth
            if ratio>2500:
                self.warningBinData=True
            
            
    
    def multiplier(self,units):
        if units=='ps':
            mult=1
        elif units=='ns':
            mult=10**3
        elif units=='µs':
            mult=10**6
        return mult

    @Slot()
    def stop(self):
        self._is_running=False
        self.statusLabel.setText("Ending measurement")
        self.g2Graphic.drawPoint(2)
        
