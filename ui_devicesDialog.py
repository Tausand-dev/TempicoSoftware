# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerFilYcl.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from findDevices import PyTempicoManager 
import pyTempico as tempico


class Ui_Devices(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        self.Dialog=Dialog
        self.deviceConnected=None
        self.Dialog.resize(460, 197)
        self.verticalLayout = QVBoxLayout(self.Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TitleFrame = QFrame(self.Dialog)
        self.TitleFrame.setObjectName(u"TitleFrame")
        self.TitleFrame.setFrameShape(QFrame.StyledPanel)
        self.TitleFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.TitleFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.DevicesComboBo = QLabel(self.TitleFrame)
        self.DevicesComboBo.setObjectName(u"DevicesComboBo")
        self.DevicesComboBo.setAlignment(Qt.AlignCenter)
        self.DevicesComboBo.setMargin(0)

        self.verticalLayout_2.addWidget(self.DevicesComboBo)


        self.verticalLayout.addWidget(self.TitleFrame)

        self.ComboBoxFrame = QFrame(self.Dialog)
        self.ComboBoxFrame.setObjectName(u"ComboBoxFrame")
        self.ComboBoxFrame.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.ComboBoxFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.DevicesComboBox = QComboBox(self.ComboBoxFrame)
        self.DevicesComboBox.setObjectName(u"DevicesComboBox")
        

        self.horizontalLayout_2.addWidget(self.DevicesComboBox)


        self.verticalLayout.addWidget(self.ComboBoxFrame)

        self.ButtoFram = QFrame(self.Dialog)
        self.ButtoFram.setObjectName(u"ButtoFram")
        self.ButtoFram.setFrameShape(QFrame.StyledPanel)
        self.ButtoFram.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.ButtoFram)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ConnectButton = QPushButton(self.ButtoFram)
        self.ConnectButton.setObjectName(u"CancelButto")
        self.ConnectButton.setDisabled(True)
        self.horizontalLayout.addWidget(self.ConnectButton)

        self.CancelButto = QPushButton(self.ButtoFram)
        self.CancelButto.setObjectName(u"ConnectButton")
        
        self.CancelButto.clicked.connect(self.cancelClick)
        self.ConnectButton.clicked.connect(self.connectClick)

        self.horizontalLayout.addWidget(self.CancelButto)


        self.verticalLayout.addWidget(self.ButtoFram)


        self.retranslateUi(self.Dialog)

        QMetaObject.connectSlotsByName(self.Dialog)
        self.add_tempicodevices()
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.DevicesComboBo.setText(QCoreApplication.translate("Dialog", u"Which device would you like to connect?", None))
        self.ConnectButton.setText(QCoreApplication.translate("Dialog", u"Connect", None))
        self.CancelButto.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi
    #To do definir funcion para conectar al dispositivo
    #Function to get the list of Tempico devices
    def add_tempicodevices(self):
        #Get devices
        ManagerDevices=PyTempicoManager()
        port_list=ManagerDevices.get_pytempico_devices()
        for i in port_list:
            self.DevicesComboBox.addItem(i)
            self.ConnectButton.setEnabled(True)

    def cancelClick(self):
        self.Dialog.close()

    def connectClick(self):
        com_value=self.DevicesComboBox.currentText()
        self.deviceConnected=tempico.TempicoDevice(com_value)
        self.Dialog.close()

        
        

    


