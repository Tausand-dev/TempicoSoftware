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




class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        savefile.create_folder()
        self.setWindowTitle("Splash Screen")
        self.setFixedSize(400, 300)
        

        # Crear una etiqueta para mostrar la imagen
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 400, 300)

        # Cargar la imagen
        pixmap = QPixmap("./Sources/splash.png")  # Ajusta la ruta de tu imagen
        self.image_label.setPixmap(pixmap)

        # Mostrar la ventana principal después de 3 segundos
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_main_window)
        self.timer.start(3000)  # Tiempo en milisegundos

    def show_main_window(self):
        # Crear la ventana principal y mostrarla
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args):
        super(MainWindow,self).__init__(parent=parent)
        #------Window parameters---------#
        
        
        self.setWindowTitle("Tempico Software")
        self.setGeometry(100,100,1000,700)
        self.setWindowIcon(QIcon('Sources/abacus_small.ico'))
        self.setMinimumSize(1000,700)
        self.conectedDevice=None
        

        if abacus.CURRENT_OS == 'win32':
            import ctypes
            myappid = 'tempico.tempico.01'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #------Menu bar-------------#
        menu_bar = self.menuBar()
        #file_menu = menu_bar.addMenu("File")
        settings_menu = menu_bar.addMenu("Settings")
        #help_menu = menu_bar.addMenu("Help")
        about_menu = menu_bar.addMenu("About")
        #-----Actions for file--------#
        #save_action=QAction("Save",self)
        #new_action=QAction("New",self)
        #Open_action=QAction("Open",self)
        #file_menu.addAction(save_action)
        #file_menu.addAction(new_action)
        #file_menu.addAction(Open_action)
        #-----Actions for settings--------#
        change_parameters_action=QAction("Channels settings",self)
        settings_menu.addAction(change_parameters_action)
        change_parameters_action.triggered.connect(self.settings_clicked)
        general_settings_action=QAction("General settings",self)
        settings_menu.addAction(general_settings_action)
        general_settings_action.triggered.connect(self.general_settings_clicked)
        about_settings_action=QAction("About Tempico Software",self)
        about_settings_action.triggered.connect(self.about_settings)
        about_menu.addAction(about_settings_action)
        #-----Qtabs for every type of measure--------#
        self.tabs=QTabWidget(self)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,"Start-Stop histogram")
        #self.tabs.addTab(self.tab2,"Lifetime")
        #self.tabs.addTab(self.tab3,"G2 Measurement")
        self.tabs.setGeometry(0,20,1000,700)
        # Crear un QVBoxLayout para agregar el QTabWidget
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        #layout.setContentsMargins(0, 30, 0, 0)
        # Establecer el layout en la ventana principal
        self.sentinel1=0
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.construct_start_stop_histogram(self.tab1)
        self.connectButton = QPushButton("Connect", self)
        self.disconnectButton = QPushButton("Disconnect", self)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.connectButton)
        buttonLayout.addWidget(self.disconnectButton)
        
        # Crear un QWidget para contener los QTabWidget y los botones
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        
        # Crear el layout vertical principal para organizar los widgets
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.addLayout(buttonLayout)  # Agregar layout de botones
        mainLayout.setContentsMargins(10, 10, 10, 10)  # Margen para los widgets
        mainLayout.addWidget(self.tabs) 
        self.connectsentinel=0
        self.connectButton.clicked.connect(self.open_dialog)
        self.disconnectButton.clicked.connect(self.disconnect_button_click)
        
        
        
        
        self.sentinel2=0
        self.sentinel3=0
        self.open_dialog()
        
        






        


    #-----Functions for construc every Qtab--------#
    def construct_start_stop_histogram(self,padre):
        if self.sentinel1==0:
            self.ui = Ui_HistogramaStartStop()
            self.ui.setupUi(padre)
            self.sentinel1=1

        # Ajustar la política de tamaño del área de configuración
        #self.ui.GraphConfigurationArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    def construct_lifetime(self,padre):
        if self.sentinel2==0:
            self.ui = Ui_Form()
            self.ui.setupUi(padre)
            self.sentinel2=1
    
    def construct_g2(self,padre):
        if self.sentinel3==0:
            self.ui = Ui_G2()
            self.ui.setupUi(padre)
            self.sentinel3=1
    def open_dialog(self):
        self.dialog=QDialog(self)
        self.uidialog = Ui_Devices()
        self.uidialog.setupUi(self.dialog)
        self.dialog.exec_()
        self.conectedDevice=  self.uidialog.deviceConnected
        if self.conectedDevice!=None:
            if self.connectsentinel==0:
                self.connectButton.setEnabled(False)
                self.disconnectButton.setEnabled(True)
                self.conectedDevice.open()
                
                checkchannel1=self.ui.Channel1Graph1
                checkchannel2=self.ui.Channel4Graph1
                checkchannel3=self.ui.Channel2Graph1
                checkchannel4=self.ui.Channel3Graph1
                startbutton=self.ui.SaveGraph1
                stopbutton=self.ui.StopGraph1
                savebutton=self.ui.SaveDoc
                #Save Plots
                save_graph_1=self.ui.SaveImage1
                
                #Clear Plots
                clear_channel_A=self.ui.ClearchannelA
                clear_channel_B=self.ui.ClearchannelB
                clear_channel_C=self.ui.ClearchannelC
                clear_channel_D=self.ui.ClearchannelD
                
                channel1=self.conectedDevice.ch1
                
                channel2=self.conectedDevice.ch2
                
                channel3=self.conectedDevice.ch3
                
                channel4=self.conectedDevice.ch4
                
                
                self.conectedDevice.setNumberOfRuns(2)
                self.connectsentinel=1
                self.grafico=Canvas(self.ui.Graph3,self.disconnectButton,self.conectedDevice,checkchannel1,checkchannel2,checkchannel3,checkchannel4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D, self.connectButton)
                self.tabs.currentChanged.connect(self.clicked_tabs)
            else:
                if hasattr(self, 'grafico'):  # Verificar si self.grafico está definido
                    self.conectedDevice.open()
                    self.grafico.show_graphic(self.conectedDevice)
                    
                    self.connectButton.setEnabled(False)
                    self.disconnectButton.setEnabled(True)
                
        else: 
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
       
    def disconnect_button_click(self):
        if hasattr(self, 'grafico'):  # Verificar si self.grafico está definido
            self.grafico.hide_graphic2()
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            self.conectedDevice.close()
            self.conectedDevice=None
            
                    
        

    #-----Functions for settings clicked--------#
    def clicked_tabs(self):
          valor_padre=self.tabs.currentIndex()
          padre=self.tab1
          if valor_padre==0:
              padre=self.tab1
              self.construct_start_stop_histogram(padre)
          elif valor_padre==1:
              padre=self.tab2
              self.construct_lifetime(padre)
          elif valor_padre==2:
              padre=self.tab3
              self.construct_g2(padre)
              
              
          
          

    def settings_clicked(self):
        if self.conectedDevice!=None:
            if not self.grafico.currentmeasurement:
                self.dialog_settings=QDialog(self)
                self.settings_channels = Ui_settings()
                self.settings_channels.setupUi(self.dialog_settings, self.conectedDevice)
                self.dialog_settings.exec_()
            else:
                message_box = QMessageBox()
                message_box.setWindowTitle("Running measurement")
                message_box.setText("It is not possible to make changes when a measurement is running.")
                message_box.setStandardButtons(QMessageBox.Ok)
                pixmap= QPixmap("/Sources/abacus_small.ico")
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Warning)
                message_box.exec_()
    
                
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)  
            message_box.setWindowTitle("No connected device")
            message_box.setText("No connected device was found")
            pixmap= QPixmap("/Sources/abacus_small.ico")
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
    
    def general_settings_clicked(self):
        if self.conectedDevice!=None:
            if not self.grafico.currentmeasurement:
                settings_windows=GeneralSettingsWindow(self.conectedDevice)
                settings_windows.exec_()
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)  # Icono de advertencia
                message_box.setWindowTitle("Error: Running measurement")
                message_box.setText("It is not possible to make changes when a measurement is running.")
                message_box.setStandardButtons(QMessageBox.Ok)

                # Mostrar el QMessageBox y esperar a que el usuario lo cierre
                message_box.exec_()
    
                
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)  # Icono de advertencia
            message_box.setWindowTitle("Error: No Device Connected")
            message_box.setText("No device connected was found")
            message_box.setStandardButtons(QMessageBox.Ok)
    
            # Mostrar el QMessageBox y esperar a que el usuario lo cierre
            message_box.exec_()
            
    

    def about_settings(self):
        
        settings_windows=AboutWindow()
        settings_windows.exec_()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 
            "Are you sure you want to close tempico software?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()  # Acepta el evento de cierre de la ventana
        else:
            event.ignore() 


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
        self.sentinelsave=0

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
    def get_new_data(self, channel,dataPure,channelIndex):
        
        
        
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
                if measurements[i+index_measurement][3]!=-1:
                    total_measurement+=measurements[i][3]
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
                return 4
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
                new_data1= self.get_new_data(self.channel1, self.datapureA,"A")
                if new_data1 is not None:
                    self.dataA.append(new_data1)
                    self.update_histogram(self.dataA,self.curveA,"A")
                    
            
            #Get the update of graph B
            if self.setinelSaveB:
                new_data2= self.get_new_data(self.channel2, self.datapureB,"B")
                if new_data2 is not None:
                    self.dataB.append(new_data2)
                    self.update_histogram(self.dataB,self.curveB,"B")
            
            #Get the update of graph C
            if self.setinelSaveC:
                new_data3= self.get_new_data(self.channel3, self.datapureC,"C")
                if new_data3 is not None:
                    self.dataC.append(new_data3)
                    self.update_histogram(self.dataC,self.curveC,"C")
            
            #Get the update of graph D
            if self.setinelSaveD:
                new_data4= self.get_new_data(self.channel4, self.datapureD,"D")
                if new_data4 is not None:
                    self.dataD.append(new_data4)
                    self.update_histogram(self.dataD,self.curveD,"D")
        except:
            msg_box = QMessageBox()
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
        if self.sentinelsave==0:
            data_prefix=savefile.read_default_data()['Default Histogram Name']
            current_date=datetime.datetime.now()
            current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            #Init filenames and data list
            filenames=[]
            data=[]
            settings=[]
            column_names=[]
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
                
                savefile.save_lists_as_columns_txt(data,filenames,column_names,folder_path,settings)
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Information)
                inital_text="The files have been saved successfully in path folder: "
                text_route="\n\n"+ str(folder_path)+"\n\n"+"with the following names:"
                index=1
                for i in filenames:
                    filenumber="File" + str(index)+": "
                    text_route+="\n\n"+filenumber+i+".txt"
                    index+=1
                message_box.setText(inital_text+text_route)
                self.oldroute="The files have already been saved in path folder: "+ text_route
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            except:
                #If an error occurs, an error message box will be displayed.
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Critical)
                message_box.setText("The changes could not be saved.")
                message_box.setWindowTitle("Error saving")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            self.savebutton.setEnabled(True)
            self.sentinelsave=1
        else:
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Information)
            message_box.setText(self.oldroute)
            message_box.setWindowTitle("Successful save")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
    
    def save_plots(self):
        try:
            graph_names=[]
            #Open select the format
            dialog = QDialog()
    
            dialog.setObjectName("ImageFormat")
            dialog.resize(182, 105)
            dialog.setWindowTitle("Select image format")
            
            pixmap = QIcon("/Sources/abacus_small.ico")
            
            dialog.setWindowIcon(pixmap)
            
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


        
        
        
        
    
    
    
        
        
        
        
        
        
        
    #Start taking data with the start button    
    
        



        # Conectar la señal 'resizeEvent' del parent (QFrame) para ajustar el tamaño del gráfico
        


#--------Execution Test----------#


if __name__ == '__main__':
    app = QApplication([])

    # Cargar la imagen del splash screen
    splash_pix = QPixmap('./Sources/splash.png')

    # Redimensionar la imagen al tamaño deseado
    desired_size = QSize(400, 300)  # Establece el tamaño deseado aquí
    splash_pix = splash_pix.scaled(desired_size, Qt.KeepAspectRatio)

    # Crear el splash screen
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)

    # Ajustar el tamaño del splash screen
    splash.setFixedSize(desired_size)

    # Agregar efecto de fade al splash screen
    opaqueness = 0.0
    step = 0.1
    splash.setWindowOpacity(opaqueness)
    splash.show()

    while opaqueness < 1:
        splash.setWindowOpacity(opaqueness)
        time.sleep(step)  # Aparece gradualmente
        opaqueness += step

    time.sleep(1)  # Mantener la imagen en la pantalla por un tiempo
    splash.close()  # Cerrar el splash screen

    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()

    app.exec_()
