from PySide2.QtCore import *
from PySide2.QtCore import Qt
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
    def __init__(self, parent, disconnect,device,check1,check2,check3,check4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D,connect, *args, **kwargs):
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
            self.viewBoxA.sigRangeChanged.connect(self.zoom_changedA)
            

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
            self.plotB.setXRange(0,5)
            self.clear_channel_B.setEnabled(True)
            widgets.append(self.winB)
            self.curveB=self.plotB.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150),name="ChannelB (Red)")
            self.setinelSaveB=True
            self.viewBoxB=self.plotB.getViewBox()
            self.viewBoxB.sigRangeChanged.connect(self.zoom_changedB)
            

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
            self.plotC.setXRange(0,5)
            self.clear_channel_C.setEnabled(True)
            widgets.append(self.winC)
            self.curveC=self.plotC.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150),name="ChannelC (Green)")
            self.setinelSaveC=True
            self.viewBoxC=self.plotC.getViewBox()
            self.plotC.sigRangeChanged.connect(self.zoom_changedC)
            

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
            self.plotD.setXRange(0,5)
            self.clear_channel_D.setEnabled(True)
            widgets.append(self.winD)
            self.curveD=self.plotD.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150),name="ChannelD (Yellow)")
            self.setinelSaveD=True
            self.viewBoxD=self.plotD.getViewBox()
            self.plotD.sigRangeChanged.connect(self.zoom_changedD)
            

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
        
        
        #Set the time for update function
        self.timer.timeout.connect(self.update)
        #Set the update graphics time
        self.timer.start(500)
    
    
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
            self.disconnectButton.setEnabled(False)
            self.currentmeasurement=True
            self.create_graphs()
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
        self.timer.stop()
    
    ##---------------------------------##
    ##---------------------------------##
    ##---Begin with get measurement----##
    ##---------------------------------##
    ##---------------------------------##  
    def get_new_data(self, channel,dataPure,channelIndex,stopnumber):
        
        
        measurements=self.device.fetch()
        if len(measurements[0])!=0:
            number_runs=self.device.getNumberOfRuns()
            if channelIndex=="A":
                index_measurement=0
                
            elif channelIndex=="B":
                index_measurement=number_runs
                
            elif channelIndex=="C":
                index_measurement=number_runs*2
                
            elif channelIndex=="D":
                index_measurement=number_runs*3
                
            total_measurement=0
            total_points=0
            for i in range(number_runs):
                if measurements[i+index_measurement][3+stopnumber]!=-1:
                    total_measurement+=measurements[i][3+stopnumber]
                    total_points+=1
            if total_points!=0:    
                average_measurement=total_measurement/total_points
                if channel.getMode()==2:
                    miliseconds_measurement=average_measurement/(10**9)
                else:
                    miliseconds_measurement=average_measurement/(10**3)    
                dataPure.append(round(average_measurement))
                return miliseconds_measurement
            else:
                return None
        else:
            return None
        
    
    
    ##---------------------------------##
    ##---------------------------------##
    ##--------Update function----------##
    ##---------------------------------##
    ##---------------------------------## 
    
    
    def update(self):
        #verify the device connection
        
        #Get the measure of the device
        try:
            self.device.measure()
            
            #Get the update of graph A
            if self.setinelSaveA:
                for numberA in range(self.channel1.getNumberOfStops()):
                    new_data1= self.get_new_data(self.channel1, self.datapureA,"A",numberA)
                    if new_data1 is not None:
                        self.dataA.append(new_data1)
                        self.update_histogram(self.dataA,self.curveA,"A")
                    
            
            #Get the update of graph B
            if self.setinelSaveB:
                for numberB in range(self.channel2.getNumberOfStops()):
                    new_data2= self.get_new_data(self.channel2, self.datapureB,"B",numberB)
                    if new_data2 is not None:
                        self.dataB.append(new_data2)
                        self.update_histogram(self.dataB,self.curveB,"B")
            
            #Get the update of graph C
            if self.setinelSaveC:
                for numberC in range(self.channel3.getNumberOfStops()):
                    new_data3= self.get_new_data(self.channel3, self.datapureC,"C",numberC)
                    if new_data3 is not None:
                        self.dataC.append(new_data3)
                        self.update_histogram(self.dataC,self.curveC,"C")
            
            #Get the update of graph D
            if self.setinelSaveD:
                for numberD in range(self.channel4.getNumberOfStops()):
                    new_data4= self.get_new_data(self.channel4, self.datapureD,"D",numberD)
                    if new_data4 is not None:
                        self.dataD.append(new_data4)
                        self.update_histogram(self.dataD,self.curveD,"D")
        except:
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
            x_range = self.viewBoxA.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
            
        elif indexChannel == "B":
            x_range = self.viewBoxB.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
        elif indexChannel == "C":
            x_range = self.viewBoxC.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = np.linspace(x_min, x_max, num=61)
        elif indexChannel == "D":
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
        # Function called for graphA zoom 
        x_range = self.viewBoxA.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsA = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histA, _ = np.histogram(self.dataA, bins=binsA)
        self.curveA.setData(binsA, self.histA)  # Update the graphic
        
        
            
    
    #Change the zoom of the graphic B
    def zoom_changedB(self):
        # Function called for graphB zoom
        x_range = self.viewBoxB.viewRange()[0]   # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]    # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsB = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histB, _ = np.histogram(self.dataB, bins=binsB)
        self.curveB.setData(binsB, self.histB)  # Update the graphic
        
    
    #Change the zoom of the graphic C
    def zoom_changedC(self):
        # Function called for graphC zoom
        x_range = self.viewBoxC.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsC = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histC, _ = np.histogram(self.dataC, bins=binsC)
        self.curveC.setData(binsC, self.histC)  # Update the graphic
        
        
    #Change the zoom of the graphic D
    def zoom_changedD(self):
        # Function called for graphD zoom
          
        x_range = self.viewBoxD.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsD = np.linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histD, _ = np.histogram(self.dataD, bins=binsD)
        self.curveD.setData(binsD, self.histD)  # Update the graphic
    
    
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
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
