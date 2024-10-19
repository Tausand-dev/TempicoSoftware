from PySide2.QtWidgets import QDialog, QDoubleSpinBox, QSpinBox, QPushButton, QMessageBox, QWhatsThis, QLabel
from PySide2.QtGui import QIcon
from PySide2.QtCore import QEvent




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
        self.spinboxNumerOfStops.setMinimum(1)  
        self.spinboxNumerOfStops.setMaximum(1000) 
        self.spinboxNumerOfStops.setSingleStep(1) 
        self.spinboxNumerOfStops.setWrapping(True)
        self.spinboxNumerOfStops.setButtonSymbols(QSpinBox.PlusMinus)  
        self.spinboxNumerOfStops.setAccelerated(True)  
        self.spinboxNumerOfStops.setGeometry(180,40,100,20)
        #------Help button---------#
        
        
        
        #------Save Button---------#
        button = QPushButton("Save changes", self)
        button.setGeometry(110, 80, 140, 40)
        

        self.getsettings()
        button.clicked.connect(self.setsettings)

    
    
    def getsettings(self):
        """
        Retrieves the device's current settings, such as the number of runs and threshold voltage, 
        and updates the corresponding values in the graphical interface.

        The function fetches the number of runs and threshold voltage from the connected device, 
        and then sets these values in the dialog's spinbox and combobox in the user interface.

        :returns: None
        """
        number_runs=self.device.getNumberOfRuns()
        self.spinboxNumerOfStops.setValue(int(number_runs))
        tresholdVoltage= self.device.getThresholdVoltage()
        self.Comboboxthresholdvoltage.setValue(float(tresholdVoltage))
    
    def setsettings(self):
        """
        Applies the settings provided by the user to the connected device.

        The function retrieves the user-defined values for the number of runs and threshold voltage 
        from the graphical interface and sends these values to the device. After applying the settings, 
        the function closes the settings dialog.

        :returns: None
        """
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

    

