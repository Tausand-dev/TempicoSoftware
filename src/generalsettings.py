from PySide2.QtWidgets import QDialog, QDoubleSpinBox, QSpinBox, QPushButton, QMessageBox, QWhatsThis, QLabel, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QIcon
from PySide2.QtCore import QEvent




class GeneralSettingsWindow(QDialog):
    """
    Represents the General Settings window for the Tempico device.

    This class creates a dialog window that allows users to configure general settings that affect all channels (A, B, C, D) and the start settings of the Tempico device. It provides a user interface to adjust various parameters applicable across the entire device.

    :param device: The Tempico device instance that the settings will apply to.
    :type device: object
    """
    def __init__(self, device):
        super().__init__()
        self.device = device

        self.setWindowTitle("General settings")
        self.setFixedSize(350, 140)
        self.setWindowIcon(QIcon('Sources/tausand_small.ico'))

        # Main Layout
        main_layout = QVBoxLayout(self)  # Main vertical layout for the window

        # Threshold Voltage Section
        threshold_layout = QHBoxLayout()  # Horizontal layout for threshold voltage
        self.thresholdvotlage = QLabel("Threshold voltage:", self)
        self.Comboboxthresholdvoltage = QDoubleSpinBox(self)
        self.Comboboxthresholdvoltage.setObjectName("Spinboxtreshold")
        self.Comboboxthresholdvoltage.setMaximum(1.60)
        self.Comboboxthresholdvoltage.setMinimum(0.90)
        self.Comboboxthresholdvoltage.setSingleStep(0.01)
        threshold_layout.addWidget(self.thresholdvotlage)
        threshold_layout.addWidget(self.Comboboxthresholdvoltage)
        main_layout.addLayout(threshold_layout)

        # Number of Runs Section
        runs_layout = QHBoxLayout()  # Horizontal layout for number of runs
        self.numberofruns = QLabel("Number of runs:", self)
        self.spinboxNumerOfStops = QSpinBox(self)
        self.spinboxNumerOfStops.setMinimum(1)
        self.spinboxNumerOfStops.setMaximum(1000)
        self.spinboxNumerOfStops.setSingleStep(1)
        self.spinboxNumerOfStops.setWrapping(True)
        self.spinboxNumerOfStops.setButtonSymbols(QSpinBox.PlusMinus)
        self.spinboxNumerOfStops.setAccelerated(True)
        runs_layout.addWidget(self.numberofruns)
        runs_layout.addWidget(self.spinboxNumerOfStops)
        main_layout.addLayout(runs_layout)

        # Save Button
        button_layout = QVBoxLayout()  # Vertical layout for the save button
        button = QPushButton("Save changes", self)
        button_layout.addWidget(button)
        main_layout.addLayout(button_layout)

        # Connect the button
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
        """
        Handles the event when the "?" (What's This) help button is clicked.

        This function intercepts the event triggered when the user clicks the "?" button (entering What's This mode). 
        It exits What's This mode immediately, changes the mouse cursor back to the arrow, and displays a help window with relevant information.

        :param event: The event object representing the triggered event.
        :type event: QEvent
        :returns: True if the event is handled; otherwise, it passes the event to the parent class for default processing.
        :rtype: bool
        """
        if event.type() == QEvent.EnterWhatsThisMode: #Event called when ? is clicked                
            QWhatsThis.leaveWhatsThisMode() #To change mouse cursor back to arrow
            self.showHelp()
            return True
        return QDialog.event(self, event)
    

    def showHelp(self):
        """
        Displays a help dialog with information about general settings.

        This function is triggered when the "?" (What's This) help button is clicked. It creates and displays a message box containing detailed information about the general settings, including instructions for the threshold voltage and the number of runs.

        The message box provides the following details:
        - **Threshold voltage**: Specifies the acceptable range for input values (0.60 V to 1.60 V).
        - **Number of runs**: Describes the number of measurements performed in each channel during one data collection.

        :returns: None
        """
        QMessageBox.information(self, "Help", "Here is the information about the general settings:\n\n"
                                      "Threshold voltage: Enter a value between 0.60 V and 1.60 V.\n"
                                      "Number of runs: Number of measurements performed in each channel during one data collection.")

    

