from PySide2.QtCore import QTimer, QTime, Qt, QMetaObject, QThread, Signal, Slot
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QComboBox, QFrame, QPushButton, QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QDialog, QVBoxLayout, QFormLayout, QDoubleSpinBox, QRadioButton, QTabWidget, QWidget, QGridLayout, QSizePolicy
import pyqtgraph as pg
from numpy import mean, sqrt, exp, array, sum, arange, histogram, linspace
from numpy import append as appnd
from createsavefile import createsavefile as savefile
import datetime
from scipy.optimize import curve_fit
import math
import re
from pyqtgraph.exporters import ImageExporter
import pyTempico as tempico
class CountEstimatedLogic():
    def __init__(self,channelACheckBox: QComboBox, channelBCheckBox: QComboBox, channelCCheckBox: QComboBox, channelDCheckBox: QComboBox,startButon: QPushButton, stopButton: QPushButton,
                 mergeRadio: QRadioButton, separateGraphics: QRadioButton, timeRangeComboBox: QComboBox, clearButtonChannelA:QPushButton, clearButtonChannelB:QPushButton, clearButtonChannelC:QPushButton, 
                 clearButtonChannelD:QPushButton, saveDataButton: QPushButton, savePlotButton: QPushButton, countChannelAValue: QLabel,countChannelBValue: QLabel,countChannelCValue: QLabel,
                 countChannelDValue: QLabel, countChannelAUncertainty: QLabel, countChannelBUncertainty: QLabel, countChannelCUncertainty: QLabel, countChannelDUncertainty: QLabel,
                 tableCounts:QTableWidget, graphicsFrame: QFrame,channelAFrameLabel: QFrame,channelBFrameLabel: QFrame,channelCFrameLabel: QFrame,channelDFrameLabel: QFrame, device, parent):
        #Get the parameters
        self.channelACheckBox = channelACheckBox
        self.channelBCheckBox = channelBCheckBox
        self.channelCCheckBox = channelCCheckBox
        self.channelDCheckBox = channelDCheckBox
        self.startButon = startButon
        self.stopButton = stopButton
        self.mergeRadio = mergeRadio
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
        self.parent = parent
        self.channelAFrameLabel=channelAFrameLabel
        self.channelBFrameLabel=channelBFrameLabel
        self.channelCFrameLabel=channelCFrameLabel
        self.channelDFrameLabel=channelDFrameLabel
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
        
        
        
        #End connection for the checkbox
        
        
        if device==None:
            self.startButon.setEnabled(False)
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
        
        if self.channelACheckBox.isChecked():
            self.channelAFrameLabel.setVisible(True)
        else:
            self.channelAFrameLabel.setVisible(False)
        
        
        if self.channelBCheckBox.isChecked():
            self.channelBFrameLabel.setVisible(True)
        else:
            self.channelBFrameLabel.setVisible(False)

        
        if self.channelCCheckBox.isChecked():
            self.channelCFrameLabel.setVisible(True)
        else:
            self.channelCFrameLabel.setVisible(False)

        if self.channelDCheckBox.isChecked():
            self.channelDFrameLabel.setVisible(True)
        else:
            self.channelDFrameLabel.setVisible(False)
        #Here we update the graphics that are shown in the interface
        self.updateGraphicsLayout()
    
    def factoryGraphChannels(self, channel):
        winCountsGraph=pg.GraphicsLayoutWidget()
        winCountsGraph.setBackground('w')
        #Add the plot to the window
        plotCounts=winCountsGraph.addPlot()
        plotCounts.showGrid(x=True, y=True)
        #Add Labels
        plotCounts.setLabel('left',f'Counts channel {channel}')
        plotCounts.setLabel('bottom','Time')
        plotCounts.addLegend()
        curve = plotCounts.plot(pen='b',  name='Counts Estimated')
        return winCountsGraph, plotCounts, curve
        
    def constructGraphicA(self):
        self.winCountsGraphA, self.plotCountsA, self.curveCountsA = self.factoryGraphChannels('A')
        
    
    def constructGraphicB(self):
        self.winCountsGraphB, self.plotCountsB, self.curveCountsB = self.factoryGraphChannels('B')
        
    
    def constructGraphicC(self):
        self.winCountsGraphC, self.plotCountsC, self.curveCountsC = self.factoryGraphChannels('C')
        
    
    def constructGraphicD(self):
        self.winCountsGraphD, self.plotCountsD, self.curveCountsD = self.factoryGraphChannels('D')
        


    #Function to update wich graphics are shown
    def updateGraphicsLayout(self):
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
        for channel, label in zip(
            [self.channelACheckBox, self.channelBCheckBox, self.channelCCheckBox, self.channelDCheckBox],
            ["A", "B", "C", "D"]
        ):
            if channel.isChecked():
                graph, _, _ = self.factoryGraphChannels(label)
                graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                selected_graphs.append(graph)

        count = len(selected_graphs)

        if count == 0:
            return  # No ocultamos el frame, solo no añadimos nada

        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        if count == 1:
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
