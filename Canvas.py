from PySide2.QtCore import *
from PySide2.QtCore import QObject, Qt
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
from PySide2.QtWidgets import QWidget, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import datetime as dt
import numpy as np
import pyTempico as tempico
import pyAbacus as abacus
from settings import SettingsWindow
from generalsettings import GeneralSettingsWindow
from aboutWindow import AboutWindow
from StartStopHistograms import StartStopHistogramsWindow as SSHistogramsWindow
from ui_StarStopHistogram import Ui_HistogramaStartStop
from ui_lifetime import Ui_Form
from ui_g2measurement import Ui_G2
from ui_devicesDialog import Ui_Devices
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide2.QtCore import QTimer
import concurrent.futures
import time
#To do eliminate import
import random
import createsavefile as savefile
import datetime
from ui_settings import Ui_settings

#Create graphic design#
class Canvas():
    def __init__(self, parent, disconnect,device,check1,check2,check3,check4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D,connect,mainWindow,statusValue,statusPoint, *args, **kwargs):
        super().__init__()
        #Disconnect button
        self.disconnectButton= disconnect
        #Connect button
        self.connectButton= connect
        #Current measurement
        self.currentmeasurement=False
        ##----------------##
        self.startbutton=startbutton
        self.stopbutton=stopbutton
        self.savebutton=savebutton
        self.save_graphs=save_graph_1
        self.clear_channel_A=clear_channel_A
        self.clear_channel_B=clear_channel_B
        self.clear_channel_C=clear_channel_C
        self.clear_channel_D=clear_channel_D
        self.clear_channel_A.clicked.connect(self.clear_a)
        self.clear_channel_B.clicked.connect(self.clear_b)
        self.clear_channel_C.clicked.connect(self.clear_c)
        self.clear_channel_D.clicked.connect(self.clear_d)
        self.savebutton.clicked.connect(self.save_graphic)
        self.save_graphs.clicked.connect(self.save_plots)
        #Disable buttons init
        self.startbutton.setEnabled(True)
        self.savebutton.setEnabled(False)
        self.stopbutton.setEnabled(False)
        self.save_graphs.setEnabled(False)
        self.clear_channel_A.setEnabled(False)
        self.clear_channel_B.setEnabled(False)
        self.clear_channel_C.setEnabled(False)
        self.clear_channel_D.setEnabled(False)
        self.checkA=check1 
        self.checkB=check2
        self.checkC=check3
        self.checkD=check4
        self.checkA.setEnabled(True)
        self.checkB.setEnabled(True)
        self.checkC.setEnabled(True)
        self.checkD.setEnabled(True)
        self.setinelSaveA=False
        self.setinelSaveB=False
        self.setinelSaveC=False
        self.setinelSaveD=False

        ##---------------------------------##
        ##---------------------------------##
        ##-------Begin graphic layout------##
        ##---------------------------------##
        ##---------------------------------##
        self.parent=parent
        self.mainWindow=mainWindow
        self.gridlayout=QGridLayout(self.parent)
        self.startbutton.clicked.connect(self.start_graphic)
        self.stopbutton.clicked.connect(self.stop_graphic)
        
        #Get the channels
        self.device=device
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        ##---------------------------------##
        ##---------------------------------##
        ##------Begin the historam data----##
        ##---------------------------------##
        ##---------------------------------##
        self.dataA=[]
        self.histA, self.binsA=np.histogram(self.dataA,bins=60)
        #Creating the histogram plot channel B
        self.dataB=[]
        self.histB, self.binsB=np.histogram(self.dataB,bins=60)
        #Creating the histogram plot channel C
        self.dataC=[]
        self.histC, self.binsC=np.histogram(self.dataC,bins=60)
        #Creating the histogram plot channel D
        self.dataD=[]
        self.histD, self.binsD=np.histogram(self.dataD,bins=60)
        
        #Pure data
        self.datapureA=[]
        self.datapureB=[]
        self.datapureC=[]
        self.datapureD=[]
        
        #Sentinel thread worker thread created
        self.threadCreatedSentinel=False
        #get the value of the status Bar
        self.statusValue=statusValue
        self.statusPoint=statusPoint
        #Check if the zoom is not changed
        self.sentinelZoomChangedA=0 
        self.sentinelZoomChangedB=0
        self.sentinelZoomChangedC=0
        self.sentinelZoomChangedD=0
        #Check if the zoom is in code
        self.zoomCodeA=False
        self.zoomCodeB=False
        self.zoomCodeC=False
        self.zoomCodeD=False
        #Check if the device take a measurement before
        self.beforeMeasurement=False
        


        
    #Function to know the state of device   
    ##---------------------------------##
    ##---------------------------------##
    ##------Begin the create graphs----##
    ##---------------------------------##
    ##---------------------------------##  
           
        
    def create_graphs(self):
        #Set the timer to update the graphics
        self.timer=QTimer()
        self.dataA=[]
        self.dataB=[]
        self.dataC=[]
        self.dataD=[]
        self.datapureA=[]
        self.datapureB=[]
        self.datapureC=[]
        self.datapureD=[]
        # Create a list with the selected widgets
        widgets = []
        
        
        #Sentinels set in false
        self.setinelSaveA=False
        self.setinelSaveB=False
        self.setinelSaveC=False
        self.setinelSaveD=False
        
        #Set if the file is save with this sentinel
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0

        # Add widgets selected to the list
        if self.checkA.isChecked():
            #Init zoom variable
            self.is_zoomingA=False
            self.winA = pg.GraphicsLayoutWidget()
            self.winA.setBackground('w')
            self.plotA = self.winA.addPlot()
            self.plotA.showGrid(x=True, y=True)
            self.plotA.setLabel('left','Frequency')
            #Check the channel A
            self.plotA.setTitle('Start-Stop Channel A')
            if self.channel1.getMode()==1:
                self.plotA.setLabel('bottom', 'Start-stop time (ns)')
            else:
                self.plotA.setLabel('bottom', 'Start-stop time (ms)')
            self.plotA.setMouseEnabled(x=True, y=False)
            self.plotA.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.plotA.setXRange(0,5)
            self.clear_channel_A.setEnabled(True)
            widgets.append(self.winA)
            self.curveA=self.plotA.plot(self.binsA, self.histA, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150),name="ChannelA (Blue)")
            self.setinelSaveA=True
            self.viewBoxA=self.plotA.getViewBox()
            self.signalConnected =self.plotA.sigRangeChanged.connect(self.zoom_changedA)
            self.autoRangeButtonA=self.plotA.autoBtn
            self.autoRangeButtonA.clicked.disconnect()
            self.autoRangeButtonA.clicked.connect(self.autoRangeA)
            

        if self.checkB.isChecked():
            #Init zoom variable
            self.is_zoomingB=False
            self.winB = pg.GraphicsLayoutWidget()
            self.winB.setBackground('w')
            self.plotB = self.winB.addPlot()
            self.plotB.showGrid(x=True, y=True)
            self.plotB.setLabel('left','Frequency')
            #Check the channel B
            self.plotB.setTitle('Start-Stop Channel B')
            if self.channel2.getMode()==1:
                self.plotB.setLabel('bottom', 'Start-stop time (ns)')
            else:
                self.plotB.setLabel('bottom', 'Start-stop time (ms)')
            self.plotB.setMouseEnabled(x=True, y=False)
            self.plotB.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeB=True
            self.plotB.setXRange(0,5)
            self.clear_channel_B.setEnabled(True)
            widgets.append(self.winB)
            self.curveB=self.plotB.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150),name="ChannelB (Red)")
            self.setinelSaveB=True
            self.viewBoxB=self.plotB.getViewBox()
            self.viewBoxB.sigRangeChanged.connect(self.zoom_changedB)
            self.autoRangeButtonB=self.plotB.autoBtn
            self.autoRangeButtonB.clicked.disconnect()
            self.autoRangeButtonB.clicked.connect(self.autoRangeB)
            

        if self.checkC.isChecked():
            #Init zoom variable
            self.is_zoomingC=False
            self.winC = pg.GraphicsLayoutWidget()
            self.winC.setBackground('w')
            self.plotC = self.winC.addPlot()
            self.plotC.showGrid(x=True, y=True)
            self.plotC.setLabel('left','Frequency')
            #Check the channel C
            self.plotC.setTitle('Start-Stop Channel C')
            if self.channel3.getMode()==1:
                self.plotC.setLabel('bottom', 'Start-stop time (ns)')
            else:
                self.plotC.setLabel('bottom', 'Start-stop time (ms)')
            self.plotC.setMouseEnabled(x=True, y=False)
            self.plotC.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeC=True
            self.plotC.setXRange(0,5)
            self.clear_channel_C.setEnabled(True)
            widgets.append(self.winC)
            self.curveC=self.plotC.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150),name="ChannelC (Green)")
            self.setinelSaveC=True
            self.viewBoxC=self.plotC.getViewBox()
            self.plotC.sigRangeChanged.connect(self.zoom_changedC)
            self.autoRangeButtonC=self.plotC.autoBtn
            self.autoRangeButtonC.clicked.disconnect()
            self.autoRangeButtonC.clicked.connect(self.autoRangeC)
            

        if self.checkD.isChecked():
            #Init zoom variable
            self.is_zoomingD=False
            self.winD = pg.GraphicsLayoutWidget()
            self.winD.setBackground('w')
            self.plotD = self.winD.addPlot()
            self.plotD.showGrid(x=True, y=True)
            self.plotD.setLabel('left','Frequency')
            #Check the channel D
            self.plotD.setTitle('Start-Stop Channel D')
            if self.channel4.getMode()==1:
                self.plotD.setLabel('bottom', 'Start-stop time (ns)')
            else:
                self.plotD.setLabel('bottom', 'Start-stop time (ms)')
            self.plotD.setMouseEnabled(x=True, y=False)
            self.plotD.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeD=True
            self.plotD.setXRange(0,5)
            self.clear_channel_D.setEnabled(True)
            widgets.append(self.winD)
            self.curveD=self.plotD.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150),name="ChannelD (Yellow)")
            self.setinelSaveD=True
            self.viewBoxD=self.plotD.getViewBox()
            self.plotD.sigRangeChanged.connect(self.zoom_changedD)
            self.autoRangeButtonD=self.plotD.autoBtn
            self.autoRangeButtonD.clicked.disconnect()
            self.autoRangeButtonD.clicked.connect(self.autoRangeD)
            

        # Clear the widget
        for i in reversed(range(self.gridlayout.count())):
            widget_to_remove = self.gridlayout.itemAt(i).widget()
            self.gridlayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Put the widgets 
        num_widgets = len(widgets)
        if num_widgets == 1:
            self.gridlayout.addWidget(widgets[0], 0, 0, 2, 2)
        elif num_widgets == 2:
            self.gridlayout.addWidget(widgets[0], 0, 0, 1, 2)
            self.gridlayout.addWidget(widgets[1], 1, 0, 1, 2)
        elif num_widgets == 3:
            self.gridlayout.addWidget(widgets[0], 0, 0)
            self.gridlayout.addWidget(widgets[1], 0, 1)
            self.gridlayout.addWidget(widgets[2], 1, 0, 1, 2)
        elif num_widgets == 4:
            self.gridlayout.addWidget(widgets[0], 0, 0)
            self.gridlayout.addWidget(widgets[1], 0, 1)
            self.gridlayout.addWidget(widgets[2], 1, 0)
            self.gridlayout.addWidget(widgets[3], 1, 1)
            
        #Crete the worker Thread
        self.worker=WorkerThreadStartStopHistogram(self.parent,self.device,self.setinelSaveA,self.setinelSaveB,self.setinelSaveC,self.setinelSaveD)
        self.worker.finished.connect(self.threadComplete)
        self.worker.dataPureSignal.connect(self.updateDataPure)
        self.worker.dataSignal.connect(self.updateSignal)
        self.worker.threadCreated.connect(self.threadRunning)
        self.worker.dialogInit.connect(self.createDialog)
        self.worker.colorValue.connect(self.changeColorThread)
        self.worker.stringValue.connect(self.changeStatusThread)
        self.worker.dialogSignal.connect(self.dialogChangeMode)
        self.worker.newMaxValueSignal.connect(self.changeZoomMax)
        self.worker.start()
        
    
    
    ##---------------------------------##
    ##---------------------------------##
    ##--Begin with start-stop buttons--##
    ##---------------------------------##
    ##---------------------------------##  
    
    
    def start_graphic(self):
        if (not self.checkA.isChecked() and not self.checkB.isChecked() and not self.checkC.isChecked() and not self.checkD.isChecked()):
            message_box = QMessageBox(self.parent)
            message_box.setText("You must select at least one channel before starting a measurement.")
            message_box.setWindowTitle("Select a channel")
            message_box.setStandardButtons(QMessageBox.Ok)
            pixmap= QPixmap("/Sources/abacus_small.ico")
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        else: 
            self.sentinelZoomChangedA=0
            self.sentinelZoomChangedB=0
            self.sentinelZoomChangedC=0
            self.sentinelZoomChangedD=0
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.disconnectButton.setEnabled(False)
            self.currentmeasurement=True
            self.create_graphs()
            self.statusValue.setText("Measurement running")
            self.changeStatusColor(1)
            self.stopbutton.setEnabled(True)
            self.startbutton.setEnabled(False)
            self.checkA.setEnabled(False)
            self.checkB.setEnabled(False)
            self.checkC.setEnabled(False)
            self.checkD.setEnabled(False)
            self.savebutton.setEnabled(False)
    
    def hide_graphic2(self):
        self.startbutton.setEnabled(False)
        self.stopbutton.setEnabled(False)
        
    
    def show_graphic(self, device_new):
        self.device=device_new
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        self.startbutton.setEnabled(True)
        
    def stop_graphic(self):
        if self.threadCreatedSentinel:
            self.worker.stop()
            time.sleep(1)
        self.beforeMeasurement=True
        self.statusValue.setText("No measurement running")
        self.changeStatusColor(0)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.disconnectButton.setEnabled(True)
        self.currentmeasurement=False
        self.stopbutton.setEnabled(False)
        self.startbutton.setEnabled(True)
        self.savebutton.setEnabled(True)
        self.save_graphs.setEnabled(True)
        self.clear_channel_A.setEnabled(False)
        self.clear_channel_B.setEnabled(False)
        self.clear_channel_C.setEnabled(False)
        self.clear_channel_D.setEnabled(False)
        self.checkA.setEnabled(True)
        self.checkB.setEnabled(True)
        self.checkC.setEnabled(True)
        self.checkD.setEnabled(True)
    
    #Future function if we want to add the option of number of measurements
    def threadComplete(self):
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.threadCreated=False
        self.stop_graphic()
    
    
        
    ##---------------------------------##
    ##---------------------------------##
    ##------Clear graphics buttons-----##
    ##---------------------------------##
    ##---------------------------------##  
    
    def clear_a(self):
        self.dataA=[]
        #self.datapureA=[]
        
    def clear_b(self):
        self.dataB=[]
        self.datapureB=[]
    
    def clear_c(self):
        self.dataC=[]
        self.datapureC=[]
    
    def clear_d(self):
        self.dataD=[]
        self.datapureD=[]
    
    
    def update_histogram(self, data, curve, indexChannel):
        # Calculate the histogram
        if indexChannel=="A":
            self.zoomCodeA=True
            x_range = self.viewBoxA.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
            
            
        elif indexChannel == "B":
            self.zoomCodeB=True
            x_range = self.viewBoxB.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
        elif indexChannel == "C":
            self.zoomCodeC=True
            x_range = self.viewBoxC.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
        elif indexChannel == "D":
            self.zoomCodeD=True
            x_range = self.viewBoxD.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
        hist, _ = np.histogram(data, bins=binsU)
        curve.setData(binsU, hist, fillLevel=0)
        
    
    ##-------------------------------------------##
    ##-------------------------------------------##
    ##--Get the histogram bins according to zoom-##
    ##-------------------------------------------##
    ##-------------------------------------------## 
    
    
    def zoom_changedA(self):
        if self.zoomCodeA:
            print("Zoom de codigo")
        else:
            self.sentinelZoomChangedA+=1
            print("Zoom de usuario")
        # Function called for graphA zoom 
        x_range = self.viewBoxA.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsA = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histA, _ = np.histogram(self.dataA, bins=binsA)
        self.curveA.setData(binsA, self.histA)  # Update the graphic
        self.zoomCodeA=False
        
    
    
        
        
        
    #Change the zoom of the graphic B
    def zoom_changedB(self):
        if self.zoomCodeB:
            print("Zoom de codigo")
        else:
            self.sentinelZoomChangedB+=1
            print("Zoom de usuario")
        # Function called for graphB zoom
        x_range = self.viewBoxB.viewRange()[0]   # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]    # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsB = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histB, _ = np.histogram(self.dataB, bins=binsB)
        self.curveB.setData(binsB, self.histB)  # Update the graphic
        self.zoomCodeB=False
        
    
    #Change the zoom of the graphic C
    def zoom_changedC(self):
        if self.zoomCodeC:
            print("Zoom de codigo")
        else:
            self.sentinelZoomChangedC+=1
            print("Zoom de usuario")
        # Function called for graphC zoom
        x_range = self.viewBoxC.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsC = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histC, _ = np.histogram(self.dataC, bins=binsC)
        self.curveC.setData(binsC, self.histC)  # Update the graphic
        self.zoomCodeC=False
        
        
    #Change the zoom of the graphic D
    def zoom_changedD(self):
        if self.zoomCodeD:
            print("Zoom de codigo")
        else:
            self.sentinelZoomChangedD+=1
            print("Zoom de usuario")
        # Function called for graphD zoom
          
        x_range = self.viewBoxD.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsD = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histD, _ = np.histogram(self.dataD, bins=binsD)
        self.curveD.setData(binsD, self.histD)  # Update the graphic
        self.zoomCodeD=False
    
    
    ##--------------##
    ##--------------##
    ##--Save files--##
    ##--------------##
    ##--------------## 
    def save_graphic(self):
        
        data_prefix=savefile.read_default_data()['Default Histogram Name']
        current_date=datetime.datetime.now()
        current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        #Init filenames and data list
        filenames=[]
        data=[]
        settings=[]
        column_names=[]
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
            total_condition= conditiontxt or conditioncsv or conditiondat
            if not total_condition:
                if self.setinelSaveA:
                    filename1=data_prefix+current_date_str+'channelA'
                    setting_A="Average cycles: "+str(self.channel1.getAverageCycles())+ "\nMode: "+str(self.channel1.getMode())+"\nNumber of stops:"+ str(self.channel1.getNumberOfStops())+"\nStop edge: "+str(self.channel1.getStopEdge())+ "\nStop mask: "+str(self.channel1.getStopMask())
                    settings.append(setting_A)
                    filenames.append(filename1)
                    data.append(self.datapureA)
                    column_names.append('channelA_data (ps)')
                if self.setinelSaveB:
                    filename2=data_prefix+current_date_str+'channelB'
                    setting_B="Average cycles: "+str(self.channel2.getAverageCycles())+ "\nMode: "+str(self.channel2.getMode())+"\nNumber of stops:"+ str(self.channel2.getNumberOfStops())+"\nStop edge: "+str(self.channel2.getStopEdge())+ "\nStop mask: "+str(self.channel2.getStopMask())
                    settings.append(setting_B)
                    filenames.append(filename2)
                    data.append(self.datapureB)
                    column_names.append('channelB_data (ps)')
                if self.setinelSaveC:
                    filename3=data_prefix+current_date_str+'channelC'
                    setting_C="Average cycles: "+str(self.channel3.getAverageCycles())+ "\nMode: "+str(self.channel3.getMode())+"\nNumber of stops:"+ str(self.channel3.getNumberOfStops())+"\nStop edge: "+str(self.channel3.getStopEdge())+ "\nStop mask: "+str(self.channel3.getStopMask())
                    settings.append(setting_C)
                    filenames.append(filename3)
                    data.append(self.datapureC)
                    column_names.append('channelC_data (ps)')
                if self.setinelSaveD:
                    filename4=data_prefix+current_date_str+'channelD'
                    setting_D="Average cycles: "+str(self.channel4.getAverageCycles())+ "\nMode: "+str(self.channel4.getMode())+"\nNumber of stops:"+ str(self.channel4.getNumberOfStops())+"\nStop edge: "+str(self.channel4.getStopEdge())+ "\nStop mask: "+str(self.channel4.getStopMask())
                    settings.append(setting_D)
                    filenames.append(filename4)
                    data.append(self.datapureD)
                    column_names.append('channelD_data (ps)')
                folder_path=savefile.read_default_data()['Folder path']
                
                try:
                    
                    savefile.save_lists_as_columns_txt(data,filenames,column_names,folder_path,settings,selected_format)
                    message_box = QMessageBox(self.parent)
                    message_box.setIcon(QMessageBox.Information)
                    inital_text="The files have been saved successfully in path folder: "
                    text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following names:"
                    index=1
                    for i in filenames:
                        filenumber="File" + str(index)+": "
                        text_route+="\n\n"+filenumber+i+"."+str(selected_format)
                        index+=1
                    message_box.setText(inital_text+text_route)
                    if selected_format=="txt":
                        self.oldroutetxt="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavetxt=1
                    elif selected_format=="csv":
                        self.oldroutecsv="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavecsv=1
                    elif selected_format=="dat":
                        self.oldroutedat="The files have already been saved in path folder: "+ text_route
                        self.sentinelsavedat=1
                    message_box.setWindowTitle("Successful save")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    self.savebutton.setEnabled(True)
                except:
                    #If an error occurs, an error message box will be displayed.
                    message_box = QMessageBox(self.parent)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                
            else:
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Information)
                if conditiontxt:
                    message_box.setText(self.oldroutetxt)
                elif conditioncsv:
                    message_box.setText(self.oldroutecsv)
                elif conditiondat:
                    message_box.setText(self.oldroutedat)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    
    def save_plots(self):
        try:
            graph_names=[]
            #Open select the format
            dialog = QDialog(self.parent)
    
            dialog.setObjectName("ImageFormat")
            dialog.resize(282, 105)
            dialog.setWindowTitle("Save plots")
            
            #pixmap = QIcon("./Sources/abacus_small.ico")
            
            #dialog.setWindowIcon()
            
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
            
            # Mostrar el diálogo y esperar a que se cierre
            if dialog.exec_() == QDialog.Accepted:
                selected_format = FormatBox.currentText()
                if self.setinelSaveA:
                    exporter= pg.exporters.ImageExporter(self.plotA)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Measure_ChannelA'+current_date_str
                    exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveB:
                    exporter= pg.exporters.ImageExporter(self.plotB)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Measure_ChannelB'+current_date_str
                    exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveC:
                    exporter= pg.exporters.ImageExporter(self.plotC)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Measure_ChannelC'+current_date_str
                    exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveD:
                    exporter= pg.exporters.ImageExporter(self.plotD)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name='Measure_ChannelD'+current_date_str
                    exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                    
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Information)
                initial_text="The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+ "with the following names:"
                text_route=""
                index=1
                for i in graph_names:
                    text_route+="\n"+"File"+str(index)+": "+i+"."+selected_format
                    index+=1
                message_box.setText(initial_text+text_route)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                # show successful save
                message_box.exec_()
                
            
        except:
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Question)  # Cambiar a un icono de pregunta
            message_box.setText("Do you want to change the mode?")  # Texto del mensaje
            message_box.setWindowTitle("Change Mode")  # Título de la ventana
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # Botones "Yes" y "No"

            # Ejecutar el cuadro de diálogo y obtener la respuesta
            response = message_box.exec_()

    #Function to connect the Thread with update signal
    def updateSignal(self,value,channel):
        if channel=="A":
            self.dataA.append(value)
            self.update_histogram(self.dataA,self.curveA,"A")
        elif channel=="B":
            self.dataB.append(value)
            self.update_histogram(self.dataB,self.curveB,"B")
        elif channel=="C":
            self.dataC.append(value)
            self.update_histogram(self.dataC,self.curveC,"C")
        elif channel=="D":
            self.dataD.append(value)
            self.update_histogram(self.dataD,self.curveD,"D")
    
    #Update dataPure
    def updateDataPure(self,value,channel):
        if channel=="A":
            self.datapureA.append(value)
        elif channel=="B":
            self.datapureB.append(value)
        elif channel=="C":
            self.datapureC.append(value)
        elif channel=="D":
            self.datapureD.append(value)
    
    #Change the status of sentinel dataThreadCreated
    def threadRunning(self,status):
        if status==0:
            self.threadCreatedSentinel=True
        elif status==1:
            self.threadCreatedSentinel=False
    
    def createDialog(self):
        msg_box = QMessageBox(self.parent)
        msg_box.setText("Connection with the device has been lost")
        msg_box.setWindowTitle("Connection Error")
        pixmap= QPixmap("/Sources/abacus_small.ico")
        msg_box.setIconPixmap(pixmap)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        self.stop_graphic()
        self.hide_graphic2()
        self.disconnectButton.setEnabled(False)
        self.connectButton.setEnabled(True)
        try:
                self.device.close()
        except:
            pass
    
    #Change the color of status Point
    #Function to change the color of point measurement
    def changeStatusColor(self, color):
        pixmap = QPixmap(self.statusPoint.size())
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
        point_size = min(self.statusPoint.width(), self.statusPoint.height()) // 2
        x = (self.statusPoint.width() - point_size) // 2
        y = (self.statusPoint.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusPoint.setPixmap(pixmap)
    
    def changeColorThread(self, color):
        pixmap = QPixmap(self.statusPoint.size())
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
        point_size = min(self.statusPoint.width(), self.statusPoint.height()) // 2
        x = (self.statusPoint.width() - point_size) // 2
        y = (self.statusPoint.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusPoint.setPixmap(pixmap)
        
        
    
    def changeStatusThread(self, newText):
        self.statusValue.setText(newText)
    
    #Open a dialog if the mode is not getting measurements in its range
    def dialogChangeMode(self, channel):
        message_box = QMessageBox(self.parent)
        message_box.setIcon(QMessageBox.Question)  
        message_box.setText("The data collected in the "+channel+" mostly falls outside the reliable range of mode 1 (12ns to 500ns). Would you like to switch to mode 2(125ns to 4ms)?")  
        message_box.setWindowTitle("Change Mode")  
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No) 
        response = message_box.exec_()
        #Change for all modes
        if response == QMessageBox.Yes:
            
            if channel=='channel A':
                self.device.ch1.setMode(2)  
                self.plotA.setLabel('bottom','Start-stop time (ms)')
                temporalDataA=[]
                for i in range(len(self.datapureA)):
                    temporalDataA.append(self.datapureA[i]/(10**9))
                self.dataA=temporalDataA
                self.update_histogram(self.dataA,self.curveA,"A")
                maxValue=max(self.dataA)
                self.zoomCodeA=True
                self.changeZoomMax(maxValue,'A')
                self.worker.changeMaxValue('A',maxValue)

            elif channel=='channel B':
                self.device.ch2.setMode(2)  
                self.plotB.setLabel('bottom','Start-stop time (ms)')
                temporalDataB=[]
                for i in range(len(self.datapureB)):
                    temporalDataB.append(self.datapureB[i]/(10**9))
                self.dataB=[]
                self.dataB=temporalDataB
                self.update_histogram(self.dataB,self.curveB,"B")
                maxValue=max(self.dataB)
                self.zoomCodeB=True
                self.changeZoomMax(maxValue,'B')
                self.worker.changeMaxValue('B',maxValue)
            elif channel=='channel C':
                self.device.ch3.setMode(2)  
                self.plotC.setLabel('bottom','Start-stop time (ms)')
                temporalDataC=[]
                for i in range(len(self.datapureC)):
                    temporalDataC.append(self.datapureC[i]/(10**9))
                self.dataC=temporalDataC
                self.update_histogram(self.dataC,self.curveC,"C")
                maxValue=max(self.dataC)
                self.zoomCodeC=True
                self.changeZoomMax(maxValue,'C')
                self.worker.changeMaxValue('C',maxValue)
            elif channel=='channel D':
                self.device.ch4.setMode(2)  
                self.plotD.setLabel('bottom','Start-stop time (ms)')
                temporalDataD=[]
                for i in range(len(self.datapureD)):
                    temporalDataD.append(self.datapureD[i]/(10**9))
                self.dataD=temporalDataD
                self.update_histogram(self.dataD,self.curveD,"D")
                maxValue=max(self.dataD)
                self.zoomCodeD=True
                self.changeZoomMax(maxValue,'D')
                self.worker.changeMaxValue('D',maxValue)
            self.worker.dialogIsOpen()
        else:
            if channel=='channel A':
                self.worker.addChannelWarning('A')
                self.worker.dialogIsOpen()
            elif channel=='channel B':
                self.worker.addChannelWarning('B')
                self.worker.dialogIsOpen()
            elif channel=='channel C':
                self.worker.addChannelWarning('C')
                self.worker.dialogIsOpen()
            elif channel=='channel D':
                self.worker.addChannelWarning('D')
                self.worker.dialogIsOpen()

        
    
    #Change the maxValue according to max value in the list
    def changeZoomMax(self, newMaxValue,channel):
        
        if channel=='A':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedA>2):
                    self.zoomCodeA=True
                    self.plotA.setXRange(0,newMaxValue)
            else:
                if not (self.sentinelZoomChangedA>0):
                    self.zoomCodeA=True
                    self.plotA.setXRange(0,newMaxValue)
                
        elif channel=='B':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedB>2):
                    self.zoomCodeB=True
                    self.plotB.setXRange(0,newMaxValue)
            else:
                if not (self.sentinelZoomChangedB>0):
                    self.zoomCodeB=True
                    self.plotB.setXRange(0,newMaxValue)
        elif channel=='C':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedC>2):
                    self.zoomCodeC=True
                    self.plotC.setXRange(0,newMaxValue)
            else:
                if not (self.sentinelZoomChangedC>0):
                    self.zoomCodeC=True
                    self.plotC.setXRange(0,newMaxValue)
                
        elif channel=='D':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedD>2):
                    self.zoomCodeD=True
                    self.plotD.setXRange(0,newMaxValue)
            else:
                if not (self.sentinelZoomChangedD>0):
                    self.zoomCodeD=True
                    self.plotD.setXRange(0,newMaxValue)
                
    #auto range beetween 0 and max of Data the graphic with autorange button
    
    #AutoRangeA
    def autoRangeA(self):
        self.zoomCodeA=True
        self.sentinelZoomChangedA=0
        if len(self.dataA)>0:
            maxValue=max(self.dataA)
            self.changeZoomMax(maxValue,'A')
    
    #AutoRangeB
    def autoRangeB(self):
        self.zoomCodeB=True
        self.sentinelZoomChangedB=0
        if len(self.dataB)>0:
            maxValue=max(self.dataB)
            self.changeZoomMax(maxValue,'B')
    
    #AutoRangeC
    def autoRangeC(self):
        self.zoomCodeC=True
        self.sentinelZoomChangedC=0
        if len(self.dataC)>0:
            maxValue=max(self.dataC)
            self.changeZoomMax(maxValue,'C')
    
    #AutoRangeD
    def autoRangeD(self):
        self.zoomCodeD=True
        self.sentinelZoomChangedD=0
        if len(self.dataD)>0:
            maxValue=max(self.dataD)
            self.changeZoomMax(maxValue,'D')
    
    
        
    
