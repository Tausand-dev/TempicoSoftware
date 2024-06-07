# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerbkmnkm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyTempico as tempico
import math



class Ui_settings(object):
    def setupUi(self, Dialog, device):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(527, 366)
       
        self.dialog_1=Dialog
        self.device=device
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(self.frame_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.AverageCyclesChannelA = QFrame(self.tab)
        self.AverageCyclesChannelA.setObjectName(u"AverageCyclesChannelA")
        self.AverageCyclesChannelA.setFrameShape(QFrame.StyledPanel)
        self.AverageCyclesChannelA.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.AverageCyclesChannelA)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AverageCyclesLabelChannelA = QLabel(self.AverageCyclesChannelA)
        self.AverageCyclesLabelChannelA.setObjectName(u"AverageCyclesLabelChannelA")

        self.horizontalLayout.addWidget(self.AverageCyclesLabelChannelA)

        self.AverageCyclesValueA = QComboBox(self.AverageCyclesChannelA)
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.addItem("")
        self.AverageCyclesValueA.setObjectName(u"AverageCyclesValueA")

        self.horizontalLayout.addWidget(self.AverageCyclesValueA)


        self.verticalLayout_3.addWidget(self.AverageCyclesChannelA)

        self.ModeChannelA = QFrame(self.tab)
        self.ModeChannelA.setObjectName(u"ModeChannelA")
        self.ModeChannelA.setFrameShape(QFrame.StyledPanel)
        self.ModeChannelA.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.ModeChannelA)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ModeLabelChannelA = QLabel(self.ModeChannelA)
        self.ModeLabelChannelA.setObjectName(u"ModeLabelChannelA")

        self.horizontalLayout_2.addWidget(self.ModeLabelChannelA)

        self.ModeValueChannelA = QComboBox(self.ModeChannelA)
        self.ModeValueChannelA.addItem("")
        self.ModeValueChannelA.addItem("")
        self.ModeValueChannelA.setObjectName(u"ModeValueChannelA")

        self.horizontalLayout_2.addWidget(self.ModeValueChannelA)


        self.verticalLayout_3.addWidget(self.ModeChannelA)

        self.NumberStopsChannelA = QFrame(self.tab)
        self.NumberStopsChannelA.setObjectName(u"NumberStopsChannelA")
        self.NumberStopsChannelA.setFrameShape(QFrame.StyledPanel)
        self.NumberStopsChannelA.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.NumberStopsChannelA)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.NumberStopsLabelChannelA = QLabel(self.NumberStopsChannelA)
        self.NumberStopsLabelChannelA.setObjectName(u"NumberStopsLabelChannelA")

        self.horizontalLayout_3.addWidget(self.NumberStopsLabelChannelA)

        self.NumberStopsValueChannelA = QComboBox(self.NumberStopsChannelA)
        self.NumberStopsValueChannelA.addItem("")
        self.NumberStopsValueChannelA.addItem("")
        self.NumberStopsValueChannelA.addItem("")
        self.NumberStopsValueChannelA.addItem("")
        self.NumberStopsValueChannelA.addItem("")
        self.NumberStopsValueChannelA.setObjectName(u"NumberStopsValueChannelA")

        self.horizontalLayout_3.addWidget(self.NumberStopsValueChannelA)


        self.verticalLayout_3.addWidget(self.NumberStopsChannelA)

        self.EdgeTypeChannelA = QFrame(self.tab)
        self.EdgeTypeChannelA.setObjectName(u"EdgeTypeChannelA")
        self.EdgeTypeChannelA.setFrameShape(QFrame.StyledPanel)
        self.EdgeTypeChannelA.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.EdgeTypeChannelA)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.EdgeTypeLabelChannelA = QLabel(self.EdgeTypeChannelA)
        self.EdgeTypeLabelChannelA.setObjectName(u"EdgeTypeLabelChannelA")

        self.horizontalLayout_4.addWidget(self.EdgeTypeLabelChannelA)

        self.EdgeTypeValueChannelA = QComboBox(self.EdgeTypeChannelA)
        self.EdgeTypeValueChannelA.addItem("")
        self.EdgeTypeValueChannelA.addItem("")
        self.EdgeTypeValueChannelA.setObjectName(u"EdgeTypeValueChannelA")

        self.horizontalLayout_4.addWidget(self.EdgeTypeValueChannelA)


        self.verticalLayout_3.addWidget(self.EdgeTypeChannelA)

        self.StopMaskChannelA = QFrame(self.tab)
        self.StopMaskChannelA.setObjectName(u"StopMaskChannelA")
        self.StopMaskChannelA.setFrameShape(QFrame.StyledPanel)
        self.StopMaskChannelA.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.StopMaskChannelA)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.StopMaskLabelChannelA = QLabel(self.StopMaskChannelA)
        self.StopMaskLabelChannelA.setObjectName(u"StopMaskLabelChannelA")

        self.horizontalLayout_5.addWidget(self.StopMaskLabelChannelA)

        self.StopMaskValueChannelA = QSpinBox(self.StopMaskChannelA)
        self.StopMaskValueChannelA.setObjectName(u"StopMaskValueChannelA")
        self.StopMaskValueChannelA.setMaximum(4000)

        self.horizontalLayout_5.addWidget(self.StopMaskValueChannelA)


        self.verticalLayout_3.addWidget(self.StopMaskChannelA)

        self.tabWidget.addTab(self.tab, "")
        self.ChannelB = QWidget()
        self.ChannelB.setObjectName(u"ChannelB")
        self.verticalLayout_4 = QVBoxLayout(self.ChannelB)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.AverageCyclesChannelB = QFrame(self.ChannelB)
        self.AverageCyclesChannelB.setObjectName(u"AverageCyclesChannelB")
        self.AverageCyclesChannelB.setFrameShape(QFrame.StyledPanel)
        self.AverageCyclesChannelB.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.AverageCyclesChannelB)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.AverageCyclesLabelChannelB = QLabel(self.AverageCyclesChannelB)
        self.AverageCyclesLabelChannelB.setObjectName(u"AverageCyclesLabelChannelB")

        self.horizontalLayout_6.addWidget(self.AverageCyclesLabelChannelB)

        self.AverageCyclesValueB = QComboBox(self.AverageCyclesChannelB)
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.addItem("")
        self.AverageCyclesValueB.setObjectName(u"AverageCyclesValueB")

        self.horizontalLayout_6.addWidget(self.AverageCyclesValueB)


        self.verticalLayout_4.addWidget(self.AverageCyclesChannelB)

        self.ModeChannelB = QFrame(self.ChannelB)
        self.ModeChannelB.setObjectName(u"ModeChannelB")
        self.ModeChannelB.setFrameShape(QFrame.StyledPanel)
        self.ModeChannelB.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.ModeChannelB)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ModeLabelChannelB = QLabel(self.ModeChannelB)
        self.ModeLabelChannelB.setObjectName(u"ModeLabelChannelB")

        self.horizontalLayout_7.addWidget(self.ModeLabelChannelB)

        self.ModeValueChannelB = QComboBox(self.ModeChannelB)
        self.ModeValueChannelB.addItem("")
        self.ModeValueChannelB.addItem("")
        self.ModeValueChannelB.setObjectName(u"ModeValueChannelB")

        self.horizontalLayout_7.addWidget(self.ModeValueChannelB)


        self.verticalLayout_4.addWidget(self.ModeChannelB)

        self.NumberStopsChannelB = QFrame(self.ChannelB)
        self.NumberStopsChannelB.setObjectName(u"NumberStopsChannelB")
        self.NumberStopsChannelB.setFrameShape(QFrame.StyledPanel)
        self.NumberStopsChannelB.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.NumberStopsChannelB)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.NumberStopsLabelChannelB = QLabel(self.NumberStopsChannelB)
        self.NumberStopsLabelChannelB.setObjectName(u"NumberStopsLabelChannelB")

        self.horizontalLayout_8.addWidget(self.NumberStopsLabelChannelB)

        self.NumberStopsValueChannelB = QComboBox(self.NumberStopsChannelB)
        self.NumberStopsValueChannelB.addItem("")
        self.NumberStopsValueChannelB.addItem("")
        self.NumberStopsValueChannelB.addItem("")
        self.NumberStopsValueChannelB.addItem("")
        self.NumberStopsValueChannelB.addItem("")
        self.NumberStopsValueChannelB.setObjectName(u"NumberStopsValueChannelB")

        self.horizontalLayout_8.addWidget(self.NumberStopsValueChannelB)


        self.verticalLayout_4.addWidget(self.NumberStopsChannelB)

        self.EdgeTypeChannelB = QFrame(self.ChannelB)
        self.EdgeTypeChannelB.setObjectName(u"EdgeTypeChannelB")
        self.EdgeTypeChannelB.setFrameShape(QFrame.StyledPanel)
        self.EdgeTypeChannelB.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.EdgeTypeChannelB)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.EdgeTypeLabelChannelB = QLabel(self.EdgeTypeChannelB)
        self.EdgeTypeLabelChannelB.setObjectName(u"EdgeTypeLabelChannelB")

        self.horizontalLayout_9.addWidget(self.EdgeTypeLabelChannelB)

        self.EdgeTypeValueChannelB = QComboBox(self.EdgeTypeChannelB)
        self.EdgeTypeValueChannelB.addItem("")
        self.EdgeTypeValueChannelB.addItem("")
        self.EdgeTypeValueChannelB.setObjectName(u"EdgeTypeValueChannelB")

        self.horizontalLayout_9.addWidget(self.EdgeTypeValueChannelB)


        self.verticalLayout_4.addWidget(self.EdgeTypeChannelB)

        self.StopMaskChannelB = QFrame(self.ChannelB)
        self.StopMaskChannelB.setObjectName(u"StopMaskChannelB")
        self.StopMaskChannelB.setFrameShape(QFrame.StyledPanel)
        self.StopMaskChannelB.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.StopMaskChannelB)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.StopMaskLabelChannelB = QLabel(self.StopMaskChannelB)
        self.StopMaskLabelChannelB.setObjectName(u"StopMaskLabelChannelB")

        self.horizontalLayout_10.addWidget(self.StopMaskLabelChannelB)

        self.StopMaskValueChannelB = QSpinBox(self.StopMaskChannelB)
        self.StopMaskValueChannelB.setObjectName(u"StopMaskValueChannelB")
        self.StopMaskValueChannelB.setMaximum(1000)

        self.horizontalLayout_10.addWidget(self.StopMaskValueChannelB)


        self.verticalLayout_4.addWidget(self.StopMaskChannelB)

        self.tabWidget.addTab(self.ChannelB, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_5 = QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.AverageCyclesChannelC = QFrame(self.tab_2)
        self.AverageCyclesChannelC.setObjectName(u"AverageCyclesChannelC")
        self.AverageCyclesChannelC.setFrameShape(QFrame.StyledPanel)
        self.AverageCyclesChannelC.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.AverageCyclesChannelC)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.AverageCyclesLabelChannelC = QLabel(self.AverageCyclesChannelC)
        self.AverageCyclesLabelChannelC.setObjectName(u"AverageCyclesLabelChannelC")

        self.horizontalLayout_11.addWidget(self.AverageCyclesLabelChannelC)

        self.AverageCyclesValueC = QComboBox(self.AverageCyclesChannelC)
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.addItem("")
        self.AverageCyclesValueC.setObjectName(u"AverageCyclesValueC")

        self.horizontalLayout_11.addWidget(self.AverageCyclesValueC)


        self.verticalLayout_5.addWidget(self.AverageCyclesChannelC)

        self.ModeChannelC = QFrame(self.tab_2)
        self.ModeChannelC.setObjectName(u"ModeChannelC")
        self.ModeChannelC.setFrameShape(QFrame.StyledPanel)
        self.ModeChannelC.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.ModeChannelC)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.ModeLabelChannelC = QLabel(self.ModeChannelC)
        self.ModeLabelChannelC.setObjectName(u"ModeLabelChannelC")

        self.horizontalLayout_12.addWidget(self.ModeLabelChannelC)

        self.ModeValueChannelC = QComboBox(self.ModeChannelC)
        self.ModeValueChannelC.addItem("")
        self.ModeValueChannelC.addItem("")
        self.ModeValueChannelC.setObjectName(u"ModeValueChannelC")

        self.horizontalLayout_12.addWidget(self.ModeValueChannelC)


        self.verticalLayout_5.addWidget(self.ModeChannelC)

        self.NumberStopsChannelC = QFrame(self.tab_2)
        self.NumberStopsChannelC.setObjectName(u"NumberStopsChannelC")
        self.NumberStopsChannelC.setFrameShape(QFrame.StyledPanel)
        self.NumberStopsChannelC.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.NumberStopsChannelC)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.NumberStopsLabelChannelC = QLabel(self.NumberStopsChannelC)
        self.NumberStopsLabelChannelC.setObjectName(u"NumberStopsLabelChannelC")

        self.horizontalLayout_13.addWidget(self.NumberStopsLabelChannelC)

        self.NumberStopsValueChannelC = QComboBox(self.NumberStopsChannelC)
        self.NumberStopsValueChannelC.addItem("")
        self.NumberStopsValueChannelC.addItem("")
        self.NumberStopsValueChannelC.addItem("")
        self.NumberStopsValueChannelC.addItem("")
        self.NumberStopsValueChannelC.addItem("")
        self.NumberStopsValueChannelC.setObjectName(u"NumberStopsValueChannelC")

        self.horizontalLayout_13.addWidget(self.NumberStopsValueChannelC)


        self.verticalLayout_5.addWidget(self.NumberStopsChannelC)

        self.EdgeTypeChannelC = QFrame(self.tab_2)
        self.EdgeTypeChannelC.setObjectName(u"EdgeTypeChannelC")
        self.EdgeTypeChannelC.setFrameShape(QFrame.StyledPanel)
        self.EdgeTypeChannelC.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.EdgeTypeChannelC)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.EdgeTypeLabelChannelC = QLabel(self.EdgeTypeChannelC)
        self.EdgeTypeLabelChannelC.setObjectName(u"EdgeTypeLabelChannelC")

        self.horizontalLayout_14.addWidget(self.EdgeTypeLabelChannelC)

        self.EdgeTypeValueChannelC = QComboBox(self.EdgeTypeChannelC)
        self.EdgeTypeValueChannelC.addItem("")
        self.EdgeTypeValueChannelC.addItem("")
        self.EdgeTypeValueChannelC.setObjectName(u"EdgeTypeValueChannelC")

        self.horizontalLayout_14.addWidget(self.EdgeTypeValueChannelC)


        self.verticalLayout_5.addWidget(self.EdgeTypeChannelC)

        self.StopMaskChannelC = QFrame(self.tab_2)
        self.StopMaskChannelC.setObjectName(u"StopMaskChannelC")
        self.StopMaskChannelC.setFrameShape(QFrame.StyledPanel)
        self.StopMaskChannelC.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.StopMaskChannelC)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.StopMaskLabelChannelC = QLabel(self.StopMaskChannelC)
        self.StopMaskLabelChannelC.setObjectName(u"StopMaskLabelChannelC")

        self.horizontalLayout_15.addWidget(self.StopMaskLabelChannelC)

        self.StopMaskValueChannelC = QSpinBox(self.StopMaskChannelC)
        self.StopMaskValueChannelC.setObjectName(u"StopMaskValueChannelC")
        self.StopMaskValueChannelC.setMaximum(1000)

        self.horizontalLayout_15.addWidget(self.StopMaskValueChannelC)


        self.verticalLayout_5.addWidget(self.StopMaskChannelC)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_6 = QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.AverageCyclesChannelD = QFrame(self.tab_3)
        self.AverageCyclesChannelD.setObjectName(u"AverageCyclesChannelD")
        self.AverageCyclesChannelD.setFrameShape(QFrame.StyledPanel)
        self.AverageCyclesChannelD.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.AverageCyclesChannelD)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.AverageCyclesLabelChannelD = QLabel(self.AverageCyclesChannelD)
        self.AverageCyclesLabelChannelD.setObjectName(u"AverageCyclesLabelChannelD")

        self.horizontalLayout_16.addWidget(self.AverageCyclesLabelChannelD)

        self.AverageCyclesValueD = QComboBox(self.AverageCyclesChannelD)
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.addItem("")
        self.AverageCyclesValueD.setObjectName(u"AverageCyclesValueD")

        self.horizontalLayout_16.addWidget(self.AverageCyclesValueD)


        self.verticalLayout_6.addWidget(self.AverageCyclesChannelD)

        self.ModeChannelD = QFrame(self.tab_3)
        self.ModeChannelD.setObjectName(u"ModeChannelD")
        self.ModeChannelD.setFrameShape(QFrame.StyledPanel)
        self.ModeChannelD.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.ModeChannelD)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.ModeLabelChannelD = QLabel(self.ModeChannelD)
        self.ModeLabelChannelD.setObjectName(u"ModeLabelChannelD")

        self.horizontalLayout_17.addWidget(self.ModeLabelChannelD)

        self.ModeValueChannelD = QComboBox(self.ModeChannelD)
        self.ModeValueChannelD.addItem("")
        self.ModeValueChannelD.addItem("")
        self.ModeValueChannelD.setObjectName(u"ModeValueChannelD")

        self.horizontalLayout_17.addWidget(self.ModeValueChannelD)


        self.verticalLayout_6.addWidget(self.ModeChannelD)

        self.NumberStopsChannelD = QFrame(self.tab_3)
        self.NumberStopsChannelD.setObjectName(u"NumberStopsChannelD")
        self.NumberStopsChannelD.setFrameShape(QFrame.StyledPanel)
        self.NumberStopsChannelD.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.NumberStopsChannelD)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.NumberStopsLabelChannelD = QLabel(self.NumberStopsChannelD)
        self.NumberStopsLabelChannelD.setObjectName(u"NumberStopsLabelChannelD")

        self.horizontalLayout_18.addWidget(self.NumberStopsLabelChannelD)

        self.NumberStopsValueChannelD = QComboBox(self.NumberStopsChannelD)
        self.NumberStopsValueChannelD.addItem("")
        self.NumberStopsValueChannelD.addItem("")
        self.NumberStopsValueChannelD.addItem("")
        self.NumberStopsValueChannelD.addItem("")
        self.NumberStopsValueChannelD.addItem("")
        self.NumberStopsValueChannelD.setObjectName(u"NumberStopsValueChannelD")

        self.horizontalLayout_18.addWidget(self.NumberStopsValueChannelD)


        self.verticalLayout_6.addWidget(self.NumberStopsChannelD)

        self.EdgeTypeChannelD = QFrame(self.tab_3)
        self.EdgeTypeChannelD.setObjectName(u"EdgeTypeChannelD")
        self.EdgeTypeChannelD.setFrameShape(QFrame.StyledPanel)
        self.EdgeTypeChannelD.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.EdgeTypeChannelD)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.EdgeTypeLabelChannelD = QLabel(self.EdgeTypeChannelD)
        self.EdgeTypeLabelChannelD.setObjectName(u"EdgeTypeLabelChannelD")

        self.horizontalLayout_19.addWidget(self.EdgeTypeLabelChannelD)

        self.EdgeTypeValueChannelD = QComboBox(self.EdgeTypeChannelD)
        self.EdgeTypeValueChannelD.addItem("")
        self.EdgeTypeValueChannelD.addItem("")
        self.EdgeTypeValueChannelD.setObjectName(u"EdgeTypeValueChannelD")

        self.horizontalLayout_19.addWidget(self.EdgeTypeValueChannelD)


        self.verticalLayout_6.addWidget(self.EdgeTypeChannelD)

        self.StopMaskChannelD = QFrame(self.tab_3)
        self.StopMaskChannelD.setObjectName(u"StopMaskChannelD")
        self.StopMaskChannelD.setFrameShape(QFrame.StyledPanel)
        self.StopMaskChannelD.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.StopMaskChannelD)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.StopMaskLabelChannelD = QLabel(self.StopMaskChannelD)
        self.StopMaskLabelChannelD.setObjectName(u"StopMaskLabelChannelD")

        self.horizontalLayout_20.addWidget(self.StopMaskLabelChannelD)

        self.StopMaskValueChannelD = QSpinBox(self.StopMaskChannelD)
        self.StopMaskValueChannelD.setObjectName(u"StopMaskValueChannelD")
        self.StopMaskValueChannelD.setMaximum(1000)

        self.horizontalLayout_20.addWidget(self.StopMaskValueChannelD)


        self.verticalLayout_6.addWidget(self.StopMaskChannelD)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.ButtonFrame = QFrame(self.frame_2)
        self.ButtonFrame.setObjectName(u"ButtonFrame")
        self.ButtonFrame.setFrameShape(QFrame.StyledPanel)
        self.ButtonFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.ButtonFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.AplicarCambios = QPushButton(self.ButtonFrame)
        self.AplicarCambios.setObjectName(u"AplicarCambios")

        self.verticalLayout_7.addWidget(self.AplicarCambios)


        self.verticalLayout_2.addWidget(self.ButtonFrame)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(Dialog)
        self.AplicarCambios.clicked.connect(self.save_changes)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Dialog)
        
        
    
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.tab.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Tapa</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.AverageCyclesLabelChannelA.setText(QCoreApplication.translate("Dialog", u"Average cycles:", None))
        self.AverageCyclesValueA.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.AverageCyclesValueA.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.AverageCyclesValueA.setItemText(2, QCoreApplication.translate("Dialog", u"4", None))
        self.AverageCyclesValueA.setItemText(3, QCoreApplication.translate("Dialog", u"8", None))
        self.AverageCyclesValueA.setItemText(4, QCoreApplication.translate("Dialog", u"16", None))
        self.AverageCyclesValueA.setItemText(5, QCoreApplication.translate("Dialog", u"32", None))
        self.AverageCyclesValueA.setItemText(6, QCoreApplication.translate("Dialog", u"64", None))
        self.AverageCyclesValueA.setItemText(7, QCoreApplication.translate("Dialog", u"128", None))

        self.ModeLabelChannelA.setText(QCoreApplication.translate("Dialog", u"Mode:", None))
        self.ModeValueChannelA.setItemText(0, QCoreApplication.translate("Dialog", u"Mode 1 range: 12ns to 500ns", None))
        self.ModeValueChannelA.setItemText(1, QCoreApplication.translate("Dialog", u"Mode 2 range: 125ns to 4ms", None))

        self.NumberStopsLabelChannelA.setText(QCoreApplication.translate("Dialog", u"Number of stops:", None))
        self.NumberStopsValueChannelA.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.NumberStopsValueChannelA.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.NumberStopsValueChannelA.setItemText(2, QCoreApplication.translate("Dialog", u"3", None))
        self.NumberStopsValueChannelA.setItemText(3, QCoreApplication.translate("Dialog", u"4", None))
        self.NumberStopsValueChannelA.setItemText(4, QCoreApplication.translate("Dialog", u"5", None))

        self.EdgeTypeLabelChannelA.setText(QCoreApplication.translate("Dialog", u"Edge Type:", None))
        self.EdgeTypeValueChannelA.setItemText(0, QCoreApplication.translate("Dialog", u"RISE", None))
        self.EdgeTypeValueChannelA.setItemText(1, QCoreApplication.translate("Dialog", u"FALL", None))

        self.StopMaskLabelChannelA.setText(QCoreApplication.translate("Dialog", u"Stop mask:", None))
        self.StopMaskValueChannelA.setSuffix(QCoreApplication.translate("Dialog", u"\u00b5s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"ChannelA", None))
        self.AverageCyclesLabelChannelB.setText(QCoreApplication.translate("Dialog", u"Average cycles:", None))
        self.AverageCyclesValueB.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.AverageCyclesValueB.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.AverageCyclesValueB.setItemText(2, QCoreApplication.translate("Dialog", u"4", None))
        self.AverageCyclesValueB.setItemText(3, QCoreApplication.translate("Dialog", u"8", None))
        self.AverageCyclesValueB.setItemText(4, QCoreApplication.translate("Dialog", u"16", None))
        self.AverageCyclesValueB.setItemText(5, QCoreApplication.translate("Dialog", u"32", None))
        self.AverageCyclesValueB.setItemText(6, QCoreApplication.translate("Dialog", u"64", None))
        self.AverageCyclesValueB.setItemText(7, QCoreApplication.translate("Dialog", u"128", None))

        self.ModeLabelChannelB.setText(QCoreApplication.translate("Dialog", u"Mode:", None))
        self.ModeValueChannelB.setItemText(0, QCoreApplication.translate("Dialog", u"Mode 1 range: 12ns to 500ns", None))
        self.ModeValueChannelB.setItemText(1, QCoreApplication.translate("Dialog", u"Mode 2 range: 125ns to 4ms", None))

        self.NumberStopsLabelChannelB.setText(QCoreApplication.translate("Dialog", u"Number of stops:", None))
        self.NumberStopsValueChannelB.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.NumberStopsValueChannelB.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.NumberStopsValueChannelB.setItemText(2, QCoreApplication.translate("Dialog", u"3", None))
        self.NumberStopsValueChannelB.setItemText(3, QCoreApplication.translate("Dialog", u"4", None))
        self.NumberStopsValueChannelB.setItemText(4, QCoreApplication.translate("Dialog", u"5", None))

        self.EdgeTypeLabelChannelB.setText(QCoreApplication.translate("Dialog", u"Edge Type:", None))
        self.EdgeTypeValueChannelB.setItemText(0, QCoreApplication.translate("Dialog", u"RISE", None))
        self.EdgeTypeValueChannelB.setItemText(1, QCoreApplication.translate("Dialog", u"FALL", None))

        self.StopMaskLabelChannelB.setText(QCoreApplication.translate("Dialog", u"Stop mask:", None))
        self.StopMaskValueChannelB.setSuffix(QCoreApplication.translate("Dialog", u"\u00b5s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ChannelB), QCoreApplication.translate("Dialog", u"ChannelB", None))
        self.AverageCyclesLabelChannelC.setText(QCoreApplication.translate("Dialog", u"Average cycles:", None))
        self.AverageCyclesValueC.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.AverageCyclesValueC.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.AverageCyclesValueC.setItemText(2, QCoreApplication.translate("Dialog", u"4", None))
        self.AverageCyclesValueC.setItemText(3, QCoreApplication.translate("Dialog", u"8", None))
        self.AverageCyclesValueC.setItemText(4, QCoreApplication.translate("Dialog", u"16", None))
        self.AverageCyclesValueC.setItemText(5, QCoreApplication.translate("Dialog", u"32", None))
        self.AverageCyclesValueC.setItemText(6, QCoreApplication.translate("Dialog", u"64", None))
        self.AverageCyclesValueC.setItemText(7, QCoreApplication.translate("Dialog", u"128", None))

        self.ModeLabelChannelC.setText(QCoreApplication.translate("Dialog", u"Mode:", None))
        self.ModeValueChannelC.setItemText(0, QCoreApplication.translate("Dialog", u"Mode 1 range: 12ns to 500ns", None))
        self.ModeValueChannelC.setItemText(1, QCoreApplication.translate("Dialog", u"Mode 2 range: 125ns to 4ms", None))

        self.NumberStopsLabelChannelC.setText(QCoreApplication.translate("Dialog", u"Number of stops:", None))
        self.NumberStopsValueChannelC.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.NumberStopsValueChannelC.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.NumberStopsValueChannelC.setItemText(2, QCoreApplication.translate("Dialog", u"3", None))
        self.NumberStopsValueChannelC.setItemText(3, QCoreApplication.translate("Dialog", u"4", None))
        self.NumberStopsValueChannelC.setItemText(4, QCoreApplication.translate("Dialog", u"5", None))

        self.EdgeTypeLabelChannelC.setText(QCoreApplication.translate("Dialog", u"Edge Type:", None))
        self.EdgeTypeValueChannelC.setItemText(0, QCoreApplication.translate("Dialog", u"RISE", None))
        self.EdgeTypeValueChannelC.setItemText(1, QCoreApplication.translate("Dialog", u"FALL", None))

        self.StopMaskLabelChannelC.setText(QCoreApplication.translate("Dialog", u"Stop mask:", None))
        self.StopMaskValueChannelC.setSuffix(QCoreApplication.translate("Dialog", u"\u00b5s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"ChannelC", None))
        self.AverageCyclesLabelChannelD.setText(QCoreApplication.translate("Dialog", u"Average cycles:", None))
        self.AverageCyclesValueD.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.AverageCyclesValueD.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.AverageCyclesValueD.setItemText(2, QCoreApplication.translate("Dialog", u"4", None))
        self.AverageCyclesValueD.setItemText(3, QCoreApplication.translate("Dialog", u"8", None))
        self.AverageCyclesValueD.setItemText(4, QCoreApplication.translate("Dialog", u"16", None))
        self.AverageCyclesValueD.setItemText(5, QCoreApplication.translate("Dialog", u"32", None))
        self.AverageCyclesValueD.setItemText(6, QCoreApplication.translate("Dialog", u"64", None))
        self.AverageCyclesValueD.setItemText(7, QCoreApplication.translate("Dialog", u"128", None))

        self.ModeLabelChannelD.setText(QCoreApplication.translate("Dialog", u"Mode:", None))
        self.ModeValueChannelD.setItemText(0, QCoreApplication.translate("Dialog", u"Mode 1 range: 12ns to 500ns", None))
        self.ModeValueChannelD.setItemText(1, QCoreApplication.translate("Dialog", u"Mode 2 range: 125ns to 4ms", None))

        self.NumberStopsLabelChannelD.setText(QCoreApplication.translate("Dialog", u"Number of stops:", None))
        self.NumberStopsValueChannelD.setItemText(0, QCoreApplication.translate("Dialog", u"1", None))
        self.NumberStopsValueChannelD.setItemText(1, QCoreApplication.translate("Dialog", u"2", None))
        self.NumberStopsValueChannelD.setItemText(2, QCoreApplication.translate("Dialog", u"3", None))
        self.NumberStopsValueChannelD.setItemText(3, QCoreApplication.translate("Dialog", u"4", None))
        self.NumberStopsValueChannelD.setItemText(4, QCoreApplication.translate("Dialog", u"5", None))

        self.EdgeTypeLabelChannelD.setText(QCoreApplication.translate("Dialog", u"Edge Type:", None))
        self.EdgeTypeValueChannelD.setItemText(0, QCoreApplication.translate("Dialog", u"RISE", None))
        self.EdgeTypeValueChannelD.setItemText(1, QCoreApplication.translate("Dialog", u"FALL", None))

        self.StopMaskLabelChannelD.setText(QCoreApplication.translate("Dialog", u"Stop mask:", None))
        self.StopMaskValueChannelD.setSuffix(QCoreApplication.translate("Dialog", u"\u00b5s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"ChannelD", None))
        self.AplicarCambios.setText(QCoreApplication.translate("Dialog", u"Apply changes", None))
        self.get_settings()
        
        
    #Get the default settings of device
    def get_settings(self):
        #Get the channels objects
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        #get from the device the value of average_cycles
        average_cyclesA=int(math.log(self.channel1.getAverageCycles(),2))
        self.AverageCyclesValueA.setCurrentIndex(average_cyclesA)
        average_cyclesB=int(math.log(self.channel2.getAverageCycles(),2))
        self.AverageCyclesValueB.setCurrentIndex(average_cyclesB)
        average_cyclesC=int(math.log(self.channel3.getAverageCycles(),2))
        self.AverageCyclesValueC.setCurrentIndex(average_cyclesC)
        average_cyclesD=int(math.log(self.channel4.getAverageCycles(),2))
        self.AverageCyclesValueD.setCurrentIndex(average_cyclesD)
        
        #get the mode
        modeA=self.channel1.getMode()
        modeB=self.channel2.getMode()
        modeC=self.channel3.getMode()
        modeD=self.channel4.getMode()
        #Get from the device the value of the mode
        self.ModeValueChannelA.setCurrentIndex(modeA-1)
        self.ModeValueChannelB.setCurrentIndex(modeB-1)
        self.ModeValueChannelC.setCurrentIndex(modeC-1)
        self.ModeValueChannelD.setCurrentIndex(modeD-1)
        
        #Get the number of stops
        number_stopsA=self.channel1.getNumberOfStops()
        number_stopsB=self.channel2.getNumberOfStops()
        number_stopsC=self.channel3.getNumberOfStops()
        number_stopsD=self.channel4.getNumberOfStops()
        #Get from the device the value of the number of stops
        self.NumberStopsValueChannelA.setCurrentIndex(number_stopsA-1)
        self.NumberStopsValueChannelB.setCurrentIndex(number_stopsB-1)
        self.NumberStopsValueChannelC.setCurrentIndex(number_stopsC-1)
        self.NumberStopsValueChannelD.setCurrentIndex(number_stopsD-1)
        #Get the stop edge
        edgeA=self.channel1.getStopEdge()
        if (edgeA=="RISE"):
            edgeA=0
        else:
            edgeA=1
        
        edgeB=self.channel2.getStopEdge()
        if (edgeB=="RISE"):
            edgeB=0
        else:
            edgeB=1
        
        edgeC=self.channel3.getStopEdge()
        if (edgeC=="RISE"):
            edgeC=0
        else:
            edgeC=1
        
        edgeD=self.channel4.getStopEdge()
        if (edgeD=="RISE"):
            edgeD=0
        else:
            edgeD=1
        #Set the stop edge value
        self.EdgeTypeValueChannelA.setCurrentIndex(edgeA)
        self.EdgeTypeValueChannelB.setCurrentIndex(edgeB)
        self.EdgeTypeValueChannelC.setCurrentIndex(edgeC)
        self.EdgeTypeValueChannelD.setCurrentIndex(edgeD)
        
        #Get the stop mask
        stop_maskA=int(self.channel1.getStopMask())
        stop_maskB=int(self.channel2.getStopMask())
        stop_maskC=int(self.channel3.getStopMask())
        stop_maskD=int(self.channel4.getStopMask())
        #Set the stop mask value
        self.StopMaskValueChannelA.setValue(stop_maskA)
        self.StopMaskValueChannelB.setValue(stop_maskB)
        self.StopMaskValueChannelC.setValue(stop_maskC)
        self.StopMaskValueChannelD.setValue(stop_maskD)
        
            
        
    def event(self, event): 
        if event.type() == QEvent.EnterWhatsThisMode: #Event called when ? is clicked                
            QWhatsThis.leaveWhatsThisMode() #To change mouse cursor back to arrow
            self.showHelp()
            return True
        return QDialog.event(self, event)       
    
     
    def showHelp(self):
        QMessageBox.information(self, "Help", 
                                "Here is the information about the general settings:\n\n"
                                "Average Cycles: This setting indicates how many internal measurements the device performs to provide an averaged result for each measurement. Increasing the number of cycles enhances data accuracy but decreases the program's response time.\n\n"
                                "Mode: This represents the time interval within which stop data will be accepted. Measurements outside this interval will be disregarded.\n\n"
                                "Number of Stops: This indicates how many stops will be measured after a start, with a maximum of 5. If all stops are not captured, the measurements will be invalid.\n\n"
                                "Edge Type: This setting specifies whether the measurement will be taken at the start of the pulse (RISE) or at the end of the pulse (FALL).\n\n"
                                "Stopmask: This accepts time values within which stops will be ignored, ranging from 0 microseconds to 4000 microseconds.")
            
    
    
    def save_changes(self):
        #Get the value of average cycles
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        value_cyclesA=int(self.AverageCyclesValueA.currentText())
        value_cyclesB=int(self.AverageCyclesValueB.currentText())
        value_cyclesC=int(self.AverageCyclesValueC.currentText())
        value_cyclesD=int(self.AverageCyclesValueD.currentText())
        #Get the values of mode
        value_modeA=int(self.ModeValueChannelA.currentIndex())+1
        value_modeB=int(self.ModeValueChannelB.currentIndex())+1
        value_modeC=int(self.ModeValueChannelC.currentIndex())+1
        value_modeD=int(self.ModeValueChannelD.currentIndex())+1
        #Get the number of stops
        value_stopsA=int(self.NumberStopsValueChannelA.currentText())
        value_stopsB=int(self.NumberStopsValueChannelB.currentText())
        value_stopsC=int(self.NumberStopsValueChannelC.currentText())
        value_stopsD=int(self.NumberStopsValueChannelD.currentText())
        #Get the stop mask
        value_maskA=int(self.StopMaskValueChannelA.value())
        value_maskB=int(self.StopMaskValueChannelB.value())
        value_maskC=int(self.StopMaskValueChannelC.value())
        value_maskD=int(self.StopMaskValueChannelD.value())
        #Get the stop edge
        value_stopsEdgeA=self.EdgeTypeValueChannelA.currentText()
        value_stopsEdgeB=self.EdgeTypeValueChannelB.currentText()
        value_stopsEdgeC=self.EdgeTypeValueChannelC.currentText()
        value_stopsEdgeD=self.EdgeTypeValueChannelD.currentText()
        #Set the average cycles
        self.channel1.setAverageCycles(value_cyclesA)
        self.channel2.setAverageCycles(value_cyclesB)
        self.channel3.setAverageCycles(value_cyclesC)
        self.channel4.setAverageCycles(value_cyclesD)
        #Set the mode
        self.channel1.setMode(value_modeA)
        self.channel2.setMode(value_modeB)
        self.channel3.setMode(value_modeC)
        self.channel4.setMode(value_modeD)
        #Set  the number of stops
        self.channel1.setNumberOfStops(value_stopsA)
        self.channel2.setNumberOfStops(value_stopsB)
        self.channel3.setNumberOfStops(value_stopsC)
        self.channel4.setNumberOfStops(value_stopsD)
        #Set the edge type
        self.channel1.setStopEdge(value_stopsEdgeA)
        self.channel2.setStopEdge(value_stopsEdgeB)
        self.channel3.setStopEdge(value_stopsEdgeC)
        self.channel4.setStopEdge(value_stopsEdgeD)
        #Set stop mask
        self.channel1.setStopMask(value_maskA)
        self.channel2.setStopMask(value_maskB)
        self.channel3.setStopMask(value_maskC)
        self.channel4.setStopMask(value_maskD)
        
        
        #Cerrar el qdialog
        self.dialog_1.accept()
        
        
        
        
                
        
        
        
        
    # retranslateUi

