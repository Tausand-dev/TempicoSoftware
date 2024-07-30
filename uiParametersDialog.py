# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designervlOVuU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class UiParameters(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        Dialog.setMinimumSize(QSize(400, 300))
        Dialog.setMaximumSize(QSize(400, 300))
        Dialog.setBaseSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.channelFrame = QFrame(Dialog)
        self.channelFrame.setObjectName(u"channelFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.channelFrame.sizePolicy().hasHeightForWidth())
        self.channelFrame.setSizePolicy(sizePolicy)
        self.channelFrame.setAutoFillBackground(True)
        self.channelFrame.setFrameShape(QFrame.Panel)
        self.channelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.channelFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.selectFrame = QFrame(self.channelFrame)
        self.selectFrame.setObjectName(u"selectFrame")
        self.selectFrame.setFrameShape(QFrame.Panel)
        self.selectFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.selectFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.selectChannelLabel = QLabel(self.selectFrame)
        self.selectChannelLabel.setObjectName(u"selectChannelLabel")

        self.verticalLayout_2.addWidget(self.selectChannelLabel)

        self.channelComboBox = QComboBox(self.selectFrame)
        self.channelComboBox.addItem("")
        self.channelComboBox.addItem("")
        self.channelComboBox.addItem("")
        self.channelComboBox.addItem("")
        self.channelComboBox.setObjectName(u"channelComboBox")

        self.verticalLayout_2.addWidget(self.channelComboBox)


        self.horizontalLayout_2.addWidget(self.selectFrame)

        self.frame_2 = QFrame(self.channelFrame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Panel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.startButton = QPushButton(self.frame_2)
        self.startButton.setObjectName(u"startButton")

        self.verticalLayout_4.addWidget(self.startButton)

        self.stopButton = QPushButton(self.frame_2)
        self.stopButton.setObjectName(u"stopButton")

        self.verticalLayout_4.addWidget(self.stopButton)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.channelFrame)

        self.measurementFrame = QFrame(Dialog)
        self.measurementFrame.setObjectName(u"measurementFrame")
        sizePolicy.setHeightForWidth(self.measurementFrame.sizePolicy().hasHeightForWidth())
        self.measurementFrame.setSizePolicy(sizePolicy)
        self.measurementFrame.setAutoFillBackground(True)
        self.measurementFrame.setFrameShape(QFrame.Panel)
        self.measurementFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.measurementFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.informationMeasureLabel = QLabel(self.measurementFrame)
        self.informationMeasureLabel.setObjectName(u"informationMeasureLabel")

        self.verticalLayout_3.addWidget(self.informationMeasureLabel)

        self.measurementLabel = QLabel(self.measurementFrame)
        self.measurementLabel.setObjectName(u"measurementLabel")

        self.verticalLayout_3.addWidget(self.measurementLabel)


        self.verticalLayout.addWidget(self.measurementFrame)

        self.statusFrame = QFrame(Dialog)
        self.statusFrame.setObjectName(u"statusFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.statusFrame.sizePolicy().hasHeightForWidth())
        self.statusFrame.setSizePolicy(sizePolicy1)
        self.statusFrame.setAutoFillBackground(True)
        self.statusFrame.setFrameShape(QFrame.Panel)
        self.statusFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout = QHBoxLayout(self.statusFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.statusLabel = QLabel(self.statusFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.statusLabel)

        self.measuremetStatusLabel = QLabel(self.statusFrame)
        self.measuremetStatusLabel.setObjectName(u"measuremetStatusLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(8)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.measuremetStatusLabel.sizePolicy().hasHeightForWidth())
        self.measuremetStatusLabel.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.measuremetStatusLabel)


        self.verticalLayout.addWidget(self.statusFrame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.selectChannelLabel.setText(QCoreApplication.translate("Dialog", u"Select Channel:", None))
        self.channelComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Channel A", None))
        self.channelComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Channel B", None))
        self.channelComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Channel C", None))
        self.channelComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"Channel D", None))

        self.startButton.setText(QCoreApplication.translate("Dialog", u"Start adquisition", None))
        self.stopButton.setText(QCoreApplication.translate("Dialog", u"Stop adquisition", None))
        self.informationMeasureLabel.setText(QCoreApplication.translate("Dialog", u"Mean time between events of Channel A:", None))
        self.measurementLabel.setText(QCoreApplication.translate("Dialog", u"Undefined", None))
        self.statusLabel.setText(QCoreApplication.translate("Dialog", u"Status:", None))
        self.measuremetStatusLabel.setText(QCoreApplication.translate("Dialog", u"Not running", None))
    # retranslateUi

