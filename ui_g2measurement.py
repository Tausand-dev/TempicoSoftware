# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'g2measurementncPcXo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_G2(object):
    def setupUi(self, G2Widget):
        if not G2Widget.objectName():
            G2Widget.setObjectName(u"G2Widget")
        G2Widget.setWindowModality(Qt.NonModal)
        G2Widget.resize(894, 801)
        self.verticalLayout = QVBoxLayout(G2Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SettingsWidget = QWidget(G2Widget)
        self.SettingsWidget.setObjectName(u"SettingsWidget")
        self.SettingsWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.SettingsWidget.sizePolicy().hasHeightForWidth())
        self.SettingsWidget.setSizePolicy(sizePolicy)
        self.SettingsWidget.setAutoFillBackground(True)
        self.horizontalLayout = QHBoxLayout(self.SettingsWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ChannelsFrame = QFrame(self.SettingsWidget)
        self.ChannelsFrame.setObjectName(u"ChannelsFrame")
        self.ChannelsFrame.setFrameShape(QFrame.Panel)
        self.ChannelsFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.ChannelsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Channel1Frame = QFrame(self.ChannelsFrame)
        self.Channel1Frame.setObjectName(u"Channel1Frame")
        self.Channel1Frame.setFrameShape(QFrame.StyledPanel)
        self.Channel1Frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.Channel1Frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Channel1Label = QLabel(self.Channel1Frame)
        self.Channel1Label.setObjectName(u"Channel1Label")

        self.horizontalLayout_2.addWidget(self.Channel1Label)

        self.Channel1ComboBox = QComboBox(self.Channel1Frame)
        self.Channel1ComboBox.addItem("")
        self.Channel1ComboBox.addItem("")
        self.Channel1ComboBox.addItem("")
        self.Channel1ComboBox.addItem("")
        self.Channel1ComboBox.setObjectName(u"Channel1ComboBox")

        self.horizontalLayout_2.addWidget(self.Channel1ComboBox)


        self.verticalLayout_2.addWidget(self.Channel1Frame)

        self.Channel2Frame = QFrame(self.ChannelsFrame)
        self.Channel2Frame.setObjectName(u"Channel2Frame")
        self.Channel2Frame.setFrameShape(QFrame.StyledPanel)
        self.Channel2Frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.Channel2Frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Channel2Labe = QLabel(self.Channel2Frame)
        self.Channel2Labe.setObjectName(u"Channel2Labe")

        self.horizontalLayout_3.addWidget(self.Channel2Labe)

        self.Channel2ComboBox = QComboBox(self.Channel2Frame)
        self.Channel2ComboBox.addItem("")
        self.Channel2ComboBox.addItem("")
        self.Channel2ComboBox.addItem("")
        self.Channel2ComboBox.addItem("")
        self.Channel2ComboBox.setObjectName(u"Channel2ComboBox")

        self.horizontalLayout_3.addWidget(self.Channel2ComboBox)


        self.verticalLayout_2.addWidget(self.Channel2Frame)


        self.horizontalLayout.addWidget(self.ChannelsFrame)

        self.ParametersFrame = QFrame(self.SettingsWidget)
        self.ParametersFrame.setObjectName(u"ParametersFrame")
        self.ParametersFrame.setFrameShape(QFrame.Panel)
        self.ParametersFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.ParametersFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        

        self.CountChannel1 = QLabel(self.ParametersFrame)
        self.CountChannel1.setObjectName(u"CountChannel1")

        self.verticalLayout_3.addWidget(self.CountChannel1)

        self.CountChannel1Value = QLabel(self.ParametersFrame)
        self.CountChannel1Value.setObjectName(u"CountChannel1Value")

        self.verticalLayout_3.addWidget(self.CountChannel1Value)

        self.CountChannel2 = QLabel(self.ParametersFrame)
        self.CountChannel2.setObjectName(u"CountChannel2")

        self.verticalLayout_3.addWidget(self.CountChannel2)

        self.CountChannel2Value = QLabel(self.ParametersFrame)
        self.CountChannel2Value.setObjectName(u"CountChannel2Value")

        self.verticalLayout_3.addWidget(self.CountChannel2Value)


        self.horizontalLayout.addWidget(self.ParametersFrame)

        self.HistParametersFrame = QFrame(self.SettingsWidget)
        self.HistParametersFrame.setObjectName(u"HistParametersFrame")
        self.HistParametersFrame.setFrameShape(QFrame.Panel)
        self.HistParametersFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_4 = QVBoxLayout(self.HistParametersFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.BinWidthFrame = QFrame(self.HistParametersFrame)
        self.BinWidthFrame.setObjectName(u"BinWidthFrame")
        self.BinWidthFrame.setFrameShape(QFrame.StyledPanel)
        self.BinWidthFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.BinWidthFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.BinWidthLabel = QLabel(self.BinWidthFrame)
        self.BinWidthLabel.setObjectName(u"BinWidthLabel")

        self.horizontalLayout_4.addWidget(self.BinWidthLabel)

        self.BinWidthValue = QComboBox(self.BinWidthFrame)
        self.powers_of_two = ["60 ps", "120 ps", "240 ps", "480 ps", "960 ps", 
                              "2 ns", "4 ns", "8 ns", "16 ns", "32 ns", "64 ns", 
                              "128 ns", "256 ns", "512 ns", "1 µs", "2 µs", 
                              "4 µs", "8 µs", "16 µs", "32 µs", "64 µs", "100 µs"]

        self.BinWidthValue.addItems(self.powers_of_two)
        self.BinWidthValue.setObjectName(u"BinWidthValue")

        self.horizontalLayout_4.addWidget(self.BinWidthValue)


        self.verticalLayout_4.addWidget(self.BinWidthFrame)
        

        self.horizontalLayout.addWidget(self.HistParametersFrame)


        self.verticalLayout.addWidget(self.SettingsWidget)

        self.ActionsButtons = QWidget(G2Widget)
        self.ActionsButtons.setObjectName(u"ActionsButtons")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(10)
        sizePolicy1.setHeightForWidth(self.ActionsButtons.sizePolicy().hasHeightForWidth())
        self.ActionsButtons.setSizePolicy(sizePolicy1)
        self.ActionsButtons.setAutoFillBackground(True)
        self.horizontalLayout_6 = QHBoxLayout(self.ActionsButtons)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ActionButtonsFrame = QFrame(self.ActionsButtons)
        self.ActionButtonsFrame.setObjectName(u"ActionButtonsFrame")
        self.ActionButtonsFrame.setFrameShape(QFrame.Panel)
        self.ActionButtonsFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_8 = QHBoxLayout(self.ActionButtonsFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.StartButton = QPushButton(self.ActionButtonsFrame)
        self.StartButton.setObjectName(u"StartButton")

        self.horizontalLayout_8.addWidget(self.StartButton)

        self.StopButton = QPushButton(self.ActionButtonsFrame)
        self.StopButton.setObjectName(u"StopButton")

        self.horizontalLayout_8.addWidget(self.StopButton)

        self.SaveDataButton = QPushButton(self.ActionButtonsFrame)
        self.SaveDataButton.setObjectName(u"SaveDataButton")

        self.horizontalLayout_8.addWidget(self.SaveDataButton)

        self.SavePlotButton = QPushButton(self.ActionButtonsFrame)
        self.SavePlotButton.setObjectName(u"SavePlotButton")

        self.horizontalLayout_8.addWidget(self.SavePlotButton)


        self.horizontalLayout_6.addWidget(self.ActionButtonsFrame)


        self.verticalLayout.addWidget(self.ActionsButtons)

        self.GraphicWidget = QWidget(G2Widget)
        self.GraphicWidget.setObjectName(u"GraphicWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(55)
        sizePolicy2.setHeightForWidth(self.GraphicWidget.sizePolicy().hasHeightForWidth())
        self.GraphicWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_7 = QHBoxLayout(self.GraphicWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.FitFrame = QFrame(self.GraphicWidget)
        self.FitFrame.setObjectName(u"FitFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.FitFrame.sizePolicy().hasHeightForWidth())
        self.FitFrame.setSizePolicy(sizePolicy3)
        self.FitFrame.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.FitFrame.setAutoFillBackground(True)
        self.FitFrame.setFrameShape(QFrame.Panel)
        self.FitFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_9 = QHBoxLayout(self.FitFrame)
        self.HelpButton= QPushButton("Help")
        self.horizontalLayout_9.addWidget(self.HelpButton)
        # self.LabelToImplement = QLabel(self.FitFrame)
        
        # self.LabelToImplement.setObjectName(u"LabelToImplement")
        # self.LabelToImplement.setGeometry(QRect(20, 40, 91, 16))

        self.horizontalLayout_7.addWidget(self.FitFrame)

        self.GraphicFrame = QFrame(self.GraphicWidget)
        self.GraphicFrame.setObjectName(u"GraphicFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(9)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.GraphicFrame.sizePolicy().hasHeightForWidth())
        self.GraphicFrame.setSizePolicy(sizePolicy4)
        self.GraphicFrame.setAutoFillBackground(True)
        self.GraphicFrame.setFrameShape(QFrame.Panel)
        self.GraphicFrame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_7.addWidget(self.GraphicFrame)


        self.verticalLayout.addWidget(self.GraphicWidget)
        
        
        self.StatusWidget = QWidget(G2Widget)
        self.StatusWidget.setObjectName(u"StatusWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(5)
        sizePolicy5.setHeightForWidth(self.StatusWidget.sizePolicy().hasHeightForWidth())
        self.StatusWidget.setSizePolicy(sizePolicy5)
        self.StatusWidget.setAutoFillBackground(True)
        self.verticalLayout_5 = QVBoxLayout(self.StatusWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.StatusFrame = QFrame(self.StatusWidget)
        self.StatusFrame.setObjectName(u"StatusFrame")
        self.StatusFrame.setFrameShape(QFrame.Panel)
        self.StatusFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_10 = QHBoxLayout(self.StatusFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_9")
        self.StatusLabel = QLabel(self.StatusFrame)
        self.StatusLabel.setObjectName(u"StatusLabel")

        self.horizontalLayout_10.addWidget(self.StatusLabel)

        self.StatusValueMeasuremen = QLabel(self.StatusFrame)
        self.StatusValueMeasuremen.setObjectName(u"StatusValueMeasuremen")

        self.horizontalLayout_10.addWidget(self.StatusValueMeasuremen)


        self.verticalLayout_5.addWidget(self.StatusFrame)


        self.verticalLayout.addWidget(self.StatusWidget)
        self.StatusPoint=QLabel()
        self.StatusPoint.setStyleSheet("background-color: transparent;")
        self.StatusPoint.setFixedSize(20, 20)
        self.drawRedPoint()
        self.horizontalLayout_10.addWidget(self.StatusPoint)


        self.retranslateUi(G2Widget)

        QMetaObject.connectSlotsByName(G2Widget)
    # setupUi

    def retranslateUi(self, G2Widget):
        G2Widget.setWindowTitle(QCoreApplication.translate("G2Widget", u"Form", None))
        self.Channel1Label.setText(QCoreApplication.translate("G2Widget", u"Channel 1:", None))
        self.Channel1ComboBox.setItemText(0, QCoreApplication.translate("G2Widget", u"Channel A", None))
        self.Channel1ComboBox.setItemText(1, QCoreApplication.translate("G2Widget", u"Channel B", None))
        self.Channel1ComboBox.setItemText(2, QCoreApplication.translate("G2Widget", u"Channel C", None))
        self.Channel1ComboBox.setItemText(3, QCoreApplication.translate("G2Widget", u"Channel D", None))

        self.Channel2Labe.setText(QCoreApplication.translate("G2Widget", u"Channel 2:", None))
        self.Channel2ComboBox.setItemText(0, QCoreApplication.translate("G2Widget", u"Channel A", None))
        self.Channel2ComboBox.setItemText(1, QCoreApplication.translate("G2Widget", u"Channel B", None))
        self.Channel2ComboBox.setItemText(2, QCoreApplication.translate("G2Widget", u"Channel C", None))
        self.Channel2ComboBox.setItemText(3, QCoreApplication.translate("G2Widget", u"Channel D", None))

        self.CountChannel1.setText(QCoreApplication.translate("G2Widget", u"Average Interval time count Channel 1:", None))
        self.CountChannel1Value.setText(QCoreApplication.translate("G2Widget", u"Undefined", None))
        self.CountChannel2.setText(QCoreApplication.translate("G2Widget", u"Average Interval time count Channel 2:", None))
        self.CountChannel2Value.setText(QCoreApplication.translate("G2Widget", u"Undefined", None))
        self.BinWidthLabel.setText(QCoreApplication.translate("G2Widget", u"Bin width:", None))
        self.StartButton.setText(QCoreApplication.translate("G2Widget", u"Start", None))
        self.StopButton.setText(QCoreApplication.translate("G2Widget", u"Stop", None))
        self.SaveDataButton.setText(QCoreApplication.translate("G2Widget", u"Save Data File", None))
        self.SavePlotButton.setText(QCoreApplication.translate("G2Widget", u"Save Plot", None))
        self.StatusLabel.setText(QCoreApplication.translate("G2Widget", u"Status:", None))
        self.StatusValueMeasuremen.setText(QCoreApplication.translate("G2Widget", u"No measurement running", None))
        # self.LabelToImplement.setText(QCoreApplication.translate("G2Widget", u"Fit Parameters:", None))
    # retranslateUi
    def drawRedPoint(self):
        pixmap = QPixmap(self.StatusPoint.size())
        pixmap.fill(Qt.transparent)  # Fondo transparente

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # Para bordes suaves
        painter.setBrush(QColor(128, 128, 128))  # Color rojo
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.StatusPoint.width(), self.StatusPoint.height())  # Dibuja el círculo
        painter.end()

        self.StatusPoint.setPixmap(pixmap)  # Establece el QPixmap en el QLabel

