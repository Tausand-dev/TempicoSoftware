# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StarStopHistogramXTzvUu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *
from PySide2.QtWidgets import *
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



from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys




class Ui_HistogramaStartStop(object):
    def setupUi(self, HistogramaStartStop):
        if not HistogramaStartStop.objectName():
            HistogramaStartStop.setObjectName(u"HistogramaStartStop")
        HistogramaStartStop.setEnabled(True)
        HistogramaStartStop.resize(1108, 874)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistogramaStartStop.sizePolicy().hasHeightForWidth())
        HistogramaStartStop.setSizePolicy(sizePolicy)
        HistogramaStartStop.setAcceptDrops(False)
        HistogramaStartStop.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(HistogramaStartStop)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.GraphConfigurationArea = QWidget(HistogramaStartStop)
        self.GraphConfigurationArea.setObjectName(u"GraphConfigurationArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.GraphConfigurationArea.sizePolicy().hasHeightForWidth())
        self.GraphConfigurationArea.setSizePolicy(sizePolicy1)
        self.GraphConfigurationArea.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(self.GraphConfigurationArea)
        self.verticalLayout.setObjectName(u"verticalLayout")
        # self.graphicSelectFrame = QFrame(self.GraphConfigurationArea)
        # self.graphicSelectFrame.setObjectName(u"graphicSelectFrame")
        # sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sizePolicy2.setHorizontalStretch(0)
        # sizePolicy2.setVerticalStretch(1)
        # sizePolicy2.setHeightForWidth(self.graphicSelectFrame.sizePolicy().hasHeightForWidth())
        # self.graphicSelectFrame.setSizePolicy(sizePolicy2)
        # self.graphicSelectFrame.setFrameShape(QFrame.Panel)
        # self.graphicSelectFrame.setFrameShadow(QFrame.Sunken)
        # self.horizontalLayout_2 = QHBoxLayout(self.graphicSelectFrame)
        # self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        # self.LabelNumbeFrame = QFrame(self.graphicSelectFrame)
        # self.LabelNumbeFrame.setObjectName(u"LabelNumbeFrame")
        # self.LabelNumbeFrame.setFrameShape(QFrame.StyledPanel)
        # self.LabelNumbeFrame.setFrameShadow(QFrame.Raised)
        # self.horizontalLayout_3 = QHBoxLayout(self.LabelNumbeFrame)
        # self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        # self.numberGraphLabel = QLabel(self.LabelNumbeFrame)
        # self.numberGraphLabel.setObjectName(u"numberGraphLabel")
        # self.numberGraphLabel.setAutoFillBackground(False)
        # self.numberGraphLabel.setTextFormat(Qt.MarkdownText)

        # self.horizontalLayout_3.addWidget(self.numberGraphLabel)


        # self.horizontalLayout_2.addWidget(self.LabelNumbeFrame)

        # self.NumbeComboBoxFrame = QFrame(self.graphicSelectFrame)
        # self.NumbeComboBoxFrame.setObjectName(u"NumbeComboBoxFrame")
        # self.NumbeComboBoxFrame.setFrameShape(QFrame.StyledPanel)
        # self.NumbeComboBoxFrame.setFrameShadow(QFrame.Raised)
        # self.verticalLayout_2 = QVBoxLayout(self.NumbeComboBoxFrame)
        # self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        # self.GraphicsComboBox = QComboBox(self.NumbeComboBoxFrame)
        # self.GraphicsComboBox.addItem("")
        # self.GraphicsComboBox.addItem("")
        # self.GraphicsComboBox.addItem("")
        # self.GraphicsComboBox.addItem("")
        # self.GraphicsComboBox.setObjectName(u"GraphicsComboBox")

        # self.verticalLayout_2.addWidget(self.GraphicsComboBox)


        # self.horizontalLayout_2.addWidget(self.NumbeComboBoxFrame)


        # self.verticalLayout.addWidget(self.graphicSelectFrame)

        self.Graph1Configuration = QFrame(self.GraphConfigurationArea)
        self.Graph1Configuration.setObjectName(u"Graph1Configuration")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(3)
        sizePolicy3.setHeightForWidth(self.Graph1Configuration.sizePolicy().hasHeightForWidth())
        self.Graph1Configuration.setSizePolicy(sizePolicy3)
        self.Graph1Configuration.setFrameShape(QFrame.Panel)
        self.Graph1Configuration.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.Graph1Configuration)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.LabelFrameGraph1 = QFrame(self.Graph1Configuration)
        self.LabelFrameGraph1.setObjectName(u"LabelFrameGraph1")
        self.LabelFrameGraph1.setFrameShape(QFrame.StyledPanel)
        self.LabelFrameGraph1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.LabelFrameGraph1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.LabelGraph1 = QLabel(self.LabelFrameGraph1)
        self.LabelGraph1.setObjectName(u"LabelGraph1")

        self.verticalLayout_4.addWidget(self.LabelGraph1)


        self.verticalLayout_3.addWidget(self.LabelFrameGraph1)

        self.ComboBoxGraph1 = QFrame(self.Graph1Configuration)
        self.ComboBoxGraph1.setObjectName(u"ComboBoxGraph1")
        self.ComboBoxGraph1.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxGraph1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.ComboBoxGraph1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Channel1Graph1 = QCheckBox(self.ComboBoxGraph1)
        self.Channel1Graph1.setObjectName(u"Channel1Graph1")

        self.horizontalLayout_4.addWidget(self.Channel1Graph1)

        self.Channel4Graph1 = QCheckBox(self.ComboBoxGraph1)
        self.Channel4Graph1.setObjectName(u"Channel4Graph1")

        self.horizontalLayout_4.addWidget(self.Channel4Graph1)

        self.Channel2Graph1 = QCheckBox(self.ComboBoxGraph1)
        self.Channel2Graph1.setObjectName(u"Channel2Graph1")

        self.horizontalLayout_4.addWidget(self.Channel2Graph1)

        self.Channel3Graph1 = QCheckBox(self.ComboBoxGraph1)
        self.Channel3Graph1.setObjectName(u"Channel3Graph1")

        self.horizontalLayout_4.addWidget(self.Channel3Graph1)


        self.verticalLayout_3.addWidget(self.ComboBoxGraph1)

        self.HistGraph1 = QFrame(self.Graph1Configuration)
        self.HistGraph1.setObjectName(u"HistGraph1")
        self.HistGraph1.setFrameShape(QFrame.StyledPanel)
        self.HistGraph1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.HistGraph1)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")




        #Boton de start measurements

        self.SaveGraph1 = QPushButton(self.HistGraph1)
        self.SaveGraph1.setObjectName(u"SaveGraph1")

        self.horizontalLayout_11.addWidget(self.SaveGraph1)

        self.StopGraph1 = QPushButton(self.HistGraph1)
        self.StopGraph1.setObjectName(u"StopGraph1")
        #self.SaveGraph1.clicked.connect(self.stoptbutton)

        self.horizontalLayout_11.addWidget(self.StopGraph1)
        self.SaveDoc = QPushButton(self.HistGraph1)
        self.SaveDoc.setObjectName(u"SaveDoc")
        #self.SaveGraph1.clicked.connect(self.stoptbutton)

        self.horizontalLayout_11.addWidget(self.SaveDoc)


        self.verticalLayout_3.addWidget(self.HistGraph1)


        self.verticalLayout.addWidget(self.Graph1Configuration)
        
        
        
        #Buttons to create the save image and clear graphics
        
        self.HistGraphsave = QFrame(self.Graph1Configuration)
        self.HistGraphsave.setObjectName(u"HistGraphsave")
        self.HistGraphsave.setFrameShape(QFrame.StyledPanel)
        self.HistGraphsave.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.HistGraphsave)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")




        #Save first graphic (ms)

        self.SaveImage1 = QPushButton(self.HistGraphsave)
        self.SaveImage1.setObjectName(u"SaveImage1")
        self.horizontalLayout_12.addWidget(self.SaveImage1)
        
        
        
        #Clear qframe
        self.HistGraphclear = QFrame(self.Graph1Configuration)
        self.HistGraphclear.setObjectName(u"HistGraphclear")
        self.HistGraphclear.setFrameShape(QFrame.StyledPanel)
        self.HistGraphclear.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.HistGraphclear)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        
        #clear graphic 1

        self.ClearchannelA = QPushButton(self.HistGraphclear)
        self.ClearchannelA.setObjectName(u"ClearchannelA")
        self.horizontalLayout_13.addWidget(self.ClearchannelA)
        
        #clear graphic 2

        self.ClearchannelB = QPushButton(self.HistGraphclear)
        self.ClearchannelB.setObjectName(u"ClearchannelB")
        self.horizontalLayout_13.addWidget(self.ClearchannelB)
        
        #clear graphic 3

        self.ClearchannelC = QPushButton(self.HistGraphclear)
        self.ClearchannelC.setObjectName(u"ClearchannelC")
        self.horizontalLayout_13.addWidget(self.ClearchannelC)
        
        #clear graphic 4

        self.ClearchannelD = QPushButton(self.HistGraphclear)
        self.ClearchannelD.setObjectName(u"ClearchannelD")
        self.horizontalLayout_13.addWidget(self.ClearchannelD)




        self.verticalLayout_3.addWidget(self.HistGraphsave)
        self.verticalLayout_3.addWidget(self.HistGraphclear)


        self.verticalLayout.addWidget(self.Graph1Configuration)
        
        #---------Fin save image -----------------------#
        
        

        


        self.horizontalLayout.addWidget(self.GraphConfigurationArea)
        

        self.GraphicArea = QWidget(HistogramaStartStop)
        self.GraphicArea.setObjectName(u"GraphicArea")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(7)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.GraphicArea.sizePolicy().hasHeightForWidth())
        self.GraphicArea.setSizePolicy(sizePolicy4)
        self.GraphicArea.setAutoFillBackground(True)
        self.gridLayout = QGridLayout(self.GraphicArea)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Graph3 = QFrame(self.GraphicArea)
        self.Graph3.setObjectName(u"Graph3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(5)
        sizePolicy5.setVerticalStretch(5)
        sizePolicy5.setHeightForWidth(self.Graph3.sizePolicy().hasHeightForWidth())
        self.Graph3.setSizePolicy(sizePolicy5)
        self.Graph3.setFrameShape(QFrame.StyledPanel)
        self.Graph3.setFrameShadow(QFrame.Plain)
        self.gridLayout.addWidget(self.Graph3, 2, 0, 1, 1)        
        self.horizontalLayout.addWidget(self.GraphicArea)
        self.retranslateUi(HistogramaStartStop)
        QMetaObject.connectSlotsByName(HistogramaStartStop)
        self.ClearchannelA.setEnabled(False)
        self.ClearchannelB.setEnabled(False)
        self.ClearchannelC.setEnabled(False)
        self.ClearchannelD.setEnabled(False)
        self.SaveGraph1.setEnabled(False)
        self.StopGraph1.setEnabled(False)
        self.SaveDoc.setEnabled(False)
        self.SaveImage1.setEnabled(False)
        self.Channel1Graph1.setEnabled(False)
        self.Channel2Graph1.setEnabled(False)
        self.Channel3Graph1.setEnabled(False)
        self.Channel4Graph1.setEnabled(False)
    # setupUi
    #Start the animation    

    def retranslateUi(self, HistogramaStartStop):
        HistogramaStartStop.setWindowTitle(QCoreApplication.translate("HistogramaStartStop", u"Form", None))
        # self.numberGraphLabel.setText(QCoreApplication.translate("HistogramaStartStop", u"Number of graphics:", None))
        # self.GraphicsComboBox.setItemText(0, QCoreApplication.translate("HistogramaStartStop", u"1", None))
        # self.GraphicsComboBox.setItemText(1, QCoreApplication.translate("HistogramaStartStop", u"2", None))
        # self.GraphicsComboBox.setItemText(2, QCoreApplication.translate("HistogramaStartStop", u"3", None))
        # self.GraphicsComboBox.setItemText(3, QCoreApplication.translate("HistogramaStartStop", u"4", None))

        self.LabelGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Select the stop channels on which you will measure:", None))
        self.Channel1Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel A", None))
        self.Channel4Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel B", None))
        self.Channel2Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel C", None))
        self.Channel3Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel D", None))
        self.SaveGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Begin measurement", None))
        self.StopGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"End measurement", None))
        self.SaveDoc.setText(QCoreApplication.translate("HistogramaStartStop", u"Save", None))
        self.SaveImage1.setText(QCoreApplication.translate("HistogramaStartStop", u"Save Plots", None))
        self.ClearchannelA.setText(QCoreApplication.translate("HistogramaStartStop", u"Clear A", None))
        self.ClearchannelB.setText(QCoreApplication.translate("HistogramaStartStop", u"Clear B", None))
        self.ClearchannelC.setText(QCoreApplication.translate("HistogramaStartStop", u"Clear C", None))
        self.ClearchannelD.setText(QCoreApplication.translate("HistogramaStartStop", u"Clear D", None))
        
    # retranslateUi

#Create graphic design#




class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_HistogramaStartStop()
        self.ui.setupUi(self)

        # Ajustar la política de tamaño del área de configuración
        self.ui.GraphConfigurationArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Agregar el área de configuración al layout central del widget principal
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self.ui.GraphConfigurationArea)
        layout.addWidget(self.ui.GraphicArea)
        self.setCentralWidget(central_widget)
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UI()
    win.show()
    app.exec_()

