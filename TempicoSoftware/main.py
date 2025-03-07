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
from TempicoSoftware.generalsettings import GeneralSettingsWindow
from TempicoSoftware.aboutWindow import AboutWindow
from TempicoSoftware.StartStopHistograms import StartStopHistogramsWindow as SSHistogramsWindow
from TempicoSoftware.ui_StarStopHistogram import Ui_HistogramaStartStop
from TempicoSoftware.ui_lifetime import Ui_Form
from TempicoSoftware.ui_g2measurement import Ui_G2
from TempicoSoftware.ui_devicesDialog import Ui_Devices
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
import TempicoSoftware.createsavefile as savefile
import datetime
from TempicoSoftware.ui_settings import Ui_settings
from TempicoSoftware.Canvas import Canvas
from TempicoSoftware.constants import *



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
        pixmap = QPixmap(BANNER)  # Ajusta la ruta de tu imagen
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
        self.setWindowIcon(QIcon(ICON_LOCATION))
        self.setMinimumSize(1000,700)
        self.conectedDevice=None
        

        if sys.platform == 'win32':
            import ctypes
            myappid = APPID  # arbitrary string
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
        self.show()
        self.dialog=QDialog(self)
        self.uidialog = Ui_Devices()
        self.uidialog.setupUi(self.dialog)
        self.dialog.exec_()
        self.conectedDevice=  self.uidialog.deviceConnected
        if self.conectedDevice!=None:
            if self.connectsentinel==0:
                self.connectButton.setEnabled(False)
                self.disconnectButton.setEnabled(True)
                try:
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
                    
                    
                    self.connectsentinel=1
                    self.grafico=Canvas(self.ui.Graph3,self.disconnectButton,self.conectedDevice,checkchannel1,checkchannel2,checkchannel3,checkchannel4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D, self.connectButton)
                    self.tabs.currentChanged.connect(self.clicked_tabs)
                except:
                    msg_box = QMessageBox(self)
                    msg_box.setText("Connection with the device failed. Check if another software is using the Tempico device or verify the hardware status.")
                    msg_box.setWindowTitle("Connection Error")
                    pixmap= QPixmap("/Sources/tausand_small.ico")
                    msg_box.setIconPixmap(pixmap)
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
                    
            else:
                if hasattr(self, 'grafico'):  # Verificar si self.grafico está definido
                    try:
                        self.conectedDevice.open()
                        self.grafico.show_graphic(self.conectedDevice)
                        
                        self.connectButton.setEnabled(False)
                        self.disconnectButton.setEnabled(True)
                    except:
                        msg_box = QMessageBox(self)
                        msg_box.setText("Connection with the device failed. Check if another software is using the Tempico device or verify the hardware status.")
                        msg_box.setWindowTitle("Connection Error")
                        pixmap= QPixmap("/Sources/tausand_small.ico")
                        msg_box.setIconPixmap(pixmap)
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setStandardButtons(QMessageBox.Ok)
                        msg_box.exec_()
                
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
                message_box = QMessageBox(self)
                message_box.setWindowTitle("Running measurement")
                message_box.setText("It is not possible to make changes when a measurement is running.")
                pixmap= QPixmap(ICON_LOCATION)
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Information)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    
                
        else:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("No connected device")
            message_box.setText("No connected device was found")
            pixmap= QPixmap(ICON_LOCATION)
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
                message_box = QMessageBox(self)  # Icono de advertencia
                message_box.setWindowTitle("Running measurement")
                message_box.setText("It is not possible to make changes when a measurement is running.")
                pixmap= QPixmap(ICON_LOCATION)
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Information)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
    
                
        else:
            message_box = QMessageBox(self)  # Icono de advertencia
            message_box.setWindowTitle("No Connected Device ")
            message_box.setText("No Connected device connected was found")
            pixmap= QPixmap(ICON_LOCATION)
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
    

    def about_settings(self):
        
        settings_windows=AboutWindow()
        settings_windows.exec_()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 
            "Are you sure you want to close tempico software?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()  
        else:
            event.ignore() 


        


#--------Execution Test----------#

def execProgram():
    app = QApplication([])
    splash_pix = QPixmap(BANNER)
    desired_size = QSize(400, 300)  
    splash_pix = splash_pix.scaled(desired_size, Qt.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setFixedSize(desired_size)
    opaqueness = 0.0
    step = 0.1
    splash.setWindowOpacity(opaqueness)
    splash.show()

    while opaqueness < 1:
        splash.setWindowOpacity(opaqueness)
        time.sleep(step)  
        opaqueness += step

    time.sleep(1)  
    splash.close() 
    window = MainWindow()
    window.show()
    app.exec_()
