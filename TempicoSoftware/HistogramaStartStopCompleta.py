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
        self.graphicSelectFrame = QFrame(self.GraphConfigurationArea)
        self.graphicSelectFrame.setObjectName(u"graphicSelectFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.graphicSelectFrame.sizePolicy().hasHeightForWidth())
        self.graphicSelectFrame.setSizePolicy(sizePolicy2)
        self.graphicSelectFrame.setFrameShape(QFrame.Panel)
        self.graphicSelectFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_2 = QHBoxLayout(self.graphicSelectFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.LabelNumbeFrame = QFrame(self.graphicSelectFrame)
        self.LabelNumbeFrame.setObjectName(u"LabelNumbeFrame")
        self.LabelNumbeFrame.setFrameShape(QFrame.StyledPanel)
        self.LabelNumbeFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.LabelNumbeFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.numberGraphLabel = QLabel(self.LabelNumbeFrame)
        self.numberGraphLabel.setObjectName(u"numberGraphLabel")
        self.numberGraphLabel.setAutoFillBackground(False)
        self.numberGraphLabel.setTextFormat(Qt.MarkdownText)

        self.horizontalLayout_3.addWidget(self.numberGraphLabel)


        self.horizontalLayout_2.addWidget(self.LabelNumbeFrame)

        self.NumbeComboBoxFrame = QFrame(self.graphicSelectFrame)
        self.NumbeComboBoxFrame.setObjectName(u"NumbeComboBoxFrame")
        self.NumbeComboBoxFrame.setFrameShape(QFrame.StyledPanel)
        self.NumbeComboBoxFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.NumbeComboBoxFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.GraphicsComboBox = QComboBox(self.NumbeComboBoxFrame)
        self.GraphicsComboBox.addItem("")
        self.GraphicsComboBox.addItem("")
        self.GraphicsComboBox.addItem("")
        self.GraphicsComboBox.addItem("")
        self.GraphicsComboBox.setObjectName(u"GraphicsComboBox")

        self.verticalLayout_2.addWidget(self.GraphicsComboBox)


        self.horizontalLayout_2.addWidget(self.NumbeComboBoxFrame)


        self.verticalLayout.addWidget(self.graphicSelectFrame)

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
        self.RangeGraph1 = QLabel(self.HistGraph1)
        self.RangeGraph1.setObjectName(u"RangeGraph1")

        self.horizontalLayout_11.addWidget(self.RangeGraph1)

        self.RangeNumericGraph1 = QSpinBox(self.HistGraph1)
        self.RangeNumericGraph1.setObjectName(u"RangeNumericGraph1")

        self.horizontalLayout_11.addWidget(self.RangeNumericGraph1)

        self.SaveGraph1 = QPushButton(self.HistGraph1)
        self.SaveGraph1.setObjectName(u"SaveGraph1")

        self.horizontalLayout_11.addWidget(self.SaveGraph1)


        self.verticalLayout_3.addWidget(self.HistGraph1)


        self.verticalLayout.addWidget(self.Graph1Configuration)

        self.Graph2Configuration = QFrame(self.GraphConfigurationArea)
        self.Graph2Configuration.setObjectName(u"Graph2Configuration")
        sizePolicy3.setHeightForWidth(self.Graph2Configuration.sizePolicy().hasHeightForWidth())
        self.Graph2Configuration.setSizePolicy(sizePolicy3)
        self.Graph2Configuration.setFrameShape(QFrame.Panel)
        self.Graph2Configuration.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_5 = QVBoxLayout(self.Graph2Configuration)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.LabelFrameGraph2 = QFrame(self.Graph2Configuration)
        self.LabelFrameGraph2.setObjectName(u"LabelFrameGraph2")
        self.LabelFrameGraph2.setFrameShape(QFrame.StyledPanel)
        self.LabelFrameGraph2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.LabelFrameGraph2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.LabelGraph2 = QLabel(self.LabelFrameGraph2)
        self.LabelGraph2.setObjectName(u"LabelGraph2")

        self.horizontalLayout_5.addWidget(self.LabelGraph2)


        self.verticalLayout_5.addWidget(self.LabelFrameGraph2)

        self.ComboBoxGraph2 = QFrame(self.Graph2Configuration)
        self.ComboBoxGraph2.setObjectName(u"ComboBoxGraph2")
        self.ComboBoxGraph2.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxGraph2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.ComboBoxGraph2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.Channel1Graph2 = QCheckBox(self.ComboBoxGraph2)
        self.Channel1Graph2.setObjectName(u"Channel1Graph2")

        self.horizontalLayout_8.addWidget(self.Channel1Graph2)

        self.Channel2Graph2 = QCheckBox(self.ComboBoxGraph2)
        self.Channel2Graph2.setObjectName(u"Channel2Graph2")

        self.horizontalLayout_8.addWidget(self.Channel2Graph2)

        self.Channel4Graph2 = QCheckBox(self.ComboBoxGraph2)
        self.Channel4Graph2.setObjectName(u"Channel4Graph2")

        self.horizontalLayout_8.addWidget(self.Channel4Graph2)

        self.Channel3Graph2 = QCheckBox(self.ComboBoxGraph2)
        self.Channel3Graph2.setObjectName(u"Channel3Graph2")

        self.horizontalLayout_8.addWidget(self.Channel3Graph2)


        self.verticalLayout_5.addWidget(self.ComboBoxGraph2)

        self.HistGraph2 = QFrame(self.Graph2Configuration)
        self.HistGraph2.setObjectName(u"HistGraph2")
        self.HistGraph2.setFrameShape(QFrame.StyledPanel)
        self.HistGraph2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.HistGraph2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.RangeGraph2 = QLabel(self.HistGraph2)
        self.RangeGraph2.setObjectName(u"RangeGraph2")

        self.horizontalLayout_12.addWidget(self.RangeGraph2)

        self.SaveGraph2 = QSpinBox(self.HistGraph2)
        self.SaveGraph2.setObjectName(u"SaveGraph2")

        self.horizontalLayout_12.addWidget(self.SaveGraph2)

        self.RangeNumericGraph2 = QPushButton(self.HistGraph2)
        self.RangeNumericGraph2.setObjectName(u"RangeNumericGraph2")

        self.horizontalLayout_12.addWidget(self.RangeNumericGraph2)


        self.verticalLayout_5.addWidget(self.HistGraph2)


        self.verticalLayout.addWidget(self.Graph2Configuration)

        self.Graph3Configuration = QFrame(self.GraphConfigurationArea)
        self.Graph3Configuration.setObjectName(u"Graph3Configuration")
        sizePolicy3.setHeightForWidth(self.Graph3Configuration.sizePolicy().hasHeightForWidth())
        self.Graph3Configuration.setSizePolicy(sizePolicy3)
        self.Graph3Configuration.setFrameShape(QFrame.Panel)
        self.Graph3Configuration.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_6 = QVBoxLayout(self.Graph3Configuration)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.LabelFrameGraph3 = QFrame(self.Graph3Configuration)
        self.LabelFrameGraph3.setObjectName(u"LabelFrameGraph3")
        self.LabelFrameGraph3.setFrameShape(QFrame.StyledPanel)
        self.LabelFrameGraph3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.LabelFrameGraph3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.LabelGraph3 = QLabel(self.LabelFrameGraph3)
        self.LabelGraph3.setObjectName(u"LabelGraph3")

        self.horizontalLayout_6.addWidget(self.LabelGraph3)


        self.verticalLayout_6.addWidget(self.LabelFrameGraph3)

        self.ComboBoxGraph3 = QFrame(self.Graph3Configuration)
        self.ComboBoxGraph3.setObjectName(u"ComboBoxGraph3")
        self.ComboBoxGraph3.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxGraph3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.ComboBoxGraph3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.Channel4Graph3 = QCheckBox(self.ComboBoxGraph3)
        self.Channel4Graph3.setObjectName(u"Channel4Graph3")

        self.horizontalLayout_9.addWidget(self.Channel4Graph3)

        self.Channel3Graph3 = QCheckBox(self.ComboBoxGraph3)
        self.Channel3Graph3.setObjectName(u"Channel3Graph3")

        self.horizontalLayout_9.addWidget(self.Channel3Graph3)

        self.Channel1Graph3 = QCheckBox(self.ComboBoxGraph3)
        self.Channel1Graph3.setObjectName(u"Channel1Graph3")

        self.horizontalLayout_9.addWidget(self.Channel1Graph3)

        self.Channel2Graph3 = QCheckBox(self.ComboBoxGraph3)
        self.Channel2Graph3.setObjectName(u"Channel2Graph3")

        self.horizontalLayout_9.addWidget(self.Channel2Graph3)


        self.verticalLayout_6.addWidget(self.ComboBoxGraph3)

        self.HistGraph3 = QFrame(self.Graph3Configuration)
        self.HistGraph3.setObjectName(u"HistGraph3")
        self.HistGraph3.setFrameShape(QFrame.StyledPanel)
        self.HistGraph3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.HistGraph3)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.RangeGraph3 = QLabel(self.HistGraph3)
        self.RangeGraph3.setObjectName(u"RangeGraph3")

        self.horizontalLayout_13.addWidget(self.RangeGraph3)

        self.SaveGraph3 = QSpinBox(self.HistGraph3)
        self.SaveGraph3.setObjectName(u"SaveGraph3")

        self.horizontalLayout_13.addWidget(self.SaveGraph3)

        self.RangeNumericGraph3 = QPushButton(self.HistGraph3)
        self.RangeNumericGraph3.setObjectName(u"RangeNumericGraph3")

        self.horizontalLayout_13.addWidget(self.RangeNumericGraph3)


        self.verticalLayout_6.addWidget(self.HistGraph3)


        self.verticalLayout.addWidget(self.Graph3Configuration)

        self.Graph4Configuration = QFrame(self.GraphConfigurationArea)
        self.Graph4Configuration.setObjectName(u"Graph4Configuration")
        sizePolicy3.setHeightForWidth(self.Graph4Configuration.sizePolicy().hasHeightForWidth())
        self.Graph4Configuration.setSizePolicy(sizePolicy3)
        self.Graph4Configuration.setFrameShape(QFrame.Panel)
        self.Graph4Configuration.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_7 = QVBoxLayout(self.Graph4Configuration)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.LabelFrameGraph4 = QFrame(self.Graph4Configuration)
        self.LabelFrameGraph4.setObjectName(u"LabelFrameGraph4")
        self.LabelFrameGraph4.setFrameShape(QFrame.StyledPanel)
        self.LabelFrameGraph4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.LabelFrameGraph4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.LabelGraph4 = QLabel(self.LabelFrameGraph4)
        self.LabelGraph4.setObjectName(u"LabelGraph4")

        self.horizontalLayout_7.addWidget(self.LabelGraph4)


        self.verticalLayout_7.addWidget(self.LabelFrameGraph4)

        self.ComboBoxGraph4 = QFrame(self.Graph4Configuration)
        self.ComboBoxGraph4.setObjectName(u"ComboBoxGraph4")
        self.ComboBoxGraph4.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxGraph4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.ComboBoxGraph4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.Channel1Graph4 = QCheckBox(self.ComboBoxGraph4)
        self.Channel1Graph4.setObjectName(u"Channel1Graph4")

        self.horizontalLayout_10.addWidget(self.Channel1Graph4)

        self.Channel2Graph4 = QCheckBox(self.ComboBoxGraph4)
        self.Channel2Graph4.setObjectName(u"Channel2Graph4")

        self.horizontalLayout_10.addWidget(self.Channel2Graph4)

        self.Channel4Graph4 = QCheckBox(self.ComboBoxGraph4)
        self.Channel4Graph4.setObjectName(u"Channel4Graph4")

        self.horizontalLayout_10.addWidget(self.Channel4Graph4)

        self.Channel3Graph4 = QCheckBox(self.ComboBoxGraph4)
        self.Channel3Graph4.setObjectName(u"Channel3Graph4")

        self.horizontalLayout_10.addWidget(self.Channel3Graph4)


        self.verticalLayout_7.addWidget(self.ComboBoxGraph4)

        self.HistGraph4 = QFrame(self.Graph4Configuration)
        self.HistGraph4.setObjectName(u"HistGraph4")
        self.HistGraph4.setFrameShape(QFrame.StyledPanel)
        self.HistGraph4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.HistGraph4)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_9 = QLabel(self.HistGraph4)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_14.addWidget(self.label_9)

        self.spinBox_4 = QSpinBox(self.HistGraph4)
        self.spinBox_4.setObjectName(u"spinBox_4")

        self.horizontalLayout_14.addWidget(self.spinBox_4)

        self.pushButton_4 = QPushButton(self.HistGraph4)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_14.addWidget(self.pushButton_4)


        self.verticalLayout_7.addWidget(self.HistGraph4)


        self.verticalLayout.addWidget(self.Graph4Configuration)


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

        self.Graph2 = QFrame(self.GraphicArea)
        self.Graph2.setObjectName(u"Graph2")
        sizePolicy5.setHeightForWidth(self.Graph2.sizePolicy().hasHeightForWidth())
        self.Graph2.setSizePolicy(sizePolicy5)
        self.Graph2.setFrameShape(QFrame.StyledPanel)
        self.Graph2.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.Graph2, 1, 1, 1, 1)

        self.Graph4 = QFrame(self.GraphicArea)
        self.Graph4.setObjectName(u"Graph4")
        sizePolicy5.setHeightForWidth(self.Graph4.sizePolicy().hasHeightForWidth())
        self.Graph4.setSizePolicy(sizePolicy5)
        self.Graph4.setFrameShape(QFrame.StyledPanel)
        self.Graph4.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.Graph4, 2, 1, 1, 1)

        self.Graph1 = QFrame(self.GraphicArea)
        self.Graph1.setObjectName(u"Graph1")
        sizePolicy5.setHeightForWidth(self.Graph1.sizePolicy().hasHeightForWidth())
        self.Graph1.setSizePolicy(sizePolicy5)
        self.Graph1.setFrameShape(QFrame.StyledPanel)
        self.Graph1.setFrameShadow(QFrame.Plain)
        self.Graph1.setStyleSheet("QFrame#Graph1 { background-image: url('./Sources/Histogram.png');"
                                  "                     background-repeat: no-repeat;"
                                  "                     background-position: center;"
                                  "                     }")
        

        self.gridLayout.addWidget(self.Graph1, 1, 0, 1, 1)


        self.horizontalLayout.addWidget(self.GraphicArea)


        self.retranslateUi(HistogramaStartStop)
        

        QMetaObject.connectSlotsByName(HistogramaStartStop)
    # setupUi

    def retranslateUi(self, HistogramaStartStop):
        HistogramaStartStop.setWindowTitle(QCoreApplication.translate("HistogramaStartStop", u"Form", None))
        self.numberGraphLabel.setText(QCoreApplication.translate("HistogramaStartStop", u"Number of graphics:", None))
        self.GraphicsComboBox.setItemText(0, QCoreApplication.translate("HistogramaStartStop", u"1", None))
        self.GraphicsComboBox.setItemText(1, QCoreApplication.translate("HistogramaStartStop", u"2", None))
        self.GraphicsComboBox.setItemText(2, QCoreApplication.translate("HistogramaStartStop", u"3", None))
        self.GraphicsComboBox.setItemText(3, QCoreApplication.translate("HistogramaStartStop", u"4", None))

        self.LabelGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channels in the graphic:", None))
        self.Channel1Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 1", None))
        self.Channel4Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel2", None))
        self.Channel2Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 3", None))
        self.Channel3Graph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 4", None))
        self.RangeGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Width (y axis)", None))
        self.RangeNumericGraph1.setSuffix(QCoreApplication.translate("HistogramaStartStop", u"ms", None))
        self.SaveGraph1.setText(QCoreApplication.translate("HistogramaStartStop", u"Save", None))
        self.LabelGraph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Channels in the graphic:", None))
        self.Channel1Graph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 1", None))
        self.Channel2Graph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel2", None))
        self.Channel4Graph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 4", None))
        self.Channel3Graph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 3", None))
        self.RangeGraph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Width (y axis)", None))
        self.SaveGraph2.setSuffix(QCoreApplication.translate("HistogramaStartStop", u"ms", None))
        self.RangeNumericGraph2.setText(QCoreApplication.translate("HistogramaStartStop", u"Save", None))
        self.LabelGraph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Channels in the graphic:", None))
        self.Channel4Graph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 1", None))
        self.Channel3Graph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 4", None))
        self.Channel1Graph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel2", None))
        self.Channel2Graph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 3", None))
        self.RangeGraph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Width (y axis)", None))
        self.SaveGraph3.setSuffix(QCoreApplication.translate("HistogramaStartStop", u"ms", None))
        self.RangeNumericGraph3.setText(QCoreApplication.translate("HistogramaStartStop", u"Save", None))
        self.LabelGraph4.setText(QCoreApplication.translate("HistogramaStartStop", u"Channels in the graphic:", None))
        self.Channel1Graph4.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 1", None))
        self.Channel2Graph4.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel2", None))
        self.Channel4Graph4.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 4", None))
        self.Channel3Graph4.setText(QCoreApplication.translate("HistogramaStartStop", u"Channel 3", None))
        self.label_9.setText(QCoreApplication.translate("HistogramaStartStop", u"Width (y axis)", None))
        self.spinBox_4.setSuffix(QCoreApplication.translate("HistogramaStartStop", u"ms", None))
        self.pushButton_4.setText(QCoreApplication.translate("HistogramaStartStop", u"Save", None))
    # retranslateUi





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

