from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QEvent
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox, QTabWidget, QCheckBox, QWidget, QSizePolicy,QApplication, QWhatsThis
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum
from Utils.createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
import math
import re
from Threads.ThreadLifeTime import WorkerThreadLifeTime
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
from PySide2.QtCore import QThread, Signal, Slot
from numpy import mean, sqrt, std
from datetime import datetime
import pyTempico as tempico
import time
import threading
import os
import numpy as np
class G2Logic():
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
        #self.externalDelaySpinBox.valueChanged.connect(self.changeExternalDelay)
        self.initialConfigs()
        self.createGraphic()
    
    
    def initialConfigs(self):
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
        self.nameTc="T_c"
        self.nameR2="R^2"
        self.nameTd="T_d"
        self.nameB="b"
        self.nameT0="T_0"
    
    def connectedDevice(self, device):
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.device=device
        self.startManualButton.setEnabled(True)
    
    def disconnectedDevice(self):
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        self.startManualButton.setEnabled(False)
    
    def resetSaveSentinels(self):
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
    
    def createGraphic(self):
        self.graphicLayout = QHBoxLayout(self.graphicFrame)
        self.winG2 = pg.GraphicsLayoutWidget()
        self.winG2.setBackground('w')
        self.plotG2 = self.winG2.addPlot()
        self.plotG2.showGrid(x=True, y=True)
        self.plotG2.setLabel('left', 'g2(tau)')
        self.plotG2.setLabel('bottom', 'Tau')
        self.legend = pg.LegendItem(offset=(0, 0))
        self.legend.setParentItem(self.plotG2.getViewBox())
        self.legend.anchor((1, 0), (1, 0))
        self.graphicLayout.addWidget(self.winG2)
        self.curveG2 = self.plotG2.plot(pen='b', name='g2 Data')
        self.curveFit = self.plotG2.plot(pen='r', name='g2 fit')
        self.legend.addItem(self.curveG2, 'g2 Data')
        self.legend.addItem(self.curveFit, 'g2 fit')
    
    
    
    
    
    def setVerticalLabel(self):
        if self.stopChannelComboBox.currentIndex()==0:
            self.plotG2.setLabel('left','g2(tau) Start-A')
        elif self.stopChannelComboBox.currentIndex()==1:
            self.plotG2.setLabel('left','g2(tau) Start-B')
        elif self.stopChannelComboBox.currentIndex()==2:
            self.plotG2.setLabel('left','g2(tau) Start-C')
        elif self.stopChannelComboBox.currentIndex()==3:
            self.plotG2.setLabel('left','g2(tau) Start-D')
    
    
    def startTimerConnection(self):
        self.connectedTimer.start(500)

    
    def stopTimerConnection(self):
        self.connectedTimer.stop()
    
    def initialParameters(self):
        self.initialExternalDelayCheckbox()
        self.initialParametersGaussian()
        self.initialParametesGaussianShifted()
        self.initalParametersLorentzian()
        self.initialParametersLorentzianShifted()
        self.initalParametersAntiBunching()
        self.initalParametersAntiBunchingShifted()
    
    def initialExternalDelayCheckbox(self):
        self.externalDelayGaussianCheckBox=False
        self.externalDelayLorentzianCheckBox=False
        self.externalDelayAntiBunchingCheckBox=False
        
    def initialParametersGaussian(self):
        self.thermalGaussianTcInitial=1
        
    
    def initialParametesGaussianShifted(self):
        self.thermalGaussianShiftTcInitial=1
        self.thermalGaussianShiftTdInitial=0
        self.thermalGaussianShiftBInitial=0
    
    def initalParametersLorentzian(self):
        self.thermalLorentzianT0Initial=1
    
    def initialParametersLorentzianShifted(self):
        self.thermalLorentzianShiftT0Initial=1
        self.thermalLorentzianShiftTdInitial=0
        self.thermalLorentzianShiftBInitial=0
    
    def initalParametersAntiBunching(self):
        self.antiBunchingTauAInitial=1
        
    
    def initalParametersAntiBunchingShifted(self):
        self.antiBunchingShiftTauAInitial=1
        self.antiBunchingShiftTaudInitial=0
        self.antiBunchingShiftBInitial=0
    
    def updateLocalDialogInitalParameters(self):
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

        selection = comboBox.currentText()
        fields = []
        if selection == "Thermal gaussian":
            fields = [self.nameTc]
            values=[self.localInitialGaussianTc]
            self.lastSelection="Thermal gaussian"
        elif selection == "Thermal gaussian shifted":
            fields = [self.nameTc, self.nameTd, self.nameB]
            values=[self.localInitialGaussianTc,self.localInitialGaussianShiftedTd,self.localInitialGaussianShiftedB]
            self.lastSelection="Thermal gaussian shifted"
        elif selection == "Thermal lorentzian":
            fields = [self.nameT0]
            values=[self.localInitialLorentzianT0]
            self.lastSelection="Thermal lorentzian"
        elif selection == "Thermal lorentzian shifted":
            fields = [self.nameT0, self.nameTd, self.nameB]
            values=[self.localInitialLorentzianT0,self.localInitialGaussianShiftedTd,self.localInitialGaussianShiftedB]
            self.lastSelection="Thermal lorentzian shifted"
        elif selection == "Antibunching":
            fields = [self.nameTc]
            values=[self.localInitialGaussianTc]
            self.lastSelection="Antibunching"
        elif selection == "Antibunching shifted":
            fields = [self.nameTc, self.nameTd, self.nameB]
            values=[self.localInitialGaussianTc,self.localInitialGaussianShiftedTd,self.localInitialGaussianShiftedB]
            self.lastSelection="Antibunching shifted"

        fieldWidgets.clear()
        self.currentValues=values
        self.currentSpinBox=[]
        
        for k in range(len(fields)):
            f=fields[k]
            currentValue=values[k]
            if self.nameTd in f: 
                checkLayout = QHBoxLayout()
                checkLayout.setSpacing(5)
                label_checkbox = QLabel("Fixed delay:")
                checkLayout.addWidget(label_checkbox)
                checkbox = QCheckBox()
                if selection=="Thermal gaussian shifted":
                    checkbox.setChecked(self.localFixedGaussian)
                elif selection=="Thermal lorentzian shifted":
                    checkbox.setChecked(self.localFixedGaussian)
                elif selection=="Antibunching shifted":
                    checkbox.setChecked(self.localFixedGaussian)
                self.currentFixedChebox=checkbox
                checkLayout.addWidget(checkbox)
                fieldLayout.addLayout(checkLayout)

            hLayout = QHBoxLayout()
            hLayout.setSpacing(5)
            label = QLabel(f)
            hLayout.addWidget(label)
            spin = QDoubleSpinBox()
            if not self.nameB in f:
                spin.setSuffix(" ns")
                spin.setDecimals(3)
                spin.setSingleStep(1)
                spin.setMaximum(9999999999999999464902769475481793196872414789632.000000000000000)
                spin.setMinimum(-9999999999999999464902769475481793196872414789632.000000000000000)
                spin.valueChanged.connect(lambda value, spinbox=spin: self.updateSpinBoxSufix(spinbox,value))
            else:
                spin.setMaximum(9999999999999999464902769475481793196872414789632.000000000000000)
                spin.setMinimum(0)
                spin.setDecimals(3)
                spin.setSingleStep(1)
            self.currentSpinBox.append(spin)
            spin.setValue(currentValue)
            hLayout.addWidget(spin)

            if self.nameTd in f:
                fieldWidgets.append((f, spin, checkbox))
            else:
                fieldWidgets.append((f, spin))

            fieldLayout.addLayout(hLayout)
        dialog.layout().activate()
        dialog.adjustSize()
    
    def changeExternalCheckBox(self):
        if self.comboBoxEquation.currentIndex()==1:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
        elif self.comboBoxEquation.currentIndex()==3:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
        elif self.comboBoxEquation.currentIndex()==5:
            self.fixedDelayCheckBox.setChecked(self.externalDelayGaussianCheckBox)
    
    def changeExternalFixed(self):
        if self.comboBoxEquation.currentIndex()==1:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
        elif self.comboBoxEquation.currentIndex()==3:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
        elif self.comboBoxEquation.currentIndex()==5:
            self.externalDelayGaussianCheckBox=self.fixedDelayCheckBox.isChecked()
    
    
    def changeExternalSpinBox(self):
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
            print(self.thermalLorentzianShiftTdInitial)
            if abs(self.thermalGaussianShiftTdInitial)<1000:
                print("Entra aca")
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
        cancelBtn.clicked.connect(self.dialogParameters.reject)
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
        currentIndexDialog=self.comboBoxDialog.currentIndex()
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
        self.dialogParameters.accept()
    
    def updateSpinBoxSufix(self, spinbox, value):
        
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
        self.thermalGaussianTcValue="nan"
        self.thermalGaussianTcStd="nan"
        self.thermalGaussianTcUnits=""
        self.thermalGaussianR2="nan"
    
    def initParametersEquationThermalGaussianShift(self):
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
        self.thermalLorentzianT0Value="nan"
        self.thermalLorentzianT0Std="nan"
        self.thermalLorentzianT0Units=""
        self.thermalLorentzianR2="nan"
    
    def initParametersEquationThermalLorentzianShift(self):
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
        self.antiBunchingTauAValue="nan"
        self.antiBunchingTauAStd="nan"
        self.antiBunchingTauAUnits=""
        self.antiBunchingR2="nan"
    
    def initParametersEquationAntiBunchingShift(self):
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
        if value == 0:
            return "0.00"
        abs_val = abs(value)
        if 0.01 <= abs_val < 1e6:
            return f"{value:.2f}"
        else:
            return f"{value:.2e}"
    
    
    def formatStd(self,valueVar,valueEstimated):
        print("Varianza")
        print(valueVar)
        print("Valor estimado")
        print(valueEstimated)
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
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-np.pi*((t/T_c)**2))

    def thermalGaussianShift(self,t,T_c,T_d,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        T_c=float(T_c)
        T_d=float(T_d)
        b=float(b)
        return 1+exp(-np.pi*((np.abs(t-T_d)/T_c)**2))+b
    
    def thermalGaussianShiftFixed(self,t,T_c,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.thermalGaussianShiftTdInitial
        else:
            T_d = self.thermalGaussianShiftTdInitial / 1000
        return 1+exp(-np.pi*((np.abs(t-T_d)/T_c)**2))+b
    
    def thermalLorentzian(self,t,T_0):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-2*(np.abs(t)/T_0))
    
    def thermalLorentzianShift(self,t,T_0,T_d,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-2*(np.abs(t-T_d)/T_0))+b
    
    def thermalLorentzianShiftFixed(self,t,T_0,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.thermalLorentzianShiftTdInitial
        else:
            T_d = self.thermalLorentzianShiftTdInitial / 1000
        return 1+exp(-2*(np.abs(t-T_d)/T_0))+b
    
    def antiBunching(self,t,T_c):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-1*((t/T_c)))
    
    def antiBunchingShift(self,t,T_c,T_d,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        return 1+exp(-1*((np.abs(t-T_d)/T_c)))+b
    
    def antiBunchingShiftFixed(self,t,T_c,b):
        t = np.array(t) if not isinstance(t, np.ndarray) else t
        if self.unitsMeasured == "ns":
            T_d = self.antiBunchingShiftTaudInitial
        else:
            T_d = self.antiBunchingShiftTaudInitial / 1000
        return 1+exp(-1*((np.abs(t-T_d)/T_c)))+b
    
    def applyFitAction(self):
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
                    stdList=[pcov[0,0],-1,pcov[1,1]]
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
                        print("Entra en el condicional del lorentzian")
                        p0=[self.thermalLorentzianT0Initial,self.thermalGaussianShiftBInitial]
                else:
                    if not self.externalDelayGaussianCheckBox:
                        p0=[self.thermalLorentzianT0Initial/1000,self.thermalGaussianShiftTdInitial/1000,self.thermalGaussianShiftBInitial]
                    else:
                        p0=[self.thermalLorentzianT0Initial/1000,self.thermalGaussianShiftBInitial]
                
                if self.externalDelayGaussianCheckBox:
                    print(p0)
                    popt, pcov= curve_fit(self.thermalLorentzianShiftFixed, self.tauValues, self.g2Values,p0)
                    if self.unitsMeasured=="ns":
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital, popt[1]]
                    else:
                        tauDInital=self.thermalGaussianShiftTdInitial
                        parametersList=[popt[0],tauDInital/1000, popt[1]]
                    stdList=[pcov[0,0],-1,pcov[1,1]]
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
                    stdList=[pcov[0,0],-1,pcov[1,1]]
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
        
    
    def calculateR2(self,data,fitData):
        arrayData=array(data)
        arrayFit=array(fitData)
        meanData=mean(arrayData)
        ssRes=sum((arrayData-arrayFit)**2)
        ssTot=sum((arrayData-meanData)**2)
        R2=1-(ssRes/ssTot)
        print("El valor de r2 es")
        print(R2)
        return round(R2,2)
    
    def showDialogNoFitParameters(self):
        QMessageBox.warning(
            self.mainWindow,
            "Fit Parameters Not Estimated",
            "The fit parameters could not be estimated for the current data.\n"
            "Please verify that the data is sufficient and properly distributed."
        )
    
    
    #Manual measurement 
    def startManualMeasurement(self):
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
        self.worker.start()
    
    def checkRangesMode(self,channel, maximumTime):
        modeChannelSelected=int(self.device.getMode(channel))
        if modeChannelSelected==1 and maximumTime>500000:
            self.modeToMeasure=2
        elif modeChannelSelected==2 and maximumTime<125000:
            self.modeToMeasure=1
        else:
            self.modeToMeasure=modeChannelSelected
    
    def getUnits(self):
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
        self.worker.stop()
        self.stopManualButton.setEnabled(False)
        
    def getPicoSecondsValue(self, valueStr):
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
        self.worker.clearG2()
        
     
    #By size measurement
    def startLimitedMeasurement(self):
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
        self.worker.start()
        
    
    def stopLimitedMeasurement(self):
        self.worker.stop()
        self.stopLimitedButtonG2.setEnabled(False)
    
    def stopAutoClearMeasurement(self):
        self.worker.stop()
        self.autoClearTimer.stop()
        self.stopAutoClearButton.setEnabled(False)
        
    
    #Auto clear measurement
    def startAutoClearMeasurement(self):
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
        self.worker.start()
    
    def generalSettingsBeforeMeasurement(self, tab):
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
        if not self.determinedParameters:
            self.showDialogNoParameters()
        self.startTimerConnection()
        if self.tauValues:
            self.applyFitButton.setEnabled(True)
            self.initialParametersButton.setEnabled(True)
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
        self.generalSettingsAfterMeasurement(0)
        self.stopManualButton.setEnabled(False)
        self.startManualButton.setEnabled(True)
        self.clearButton.setEnabled(False)
        
        
    
    def finishLimitedMeasurement(self):
        self.generalSettingsAfterMeasurement(1)
        self.stopLimitedButtonG2.setEnabled(False)
        self.startLimitedButtonG2.setEnabled(True)
        self.clearLimitedButtonG2.setEnabled(False)
        self.numberMeasurementsSpinBox.setEnabled(True)
    
    
    def finishAutoClearMeasurement(self):
        self.generalSettingsAfterMeasurement(2)
        self.stopAutoClearButton.setEnabled(False)
        self.startAutoClearButton.setEnabled(True)
        self.clearAutoClearButton.setEnabled(False)
        self.autoClearSpinBox.setEnabled(True)
        
    
    
    def showDialogNoParameters(self):
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
        
        
    
    def getChannelComboBox(self):
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
        self.calculatedParameter.setText(text)
    
    def changeEstimatedParameterStartTimer(self,text):
        self.calculatedParameter.setText(text)
        everyValue=self.autoClearSpinBox.value()
        self.autoClearTimer.start(everyValue*1000)
        
    def changeDeterminedParameters(self):
        self.determinedParameters=True
    
    
        
        
    
    def captureTauValues(self, tauValues, unitFactor, mode):
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
                    
        
        
    
    
    
    def captureMeasurement(self, g2Values, totalStarts, totalStops):
        self.g2Values=g2Values
        self.curveG2.setData(self.tauValues, self.g2Values)
        self.totalStartsLabel.setText(str(totalStarts))
        self.totalStopsLabel.setText(str(totalStops))
    
    
    def saveG2Data(self):
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
                    fitSetting+=f"Thermal gaussian fit:\tT_c: {self.thermalGaussianTcValue} {self.thermalGaussianTcUnits} \n"
                else:
                    fitSetting+=""
                if self.thermalGaussianShiftTcValue!="nan" or self.thermalGaussianShiftTdValue!="nan" or self.thermalGaussianShiftBValue!="nan":
                    fitSetting+=(f"Thermal gaussian shifted fit:\tT_c: {self.thermalGaussianShiftTcValue} {self.thermalGaussianShiftTcUnits}"
                                 f"\tT_d: {self.thermalGaussianShiftTdValue} {self.thermalGaussianShiftTdUnits}"
                                 f"\tB: {self.thermalGaussianShiftBValue} {self.thermalGaussianShiftBUnits}\n")
                else:
                    fitSetting+=""
                if self.thermalLorentzianT0Value!="nan":
                    fitSetting+=f"Thermal lorentzian fit:\tT_0: {self.thermalLorentzianT0Value} {self.thermalLorentzianT0Units}\n"
                else:
                    fitSetting+=""
                if self.thermalLorentzianShiftT0Value!="nan" or self.thermalLorentzianShiftTdValue!="nan" or self.thermalLorentzianShiftBValue!="nan":
                    fitSetting+=(f"Thermal lorentzian shifted fit:\tT_0: {self.thermalLorentzianShiftT0Value} {self.thermalLorentzianShiftT0Units}"
                                 f"\tT_d: {self.thermalLorentzianShiftTdValue} {self.thermalLorentzianShiftTdUnits}"
                                 f"\tB: {self.thermalLorentzianShiftBValue} {self.thermalLorentzianShiftBUnits}\n")
                else:
                    fitSetting+=""
                if self.antiBunchingTauAValue!="nan":
                    fitSetting+=f"Antibunching fit:\tT_A: {self.antiBunchingTauAValue} {self.antiBunchingTauAUnits}\n"
                else:
                    fitSetting+=""
                if self.antiBunchingShiftTauAValue!="nan" and self.antiBunchingShiftTaudValue!="nan" and self.antiBunchingShiftBValue!="nan":
                    fitSetting+=(f"Antibunching shifted fit:\tT_A: {self.antiBunchingShiftTauAValue} {self.antiBunchingShiftTauAUnits}"
                                 f"\tT_d: {self.antiBunchingShiftTaudValue} {self.antiBunchingShiftTaudUnits}"
                                 f"\tB: {self.antiBunchingShiftBValue} {self.antiBunchingShiftBUnits}\n")
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
                equationLabel = f"Thermal gaussian 1+e^(-pi*(T/T_c)^2): {self.nameTc} = {self.formatValue(self.thermalGaussianTcValue)}"
                print("Entra aca")
        elif self.comboBoxEquation.currentIndex() == 1:
            if (self.thermalGaussianShiftTcValue != "nan" or 
                self.thermalGaussianShiftTdValue != "nan" or 
                self.thermalGaussianShiftBValue != "nan"):
                equationLabel = (f"Thermal gaussian shifted 1+e^(-pi*(|T-T_d|/T_c)^2)+b: {self.nameTc} = {self.formatValue(self.thermalGaussianTcValue)} "
                            f"  ,{self.nameTd} = {self.formatValue(self.thermalGaussianShiftTdValue)} "
                            f"  ,{self.nameB} = {self.formatValue(self.thermalGaussianShiftBValue)}")
        elif self.comboBoxEquation.currentIndex() == 2:
            if self.thermalLorentzianT0Value != "nan":
                equationLabel = f"Thermal Lorentzian 1+e^(-2*(|T|/T_0)): {self.nameT0} = {self.formatValue(self.thermalLorentzianT0Value)}"
        elif self.comboBoxEquation.currentIndex() == 3:
            if (self.thermalLorentzianShiftT0Value != "nan" or 
                self.thermalLorentzianShiftTdValue != "nan" or 
                self.thermalLorentzianShiftBValue != "nan"):
                equationLabel = (f"Thermal Shifted 1+e^(-2*(|T-T_d|/T_0))+b: {self.nameT0} = {self.formatValue(self.thermalLorentzianShiftT0Value)} "
                            f"  ,{self.nameTd} = {self.formatValue(self.thermalLorentzianShiftTdValue)} "
                            f"  ,{self.nameB} = {self.formatValue(self.thermalLorentzianShiftBValue)}")
        elif self.comboBoxEquation.currentIndex() == 4:
            if self.antiBunchingTauAValue != "nan":
                equationLabel = f"Antibunching 1-e^(-(T/T_c)): {self.nameTc} = {self.formatValue(self.antiBunchingTauAValue)}"
        elif self.comboBoxEquation.currentIndex() == 5:
            if (self.antiBunchingShiftTauAValue != "nan" or 
                self.antiBunchingShiftTaudValue != "nan" or 
                self.antiBunchingShiftBValue != "nan"):
                equationLabel = (f"Antibunching Shifted 1-e^(-(|T-T_d|/T_c)+b): {self.nameTc} = {self.formatValue(self.antiBunchingShiftTauAValue)} "
                            f"  ,{self.nameTd} = {self.formatValue(self.antiBunchingShiftTaudValue)} "
                            f"  ,{self.nameB} = {self.formatValue(self.antiBunchingShiftBValue)}")
    
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
    
    
        
    
    
        
    
    
                
class WorkerThreadG2(QThread):
    updateMeasurement=Signal(list, int, int)
    updateTauValues=Signal(list,int,int)
    updateStatusLabel=Signal(str)
    updateColorLabel=Signal(int)
    updateEstimatedParameter=Signal(str)
    updateDeterminedParameters=Signal()
    updateFirstParameter=Signal(str)
    def __init__(self, stopChannel: str, maximumTime: float, numberBins:int, coincidenceWindow: float, device: tempico.TempicoDevice, 
                 mode,units,limitedMeasurement=False,numberOfMeasurements=0,autoclearMeasure=False):
        super().__init__()
        self.totalStarts=0
        self.totalStops=0
        self.running=True
        self.stopChannel=stopChannel
        self.maximumTime=maximumTime
        self.maximumTimeSeconds=self.psToS(maximumTime)
        self.modeSettings=mode
        self.units=units
        self.cumulatedEstimatedParameter=0
        self.totalEstimatedParameter=0
        self.numberBins=numberBins
        self.coincidenceWindow=self.psToS(coincidenceWindow)
        self.isLimitedMeasurement=limitedMeasurement
        self.numberMeasurements=numberOfMeasurements
        self.autoclearMeasure=autoclearMeasure
        self.device=device
        self.totalTimeIntegration=0
        self.bins=self.generateBinList()
        self.divisionFactor=self.getDivisionFactor()
        self.TauValues = (0.5 * (self.bins[:-1] + self.bins[1:])/self.divisionFactor)
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.baseg2Histogram=np.array(np.zeros(len(self.TauValues)))
        print(self.baseg2Histogram)
        self.saveSettings()
        self.settingsForEstimate()
        
    
    def run(self):
        self.estimatedParameter=self.estimatedParameterValue()
        if self.estimatedParameter==-1 and self.running:
            print("Cannot estimated due to low number of values")
        elif self.estimatedParameter!=-1 and self.running:
            self.cumulatedEstimatedParameter+=self.estimatedParameter
            self.totalEstimatedParameter+=1
            if not self.autoclearMeasure:
                self.updateEstimatedParameter.emit(str(int(self.estimatedParameter)))
            else:
                self.updateFirstParameter.emit(str(int(self.estimatedParameter)))
            self.updateDeterminedParameters.emit()
            self.updateTauValues.emit(self.TauValues,self.divisionFactor,self.modeSettings)
        self.settingsForMeasurement()
        self.updateStatusLabel.emit("Running measurement")
        self.updateColorLabel.emit(1)
        while self.running:
            self.getMeasurement()
        self.recoverSettings()
    
    def getDivisionFactor(self):
        factor=1
        if self.units=="ns":
            factor=10**3
        elif self.units=="us":
            factor=10**6
        elif self.units=="ms":
            factor=10**9
        return factor
            
    
    def settingsForEstimate(self):
        self.device.setNumberOfRuns(1)
        self.device.disableChannel(1)
        self.device.disableChannel(2)
        self.device.disableChannel(3)
        self.device.disableChannel(4)
        if self.stopChannel=="A":
            self.device.enableChannel(1)
            self.device.setAverageCycles(1,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(1,2)
        elif self.stopChannel=="B":
            self.device.enableChannel(2)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(2,2)
        elif self.stopChannel=="C":
            self.device.enableChannel(3)
            self.device.setAverageCycles(3,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(3,2)
        elif self.stopChannel=="D":
            self.device.enableChannel(4)
            self.device.setAverageCycles(2,1)
            self.device.setStopMask(1,0)
            self.device.setMode(1,self.modeSettings)
            self.device.setNumberOfStops(4,2)
    
    def settingsForMeasurement(self):
        self.device.setNumberOfRuns(100)
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,1)
            self.device.setMode(1,self.modeSettings)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,1)
            self.device.setMode(2,self.modeSettings)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,1)
            self.device.setMode(3,self.modeSettings)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,1)
            self.device.setMode(4,self.modeSettings)
    
    def settingsForEstimatedParameters(self):
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,2)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,2)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,2)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,2)
        
        
        
    def saveSettings(self):
        self.numberRunsSaved=self.device.getNumberOfRuns()
        self.numberStopsChannelA=self.device.getNumberOfStops(1)
        self.numberStopsChannelB=self.device.getNumberOfStops(2)
        self.numberStopsChannelC=self.device.getNumberOfStops(3)
        self.numberStopsChannelD=self.device.getNumberOfStops(4)
        self.stopMaskChannelA=self.device.getStopMask(1)
        self.stopMaskChannelB=self.device.getStopMask(2)
        self.stopMaskChannelC=self.device.getStopMask(3)
        self.stopMaskChannelD=self.device.getStopMask(4)
        self.averageCyclesChannelA=self.device.getAverageCycles(1)
        self.averageCyclesChannelB=self.device.getAverageCycles(2)
        self.averageCyclesChannelC=self.device.getAverageCycles(3)
        self.averageCyclesChannelD=self.device.getAverageCycles(4)
        self.modeChannelA=self.device.getMode(1)
        self.modeChannelB=self.device.getMode(2)
        self.modeChannelC=self.device.getMode(3)
        self.modeChannelD=self.device.getMode(4)
    
    def recoverSettings(self):
        self.device.enableChannel(1)
        self.device.enableChannel(2)
        self.device.enableChannel(3)
        self.device.enableChannel(4)
        self.device.setNumberOfRuns(self.numberRunsSaved)
        self.device.setNumberOfStops(1,self.numberStopsChannelA)
        self.device.setNumberOfStops(2,self.numberStopsChannelB)
        self.device.setNumberOfStops(3,self.numberStopsChannelC)
        self.device.setNumberOfStops(4,self.numberStopsChannelD)
        self.device.setStopMask(1,self.stopMaskChannelA)
        self.device.setStopMask(2,self.stopMaskChannelB)
        self.device.setStopMask(3,self.stopMaskChannelC)
        self.device.setStopMask(4,self.stopMaskChannelD)
        self.device.setAverageCycles(1,self.averageCyclesChannelA)
        self.device.setAverageCycles(2,self.averageCyclesChannelB)
        self.device.setAverageCycles(3,self.averageCyclesChannelC)
        self.device.setAverageCycles(4,self.averageCyclesChannelD)
        self.device.setMode(1,self.modeChannelA)
        self.device.setMode(2,self.modeChannelB)
        self.device.setMode(3,self.modeChannelC)
        self.device.setMode(4,self.modeChannelD)
    
    def estimatedParameterValue(self):
        self.settingsForEstimatedParameters()
        notRegisteredMeasurements=0
        percentage=0
        self.updateStatusLabel.emit(f"Taking initial parameters {percentage}%")
        self.updateColorLabel.emit(2)
        estimatedDifferences=[]
        notStartsDetected=0
        for i in range(100):
            if not self.running:
                return -1
            measurement=self.device.measure()
            print(measurement)
            if notStartsDetected>=10:
                self.updateStatusLabel.emit(f"Taking initial parameters 100% (Waiting start 10/10)")
                return -1
            if not measurement:
                notRegisteredMeasurements+=1
                notStartsDetected+=1
                
            else:
                notStartsDetected=0
                if len(measurement[0])==5:
                    stop1=measurement[0][3]
                    stop2=measurement[0][4]
                    differenceEstimated=stop2-stop1
                    estimatedDifferences.append(differenceEstimated)
                else:
                    notRegisteredMeasurements+=1
            percentage=i+1
            if notRegisteredMeasurements>0:
                self.updateStatusLabel.emit(f"Taking initial parameters {percentage}% (Waiting start {notRegisteredMeasurements}/10)")
            else:
                self.updateStatusLabel.emit(f"Taking initial parameters {percentage}%")
                
        self.updateStatusLabel.emit(f"Taking initial parameters 100%")
        if notRegisteredMeasurements>700:
            return -1
        else:
            return self.getCountPerSecondParameter(estimatedDifferences)
    
    
    def getMeasurement(self):
        self.settingsForMeasurement()
        measurement = self.device.measure()
        totalStopPerMeasurement=0
        timeDifferences, stopDifferences = [], []
        notStartsMeasurement=0
        for run in measurement:
            if not run:
                notStartsMeasurement+=1
                continue
            totalStopPerMeasurement+=self.processRun(run, timeDifferences)
            if self.isLimitedMeasurement and self.totalStops>=self.numberMeasurements:
                self.updateDeterminedParameters.emit()
                self.running=False
                break
        stopDifferences=self.estimateParameterInMeasurement()
        if self.totalTimeIntegration>0:
            g2Values=self.buildG2Histogram(timeDifferences)
            self.updateMeasurement.emit(g2Values, self.totalStarts,self.totalStops)
        else:
            self.updateMeasurement.emit(self.g2Histogram, self.totalStarts,self.totalStops)
        if stopDifferences:
            self.cumulatedEstimatedParameter+=self.getCountPerSecondParameter(stopDifferences)
            self.totalEstimatedParameter+=1
            self.estimatedParameter=self.cumulatedEstimatedParameter/self.totalEstimatedParameter
            self.updateEstimatedParameter.emit(str(int(self.estimatedParameter)))
        if len(measurement)==0:
            self.updateStatusLabel.emit(f"No measurements in start channel")
            self.updateColorLabel.emit(3)
        elif notStartsMeasurement>70:
            self.updateStatusLabel.emit(f"No measurements in start channel")
            self.updateColorLabel.emit(3)
        elif totalStopPerMeasurement>70:
            self.updateStatusLabel.emit(f"No measurements in channels {self.stopChannel}")
            self.updateColorLabel.emit(3)
        else:
            self.updateStatusLabel.emit(f"Running measurement")
            self.updateColorLabel.emit(1)
            
    def estimateParameterInMeasurement(self):
        self.settingsForEstimatedParameters()
        estimatedDifferences=[]
        measure=self.device.measure()
        for run in measure:
            if not run:
                continue
            if len(run)==5:
                stop1=run[3]
                stop2=run[4]
                differenceEstimated=stop2-stop1
                estimatedDifferences.append(differenceEstimated)
        return estimatedDifferences
            
            
    
    
    def processRun(self, run, timeDifferences):
        self.totalStarts += 1
        if run[3] == -1:
            return 1
        
        if run[3]<self.maximumTime:
            timeDifferences.append(run[3])
            self.totalStops += 1
        self.totalTimeIntegration += run[3]
        return 0

 
    def getCountPerSecondParameter(self,estimatedDifferences):
        meanDifferences=np.mean(estimatedDifferences)
        estimatedValue= (10**(12))/meanDifferences
        return round(estimatedValue,0)

    
    def buildG2Histogram(self,timeDifferences):
        g2TemporalHistogram,_=np.histogram(timeDifferences, bins=self.bins)
        if len(g2TemporalHistogram)==0:
            g2TemporalHistogram=self.baseg2Histogram
        if len(self.g2Histogram)!=0:
            self.g2Histogram=self.g2Histogram+ g2TemporalHistogram
        else:
            self.g2Histogram=g2TemporalHistogram
        integrationTimeS=self.psToS(self.totalTimeIntegration)
        normalizedParameter=1/((self.estimatedParameter**2)*integrationTimeS*self.coincidenceWindow)
        histogramToEmit=self.g2Histogram*normalizedParameter
        return histogramToEmit
        
        
    def generateBinList(self):
        if self.modeSettings==1:
            histogramToBuild=np.linspace(12500, self.maximumTime, self.numberBins + 1)
        elif self.modeSettings==2:
            histogramToBuild=np.linspace(125000, self.maximumTime, self.numberBins + 1)
        return histogramToBuild
    
    
    def getG2Average(self,g2Histogram):
        valueSum=np.sum(g2Histogram)
        return valueSum/len(g2Histogram)
    
    def sortByStart(self, measurement):
        dataFiltered=[]
        for run in measurement:
            if run:
                dataFiltered.append(run)
        dataFiltered.sort(key=lambda x: x[2])
        return dataFiltered
    
    def changeToOneStop(self):
        if self.stopChannel=="A":
            self.device.setNumberOfStops(1,1)
        elif self.stopChannel=="B":
            self.device.setNumberOfStops(2,1)
        elif self.stopChannel=="C":
            self.device.setNumberOfStops(3,1)
        elif self.stopChannel=="D":
            self.device.setNumberOfStops(4,1)
    
    def psToS(self,picoseconds):
        return picoseconds * 1e-12

    def clearG2(self):
        self.totalTimeIntegration=0
        self.g2Histogram=np.array(np.zeros(len(self.TauValues)))
        self.totalStarts=0
        self.totalStops=0
        self.cumulatedEstimatedParameter=0
        self.totalEstimatedParameter=0
        
    
    def stop(self):
        self.updateDeterminedParameters.emit()
        self.running=False
            
    
        
        
    
    
        
    
    
    
    
    
    
        
        
