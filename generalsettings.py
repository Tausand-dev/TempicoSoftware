from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget, QLabel,QComboBox, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import datetime as dt
import numpy as np
import pyTempico as tempico
import pyAbacus as abacus



class GeneralSettingsWindow(QDialog):
    def __init__(self,device):
        self.device=device
        
        super().__init__()
        self.setWindowTitle("General settings")
        self.setFixedSize(350,140)
        self.setWindowIcon(QIcon('Sources/abacus_small.ico'))
        #self.setWindowFlags(self.windowFlags() | Qt.WindowContextHelpButtonHint)
        #------Change treshold Voltage---------#
        self.thresholdvotlage=QLabel("Threshold voltage:",self)
        self.thresholdvotlage.setGeometry(65,10,150,20)
        self.Comboboxthresholdvoltage = QDoubleSpinBox(self)
        self.Comboboxthresholdvoltage.setObjectName(u"Spinboxtreshold")
        self.Comboboxthresholdvoltage.setMaximum(1.60)
        self.Comboboxthresholdvoltage.setMinimum(0.90)
        self.Comboboxthresholdvoltage.setSingleStep(0.01)
        self.Comboboxthresholdvoltage.setGeometry(180,10,100,20)
        #------Change number of runs---------#
        self.numberofruns=QLabel("Number of runs:",self)
        self.numberofruns.setGeometry(65,40,150,20)
        self.spinboxNumerOfStops = QSpinBox(self)
        self.spinboxNumerOfStops.setMinimum(1)  # Valor mínimo permitido
        self.spinboxNumerOfStops.setMaximum(1000)  # Valor máximo permitido
        self.spinboxNumerOfStops.setSingleStep(1)  # Incremento/decremento en 1
        self.spinboxNumerOfStops.setWrapping(True)  # Volver al valor mínimo después del valor máximo
        self.spinboxNumerOfStops.setButtonSymbols(QSpinBox.PlusMinus)  # Mostrar botones de más/menos
        self.spinboxNumerOfStops.setAccelerated(True)  # Acelerar la velocidad del aumento/decremento
        self.spinboxNumerOfStops.setGeometry(180,40,100,20)
        #------Help button---------#
        
        
        
        #------Save Button---------#
        button = QPushButton("Save changes", self)
        button.setGeometry(110, 80, 140, 40)
        

        # If we use css to the buttons 
        # TO DO: If we dont use css delete this code
        # button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #f0f0f0;
        #         border-style: solid;
        #         border-width: 2px;
        #         border-color: #b0b0b0;
        #         border-radius: 5px;
        #         font-size: 16px;
        #         font-weight: bold;
        #         color: #333;
        #     }
        #     QPushButton:hover {
        #         background-color: #e0e0e0;
        #     }
        #     QPushButton:pressed {
        #         background-color: #d0d0d0;
        #         border-color: #909090;
        #     }
        # """)
        self.getsettings()
        button.clicked.connect(self.setsettings)

        #Definimos que cosas se hacen
        #Cambiar el treshold voltage
        #Cambiar el number of runs
        #Resetear
    
    
    def getsettings(self):
        number_runs=self.device.getNumberOfRuns()
        self.spinboxNumerOfStops.setValue(int(number_runs))
        tresholdVoltage= self.device.getThresholdVoltage()
        self.Comboboxthresholdvoltage.setValue(float(tresholdVoltage))
    
    def setsettings(self):
        self.device.setNumberOfRuns(self.spinboxNumerOfStops.value())
        self.device.setThresholdVoltage(self.Comboboxthresholdvoltage.value())
        self.accept()
    
    def event(self, event): 
        if event.type() == QEvent.EnterWhatsThisMode: #Event called when ? is clicked                
            QWhatsThis.leaveWhatsThisMode() #To change mouse cursor back to arrow
            self.showHelp()
            return True
        return QDialog.event(self, event)
    

    def showHelp(self):
        QMessageBox.information(self, "Help", "Here is the information about the general settings:\n\n"
                                      "Threshold voltage: Enter a value between 0.60 V and 1.60 V.\n"
                                      "Number of runs: Number of measurements performed in each channel during one data collection.")

    