class WorkerThreadStartStopHistogram(QThread):
    dataSignal=Signal(float,str)
    dataPureSignal=Signal(float,str)
    threadCreated=Signal(int)
    dialogInit=Signal()
    colorValue=Signal(int)
    stringValue=Signal(str)
    dialogSignal=Signal(str)
    newMaxValueSignal=Signal(float,str)
    
    
    def __init__(self,parent,device,sentinelSaveA,sentinelSaveB,sentinelSaveC,sentinelSaveD):
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
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
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


        
    #Main function
    def run(self):
        self.threadCreated.emit(0)
        while self.itsRunning:
             self.update()
             time.sleep(0.5)
        
    
    
    ##---------------------------------##
    ##---------------------------------##
    ##--------Update function----------##
    ##---------------------------------##
    ##---------------------------------## 
    def update(self):
        #verify the device connection
        #Get the measure of the device
        
        try:
            #Get the update of graph A
            if self.setinelSaveA:
                for numberA in range(self.device.ch1.getNumberOfStops()):
                    new_data1= self.getNewData(self.device.ch1,"A",numberA)

                    if new_data1 is not None:
                        
                        #Check if data is out of range
                        if self.totalA>10:
                            ratioValue=self.outOfRangeA/self.totalA
                            if ratioValue>0.6:
                                if not self.sentinelDialogA:
                                    self.openDialog=True
                                    self.dialogSignal.emit("channel A")
                                    self.sentinelDialogA=True
                                    #Active waiting
                                    while(self.openDialog):
                                        print("Dialog Open, waiting for close...")
                                        time.sleep(1)
                                    if self.device.ch1.getMode()==1:
                                        self.dataSignal.emit(new_data1,"A")
                                    else:
                                        self.outOfRangeA=0
                                else:
                                    self.dataSignal.emit(new_data1,"A")
                            else:
                                self.dataSignal.emit(new_data1,"A")
                                if 'A' in self.channelsToChange:
                                    self.channelsToChange.remove('A')
                        ###############################
                        else:
                        #Emit data
                            self.dataSignal.emit(new_data1,"A")
                    else:
                        if self.noMeasurementA>2 and ('A' not in self.channelsNM):
                            self.channelsNM.append('A')
                        elif 'A' in self.channelsNM and self.noMeasurementA==0:
                            self.channelsNM.remove('A')
                        
                    
            
            #Get the update of graph B
            if self.setinelSaveB:
                for numberB in range(self.device.ch2.getNumberOfStops()):
                    new_data2= self.getNewData(self.device.ch2,"B",numberB)
                    if new_data2 is not None:
                        #Check if data is out of range
                        if self.totalB>10:
                            ratioValue=self.outOfRangeB/self.totalB
                            if ratioValue>0.6:
                                if not self.sentinelDialogB:
                                    self.openDialog=True
                                    self.dialogSignal.emit("channel B")
                                    self.sentinelDialogB=True
                                    #Active waiting
                                    while(self.openDialog):
                                        print("Dialog Open, waiting for close...")
                                        time.sleep(1)
                                    if self.device.ch2.getMode()==1:
                                        self.dataSignal.emit(new_data2,"B")
                                    else:
                                        self.outOfRangeB=0
                                else:
                                    self.dataSignal.emit(new_data2,"B")
                            else:
                                self.dataSignal.emit(new_data2,"B")
                                if 'B' in self.channelsToChange:
                                    self.channelsToChange.remove('B')
                        ###############################
                        #Emit data
                        else:
                            self.dataSignal.emit(new_data2,"B")

                    else:
                        if self.noMeasurementB>2 and ('B' not in self.channelsNM):
                            self.channelsNM.append('B')
                        elif 'B' in self.channelsNM and self.noMeasurementB==0:
                            self.channelsNM.remove('B')
                            
                    



            #Get the update of graph C
            if self.setinelSaveC:
                for numberC in range(self.device.ch3.getNumberOfStops()):
                    new_data3= self.getNewData(self.device.ch3,"C",numberC)
                    if new_data3 is not None:
                        #Check if data is out of range
                        if self.totalC>10:
                            ratioValue=self.outOfRangeC/self.totalC
                            if ratioValue>0.6:
                                if not self.sentinelDialogC:
                                    self.openDialog=True
                                    self.dialogSignal.emit("channel C")
                                    self.sentinelDialogC=True
                                    #Active waiting
                                    while(self.openDialog):
                                        print("Dialog Open, waiting for close...")
                                        time.sleep(1)
                                    if self.device.ch3.getMode()==1:
                                        self.dataSignal.emit(new_data3,"C")
                                    else:
                                        self.outOfRangeC=0
                                else:
                                    self.dataSignal.emit(new_data3,"C")
                            else:
                                self.dataSignal.emit(new_data3,"C")
                                if 'C' in self.channelsToChange:
                                    self.channelsToChange.remove('C')
                        ###############################
                        
                        #Emit data
                        else:
                            self.dataSignal.emit(new_data3,"C")

                    else:
                        if self.noMeasurementC>2 and ('C' not in self.channelsNM):
                            self.channelsNM.append('C')
                        elif 'C' in self.channelsNM and self.noMeasurementC==0:
                            self.channelsNM.remove('C')
                    
                    
            
            
            #Get the update of graph D
            if self.setinelSaveD:
                for numberD in range(self.device.ch4.getNumberOfStops()):
                    new_data4= self.getNewData(self.device.ch4,"D",numberD)
                    if new_data4 is not None:
                        #Check if data is out of range
                        if self.totalD>10:
                            ratioValue=self.outOfRangeD/self.totalD
                            if ratioValue>0.6:
                                if not self.sentinelDialogD:
                                    self.openDialog=True
                                    self.dialogSignal.emit("channel D")
                                    self.sentinelDialogD=True
                                    #Active waiting
                                    while(self.openDialog):
                                        print("Dialog Open, waiting for close...")
                                        time.sleep(1)
                                    if self.device.ch4.getMode()==1:
                                        self.dataSignal.emit(new_data4,"D")
                                    else:
                                        self.outOfRangeD=0
                                else:
                                    self.dataSignal.emit(new_data4,"D")
                            else:
                                self.dataSignal.emit(new_data4,"D")
                                if 'D' in self.channelsToChange:
                                    self.channelsToChange.remove('D')
                                
                        ###############################
                        #Emit data
                        else:
                            self.dataSignal.emit(new_data4,"D")

                    else:
                        if self.noMeasurementD>2 and ('D' not in self.channelsNM):
                            self.channelsNM.append('D')
                        elif 'D' in self.channelsNM and self.noMeasurementD==0:
                            self.channelsNM.remove('D')
                    
            
            if len(self.channelsToChange)>0:
                stringEmit="Consider changing mode of the channels:"
                for i in range(len(self.channelsToChange)):
                    if i==0:
                        stringEmit+=" "+self.channelsToChange[i]
                    else:
                        stringEmit+=", "+self.channelsToChange[i]
                self.currentState= stringEmit
                self.colorValue.emit(3)
                self.stringValue.emit(self.currentState)
            
                
            if len(self.channelsNM)>0:
                stringEmit="NM: "
                for i in range(len(self.channelsNM)):
                    if i==0:
                        stringEmit+=" "+self.channelsNM[i] 
                    else:
                        stringEmit+=", "+self.channelsNM[i] 
                self.currentNM=stringEmit
                emitStringProblems=self.currentState+" "+self.currentNM
                self.colorValue.emit(3)
                self.stringValue.emit(emitStringProblems)

            if len(self.channelsToChange)==0:
                self.currentState=""

            if len(self.channelsNM)==0 and len(self.channelsToChange)==0:
                self.colorValue.emit(1)
                self.stringValue.emit("Measurement running")        
                
                

                    



                        
                        
        except NameError as e:
            print(e)
            self.dialogInit.emit()
            self.stop()
             
    ##---------------------------------##
    ##---------------------------------##
    ##---Begin with get measurement----##
    ##---------------------------------##
    ##---------------------------------##  
    
    def getNewData(self,channel,channelIndex,stopNumber):
        
        measurements=self.device.measure()
        if len(measurements)==0:
            number_runs=self.device.getNumberOfRuns()
            self.totalStarts+=number_runs
        

        if len(measurements)!=0:
            if len(measurements[0])!=0:
                self.totalStarts=0
                
                number_runs=self.device.getNumberOfRuns()
                if channelIndex=="A":
                    self.noMeasurementA+=1
                    index_measurement=0    
                elif channelIndex=="B":
                    self.noMeasurementB+=1
                    index_measurement=number_runs
                elif channelIndex=="C":
                    self.noMeasurementC+=1
                    index_measurement=number_runs*2
                elif channelIndex=="D":
                    self.noMeasurementD+=1
                    index_measurement=number_runs*3
                    
                total_measurement=0
                total_points=0
                for i in range(number_runs):
                    if measurements[i+index_measurement][3+stopNumber]!=-1:
                        total_measurement+=measurements[i+index_measurement][3+stopNumber]
                        total_points+=1
                if total_points!=0:    
                    if channelIndex=='A':
                        self.noMeasurementA=0
                    elif channelIndex=='B':
                        self.noMeasurementB=0
                    elif channelIndex=='C':
                        self.noMeasurementC=0
                    elif channelIndex=='D':
                        self.noMeasurementD=0
                    average_measurement=total_measurement/total_points
                    if channel.getMode()==2:
                        miliseconds_measurement=average_measurement/(10**9)
                    else:
                        if average_measurement>800000:
                            if channelIndex=='A':
                                self.outOfRangeA+=1
                            elif channelIndex=='B':
                                self.outOfRangeB+=1
                            elif channelIndex=='C':
                                self.outOfRangeC+=1
                            elif channelIndex=='D':
                                self.outOfRangeD+=1
                        miliseconds_measurement=average_measurement/(10**3) 
                    
                    #Change the histogram range according to max Value
                    if channelIndex=='A' and miliseconds_measurement>self.currentMaxValueA:
                        self.currentMaxValueA=miliseconds_measurement
                        self.newMaxValueSignal.emit(miliseconds_measurement,'A')
                    elif channelIndex=='B' and miliseconds_measurement>self.currentMaxValueB:
                        self.currentMaxValueB=miliseconds_measurement
                        self.newMaxValueSignal.emit(miliseconds_measurement,'B')
                    elif channelIndex=='C' and miliseconds_measurement>self.currentMaxValueC:
                        self.currentMaxValueC=miliseconds_measurement
                        self.newMaxValueSignal.emit(miliseconds_measurement,'C')
                    elif channelIndex=='D' and miliseconds_measurement>self.currentMaxValueD:
                        self.currentMaxValueC=miliseconds_measurement
                        self.newMaxValueSignal.emit(miliseconds_measurement,'D')
                        
                    if channelIndex=='A':
                        self.totalA+=1    
                    elif channelIndex=='B':
                        self.totalB+=1    
                    elif channelIndex=='C':
                        self.totalC+=1    
                    elif channelIndex=='D':
                        self.totalD+=1    
                    print(average_measurement)
                    self.dataPureSignal.emit(round(average_measurement),channelIndex)
                    return miliseconds_measurement
                else:
                    return None
            else:
                return None
        else:
            return None
    

    #Function to know if a dialog is open
    def dialogIsOpen(self):
        self.openDialog=False 
    
    #Change the max Value if the mode is changed
    def changeMaxValue(self,channel,valueMax):
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
        if channel=='A':
            self.channelsToChange.append('A')
        elif channel=='B':
            self.channelsToChange.append('B')
        elif channel=='C':
            self.channelsToChange.append('C')
        elif channel=='D':
            self.channelsToChange.append('D')



    @Slot()
    def stop(self):
        self.threadCreated.emit(1)
        self.itsRunning=False
    
        
        
        
