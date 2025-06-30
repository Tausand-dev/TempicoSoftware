from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor, QFont
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QCheckBox, QRadioButton,QLabel, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QHeaderView,QAbstractItemView, QApplication, QHBoxLayout
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace, std
from numpy import append as appnd
from createsavefile import createsavefile as savefile
from datetime import datetime, date
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
import time
import random
import threading
from pyqtgraph import mkPen
import os
import numpy as np
class CountEstimatedLogic():
    """
    Class responsible for managing the logic and graphical representation of the Count Estimation window.

    This class handles user interactions and graphical updates related to photon/event count estimations across multiple channels (A, B, C, D). It coordinates the initialization of graphical elements, manages real-time measurements, and provides options for data saving, graphical visualization modes, and uncertainty tracking per channel. The main responsibilities include:
    - Initializing and updating graphical frames for each measurement channel.
    - Starting and stopping the count measurements.
    - Handling user interactions with checkboxes, radio buttons, and combo boxes.
    - Displaying and updating count values and their uncertainties.
    - Managing separate, merged, or detached graphics.
    - Saving count data and graphical plots.
    - Monitoring the device connection and measurement state.

    :param channelACheckBox: Checkbox for enabling/disabling measurements on channel A (QCheckBox).
    :param channelBCheckBox: Checkbox for enabling/disabling measurements on channel B (QCheckBox).
    :param channelCCheckBox: Checkbox for enabling/disabling measurements on channel C (QCheckBox).
    :param channelDCheckBox: Checkbox for enabling/disabling measurements on channel D (QCheckBox).
    :param startButton: Button to start the count measurement (QPushButton).
    :param stopButton: Button to stop the count measurement (QPushButton).
    :param mergeRadio: Radio button to merge all channel plots into one graph (QRadioButton).
    :param separateGraphics: Radio button to display plots separately per channel (QRadioButton).
    :param deatachedGraphics: Radio button to display detached external graphics (QRadioButton).
    :param timeRangeComboBox: Combo box for selecting the time range for plot visualization (QComboBox).
    :param clearButtonChannelA: Button to clear the graph and data of channel A (QPushButton).
    :param clearButtonChannelB: Button to clear the graph and data of channel B (QPushButton).
    :param clearButtonChannelC: Button to clear the graph and data of channel C (QPushButton).
    :param clearButtonChannelD: Button to clear the graph and data of channel D (QPushButton).
    :param saveDataButton: Button to save count data for all channels (QPushButton).
    :param savePlotButton: Button to save the plot images (QPushButton).
    :param countChannelAValue: Label displaying current count value on channel A (QLabel).
    :param countChannelBValue: Label displaying current count value on channel B (QLabel).
    :param countChannelCValue: Label displaying current count value on channel C (QLabel).
    :param countChannelDValue: Label displaying current count value on channel D (QLabel).
    :param countChannelAUncertainty: Label showing uncertainty of channel A (QLabel).
    :param countChannelBUncertainty: Label showing uncertainty of channel B (QLabel).
    :param countChannelCUncertainty: Label showing uncertainty of channel C (QLabel).
    :param countChannelDUncertainty: Label showing uncertainty of channel D (QLabel).
    :param tableCounts: Table displaying count and uncertainty data per measurement cycle (QTableWidget).
    :param graphicsFrame: Frame container for holding the graphical layouts (QFrame).
    :param channelAFrameLabel: Frame label associated with channel A graphics (QFrame).
    :param channelBFrameLabel: Frame label associated with channel B graphics (QFrame).
    :param channelCFrameLabel: Frame label associated with channel C graphics (QFrame).
    :param channelDFrameLabel: Frame label associated with channel D graphics (QFrame).
    :param statusLabel: Label showing the system status (QLabel).
    :param pointStatusLabel: Label showing the status of the current measurement point (QLabel).
    :param deatachedCheckBox: Checkbox to toggle between embedded and detached graphics layout (QCheckBox).
    :param device: The connected measurement device.
    :param parent: The parent window containing the UI (usually a QMainWindow).
    :param timerConnection: Timer responsible for checking device connection status (QTimer).
    :return: None
    """
    def __init__(self,channelACheckBox: QCheckBox, channelBCheckBox: QCheckBox, channelCCheckBox: QCheckBox, channelDCheckBox: QCheckBox,startButton: QPushButton, stopButton: QPushButton,
                 mergeRadio: QRadioButton, separateGraphics: QRadioButton, deatachedGraphics:QRadioButton, timeRangeComboBox: QComboBox, clearButtonChannelA:QPushButton, clearButtonChannelB:QPushButton, clearButtonChannelC:QPushButton, 
                 clearButtonChannelD:QPushButton, saveDataButton: QPushButton, savePlotButton: QPushButton, countChannelAValue: QLabel,countChannelBValue: QLabel,countChannelCValue: QLabel,
                 countChannelDValue: QLabel, countChannelAUncertainty: QLabel, countChannelBUncertainty: QLabel, countChannelCUncertainty: QLabel, countChannelDUncertainty: QLabel,
                 tableCounts:QTableWidget, graphicsFrame: QFrame,channelAFrameLabel: QFrame,channelBFrameLabel: QFrame,channelCFrameLabel: QFrame,channelDFrameLabel: QFrame, statusLabel: QLabel, pointStatusLabel: QLabel, deatachedCheckBox: QCheckBox, detachedLabelCheckBox: QCheckBox, helpButton: QPushButton, device: tempico.TempicoDevice, parent, timerConnection):
        #Get the parameters
        self.savefile=savefile()
        self.channelACheckBox = channelACheckBox
        self.channelCCheckBox = channelBCheckBox
        self.channelBCheckBox = channelCCheckBox
        self.channelDCheckBox = channelDCheckBox
        self.startButton = startButton
        self.stopButton = stopButton
        self.mergeGraphics = mergeRadio
        self.deatachedGraphics = deatachedGraphics
        self.separateGraphics = separateGraphics
        self.timeRangeComboBox = timeRangeComboBox
        self.clearButtonChannelA = clearButtonChannelA
        self.clearButtonChannelB = clearButtonChannelB
        self.clearButtonChannelC = clearButtonChannelC
        self.clearButtonChannelD = clearButtonChannelD
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.countChannelAValue = countChannelAValue
        self.countChannelBValue = countChannelBValue
        self.countChannelCValue = countChannelCValue
        self.countChannelDValue = countChannelDValue
        self.countChannelAUncertainty = countChannelAUncertainty
        self.countChannelBUncertainty = countChannelBUncertainty
        self.countChannelCUncertainty = countChannelCUncertainty
        self.countChannelDUncertainty = countChannelDUncertainty
        self.tableCounts = tableCounts
        self.graphicsFrame= graphicsFrame
        self.device = device
        self.mainWindow = parent
        self.timerConnection=timerConnection
        self.channelAFrameLabel=channelAFrameLabel
        self.channelBFrameLabel=channelBFrameLabel
        self.channelCFrameLabel=channelCFrameLabel
        self.channelDFrameLabel=channelDFrameLabel
        self.statusLabel=statusLabel
        self.pointStatusLabel=pointStatusLabel
        self.deatachedCheckBox= deatachedCheckBox
        self.detachedLabelCheckBox= detachedLabelCheckBox
        self.helpButton=helpButton
        #Init for the buttons
        self.stopButton.setEnabled(False)
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        #Construct the graphics
        self.constructGraphicA()
        self.constructGraphicB()
        self.constructGraphicC()
        self.constructGraphicD()
        #Connection for the checkbox
        self.channelACheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelBCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelCCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.channelDCheckBox.stateChanged.connect(self.checkBoxListenerChannels)
        self.deatachedCheckBox.stateChanged.connect(self.deatachedTable)
        self.detachedLabelCheckBox.stateChanged.connect(self.detachedLabels)
        #Connection for the radio button
        self.separateGraphics.toggled.connect(self.updateGraphicsLayout)
        self.mergeGraphics.toggled.connect(self.updateGraphicsLayout)
        #Activate sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Sentinels to know wich graphic was selected in measurement
        self.measurementChannelA=False
        self.measurementChannelB=False
        self.measurementChannelC=False
        self.measurementChannelD=False
        #Sentinel to know if the device was disconnected in measurement
        self.disconnectedMeasurement=False
        #Sentinel to detect that a measurement begin was created
        self.treadCreated=False
        #variables for dialogs
        self.dialogACreated=None
        self.dialogBCreated=None
        self.dialogCCreated=None
        self.dialogDCreated=None
        self.dialogTableOpen=None
        self.dialogLabelOpen=None
        #Configure labels
        self.countChannelAValue.setText("A: No running")
        self.countChannelBValue.setText("B: No running")
        self.countChannelCValue.setText("C: No running")
        self.countChannelDValue.setText("D: No running")
        # label dialog 
        self.countChannelAValueClone= QLabel("A: No running")
        self.countChannelBValueClone= QLabel("B: No running")
        self.countChannelCValueClone= QLabel("C: No running")
        self.countChannelDValueClone= QLabel("D: No running")
        # uncertainties labels dialog
        self.countChannelAUncertaintyClone= QLabel("Not estimated yet")
        self.countChannelBUncertaintyClone= QLabel("Not estimated yet")
        self.countChannelCUncertaintyClone= QLabel("Not estimated yet")
        self.countChannelDUncertaintyClone= QLabel("Not estimated yet")
        #Connection for the buttons
        self.startButton.clicked.connect(self.startMeasure)
        self.stopButton.clicked.connect(self.stopMeasure)
        self.clearButtonChannelA.clicked.connect(self.clearChannelA)
        self.clearButtonChannelB.clicked.connect(self.clearChannelB)
        self.clearButtonChannelC.clicked.connect(self.clearChannelC)
        self.clearButtonChannelD.clicked.connect(self.clearChannelD)
        self.savePlotButton.clicked.connect(self.savePlots)
        self.saveDataButton.clicked.connect(self.saveData)
        self.helpButton.clicked.connect(self.helpButtonDialog)
        #Connection for the combo Box
        self.timeRangeComboBox.currentIndexChanged.connect(self.updateGraphic)
        #Creation data list for measurements
        #TODO: improve querys with deque, add uncertainties
        self.timestampsChannelA=[]
        self.timestampsChannelB=[]
        self.timestampsChannelC=[]
        self.timestampsChannelD=[]
        self.channelAValues=[]
        self.channelBValues=[]
        self.channelCValues=[]
        self.channelDValues=[]
        self.channelAUncertainties=[]
        self.channelBUncertainties=[]
        self.channelCUncertainties=[]
        self.channelDUncertainties=[]
        #Values for save data
        self.timestampsDateChannelA=[]
        self.timestampsDateChannelB=[]
        self.timestampsDateChannelC=[]
        self.timestampsDateChannelD=[]
        #Value for inital and final date
        self.initialDate=""
        self.finalDate=""
        #End connection for the checkbox
        
        #Create the sentinels for connection
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        #Create Clone Table
        self.createCloneTable()
        
        
        
        if device==None:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.clearButtonChannelA.setEnabled(False)
            self.clearButtonChannelB.setEnabled(False)
            self.clearButtonChannelC.setEnabled(False)
            self.clearButtonChannelD.setEnabled(False)
            self.saveDataButton.setEnabled(False)
            self.savePlotButton.setEnabled(False)
            
        
    
    #Funcion to dinamically changes the interface
    def checkBoxListenerChannels(self):
        """
        Updates the visibility of graphical elements and table columns based on the state of the channel checkboxes.

        This function performs the following actions:
        - Checks the state of each channel's checkbox (A, B, C, D).
        - Shows or hides the corresponding frame label for each channel depending on whether the checkbox is checked.
        - Calls `hideColumns()` to hide the table columns associated with unchecked channels.
        - Calls `updateGraphicsLayout()` to refresh the displayed plots based on the selected channels.

        :return: None
        """
        self.hideColumns()
        if self.channelACheckBox.isChecked():
            self.channelAFrameLabel.setVisible(True)
            if self.dialogLabelOpen:
                self.channelAFrameLabelClone.setVisible(True)
    
        else:
            self.channelAFrameLabel.setVisible(False)
            if self.dialogLabelOpen:
                self.channelAFrameLabelClone.setVisible(False)
                
        
        
        if self.channelBCheckBox.isChecked():
            self.channelBFrameLabel.setVisible(True)
            if self.dialogLabelOpen:
                self.channelBFrameLabelClone.setVisible(True)
                
        else:
            self.channelBFrameLabel.setVisible(False)
            if self.dialogLabelOpen:
                self.channelBFrameLabelClone.setVisible(False)
                

        
        if self.channelCCheckBox.isChecked():
            self.channelCFrameLabel.setVisible(True)
            if self.dialogLabelOpen:
                self.channelCFrameLabelClone.setVisible(True)
                
        else:
            self.channelCFrameLabel.setVisible(False)
            if self.dialogLabelOpen:
                self.channelCFrameLabelClone.setVisible(False)
                

        if self.channelDCheckBox.isChecked():
            self.channelDFrameLabel.setVisible(True)
            if self.dialogLabelOpen:
                self.channelDFrameLabelClone.setVisible(True)
                
        else:
            self.channelDFrameLabel.setVisible(False)
            if self.dialogLabelOpen:
                self.channelDFrameLabelClone.setVisible(False)
                
        #Here we update the graphics that are shown in the interface
        self.updateGraphicsLayout()
    
    def factoryGraphChannels(self, channel):
        """
        Creates and returns a configured plot widget for the specified measurement channel.

        This factory function generates a graphical layout for visualizing count data from one of the four available channels (A, B, C, or D). The plot is customized with a unique color per channel, grid display, axis labeling, and a legend. It returns the PyQtGraph components necessary for real-time plotting.

        This function performs the following actions:
        - Selects a predefined color for the specified channel.
        - Initializes a `GraphicsLayoutWidget` with a white background.
        - Adds a plot to the widget with grid lines, axis labels, and legend.
        - Creates a stylized curve object for plotting count data using markers and colored lines.
        - Returns the components needed to integrate the plot into the GUI and update it dynamically.

        :param channel: A single-character string indicating the channel ('A', 'B', 'C', or 'D').
        :return: A tuple containing:
            - `GraphicsLayoutWidget`: the plot container.
            - `PlotItem`: the configured plot.
            - `PlotDataItem`: the curve used for plotting the counts.
        """
        colors = {
            "A": (0, 114, 189),    # azul
            "B": (217, 83, 25),    # rojo-naranja
            "C": (237, 177, 32),   # amarillo
            "D": (126, 47, 142),   # púrpura
        }

        color = colors.get(channel, "k")

        winCountsGraph = pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')

        plotCounts = winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        plotCounts.setLabel('left', f'Counts channel {channel}')
        plotCounts.setLabel('bottom', 'Time (s)')
        plotCounts.addLegend()

        pen = mkPen(color=color, width=2.5)

      
        curve = plotCounts.plot(
            pen=pen,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=color,
            name='Counts Estimated'
        )

        return winCountsGraph, plotCounts, curve

    def factoryGraphsAllChannels(self):
        """
        Creates and returns a single plot widget containing curves for all selected measurement channels.

        This factory function generates a unified graphical layout that displays the estimated counts for channels A, B, C, and D in a single plot. Each channel is represented with a distinct color and labeled curve, depending on whether its checkbox is enabled. This approach consolidates the visualization into one graph rather than creating separate ones per channel.

        This function performs the following actions:
        - Defines a unique color for each channel (A, B, C, D).
        - Initializes a `GraphicsLayoutWidget` with a white background and grid lines.
        - Configures a single plot with appropriate axis labels and a legend.
        - Creates curve objects for each channel using stylized markers and pens.
        - Only assigns a name to a curve if its corresponding channel checkbox is checked.
        - Returns the complete widget and all channel curves for display and real-time updates.

        :return: A tuple containing:
            - `GraphicsLayoutWidget`: the shared plot container for all channels.
            - `PlotItem`: the unified plot area.
            - `PlotDataItem`: curve for channel A.
            - `PlotDataItem`: curve for channel B.
            - `PlotDataItem`: curve for channel C.
            - `PlotDataItem`: curve for channel D.
        """
        colors = {
            "A": (0, 114, 189),    # azul
            "B": (217, 83, 25),    # rojo-naranja
            "C": (237, 177, 32),   # amarillo
            "D": (126, 47, 142),   # púrpura
        }

        colorA = colors.get("A", "k")
        colorB = colors.get("B", "k")
        colorC = colors.get("C", "k")
        colorD = colors.get("D", "k")

        winCountsGraph = pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')

        plotCounts = winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        plotCounts.setLabel('left', f'Counts channels')
        plotCounts.setLabel('bottom', 'Time (s)')
        plotCounts.addLegend()

        penA = mkPen(color=colorA, width=2.5)
        penB = mkPen(color=colorB, width=2.5)
        penC = mkPen(color=colorC, width=2.5)
        penD = mkPen(color=colorD, width=2.5)

      
        curveA = plotCounts.plot(
            pen=penA,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorA,
            name='Counts Estimated A'  if self.channelACheckBox.isChecked() else None
        )
        
        curveB = plotCounts.plot(
            pen=penB,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorB,
            name='Counts Estimated B' if self.channelBCheckBox.isChecked() else None
        )
        
        curveC = plotCounts.plot(
            pen=penC,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorC,
            name='Counts Estimated C' if self.channelCCheckBox.isChecked() else None
        )
        
        curveD = plotCounts.plot(
            pen=penD,
            symbol='o',                   
            symbolSize=7,
            symbolBrush=colorD,
            name='Counts Estimated D' if self.channelDCheckBox.isChecked() else None
        )

        return winCountsGraph, plotCounts, curveA, curveB, curveC, curveD
    

    def constructGraphicA(self):
        """
        Constructs and initializes the graphical components for channel A.

        This function uses the `factoryGraphChannels` method to generate the graphical layout for channel A, including the main plot widget, the plot area, and the curve used to display count data. The resulting components are stored as instance variables for later access and updates during measurement.

        This function performs the following actions:
        - Calls `factoryGraphChannels` with channel 'A' to generate the graph.
        - Stores the returned plot widget, plot item, and curve for channel A.

        :return: None
        """
        self.winCountsGraphA, self.plotCountsA, self.curveCountsA = self.factoryGraphChannels('A')
        
    
    def constructGraphicB(self):
        """
        Constructs and initializes the graphical components for channel B.

        This function uses the `factoryGraphChannels` method to generate the graphical layout for channel B, including the main plot widget, the plot area, and the curve used to display count data. The resulting components are stored as instance variables for later access and updates during measurement.

        This function performs the following actions:
        - Calls `factoryGraphChannels` with channel 'B' to generate the graph.
        - Stores the returned plot widget, plot item, and curve for channel B.

        :return: None
        """
        self.winCountsGraphB, self.plotCountsB, self.curveCountsB = self.factoryGraphChannels('B')
        
    
    def constructGraphicC(self):
        """
        Constructs and initializes the graphical components for channel C.

        This function uses the `factoryGraphChannels` method to generate the graphical layout for channel C, including the main plot widget, the plot area, and the curve used to display count data. The resulting components are stored as instance variables for later access and updates during measurement.

        This function performs the following actions:
        - Calls `factoryGraphChannels` with channel 'C' to generate the graph.
        - Stores the returned plot widget, plot item, and curve for channel C.

        :return: None
        """
        self.winCountsGraphC, self.plotCountsC, self.curveCountsC = self.factoryGraphChannels('C')
        
    
    def constructGraphicD(self):
        """
        Constructs and initializes the graphical components for channel D.

        This function uses the `factoryGraphChannels` method to generate the graphical layout for channel D, including the main plot widget, the plot area, and the curve used to display count data. The resulting components are stored as instance variables for later access and updates during measurement.

        This function performs the following actions:
        - Calls `factoryGraphChannels` with channel 'D' to generate the graph.
        - Stores the returned plot widget, plot item, and curve for channel D.

        :return: None
        """
        self.winCountsGraphD, self.plotCountsD, self.curveCountsD = self.factoryGraphChannels('D')
    
    def constructAllGraphics(self):
        """
        Constructs and initializes the unified graphical layout for all measurement channels.

        This function calls `factoryGraphsAllChannels` to generate a single plot widget that contains curves for channels A, B, C, and D. Each curve is customized by color and visibility based on whether its corresponding checkbox is enabled. The resulting components are stored as instance variables for centralized access and updates.

        This function performs the following actions:
        - Calls `factoryGraphsAllChannels` to create the shared plot and individual channel curves.
        - Stores the plot widget, plot item, and all channel-specific curves as instance variables.

        :return: None
        """
        self.winCountsAllGraph, self.plotCountsAllC, self.cuveCountsAllA, self.cuveCountsAllB, self.cuveCountsAllC,self.cuveCountsAllD =self.factoryGraphsAllChannels()
        

    def createCloneTable(self):
        """
        Creates and configures a cloned table instance for storing a copy of the measurement data.

        This function initializes a separate `QTableWidget` that mirrors the structure of the main count table. It includes predefined column headers for the date and channels A, B, C, and D. The cloned table is set to stretch its columns to fit the available space and is made read-only to prevent user edits.

        This function performs the following actions:
        - Creates a new `QTableWidget` instance with 5 columns.
        - Sets the horizontal headers to ['Date', 'A', 'B', 'C', 'D'].
        - Enables automatic stretching of column widths.
        - Disables editing to preserve the integrity of the data.

        :return: None
        """
        self.cloneTable=QTableWidget()
        self.cloneTable.setColumnCount(5)
        self.cloneTable.setHorizontalHeaderLabels(['Date','A','B','C','D'])
        self.cloneTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cloneTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        

    #Function to update wich graphics are shown
    def updateGraphicsLayout(self):
        """
        Updates the graphical layout based on the selected visualization mode and active channel checkboxes.

        This function dynamically reconfigures how the channel plots are displayed, depending on the selected radio button mode: 
        separate graphics, merged graph, or detached dialogs. It ensures that the interface reflects the current user selections by showing or hiding the corresponding curves, windows, or layouts.

        This function performs the following actions:
        - If **separate graphics** mode is selected:
            - Closes any open detached dialogs.
            - Clears the current layout inside the `graphicsFrame`.
            - Creates individual graphs for each selected channel (A–D).
            - Arranges them responsively:
                - 1 channel → full frame.
                - 2 channels → one above the other.
                - 3 channels → two top, one bottom.
                - 4 channels → 2×2 grid layout.
        - If **merge graphics** mode is selected:
            - Closes detached dialogs if any exist.
            - Clears the layout in `graphicsFrame`.
            - Creates a single graph containing all curves.
            - Displays or hides each curve depending on its checkbox status.
        - If **detached graphics** mode is selected:
            - Clears the main `graphicsFrame` layout.
            - For each selected channel (A–D), opens a dedicated dialog window.
            - Loads previous data into the newly created plots.
            - Closes dialog windows for unchecked channels.

        :return: None
        """
        if self.separateGraphics.isChecked():
            if self.dialogACreated:
                self.dialogACreated.close()
                self.dialogACreated=None
                self.channelACheckBox.setChecked(True)
            if self.dialogBCreated:
                self.dialogBCreated.close()
                self.dialogBCreated=None
                self.channelBCheckBox.setChecked(True)
            if self.dialogCCreated:
                self.dialogCCreated.close()
                self.dialogCCreated=None
                self.channelCCheckBox.setChecked(True)
            if self.dialogDCreated:
                self.dialogDCreated.close()
                self.dialogDCreated=None
                self.channelDCheckBox.setChecked(True)
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy

            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)

            selected_graphs = []

            for checkbox, label in zip(
                [self.channelACheckBox, self.channelBCheckBox, self.channelCCheckBox, self.channelDCheckBox],
                ["A", "B", "C", "D"]
            ):
                if checkbox.isChecked():
                    graph, plot, curve = self.factoryGraphChannels(label)
                    graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    selected_graphs.append(graph)

                    # Copiar los datos antiguos a las nuevas curvas
                    if label == "A":
                        curve.setData(self.timestampsChannelA, self.channelAValues)
                        self.curveCountsA = curve
                        self.winCountsGraphA = graph
                        self.plotCountsA = plot
                    elif label == "B":
                        curve.setData(self.timestampsChannelB, self.channelBValues)
                        self.curveCountsB = curve
                        self.winCountsGraphB = graph
                        self.plotCountsB = plot
                    elif label == "C":
                        curve.setData(self.timestampsChannelC, self.channelCValues)
                        self.curveCountsC = curve
                        self.winCountsGraphC = graph
                        self.plotCountsC = plot
                    elif label == "D":
                        curve.setData(self.timestampsChannelD, self.channelDValues)
                        self.curveCountsD = curve
                        self.winCountsGraphD = graph
                        self.plotCountsD = plot

            count = len(selected_graphs)
            if count == 0:
                return

            top_row = QHBoxLayout()
            bottom_row = QHBoxLayout()

            if count == 1:
                
                selected_graphs[0].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                top_row.addWidget(selected_graphs[0])
                layout.addLayout(top_row)

            elif count == 2:
                top_row.addWidget(selected_graphs[0])
                bottom_row.addWidget(selected_graphs[1])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
            elif count == 3:
                top_row.addWidget(selected_graphs[0])
                top_row.addWidget(selected_graphs[1])
                selected_graphs[2].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                bottom_row.addWidget(selected_graphs[2])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
            elif count == 4:
                top_row.addWidget(selected_graphs[0])
                top_row.addWidget(selected_graphs[1])
                bottom_row.addWidget(selected_graphs[2])
                bottom_row.addWidget(selected_graphs[3])
                layout.addLayout(top_row)
                layout.addLayout(bottom_row)
        elif self.mergeGraphics.isChecked():
            if self.dialogACreated:
                self.dialogACreated.close()
                self.dialogACreated=None
                self.channelACheckBox.setChecked(True)
            if self.dialogBCreated:
                self.dialogBCreated.close()
                self.dialogBCreated=None
                self.channelBCheckBox.setChecked(True)
            if self.dialogCCreated:
                self.dialogCCreated.close()
                self.dialogCCreated=None
                self.channelCCheckBox.setChecked(True)
            if self.dialogDCreated:
                self.dialogDCreated.close()
                self.dialogDCreated=None
                self.channelDCheckBox.setChecked(True)
            
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy

            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)
            
            graph, plot, curveA, curveB, curveC,curveD = self.factoryGraphsAllChannels()
            graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            curveA.setData(self.timestampsChannelA, self.channelAValues)
            curveB.setData(self.timestampsChannelB, self.channelBValues)
            curveC.setData(self.timestampsChannelC, self.channelCValues)
            curveD.setData(self.timestampsChannelD, self.channelDValues)
            self.curveCountsA= curveA
            self.curveCountsB= curveB
            self.curveCountsC= curveC
            self.curveCountsD= curveD
            self.winCountsGraphA = graph
            self.winCountsGraphB = graph
            self.winCountsGraphC = graph
            self.winCountsGraphD = graph
            self.plotCountsA = plot
            self.plotCountsB = plot
            self.plotCountsC = plot
            self.plotCountsD = plot
            top_row = QHBoxLayout()
            if self.channelACheckBox.isChecked() or self.channelBCheckBox.isChecked() or self.channelCCheckBox.isChecked() or self.channelDCheckBox.isChecked():
                top_row.addWidget(graph)
                layout.addLayout(top_row)
            if not self.channelACheckBox.isChecked():
                self.curveCountsA.hide()
            if not self.channelBCheckBox.isChecked():
                self.curveCountsB.hide()
            if not self.channelCCheckBox.isChecked():
                self.curveCountsC.hide()
            if not self.channelDCheckBox.isChecked():
                self.curveCountsD.hide()
        elif self.deatachedGraphics.isChecked():  
            from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
            #Delete layout
            layout = self.graphicsFrame.layout()
            if layout is None or not isinstance(layout, QVBoxLayout):
                layout = QVBoxLayout()
                self.graphicsFrame.setLayout(layout)
            else:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.layout():
                        sublayout = item.layout()
                        while sublayout.count():
                            subitem = sublayout.takeAt(0)
                            if subitem.widget():
                                subitem.widget().setParent(None)
                        layout.removeItem(item)
            #Check the selected graphics
            if not self.dialogACreated and self.channelACheckBox.isChecked():
                self.dialogACreated= self.createDialogFactory("A")
                self.winCountsGraphA, self.plotCountsA, self.curveCountsA= self.factoryGraphChannels("A")
                layoutChannelA=QVBoxLayout(self.dialogACreated)
                layoutChannelA.addWidget(self.winCountsGraphA)
                self.curveCountsA.setData(self.timestampsChannelA, self.channelAValues)
                self.dialogACreated.show()
            elif self.dialogACreated and not self.channelACheckBox.isChecked():
                self.dialogACreated.close()
                self.dialogACreated=None
            if not self.dialogBCreated and self.channelBCheckBox.isChecked():
                self.dialogBCreated= self.createDialogFactory("B")
                self.winCountsGraphB, self.plotCountsB, self.curveCountsB= self.factoryGraphChannels("B")
                layoutChannelB=QVBoxLayout(self.dialogBCreated)
                layoutChannelB.addWidget(self.winCountsGraphB)
                self.curveCountsB.setData(self.timestampsChannelB, self.channelBValues)
                self.dialogBCreated.show()
            elif self.dialogBCreated and not self.channelBCheckBox.isChecked():
                self.dialogBCreated.close()
                self.dialogBCreated=None
            if not self.dialogCCreated and self.channelCCheckBox.isChecked():
                self.dialogCCreated= self.createDialogFactory("C")
                self.winCountsGraphC, self.plotCountsC, self.curveCountsC= self.factoryGraphChannels("C")
                layoutChannelC=QVBoxLayout(self.dialogCCreated)
                layoutChannelC.addWidget(self.winCountsGraphC)
                self.curveCountsC.setData(self.timestampsChannelC, self.channelCValues)
                self.dialogCCreated.show()
            elif self.dialogCCreated and not self.channelCCheckBox.isChecked():
                self.dialogCCreated.close()
                self.dialogCCreated=None
            if not self.dialogDCreated and self.channelDCheckBox.isChecked():
                self.dialogDCreated= self.createDialogFactory("D")
                self.winCountsGraphD, self.plotCountsD, self.curveCountsD= self.factoryGraphChannels("D")
                layoutChannelD=QVBoxLayout(self.dialogDCreated)
                layoutChannelD.addWidget(self.winCountsGraphD)
                self.curveCountsD.setData(self.timestampsChannelD, self.channelDValues)
                self.dialogDCreated.show()
            elif self.dialogDCreated and not self.channelDCheckBox.isChecked():
                self.dialogDCreated.close()
                self.dialogDCreated=None
                
        self.updateGraphic()
    
    
    def connectedDevice(self,device):
        """
        Handles the UI and internal state updates when the device is successfully connected.

        This function performs the following actions:
        - Enables the disconnect button and disables the connect button in the main window.
        - Updates the internal sentinel to indicate that the device is connected and measurements are allowed.
        - Stores the reference to the connected device.
        - Enables the start button to allow measurements to begin.
        - (Optional) Starts a timer for updating measurement status (currently commented out).

        :param device: The connected device instance.
        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(True)
        self.mainWindow.connectButton.setEnabled(False)
        self.disconnectedMeasurement=False
        #TODO: SET THE TIMER OF MEASUREMENTS
        #self.timerStatus.start(500)
        self.device=device
        self.startButton.setEnabled(True)
    
    
    
    
    def disconnectedDevice(self):
        """
        Handles the UI and internal state updates when the device is disconnected.

        This function performs the following actions:
        - Disables the disconnect button and enables the connect button in the main window.
        - Disables the start button to prevent new measurements from being initiated.
        - (Optional) May start a timer for monitoring status or reconnection attempts (currently commented out).

        :return: None
        """
        self.mainWindow.disconnectButton.setEnabled(False)
        self.mainWindow.connectButton.setEnabled(True)
        #TODO: SET THE TIMER OF MEASUREMENTS
        #self.timerStatus.start(500)
        self.startButton.setEnabled(False)

    def startMeasure(self):
        """
        Starts the count measurement process by configuring the UI, preparing internal states, and launching the background worker thread.

        This function is triggered when the user clicks the Start button. It verifies that at least one measurement channel (A–D) is selected. If so, it proceeds to initialize the measurement by disabling conflicting buttons and tabs, saving current settings, resetting values, and setting up the worker thread responsible for data acquisition. If no channels are selected, it displays a dialog warning the user.

        This function performs the following actions:
        - Verifies that at least one channel checkbox is active.
        - Disables the Start button and enables the Stop button.
        - Disables data saving buttons and tab navigation to prevent user interference.
        - Saves current settings and stops the connection monitoring timer.
        - Resets measurement values and identifies the selected channels.
        - Updates the UI status bar to indicate active measurement.
        - Creates and configures a `WorkerThreadCountsEstimated` thread to perform background data acquisition.
        - Connects various thread signals to corresponding update methods in the class.
        - Starts the measurement thread.
        - If no channels are selected, displays a warning dialog prompting the user to activate at least one channel.

        :return: None
        """
        if self.channelACheckBox.isChecked() or self.channelBCheckBox.isChecked() or self.channelCCheckBox.isChecked() or self.channelDCheckBox.isChecked():
            self.initialDate=""
            self.finalDate=""
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            #Disable save buttons
            self.saveDataButton.setEnabled(False)
            self.savePlotButton.setEnabled(False)
            #Disable other tabs while the software is taking measurements
            self.mainWindow.tabs.setTabEnabled(0,False)
            self.mainWindow.tabs.setTabEnabled(1,False)
            self.mainWindow.saveSettings()
            self.saveSettings()
            self.stopTimerConnection()
            self.resetValues()
            self.getChannelsMeasure()
            self.enableButtons()
            self.changeStatusColor(1)
            self.mainWindow.activeMeasurement()
            self.worker=WorkerThreadCountsEstimated(self.selectChannelA,self.selectChannelB,self.selectChannelC,self.selectChannelD, self.device)
            self.worker.finished.connect(self.finishedThread)
            self.worker.newMeasurement.connect(self.captureMeasurement)
            self.worker.updateLabel.connect(self.updateLabels)
            self.worker.initialDate.connect(self.captureInitalDate)
            self.worker.finalDate.connect(self.captureFinalDate)
            self.worker.noTotalMeasurements.connect(self.noMeasurementsFounded)
            self.worker.noPartialMeasurements.connect(self.eliminateCheckBoxChannels)
            self.worker.changeStatusText.connect(self.changeStatusLabel)
            self.worker.changeStatusColor.connect(self.changeStatusColor)
            self.worker.disconnectedDevice.connect(self.lostConnection)
            self.worker.start()
        else:
            self.noChannelsSelected()
    
    def stopMeasure(self):
        """
        Stops the ongoing measurement process and restores the UI and device to their initial configuration.

        This function is triggered when the user clicks the Stop button. It halts the background measurement thread, resets relevant internal flags (sentinels), re-enables UI tabs and controls, and restores the initial settings of the Tempico device if the disconnection did not occur. If the device was disconnected during measurement, it triggers the disconnection handling routine.

        This function performs the following actions:
        - Re-enables the disabled UI tabs to allow user interaction post-measurement.
        - Calls `resetSentinels()` to clear internal flags related to active measurement channels.
        - Disables the Stop button and signals the worker thread to stop.
        - If the device is still connected:
            - Restarts the connection-monitoring timer.
            - Re-enables the disconnect button.
        - If the device was disconnected during measurement:
            - Triggers the disconnection handling logic in the main window.
        - Updates the main window status to indicate that no measurement is currently running.
        - Calls `returnSettings()` to restore device parameters to their original configuration.

        :return: None
        """
        self.mainWindow.tabs.setTabEnabled(0,True)
        self.mainWindow.tabs.setTabEnabled(1,True)
        self.resetSentinels()
        self.stopButton.setEnabled(False)
        self.worker.stop()
        
        if not self.disconnectedMeasurement:
            self.startTimerConnection()
            self.mainWindow.disconnectButton.setEnabled(True)        
        else:
            self.mainWindow.disconnectedDevice()
        self.mainWindow.noMeasurement()
        self.returnSettings()
        self.mainWindow.enableSettings()
        
        
    
    def stopTimerConnection(self):
        """
        Stops the connection monitoring timer during an active measurement.

        This function is called when a measurement begins to prevent interference from the periodic connection checks. It halts the `timerConnection`, which normally runs in the background to monitor the status of the Tempico device.

        :return: None
        """
        #Stop timer when a measurement begins
        self.timerConnection.stop()
    
    def startTimerConnection(self):
        """
        Starts the connection monitoring timer to periodically check the device status.

        This function activates the `timerConnection`, which verifies the connection with the Tempico device every 500 milliseconds. It is typically called after a measurement has ended or when the device is reconnected, ensuring continuous monitoring of the device’s availability.

        :return: None
        """
        #Start timer when a measurement begins
        self.timerConnection.start(500)
    
    def clearChannelA(self):
        """
        Clears all stored measurement data for channel A and updates the corresponding plot.

        This function is called when the user clicks the Clear button for channel A. It resets the timestamp lists and count values associated with channel A, and refreshes the plot to reflect the cleared state.

        This function performs the following actions:
        - Empties the list of raw timestamps and formatted date timestamps for channel A.
        - Clears the list of count values associated with channel A.
        - Updates the channel A curve to remove all plotted data.

        :return: None
        """

        self.timestampsChannelA=[]
        self.timestampsDateChannelA=[]
        self.channelAValues=[]
        self.channelAUncertainties=[]
        self.curveCountsA.setData(self.timestampsChannelA,self.channelAValues)
    
    def clearChannelB(self):
        """
        Clears all stored measurement data for channel B and updates the corresponding plot.

        This function is called when the user clicks the Clear button for channel B. It resets the timestamp lists and count values associated with channel B, and refreshes the plot to reflect the cleared state.

        This function performs the following actions:
        - Empties the list of raw timestamps and formatted date timestamps for channel B.
        - Clears the list of count values associated with channel B.
        - Updates the channel B curve to remove all plotted data.

        :return: None
        """
        self.timestampsChannelB=[]
        self.timestampsDateChannelB=[]
        self.channelBValues=[]
        self.channelBUncertainties=[]
        self.curveCountsB.setData(self.timestampsChannelB,self.channelBValues)
    
    def clearChannelC(self):
        """
        Clears all stored measurement data for channel C and updates the corresponding plot.

        This function is called when the user clicks the Clear button for channel C. It resets the timestamp lists and count values associated with channel C, and refreshes the plot to reflect the cleared state.

        This function performs the following actions:
        - Empties the list of raw timestamps and formatted date timestamps for channel C.
        - Clears the list of count values associated with channel C.
        - Updates the channel C curve to remove all plotted data.

        :return: None
        """
        self.timestampsChannelC=[]
        self.timestampsDateChannelC=[]
        self.channelCValues=[]
        self.channelCUncertainties=[]
        self.curveCountsC.setData(self.timestampsChannelC,self.channelCValues)
    
    def clearChannelD(self):
        """
        Clears all stored measurement data for channel D and updates the corresponding plot.

        This function is called when the user clicks the Clear button for channel D. It resets the timestamp lists and count values associated with channel D, and refreshes the plot to reflect the cleared state.

        This function performs the following actions:
        - Empties the list of raw timestamps and formatted date timestamps for channel D.
        - Clears the list of count values associated with channel D.
        - Updates the channel D curve to remove all plotted data.

        :return: None
        """
        self.timestampsChannelD=[]
        self.timestampsDateChannelD=[]
        self.channelDValues=[]
        self.channelDUncertainties=[]
        self.curveCountsD.setData(self.timestampsChannelD,self.channelDValues)
        
    #Functions to create all the dialogs for each graphic
    def createDialogFactory(self, channel):
        """
        Creates and returns a non-modal dialog window for displaying detached graphics for the specified channel.

        This factory function is used when the user selects the "detached graphics" mode. It generates a dedicated `QDialog` for a given channel (A, B, C, or D), configures its appearance and behavior, and positions it to avoid overlap with other dialogs. The dialog is linked to a callback that ensures proper cleanup when it is closed.

        This function performs the following actions:
        - Instantiates a `QDialog` as a child of the main window.
        - Sets the dialog title and default size.
        - Connects the `finished` signal to a cleanup method for the channel.
        - Assigns a fixed screen position for each channel to avoid visual overlap.

        :param channel: A string indicating the target channel ('A', 'B', 'C', or 'D').
        :return: A configured, ready-to-display `QDialog` for the given channel.
        """
        dialog = QDialog(self.mainWindow)
        dialog.setWindowTitle(f"Detached Graphics {channel}")
        dialog.resize(400, 300)
        dialog.setModal(False)
        dialog.finished.connect(lambda _: self.closeDialogChannels(channel))

        # Asignar posición para evitar superposición
        offsets = {
            "A": (100, 100),
            "B": (550, 100),
            "C": (100, 450),
            "D": (550, 450)
        }
        if channel in offsets:
            x, y = offsets[channel]
            dialog.move(x, y)

        return dialog
        
    def updateGraphic(self):
        """
        Updates the visible X-axis range of all channel plots based on the selected time window.

        This function is triggered when the user changes the time range using the `timeRangeComboBox`. It determines the most recent timestamp in channel A and adjusts the X-axis range for all plots (A–D) accordingly, displaying only the data within the selected time interval.

        This function performs the following actions:
        - Verifies that channel A has data; if not, it exits early.
        - Attempts to extract the number of seconds from the selected combo box option.
        - Calculates the minimum and maximum X-axis values based on the most recent timestamp.
        - Updates the X-axis range of all plots (A, B, C, and D) to reflect the selected time window.

        :return: None
        """
        if not self.timestampsChannelA:
            return
        # Apply seconds filter to the list
        try:
            segundosValue= int(self.timeRangeComboBox.currentText().split()[0])
        except ValueError:
            segundosValue = 10  # fallback
        x_max = self.timestampsChannelA[-1]
        x_min = x_max - segundosValue
        self.plotCountsA.setXRange(x_min, x_max, padding=0)
        self.plotCountsB.setXRange(x_min, x_max, padding=0)
        self.plotCountsC.setXRange(x_min, x_max, padding=0)
        self.plotCountsD.setXRange(x_min, x_max, padding=0)
        
    
    def getChannelsMeasure(self):
        """
        Determines which measurement channels are selected and updates internal sentinels accordingly.

        This function evaluates the state of each channel's checkbox (A, B, C, D) to establish which channels will participate in the measurement. It sets the corresponding selection and measurement sentinels to `True` or `False` based on the checkboxes. Additionally, it disables the checkbox for any unselected channel to prevent user changes during the active measurement session.

        This function performs the following actions:
        - Assumes all channels are selected by default.
        - Checks the state of each channel checkbox and updates:
            - `selectChannelX`: sentinel to include channel X in the measurement loop.
            - `measurementChannelX`: sentinel to track measurement activity per channel.
        - Disables the checkbox for any channel that was not selected to lock in the configuration.

        :return: None
        """
        self.selectChannelA=True
        self.selectChannelB=True
        self.selectChannelC=True
        self.selectChannelD=True
        self.measurementChannelA=True
        self.measurementChannelB=True
        self.measurementChannelC=True
        self.measurementChannelD=True
        if not self.channelACheckBox.isChecked():
            self.selectChannelA=False
            self.measurementChannelA=False
            self.channelACheckBox.setEnabled(False)
        if not self.channelBCheckBox.isChecked():
            self.selectChannelB=False
            self.measurementChannelB=False
            self.channelBCheckBox.setEnabled(False)
        if not self.channelCCheckBox.isChecked():
            self.selectChannelC=False
            self.measurementChannelC=False
            self.channelCCheckBox.setEnabled(False)
        if not self.channelDCheckBox.isChecked():
            self.selectChannelD=False
            self.measurementChannelD=False
            self.channelDCheckBox.setEnabled(False)
    
    def resetSentinels(self):
        """
        Resets internal channel selection sentinels and re-enables all channel checkboxes.

        This function is typically called after a measurement is stopped. It clears the selection flags (`selectChannelX`) for all channels (A–D) and re-enables their corresponding checkboxes in the UI, allowing the user to configure new measurement selections.

        This function performs the following actions:
        - Sets all `selectChannelX` sentinels to `False`, indicating no active selections.
        - Enables the checkboxes for channels A, B, C, and D to restore full configuration flexibility.

        :return: None
        """
        #Reset selected sentinels
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Reset enable checkbox
        self.channelACheckBox.setEnabled(True)
        self.channelBCheckBox.setEnabled(True)
        self.channelCCheckBox.setEnabled(True)
        self.channelDCheckBox.setEnabled(True)
    
    def saveSettings(self):
        """
        Saves the current configuration settings of the Tempico device for all channels.

        This function queries the device and stores key configuration parameters for each channel (A–D), such as the number of stops, acquisition mode, averaging cycles, and stop mask. These values are cached in instance variables so they can be restored later (e.g., after a measurement session). If the device is unavailable or any read operation fails, the function safely ignores the error.

        This function performs the following actions:
        - Retrieves and stores the global number of acquisition runs.
        - Retrieves and stores the number of stops per channel.
        - Retrieves and stores the operation mode per channel.
        - Retrieves and stores the number of averaging cycles per channel.
        - Retrieves and stores the stop mask per channel.
        - Ignores exceptions silently if the device is not ready.

        :return: None
        """
        try:
            self.numberRunsSetting=self.device.getNumberOfRuns()
            #Number of stops
            self.numberStopsChannelASetting=self.device.ch1.getNumberOfStops()
            self.numberStopsChannelBSetting=self.device.ch2.getNumberOfStops()
            self.numberStopsChannelCSetting=self.device.ch3.getNumberOfStops()
            self.numberStopsChannelDSetting=self.device.ch4.getNumberOfStops()
            #Mode
            self.modeChannelASetting=self.device.ch1.getMode()
            self.modeChannelBSetting=self.device.ch2.getMode()
            self.modeChannelCSetting=self.device.ch3.getMode()
            self.modeChannelDSetting=self.device.ch4.getMode()
            #AverageCycles
            self.averageCyclesChannelASetting=self.device.ch1.getAverageCycles()
            self.averageCyclesChannelBSetting=self.device.ch2.getAverageCycles()
            self.averageCyclesChannelCSetting=self.device.ch3.getAverageCycles()
            self.averageCyclesChannelDSetting=self.device.ch4.getAverageCycles()
            #StopMask
            self.stopMaskChannelASetting=self.device.ch1.getStopMask()
            self.stopMaskChannelBSetting=self.device.ch2.getStopMask()
            self.stopMaskChannelCSetting=self.device.ch3.getStopMask()
            self.stopMaskChannelDSetting=self.device.ch4.getStopMask()
            #Settings to save in the data
            self.thresholdVoltageSetting=self.device.getThresholdVoltage()
            self.channelAEdgeTypeSetting=self.device.ch1.getStopEdge()
            self.channelBEdgeTypeSetting=self.device.ch2.getStopEdge()
            self.channelCEdgeTypeSetting=self.device.ch3.getStopEdge()
            self.channelDEdgeTypeSetting=self.device.ch4.getStopEdge()
        except:
            pass
        
    
    
    
    def returnSettings(self):
        """
        Restores the previously saved configuration settings to the Tempico device.

        This function is typically called after a measurement session ends. It applies the saved settings—previously captured via `saveSettings()`—back to the Tempico device for all channels (A–D). This includes restoring the number of runs, number of stops, mode, averaging cycles, and stop mask values. If any of the required variables were not initialized (e.g., due to a missing `saveSettings()` call), the function catches the `NameError` and prints the exception.

        This function performs the following actions:
        - Restores the number of acquisition runs for the entire device.
        - Restores the number of averaging cycles for each channel.
        - Restores the number of stop events for each channel.
        - Restores the operation mode for each channel.
        - Restores the stop mask configuration for each channel.
        - Catches and prints `NameError` if any setting is undefined.

        :return: None
        """
        try:
            
            #Return number of runs
            self.device.setNumberOfRuns(self.numberRunsSetting)
            #Return average cycles
            self.device.ch1.setAverageCycles(int(self.averageCyclesChannelASetting))
            self.device.ch2.setAverageCycles(int(self.averageCyclesChannelBSetting))
            self.device.ch3.setAverageCycles(int(self.averageCyclesChannelCSetting))
            self.device.ch4.setAverageCycles(int(self.averageCyclesChannelDSetting))
            #Return number of stops
            self.device.ch1.setNumberOfStops(self.numberStopsChannelASetting)
            self.device.ch2.setNumberOfStops(self.numberStopsChannelBSetting)
            self.device.ch3.setNumberOfStops(self.numberStopsChannelCSetting)
            self.device.ch4.setNumberOfStops(self.numberStopsChannelDSetting)
            #Return mode
            self.device.ch1.setMode(self.modeChannelASetting)
            self.device.ch2.setMode(self.modeChannelBSetting)
            self.device.ch3.setMode(self.modeChannelCSetting)
            self.device.ch4.setMode(self.modeChannelDSetting)
            
            #Return stop mask
            self.device.ch1.setStopMask(self.stopMaskChannelASetting)
            self.device.ch2.setStopMask(self.stopMaskChannelBSetting)
            self.device.ch3.setStopMask(self.stopMaskChannelCSetting)
            self.device.ch4.setStopMask(self.stopMaskChannelDSetting)   
        except:
            pass
        
    def resetValues(self):
        """
        Resets all measurement-related data, graphics, tables, and save-state sentinels to their initial state.

        This function is typically called before starting a new measurement session. It ensures that all previous data and UI elements are cleared to avoid inconsistencies or overlapping results. It resets internal storage lists, clears the curves on the plots, empties the result tables, and resets file save status indicators.

        This function performs the following actions:
        - Clears all count values and timestamps for channels A–D.
        - Clears the corresponding date-formatted timestamp lists.
        - Resets the row count of the main and cloned data tables.
        - Clears all data from the plotted curves for each channel.
        - Resets internal sentinels that track whether the data has been saved in TXT, CSV, or DAT format.

        :return: None
        """
        #Delete the values
        self.channelAValues=[]
        self.channelBValues=[]
        self.channelCValues=[]
        self.channelDValues=[]
        #Delete the timestamps
        self.timestampsChannelA=[]
        self.timestampsChannelB=[]
        self.timestampsChannelC=[]
        self.timestampsChannelD=[]
        #Delete date time stamps
        self.timestampsDateChannelA=[]
        self.timestampsDateChannelB=[]
        self.timestampsDateChannelC=[]
        self.timestampsDateChannelD=[]
        #Reset Uncertainties
        self.channelAUncertainties=[]
        self.channelBUncertainties=[]
        self.channelCUncertainties=[]
        self.channelDUncertainties=[]
        #Reset table rows
        self.tableCounts.setRowCount(0)
        self.cloneTable.setRowCount(0)
        #Reset graphics
        self.curveCountsA.setData(self.timestampsChannelA,self.channelAValues)
        self.curveCountsB.setData(self.timestampsChannelB,self.channelBValues)
        self.curveCountsC.setData(self.timestampsChannelC,self.channelCValues)
        self.curveCountsD.setData(self.timestampsChannelD,self.channelDValues)
        #Reset sentinels to save data
        self.sentinelsavetxt=0
        self.sentinelsavecsv=0
        self.sentinelsavedat=0
        

    
    def enableButtons(self):
        """
        Enables or disables the clear buttons for each channel based on the current selection state.

        This function checks which channels (A–D) have been marked as selected for measurement and enables their corresponding "Clear" buttons. If a channel is not selected, its clear button remains disabled. Additionally, it disables the disconnect button to prevent accidental disconnection during an active measurement setup.

        This function performs the following actions:
        - Enables the "Clear" button for each selected channel.
        - Disables the "Clear" button for any unselected channel.
        - Disables the disconnect button in the main window.

        :return: None
        """
        if not self.selectChannelA:
            self.clearButtonChannelA.setEnabled(False)
        else:
            self.clearButtonChannelA.setEnabled(True)
        
        if not self.selectChannelB:
            self.clearButtonChannelB.setEnabled(False)
        else:
            self.clearButtonChannelB.setEnabled(True)
        
        if not self.selectChannelC:
            self.clearButtonChannelC.setEnabled(False)
        else:
            self.clearButtonChannelC.setEnabled(True)
        
        if not self.selectChannelD:
            self.clearButtonChannelD.setEnabled(False)
        else:
            self.clearButtonChannelD.setEnabled(True)
        self.mainWindow.disconnectButton.setEnabled(False)
            
    
    #Hide and show column for channels measurement
    def hideColumns(self):
        """
        Updates the visibility of the table columns based on the selected measurement channels.

        This function ensures that only the columns corresponding to active channels (A–D) are visible in both the main and cloned data tables. It first shows all channel columns, then hides those whose associated checkboxes are unchecked.

        This function performs the following actions:
        - Ensures all channel columns (1–4) are visible initially in both `tableCounts` and `cloneTable`.
        - Checks the state of each channel's checkbox.
        - Hides the column in both tables for any channel that is not currently selected.

        :return: None
        """
        #First show all columns
        self.tableCounts.showColumn(1);
        self.tableCounts.showColumn(2);
        self.tableCounts.showColumn(3);
        self.tableCounts.showColumn(4);
        #Show all columns for clone table
        self.cloneTable.showColumn(1);
        self.cloneTable.showColumn(2);
        self.cloneTable.showColumn(3);
        self.cloneTable.showColumn(4);
        #Hide columns according sentinels
        if not self.channelACheckBox.isChecked():
            self.tableCounts.hideColumn(1)
            self.cloneTable.hideColumn(1)
        if not self.channelBCheckBox.isChecked():
            self.tableCounts.hideColumn(2)
            self.cloneTable.hideColumn(2)
        if not self.channelCCheckBox.isChecked():
            self.tableCounts.hideColumn(3)
            self.cloneTable.hideColumn(3)
        if not self.channelDCheckBox.isChecked():
            self.tableCounts.hideColumn(4)
            self.cloneTable.hideColumn(4)
        
        
    
        
    
    def captureMeasurement(self,secondsTime,dateTime,channelAValue,channelAUncertainty,channelBValue,channelBUncertainty,channelCValue,channelCUncertainty,channelDValue,channelDUncertainty):
        """
        Captures and processes a new set of measurement values emitted via signal, updating the UI and internal data structures.

        This function is connected to a QSignal from the background worker thread and is responsible for handling a single measurement cycle. It validates the presence of data, provides real-time user feedback when no measurements are detected for specific channels, updates plots with valid values, populates the measurement table, and refreshes visual labels.

        This function performs the following actions:
        - Checks for zero values in any channel and informs the user if one or more channels are not receiving valid measurements.
        - Updates the status bar and color indicator depending on whether all channels are acquiring data.
        - Appends valid count values and timestamps to the corresponding lists for each channel.
        - Updates the graphical curves for each channel if valid data is present.
        - Converts zero and -1 values into status messages like "Low Counts" or "Not Selected" for display purposes.
        - Adds the latest measurement row to both the main table (`tableCounts`) and its clone (`cloneTable`).
        - Updates the live count and uncertainty labels for any actively selected channel.
        - Refreshes the visible X-axis range of the graphs using `updateGraphic()`.

        :param secondsTime: Timestamp in seconds since measurement start (float).
        :param dateTime: Human-readable datetime string for the measurement (str).
        :param channelAValue: Count value for channel A (float or int).
        :param channelAUncertainty: Uncertainty value for channel A (float).
        :param channelBValue: Count value for channel B (float or int).
        :param channelBUncertainty: Uncertainty value for channel B (float).
        :param channelCValue: Count value for channel C (float or int).
        :param channelCUncertainty: Uncertainty value for channel C (float).
        :param channelDValue: Count value for channel D (float or int).
        :param channelDUncertainty: Uncertainty value for channel D (float).
        :return: None
        """
        channelsWithoutMeasurements=[]
        #Manage status
        if channelAValue==0:
            channelsWithoutMeasurements.append("A")
        if channelBValue==0:
            channelsWithoutMeasurements.append("B")
        if channelCValue==0:
            channelsWithoutMeasurements.append("C")
        if channelDValue==0:
            channelsWithoutMeasurements.append("D")
        
        if len(channelsWithoutMeasurements)==0:
            self.changeStatusColor(1)
            self.changeStatusLabel("Running measurement")
        else:
            channelString=', '.join(channelsWithoutMeasurements)
            self.changeStatusColor(3)
            if len(channelsWithoutMeasurements)==1:
                self.changeStatusLabel(f"The channnel {channelString} is not taking measurements")
            else:
                self.changeStatusLabel(f"The channnels {channelString} are not taking measurements")
                
            
            
        #Add values in table
        #Channel A
        
        if channelAValue!=0 and channelAValue!=-1:
            channelAValue=round(channelAValue,5)
            channelAUncertainty= round(channelAUncertainty,5)
            self.timestampsChannelA.append(secondsTime)
            self.timestampsDateChannelA.append(dateTime)
            self.channelAValues.append(channelAValue)
            self.channelAUncertainties.append(channelAUncertainty)
            self.curveCountsA.setData(self.timestampsChannelA, self.channelAValues)
            channelAValue=f"{channelAValue:.5f}"
            channelAUncertainty=f"{channelAUncertainty:.5f}"
        elif channelAValue==0:
            channelAValue="Low Counts"
            channelAUncertainty="Low Counts"
        elif channelAValue == -1:
            channelAValue="Not Selected"
            channelAUncertainty="Not Selected"
        #Channel B
        if channelBValue!=0 and channelBValue!=-1:
            channelBValue=round(channelBValue,5)
            channelBUncertainty= round(channelBUncertainty,5)
            self.timestampsChannelB.append(secondsTime)
            self.timestampsDateChannelB.append(dateTime)
            self.channelBValues.append(channelBValue)
            self.channelBUncertainties.append(channelBUncertainty)
            self.curveCountsB.setData(self.timestampsChannelB, self.channelBValues)
            channelBValue=f"{channelBValue:.5f}"
            channelBUncertainty=f"{channelBUncertainty:.5f}"
        elif channelBValue==0:
            channelBValue="Low Counts"
            channelBUncertainty="Low Counts"
        elif channelBValue == -1:
            channelBValue="Not Selected"
            channelBUncertainty="Not Selected"
        #Channel C
        if channelCValue!=0 and channelCValue!=-1:
            channelCValue=round(channelCValue,5)
            channelCUncertainty= round(channelCUncertainty,5)
            self.timestampsChannelC.append(secondsTime)
            self.timestampsDateChannelC.append(dateTime)
            self.channelCValues.append(channelCValue)
            self.channelCUncertainties.append(channelCUncertainty)
            self.curveCountsC.setData(self.timestampsChannelC, self.channelCValues)
            channelCValue=f"{channelCValue:.5f}"
            channelCUncertainty=f"{channelCUncertainty:.5f}"
        elif channelCValue==0:
            channelCValue="Low Counts"
            channelCUncertainty="Low Counts"
        elif channelCValue == -1:
            channelCValue="Not Selected"
            channelCUncertainty="Not Selected"
        #Channel D
        if channelDValue!=0 and channelDValue!=-1:
            channelDValue=round(channelDValue,5)
            channelDUncertainty= round(channelDUncertainty,5)
            self.timestampsChannelD.append(secondsTime)
            self.timestampsDateChannelD.append(dateTime)
            self.channelDValues.append(channelDValue)
            self.channelDUncertainties.append(channelDUncertainty)
            self.curveCountsD.setData(self.timestampsChannelD, self.channelDValues)
            channelDValue=f"{channelDValue:.5f}"
            channelDUncertainty=f"{channelDUncertainty:.5f}"
        elif channelDValue==0:
            channelDValue="Low Counts"
            channelDUncertainty="Low Counts"
        elif channelDValue == -1:
            channelDValue="Not Selected"
            channelDUncertainty="Not Selected"
        
        
        newData=[dateTime,channelAValue,channelBValue,channelCValue,channelDValue]
        self.tableCounts.insertRow(0)
        self.cloneTable.insertRow(0)
        for col, value in enumerate(newData):
            self.tableCounts.setItem(0, col, self.rightAlignedItem(value))
            self.cloneTable.setItem(0, col, self.rightAlignedItem(value))
        #Update values to label
        if self.channelACheckBox.isChecked():
            self.updateLabels("A",channelAValue, channelAUncertainty)
        if self.channelBCheckBox.isChecked():
            self.updateLabels("B",channelBValue, channelBUncertainty)
        if self.channelCCheckBox.isChecked():
            self.updateLabels("C",channelCValue, channelCUncertainty)
        if self.channelDCheckBox.isChecked():
            self.updateLabels("D",channelDValue, channelDUncertainty)
        
        self.updateGraphic()
            
        
    def rightAlignedItem(self,value):
        """
        Creates a QTableWidgetItem with right-aligned and vertically centered text.

        This function takes a value, converts it to a string, wraps it in a QTableWidgetItem,
        and sets the text alignment to align the content to the right and center it vertically.
        It is used to ensure consistent formatting of numerical or textual data in table cells.

        :param value: The value to be displayed in the table cell.
        :type value: Any
        :return: A QTableWidgetItem with the specified alignment.
        :rtype: QTableWidgetItem
        """
        item = QTableWidgetItem(str(value))
        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return item

    def updateLabels(self, channel, value, uncertainty):
        """
        Updates the UI labels displaying the latest measurement value and its uncertainty for the specified channel.

        This function formats and sets the value and uncertainty labels for a given channel (A–D). If the value is a string (e.g., "Low Counts" or "Not Selected"), it is displayed as-is. If it is a numeric value, the function rounds it for clearer presentation before updating the corresponding labels.

        This function performs the following actions:
        - Determines if the value is a string or numeric.
        - Rounds numeric values (value to 2 decimals, uncertainty to 5 decimals).
        - Updates the `QLabel` elements associated with the selected channel to reflect the latest measurement results.

        :param channel: The target channel identifier ('A', 'B', 'C', or 'D').
        :param value: The most recent measured value (float, int, or str).
        :param uncertainty: The associated uncertainty of the measurement (float or str).
        :return: None
        """
        finalValue = value
        finalUncertainty = uncertainty
        # if value=="Low Counts":
        #     finalValue=value
        #     finalUncertainty=uncertainty
        # elif value=="Not Selected":
        #     finalValue=value
        #     finalUncertainty=uncertainty
        # else:    
        #     finalValue=round(value,2)
        #     finalUncertainty=round(uncertainty,5)
        if channel=="A":    
            self.countChannelAValue.setText(f"A: {finalValue}")
            self.countChannelAUncertainty.setText(f"{finalUncertainty}")
            self.countChannelAValueClone.setText(f"A: {finalValue}")
            self.countChannelAUncertaintyClone.setText(f"{finalUncertainty}")
        elif channel=="B":
            self.countChannelBValue.setText(f"B: {finalValue}")
            self.countChannelBUncertainty.setText(f"{finalUncertainty}")
            self.countChannelBValueClone.setText(f"B: {finalValue}")
            self.countChannelBUncertaintyClone.setText(f"{finalUncertainty}")
        elif channel=="C":
            self.countChannelCValue.setText(f"C: {finalValue}")
            self.countChannelCUncertainty.setText(f"{finalUncertainty}")
            self.countChannelCValueClone.setText(f"C: {finalValue}")
            self.countChannelCUncertaintyClone.setText(f"{finalUncertainty}")
        elif channel=="D":
            self.countChannelDValue.setText(f"D: {finalValue}")
            self.countChannelDUncertainty.setText(f"{finalUncertainty}")
            self.countChannelDValueClone.setText(f"D: {finalValue}")
            self.countChannelDUncertaintyClone.setText(f"{finalUncertainty}")
    
    
    
    
    def closeDialogChannels(self, channel):
        """
        Handles cleanup and UI updates when a detached graphics dialog is closed.

        This function is triggered when a user manually closes a detached dialog window corresponding to a specific channel. It clears the internal reference to the dialog and unchecks the associated channel checkbox to reflect that the channel is no longer active in the detached view.

        This function performs the following actions:
        - Sets the corresponding `dialogXCreated` variable to `None`, where X is the channel (A–D).
        - Unchecks the checkbox for the specified channel to visually indicate it is no longer selected.

        :param channel: The identifier of the channel whose dialog was closed ('A', 'B', 'C', or 'D').
        :return: None
        """
        if channel == "A":
            self.dialogACreated=None
            self.channelACheckBox.setChecked(False)
        elif channel == "B":
            self.dialogBCreated=None
            self.channelBCheckBox.setChecked(False)
        elif channel == "C":
            self.dialogCCreated=None
            self.channelCCheckBox.setChecked(False)
        elif channel == "D":
            self.dialogDCreated=None
            self.channelDCheckBox.setChecked(False)
    
    def finishedThread(self):
        """
        Handles the post-execution cleanup and UI updates when the measurement thread finishes.

        This function is automatically triggered when the background measurement thread completes. It resets internal sentinels, updates the UI to reflect the end of the measurement, enables or disables appropriate buttons depending on whether data was captured, and invokes the standard stop measurement routine.

        This function performs the following actions:
        - Resets all `selectChannelX` sentinels (A–D) to `False`.
        - Enables the Start button and disables the Stop button.
        - If any channel has collected data, enables the save buttons for data and plots.
        - Disables all "Clear" buttons for individual channels.
        - Updates the status label and color to indicate that no measurement is running.
        - Calls `stopMeasure()` to finalize the stop process and restore the interface to its initial state.

        :return: None
        """
        #Restart the sentinels
        
        self.selectChannelA=False
        self.selectChannelB=False
        self.selectChannelC=False
        self.selectChannelD=False
        #Start button enabled and stop button disabled
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        if self.timestampsChannelA or self.timestampsChannelB or self.timestampsChannelC or self.timestampsChannelD:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
        #Disable clear channels
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        self.changeStatusColor(0)
        self.changeStatusLabel("No running")
        
        
        #actions for stop button
        self.stopMeasure()
    
    #No selected channels function
    def noChannelsSelected(self):
        """
        Displays a warning dialog indicating that no channels have been selected for measurement.

        This function is called when the user attempts to start a measurement without selecting any channels. It generates a modal warning dialog to inform the user that at least one channel must be selected to proceed.

        This function performs the following actions:
        - Opens a `QMessageBox` warning with a title and informative message.
        - Prevents the measurement process from starting until the issue is resolved.

        :return: None
        """
        QMessageBox.warning(
            self.mainWindow,  
            "Not selected channels",
            "You must select at least one channel to start measurement"
        )
        
        
    
    #Function to define that no measurements were founded
    def noMeasurementsFounded(self):
        """
        Displays a warning dialog and disables channel interactions when no measurements are detected.

        This function is triggered when the system fails to obtain valid measurements from any of the selected channels. It informs the user of the issue, disables the "Clear" buttons for all channels, and resets the internal sentinels that indicate active measurement states.

        This function performs the following actions:
        - Shows a `QMessageBox` warning explaining that no measurements were found and outlines the minimum requirements for detection (e.g., 500 pulses per second).
        - Disables the "Clear" buttons for channels A–D to prevent further user interaction.
        - Resets `measurementChannelX` sentinels (A–D) to `False`, marking all channels as inactive.

        :return: None
        """
        QMessageBox.warning(
            self.mainWindow,  
            "No Measurements Found",
            "Unable to obtain a measurement in any of the selected channels: At least 500 pulses per second are required to estimate the counts in each channel. That is, two consecutive stops are needed after a start within a 4 ms window"
        )
        self.clearButtonChannelA.setEnabled(False)
        self.clearButtonChannelB.setEnabled(False)
        self.clearButtonChannelC.setEnabled(False)
        self.clearButtonChannelD.setEnabled(False)
        #Reset measurements
        self.measurementChannelA=False
        self.measurementChannelB=False
        self.measurementChannelC=False
        self.measurementChannelD=False
    
    #Function to eliminate channels where there is no measurements
    def eliminateCheckBoxChannels(self, channelList):
        """
        Handles the removal of channels with insufficient measurement signals and prompts the user to continue or stop.

        This function is triggered when one or more selected channels fail to meet the minimum pulse requirements for reliable count estimation (e.g., fewer than 500 pulses per second). It presents a dialog informing the user about the affected channels and asks whether to continue the measurement with the remaining valid channels or to stop entirely.

        This function performs the following actions:
        - Builds a human-readable list of the channels that failed to provide sufficient data.
        - Displays a warning dialog with the option to continue or cancel the measurement.
        - If the user chooses to continue:
            - Disables the affected channels in the device.
            - Unchecks and disables the associated checkboxes.
            - Disables the "Clear" button for each affected channel.
            - Marks the `measurementChannelX` sentinel as `False` for each affected channel.
        - If the user chooses not to continue:
            - Stops the measurement thread.
        - Signals the worker thread to proceed based on the user's decision via `continueEvent`.

        :param channelList: A list of channel identifiers (e.g., ['A', 'C']) that failed to meet the minimum measurement conditions.
        :return: None
        """
        newChannelList=[]
        for i in channelList:
            newValues="Channel "+i
            newChannelList.append(newValues)
        if newChannelList:
            channelStr = ", ".join(newChannelList)
            message = (
                "Unable to obtain a measurement: At least 500 pulses per second are required to estimate the counts in each channel. That is, two consecutive stops are needed after a start within a 4 ms window "
                f"in the following channels:\n\n{channelStr}\n\n"
                "Do you want to continue with the measurement?"
            )

            reply = QMessageBox.question(
                self.mainWindow,                  # Parent
                "Estimation Warning",             # Title
                message,                          # Message
                QMessageBox.Yes | QMessageBox.No, # Buttons
                QMessageBox.Yes                   # Default
            )

            for channelValue in channelList:
                if channelValue == "A":
                    self.device.ch1.disableChannel()
                    self.channelACheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelACheckBox.setEnabled(False)
                    self.measurementChannelA=False
                    self.clearButtonChannelA.setEnabled(False)
                elif channelValue == "B":
                    self.device.ch2.disableChannel()
                    self.channelBCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelBCheckBox.setEnabled(False)
                    self.measurementChannelB=False
                    self.clearButtonChannelB.setEnabled(False)
                elif channelValue == "C":
                    self.device.ch3.disableChannel()
                    self.channelCCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelCCheckBox.setEnabled(False)
                    self.measurementChannelC=False
                    self.clearButtonChannelC.setEnabled(False)
                elif channelValue == "D":
                    self.device.ch4.disableChannel()
                    self.channelDCheckBox.setChecked(False)
                    QApplication.processEvents()
                    self.channelDCheckBox.setEnabled(False)
                    self.measurementChannelD=False
                    self.clearButtonChannelD.setEnabled(False)

            # Continuar o parar según respuesta
            self.worker.continueEvent.set()

            if reply == QMessageBox.No:
                self.worker.stop()
    
    def deatachedTable(self):
        """
        Manages the visibility of the estimated counts table in a detached dialog window.

        This function is triggered when the `deatachedCheckBox` is toggled. If the checkbox is checked, it opens a new non-modal `QDialog` containing the cloned measurement table (`cloneTable`). If the checkbox is unchecked, it closes the dialog and resets the internal reference to `None`.

        This function performs the following actions:
        - If the detached table mode is enabled:
            - Creates and configures a new `QDialog` with the cloned table.
            - Displays the dialog to the user.
            - Connects the dialog's close event to a cleanup function.
        - If the detached table mode is disabled:
            - Closes the existing dialog if it is open.
            - Clears the internal dialog reference.

        :return: None
        """
        if self.deatachedCheckBox.isChecked():
            self.dialogTableOpen = QDialog(self.mainWindow)
            self.dialogTableOpen.setWindowTitle(f"Estimated counts Table")
            self.dialogTableOpen.resize(530, 400)
            self.dialogTableOpen.setModal(False)
            layoutDialogTable= QVBoxLayout(self.dialogTableOpen)
            layoutDialogTable.addWidget(self.cloneTable)
            self.dialogTableOpen.show()
            self.dialogTableOpen.finished.connect(lambda _: self.closeTableDialog())
        else:
            if self.dialogTableOpen:
                self.dialogTableOpen.close()
                self.dialogTableOpen=None
    
    def detachedLabels(self):
        """
        Displays or hides a dialog showing current measurement values for selected channels.

        When the 'Detached current measurement' checkbox is checked, this function creates 
        and displays a non-modal QDialog containing the current estimated count rates 
        and their uncertainties for each selected channel (A–D). Each visible row in the 
        dialog corresponds to a channel, displaying the estimated counts (in cps) and the 
        associated uncertainty. If a channel is not selected, its row remains hidden.

        The dialog layout is organized using a sunken panel-style QFrame with a vertical 
        layout. A bold header row indicates the meaning of each column. This interface 
        allows users to quickly inspect the most recent count values without modifying the 
        ongoing measurement.

        If the checkbox is unchecked, any open measurement dialog is closed automatically.

        :return: None
        """
        if self.detachedLabelCheckBox.isChecked():
            self.dialogLabelOpen = QDialog(self.mainWindow)
            self.dialogLabelOpen.setWindowTitle("Current measurements values")
            self.dialogLabelOpen.setModal(False)

            
            frame = QFrame()
            frame.setFrameShape(QFrame.Panel)
            frame.setFrameShadow(QFrame.Sunken)

            
            frameLayout = QVBoxLayout()

            
            headerLayout = QHBoxLayout()

            
            titleFont = QFont()
            titleFont.setPointSize(12)
            titleFont.setBold(True)

            
            labelCounts = QLabel("Est. counts (cps)")
            labelUncertainty = QLabel("Uncertainty")
            labelCounts.setFont(titleFont)
            labelUncertainty.setFont(titleFont)

            # Alinear a la derecha
            labelCounts.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            labelUncertainty.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            headerLayout.addWidget(labelCounts)
            headerLayout.addWidget(labelUncertainty)
            frameLayout.addLayout(headerLayout)
            
            self.channelAFrameLabelClone=self.createRow(self.countChannelAValueClone, self.countChannelAUncertaintyClone)
            self.channelBFrameLabelClone=self.createRow(self.countChannelBValueClone, self.countChannelBUncertaintyClone)
            self.channelCFrameLabelClone=self.createRow(self.countChannelCValueClone, self.countChannelCUncertaintyClone)
            self.channelDFrameLabelClone=self.createRow(self.countChannelDValueClone, self.countChannelDUncertaintyClone)
            frameLayout.addWidget(self.channelAFrameLabelClone)
            frameLayout.addWidget(self.channelBFrameLabelClone)
            frameLayout.addWidget(self.channelCFrameLabelClone)
            frameLayout.addWidget(self.channelDFrameLabelClone)
            if not self.channelACheckBox.isChecked():
                self.channelAFrameLabelClone.setVisible(False)
            if not self.channelBCheckBox.isChecked():
                self.channelBFrameLabelClone.setVisible(False)
            if not self.channelCCheckBox.isChecked():
                self.channelCFrameLabelClone.setVisible(False)
            if not self.channelDCheckBox.isChecked():
                self.channelDFrameLabelClone.setVisible(False)

            frame.setLayout(frameLayout)

            # Agregar al layout principal
            mainLayout = QVBoxLayout()
            mainLayout.addWidget(frame)

            self.dialogLabelOpen.setLayout(mainLayout)
            self.dialogLabelOpen.resize(400, 300)
            self.dialogLabelOpen.show()
            self.dialogLabelOpen.finished.connect(lambda _: self.closeLabelDialog())
        else:
            if self.dialogLabelOpen:
                self.dialogLabelOpen.close()
                self.dialogLabelOpen = None
        
        
    def createRow(self, leftLabel, rightLabel):
        """
        Creates a horizontal row frame containing two labels.

        This function constructs a `QFrame` that represents a single row in a dialog or panel.
        It arranges two given `QLabel` widgets — one aligned to the left and the other to the right —
        using a `QHBoxLayout`. The labels are styled with a consistent font size and the vertical
        margins are removed to minimize vertical spacing between rows.

        This method is used to visually structure measurement data (such as estimated counts and uncertainties)
        in a clean, compact format.

        :param leftLabel: QLabel - The label to place on the left side of the row.
        :param rightLabel: QLabel - The label to place on the right side of the row.
        :return: QFrame - A frame containing the two labels arranged horizontally.
        """
        
        row = QFrame()
        rowLayout = QHBoxLayout()

        left, _, right, _ = rowLayout.getContentsMargins()
        rowLayout.setContentsMargins(left, 0, right, 0)
        rowLayout.setSpacing(10)

        font = QFont()
        font.setPointSize(14)

        leftLabel.setFont(font)
        rightLabel.setFont(font)

        # Alinear texto a la derecha
        leftLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        rightLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        rowLayout.addWidget(leftLabel)
        rowLayout.addWidget(rightLabel)
        row.setLayout(rowLayout)
        return row
    
    
    def closeLabelDialog(self):
        """
        Resets the dialog state and unchecks the measurement label checkbox
        if the dialog was closed while still marked as active.
        
        :return: None
        """
        
        if self.detachedLabelCheckBox.isChecked():
            self.dialogLabelOpen=None
            self.detachedLabelCheckBox.setChecked(False)
            
            
                
            
        
        
    def closeTableDialog(self):
        """
        Handles cleanup when the detached table dialog is closed.

        This function is triggered when the detached table dialog (`dialogTableOpen`) is closed by the user.
        It performs the following actions to maintain consistency in the UI state:
        
        - Sets the internal dialog reference `dialogTableOpen` to `None`.
        - Unchecks the `deatachedCheckBox` to reflect that the detached view is no longer active.

        This ensures that the application's interface remains synchronized and avoids inconsistencies
        when reopening or reattaching the measurement table view.

        :return: None
        """
        if self.deatachedCheckBox.isChecked():
            self.dialogTableOpen=None
            self.deatachedCheckBox.setChecked(False)
           

    def changeStatusLabel(self,textValue):
        """
        Updates the status label with a new message.

        This function sets the text of the `statusLabel` widget to the given string.
        It is used throughout the application to inform the user of the current 
        measurement status, errors, warnings, or progress.

        :param textValue: str - The message to display in the status label.
        :return: None
        """
        self.statusLabel.setText(textValue)
    

    
        #Function to change the color of point measurement
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
        pixmap = QPixmap(self.pointStatusLabel.size())
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
        point_size = min(self.pointStatusLabel.width(), self.pointStatusLabel.height()) // 2
        x = (self.pointStatusLabel.width() - point_size) // 2
        y = (self.pointStatusLabel.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.pointStatusLabel.setPixmap(pixmap)




#Save plots
    def savePlots(self):
        """
        Saves the current plots in the selected image format.

        This method opens a dialog for the user to select an image format (PNG, TIFF, or JPG) 
        and saves the plots for channels A, B, C, and D if their respective flags are set to True. 
        The plots are saved with a timestamp in the specified format in the default folder path.

        :return: None
        """
        try:
            graph_names=[]
            #Open select the format
            dialog = QDialog(self.mainWindow)
    
            dialog.setObjectName("ImageFormat")
            dialog.resize(282, 105)
            dialog.setWindowTitle("Save plots")
            
            #pixmap = QIcon("./Sources/tausand_small.ico")
            
            #dialog.setWindowIcon()
            
            verticalLayout_2 = QVBoxLayout(dialog)
            verticalLayout_2.setObjectName("verticalLayout_2")
            
            VerticalImage = QVBoxLayout()
            VerticalImage.setObjectName("VerticalImage")
            
            graphicsToSaveLabel=QLabel("Only the current plots with the current view will be saved.")

            VerticalImage.addWidget(graphicsToSaveLabel)
            
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
                
                if self.channelACheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    
                    winCopy, plotCopy, curveCopy = self.factoryGraphChannels("A")
                    curveCopy.setData(self.timestampsChannelA, self.channelAValues)
                    x_range, y_range = self.plotCountsA.viewRange()
                    plotCopy.setXRange(x_range[0], x_range[1])
                    plotCopy.setYRange(y_range[0], y_range[1])
                    plotCopy.getAxis('left').setWidth(80)  
                    plotCopy.setAspectLocked(False)
                    QApplication.processEvents()
                    exporter = pg.exporters.ImageExporter(winCopy.scene())
                    exporter.parameters()['width'] = 1200
                    exporter.parameters()['height'] = 800
                    folder_path = self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date = datetime.now()
                    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name = 'Counts_ChannelA' + current_date_str
                    output_path = os.path.join(folder_path, f'{graph_name}.{selected_format}')
                    exporter.export(output_path)
                    graph_names.append(graph_name)
                    
                if self.channelBCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    winCopy, plotCopy, curveCopy = self.factoryGraphChannels("B")
                    curveCopy.setData(self.timestampsChannelB, self.channelBValues)
                    x_range, y_range = self.plotCountsB.viewRange()
                    plotCopy.setXRange(x_range[0], x_range[1])
                    plotCopy.setYRange(y_range[0], y_range[1])
                    plotCopy.getAxis('left').setWidth(80)  
                    plotCopy.setAspectLocked(False)
                    QApplication.processEvents()
                    exporter = pg.exporters.ImageExporter(winCopy.scene())
                    exporter.parameters()['width'] = 1400
                    exporter.parameters()['height'] = 1000
                    folder_path = self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date = datetime.now()
                    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name = 'Counts_ChannelB' + current_date_str
                    output_path = os.path.join(folder_path, f'{graph_name}.{selected_format}')
                    exporter.export(output_path)
                    graph_names.append(graph_name)
                if self.channelCCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    winCopy, plotCopy, curveCopy = self.factoryGraphChannels("C")
                    curveCopy.setData(self.timestampsChannelC, self.channelCValues)
                    x_range, y_range = self.plotCountsC.viewRange()
                    plotCopy.setXRange(x_range[0], x_range[1])
                    plotCopy.setYRange(y_range[0], y_range[1])
                    plotCopy.getAxis('left').setWidth(80)  
                    plotCopy.setAspectLocked(False)
                    QApplication.processEvents()
                    exporter = pg.exporters.ImageExporter(winCopy.scene())
                    exporter.parameters()['width'] = 1400
                    exporter.parameters()['height'] = 1000
                    folder_path = self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date = datetime.now()
                    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name = 'Counts_ChannelC' + current_date_str
                    output_path = os.path.join(folder_path, f'{graph_name}.{selected_format}')
                    exporter.export(output_path)
                    graph_names.append(graph_name)
                if self.channelDCheckBox.isChecked() and (self.separateGraphics.isChecked() or self.deatachedGraphics.isChecked()):
                    winCopy, plotCopy, curveCopy = self.factoryGraphChannels("D")
                    curveCopy.setData(self.timestampsChannelD, self.channelDValues)
                    x_range, y_range = self.plotCountsD.viewRange()
                    plotCopy.setXRange(x_range[0], x_range[1])
                    plotCopy.setYRange(y_range[0], y_range[1])
                    plotCopy.getAxis('left').setWidth(80)  
                    plotCopy.setAspectLocked(False)
                    QApplication.processEvents()
                    exporter = pg.exporters.ImageExporter(winCopy.scene())
                    exporter.parameters()['width'] = 1400
                    exporter.parameters()['height'] = 1000
                    folder_path = self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date = datetime.now()
                    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name = 'Counts_ChannelD' + current_date_str
                    output_path = os.path.join(folder_path, f'{graph_name}.{selected_format}')
                    exporter.export(output_path)
                    graph_names.append(graph_name)
                if self.mergeGraphics.isChecked():
                    winCopy, plotCopy, curveACopy,curveBCopy,curveCCopy, curveDCopy = self.factoryGraphsAllChannels()
                    curveACopy.setData(self.timestampsChannelA, self.channelAValues)
                    curveBCopy.setData(self.timestampsChannelB, self.channelBValues)
                    curveCCopy.setData(self.timestampsChannelC, self.channelCValues)
                    curveDCopy.setData(self.timestampsChannelD, self.channelDValues)
                    x_range, y_range = self.plotCountsA.viewRange()
                    plotCopy.setXRange(x_range[0], x_range[1])
                    plotCopy.setYRange(y_range[0], y_range[1])
                    plotCopy.getAxis('left').setWidth(80)  
                    plotCopy.setAspectLocked(False)
                    QApplication.processEvents()
                    exporter = pg.exporters.ImageExporter(winCopy.scene())
                    exporter.parameters()['width'] = 1400
                    exporter.parameters()['height'] = 1000
                    folder_path = self.savefile.read_default_data()['Folder path'].replace('\n', '')
                    current_date = datetime.now()
                    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
                    graph_name = 'Counts_AllChannels' + current_date_str
                    output_path = os.path.join(folder_path, f'{graph_name}.{selected_format}')
                    exporter.export(output_path)
                    graph_names.append(graph_name)
                message_box = QMessageBox(self.mainWindow)
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
            message_box = QMessageBox(self.mainWindow)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The graphics could not be saved, check the folder path or system files")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()


    def captureInitalDate(self,date):
        """
        Stores the initial date received from a signal.

        :param date: QDateTime - The start date of the measurement range.
        :return: None
        """
        self.initialDate=date
    
    def captureFinalDate(self,date):
        """
        Stores the final date received from a signal.

        :param date: QDateTime - The end date of the measurement range.
        :return: None
        """
        self.finalDate=date
    
    
    def saveData(self):
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
        
        data_prefix="CountsEstimated"
        current_date=datetime.now()
        current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
        #Init filenames and data list
        filenames=[]
        data=[]
        dataUncertainties=[]
        timeStamps=[]
        settings=[]
        channels=[]
        
        #Open select the format
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
            total_condition= conditiontxt or conditioncsv or conditiondat
            if not total_condition:
                if self.measurementChannelA:
                    filename1=data_prefix+current_date_str+'channelA'
                    setting_A=f"Initial date:{self.initialDate} \nFinal date:{self.finalDate} \nThreshold Voltage: {self.thresholdVoltageSetting} \nStop Edge: {self.channelAEdgeTypeSetting} \n"
                    settings.append(setting_A)
                    filenames.append(filename1)
                    timeStamps.append(self.timestampsDateChannelA)
                    channels.append("A")
                    data.append(self.channelAValues)
                    dataUncertainties.append(self.channelAUncertainties)
                if self.measurementChannelB:
                    filename2=data_prefix+current_date_str+'channelB'
                    setting_B=f"Initial date:{self.initialDate} \nFinal date:{self.finalDate} \nThreshold Voltage: {self.thresholdVoltageSetting} \nStop Edge: {self.channelBEdgeTypeSetting} \n"
                    settings.append(setting_B)
                    filenames.append(filename2)
                    timeStamps.append(self.timestampsDateChannelB)
                    channels.append("B")
                    data.append(self.channelBValues)
                    dataUncertainties.append(self.channelBUncertainties)
                if self.measurementChannelC:
                    filename3=data_prefix+current_date_str+'channelC'
                    setting_C=f"Initial date:{self.initialDate} \nFinal date:{self.finalDate} \nThreshold Voltage: {self.thresholdVoltageSetting} \nStop Edge: {self.channelCEdgeTypeSetting} \n"
                    settings.append(setting_C)
                    filenames.append(filename3)
                    timeStamps.append(self.timestampsDateChannelC)
                    channels.append("C")
                    data.append(self.channelCValues)
                    dataUncertainties.append(self.channelCUncertainties)
                if self.measurementChannelD:
                    filename4=data_prefix+current_date_str+'channelD'
                    setting_D=f"Initial date:{self.initialDate} \nFinal date:{self.finalDate} \nThreshold Voltage: {self.thresholdVoltageSetting} \nStop Edge: {self.channelDEdgeTypeSetting} \n"
                    settings.append(setting_D)
                    filenames.append(filename4)
                    timeStamps.append(self.timestampsDateChannelD)
                    channels.append("D")
                    data.append(self.channelDValues)
                    dataUncertainties.append(self.channelDUncertainties)
                folder_path=self.savefile.read_default_data()['Folder path']
                
                try:
                    
                    self.savefile.save_counts_data(timeStamps,data,dataUncertainties,filenames,folder_path,settings,selected_format,channels)
                    message_box = QMessageBox(self.mainWindow)
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
                except:
                    message_box = QMessageBox(self.mainWindow)
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setText("The changes could not be saved.")
                    message_box.setWindowTitle("Error saving")
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                
            else:
                message_box = QMessageBox(self.mainWindow)
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
    
    def lostConnection(self):
        """
        Displays a critical error message indicating that the device connection has been lost.

        This function sets the sentinel flag `disconnectedMeasurement` to True and shows
        a modal QMessageBox with a critical icon to inform the user that the connection to
        the device has been lost. The dialog must be acknowledged before continuing.

        :return: None
        """
        self.disconnectedMeasurement=True
        msg_box = QMessageBox(self.mainWindow)
        msg_box.setText("Connection with the device has been lost")
        msg_box.setWindowTitle("Connection Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def helpButtonDialog(self):
        message_box = QMessageBox(self.mainWindow)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Counts estimated Information")
        message_box.setText("To perform measurements in this window, you must connect a periodic signal to the Start input that is different from the source you want to measure. Then, connect the source you want to estimate pulses from to the Stop channels.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()
        
    
    
        
    
    
    
    
    

class WorkerThreadCountsEstimated(QThread):
    """
    This class represents a worker thread that processes Start-Stop measurements in a separate thread
    to avoid blocking the main GUI thread. It handles data acquisition from the Tempico device,
    determines the feasibility of performing measurements per channel, and continuously collects
    and emits measurement data while running.

    The thread evaluates which channels meet the minimum requirements for valid measurements
    (at least 2 stops within a 4 ms window), disables those that do not, and allows the user
    to decide whether to continue with the remaining ones.

    Signals are used extensively to communicate with the GUI, updating labels, graphs, and table data
    with real-time values or to notify when no valid measurements are possible.

    :param channelASentinel: Boolean indicating if Channel A is initially selected for measurement.
    :param channelBSentinel: Boolean indicating if Channel B is initially selected for measurement.
    :param channelCSentinel: Boolean indicating if Channel C is initially selected for measurement.
    :param channelDSentinel: Boolean indicating if Channel D is initially selected for measurement.
    :param device: The TempicoDevice instance used to perform the measurement operations.

    Signals:
        - newValue(str, float, float): Emitted with updated values for display.
        - updateLabel(str, float, float): Updates label data in the GUI.
        - newMeasurement(float, datetime, float, float, float, float, float, float, float, float): 
          Emitted with measurement data for timestamp and all channels.
        - noTotalMeasurements(): Emitted when none of the channels provide valid stop data.
        - noPartialMeasurements(list): Emitted with a list of channels that failed.
        - changeStatusText(str): Updates the status label in the GUI with custom text.
        - changeStatusColor(int): Changes the GUI status label color (e.g., green, yellow, red).
        - disconnectedDevice(): Emitted when the Tempico device becomes unreachable.
    """
    
    #One value is for the count estimated and the other is for the uncertainty
    newValue=Signal(str,float,float)
    updateLabel= Signal(str,float,float)
    #Represents date, channelAValue, channelAUncertainty, channelBValue, channelBUncertainty,channelCValue, channelCUncertainty,channelDValue, channelDUncertainty
    newMeasurement=Signal(float,datetime,float,float,float,float,float,float,float,float)
    #Signals to manage the total stops values
    noTotalMeasurements=Signal()
    noPartialMeasurements=Signal(list)
    changeStatusText=Signal(str)
    changeStatusColor=Signal(int)
    disconnectedDevice=Signal()
    initialDate=Signal(str)
    finalDate=Signal(str)
    
    
    def __init__(self, channelASentinel, channelBSentinel, channelCSentinel,channelDSentinel, device: tempico.TempicoDevice):
        super().__init__()
        #Set the values for the  thread
        self.channelASentinel= channelASentinel
        self.channelBSentinel= channelBSentinel
        self.channelCSentinel= channelCSentinel
        self.channelDSentinel= channelDSentinel
        self.device= device
        self.channelsMeasure=[]
        self.channelsWithoutMeasurements=[]
        #Set the settings for the device
        #for the moment the stops number will be set to 5
        self.enableDisableChannels()
        self.device.setNumberOfRuns(25)
        self.continueEvent=threading.Event()
        self.running=True
        self.numberStopsChannelA=0
        self.numberStopsChannelB=0
        self.numberStopsChannelC=0
        self.numberStopsChannelD=0
        
        
        
    
    #Main function
    def run(self):
        """
        Executes the thread's main loop to perform count estimations from the Tempico device.

        First, it evaluates each selected channel to determine whether valid measurements can be 
        obtained. If a channel does not meet the required threshold, it is disabled and removed 
        from the measurement process. If at least one channel is valid, the measurement process begins.

        The loop runs continuously while the thread is active, triggering measurements every second. 
        If the device becomes unresponsive or the user stops the measurement, the thread exits.

        :return: None
        """
        # self.createdSignal.emit()
        # for i in range(10):
        #     self.getMeasurements()
        #     time.sleep(1)
        
        
        #Test determine stops measurement
        for channel in self.channelsMeasure:
            self.changeStatusText.emit(f"Estimating number stops in channel {channel} 0%")
            self.changeStatusColor.emit(3)
            try:
                totalStops=self.determineStopsNumber(channel)
                if totalStops<2 and self.running:
                    if channel=="A":
                        self.channelASentinel=False
                    elif channel == "B":
                        self.channelBSentinel=False
                    elif channel == "C":
                        self.channelCSentinel=False
                    elif channel == "D":
                        self.channelDSentinel=False
                    self.channelsWithoutMeasurements.append(channel)
                else:
                    if self.running:
                        if channel=="A":
                            self.numberStopsChannelA=totalStops
                        elif channel=="B":
                            self.numberStopsChannelB=totalStops
                        elif channel=="C":
                            self.numberStopsChannelC=totalStops
                        elif channel=="D":
                            self.numberStopsChannelD=totalStops
            except:
                self.running=False
                

        if len(self.channelsWithoutMeasurements)== len(self.channelsMeasure) and self.running:
            self.noTotalMeasurements.emit()
            self.running=False

        elif self.channelsWithoutMeasurements and self.running:
            self.noPartialMeasurements.emit(self.channelsWithoutMeasurements)
            self.continueEvent.wait()
        if self.running:
            self.enableDisableChannels()
        if self.running:
            #Get the init time for measurement
            self.initialDate.emit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.initialMeasurementTime = time.time()
        while self.running:
            try:
                self.device.readIdnFromDevice()
            except:
                self.running=False
                self.disconnectedDevice.emit()
            if self.running:
                self.getMeasurements()
                time.sleep(1)
        self.finalDate.emit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            
        
    def getMeasurements(self):
        """
        Retrieves and processes the latest measurement data from the Tempico device.

        For each enabled channel, it verifies that the received data is valid, calculates 
        stop intervals based on the number of pulses received, and computes both the mean 
        and standard deviation of the intervals. These values represent the estimated count 
        and its uncertainty.

        If valid data is found, the results are emitted via a signal along with the timestamp 
        of the measurement. If no data is available, default values are emitted depending 
        on the state of each channel.

        :return: None
        """
        values=[]
        valuesB=[]
        valuesC=[]
        valuesD=[]
        measure=self.device.measure()
        if measure:
            if len(measure)!=0:
                for run in measure:
                    if self.channelASentinel:
                        if run:
                            if run[0]==1 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelA)
                               
                                values=values+intervalValues
                    if self.channelBSentinel:
                        if run:
                            if run[0]==2 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run,self.numberStopsChannelB)
                                valuesB=valuesB+intervalValues
                    
                    if self.channelCSentinel:
                        if run:
                            if run[0]==3 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelC)
                                valuesC=valuesC+intervalValues
                    
                    if self.channelDSentinel:
                        if run:
                            if run[0]==4 and run[3]!=-1 :
                                intervalValues=self.calculateIntervalWithStops(run, self.numberStopsChannelC)
                                valuesD=valuesD+intervalValues
        if len(values)>0:
            meanValue=(10**12)/mean(values)
            desvestValues=std(values)
            meanValuePs=mean(values)
            if desvestValues == 0:
                uncertaintyValue = 0
            else:
                uncertaintyValue = (desvestValues / (meanValuePs ** 2))* 1e12
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelASentinel:
                valueChannelA=meanValue
                uncertaintyChannelA=uncertaintyValue
            else:
                valueChannelA=-1
                uncertaintyChannelA=-1
        else:
            if self.channelASentinel:
                valueChannelA=0
                uncertaintyChannelA=0
            else:
                valueChannelA=-1
                uncertaintyChannelA=-1
                
            
        
        
        if len(valuesB)>0:
            meanValueB=(10**12)/mean(valuesB)
            desvestValuesB=std(valuesB)
            meanValueBPs=mean(valuesB)
            if desvestValuesB == 0:
                uncertaintyValueB = 0
            else:
                uncertaintyValueB = (desvestValuesB / (meanValueBPs ** 2))* 1e12
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelBSentinel:
                valueChannelB=meanValueB
                uncertaintyChannelB=uncertaintyValueB
            else:
                valueChannelB=-1
                uncertaintyChannelB=-1
        else:
            if self.channelBSentinel:
                valueChannelB=0
                uncertaintyChannelB=0
            else:
                valueChannelB=-1
                uncertaintyChannelB=-1

        if len(valuesC)>0:
            meanValueC=(10**12)/mean(valuesC)
            desvestValuesC=std(valuesC)
            meanValuesCPs=mean(valuesC)
            if desvestValuesC == 0:
                uncertaintyValueC = 0
            else:
                uncertaintyValueC = (desvestValuesC / (meanValuesCPs ** 2))* 1e12
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelCSentinel:
                valueChannelC=meanValueC
                uncertaintyChannelC=uncertaintyValueC
            else:
                valueChannelC=-1
                uncertaintyChannelC=-1
        else:
            if self.channelCSentinel:
                valueChannelC=0
                uncertaintyChannelC=0
            else:
                valueChannelC=-1
                uncertaintyChannelC=-1
        
        if len(valuesD)>0:
            meanValueD=(10**12)/mean(valuesD)
            desvestValuesD = np.std(valuesD)
            meanValuesDPs=mean(valuesD)
            if desvestValuesD == 0:
                uncertaintyValueD = 0
            else:
                uncertaintyValueD = (desvestValuesD / (meanValuesDPs ** 2))* 1e12
            #Send the signal to the main window
            #TODO calculate everything for all channels
            
            if self.channelDSentinel:
                valueChannelD=meanValueD
                uncertaintyChannelD=uncertaintyValueD
            else:
                valueChannelD=-1
                uncertaintyChannelD=-1
        else:
            if self.channelDSentinel:
                valueChannelD=0
                uncertaintyChannelD=0
            else:
                valueChannelD=-1
                uncertaintyChannelD=-1 
            
        currentTime = time.time()-self.initialMeasurementTime
        currentDate= datetime.now().strftime("%H:%M:%S")
        self.newMeasurement.emit(currentTime,currentDate, valueChannelA, uncertaintyChannelA, valueChannelB, uncertaintyChannelB, valueChannelC, uncertaintyChannelC, valueChannelD, uncertaintyChannelD)


    def calculateIntervalWithStops(self, currentMeasure, numberStops):
        """
        Calculates stop time intervals based on pulse timestamps from the measurement.

        The function receives a raw measurement and the expected number of stops, 
        then iteratively computes the time differences between consecutive valid 
        pulse timestamps. Each interval is converted to a frequency in Hz by 
        dividing 10^12 by the difference in timestamp units (assuming picoseconds).

        :param currentMeasure: A list containing pulse data for a single run.
        :param numberStops: The number of stop intervals expected in the measurement.
        :return: A list of frequency values (in Hz) calculated from the stop intervals.
        """
        #TODO: CHANGE RECALCULATING NUMBER OF STOPS
        tempValues=[]
        for i in range(numberStops-1):
            if currentMeasure[i+3]!=-1 and currentMeasure[i+4]!=-1:
                differenceValue=currentMeasure[i+4]-currentMeasure[i+3]
                tempValues.append(differenceValue)
        
        return tempValues
    
    
    #TODO: DETERMINE THE NUMBER OF STOPS TO PERFORM THE MEASUREMENTS
    def determineStopsNumber(self, channelTest):
        """
        Determines the optimal number of stop pulses for a given channel to ensure valid measurements.

        This function tests different stop configurations by progressively reducing the number of 
        required stop pulses (from 5 down to 2). For each configuration, it performs multiple test 
        measurements and checks if at least half of them return valid data. If a configuration with 
        sufficient measurements is found, it is returned. If none meet the condition, 1 is returned 
        by default. If the thread is stopped during execution, the process halts.

        :param channelTest: A string indicating the channel to test ("A", "B", "C", or "D").
        :return: An integer representing the number of stop pulses that reliably produce measurements.
        """
        #Disable all channels
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        ##-------------------
        ##Enable only the tested channel
        if channelTest == "A":
            self.device.ch1.enableChannel()
            channel=self.device.ch1
        elif channelTest == "B":
            self.device.ch2.enableChannel()
            channel=self.device.ch2
        elif channelTest == "C":
            self.device.ch3.enableChannel()
            channel=self.device.ch3
        elif channelTest == "D":
            self.device.ch4.enableChannel()
            channel=self.device.ch4
        ##--------------------
            
        #Pre settings for determine stop number
        self.device.setNumberOfRuns(1)
        channel.setMode(2)
        ##-------------
        valuePercent=round(100/80,2)
        stopsInMeasure=5
        stopsFounded=False
        totalIterations=20
        #This number is arbitrary in order to determine how many measurements are necessary for determine the stop number
        while(stopsInMeasure>=2 and (not stopsFounded) and self.running):
            
            channel.setNumberOfStops(stopsInMeasure)
            totalMeasurements=0
            for i in range(totalIterations):
                try:
                    self.device.readIdnFromDevice()
                except:
                    self.running=False
                    self.disconnectedDevice.emit()
                if not self.running:
                    break
                self.changeStatusText.emit(f"Estimating number stops in channel {channelTest} {valuePercent}%")
                valuePercent+=100/80
                valuePercent=round(valuePercent,2)    
                measurements=self.device.measure()
                if measurements:
                    if measurements[0]:
                        if measurements[0][3] != -1:
                            totalMeasurements+=1
            if totalMeasurements>totalIterations/2:
                stopsFounded=True
            else:
                stopsInMeasure-=1
        if self.running:
            self.changeStatusText.emit(f"Estimating number stops in channel {channelTest} 100%")
            time.sleep(1)
        
        return stopsInMeasure
        
    
    def enableDisableChannels(self):
        """
        Enables or disables device channels based on active measurement sentinels.

        This function disables all channels initially, then enables only the selected ones based on 
        the sentinel flags. It configures each enabled channel with a default stop mask and averaging 
        settings, and adds them to the list of channels to be measured. This reduces processing time 
        by avoiding unnecessary measurements from inactive channels.

        :return: None
        """
        self.device.ch1.disableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()
        if self.channelASentinel:
            self.channelsMeasure.append("A")
            self.device.ch1.enableChannel()
            self.device.ch1.setStopMask(0)
            self.device.ch1.setAverageCycles(1)
        if self.channelBSentinel:
            self.channelsMeasure.append("B")
            self.device.ch2.enableChannel()
            self.device.ch2.setStopMask(0)
            self.device.ch2.setAverageCycles(1)            
        if self.channelCSentinel:
            self.channelsMeasure.append("C")
            self.device.ch3.enableChannel()
            self.device.ch3.setStopMask(0)
            self.device.ch3.setAverageCycles(1)
        if self.channelDSentinel:
            self.channelsMeasure.append("D")
            self.device.ch4.enableChannel()
            self.device.ch4.setStopMask(0)
            self.device.ch4.setAverageCycles(1)
        self.device.ch1.setMode(2)
        self.device.ch2.setMode(2)
        self.device.ch3.setMode(2)
        self.device.ch4.setMode(2)
        
    @Slot()   
    def stop(self):
        """
        Stops the measurement process by setting the running sentinel to False.

        This function is typically called from the GUI when the user requests to stop the measurement. 
        Once the sentinel is set to False, the running loop in the thread will exit, effectively 
        terminating the background measurement process.

        :return: None
        """
        self.running=False
        