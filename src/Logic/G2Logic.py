from PySide2.QtCore import QTimer, Qt, QMetaObject, QEvent
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox, QTabWidget, QCheckBox, QWidget, QSizePolicy,QApplication, QWhatsThis, QGridLayout
import pyqtgraph as pg
from numpy import mean, exp, array, sum
from Utils.createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
from Threads.ThreadG2 import WorkerThreadG2
import pyTempico as tempico
from numpy import mean
from datetime import datetime
import pyTempico as tempico
import os
import numpy as np
class G2Logic():
    """
    Manages the logic for the g² (second-order correlation) tab in the GUI.

    This class is responsible for handling the interaction between the user 
    interface and the underlying measurement logic for g² experiments. It 
    connects UI elements, manages measurement control (manual, limited, and 
    auto-clear modes), handles saving data/plots, and provides integration 
    with fitting equations and parameter configuration.

    Key responsibilities:
    - Control of manual, limited, and auto-clear measurements.
    - Management of fitting parameters and application of selected models.
    - Handling of measurement reset, saving, and plot export.
    - Connection of GUI elements (buttons, combo boxes, spin boxes, etc.) 
      to their respective actions.
    - Preparation and update of the graphical frame for g² visualization.

    :param stopChannelComboBox: Combo box to select the stop channel (QComboBox).
    :param coincidenceWindowComboBox: Combo box to select the coincidence window (QComboBox).
    :param numberMeasurementsSpinBox: Spin box to define the number of measurements (QSpinBox).
    :param numberBinsLabel: Label to display the number of histogram bins (QLabel).
    :param startManualButton: Button to start a manual measurement (QPushButton).
    :param stopManualButton: Button to stop a manual measurement (QPushButton).
    :param clearButton: Button to clear the current measurement (QPushButton).
    :param saveDataButton: Button to save g² measurement data (QPushButton).
    :param savePlotButton: Button to save the g² plot (QPushButton).
    :param comboBoxEquation: Combo box to select the fitting equation (QComboBox).
    :param applyFitButton: Button to apply the selected fit to the data (QPushButton).
    :param parametersTable: Table to show and edit fitting parameters (QTableWidget).
    :param initialParametersButton: Button to restore or configure initial fit parameters (QPushButton).
    :param statusValueLabel: Label to display the current measurement status (QLabel).
    :param statusColorLabel: Label to show the status with a color indicator (QLabel).
    :param totalStartsLabel: Label to display the total number of start events (QLabel).
    :param totalStopsLabel: Label to display the total number of stop events (QLabel).
    :param calculatedParameter: Label to show the calculated parameter value (QLabel).
    :param helpButton: Button to open the help dialog (QPushButton).
    :param graphicFrame: Frame where the g² plot is displayed (QFrame).
    :param startLimitedButtonG2: Button to start a limited measurement (QPushButton).
    :param stopLimitedButtonG2: Button to stop a limited measurement (QPushButton).
    :param clearLimitedButtonG2: Button to clear a limited measurement (QPushButton).
    :param autoClearSpinBox: Spin box to configure auto-clear interval (QSpinBox).
    :param startAutoClearButton: Button to start auto-clear measurements (QPushButton).
    :param stopAutoClearButton: Button to stop auto-clear measurements (QPushButton).
    :param clearAutoClearButton: Button to clear auto-clear measurement results (QPushButton).
    :param maximumTimeComboBox: Combo box to select the maximum integration time (QComboBox).
    :param tabSettings: Tab widget containing g² settings (QTabWidget).
    :param fixedDelayCheckBox: Checkbox to enable/disable fixed delay (QCheckBox).
    :param externalDelaySpinBox: Spin box to set the external delay value (QDoubleSpinBox).
    :param device: The Tempico device used for data acquisition (tempico.TempicoDevice).
    :param mainWindow: Reference to the main application window.
    :param connectedTimer: Timer used to monitor device connection (QTimer).
    """
    def __init__(self,stopChannelComboBox: QComboBox, coincidenceWindowComboBox: QComboBox, numberMeasurementsSpinBox: QSpinBox, numberBinsLabel: QLabel,startManualButton: QPushButton, stopManualButton: QPushButton,
                 clearButton: QPushButton,saveDataButton: QPushButton, savePlotButton: QPushButton, comboBoxEquation: QComboBox, applyFitButton: QPushButton, 
                 parametersTable: QTableWidget, initialParametersButton: QPushButton, statusValueLabel: QLabel, statusColorLabel: QLabel, totalStartsLabel: QLabel, totalStopsLabel: QLabel, calculatedParameter: QLabel, helpButton: QPushButton,
                 graphicFrame:QFrame, startLimitedButtonG2: QPushButton, stopLimitedButtonG2: QPushButton, clearLimitedButtonG2: QPushButton, autoClearSpinBox: QSpinBox, startAutoClearButton: QPushButton,
                 stopAutoClearButton: QPushButton, clearAutoClearButton: QPushButton,maximumTimeComboBox: QComboBox, tabSettings: QTabWidget,fixedDelayCheckBox: QCheckBox,externalDelaySpinBox: QDoubleSpinBox,device: tempico.TempicoDevice, mainWindow, connectedTimer: QTimer):
        self.savefile=savefile()
        self.stopChannelComboBox= stopChannelComboBox
        self.coincidenceWindowComboBox = coincidenceWindowComboBox
        self.numberMeasurementsSpinBox= numberMeasurementsSpinBox
        self.numberBinsLabel = numberBinsLabel
        self.startManualButton = startManualButton
        self.stopManualButton = stopManualButton
        self.clearButton = clearButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.comboBoxEquation = comboBoxEquation
        self.applyFitButton = applyFitButton
        self.parametersTable = parametersTable
        self.initialParametersButton = initialParametersButton
        self.statusValueLabel = statusValueLabel
        self.statusColorLabel = statusColorLabel
        self.totalStartsLabel = totalStartsLabel
        self.totalStopsLabel = totalStopsLabel
        self.calculatedParameter = calculatedParameter
        self.helpButton = helpButton
        self.device = device
        self.mainWindow= mainWindow
        self.connectedTimer=connectedTimer
        self.graphicFrame=graphicFrame
        self.startLimitedButtonG2=startLimitedButtonG2
        self.stopLimitedButtonG2=stopLimitedButtonG2
        self.clearLimitedButtonG2=clearLimitedButtonG2
        self.autoClearSpinBox=autoClearSpinBox
        self.startAutoClearButton=startAutoClearButton
        self.stopAutoClearButton=stopAutoClearButton
        self.clearAutoClearButton=clearAutoClearButton
        self.maximumTimeComboBox=maximumTimeComboBox
        self.tabSettings=tabSettings
        self.fixedDelayCheckBox=fixedDelayCheckBox
        self.externalDelaySpinBox=externalDelaySpinBox
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        self.currentMeasurement=False
        self.regionDisable=None
        #Connect elements
        self.comboBoxEquation.currentIndexChanged.connect(self.changeTableParameters)
        self.startManualButton.clicked.connect(self.startManualMeasurement)
        self.stopManualButton.clicked.connect(self.stopManualMeasurement)
        self.clearButton.clicked.connect(self.clearManualMeasurement)
        self.startLimitedButtonG2.clicked.connect(self.startLimitedMeasurement)
        self.stopLimitedButtonG2.clicked.connect(self.stopLimitedMeasurement)
        self.clearLimitedButtonG2.clicked.connect(self.clearManualMeasurement)
        self.startAutoClearButton.clicked.connect(self.startAutoClearMeasurement)
        self.stopAutoClearButton.clicked.connect(self.stopAutoClearMeasurement)
        self.clearAutoClearButton.clicked.connect(self.clearManualMeasurement)
        self.applyFitButton.clicked.connect(self.applyFitAction)
        self.initialParametersButton.clicked.connect(self.showParameterDialog)
        self.saveDataButton.clicked.connect(self.saveG2Data)
        self.fixedDelayCheckBox.clicked.connect(self.changeExternalFixed)
        self.externalDelaySpinBox.valueChanged.connect(self.changeReverseExternalSpinBox)
        self.savePlotButton.clicked.connect(self.saveG2Plot)
        self.helpButton.clicked.connect(self.helpButtonDialog)
        #Tau values
        self.tauValues=[]
        #Fit lists values
        self.g2FitGaussian=[]
        self.g2FitGaussianShift=[]
        self.g2FitLorentzian=[]
        self.g2FitLorentzianShift=[]
        self.g2FitAntibunching=[]
        self.g2FitAntibunchingShift=[]
        self.stopChannelSave=""
        self.parametersChange=False
        #self.externalDelaySpinBox.valueChanged.connect(self.changeExternalDelay)
        self.initialConfigs()
        self.createGraphic()
    
    
    def initialConfigs(self):
        """
        Initializes the default configuration for the application interface and 
        fitting parameters. 

        This method disables buttons related to starting, stopping, clearing, 
        and saving measurements when the device is not connected. It also sets 
        default suffixes, initializes fitting parameter equations, updates tables, 
        and prepares the interface for user interaction.

        :return: None
        """
        if self.device==None:
            self.startManualButton.setEnabled(False)
            self.startLimitedButtonG2.setEnabled(False)
            self.startAutoClearButton.setEnabled(False)
        self.parametersFitName()
        self.externalDelaySpinBox.setSuffix(" ns")
        self.stopManualButton.setEnabled(False)
        self.stopLimitedButtonG2.setEnabled(False)
        self.stopAutoClearButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.clearLimitedButtonG2.setEnabled(False)    
        self.clearAutoClearButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.applyFitButton.setEnabled(False)
        self.initialParametersButton.setEnabled(False)
        self.initParametersEquationThermalGaussian()
        self.initParametersEquationThermalGaussianShift()
        self.initParametersEquationThermalLorentzian()
        self.initParametersEquationThermalLorentzianShift()
        self.initParametersEquationAntiBunching()
        self.initParametersEquationAntiBunchingShift()
        self.changeTermalGaussianTableParameters()
        self.isManualChange=True        
        self.initialParameters()
    
    def parametersFitName(self):
        """
        Initializes the parameter names used in curve fitting.

        :return: None
        """
        self.nameTc="T_c"
        self.nameR2="R^2"
        self.nameTd="T_d"
        self.nameB="b"
        self.nameT0="T_0"
        self.nameTau="Tau"
    
    def connectedDevice(self, device):
        """
        Handles actions after a device is connected.

        :param device: The connected device object.
        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.device=device
        self.startManualButton.setEnabled(True)
        self.startLimitedButtonG2.setEnabled(True)
        self.startAutoClearButton.setEnabled(True)
    
    def disconnectedDevice(self):
        """
        Handles actions after the device is disconnected.

        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startManualButton.setEnabled(False)
        self.startLimitedButtonG2.setEnabled(False)
        self.startAutoClearButton.setEnabled(False)
    
    def resetSaveSentinels(self):
        """
        Resets the sentinel values for saving files.

        :return: None
        """
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
    
    def createGraphic(self):
        """
        Creates the main g2(tau) plot using PyQtGraph.

        This function sets up a GraphicsLayoutWidget inside the graphic frame,
        configures grid, axes labels, and a legend, and adds two curves:
        one for the experimental g2 data and another for the fitted curve. 
        The plot is embedded into a QHBoxLayout for display in the UI.

        :return: None
        """

        self.graphicLayout = QHBoxLayout(self.graphicFrame)
        self.winG2 = pg.GraphicsLayoutWidget()
        self.winG2.setBackground('w')
        self.plotG2 = self.winG2.addPlot()
        self.plotG2.showGrid(x=True, y=True)
        self.plotG2.setLabel('left', f'g2({self.nameTau})')
        self.plotG2.setLabel('bottom', self.nameTau)
        self.legend = pg.LegendItem(offset=(0, 0))
        self.legend.setParentItem(self.plotG2.getViewBox())
        self.legend.anchor((1, 0), (1, 0))
        self.graphicLayout.addWidget(self.winG2)
        self.curveG2 = self.plotG2.plot(pen='b', name='g2 Data')
        self.curveFit = self.plotG2.plot(pen='r', name='g2 fit')
        self.legend.addItem(self.curveG2, 'g2 Data')
        self.legend.addItem(self.curveFit, 'g2 fit')
    
    
    
    
    
    def setVerticalLabel(self):
        """
        Updates the Y-axis label of the g2(tau) plot based on the selected stop channel.

        The label reflects which channel (A, B, C, or D) is currently used as 
        the stop channel in the correlation measurement.

        :return: None
        """
        if self.stopChannelComboBox.currentIndex()==0:
            self.plotG2.setLabel('left',f'g2({self.nameTau}) Start-A')
        elif self.stopChannelComboBox.currentIndex()==1:
            self.plotG2.setLabel('left',f'g2({self.nameTau}) Start-B')
        elif self.stopChannelComboBox.currentIndex()==2:
            self.plotG2.setLabel('left',f'g2({self.nameTau}) Start-C')
        elif self.stopChannelComboBox.currentIndex()==3:
            self.plotG2.setLabel('left',f'g2({self.nameTau}) Start-D')
    
    
    def startTimerConnection(self):
        """
        Starts the connection timer with a 500 ms interval.

        :return: None
        """
        self.connectedTimer.start(500)

    
    def stopTimerConnection(self):
        """
        Stops the connection timer.

        :return: None
        """
        self.connectedTimer.stop()
    
    def initialParameters(self):
        """
        Initializes all default fitting parameters by calling the corresponding 
        setup methods for Gaussian, Lorentzian, and Anti-Bunching models.

        :return: None
        """
        self.initialExternalDelayCheckbox()
        self.initialParametersGaussian()
        self.initialParametesGaussianShifted()
        self.initalParametersLorentzian()
        self.initialParametersLorentzianShifted()
        self.initalParametersAntiBunching()
        self.initalParametersAntiBunchingShifted()
    
    def initialExternalDelayCheckbox(self):
        """
        Resets the external delay checkboxes for Gaussian, Lorentzian, 
        and Anti-Bunching models to False.

        :return: None
        """
        self.externalDelayGaussianCheckBox=False
        self.externalDelayLorentzianCheckBox=False
        self.externalDelayAntiBunchingCheckBox=False
        
    def initialParametersGaussian(self):
        """
        Initializes the default parameter for the Gaussian thermal model.

        :return: None
        """
        self.thermalGaussianTcInitial=1
        
    
    def initialParametesGaussianShifted(self):
        """
        Initializes the default parameters for the shifted Gaussian thermal model.

        :return: None
        """
        self.thermalGaussianShiftTcInitial=1
        self.thermalGaussianShiftTdInitial=0
        self.thermalGaussianShiftBInitial=0
    
    def initalParametersLorentzian(self):
        """
        Initializes the default parameter for the Lorentzian thermal model.

        :return: None
        """
        self.thermalLorentzianT0Initial=1
    
    def initialParametersLorentzianShifted(self):
        """
        Initializes the default parameters for the shifted Lorentzian thermal model.

        :return: None
        """
        self.thermalLorentzianShiftT0Initial=1
        self.thermalLorentzianShiftTdInitial=0
        self.thermalLorentzianShiftBInitial=0
    
    def initalParametersAntiBunching(self):
        """
        Initializes the default parameter for the Anti-Bunching model.

        :return: None
        """
        self.antiBunchingTauAInitial=1
        
    
    def initalParametersAntiBunchingShifted(self):
        """
        Initializes the default parameters for the shifted Anti-Bunching model.

        :return: None
        """
        self.antiBunchingShiftTauAInitial=1
        self.antiBunchingShiftTaudInitial=0
        self.antiBunchingShiftBInitial=0
    
    def initialParametersWithUnits(self):
        """
        Initializes the default parameters for all models depending on the 
        measurement units.  

        If parameters have not been changed manually, the function sets values 
        close to 1 when the units are nanoseconds ("ns"). For other units, the 
        parameters are initialized with values around 1000. This initialization 
        applies to Gaussian, shifted Gaussian, Lorentzian, shifted Lorentzian, 
        Anti-Bunching, and shifted Anti-Bunching models.  

        :return: None
        """
        if not self.parametersChange:
            if self.unitsMeasured=="ns":
                self.thermalGaussianTcInitial=1
                self.thermalGaussianShiftTcInitial=1
                self.thermalGaussianShiftTdInitial=0
                self.thermalGaussianShiftBInitial=0
                self.thermalLorentzianT0Initial=1
                self.thermalLorentzianShiftT0Initial=1
                self.thermalLorentzianShiftTdInitial=0
                self.thermalLorentzianShiftBInitial=0
                self.antiBunchingTauAInitial=1
                self.antiBunchingShiftTauAInitial=1
                self.antiBunchingShiftTaudInitial=0
                self.antiBunchingShiftBInitial=0
            else:
                self.thermalGaussianTcInitial=1000
                self.thermalGaussianShiftTcInitial=1000
                self.thermalGaussianShiftTdInitial=0
                self.thermalGaussianShiftBInitial=0
                self.thermalLorentzianT0Initial=1000
                self.thermalLorentzianShiftT0Initial=1000
                self.thermalLorentzianShiftTdInitial=0
                self.thermalLorentzianShiftBInitial=0
                self.antiBunchingTauAInitial=1000
                self.antiBunchingShiftTauAInitial=1000
                self.antiBunchingShiftTaudInitial=0
                self.antiBunchingShiftBInitial=0
    
    def updateLocalDialogInitalParameters(self):
        """
        Updates the local copies of initial parameters based on the last selected 
        fitting model and the values entered in the dialog spin boxes.  

        Depending on the selected model (Gaussian, shifted Gaussian, Lorentzian, 
        shifted Lorentzian, Anti-Bunching, or shifted Anti-Bunching), the function 
        reads the corresponding spin box values, applies unit conversion if needed 
        (from microseconds to nanoseconds), and assigns them to the appropriate 
        local variables. It also stores the fixed-state option from the checkbox 
        when available.  

        :return: None
        """
        if self.lastSelection=="Thermal gaussian":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialGaussianTc=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialGaussianTc=self.currentSpinBox[0].value()
        if self.lastSelection=="Thermal gaussian shifted":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialGaussianTc=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialGaussianTc=self.currentSpinBox[0].value()
            if self.currentSpinBox[1].suffix()==" us":
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()*1000
            else:
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()
            self.localInitialGaussianShiftedB=self.currentSpinBox[2].value()    
            self.localFixedGaussian=self.currentFixedChebox.isChecked()
        if self.lastSelection=="Thermal lorentzian":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialLorentzianT0=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialLorentzianT0=self.currentSpinBox[0].value()
        if self.lastSelection=="Thermal lorentzian shifted":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialLorentzianT0=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialLorentzianT0=self.currentSpinBox[0].value()
            if self.currentSpinBox[1].suffix()==" us":
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()*1000
            else:
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()
            self.localInitialGaussianShiftedB=self.currentSpinBox[2].value()
            self.localFixedGaussian=self.currentFixedChebox.isChecked()
        if self.lastSelection=="Antibunching":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialGaussianTc=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialGaussianTc=self.currentSpinBox[0].value()
        if self.lastSelection=="Antibunching shifted":
            if self.currentSpinBox[0].suffix()==" us":
                self.localInitialGaussianTc=self.currentSpinBox[0].value()*1000
            else:
                self.localInitialGaussianTc=self.currentSpinBox[0].value()
            if self.currentSpinBox[1].suffix()==" us":
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()*1000
            else:
                self.localInitialGaussianShiftedTd=self.currentSpinBox[1].value()
            self.localInitialGaussianShiftedB=self.currentSpinBox[2].value()
            self.localFixedGaussian=self.currentFixedChebox.isChecked()
        
    def updateParameterFields(self, comboBox, fieldLayout, fieldWidgets, dialog):
        """
        Updates the dialog fields for the initial parameters.

        This function rebuilds the parameter input fields in the dialog based on the
        current selection of the combo box. It updates the corresponding local variables
        with the current values, clears the previous layout, and dynamically adds the
        spin boxes and checkboxes required for the selected equation. The created widgets
        are connected to functions so that values are correctly saved when modified.

        :param comboBox: Combo box containing the equation selection (QComboBox).
        :param fieldLayout: Layout where the parameter fields will be placed (QLayout).
        :param fieldWidgets: List that stores the generated field widgets (list).
        :param dialog: Dialog window containing the parameter fields (QDialog).
        :return: None
        """
        if self.currentSpinBox:
            self.updateLocalDialogInitalParameters()


        for i in reversed(range(fieldLayout.count())):
            item = fieldLayout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)
                fieldLayout.removeItem(item.layout())

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(5)
        fieldLayout.addLayout(grid)

        selection = comboBox.currentText()
        fields, values = [], []

        if selection == "Thermal gaussian":
            fields = [self.nameTc]
            values = [self.localInitialGaussianTc]
            self.lastSelection = "Thermal gaussian"
        elif selection == "Thermal gaussian shifted":
            fields = [self.nameTc, self.nameTd, self.nameB]
            values = [self.localInitialGaussianTc,
                    self.localInitialGaussianShiftedTd,
                    self.localInitialGaussianShiftedB]
            self.lastSelection = "Thermal gaussian shifted"
        elif selection == "Thermal lorentzian":
            fields = [self.nameT0]
            values = [self.localInitialLorentzianT0]
            self.lastSelection = "Thermal lorentzian"
        elif selection == "Thermal lorentzian shifted":
            fields = [self.nameT0, self.nameTd, self.nameB]
            values = [self.localInitialLorentzianT0,
                    self.localInitialGaussianShiftedTd,
                    self.localInitialGaussianShiftedB]
            self.lastSelection = "Thermal lorentzian shifted"
        elif selection == "Antibunching":
            fields = [self.nameTc]
            values = [self.localInitialGaussianTc]
            self.lastSelection = "Antibunching"
        elif selection == "Antibunching shifted":
            fields = [self.nameTc, self.nameTd, self.nameB]
            values = [self.localInitialGaussianTc,
                    self.localInitialGaussianShiftedTd,
                    self.localInitialGaussianShiftedB]
            self.lastSelection = "Antibunching shifted"

        fieldWidgets.clear()
        self.currentValues = values
        self.currentSpinBox = []

        row = 0
        for k, f in enumerate(fields):
            currentValue = values[k]

            if self.nameTd in f:
                label_checkbox = QLabel("Fixed delay:")
                checkbox = QCheckBox()
                checkbox.setStyleSheet("QCheckBox { margin:0; padding:0; }")
                if selection.endswith("shifted"):
                    checkbox.setChecked(self.localFixedGaussian)
                self.currentFixedChebox = checkbox

                grid.addWidget(label_checkbox, row, 0)
                grid.addWidget(checkbox,       row, 1, Qt.AlignLeft)
                row += 1

            label = QLabel(f"{f}:")
            spin = QDoubleSpinBox()
            if self.nameB not in f:
                spin.setSuffix(" ns")
                spin.setDecimals(3)
                spin.setSingleStep(1)
                spin.setMaximum(1e18)
                spin.setMinimum(-1e18)
                spin.valueChanged.connect(lambda v, s=spin: self.updateSpinBoxSufix(s, v))
            else:
                spin.setMaximum(1e18)
                spin.setMinimum(0)
                spin.setDecimals(3)
                spin.setSingleStep(1)

            spin.setValue(currentValue)
            self.currentSpinBox.append(spin)

            if self.nameTd in f:
                fieldWidgets.append((f, spin, checkbox))
            else:
                fieldWidgets.append((f, spin))

            grid.addWidget(label, row, 0)
            grid.addWidget(spin,  row, 1)
            row += 1

        dialog.layout().activate()
        dialog.adjustSize()
    
    def changeExternalCheckBox(self):
        """
        Updates the state of the main UI checkbox.

        This function synchronizes the checkbox in the main interface with the stored
        variable value. Depending on the current index of the equation combo box, the
        main checkbox is updated to reflect the corresponding saved state.

        :return: None
        """
        if self.comboBoxEquation.currentIndex()==1:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
        elif self.comboBoxEquation.currentIndex()==3:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
        elif self.comboBoxEquation.currentIndex()==5:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
    
    def changeExternalFixed(self):
        """
        Updates the stored variable according to the main UI checkbox state.

        This function sets the value of the corresponding variable based on whether
        the main checkbox is selected or not. The assignment depends on the current
        index of the equation combo box.

        :return: None
        """
        if self.comboBoxEquation.currentIndex()==1:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
        elif self.comboBoxEquation.currentIndex()==3:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
        elif self.comboBoxEquation.currentIndex()==5:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
    
    
    def changeExternalSpinBox(self):
        """
        Updates the main UI spin box with the correct units.

        This function modifies the value, suffix, step size, and decimals of the main
        spin box (`externalDelaySpinBox`) depending on the selected equation in the
        combo box. The units are set to nanoseconds (ns) if the value is below 1000,
        or microseconds (us) otherwise. The corresponding stored initial delay value
        is used for the assignment.

        :return: None
        """
        if self.comboBoxEquation.currentIndex()==1:
            self.isManualChange=False
            if abs(self.thermalGaussianShiftTdInitial)<1000:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial)
                self.externalDelaySpinBox.setSuffix(" ns")
                self.externalDelaySpinBox.setSingleStep(1)
                self.externalDelaySpinBox.setDecimals(3)
            else:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial/1000)
                self.externalDelaySpinBox.setSuffix(" us")
                self.externalDelaySpinBox.setSingleStep(0.1)
                self.externalDelaySpinBox.setDecimals(6)
        elif self.comboBoxEquation.currentIndex()==3:
            self.isManualChange=False
            if abs(self.thermalGaussianShiftTdInitial)<1000:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial)
                self.externalDelaySpinBox.setSuffix(" ns")
                self.externalDelaySpinBox.setSingleStep(1)
                self.externalDelaySpinBox.setDecimals(3)
            else:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial/1000)
                self.externalDelaySpinBox.setSuffix(" us")
                self.externalDelaySpinBox.setSingleStep(0.1)
                self.externalDelaySpinBox.setDecimals(6)
        elif self.comboBoxEquation.currentIndex()==5:
            self.isManualChange=False
            if abs(self.thermalGaussianShiftTdInitial)<1000:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial)
                self.externalDelaySpinBox.setSuffix(" ns")
                self.externalDelaySpinBox.setSingleStep(1)
                self.externalDelaySpinBox.setDecimals(3)
            else:
                self.externalDelaySpinBox.setValue(self.thermalGaussianShiftTdInitial/1000)
                self.externalDelaySpinBox.setSuffix(" us")
                self.externalDelaySpinBox.setSingleStep(0.1)
                self.externalDelaySpinBox.setDecimals(6)
        self.isManualChange=True
                
                
    
    def changeReverseExternalSpinBox(self):
        """
        Updates the internal delay variable based on the value set in the main spin box.

        This function reads the current value and suffix ("ns" or "us") from
        `externalDelaySpinBox` and updates the corresponding internal variable
        (`thermalGaussianShiftTdInitial`). If the spin box value exceeds the
        unit threshold (>=1000 ns or <1 us), it automatically adjusts the units
        and rescales the displayed value. The update is applied according to the
        currently selected equation in the combo box.

        :return: None
        """
        if self.isManualChange:
            if abs(self.externalDelaySpinBox.value())>=1000 and self.externalDelaySpinBox.suffix()==" ns":
                self.externalDelaySpinBox.blockSignals(True)
                self.externalDelaySpinBox.setSuffix(" us")
                newValue=self.externalDelaySpinBox.value()/1000
                self.externalDelaySpinBox.setValue(newValue)
                self.externalDelaySpinBox.setDecimals(6)
                self.externalDelaySpinBox.setSingleStep(0.1)
                self.externalDelaySpinBox.blockSignals(False)
            if abs(self.externalDelaySpinBox.value())<1 and self.externalDelaySpinBox.suffix()==" us":
                self.externalDelaySpinBox.blockSignals(True)
                self.externalDelaySpinBox.setSuffix(" ns")
                newValue=self.externalDelaySpinBox.value()*1000
                self.externalDelaySpinBox.setValue(newValue)
                self.externalDelaySpinBox.setSingleStep(1)
                self.externalDelaySpinBox.setDecimals(3)
                self.externalDelaySpinBox.blockSignals(False)
            if self.comboBoxEquation.currentIndex()==1:
                if self.externalDelaySpinBox.suffix()==" ns":
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()
                else:
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()*1000
            elif self.comboBoxEquation.currentIndex()==3:
                print("Entra aca")
                if self.externalDelaySpinBox.suffix()==" ns":
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()
                else:
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()*1000
            elif self.comboBoxEquation.currentIndex()==5:
                if self.externalDelaySpinBox.suffix()==" ns":
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()
                else:
                    self.thermalGaussianShiftTdInitial=self.externalDelaySpinBox.value()*1000
        self.isManualChange=True
    
    def initLocalDialogParameters(self):
        """
        Initializes the local dialog parameters based on the current stored values.

        This function copies the internal state variables that hold the initial
        parameters for Gaussian, Lorentzian, and Antibunching models (including
        their shifted versions) into the corresponding local variables used by
        the parameter dialog. It also initializes the local checkbox states
        for external delay options.

        :return: None
        """
        #Gaussian
        self.localInitialGaussianTc=self.thermalGaussianTcInitial
        #Gaussian shifted
        self.localInitialGaussianShiftedTc=self.thermalGaussianShiftTcInitial
        self.localInitialGaussianShiftedTd=self.thermalGaussianShiftTdInitial
        self.localInitialGaussianShiftedB=self.thermalGaussianShiftBInitial
        #Lorentzian
        self.localInitialLorentzianT0=self.thermalLorentzianT0Initial
        #Lorentizian shifted
        self.localInitialLorentzianShiftedT0=self.thermalLorentzianShiftT0Initial
        self.localInitialLorentzianShiftedTd=self.thermalLorentzianShiftTdInitial
        self.localInitialLorentzianShiftedB=self.thermalLorentzianShiftBInitial
        #Antibunching
        self.localInitialAntiBunchingTA=self.antiBunchingTauAInitial
        #Antibunching shifted
        self.localInitialAntiBunchingShiftedTA=self.antiBunchingShiftTauAInitial
        self.localInitialAntiBunchingShiftedTd=self.antiBunchingShiftTaudInitial
        self.localInitialAntiBunchingShiftedB=self.antiBunchingShiftBInitial
        #Checbox values
        self.localFixedGaussian=self.externalDelayGaussianCheckBox
        self.localFixedLorentzian=self.externalDelayLorentzianCheckBox
        self.localFixedAntibunching=self.externalDelayAntiBunchingCheckBox
    
    def helpEventFilter(dialog, obj, event):
        """
        Global event filter for the help '?' button.

        :param dialog: QDialog being filtered.
        :param obj: QObject that received the event.
        :param event: QEvent instance.
        :return: True if handled, False otherwise.
        """
        if event.type() == QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            QMessageBox.information(dialog, "Help",
                "Aquí va la información de ayuda para este diálogo.")
            return True
        return False

        
    def showParameterDialog(self):
        """
        Shows the dialog window for configuring initial parameters.

        This function creates and displays a dialog that allows the user to
        configure initial parameters for Gaussian, Lorentzian, and Antibunching
        models (including shifted versions). The dialog contains a combo box
        for selecting the model, dynamic parameter fields, and control buttons
        (Apply, Default settings, Cancel). It also integrates a help button
        that opens the parameter help window.

        :return: A tuple (bool, list). The boolean indicates whether the dialog
                was accepted (True) or canceled (False). The list contains
                the field widgets created for the selected parameters.
        """
        self.lastSelection = ""
        self.initLocalDialogParameters()
        self.currentSpinBox = []
        self.currentValues = []
        self.currentFixedChebox = None
        
        self.dialogParameters = QDialog(self.mainWindow)
        self.dialogParameters.setWindowTitle("Initial Parameters")
        
        # AGREGAR EL BOTÓN DE AYUDA (misma línea que tu ejemplo)
        self.dialogParameters.setWindowFlags(self.dialogParameters.windowFlags() | Qt.WindowContextHelpButtonHint)
        
        outerLayout = QVBoxLayout(self.dialogParameters)
        outerLayout.setContentsMargins(6, 6, 6, 6)
        outerLayout.setSpacing(6)

        self.comboBoxDialog = QComboBox()
        self.comboBoxDialog.addItems([
            "Thermal gaussian", "Thermal gaussian shifted", "Thermal lorentzian",
            "Thermal lorentzian shifted", "Antibunching", "Antibunching shifted"
        ])
        outerLayout.addWidget(self.comboBoxDialog)

        fieldLayout = QVBoxLayout()
        fieldLayout.setContentsMargins(0, 0, 0, 0)
        fieldLayout.setSpacing(6)
        outerLayout.addLayout(fieldLayout)

        fieldWidgets = []

        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(8)
        applyBtn = QPushButton("Apply")
        defaultBtn = QPushButton("Default settings")
        cancelBtn = QPushButton("Cancel")
        btnLayout.addWidget(applyBtn)
        btnLayout.addWidget(defaultBtn)
        btnLayout.addWidget(cancelBtn)
        outerLayout.addLayout(btnLayout)
        
        self.updateParameterFields(self.comboBoxDialog, fieldLayout, fieldWidgets, self.dialogParameters)
        self.comboBoxDialog.currentTextChanged.connect(
            lambda: self.updateParameterFields(self.comboBoxDialog, fieldLayout, fieldWidgets, self.dialogParameters)
        )
        applyBtn.clicked.connect(self.updateInitialParameters)
        cancelBtn.clicked.connect(self.cancelParameters)
        defaultBtn.clicked.connect(self.setDefaultParameters)
        
        # OVERRIDE del método event (exactamente igual que tu ejemplo)
        original_event = self.dialogParameters.event
        def custom_event(event):
            if event.type() == QEvent.EnterWhatsThisMode:
                QWhatsThis.leaveWhatsThisMode()
                self.showParameterHelp()
                return True
            return original_event(event)
        
        self.dialogParameters.event = custom_event
        
        self.dialogParameters.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.dialogParameters.adjustSize()
        
        result = self.dialogParameters.exec_()
        return result == QDialog.Accepted, fieldWidgets
    
    def cancelParameters(self):
        """
        Cancels the parameter dialog.

        This function checks the parameter values and closes the dialog
        without applying changes.

        :return: None
        """
        self.checkParametersValue()
        self.dialogParameters.reject()

    def showParameterHelp(self):
        """
        Shows a fixed message.

        :return: None
        """
        help_message = (
            "For shifted fits, the delay parameter T_d can be either fixed or free.\n\n"
            "When T_d is fixed, it remains constant during the fit and only the other "
            "parameters are optimized.\n"
            "When T_d is not fixed, all parameters, including T_d, are determined by the fit."
        )

        QMessageBox.information(
            self.dialogParameters,
            "Parameter Help",
            help_message
        )

    def setDefaultParameters(self):
        """
        Sets the default parameters for the selected model.

        This function initializes the parameters depending on the measurement units 
        (ns or ps) and updates the spin boxes in the dialog with the corresponding 
        default values.

        :return: None
        """
        currentIndexDialog=self.comboBoxDialog.currentIndex()
        if self.unitsMeasured=="ns":
            self.localInitialGaussianTc=1
            self.localInitialGaussianShiftedTc=1
            self.localInitialGaussianShiftedTd=0
            self.localInitialGaussianShiftedB=0
            self.localInitialLorentzianT0=1
            self.localInitialLorentzianShiftedT0=1
            self.localInitialLorentzianShiftedTd=0
            self.localInitialLorentzianShiftedB=0
            self.localInitialAntiBunchingTA=1
            self.localInitialAntiBunchingShiftedTA=1
            self.localInitialAntiBunchingShiftedTd=0
            self.localInitialAntiBunchingShiftedB=0
        else:
            self.localInitialGaussianTc=1000
            self.localInitialGaussianShiftedTc=1000
            self.localInitialGaussianShiftedTd=0
            self.localInitialGaussianShiftedB=0
            self.localInitialLorentzianT0=1000
            self.localInitialLorentzianShiftedT0=1000
            self.localInitialLorentzianShiftedTd=0
            self.localInitialLorentzianShiftedB=0
            self.localInitialAntiBunchingTA=1000
            self.localInitialAntiBunchingShiftedTA=1000
            self.localInitialAntiBunchingShiftedTd=0
            self.localInitialAntiBunchingShiftedB=0
        if currentIndexDialog==0:
            self.currentSpinBox[0].setValue(self.localInitialGaussianTc)
            self.currentSpinBox[0].setValue(self.localInitialGaussianTc)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
        elif currentIndexDialog==1:
            self.currentSpinBox[0].setValue(self.localInitialGaussianShiftedTc)
            self.currentSpinBox[0].setValue(self.localInitialGaussianShiftedTc)
            self.currentSpinBox[1].setValue(self.localInitialGaussianShiftedTd)
            self.currentSpinBox[1].setValue(self.localInitialGaussianShiftedTd)
            self.currentSpinBox[2].setValue(self.localInitialGaussianShiftedB)
            self.currentSpinBox[2].setValue(self.localInitialGaussianShiftedB)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
            self.currentSpinBox[1].setSuffix(" ns")
            self.currentSpinBox[1].setDecimals(3)
        elif currentIndexDialog==2:
            self.currentSpinBox[0].setValue(self.localInitialLorentzianT0)
            self.currentSpinBox[0].setValue(self.localInitialLorentzianT0)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
        elif currentIndexDialog==3:
            self.currentSpinBox[0].setValue(self.localInitialLorentzianShiftedT0)
            self.currentSpinBox[0].setValue(self.localInitialLorentzianShiftedT0)
            self.currentSpinBox[1].setValue(self.localInitialLorentzianShiftedTd)
            self.currentSpinBox[1].setValue(self.localInitialLorentzianShiftedTd)
            self.currentSpinBox[2].setValue(self.localInitialLorentzianShiftedB)
            self.currentSpinBox[2].setValue(self.localInitialLorentzianShiftedB)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
            self.currentSpinBox[1].setSuffix(" ns")
            self.currentSpinBox[1].setDecimals(3)
        elif currentIndexDialog==4:
            self.currentSpinBox[0].setValue(self.localInitialAntiBunchingTA)
            self.currentSpinBox[0].setValue(self.localInitialAntiBunchingTA)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
        elif currentIndexDialog==5:
            self.currentSpinBox[0].setValue(self.localInitialAntiBunchingShiftedTA)
            self.currentSpinBox[0].setValue(self.localInitialAntiBunchingShiftedTA)
            self.currentSpinBox[1].setValue(self.localInitialAntiBunchingShiftedTd)
            self.currentSpinBox[1].setValue(self.localInitialAntiBunchingShiftedTd)
            self.currentSpinBox[2].setValue(self.localInitialAntiBunchingShiftedB)
            self.currentSpinBox[2].setValue(self.localInitialAntiBunchingShiftedB)
            self.currentSpinBox[0].setSuffix(" ns")
            self.currentSpinBox[0].setDecimals(3)
            self.currentSpinBox[1].setSuffix(" ns")
            self.currentSpinBox[1].setDecimals(3)
        

    def updateInitialParameters(self):
        """
        Applies and saves the changes made in the Initial Parameters dialog.

        This function updates the global initial parameters with the values 
        set in the dialog's local variables for each type of equation: Gaussian, 
        Gaussian shifted, Lorentzian, Lorentzian shifted, Antibunching, 
        and Antibunching shifted. It also updates the state of the external 
        delay checkboxes in the main UI to reflect whether the delay is fixed 
        or not, and updates the spin box that stores the T_d value according 
        to the current units. Finally, it calls checkParametersValue() to 
        verify if the current values differ from the defaults and closes the 
        dialog with accept().

        :return: None
        """
        self.updateLocalDialogInitalParameters()
        #Gaussian
        self.thermalGaussianTcInitial=self.localInitialGaussianTc
        #Gaussian shifted
        self.thermalGaussianShiftTcInitial=self.localInitialGaussianShiftedTc
        self.thermalGaussianShiftTdInitial=self.localInitialGaussianShiftedTd
        self.thermalGaussianShiftBInitial=self.localInitialGaussianShiftedB
        #Lorentzian
        self.thermalLorentzianT0Initial=self.localInitialLorentzianT0
        #Lorentizian shifted
        self.thermalLorentzianShiftT0Initial=self.localInitialLorentzianShiftedT0
        self.thermalLorentzianShiftTdInitial=self.localInitialLorentzianShiftedTd
        self.thermalLorentzianShiftBInitial=self.localInitialLorentzianShiftedB
        #Antibunching
        self.antiBunchingTauAInitial=self.localInitialAntiBunchingTA
        #Antibunching shifted
        self.antiBunchingShiftTauAInitial=self.localInitialAntiBunchingShiftedTA
        self.antiBunchingShiftTaudInitial=self.localInitialAntiBunchingShiftedTd
        self.antiBunchingShiftBInitial=self.localInitialAntiBunchingShiftedB
        #Fixed delays
        self.externalDelayGaussianCheckBox=self.localFixedGaussian
        self.externalDelayLorentzianCheckBox=self.localFixedLorentzian
        self.externalDelayAntiBunchingCheckBox=self.localFixedAntibunching
        self.changeExternalCheckBox()
        self.changeExternalSpinBox()
        self.checkParametersValue()
        self.dialogParameters.accept()
    
    def updateSpinBoxSufix(self, spinbox, value):
        """
        Updates the QDoubleSpinBox value and suffix according to its magnitude. 
        Converts between ns and us automatically and adjusts decimals and step. 

        :param spinbox: The QDoubleSpinBox being updated (QDoubleSpinBox)
        :param value: The new value of the spinbox (float)
        :return: None
        """
        currentSuffix = spinbox.suffix()

        # ns → us
        if currentSuffix == " ns" and abs(value) >= 1000:
            spinbox.blockSignals(True)
            spinbox.setDecimals(6)
            spinbox.setValue(value / 1000.0)
            spinbox.setSuffix(" us")
            spinbox.setSingleStep(0.1)
            spinbox.blockSignals(False)

        elif currentSuffix == " us" and abs(value) < 1:
            spinbox.blockSignals(True)
            spinbox.setDecimals(3)
            spinbox.setValue(value * 1000.0)  # sin 999
            spinbox.setSuffix(" ns")
            spinbox.setSingleStep(1)
            spinbox.blockSignals(False)
        
    
        
    
    def initParametersEquationThermalGaussian(self):
        """
        Initializes the fit parameters for the Thermal Gaussian equation. 
        Sets the parameter values, standard deviations, units, and R² to default (not-a-number) values.

        :return: None
        """
        self.thermalGaussianTcValue="nan"
        self.thermalGaussianTcStd="nan"
        self.thermalGaussianTcUnits=""
        self.thermalGaussianR2="nan"
    
    def initParametersEquationThermalGaussianShift(self):
        """
        Initializes the fit parameters for the Thermal Gaussian Shifted equation.
        Sets the parameter values, standard deviations, units, and R² to default (not-a-number) values.

        :return: None
        """
        self.thermalGaussianShiftTcValue="nan"
        self.thermalGaussianShiftTcStd="nan"
        self.thermalGaussianShiftTcUnits=""
        self.thermalGaussianShiftTdValue="nan"
        self.thermalGaussianShiftTdStd="nan"
        self.thermalGaussianShiftTdUnits=""
        self.thermalGaussianShiftBValue="nan"   
        self.thermalGaussianShiftBStd="nan"
        self.thermalGaussianShiftBUnits=""
        self.thermalGaussianShiftR2="nan"
    
    def initParametersEquationThermalLorentzian(self):
        """
        Initializes the fit parameters for the Thermal Lorentzian equation.
        Sets the parameter value, standard deviation, units, and R² to default (not-a-number) values.

        :return: None
        """
        self.thermalLorentzianT0Value="nan"
        self.thermalLorentzianT0Std="nan"
        self.thermalLorentzianT0Units=""
        self.thermalLorentzianR2="nan"
    
    def initParametersEquationThermalLorentzianShift(self):
        """
        Initializes the fit parameters for the shifted Thermal Lorentzian equation.
        All parameter values, standard deviations, units, and R² are set to default (not-a-number) values.

        :return: None
        """
        self.thermalLorentzianShiftT0Value="nan"
        self.thermalLorentzianShiftT0Std="nan"
        self.thermalLorentzianShiftT0Units=""
        self.thermalLorentzianShiftTdValue="nan"
        self.thermalLorentzianShiftTdStd="nan"
        self.thermalLorentzianShiftTdUnits=""
        self.thermalLorentzianShiftBValue="nan"
        self.thermalLorentzianShiftBStd="nan"
        self.thermalLorentzianShiftBUnits=""
        self.thermalLorentzianShiftR2="nan"
        
    
    def initParametersEquationAntiBunching(self):
        """
        Initializes the fit parameters for the Antibunching equation.
        All parameter values, standard deviations, units, and R² are set to default (not-a-number) values.

        :return: None
        """
        self.antiBunchingTauAValue="nan"
        self.antiBunchingTauAStd="nan"
        self.antiBunchingTauAUnits=""
        self.antiBunchingR2="nan"
    
    def initParametersEquationAntiBunchingShift(self):
        """
        Initializes the fit parameters for the shifted Antibunching equation.
        All values, standard deviations, units, and R² are set to default (not-a-number) values.

        :return: None
        """
        self.antiBunchingShiftTauAValue="nan"
        self.antiBunchingShiftTauAStd="nan"
        self.antiBunchingShiftTauAUnits=""
        self.antiBunchingShiftTaudValue="nan"
        self.antiBunchingShiftTaudStd="nan"
        self.antiBunchingShiftTaudUnits=""
        self.antiBunchingShiftBValue="nan"
        self.antiBunchingShiftBStd="nan"
        self.antiBunchingShiftBUnits=""
        self.antiBunchingShiftR2="nan"
    
    def changeTableParameters(self):
        """
        Updates the UI parameter table and the main curve plot according to the currently selected equation.

        The method first updates the main UI elements, including the fixed delay checkbox and the external delay spinbox, 
        to reflect the current state of the selected equation. It then clears the parameter table and fills it 
        with the parameters corresponding to the selected equation type.

        Depending on the selection in comboBoxEquation, it updates the table and the main plot with the corresponding 
        fit data. If the fit data is empty, the main plot is cleared.

        :return: None
        """

        self.changeExternalCheckBox()
        self.changeExternalSpinBox()
        self.parametersTable.setRowCount(0)
        if self.comboBoxEquation.currentIndex()==0:
            self.changeTermalGaussianTableParameters()
            if len(self.g2FitGaussian)>0:
                self.curveFit.setData(self.tauValues, self.g2FitGaussian)
            else:
                self.curveFit.setData([], [])
                
        elif self.comboBoxEquation.currentIndex()==1:
            self.changeTermalGaussianShiftTableParameters()
            if len(self.g2FitGaussianShift)>0:
                self.curveFit.setData(self.tauValues, self.g2FitGaussianShift)
            else:
                self.curveFit.setData([], [])
        elif self.comboBoxEquation.currentIndex()==2:
            self.changeTermalLorentzianTableParameters()
            if len(self.g2FitLorentzian)>0:
                self.curveFit.setData(self.tauValues, self.g2FitLorentzian)
            else:
                self.curveFit.setData([], [])
        elif self.comboBoxEquation.currentIndex()==3:
            self.changeTermalLorentzianShiftTableParameters()
            if len(self.g2FitLorentzianShift)>0:
                self.curveFit.setData(self.tauValues, self.g2FitLorentzianShift)
            else:
                self.curveFit.setData([], [])
        elif self.comboBoxEquation.currentIndex()==4:
            self.changeAntiBunchingTableParameters()
            if len(self.g2FitAntibunching)>0:
                self.curveFit.setData(self.tauValues, self.g2FitAntibunching)
            else:
                self.curveFit.setData([], [])
        elif self.comboBoxEquation.currentIndex()==5:
            self.changeAntibunchingShiftTableParameters()
            if len(self.g2FitAntibunchingShift)>0:
                self.curveFit.setData(self.tauValues, self.g2FitAntibunchingShift)
            else:
                self.curveFit.setData([], [])
    
    def changeTermalGaussianTableParameters(self):
        """
        Updates the parameter table specifically for the Thermal Gaussian equation.

        This method inserts two rows into the parameters table. The first row corresponds to the Gaussian 
        time constant (Tc) and the second row corresponds to the R² value of the fit.

        If the value of Tc or R² is not available ("nan"), the table shows "Undefined" and leaves the 
        other cells empty. Otherwise, it formats and displays the value, its standard deviation (if applicable), 
        and the units for Tc, and the numeric value for R².

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        if self.thermalGaussianTcValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.thermalGaussianTcValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.thermalGaussianTcStd,self.thermalGaussianTcValue)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.thermalGaussianTcUnits)))
            
        if self.thermalGaussianR2=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem(str(self.thermalGaussianR2)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
    
    
    def changeTermalGaussianShiftTableParameters(self):
        """
        Updates the parameter table for the Thermal Gaussian Shifted equation.

        This method inserts four rows in the parameters table. The first three rows correspond to the 
        fit parameters Tc, Td, and B, and the fourth row shows the R² value of the fit.

        For each parameter, if its value is not defined ("nan"), the table shows "Undefined" and leaves 
        the remaining cells empty. If a value exists, it displays the formatted value, its standard deviation, 
        and units. The R² row only displays the numeric value if available.

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        self.parametersTable.insertRow(2)
        self.parametersTable.insertRow(3)
        if self.thermalGaussianShiftTcValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.thermalGaussianShiftTcValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.thermalGaussianShiftTcStd,self.thermalGaussianShiftTcValue)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.thermalGaussianShiftTcUnits)))
        
        
        if self.thermalGaussianShiftTdValue=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem(self.formatValue(self.thermalGaussianShiftTdValue)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(self.formatStd(self.thermalGaussianShiftTdStd,self.thermalGaussianShiftTdValue )))
            self.parametersTable.setItem(1,3,QTableWidgetItem(str(self.thermalGaussianShiftTdUnits)))
        
        if self.thermalGaussianShiftBValue=="nan":
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(2,2,QTableWidgetItem(""))
            self.parametersTable.setItem(2,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem(self.formatValue(self.thermalGaussianShiftBValue)))
            self.parametersTable.setItem(2,2,QTableWidgetItem(self.formatStd(self.thermalGaussianShiftBStd,self.thermalGaussianShiftBValue)))
            self.parametersTable.setItem(2,3,QTableWidgetItem(str(self.thermalGaussianShiftBUnits)))
        
        
        if self.thermalGaussianShiftR2=="nan":
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem(str(self.thermalGaussianShiftR2)))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
    
    
    def changeTermalLorentzianTableParameters(self):
        """
        Updates the parameter table for the Thermal Lorentzian equation.

        This method inserts two rows in the table. The first row corresponds to the T0 fit parameter and 
        the second row to the R² value. If a parameter value is "nan", it displays "Undefined" and leaves 
        the other cells empty. Otherwise, it shows the formatted value, its standard deviation, and units. 
        The R² row only shows the numeric value if available.

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        if self.thermalLorentzianT0Value=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameT0))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameT0))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.thermalLorentzianT0Value)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.thermalLorentzianT0Std,self.thermalLorentzianT0Value)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.thermalLorentzianT0Units)))
            
        if self.thermalLorentzianR2=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem(str(self.thermalLorentzianR2)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
    
    def changeTermalLorentzianShiftTableParameters(self):
        """
        Updates the parameter table for the Thermal Lorentzian Shifted equation.

        Four rows are inserted corresponding to the fit parameters T0, Td, B, and the R² value. Each row
        displays the parameter name, formatted value, standard deviation, and units if available. If a
        parameter value is "nan", the table shows "Undefined" and leaves the other columns empty.

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        self.parametersTable.insertRow(2)
        self.parametersTable.insertRow(3)
        if self.thermalLorentzianShiftT0Value=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameT0))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameT0))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.thermalLorentzianShiftT0Value)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.thermalLorentzianShiftT0Std,self.thermalLorentzianShiftT0Value)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.thermalLorentzianShiftT0Units)))
        
        
        if self.thermalLorentzianShiftTdValue=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem(self.formatValue(self.thermalLorentzianShiftTdValue)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(self.formatStd(self.thermalLorentzianShiftTdStd,self.thermalLorentzianShiftTdValue)))
            self.parametersTable.setItem(1,3,QTableWidgetItem(str(self.thermalLorentzianShiftTdUnits)))
        
        if self.thermalLorentzianShiftBValue=="nan":
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(2,2,QTableWidgetItem(""))
            self.parametersTable.setItem(2,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem(self.formatValue(self.thermalLorentzianShiftBValue)))
            self.parametersTable.setItem(2,2,QTableWidgetItem(self.formatStd(self.thermalLorentzianShiftBStd,self.thermalLorentzianShiftBValue)))
            self.parametersTable.setItem(2,3,QTableWidgetItem(str(self.thermalLorentzianShiftBUnits)))
        
        
        if self.thermalLorentzianShiftR2=="nan":
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem(str(self.thermalLorentzianShiftR2)))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
    
    
    def changeAntiBunchingTableParameters(self):
        """
        Updates the parameter table for the Antibunching equation.

        Two rows are inserted for the TauA parameter and the R² value. Each row displays the parameter name, 
        formatted value, standard deviation, and units if available. If a parameter value is "nan", the table 
        shows "Undefined" and leaves the other columns empty.

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        if self.antiBunchingTauAValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.antiBunchingTauAValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.antiBunchingTauAStd,self.antiBunchingTauAValue)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.antiBunchingTauAUnits)))
            
        if self.antiBunchingR2=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(1,1,QTableWidgetItem(str(self.antiBunchingR2)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
    
    
    def changeAntibunchingShiftTableParameters(self):
        """
        Updates the parameter table for the Antibunching Shift equation.

        Four rows are inserted for the parameters TauA, Taud, B, and R². Each row displays the parameter name, 
        formatted value, standard deviation, and units if available. If a parameter value is "nan", the table 
        shows "Undefined" and leaves the other columns empty.

        :return: None
        """
        self.parametersTable.insertRow(0)
        self.parametersTable.insertRow(1)
        self.parametersTable.insertRow(2)
        self.parametersTable.insertRow(3)
        if self.antiBunchingShiftTauAValue=="nan":
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(0,2,QTableWidgetItem(""))
            self.parametersTable.setItem(0,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(0,0,QTableWidgetItem(self.nameTc))
            self.parametersTable.setItem(0,1,QTableWidgetItem(self.formatValue(self.antiBunchingShiftTauAValue)))
            self.parametersTable.setItem(0,2,QTableWidgetItem(self.formatStd(self.antiBunchingShiftTauAStd,self.antiBunchingShiftTauAValue)))
            self.parametersTable.setItem(0,3,QTableWidgetItem(str(self.antiBunchingShiftTauAUnits)))
        
        
        if self.antiBunchingShiftTaudValue=="nan":
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(1,2,QTableWidgetItem(""))
            self.parametersTable.setItem(1,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(1,0,QTableWidgetItem(self.nameTd))
            self.parametersTable.setItem(1,1,QTableWidgetItem(self.formatValue(self.antiBunchingShiftTaudValue)))
            self.parametersTable.setItem(1,2,QTableWidgetItem(self.formatStd(self.antiBunchingShiftTaudStd,self.antiBunchingShiftTaudValue)))
            self.parametersTable.setItem(1,3,QTableWidgetItem(str(self.antiBunchingShiftTaudUnits)))
        
        if self.antiBunchingShiftBValue=="nan":
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(2,2,QTableWidgetItem(""))
            self.parametersTable.setItem(2,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(2,0,QTableWidgetItem(self.nameB))
            self.parametersTable.setItem(2,1,QTableWidgetItem(self.formatValue(self.antiBunchingShiftBValue)))
            self.parametersTable.setItem(2,2,QTableWidgetItem(self.formatStd(self.antiBunchingShiftBStd,self.antiBunchingShiftBValue)))
            self.parametersTable.setItem(2,3,QTableWidgetItem(str(self.antiBunchingShiftBUnits)))
        
        
        if self.antiBunchingShiftR2=="nan":
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem("Undefined"))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
        else:
            self.parametersTable.setItem(3,0,QTableWidgetItem(self.nameR2))
            self.parametersTable.setItem(3,1,QTableWidgetItem(str(self.antiBunchingShiftR2)))
            self.parametersTable.setItem(3,2,QTableWidgetItem(""))
            self.parametersTable.setItem(3,3,QTableWidgetItem(""))
    
    def formatValue(self,value):
        """
        Formats a numerical value for display in the parameter table.

        Values between 0.01 and 1,000,000 are shown with two decimal places. Values outside this range 
        are displayed in scientific notation with two significant figures. Zero is formatted as "0.00".

        :param value: The numerical value to format (float or int).
        :return: Formatted string representing the value (str).
        """
        if value == 0:
            return "0.00"
        abs_val = abs(value)
        if 0.01 <= abs_val < 1e6:
            return f"{value:.2f}"
        else:
            return f"{value:.2e}"
    
    
    def formatStd(self,valueVar,valueEstimated):
        """
        Formats the standard deviation of a parameter for display in the table.

        If the standard deviation is "N/A", it returns it unchanged. Negative values return "nan". 
        If the relative uncertainty (std / estimated value) exceeds 3, it returns "nan". Values of 0 
        are formatted as "0.00". Values between 0.01 and 1,000,000 are shown with two decimals, and 
        other values are displayed in scientific notation with two significant figures.

        :param valueVar: The variance or standard deviation to format (float, int, or "N/A").
        :param valueEstimated: The estimated value of the parameter (float or int) used to calculate relative uncertainty.
        :return: Formatted string representing the standard deviation (str).
        """
        if valueVar=="N/A":
            return valueVar
        if valueVar<0:
            return "nan"
        valueStd=np.sqrt(valueVar)
        relativeUncertainty=valueStd/abs(valueEstimated)
        if relativeUncertainty>3:
            return "nan"   
        if valueVar == 0:
            return "0.00"
        abs_val = abs(valueVar)
        if 0.01 <= abs_val < 1e6:
            return f"{valueVar:.2f}"
        else:
            return f"{valueVar:.2e}"
    
    
    def thermalGaussian(self,t,T_c):
        """
        Computes the thermal Gaussian correlation function.

        :param t: Time values (list or np.ndarray)
        :param T_c: Correlation time (float)
        :return: Values of the thermal Gaussian function at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-np.pi*((t/T_c)**2))

    def thermalGaussianShift(self,t,T_c,T_d,b):
        """
        Computes the thermal Gaussian correlation function with a time shift and baseline.

        :param t: Time values (list or np.ndarray)
        :param T_c: Correlation time (float)
        :param T_d: Time shift (float)
        :param b: Baseline offset (float)
        :return: Values of the shifted thermal Gaussian function at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        T_c=float(T_c)
        T_d=float(T_d)
        b=float(b)
        return 1+exp(-np.pi*((np.abs(t-T_d)/T_c)**2))+b
    
    def thermalGaussianShiftFixed(self,t,T_c,b):
        """
        Computes the thermal Gaussian correlation function with a fixed time shift.

        The time shift T_d is taken from the initial parameter depending on the units measured.

        :param t: Time values (list or np.ndarray)
        :param T_c: Correlation time (float)
        :param b: Baseline offset (float)
        :return: Values of the shifted thermal Gaussian function at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.thermalGaussianShiftTdInitial
        else:
            T_d = self.thermalGaussianShiftTdInitial / 1000
        return 1+exp(-np.pi*((np.abs(t-T_d)/T_c)**2))+b
    
    def thermalLorentzian(self,t,T_0):
        """
        Computes the thermal Lorentzian correlation function.

        :param t: Time values (list or np.ndarray)
        :param T_0: Characteristic decay time (float)
        :return: Values of the thermal Lorentzian function at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-2*(np.abs(t)/T_0))
    
    def thermalLorentzianShift(self,t,T_0,T_d,b):
        """
        Computes the thermal Lorentzian correlation function with a time shift and offset.

        :param t: Time values (list or np.ndarray)
        :param T_0: Characteristic decay time (float)
        :param T_d: Time shift (float)
        :param b: Constant offset (float)
        :return: Values of the shifted thermal Lorentzian function at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-2*(np.abs(t-T_d)/T_0))+b
    
    def thermalLorentzianShiftFixed(self,t,T_0,b):
        """
        Computes the thermal Lorentzian correlation function with a fixed time shift and offset.

        The time shift T_d is taken from the initial value stored in the object,
        and automatically converted if the units are not in nanoseconds.

        :param t: Time values (list or np.ndarray)
        :param T_0: Characteristic decay time (float)
        :param b: Constant offset (float)
        :return: Values of the thermal Lorentzian function with fixed shift at each time t (np.ndarray)
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.thermalLorentzianShiftTdInitial
        else:
            T_d = self.thermalLorentzianShiftTdInitial / 1000
        return 1+exp(-2*(np.abs(t-T_d)/T_0))+b
    
    def antiBunching(self,t,T_c):
        """
        Computes the antibunching correlation function.

        :param t: Time values (list or np.ndarray)
        :param T_c: Characteristic antibunching time (float)
        :return: Antibunching function values as np.ndarray
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-1*((t/T_c)))
    
    def antiBunchingShift(self,t,T_c,T_d,b):
        """
        Computes the shifted antibunching correlation function.

        :param t: Time values (list or np.ndarray)
        :param T_c: Characteristic antibunching time (float)
        :param T_d: Time shift applied to the function (float)
        :param b: Baseline offset added to the function (float)
        :return: Shifted antibunching function values as np.ndarray
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-1*((np.abs(t-T_d)/T_c)))+b
    
    def antiBunchingShiftFixed(self,t,T_c,b):
        """
        Computes the shifted antibunching correlation function with a fixed time shift.

        :param t: Time values (list or np.ndarray)
        :param T_c: Characteristic antibunching time (float)
        :param b: Baseline offset added to the function (float)
        :return: Shifted antibunching function values as np.ndarray
        """
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.antiBunchingShiftTaudInitial
        else:
            T_d = self.antiBunchingShiftTaudInitial / 1000
        return 1+exp(-1*((np.abs(t-T_d)/T_c)))+b
    
    def applyFitAction(self):
        """
        Applies the selected fit to the current data. 
        The function disables the fit button and equation selector during processing.
        It determines which equation is selected, applies the corresponding fit, 
        and updates the parameter table with the fit results. Once done, it re-enables
        the UI controls.

        :return: None
        """
        self.applyFitButton.setEnabled(False)
        self.comboBoxEquation.setEnabled(False)
        if self.comboBoxEquation.currentIndex()==0:
            parametersList,stdList=self.applyFit("Thermal gaussian")
            self.applyFitToTable(parametersList, stdList,"Thermal gaussian")
        if self.comboBoxEquation.currentIndex()==1:
            parametersList,stdList=self.applyFit("GaussianShift")
            self.applyFitToTable(parametersList, stdList, "GaussianShift")
        if self.comboBoxEquation.currentIndex()==2:
            parametersList,stdList=self.applyFit("Thermal lorentzian")
            self.applyFitToTable(parametersList, stdList, "Thermal lorentzian")
        if self.comboBoxEquation.currentIndex()==3:
            parametersList,stdList=self.applyFit("LorentzianShift")
            self.applyFitToTable(parametersList, stdList, "LorentzianShift")
        if self.comboBoxEquation.currentIndex()==4:
            parametersList,stdList=self.applyFit("AntiBunching")
            self.applyFitToTable(parametersList, stdList,"AntiBunching")
        if self.comboBoxEquation.currentIndex()==5:
            parametersList,stdList=self.applyFit("AntiBunchingShift")
            self.applyFitToTable(parametersList, stdList,"AntiBunchingShift")
        self.applyFitButton.setEnabled(True)
        self.comboBoxEquation.setEnabled(True)
            
        
    
    def applyFitToTable(self, parametersList, stdList,fitApplied):
        """
        Applies the results of a curve fit to the corresponding parameters in the application,
        updates the plotted curve, calculates the goodness of fit (R²), and updates the parameter table in the UI.
        If the fit fails, produces NaN values, or the parameter list is empty, the method resets the parameters 
        for the selected equation to their default state and notifies the user with a dialog.

        The function handles six types of fits: 
        - Thermal Gaussian
        - Gaussian Shift
        - Thermal Lorentzian
        - Lorentzian Shift
        - AntiBunching
        - AntiBunching Shift

        For each fit type, it assigns the fitted parameter values and their standard deviations to 
        internal variables, computes the fitted g² curve, and calculates R². 
        If the fitted curve contains invalid values (NaNs), the method resets the parameters and shows a warning dialog.
        After updating or resetting the parameters, the corresponding table in the UI is refreshed to reflect the current values.

        :param parametersList: List of fitted parameter values (list). The order depends on the selected fit type.
        :param stdList: List of standard deviations of the fitted parameters (list). Same order as parametersList.
        :param fitApplied: Name of the fit applied (str). Must be one of the recognized fit types.
        :return: None
        """
        try:
            if fitApplied=="Thermal gaussian":
                if len(parametersList)>0:
                    self.thermalGaussianTcValue=parametersList[0]
                    self.thermalGaussianTcStd=stdList[0]
                    self.g2FitGaussian=self.thermalGaussian(self.tauValues,self.thermalGaussianTcValue)
                    self.thermalGaussianR2=self.calculateR2(self.g2Values,self.g2FitGaussian)
                    self.curveFit.setData(self.tauValues, self.g2FitGaussian)
                else:
                    self.initParametersEquationThermalGaussian()
            if fitApplied=="GaussianShift":
                if len(parametersList)>0:
                    self.thermalGaussianShiftTcValue=parametersList[0]
                    self.thermalGaussianShiftTcStd=stdList[0]
                    self.thermalGaussianShiftTdValue=parametersList[1]
                    self.thermalGaussianShiftTdStd=stdList[1]
                    self.thermalGaussianShiftBValue=parametersList[2]
                    self.thermalGaussianShiftBStd=stdList[2]
                    self.g2FitGaussianShift=self.thermalGaussianShift(self.tauValues,self.thermalGaussianTcValue,self.thermalGaussianShiftTdValue,self.thermalGaussianShiftBValue)
                    if np.any(np.isnan(self.g2FitGaussianShift)):
                        self.initParametersEquationThermalGaussianShift()
                        self.showDialogNoFitParameters()
                    else:    
                        self.thermalGaussianShiftR2=self.calculateR2(self.g2Values,self.g2FitGaussianShift)
                        self.curveFit.setData(self.tauValues, self.g2FitGaussianShift)
                else:
                    self.initParametersEquationThermalGaussianShift()
            if fitApplied=="Thermal lorentzian":
                if len(parametersList)>0:
                    self.thermalLorentzianT0Value=parametersList[0]
                    self.thermalLorentzianT0Std=stdList[0]
                    self.g2FitLorentzian=self.thermalLorentzian(self.tauValues,self.thermalLorentzianT0Value)
                    if np.any(np.isnan(self.g2FitLorentzian)):
                        self.initParametersEquationThermalLorentzian()
                        self.showDialogNoFitParameters()
                    else:    
                        self.thermalLorentzianR2=self.calculateR2(self.g2Values,self.g2FitLorentzian)
                        self.curveFit.setData(self.tauValues, self.g2FitLorentzian)
                else:
                    self.initParametersEquationThermalLorentzian()
            if fitApplied=="LorentzianShift":
                if len(parametersList)>0:
                    self.thermalLorentzianShiftT0Value=parametersList[0]
                    self.thermalLorentzianShiftT0Std=stdList[0]
                    self.thermalLorentzianShiftTdValue=parametersList[1]
                    self.thermalLorentzianShiftTdStd=stdList[1]
                    self.thermalLorentzianShiftBValue=parametersList[2]
                    self.thermalLorentzianShiftBStd=stdList[2]
                    self.g2FitLorentzianShift=self.thermalLorentzianShift(self.tauValues,self.thermalLorentzianShiftT0Value,self.thermalLorentzianShiftTdValue,self.thermalLorentzianShiftBValue)
                    if np.any(np.isnan(self.g2FitLorentzianShift)):
                        self.initParametersEquationThermalLorentzianShift()
                        self.showDialogNoFitParameters()
                    else:
                        self.thermalLorentzianShiftR2=self.calculateR2(self.g2Values,self.g2FitLorentzianShift)
                        self.curveFit.setData(self.tauValues, self.g2FitLorentzianShift)
                else:
                    self.initParametersEquationThermalLorentzianShift()
            if fitApplied=="AntiBunching":
                if len(parametersList)>0:
                    self.antiBunchingTauAValue=parametersList[0]
                    self.antiBunchingTauAStd=stdList[0]
                    self.g2FitAntibunching=self.antiBunching(self.tauValues,self.antiBunchingTauAValue)
                    if np.any(np.isnan(self.g2FitAntibunching)):
                        self.initParametersEquationAntiBunching()
                        self.showDialogNoFitParameters()
                    else:
                        self.antiBunchingR2=self.calculateR2(self.g2Values,self.g2FitAntibunching)
                        self.curveFit.setData(self.tauValues, self.g2FitAntibunching)
                else:
                    self.initParametersEquationAntiBunching()
            if fitApplied=="AntiBunchingShift":
                if len(parametersList)>0:
                    self.antiBunchingShiftTauAValue=parametersList[0]
                    self.antiBunchingShiftTauAStd=stdList[0]
                    self.antiBunchingShiftTaudValue=parametersList[1]
                    self.antiBunchingShiftTaudStd=stdList[1]
                    self.antiBunchingShiftBValue=parametersList[2]
                    self.antiBunchingShiftBStd=stdList[2]
                    self.g2FitAntibunchingShift=self.antiBunchingShift(self.tauValues,self.antiBunchingShiftTauAValue,self.antiBunchingShiftTaudValue,self.antiBunchingShiftBValue)
                    if np.any(np.isnan(self.g2FitAntibunchingShift)):
                        self.initParametersEquationAntiBunchingShift()
                        self.showDialogNoFitParameters()
                    else:
                        self.antiBunchingShiftR2=self.calculateR2(self.g2Values,self.g2FitAntibunchingShift)
                        self.curveFit.setData(self.tauValues, self.g2FitAntibunchingShift)
                else:
                    self.initParametersEquationAntiBunchingShift()
        except:
            if fitApplied=="Thermal gaussian":
                self.initParametersEquationThermalGaussian()
            elif fitApplied=="GaussianShift":
                self.initParametersEquationThermalGaussianShift()
            elif fitApplied=="Thermal lorentzian":
                self.initParametersEquationThermalLorentzian()
            elif fitApplied=="LorentzianShift":
                self.initParametersEquationThermalLorentzianShift()
            elif fitApplied=="AntiBunching":
                self.initParametersEquationAntiBunching()
            elif fitApplied=="AntiBunchingShift":
                self.initParametersEquationAntiBunchingShift()
            self.curveFit.setData([],[])
            self.showDialogNoFitParameters()
        self.changeTableParameters()
    
    def applyFit(self, fitName):
        """
        Performs a curve fit for a selected equation using the measured g² data and initial parameter guesses,
        and returns the fitted parameter values along with their estimated standard deviations.

        The method supports fits for thermal Gaussian, GaussianShift, thermal Lorentzian, LorentzianShift,
        AntiBunching, and AntiBunchingShift. Initial parameters are automatically adjusted according to the
        measurement units (ns or other) and the method can handle fits where certain delay parameters are fixed
        based on the externalDelayGaussianCheckBox. 

        When the fit is successful, the function returns the fitted parameters in the order required by the
        corresponding equation, along with their estimated variances or "N/A" for fixed parameters. If the
        fit fails due to any reason such as non-convergence, the method shows a dialog informing the user and
        returns empty lists for both parameters and standard deviations.

        :param fitName: Name of the fit to apply (str). Must match one of the recognized fit types.
        :return: A tuple containing the list of fitted parameter values and the list of corresponding standard deviations.
        """
        parametersList =[]
        stdList=[]
        try:
            if fitName=="Thermal gaussian":
                if self.unitsMeasured=="ns":
                    p0=[self.thermalGaussianTcInitial]
                else:
                    p0=[self.thermalGaussianTcInitial/1000]
                popt, pcov= curve_fit(self.thermalGaussian, self.tauValues, self.g2Values,p0)
                parametersList=popt
                stdList=[pcov[0,0]]
            elif fitName=="GaussianShift":
                if self.unitsMeasured=="ns":
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.self.thermalGaussianTcInitial,self.thermalGaussianShiftTdInitial,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.self.thermalGaussianTcInitial,self.thermalGaussianShiftBInitial]
                else:
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalGaussianTcInitial/1000,self.thermalGaussianShiftTdInitial/1000,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.thermalGaussianTcInitial/1000,self.thermalGaussianShiftBInitial]
                
                if self.externalDelayGaussianCheckBox:
                    popt, pcov= curve_fit(self.thermalGaussianShiftFixed, self.tauValues, self.g2Values,p0)
                    if self.unitsMeasured=="ns":
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital, popt[1]]
                    else:
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital/1000, popt[1]]
                    stdList=[pcov[0,0],"N/A",pcov[1,1]]
                else:
                    popt, pcov= curve_fit(self.thermalGaussianShift, self.tauValues, self.g2Values,p0)
                    parametersList=popt
                    stdList=[pcov[0,0],pcov[1,1],pcov[2,2]]
            elif fitName == "Thermal lorentzian":
                if self.unitsMeasured=="ns":
                    p0=[self.thermalLorentzianT0Initial]
                else:
                    p0=[self.thermalLorentzianT0Initial/1000]
                popt, pcov= curve_fit(self.thermalLorentzian, self.tauValues, self.g2Values,p0)
                parametersList=popt
                stdList=[pcov[0,0]]
            elif fitName == "LorentzianShift":
                if self.unitsMeasured=="ns":
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalLorentzianT0Initial,self.thermalGaussianShiftTdInitial,self.thermalGaussianShiftBInitial]
                    else:
                        
                        p0=[self.thermalLorentzianT0Initial,self.thermalGaussianShiftBInitial]
                else:
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalLorentzianT0Initial/1000,self.thermalGaussianShiftTdInitial/1000,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.thermalLorentzianT0Initial/1000,self.thermalGaussianShiftBInitial]
                
                if self.externalDelayGaussianCheckBox:
                    
                    popt, pcov= curve_fit(self.thermalLorentzianShiftFixed, self.tauValues, self.g2Values,p0)
                    if self.unitsMeasured=="ns":
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital, popt[1]]
                    else:
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital/1000, popt[1]]
                    stdList=[pcov[0,0],"N/A",pcov[1,1]]
                else:
                    popt, pcov= curve_fit(self.thermalLorentzianShift, self.tauValues, self.g2Values,p0)
                    parametersList=popt
                    stdList=[pcov[0,0],pcov[1,1],pcov[2,2]]
            elif fitName == "AntiBunching":
                if self.unitsMeasured=="ns":
                    p0=[self.thermalGaussianTcInitial]
                else:
                    p0=[self.thermalGaussianTcInitial/1000]
                popt, pcov= curve_fit(self.antiBunching, self.tauValues, self.g2Values,p0)
                parametersList=popt
                stdList=[pcov[0,0]]
            elif fitName == "AntiBunchingShift":
                if self.unitsMeasured=="ns":
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalGaussianTcInitial,self.thermalGaussianShiftTdInitial,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.thermalGaussianTcInitial,self.thermalGaussianShiftBInitial]
                else:
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalGaussianTcInitial/1000,self.thermalGaussianShiftTdInitial/1000,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.thermalGaussianTcInitial/1000,self.thermalGaussianShiftBInitial]
                
                if self.externalDelayGaussianCheckBox:
                    popt, pcov= curve_fit(self.antiBunchingShiftFixed, self.tauValues, self.g2Values,p0)
                    if self.unitsMeasured=="ns":
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital, popt[1]]
                    else:
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital/1000, popt[1]]
                    stdList=[pcov[0,0],"N/A",pcov[1,1]]
                else:
                    popt, pcov= curve_fit(self.antiBunchingShift, self.tauValues, self.g2Values,p0)
                    parametersList=popt
                    stdList=[pcov[0,0],pcov[1,1],pcov[2,2]]
            self.resetSaveSentinels()
        except:
            self.showDialogNoFitParameters()
            parametersList=[]
            stdList=[]
        return parametersList, stdList
        
    
    def calculateR2(self, data, fitData):
        """
        Computes the coefficient of determination (R²) between measured and fitted data.

        :param data: Measured data points (list).
        :param fitData: Fitted data points (list).
        :return: R² value rounded to two decimal places (float).
        """
        arrayData = array(data)
        arrayFit  = array(fitData)
        meanData  = mean(arrayData)

        ssReg = sum((arrayFit - meanData) ** 2)   # SSR
        ssTot = sum((arrayData - meanData) ** 2)  # SST

        R2 = ssReg / ssTot
        return round(R2, 2)
    
    def showDialogNoFitParameters(self):
        """
        Displays a warning dialog indicating that the fit parameters could not be estimated.

        :return: None
        """
        QMessageBox.warning(
            self.mainWindow,
            "Fit Parameters Not Estimated",
            "The fit parameters could not be estimated for the current data.\n"
            "Please verify that the data is sufficient and properly distributed."
        )
    
    
    #Manual measurement 
    def startManualMeasurement(self):
        """
        Starts a manual measurement session. The user can start and stop the measurement using
        the corresponding buttons. Initializes measurement settings, retrieves selected
        parameters, and starts the worker thread for data acquisition.

        :return: None
        """
        self.stopManualButton.setEnabled(True)
        self.startManualButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.generalSettingsBeforeMeasurement(0)
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeComboBox.currentText())
        numberBins=int(self.numberBinsLabel.text())
        self.checkRangesMode(channelSelected,maximumTime)
        
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device, self.modeToMeasure, self.getUnits())
        self.threadSettingsBeforeMeasurement(0)
        self.disableTabs()
        self.worker.start()
    
    def enableTabs(self):
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.mainWindow.tabs.setTabEnabled(2,True)
        self.mainWindow.tabs.setTabEnabled(3,True)
    

    def disableTabs(self):
        self.mainWindow.tabs.setTabEnabled(0,False)
        self.mainWindow.tabs.setTabEnabled(1,False)
        self.mainWindow.tabs.setTabEnabled(2,False)
        self.mainWindow.tabs.setTabEnabled(3,False)

    def checkRangesMode(self,channel, maximumTime):
        """
        Determines the optimal measurement mode for the device based on the selected 
        channel and the maximum measurement time. Some device channels support multiple
        modes, and the appropriate mode is chosen to ensure accurate measurements within 
        the specified maximum time. The selected mode is stored in the instance variable 
        `modeToMeasure`.

        :param channel: The channel to be measured (int).
        :param maximumTime: The maximum measurement time in picoseconds (int).
        :return: None
        """
        modeChannelSelected=int(self.device.getMode(channel))
        if modeChannelSelected==1 and maximumTime>500000:
            self.modeToMeasure=2
        elif modeChannelSelected==2 and maximumTime<125000:
            self.modeToMeasure=1
        else:
            self.modeToMeasure=modeChannelSelected
    
    def getUnits(self):
        """
        Retrieves the time units selected in the maximum time combo box, updates the 
        internal `unitsMeasured` variable, updates the plot label and parameter units 
        accordingly, and returns the selected units.

        :return: The selected time units as a string ('ps', 'ns', 'us', or 'ms').
        """
        unitsLabel="ps"
        if self.maximumTimeComboBox.currentText().endswith("ps"):
            unitsLabel="ps"
        elif self.maximumTimeComboBox.currentText().endswith("ns"):
            unitsLabel="ns"
        elif self.maximumTimeComboBox.currentText().endswith("μs"):
            unitsLabel="us"
        elif self.maximumTimeComboBox.currentText().endswith("ms"):
            unitsLabel="ms"
        self.unitsMeasured=unitsLabel
        bottomLabel=f"Tau ({unitsLabel})"
        self.updateParameterUnits(unitsLabel)
        self.plotG2.setLabel('bottom',bottomLabel)
        return unitsLabel
    
    def updateParameterUnits(self, unitsLabel):
        """
        Updates the units for all initial measurement parameters to the specified label.

        :param unitsLabel: The units to assign to the parameters (str), e.g., 'ps', 'ns', 'us', or 'ms'.
        :return: None
        """
        self.thermalGaussianTcUnits=unitsLabel
        self.thermalGaussianShiftTcUnits=unitsLabel
        self.thermalGaussianShiftTdUnits=unitsLabel
        self.thermalLorentzianT0Units=unitsLabel
        self.thermalLorentzianShiftT0Units=unitsLabel
        self.thermalLorentzianShiftTdUnits=unitsLabel
        self.thermalLorentzianShiftTdUnits=unitsLabel
        self.antiBunchingTauAUnits=unitsLabel
        self.antiBunchingShiftTauAUnits=unitsLabel
        self.antiBunchingShiftTaudUnits=unitsLabel
        
        
    
    
    def stopManualMeasurement(self):
        """
        Stops the ongoing manual measurement by stopping the worker thread
        and disables the stop button.

        :return: None
        """
        self.worker.stop()
        self.stopManualButton.setEnabled(False)
        self.enableTabs()
        
    def getPicoSecondsValue(self, valueStr):
        """
        Converts a time value with units (ps, ns, us, ms) to picoseconds.

        :param valueStr: A string containing the value and its unit, e.g., '10 ns' (str).
        :return: The value converted to picoseconds (float).
        """
        units=valueStr.split(" ")
        print(units)
        if units[1]=="ps":
            value=float(units[0])
        elif units[1]=="ns":
            value=float(units[0])*(10**(3))
        elif units[1]=="μs":
            value=float(units[0])*(10**(6))
        elif units[1]=="ms":
            value=float(units[0])*(10**(9))
        return value
        
    
    def clearManualMeasurement(self):
        """
        Clears the data captured during a manual measurement by calling the worker thread.

        :return: None
        """
        self.worker.clearG2()
        
     
    #By size measurement
    def startLimitedMeasurement(self):
        """
        Starts a limited manual measurement in which the user specifies the number of measurements 
        to perform. After reaching this number, the measurement automatically stops.

        Configures the measurement parameters, disables/enables the corresponding buttons and spinboxes,
        determines the device mode based on the selected channel and maximum time, and starts the worker thread.

        :return: None
        """
        self.stopLimitedButtonG2.setEnabled(True)
        self.startLimitedButtonG2.setEnabled(False)
        self.clearLimitedButtonG2.setEnabled(True)
        self.numberMeasurementsSpinBox.setEnabled(False)
        self.generalSettingsBeforeMeasurement(1)
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeComboBox.currentText())
        numberBins=int(self.numberBinsLabel.text())
        numberMeasurements=int(self.numberMeasurementsSpinBox.value())
        self.checkRangesMode(channelSelected,maximumTime)
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device,self.modeToMeasure, self.getUnits(), True, numberMeasurements)
        self.threadSettingsBeforeMeasurement(1)
        self.disableTabs()
        self.worker.start()
        
        
    
    def stopLimitedMeasurement(self):
        """
        Stops the ongoing limited manual measurement and disables the corresponding stop button.

        This interrupts the worker thread responsible for collecting the data.

        :return: None
        """
        self.worker.stop()
        self.stopLimitedButtonG2.setEnabled(False)
        self.enableTabs()
    
    def stopAutoClearMeasurement(self):
        """
        Stops the auto-clear measurement. This stops the data collection worker
        thread and disables the QTimer that periodically clears the graph.

        :return: None
        """
        self.worker.stop()
        self.autoClearTimer.stop()
        self.stopAutoClearButton.setEnabled(False)
        self.enableTabs()
        
    
    #Auto clear measurement
    def startAutoClearMeasurement(self):
        """
        Starts an auto-clear measurement where the plot is periodically cleared
        based on the user-selected time interval. This measurement continuously
        collects data while automatically resetting the graph at each interval.

        Sets up and starts the worker thread for data collection and a QTimer
        to trigger the clearing of the graph.

        :return: None
        """
        self.stopAutoClearButton.setEnabled(True)
        self.startAutoClearButton.setEnabled(False)
        self.clearAutoClearButton.setEnabled(True)
        self.autoClearSpinBox.setEnabled(False)
        self.generalSettingsBeforeMeasurement(2)
        self.autoClearTimer=QTimer()
        self.autoClearTimer.timeout.connect(self.clearManualMeasurement)
        channelSelected=self.getChannelComboBox()
        coincidenceWindowSelected=self.getPicoSecondsValue(self.coincidenceWindowComboBox.currentText())
        maximumTime=self.getPicoSecondsValue(self.maximumTimeComboBox.currentText())
        numberBins=int(self.numberBinsLabel.text())
        self.checkRangesMode(channelSelected,maximumTime)
        self.worker=WorkerThreadG2(channelSelected,maximumTime,numberBins,coincidenceWindowSelected,self.device,self.modeToMeasure, self.getUnits(),False,0,True)
        self.threadSettingsBeforeMeasurement(2)
        self.disableTabs()
        self.worker.start()
    
    def generalSettingsBeforeMeasurement(self, tab):
        """
        Applies general pre-measurement settings for all three types of measurements
        (manual, limited, auto-clear). It stops any running timers, disables
        controls that should not be changed during measurement, resets data
        arrays, flags, and fit parameters. Also manages which tabs are enabled
        based on the selected measurement type.

        :param tab: Index indicating the type of measurement (0: manual, 1: limited, 2: auto-clear).
        :type tab: int
        :return: None
        """
        self.stopTimerConnection()
        self.setVerticalLabel()
        self.applyFitButton.setEnabled(False)
        self.stopChannelSave=self.stopChannelComboBox.currentText()
        self.stopChannelComboBox.setEnabled(False)
        self.coincidenceWindowComboBox.setEnabled(False)
        self.maximumTimeComboBox.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.tauValues=[]
        self.determinedParameters=False
        self.currentMeasurement=True
        self.resetFits()
        if tab==0:
            self.tabSettings.setTabEnabled(1,False)
            self.tabSettings.setTabEnabled(2,False)
        elif tab==1:
            self.tabSettings.setTabEnabled(0,False)
            self.tabSettings.setTabEnabled(2,False)
        else:
            self.tabSettings.setTabEnabled(0,False)
            self.tabSettings.setTabEnabled(1,False)
    
    
    def threadSettingsBeforeMeasurement(self, tab):
        """
        Connects signals from the worker thread responsible for executing the measurement
        to the appropriate GUI update functions. Sets up handling for status updates,
        color changes, estimated parameters, tau values, and measurement data capture.
        Also records the start time of the measurement and connects the worker's finished
        signal to the corresponding finish function based on the type of measurement.

        :param tab: Index indicating the type of measurement (0: manual, 1: limited, 2: auto-clear).
        :type tab: int
        :return: None
        """
        self.worker.updateStatusLabel.connect(self.changeStatus)
        self.worker.updateColorLabel.connect(self.changeStatusColor)
        self.worker.updateEstimatedParameter.connect(self.changeEstimatedParameter)
        self.worker.updateDeterminedParameters.connect(self.changeDeterminedParameters)
        self.worker.updateTauValues.connect(self.captureTauValues)
        self.worker.updateMeasurement.connect(self.captureMeasurement)
        self.initDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tab==0:
            self.worker.finished.connect(self.finishManualMeasurement)
        elif tab==1:
            self.worker.finished.connect(self.finishLimitedMeasurement)
        elif tab==2:
            self.worker.updateFirstParameter.connect(self.changeEstimatedParameterStartTimer)
            self.worker.finished.connect(self.finishAutoClearMeasurement)
            
    
    def resetFits(self):
        """
        Resets all fit data and related parameters for every type of measurement.
        Clears the calculated fit arrays, reinitializes the fit parameters,
        updates the parameters table, clears the displayed curve, and resets
        all save sentinels.

        :return: None
        """
        self.g2FitGaussian=[]
        self.g2FitGaussianShift=[]
        self.g2FitLorentzian=[]
        self.g2FitLorentzianShift=[]
        self.g2FitAntibunching=[]
        self.g2FitAntibunchingShift=[]
        self.initParametersEquationThermalGaussian()
        self.initParametersEquationThermalGaussianShift()
        self.initParametersEquationThermalLorentzian()
        self.initParametersEquationThermalLorentzianShift()
        self.initParametersEquationAntiBunching()
        self.initParametersEquationAntiBunchingShift()
        self.changeTableParameters()
        self.curveFit.setData([], [])
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        self.sentinelsavetxt=0
        
    
    def generalSettingsAfterMeasurement(self, channel):
        """
        Restores general UI and measurement settings after a measurement ends.
        This includes enabling/disabling buttons and combo boxes, setting initial
        parameters if tau values were captured, updating the status and finish time,
        and re-enabling the appropriate tabs depending on which measurement mode
        was active.

        :param channel: Index of the measurement mode that was active (0: Manual, 1: Limited, 2: AutoClear) (int)
        :return: None
        """
        if not self.determinedParameters:
            self.showDialogNoParameters()
        self.startTimerConnection()
        if self.tauValues:
            self.applyFitButton.setEnabled(True)
            self.initialParametersButton.setEnabled(True)
            self.initialParametersWithUnits()
        self.stopChannelComboBox.setEnabled(True)
        self.coincidenceWindowComboBox.setEnabled(True)
        self.maximumTimeComboBox.setEnabled(True)
        self.saveDataButton.setEnabled(True)
        self.savePlotButton.setEnabled(True)
        self.finishDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.changeStatus("No running measurement")
        self.changeStatusColor(0)
        self.currentMeasurement=False
        if channel==0:
            self.tabSettings.setTabEnabled(1,True)
            self.tabSettings.setTabEnabled(2,True)
        elif channel==1:
            self.tabSettings.setTabEnabled(0,True)
            self.tabSettings.setTabEnabled(2,True)
        elif channel==2:
            self.tabSettings.setTabEnabled(0,True)
            self.tabSettings.setTabEnabled(1,True)
    
    
    
    
    def finishManualMeasurement(self):
        """
        Finalizes a manual measurement once the measurement thread finishes.
        Restores the general settings for the UI, disables the stop button,
        enables the start button, and disables the clear button.

        :return: None
        """
        self.generalSettingsAfterMeasurement(0)
        self.stopManualButton.setEnabled(False)
        self.startManualButton.setEnabled(True)
        self.clearButton.setEnabled(False)
        self.enableTabs()
        
        
    
    def finishLimitedMeasurement(self):
        """
        Finalizes a limited measurement once the measurement thread finishes.
        Restores the general settings for the UI, disables the stop button,
        enables the start button, disables the clear button, and re-enables
        the spin box for selecting the number of measurements.

        :return: None
        """
        self.generalSettingsAfterMeasurement(1)
        self.stopLimitedButtonG2.setEnabled(False)
        self.startLimitedButtonG2.setEnabled(True)
        self.clearLimitedButtonG2.setEnabled(False)
        self.numberMeasurementsSpinBox.setEnabled(True)
        self.enableTabs()
    
    
    def finishAutoClearMeasurement(self):
        """
        Finalizes an auto-clear measurement after the measurement thread completes.
        Restores the general settings for the UI, disables the stop button,
        enables the start button, disables the clear button, and re-enables
        the spin box for selecting the auto-clear interval.

        :return: None
        """
        self.generalSettingsAfterMeasurement(2)
        self.stopAutoClearButton.setEnabled(False)
        self.startAutoClearButton.setEnabled(True)
        self.clearAutoClearButton.setEnabled(False)
        self.autoClearSpinBox.setEnabled(True)
        self.enableTabs()
        
    
    
    def showDialogNoParameters(self):
        """
        Displays a warning dialog indicating that there are insufficient measurements
        on the START or STOP channel, making it impossible to determine the parameters
        required to calculate g².

        :return: None
        """
        QMessageBox.warning(
            self.mainWindow,
            "Insufficient Measurements",
            "Not enough measurements have been detected on the START or STOP channel.\n"
            "Therefore, it is not possible to determine the parameters required "
            "to correctly calculate g²."
        )
    
    def showDialogChangeMode(self, channel):
        currentMode=self.device.getMode(channel)
        suggestedMode=((currentMode)%2)+1
        if suggestedMode==1:
            ranges="12ns-500ns"
            rangeLine="(below 125 ns)"
        else:
            ranges="125ns-4ms"
            rangeLine="(above 500 ns)"
        msg = QMessageBox(self.mainWindow)
        msg.setWindowTitle("Mode Selection")
        msg.setText(
            f"Due to the maximum measurement range, mode {currentMode} "
            f"cannot obtain measurements for this range in channel {channel} {rangeLine}. "
            f"Mode {suggestedMode} supports the ranges {ranges}. "
            f"Do you want to switch to mode {suggestedMode} in channel {channel}?"
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.device.setMode(channel,suggestedMode)
    
    def helpButtonDialog(self):
        """
        Displays an informational dialog with instructions for using the g² window.

        This function shows a modal QMessageBox explaining how g²(τ) is calculated
        from the coincidence histogram and the required experimental setup.

        :return: None
        """
        message_box = QMessageBox(self.mainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("g² Information")
        message_box.setText(
            "The second-order correlation function is estimated as:\n\n"
            "g²(τ) ≈ N(τ) / (N² · Δt · T)\n\n"
            "where N(τ) is the coincidence histogram, N is the average count rate, "
            "Δt is the bin width, and T is the integration time.\n\n"
            "A 50/50 beam splitter configuration is required, since the system "
            "measures only Start–Stop time differences for coincidences."
        )
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
        
        
    
    def getChannelComboBox(self):
        """
        Returns the letter of the currently selected STOP channel from the combo box.

        :return: The channel letter as a string ("A", "B", "C", or "D").
        """
        if self.stopChannelComboBox.currentText()=="Channel A":
            return "A"
        elif self.stopChannelComboBox.currentText()=="Channel B":
            return "B"
        elif self.stopChannelComboBox.currentText()=="Channel C":
            return "C"
        elif self.stopChannelComboBox.currentText()=="Channel D":
            return "D"
    #Change status
    def changeStatus(self, text):
        """
        Updates the status label with the provided text.

        :param text: The new status text to display (str).
        :return: None
        """
        self.statusValueLabel.setText(text)
    
    def changeStatusColor(self, color):
        """
        Changes the color of the point in the status bar. Each color is assigned a specific numeric value.

        :param color: The numeric value corresponding to the desired color (int).
                    - 0: Gray
                    - 1: Green
                    - 2: Yellow
                    - 3: Orange
        :return: None
        """
        pixmap = QPixmap(self.statusColorLabel.size())
        pixmap.fill(Qt.transparent)  
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        if color==0:
            painter.setBrush(QColor(128, 128, 128))  
        elif color==1:
            painter.setBrush(QColor(0, 255, 0))  
        elif color==2:
            painter.setBrush(QColor(255, 255, 0))  
        elif color==3:
            painter.setBrush(QColor(255, 165, 0))  
        painter.setPen(Qt.NoPen)
        point_size = min(self.statusColorLabel.width(), self.statusColorLabel.height()) // 2
        x = (self.statusColorLabel.width() - point_size) // 2
        y = (self.statusColorLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusColorLabel.setPixmap(pixmap)
    
    def changeEstimatedParameter(self, text):
        """
        Updates the label showing the currently estimated parameter.

        :param text: The new estimated parameter value to display (str).
        :return: None
        """
        self.calculatedParameter.setText(text)
    
    def changeEstimatedParameterStartTimer(self,text):
        """
        Updates the label with the estimated parameter and starts the auto-clear timer.
        The timer will trigger at intervals defined by the user in the auto-clear spin box.

        :param text: The new estimated parameter value to display (str).
        :return: None
        """
        self.calculatedParameter.setText(text)
        everyValue=self.autoClearSpinBox.value()
        self.autoClearTimer.start(everyValue*1000)
        
    def changeDeterminedParameters(self):
        """
        Sets the flag indicating that the measurement parameters have been determined.

        :return: None
        """
        self.determinedParameters=True
    


    
        
        
    
    def captureTauValues(self, tauValues, unitFactor, mode):
        """
        Captures tau (time delay) values from the measurement thread and updates the G² plot.

        This function sets the tauValues attribute, adjusts the plot's X and Y limits,
        and adds a non-movable shaded region indicating the measurement range. The region
        size depends on the acquisition mode and unit factor.

        :param tauValues: List of tau values from the measurement (list of float).
        :param unitFactor: Conversion factor to adjust the measurement units (float).
        :param mode: Acquisition mode of the device, affecting the region size (int).
        :return: None
        """
        if self.regionDisable:
            self.plotG2.removeItem(self.regionDisable)
        self.tauValues = tauValues
        region = 125000/unitFactor
        if mode == 1:
            region = 12500/unitFactor

        if len(tauValues) > 0:
            x_max = max(tauValues)
            
            margin = x_max * 0.05
            x_min_limit = 0
            x_max_limit = x_max + margin
            
            self.plotG2.getViewBox().setLimits(xMin=x_min_limit, xMax=x_max_limit, yMin=-0.1)
            self.plotG2.setXRange(x_min_limit, x_max_limit, padding=0)
        
        
        self.regionDisable = pg.LinearRegionItem(values=[0, region], orientation="vertical")
        self.regionDisable.setBrush((150,150,150,120))
        self.regionDisable.setMovable(False)
        self.regionDisable.setZValue(-10)
        for line in self.regionDisable.lines:
            line.setPen(pg.mkPen(None))
        self.plotG2.addItem(self.regionDisable)
        
    def checkParametersValue(self):
        """
        Checks whether all initial fit parameters are set to their default values.

        This function verifies if all the initial parameters are either 1 or 1000.
        If so, it sets the `parametersChange` flag to False, indicating no user
        modifications. Otherwise, the flag is set to True.

        :return: None
        """
        values = [
            self.thermalGaussianTcInitial,
            self.thermalGaussianShiftTcInitial,
            self.thermalGaussianShiftTdInitial,
            self.thermalGaussianShiftBInitial,
            self.thermalLorentzianT0Initial,
            self.thermalLorentzianShiftT0Initial,
            self.thermalLorentzianShiftTdInitial,
            self.thermalLorentzianShiftBInitial,
            self.antiBunchingTauAInitial,
            self.antiBunchingShiftTauAInitial,
            self.antiBunchingShiftTaudInitial,
            self.antiBunchingShiftBInitial
        ]

        if all(v == 1 for v in values) or all(v == 1000 for v in values):
            self.parametersChange=False
        else:
            self.parametersChange=True
            
                    
        
    
    
    def captureMeasurement(self, g2Values, totalStarts, totalStops):
        """
        Captures the current g² measurement from the worker thread and updates the plot and labels.

        This function stores the g² values, updates the main curve in the plot, 
        and refreshes the total START and STOP counts displayed in the UI.

        :param g2Values: List of g² values from the measurement (list).
        :param totalStarts: Total counts detected on the START channel (int).
        :param totalStops: Total counts detected on the STOP channel (int).
        :return: None
        """
        self.g2Values=g2Values
        self.curveG2.setData(self.tauValues, self.g2Values)
        self.totalStartsLabel.setText(str(totalStarts))
        self.totalStopsLabel.setText(str(totalStops))
    
    
    def saveG2Data(self):
        """
        Saves the current g² measurement data along with associated fit parameters and channel settings.

        This function opens a dialog for the user to select the desired text format (txt, csv, dat). 
        It checks if the data has already been saved in that format to avoid duplicates. 
        The g² values and tau values are rounded for precision, and any calculated fit parameters 
        for Gaussian, Gaussian Shifted, Lorentzian, Lorentzian Shifted, Antibunching, and 
        Antibunching Shifted models are included in the saved file with their corresponding units.
        The save location and filename are generated based on the current date and a predefined prefix.
        After saving, a message box informs the user of the file path and name or reports an error 
        if the save was unsuccessful.

        :return: None
        """
        dataFolderPrefix=self.savefile.getDataFolderPrefix()
        folder_path=dataFolderPrefix["saveFolder"]
        data_prefix=dataFolderPrefix["g2Prefix"]
        dialog = QDialog(self.mainWindow)
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
            total_condition= conditiontxt or conditiondat or conditioncsv
            if not total_condition:
                current_date=datetime.now()
                current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                fitSetting=f"Initial Date:\t{self.initDate}\nFinish Date:\t{self.finishDate}\n"
                if self.thermalGaussianTcValue!="nan":
                    if self.thermalGaussianTcUnits=="ns":
                        gaussianTcValue=round(self.thermalGaussianTcValue,3)
                    else:
                        gaussianTcValue=round(self.thermalGaussianTcValue,6)
                    fitSetting+=f"Thermal gaussian fit:\tT_c: {gaussianTcValue} {self.thermalGaussianTcUnits} \n"
                else:
                    fitSetting+=""
                if self.thermalGaussianShiftTcValue!="nan" or self.thermalGaussianShiftTdValue!="nan" or self.thermalGaussianShiftBValue!="nan":
                    if self.thermalGaussianShiftTcUnits=="ns":
                        gaussianTcShift=round(self.thermalGaussianShiftTcValue,3)
                        gaussianTdShift=round(self.thermalGaussianShiftTdValue,3)
                        gaussianBShift=round(self.thermalGaussianShiftBValue,3)
                    else:
                        gaussianTcShift=round(self.thermalGaussianShiftTcValue,6)
                        gaussianTdShift=round(self.thermalGaussianShiftTdValue,6)
                        gaussianBShift=round(self.thermalGaussianShiftBValue,6)
                        
                    fitSetting+=(f"Thermal gaussian shifted fit:\t{self.nameTc}: {gaussianTcShift} {self.thermalGaussianShiftTcUnits}"
                                 f"\t{self.nameTd}: {gaussianTdShift} {self.thermalGaussianShiftTdUnits}"
                                 f"\t{self.nameB}: {gaussianBShift} {self.thermalGaussianShiftBUnits}\n")
                else:
                    fitSetting+=""
                if self.thermalLorentzianT0Value!="nan":
                    if self.thermalLorentzianT0Units=="ns":
                        lorentzianT0=round(self.thermalLorentzianT0Value,3)
                    else:
                        lorentzianT0=round(self.thermalLorentzianT0Value,6)
                    fitSetting+=f"Thermal lorentzian fit:\t{self.nameT0}: {lorentzianT0} {self.thermalLorentzianT0Units}\n"
                else:
                    fitSetting+=""
                if self.thermalLorentzianShiftT0Value!="nan" or self.thermalLorentzianShiftTdValue!="nan" or self.thermalLorentzianShiftBValue!="nan":
                    if self.thermalLorentzianShiftT0Units=="ns":
                        lorentzianT0Shift=round(self.thermalLorentzianShiftT0Value,3)
                        lorentzianTdShift=round(self.thermalLorentzianShiftTdValue,3)
                        lorentzianBShift=round(self.thermalLorentzianShiftBValue,3)
                    else:
                        lorentzianT0Shift=round(self.thermalLorentzianShiftT0Value,6)
                        lorentzianTdShift=round(self.thermalLorentzianShiftTdValue,6)
                        lorentzianBShift=round(self.thermalLorentzianShiftBValue,6)
                    fitSetting+=(f"Thermal lorentzian shifted fit:\t{self.nameT0}: {lorentzianT0Shift} {self.thermalLorentzianShiftT0Units}"
                                 f"\t{self.nameTd}: {lorentzianTdShift} {self.thermalLorentzianShiftTdUnits}"
                                 f"\t{self.nameB}: {lorentzianBShift} {self.thermalLorentzianShiftBUnits}\n")
                else:
                    fitSetting+=""
                if self.antiBunchingTauAValue!="nan":
                    if self.antiBunchingTauAUnits=="ns":
                        antibunchingTauA=round(self.antiBunchingTauAValue,3)
                    else:
                        antibunchingTauA=round(self.antiBunchingTauAValue,6)
                    fitSetting+=f"Antibunching fit:\t{self.nameTc}: {antibunchingTauA} {self.antiBunchingTauAUnits}\n"
                else:
                    fitSetting+=""
                if self.antiBunchingShiftTauAValue!="nan" and self.antiBunchingShiftTaudValue!="nan" and self.antiBunchingShiftBValue!="nan":
                    if self.antiBunchingShiftTauAUnits=="ns":
                        antibunchingShiftTauA=round(self.antiBunchingShiftTauAValue,3)
                        antibunchingShiftTaud=round(self.antiBunchingShiftTaudValue,3)
                        antibunchingShiftB=round(self.antiBunchingShiftBValue,3)
                    else:
                        antibunchingShiftTauA=round(self.antiBunchingShiftTauAValue,6)
                        antibunchingShiftTaud=round(self.antiBunchingShiftTaudValue,6)
                        antibunchingShiftB=round(self.antiBunchingShiftBValue,6)
                    fitSetting+=(f"Antibunching shifted fit:\t{self.nameTc}: {antibunchingShiftTauA} {self.antiBunchingShiftTauAUnits}"
                                 f"\t{self.nameTd}: {antibunchingShiftTaud} {self.antiBunchingShiftTaudUnits}"
                                 f"\t{self.nameB}: {antibunchingShiftB} {self.antiBunchingShiftBUnits}\n")
                else:
                    fitSetting+=""
                #Channel Setting
                fitSetting+=f"Stop Channel:\t{self.stopChannelSave}"
                #Put the settings and fit
                filename=data_prefix+current_date_str
                #Round the values in order to get a better txt files
                roundedTauValues=[]
                roundedg2Values=[]
                for i in self.tauValues:
                    newValue=round(i,6)
                    roundedTauValues.append(newValue)
                for i in self.g2Values:
                    newValue=round(i,6)
                    roundedg2Values.append(newValue)
                data=[roundedTauValues,roundedg2Values ]
                timeLabel=f"Tau ({self.unitsMeasured})"
                try:
                    self.savefile.save_g2Hbt_data(data,filename,folder_path,fitSetting,selected_format, timeLabel)
                    if selected_format=="txt":
                        self.oldtxtName=filename
                        self.sentinelsavetxt=1
                    elif selected_format=="csv":
                        self.oldcsvName=filename
                        self.sentinelsavecsv=1
                    elif selected_format=="dat":
                        self.olddatName=filename
                        self.sentinelsavedat=1
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Information)
                    if selected_format=="txt":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldtxtName+".txt"
                    elif selected_format=="csv":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldcsvName+".csv"
                    elif selected_format=="dat":
                        textRoute="The files have been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.olddatName+".dat"
                    message_box.setText(textRoute)
                    message_box.setWindowTitle("Successful save")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()   
                except NameError as e:
                    print(e)
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()         
            else:
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Information)
                if selected_format=="txt":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldtxtName+".txt"
                elif selected_format=="csv":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.oldcsvName+".csv"
                elif selected_format=="dat":
                    textRoute="The files have already been saved in path folder: \n"+folder_path+"\n"+"with the name: \n"+self.olddatName+".dat"
                message_box.setText(textRoute)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
        
    def createGraphicToSave(self):
        """
        Creates a copy of the current g² plot for saving purposes without affecting the on-screen graph.

        This function generates a new GraphicsLayoutWidget, copies the curves, labels, and legend 
        from the main plot, and optionally adds a footer showing the current fit equation and parameters.
        The returned widget can be resized or modified independently of the main plot for saving.

        :return: tuple containing
            - saveWinG2 (GraphicsLayoutWidget): The copied plot widget ready for saving.
            - savePlotG2 (PlotItem): The main plot area within the copied widget.
        """
        saveWinG2 = pg.GraphicsLayoutWidget()
        saveWinG2.setBackground('w')
        savePlotG2 = saveWinG2.addPlot()
        savePlotG2.showGrid(x=True, y=True)
        
        # Old Labels
        leftCurrentLabel = self.plotG2.getAxis("left").labelText
        bottomCurrentLabel = self.plotG2.getAxis("bottom").labelText
        savePlotG2.setLabel('left', leftCurrentLabel)
        savePlotG2.setLabel('bottom', bottomCurrentLabel)
        
        # Legend
        saveLegend = pg.LegendItem(offset=(0, 0))
        saveLegend.setParentItem(savePlotG2.getViewBox())
        saveLegend.anchor((1, 0), (1, 0))
        
        # Curves
        saveCurveG2 = savePlotG2.plot(pen='b', name='g2 Data')
        saveCurveFit = savePlotG2.plot(pen='r', name='g2 fit')
        saveLegend.addItem(saveCurveG2, 'g2 Data')
        saveLegend.addItem(saveCurveFit, 'g2 fit')
        
        # Set data
        saveCurveG2.setData(self.tauValues, self.g2Values)
        
        if self.comboBoxEquation.currentIndex() == 0:
            if len(self.g2FitGaussian) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitGaussian)
        elif self.comboBoxEquation.currentIndex() == 1:
            if len(self.g2FitGaussianShift) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitGaussianShift)
        elif self.comboBoxEquation.currentIndex() == 2:
            if len(self.g2FitLorentzian) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitLorentzian)
        elif self.comboBoxEquation.currentIndex() == 3:
            if len(self.g2FitLorentzianShift) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitLorentzianShift)
        elif self.comboBoxEquation.currentIndex() == 4:
            if len(self.g2FitAntibunching) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitAntibunching)
        elif self.comboBoxEquation.currentIndex() == 5:
            if len(self.g2FitAntibunchingShift) > 0:
                saveCurveFit.setData(self.tauValues, self.g2FitAntibunchingShift)
        
        # Equation label
        equationLabel = ""
        if self.comboBoxEquation.currentIndex() == 0:
            if self.thermalGaussianTcValue != "nan":
                equationLabel = f"Thermal gaussian 1+e^(-pi*({self.nameTau}/T_c)^2): {self.nameTc} = {self.formatValue(self.thermalGaussianTcValue)}"
        elif self.comboBoxEquation.currentIndex() == 1:
            if (self.thermalGaussianShiftTcValue != "nan" or 
                self.thermalGaussianShiftTdValue != "nan" or 
                self.thermalGaussianShiftBValue != "nan"):
                equationLabel = (f"Thermal gaussian shifted 1+e^(-pi*(|{self.nameTau}-T_d|/T_c)^2)+b: {self.nameTc} = {self.formatValue(self.thermalGaussianTcValue)} "
                            f",  {self.nameTd} = {self.formatValue(self.thermalGaussianShiftTdValue)} "
                            f",  {self.nameB} = {self.formatValue(self.thermalGaussianShiftBValue)}")
        elif self.comboBoxEquation.currentIndex() == 2:
            if self.thermalLorentzianT0Value != "nan":
                equationLabel = f"Thermal Lorentzian 1+e^(-2*(|{self.nameTau}|/T_0)): {self.nameT0} = {self.formatValue(self.thermalLorentzianT0Value)}"
        elif self.comboBoxEquation.currentIndex() == 3:
            if (self.thermalLorentzianShiftT0Value != "nan" or 
                self.thermalLorentzianShiftTdValue != "nan" or 
                self.thermalLorentzianShiftBValue != "nan"):
                equationLabel = (f"Thermal Shifted 1+e^(-2*(|{self.nameTau}-T_d|/T_0))+b: {self.nameT0} = {self.formatValue(self.thermalLorentzianShiftT0Value)} "
                            f",  {self.nameTd} = {self.formatValue(self.thermalLorentzianShiftTdValue)} "
                            f",  {self.nameB} = {self.formatValue(self.thermalLorentzianShiftBValue)}")
        elif self.comboBoxEquation.currentIndex() == 4:
            if self.antiBunchingTauAValue != "nan":
                equationLabel = f"Antibunching 1-e^(-({self.nameTau}/T_c)): {self.nameTc} = {self.formatValue(self.antiBunchingTauAValue)}"
        elif self.comboBoxEquation.currentIndex() == 5:
            if (self.antiBunchingShiftTauAValue != "nan" or 
                self.antiBunchingShiftTaudValue != "nan" or 
                self.antiBunchingShiftBValue != "nan"):
                equationLabel = (f"Antibunching Shifted 1-e^(-(|{self.nameTau}-T_d|/T_c)+b): {self.nameTc} = {self.formatValue(self.antiBunchingShiftTauAValue)} "
                            f",  {self.nameTd} = {self.formatValue(self.antiBunchingShiftTaudValue)} "
                            f",  {self.nameB} = {self.formatValue(self.antiBunchingShiftBValue)}")
    
        if equationLabel.strip():
            footer = pg.LabelItem(text=equationLabel, justify='left')
            saveWinG2.addItem(footer, row=2, col=0)
            saveWinG2.ci.layout.setRowStretchFactor(0, 1)   
            saveWinG2.ci.layout.setRowStretchFactor(2, 0)   
        
        return saveWinG2, savePlotG2
    
    
    def saveG2Plot(self):
        """
        Saves the graph image in the specified format (PNG, TIFF, or JPG) based on the user's selection.
        :return: None
        """
        try:
            dataFolderPrefix=self.savefile.getDataFolderPrefix()
            folder_path=dataFolderPrefix["saveFolder"]
            data_prefix=dataFolderPrefix["g2Prefix"]
            dialog =QDialog(self.mainWindow)    
            dialog.setObjectName("ImageFormat")
            dialog.resize(285,105)
            dialog.setWindowTitle("Save Plots")
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
            accepButton.clicked.connect(dialog.accept)
            if dialog.exec_()==QDialog.Accepted:
                selected_format=FormatBox.currentText()
                saveWinG2, savePlotG2=self.createGraphicToSave()
                xRange, yRange = self.plotG2.viewRange()
                savePlotG2.setXRange(xRange[0],xRange[1])
                savePlotG2.setYRange(yRange[0],yRange[1])
                savePlotG2.getAxis('left').setWidth(80)
                savePlotG2.setAspectLocked(False)
                QApplication.processEvents()
                exporter=pg.exporters.ImageExporter(saveWinG2.scene())
                exporter.parameters()['width'] = 1400
                exporter.parameters()['height'] = 800
                currentDate = datetime.now()
                currentDateStr = currentDate.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                graphName= data_prefix+currentDateStr
                outputPath=os.path.join(folder_path,f"{graphName}.{selected_format}")
                exporter.export(outputPath)
                initial_text="The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+ "with the following names:"
                text_route="\n"+graphName+"."+selected_format
                message_box = QMessageBox(self.mainWindow)
                message_box.setIcon(QMessageBox.Information)
                message_box.setText(initial_text+text_route)
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()            
        except:
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
    
    
        
    
    
        
    
    
                

            
    
        
        
    
    
        
    
    
    
    
    
    
        
        
