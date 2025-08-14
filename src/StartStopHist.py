from PySide2.QtCore import QTimer, QMetaObject, QThread, Signal, Slot, Qt
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout
from numpy import histogram, linspace
import time
import pyqtgraph as pg
from PySide2.QtCore import QTimer
import time
#To do eliminate import
from createsavefile import createsavefile as savefile
import datetime
import os
import io
import pyTempico as tempico
import sys

#Create graphic design#
class StartStopLogic():
    """
    This class handles the functionality for managing buttons, checkboxes, and graphs for histograms related to the Start-Stop measurements. 
    It controls which channels are active, manages the display of histograms, and records the data from the Tempico device based on the user's interactions. 
    It also handles the zooming feature for creating bars according to the time range received from the device.

    :param parent: The parent QWindow for the logic.
    :param disconnect: The QPushButton used to disconnect.
    :param device: The Tempico device class that handles the measurements.
    :param check1, check2, check3, check4: QCheckBoxes that control the visibility of each histogram.
    :param startbutton, stopbutton: QPushButtons to start and stop the measurement process.
    :param savebutton, save_graph_1: QPushButtons to save data and save the graph.
    :param clear_channel_A, clear_channel_B, clear_channel_C, clear_channel_D: QPushButtons to clear data for each respective channel.
    :param connect: QPushButton to connect to the Tempico device.
    :param mainWindow: The main window (QWindow) for the GUI.
    :param statusValue, statusPoint: QLabel widgets for displaying status information (e.g., values and points).
    """
    def __init__(self, parent, disconnect,device,check1,check2,check3,check4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D,connect,mainWindow,statusValue,statusPoint,timerStatus, *args, **kwargs):
        super().__init__()
        self.savefile=savefile()
        #timer to manage disconnection
        self.timerConnection=timerStatus
        #Disconnect button
        self.disconnectButton= disconnect
        #Connect button
        self.connectButton= connect
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
        self.withoutMeasurement=False

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
        self.histA, self.binsA=histogram(self.dataA,bins=60)
        #Creating the histogram plot channel B
        self.dataB=[]
        self.histB, self.binsB=histogram(self.dataB,bins=60)
        #Creating the histogram plot channel C
        self.dataC=[]
        self.histC, self.binsC=histogram(self.dataC,bins=60)
        #Creating the histogram plot channel D
        self.dataD=[]
        self.histD, self.binsD=histogram(self.dataD,bins=60)
        
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
        self.maxYA=0
        self.maxYB=0
        self.maxYC=0
        self.maxYD=0
        
        


        
    #Function to know the state of device   
    ##---------------------------------##
    ##---------------------------------##
    ##------Begin the create graphs----##
    ##---------------------------------##
    ##---------------------------------##  
           
        
    def create_graphs(self):
        """
        Creates histograms and plots for the selected channels (A, B, C, D) and arranges them on the GUI. 

        This function initializes the graphical components and assigns the appropriate properties to the plots based on the selected channels.
        It also manages the layout of the graphs, resizing them according to the number of selected channels (1, 2, 3, or 4). 
        After setting up the graphical components, the function starts a worker thread that handles the measurement process in parallel with the GUI thread, ensuring the UI remains responsive.

        :return: None
        """
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
            self.plotA.sigRangeChanged.connect(self.zoom_changedA)
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
            #Button autorange
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
        self.worker=WorkerThreadStartStopHistogram(self.parent,self.device,self.setinelSaveA,self.setinelSaveB,self.setinelSaveC,self.setinelSaveD,self.checkA.isChecked(),self.checkB.isChecked(),self.checkC.isChecked(),self.checkD.isChecked())
        self.worker.finished.connect(self.threadComplete)
        self.worker.dataPureSignal.connect(self.updateDataPure)
        self.worker.dataSignal.connect(self.updateSignal)
        self.worker.threadCreated.connect(self.threadRunning)
        self.worker.dialogInit.connect(self.createDialog)
        self.worker.colorValue.connect(self.changeColorThread)
        self.worker.stringValue.connect(self.changeStatusThread)
        self.worker.dialogSignal.connect(self.dialogChangeMode)
        self.worker.newMaxValueSignal.connect(self.changeZoomMax)
        self.worker.dataBashSignal.connect(self.updateBashSignal)
        self.worker.dataPureBashSignal.connect(self.updateBashDataPure)
        self.worker.start()
        
    
    
    ##---------------------------------##
    ##---------------------------------##
    ##--Begin with start-stop buttons--##
    ##---------------------------------##
    ##---------------------------------##  
    
    
    
    
    
    def start_graphic(self):
        """
        Starts the graphical representation of the measurement based on the selected channels.

        If no channels are selected, it prompts the user to select at least one channel before proceeding. 
        It also disables certain buttons to prevent interaction during the measurement process.

        :return: None
        """
        if (not self.checkA.isChecked() and not self.checkB.isChecked() and not self.checkC.isChecked() and not self.checkD.isChecked()):
            message_box = QMessageBox(self.parent)
            message_box.setText("You must select at least one channel before starting a measurement.")
            message_box.setWindowTitle("Select a channel")
            message_box.setStandardButtons(QMessageBox.Ok)
            pixmap= QPixmap("/Sources/tausand_small.ico")
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        else: 
            self.mainWindow.saveSettings()
            self.withoutMeasurement=False
            self.stopTimerConnection()
            self.sentinelZoomChangedA=0
            self.sentinelZoomChangedB=0
            self.sentinelZoomChangedC=0
            self.sentinelZoomChangedD=0
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.tabs.setTabEnabled(2,False)
            self.mainWindow.tabs.setTabEnabled(3,False)
            self.disconnectButton.setEnabled(False)
            self.mainWindow.activeMeasurement()
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
            
    
    
    
    def stopTimerConnection(self):
        """
        Stops the timer responsible for checking the device connection.

        This function is typically called when a measurement begins to avoid interference
        during the acquisition process.

        :return: None
        """
        #Stop timer when a measurement begins
        self.timerConnection.stop()
    
    def startTimerConnection(self):
        """
        Starts the timer that periodically checks the device connection.

        The timer runs every 500 milliseconds to monitor connectivity. This is typically 
        called after a measurement finishes or when the application is idle.

        :return: None
        """
        #Start timer when a measurement begins
        self.timerConnection.start(500)
    
    def hide_graphic2(self):
        """
        Disables the start and stop buttons in the graphical interface.

        This function is typically used to prevent user interaction during certain operations.

        :return: None
        """
        self.startbutton.setEnabled(False)
        self.stopbutton.setEnabled(False)
        
    
    def show_graphic(self, device_new):
        """
        Sets the device and its channels, enabling the start button for measurement.

        :param device_new: The new device to be set (DeviceType).
        :return: None
        """
        self.device=device_new
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        self.startbutton.setEnabled(True)
        
    def stop_graphic(self):
        """
        Enables the functions to initiate a new measurement while disabling the buttons to clear graphs. 
        It also updates the status bar text and color.

        :return: None
        """
        if not self.withoutMeasurement:
            self.startTimerConnection()
        if self.threadCreatedSentinel:
            self.worker.stop()
            time.sleep(1)
        self.beforeMeasurement=True
        self.statusValue.setText("No measurement running")
        self.changeStatusColor(0)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.mainWindow.tabs.setTabEnabled(3,True)
        self.disconnectButton.setEnabled(True)
        self.mainWindow.noMeasurement()
        self.stopbutton.setEnabled(False)
        if not self.withoutMeasurement:
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
        """
        Handles the completion of the measurement thread by enabling the ability to switch between windows. 
        It also calls the stop_graphic() function to update the UI accordingly.

        :return: None
        """
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.mainWindow.tabs.setTabEnabled(3,True)
        self.threadCreated=False
        self.stop_graphic()
    
    
        
    ##---------------------------------##
    ##---------------------------------##
    ##------Clear graphics buttons-----##
    ##---------------------------------##
    ##---------------------------------##  
    
    def clear_a(self):
        """
        Clears the lists containing measured data for channel A by resetting them to empty lists.

        :return: None
        """
        self.dataA=[]
        self.datapureA=[]
        
    def clear_b(self):
        """
        Clears the lists containing measured data for channel B by resetting them to empty lists.

        :return: None
        """
        self.dataB=[]
        self.datapureB=[]
    
    def clear_c(self):
        """
        Clears the lists containing measured data for channel C by resetting them to empty lists.

        :return: None
        """
        self.dataC=[]
        self.datapureC=[]
    
    def clear_d(self):
        """
        Clears the lists containing measured data for channel D by resetting them to empty lists.

        :return: None
        """
        self.dataD=[]
        self.datapureD=[]
    
    
    def update_histogram(self, data, curve, indexChannel):
        """
        Calculates and updates the histogram for the specified channel based on the measured data.

        The function first checks the selected channel (A, B, C, or D) and retrieves the 
        current view range from the corresponding view box. It then creates bins for the 
        histogram based on this range, using a total of 61 bins. 

        Finally, it computes the histogram of the provided data and updates the specified 
        curve in the plot with the histogram values.

        :param data: The measured data used to calculate the histogram (list).
        :param curve: The curve item from the plot in PyQt5 with PyQtGraph that corresponds 
                    to the channel (PlotCurveItem).
        :param indexChannel: The identifier of the channel for the histogram, which can 
                            be "A", "B", "C", or "D" (str).
        :return: None
        """
        
        # Calculate the histogram
        if indexChannel=="A":
            self.zoomCodeA=True
            x_range = self.viewBoxA.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = linspace(x_min, x_max, num=61)
            
            
        elif indexChannel == "B":
            self.zoomCodeB=True
            x_range = self.viewBoxB.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = linspace(x_min, x_max, num=61)
        elif indexChannel == "C":
            self.zoomCodeC=True
            x_range = self.viewBoxC.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = linspace(x_min, x_max, num=61)
        elif indexChannel == "D":
            self.zoomCodeD=True
            x_range = self.viewBoxD.viewRange()[0]
            x_min, x_max = x_range[0], x_range[1]
            binsU = linspace(x_min, x_max, num=61)
        hist, _ = histogram(data, bins=binsU)
        curve.setData(binsU, hist, fillLevel=0)
        
    
    ##-------------------------------------------##
    ##-------------------------------------------##
    ##--Get the histogram bins according to zoom-##
    ##-------------------------------------------##
    ##-------------------------------------------## 
    
    
    def zoom_changedA(self):
        """
        Automatically calculates and updates the histogram for channel A when the user 
        zooms in on the corresponding graph.

        The function checks if the zoom was triggered by code or user action. If it was 
        triggered by the user, it increments the sentinel for zoom changes. It then 
        retrieves the current x-range from the view box for channel A and computes the 
        bin width for the histogram.

        Next, it creates 61 bins based on the x-range and calculates the histogram 
        using the measured data. The histogram data is then used to update the curve 
        item for channel A in the plot.

        :param: None
        :return: None
        """
        if self.zoomCodeA:
            #print("Zoom Code")
            pass
        else:
            self.sentinelZoomChangedA+=1
            #print("Zoom user")
        # Function called for graphA zoom 
        x_range = self.viewBoxA.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsA = linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histA, _ = histogram(self.dataA, bins=binsA)
        self.curveA.setData(binsA, self.histA)  # Update the graphic
        if max(self.histA)!=self.maxYA:
            self.maxYA=max(self.histA)
            self.zoomCodeA=True
        else:    
            self.zoomCodeA=False
        
    
    
        
        
        
    #Change the zoom of the graphic B
    def zoom_changedB(self):
        """
        Automatically calculates and updates the histogram for channel B when the user 
        zooms in on the corresponding graph.

        The function checks if the zoom was triggered by code or user action. If it was 
        triggered by the user, it increments the sentinel for zoom changes. It then 
        retrieves the current x-range from the view box for channel B and computes the 
        bin width for the histogram.

        Next, it creates 61 bins based on the x-range and calculates the histogram 
        using the measured data. The histogram data is then used to update the curve 
        item for channel B in the plot.

        :param: None
        :return: None
        """
        if self.zoomCodeB:
            #print("Zoom code")
            pass
        else:
            self.sentinelZoomChangedB+=1
            #print("Zoom user")
        # Function called for graphB zoom
        x_range = self.viewBoxB.viewRange()[0]   # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]    # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsB = linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histB, _ = histogram(self.dataB, bins=binsB)
        self.curveB.setData(binsB, self.histB)  # Update the graphic
        if max(self.histB)!=self.maxYB:
            self.maxYB=max(self.histB)
            self.zoomCodeB=True
        else:    
            self.zoomCodeB=False
        
        
    
    #Change the zoom of the graphic C
    def zoom_changedC(self):
        """
        Automatically calculates and updates the histogram for channel C when the user 
        zooms in on the corresponding graph.

        The function checks if the zoom was triggered by code or user action. If it was 
        triggered by the user, it increments the sentinel for zoom changes. It then 
        retrieves the current x-range from the view box for channel C and computes the 
        bin width for the histogram.

        Next, it creates 61 bins based on the x-range and calculates the histogram 
        using the measured data. The histogram data is then used to update the curve 
        item for channel C in the plot.

        :param: None
        :return: None
        """
        if self.zoomCodeC:
            #print("Zoom code")
            pass
        else:
            self.sentinelZoomChangedC+=1
            #print("Zoom user")
        # Function called for graphC zoom
        x_range = self.viewBoxC.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsC = linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histC, _ = histogram(self.dataC, bins=binsC)
        self.curveC.setData(binsC, self.histC)  # Update the graphic
        if max(self.histC)!=self.maxYC:
            self.maxYC=max(self.histC)
            self.zoomCodeC=True
        else:    
            self.zoomCodeC=False
        
        
        
    #Change the zoom of the graphic D
    def zoom_changedD(self):
        """
        Automatically calculates and updates the histogram for channel D when the user 
        zooms in on the corresponding graph.

        The function checks if the zoom was triggered by code or user action. If it was 
        triggered by the user, it increments the sentinel for zoom changes. It then 
        retrieves the current x-range from the view box for channel D and computes the 
        bin width for the histogram.

        Next, it creates 61 bins based on the x-range and calculates the histogram 
        using the measured data. The histogram data is then used to update the curve 
        item for channel D in the plot.

        :param: None
        :return: None
        """
        if self.zoomCodeD:
            #print("Zoom code")
            pass
        else:
            self.sentinelZoomChangedD+=1
            #print("Zoom user")
        # Function called for graphD zoom
          
        x_range = self.viewBoxD.viewRange()[0]  # Get current x range in the view
        x_min, x_max = x_range[0], x_range[1]   # Get the max and min current range in the view
        bin_width = (x_max - x_min) / 61  
        binsD = linspace(x_min, x_max, num=61)  # Create 61 points in order to get the boundaries
        self.histD, _ = histogram(self.dataD, bins=binsD)
        self.curveD.setData(binsD, self.histD)  # Update the graphic
        if max(self.histD)!=self.maxYD:
            self.maxYD=max(self.histD)
            self.zoomCodeD=True
        else:    
            self.zoomCodeD=False

    
    
    ##--------------##
    ##--------------##
    ##--Save files--##
    ##--------------##
    ##--------------## 
    def save_graphic(self):
        """
        Saves the current data according to the selected format specified in the dialog box.

        The function starts by retrieving the default histogram name and the current 
        date, which is formatted to create a unique filename. It then initializes lists 
        to hold filenames, data, settings, and column names for the saved files.

        A dialog box is displayed for the user to select the desired file format 
        (txt, csv, or dat) for saving the data. Once the user accepts the selection, 
        the function checks if the selected format has already been saved before.

        If the selected format has not been saved, it collects data from the various 
        channels (A, B, C, D) if their corresponding sentinel variables indicate 
        they should be saved. It retrieves the average cycles, mode, number of stops, 
        stop edge, and stop mask for each channel to include in the settings. The 
        function then attempts to save the collected data in the specified format.

        If the save operation is successful, a message box is displayed, confirming 
        the successful save and showing the folder path and file names. If an error 
        occurs during the save process, an error message box is shown.

        If the selected format has already been saved, a message box is displayed 
        with the previous save information.

        :return: None
        """
        
        dataFolderPrefix=self.savefile.getDataFolderPrefix()
        folder_path=dataFolderPrefix["saveFolder"]
        data_prefix=dataFolderPrefix["startStopHistogramPrefix"]
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
                    setting_A="Average cycles:\t"+str(self.channel1.getAverageCycles())+ "\nMode:\t"+str(self.channel1.getMode())+"\nNumber of stops:\t"+ str(self.channel1.getNumberOfStops())+"\nStop edge:\t"+str(self.channel1.getStopEdge())+ "\nStop mask:\t"+str(self.channel1.getStopMask())
                    settings.append(setting_A)
                    filenames.append(filename1)
                    data.append(self.datapureA)
                    column_names.append('channelA_data (ps)')
                if self.setinelSaveB:
                    filename2=data_prefix+current_date_str+'channelB'
                    setting_B="Average cycles:\t"+str(self.channel2.getAverageCycles())+ "\nMode:\t"+str(self.channel2.getMode())+"\nNumber of stops:\t"+ str(self.channel2.getNumberOfStops())+"\nStop edge:\t"+str(self.channel2.getStopEdge())+ "\nStop mask:\t"+str(self.channel2.getStopMask())
                    settings.append(setting_B)
                    filenames.append(filename2)
                    data.append(self.datapureB)
                    column_names.append('channelB_data (ps)')
                if self.setinelSaveC:
                    filename3=data_prefix+current_date_str+'channelC'
                    setting_C="Average cycles:\t"+str(self.channel3.getAverageCycles())+ "\nMode:\t"+str(self.channel3.getMode())+"\nNumber of stops:\t"+ str(self.channel3.getNumberOfStops())+"\nStop edge:\t"+str(self.channel3.getStopEdge())+ "\nStop mask:\t"+str(self.channel3.getStopMask())
                    settings.append(setting_C)
                    filenames.append(filename3)
                    data.append(self.datapureC)
                    column_names.append('channelC_data (ps)')
                if self.setinelSaveD:
                    filename4=data_prefix+current_date_str+'channelD'
                    setting_D="Average cycles: "+str(self.channel4.getAverageCycles())+ "\nMode:\t"+str(self.channel4.getMode())+"\nNumber of stops:\t"+ str(self.channel4.getNumberOfStops())+"\nStop edge:\t"+str(self.channel4.getStopEdge())+ "\nStop mask:\t"+str(self.channel4.getStopMask())
                    settings.append(setting_D)
                    filenames.append(filename4)
                    data.append(self.datapureD)
                    column_names.append('channelD_data (ps)')
                
                try:
                    
                    self.savefile.save_lists_as_columns_txt(data,filenames,column_names,folder_path,settings,selected_format)
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
        """
        Saves the current plots in the selected image format.

        This method opens a dialog for the user to select an image format (PNG, TIFF, or JPG) 
        and saves the plots for channels A, B, C, and D if their respective flags are set to True. 
        The plots are saved with a timestamp in the specified format in the default folder path.

        :return: None
        """
        try:
            dataFolderPrefix=self.savefile.getDataFolderPrefix()
            folder_path=dataFolderPrefix["saveFolder"]
            data_prefix=dataFolderPrefix["startStopHistogramPrefix"]
            graph_names=[]
            #Open select the format
            dialog = QDialog(self.parent)
    
            dialog.setObjectName("ImageFormat")
            dialog.resize(282, 105)
            dialog.setWindowTitle("Save plots")
            
            #pixmap = QIcon("./Sources/tausand_small.ico")
            
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
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name=data_prefix+'Measure_ChannelA'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveB:
                    exporter= pg.exporters.ImageExporter(self.plotB)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name=data_prefix+'Measure_ChannelB'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveC:
                    exporter= pg.exporters.ImageExporter(self.plotC)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name=data_prefix+'Measure_ChannelC'+current_date_str
                    if os.name == 'posix':  
                        exporter.export(folder_path+'/'+graph_name+'.'+selected_format)
                    else:  
                        exporter.export(folder_path+'\\'+graph_name+'.'+selected_format)
                    graph_names.append(graph_name)
                if self.setinelSaveD:
                    exporter= pg.exporters.ImageExporter(self.plotD)
                    exporter.parameters()['width'] = 800
                    exporter.parameters()['height'] = 600
                    current_date=datetime.datetime.now()
                    current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name=data_prefix+'Measure_ChannelD'+current_date_str
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
            message_box.setText("The graphics could not be saved, check the folder path or system files")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            

    #Function to connect the Thread with update signal
    def updateSignal(self,value,channel):
        """
        Updates the normalized data values for the specified channel and refreshes the corresponding histogram.

        This method appends the new value to the list of normalized data for the specified channel 
        (A, B, C, or D) and calls the update_histogram method to refresh the histogram with the 
        updated data.

        :param value: The normalized value to append to the data list (float or int).
        :param channel: The channel identifier for which the value is to be updated (str). 
                        Accepted values are "A", "B", "C", and "D".
        :return: None
        """
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
    
    def updateBashSignal(self,valueListA,valueListB,valueListC,valueListD):
        for value in valueListA:
            self.dataA.append(value)
        if self.dataA:
            self.update_histogram(self.dataA,self.curveA,"A")
        for value in valueListB:
            self.dataB.append(value)
        if self.dataB:
            self.update_histogram(self.dataB,self.curveB,"B")
        for value in valueListC:
            self.dataC.append(value)
        if self.dataC:
            self.update_histogram(self.dataC,self.curveC,"C")
        for value in valueListD:
            self.dataD.append(value)
        if self.dataD:
            self.update_histogram(self.dataD,self.curveD,"D")
        
    
    #Update dataPure
    def updateDataPure(self,value,channel):
        """
        Updates the raw data values for the specified channel.

        This method appends the new raw value (in picoseconds) to the list of data for the specified 
        channel (A, B, C, or D).

        :param value: The raw data value to append to the data list (float or int). 
                    This value is in picoseconds.
        :param channel: The channel identifier for which the value is to be updated (str). 
                        Accepted values are "A", "B", "C", and "D".
        :return: None
        """
        if channel=="A":
            self.datapureA.append(int(value))
        elif channel=="B":
            self.datapureB.append(int(value))
        elif channel=="C":
            self.datapureC.append(int(value))
        elif channel=="D":
            self.datapureD.append(int(value))

    def updateBashDataPure(self,valuesPureA,valuesPureB,valuesPureC,valuesPureD):
        
        for value in valuesPureA:
            self.datapureA.append(int(value))
        for value in valuesPureB:
            self.datapureB.append(int(value))
        for value in valuesPureC:
            self.datapureC.append(int(value))
        for value in valuesPureD:
            self.datapureD.append(int(value))
            
    #Change the status of sentinel dataThreadCreated
    def threadRunning(self,status):
        """
        Updates the thread creation status.

        This method sets the threadCreatedSentinel attribute to indicate whether a thread has been created 
        based on the provided status value. 

        :param status: The status indicating whether a thread has been created (int). 
                    Use 0 to indicate that the thread has been created, and 1 to indicate that it has not.
        :return: None
        """
        if status==0:
            self.threadCreatedSentinel=True
        elif status==1:
            self.threadCreatedSentinel=False
    
    def createDialog(self):
        """
        Creates a dialog box to notify the user when the connection with the device has been lost.

        This method displays a critical error message box indicating that the connection with the device
        has been lost. It also stops any ongoing graphic updates, hides relevant graphics, 
        and disables the disconnect button while enabling the connect button.

        :return: None
        """
        self.withoutMeasurement=True
        self.disconnectedDevice()
        msg_box = QMessageBox(self.mainWindow)
        msg_box.setText("Connection with the device has been lost")
        msg_box.setWindowTitle("Connection Error")
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
        self.mainWindow.disconnectedDevice()
    
    #Change the color of status Point
    #Function to change the color of point measurement
    def changeStatusColor(self, color):
        """
        Changes the color of the status point in the status bar based on the input value.

        This method updates the status point's color by drawing a filled circle with the specified color.
        The mapping of numerical values to colors is as follows:
        - 0: Gray
        - 1: Green
        - 2: Yellow
        - 3: Orange

        :param color: A numerical value representing the desired color (int).
                    0 for gray, 1 for green, 2 for yellow, 3 for orange.
        :return: None
        """
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
        
    def resetSaveSentinels(self):
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0  
    
    def changeStatusThread(self, newText):
        """
        Updates the text displayed in the status bar.

        This method sets the status value text to the specified new text, 
        reflecting the current status or information relevant to the user.

        :param newText: The text to display in the status bar (str).
        :return: None
        """
        self.statusValue.setText(newText)
    
    #Open a dialog if the mode is not getting measurements in its range
    def dialogChangeMode(self, channel):
        """
        Opens a dialog box to ask the user if they want to change the mode for the selected channel.

        The dialog informs the user that the collected data for the specified channel falls 
        mostly outside the reliable range of mode 1 and prompts them to switch to mode 2. 
        If the user confirms, the function updates the mode and processes the data accordingly.

        :param channel: The channel for which to change the mode (str). 
                        Expected values are 'channel A', 'channel B', 'channel C', or 'channel D'.
        :return: None
        """
        message_box = QMessageBox(self.parent)
        message_box.setIcon(QMessageBox.Question)  
        message_box.setText("The data collected in the "+channel+" mostly falls outside the reliable range of mode 1 (12ns to 500ns). Would you like to switch to mode 2 (125ns to 4ms)?")  
        message_box.setWindowTitle("Change Mode")  
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No) 
        response = message_box.exec_()
        #Change for all modes
        if response == QMessageBox.Yes:
            
            if channel=='channel A':
                self.device.ch1.setMode(2)  
                self.plotA.setLabel('bottom','Start-stop time (ms)')
                temporalDataA=[]
                self.beforeMeasurement=True
                self.sentinelZoomChangedA=0
                for i in range(len(self.datapureA)):
                    temporalDataA.append(self.datapureA[i]/(10**9))
                self.dataA=temporalDataA
                self.update_histogram(self.dataA,self.curveA,"A")
                maxValue=0
                self.zoomCodeA=True
                self.changeZoomMax(maxValue,'A')
                self.worker.changeMaxValue('A',maxValue)

            elif channel=='channel B':
                self.device.ch2.setMode(2)  
                self.plotB.setLabel('bottom','Start-stop time (ms)')
                temporalDataB=[]
                self.beforeMeasurement=True
                self.sentinelZoomChangedB=0
                for i in range(len(self.datapureB)):
                    temporalDataB.append(self.datapureB[i]/(10**9))
                self.dataB=[]
                self.dataB=temporalDataB
                self.update_histogram(self.dataB,self.curveB,"B")
                maxValue=0
                self.zoomCodeB=True
                self.changeZoomMax(maxValue,'B')
                self.worker.changeMaxValue('B',maxValue)
            elif channel=='channel C':
                self.device.ch3.setMode(2)  
                self.plotC.setLabel('bottom','Start-stop time (ms)')
                temporalDataC=[]
                self.beforeMeasurement=True
                self.sentinelZoomChangedC=0
                for i in range(len(self.datapureC)):
                    temporalDataC.append(self.datapureC[i]/(10**9))
                self.dataC=temporalDataC
                self.update_histogram(self.dataC,self.curveC,"C")
                maxValue=0
                self.changeZoomMax(maxValue,'C')
                self.worker.changeMaxValue('C',maxValue)
            elif channel=='channel D':
                self.device.ch4.setMode(2)  
                self.plotD.setLabel('bottom','Start-stop time (ms)')
                temporalDataD=[]
                self.beforeMeasurement=True
                self.sentinelZoomChangedD=0
                for i in range(len(self.datapureD)):
                    temporalDataD.append(self.datapureD[i]/(10**9))
                self.dataD=temporalDataD
                self.update_histogram(self.dataD,self.curveD,"D")
                maxValue=0
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
        """
        Automatically adjusts the zoom level of the plot to the maximum value found.

        The function sets the x-axis range of the specified channel's plot to [0, newMaxValue].
        It considers whether measurements have been taken and limits the zoom change based on 
        the sentinel zoom change counters.

        :param newMaxValue: The new maximum value for the zoom range (float).
        :param channel: The channel to which the zoom change applies (str).
                        Expected values are 'A', 'B', 'C', or 'D'.
        :return: None
        """
        
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
        """
        Automatically adjusts the zoom level of channel A to the maximum value in the data.

        The function sets a sentinel for zoom changes, checks if there are any data points in 
        channel A, and if so, finds the maximum value. It then calls the changeZoomMax function
        to adjust the zoom accordingly.

        :return: None
        """
        self.zoomCodeA=True
        self.sentinelZoomChangedA=0
        if len(self.dataA)>0:
            maxValue=max(self.dataA)
            self.changeZoomMax(maxValue,'A')
    
    #AutoRangeB
    def autoRangeB(self):
        """
        Automatically adjusts the zoom level of channel B to the maximum value in the data.

        The function sets a sentinel for zoom changes, checks if there are any data points in 
        channel B, and if so, finds the maximum value. It then calls the changeZoomMax function
        to adjust the zoom accordingly.

        :return: None
        """
        self.zoomCodeB=True
        self.sentinelZoomChangedB=0
        if len(self.dataB)>0:
            maxValue=max(self.dataB)
            self.changeZoomMax(maxValue,'B')
    
    #AutoRangeC
    def autoRangeC(self):
        """
        Automatically adjusts the zoom level of channel C to the maximum value in the data.

        The function sets a sentinel for zoom changes, checks if there are any data points in 
        channel C, and if so, finds the maximum value. It then calls the changeZoomMax function
        to adjust the zoom accordingly.

        :return: None
        """
        self.zoomCodeC=True
        self.sentinelZoomChangedC=0
        if len(self.dataC)>0:
            maxValue=max(self.dataC)
            self.changeZoomMax(maxValue,'C')
    
    #AutoRangeD
    def autoRangeD(self):
        """
        Automatically adjusts the zoom level of channel D to the maximum value in the data.

        The function sets a sentinel for zoom changes, checks if there are any data points in 
        channel D, and if so, finds the maximum value. It then calls the changeZoomMax function
        to adjust the zoom accordingly.

        :return: None
        """
        self.zoomCodeD=True
        self.sentinelZoomChangedD=0
        if len(self.dataD)>0:
            maxValue=max(self.dataD)
            self.changeZoomMax(maxValue,'D')
    
    
    def disconnectedDevice(self):
        """
        Disables device interaction controls when the device is disconnected.

        This function updates the GUI to reflect that the device is no longer connected 
        by disabling the disconnect and start buttons and enabling the connect button.

        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startbutton.setEnabled(False)
    
    
        
    
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
                QThread.msleep(20)
                self.applyCurrentSettings()
                QThread.msleep(20)
            elif not measurement and self.noMeasurementsSequent >=3:
                self.noAbortsSequent+=1
                self.device.abort()
                QThread.msleep(20)
            valuesToSkip=0
            
            if measurement:
                totalLenMeasurement= len(measurement)
                self.noAbortsSequent=0
                for indexRun in range(totalLenMeasurement):
                    run=measurement[indexRun]
                    
                    if indexRun<(totalLenMeasurement-2) and valuesToSkip<1:
                        nextRun=measurement[indexRun+1]
                        valuesToSkip=self.checkCorruptData(run,nextRun)
                    if valuesToSkip>0:
                        valuesToSkip-=1
                        continue
                    if run:
                        if "Start" in self.channelsNM:
                            self.channelsNM.remove("Start")
                        #Channel A
                        if run[0]==1:
                            totalRangeA=self.getRange(run,self.numberStopsChannelA)
                            for i in range(totalRangeA):
                                if run[3+i]!=-1:
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
                                if run[3+i]!=-1:
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
                                if run[3+i]!=-1:
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
                                if run[3+i]!=-1:
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
        if pureMeasurement<5000000000:
            if self.isBashed:
                listValues.append(measurement)
                pureList.append(pureMeasurement)
                if measurement>self.currentMaxValueA:
                    self.currentMaxValueA=measurement
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
    
        
        
        
