from PySide2.QtCore import QTimer, QMetaObject, Qt
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout
from numpy import histogram, linspace
import time
import pyqtgraph as pg
from PySide2.QtCore import QTimer
import time
from Utils.createsavefile import createsavefile as savefile
import datetime
import os
from Threads.ThreadStartStop import WorkerThreadStartStopHistogram
import Utils.constants as constants
import pyTempico as Tempico

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
    def __init__(self, parent, disconnect,device: Tempico.TempicoDevice,check1,check2,check3,check4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D,connect,mainWindow,statusValue,statusPoint,timerStatus, *args, **kwargs):
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
        self.getMinimumValue()
        
        


        
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
                self.channel1Mode=1
            else:
                self.plotA.setLabel('bottom', 'Start-stop time (ms)')
                self.channel1Mode=2
            self.plotA.setMouseEnabled(x=True, y=False)
            self.plotA.disableAutoRange(axis=pg.ViewBox.XAxis)
            if self.channel1Mode==1:
                self.plotA.setXRange(self.minimumNs,5)
            else:
                self.plotA.setXRange(self.minimumMs,5)
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
                self.channel2Mode=1
            else:
                self.plotB.setLabel('bottom', 'Start-stop time (ms)')
                self.channel2Mode=2
            self.plotB.setMouseEnabled(x=True, y=False)
            self.plotB.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeB=True
            if self.channel2Mode==1:
                self.plotB.setXRange(self.minimumNs,5)
            else:
                self.plotB.setXRange(self.minimumMs,5)
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
                self.channel3Mode=1
            else:
                self.plotC.setLabel('bottom', 'Start-stop time (ms)')
                self.channel3Mode=2
            self.plotC.setMouseEnabled(x=True, y=False)
            self.plotC.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeC=True
            if self.channel3Mode==1:
                self.plotC.setXRange(self.minimumNs,5)
            else:
                self.plotC.setXRange(self.minimumMs,5)
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
                self.channel4Mode=1
            else:
                self.plotD.setLabel('bottom', 'Start-stop time (ms)')
                self.channel4Mode=2
            self.plotD.setMouseEnabled(x=True, y=False)
            self.plotD.disableAutoRange(axis=pg.ViewBox.XAxis)
            self.zoomCodeD=True
            if self.channel4Mode==1:
                self.plotD.setXRange(self.minimumNs,5)
            else:
                self.plotD.setXRange(self.minimumMs,5)
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
    
    
    def getMinimumValue(self):
        if "TP12" in constants.VERSION_PARAMETER:
            self.minimumMs=-0.00025
            self.minimumNs=-250
        else:
            self.minimumMs=0
            self.minimumNs=0
    
    
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
            if "TP12" in constants.VERSION_PARAMETER:
                self.calibrateDeviceDelay()
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
            
    
    def calibrateDeviceDelay(self):
        self.device.calibrateDelay()
    
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
                    if self.channel1Mode==1:
                        self.plotA.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotA.setXRange(self.minimumMs,newMaxValue)
            else:
                if not (self.sentinelZoomChangedA>0):
                    self.zoomCodeA=True
                    if self.channel1Mode==1:
                        self.plotA.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotA.setXRange(self.minimumMs,newMaxValue)
                
        elif channel=='B':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedB>2):
                    self.zoomCodeB=True
                    if self.channel2Mode==1:
                        self.plotB.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotB.setXRange(self.minimumMs,newMaxValue)
            else:
                if not (self.sentinelZoomChangedB>0):
                    self.zoomCodeB=True
                    if self.channel2Mode==1:
                        self.plotB.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotB.setXRange(self.minimumMs,newMaxValue)
        elif channel=='C':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedC>2):
                    self.zoomCodeC=True
                    if self.channel3Mode==1:
                        self.plotC.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotC.setXRange(self.minimumMs,newMaxValue)
            else:
                if not (self.sentinelZoomChangedC>0):
                    self.zoomCodeC=True
                    if self.channel3Mode==1:
                        self.plotC.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotC.setXRange(self.minimumMs,newMaxValue)
                
        elif channel=='D':
            if self.beforeMeasurement:
                if not (self.sentinelZoomChangedD>2):
                    self.zoomCodeD=True
                    if self.channel4Mode==1:
                        self.plotD.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotD.setXRange(self.minimumMs,newMaxValue)
            else:
                if not (self.sentinelZoomChangedD>0):
                    self.zoomCodeD=True
                    if self.channel4Mode==1:
                        self.plotD.setXRange(self.minimumNs,newMaxValue)
                    else:
                        self.plotD.setXRange(self.minimumMs,newMaxValue)
                
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
