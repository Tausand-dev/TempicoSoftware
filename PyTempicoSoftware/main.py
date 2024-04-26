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





class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.conectedDevice=None
        
        


        #------Menu bar-------------#
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        settings_menu = menu_bar.addMenu("Settings")
        help_menu = menu_bar.addMenu("Help")
        about_menu = menu_bar.addMenu("About")
        #-----Actions for file--------#
        save_action=QAction("Save",self)
        new_action=QAction("New",self)
        Open_action=QAction("Open",self)
        file_menu.addAction(save_action)
        file_menu.addAction(new_action)
        file_menu.addAction(Open_action)
        #-----Actions for settings--------#
        change_parameters_action=QAction("Channels settings",self)
        settings_menu.addAction(change_parameters_action)
        change_parameters_action.triggered.connect(self.settings_clicked)
        general_settings_action=QAction("General settings",self)
        settings_menu.addAction(general_settings_action)
        general_settings_action.triggered.connect(self.general_settings_clicked)
        about_settings_action=QAction("About Us",self)
        about_settings_action.triggered.connect(self.about_settings)
        about_menu.addAction(about_settings_action)
        #-----Qtabs for every type of measure--------#
        self.tabs=QTabWidget(self)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,"Start-Stop histogram")
        self.tabs.addTab(self.tab2,"Lifetime")
        self.tabs.addTab(self.tab3,"G2 Measurement")
        self.tabs.setGeometry(0,20,1000,700)
        # Crear un QVBoxLayout para agregar el QTabWidget
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        # Establecer el layout en la ventana principal
        self.sentinel1=0
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.construct_start_stop_histogram(self.tab1)
        
        
        
        
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
            self.conectedDevice.open()
            spinrange=self.ui.RangeNumericGraph1
            checkchannel1=self.ui.Channel1Graph1
            checkchannel2=self.ui.Channel4Graph1
            self.conectedDevice.setNumberOfRuns(2)
            self.grafico=Canvas(self.ui.Graph3,0,self.conectedDevice,spinrange,checkchannel1,checkchannel2)
            self.tabs.currentChanged.connect(self.clicked_tabs)


        

    


        
        
        
        

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
        settings_windows=SettingsWindow()
        settings_windows.exec_()
    
    def general_settings_clicked(self):
        settings_windows=GeneralSettingsWindow()
        settings_windows.exec_()

    def about_settings(self):
        print("Se ejecuta")
        settings_windows=AboutWindow()
        settings_windows.exec_()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 
            "Are you sure you want to close tempico software?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        

        if reply == QMessageBox.Yes:
            event.accept()
            if self.conectedDevice!=None:
                self.conectedDevice.close()
        else:
            event.ignore()


#Create graphic design#
class Canvas(FigureCanvas):
    def __init__(self, parent, valor,device,width,check1,check2, *args, **kwargs):
        super(Canvas, self).__init__(plt.Figure(figsize=(10, 4)))
        self.ax = self.figure.subplots()
        self.ax.grid(True)
        self.device = device
        self.range=width
        self.checkA=check1
        self.checkB=check2
        
        self.verticalLayout = QVBoxLayout(parent)
        self.verticalLayout.addWidget(self)

        self.ys1 = []
        self.ys2 = []
        self.ani = FuncAnimation(self.figure, self.update_plot, interval=100)

    def update_plot(self, frame):
        new_data = self.get_new_data()
        new_data2 = self.get_new_data2()
        if new_data is not None:
            
            self.ys1.append(new_data)
            self.ys2.append(new_data2)

            # Limpiar y volver a dibujar el histograma
            self.ax.clear()
            #print(self.width.value())
            if self.checkA.isChecked():
                self.ax.hist(self.ys1, bins=np.linspace(0, self.range.value(), 50), color='blue', edgecolor='black')
            if self.checkB.isChecked():
                self.ax.hist(self.ys2, bins=np.linspace(0, self.range.value(), 50), color='red', edgecolor='black')

            # Configurar etiquetas y títulos si es necesario
            self.ax.set_xlabel('Value (ms)')
            self.ax.set_ylabel('Frecuency')
            self.ax.set_title('Start-Stop Histogram')

            # Forzar la actualización del gráfico en el lienzo
            self.draw()

    def get_new_data(self):
        # Ejemplo de función para obtener nuevos datos (reemplázala con tu propia lógica)
        # Simplemente genera un valor aleatorio para demostración
        self.device.measure()
        
        measurements=self.device.fetch()
        print(measurements)
        if len(measurements[0])!=0:
            measurement1=measurements[0][3]
            measurement2=measurements[1][3]
            average_measurement=(measurement1+measurement2)/2
            miliseconds_measurement=average_measurement/(10**9)
            return miliseconds_measurement
        else:
            return None
    
    def get_new_data2(self):
        # Ejemplo de función para obtener nuevos datos (reemplázala con tu propia lógica)
        # Simplemente genera un valor aleatorio para demostración
        return 3.14



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
