# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generatorSettingsDialogLLkvnq.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyTempico as tempico


class Ui_Generator(object):
    def setupUi(self, Dialog, device: tempico.TempicoDevice):
        if not Dialog.objectName():
            self.dialog=Dialog
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(331, 204)
        Dialog.setAutoFillBackground(True)
        self.device=device
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.tabChannelsWidget = QTabWidget(Dialog)
        self.tabChannelsWidget.setObjectName(u"tabChannelsWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.tabChannelsWidget.sizePolicy().hasHeightForWidth())
        self.tabChannelsWidget.setSizePolicy(sizePolicy)
        self.channelA = QWidget()
        self.channelA.setObjectName(u"channelA")
        self.verticalLayout_2 = QVBoxLayout(self.channelA)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ChannelAStartSourceFrame = QFrame(self.channelA)
        self.ChannelAStartSourceFrame.setObjectName(u"ChannelAStartSourceFrame")
        self.ChannelAStartSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelAStartSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.ChannelAStartSourceFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.channelAStartSourceLabel = QLabel(self.ChannelAStartSourceFrame)
        self.channelAStartSourceLabel.setObjectName(u"channelAStartSourceLabel")

        self.horizontalLayout_2.addWidget(self.channelAStartSourceLabel)

        self.channelAStartSourceComboBox = QComboBox(self.ChannelAStartSourceFrame)
        self.channelAStartSourceComboBox.addItem("")
        self.channelAStartSourceComboBox.addItem("")
        self.channelAStartSourceComboBox.setObjectName(u"channelAStartSourceComboBox")

        self.horizontalLayout_2.addWidget(self.channelAStartSourceComboBox)


        self.verticalLayout_2.addWidget(self.ChannelAStartSourceFrame)

        self.channelAStopSourceFrame = QFrame(self.channelA)
        self.channelAStopSourceFrame.setObjectName(u"channelAStopSourceFrame")
        self.channelAStopSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.channelAStopSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.channelAStopSourceFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.channelAStopSourceLabel = QLabel(self.channelAStopSourceFrame)
        self.channelAStopSourceLabel.setObjectName(u"channelAStopSourceLabel")

        self.horizontalLayout_3.addWidget(self.channelAStopSourceLabel)

        self.channelAStopSourceComboBox = QComboBox(self.channelAStopSourceFrame)
        self.channelAStopSourceComboBox.addItem("")
        self.channelAStopSourceComboBox.addItem("")
        self.channelAStopSourceComboBox.setObjectName(u"channelAStopSourceComboBox")

        self.horizontalLayout_3.addWidget(self.channelAStopSourceComboBox)


        self.verticalLayout_2.addWidget(self.channelAStopSourceFrame)

        self.tabChannelsWidget.addTab(self.channelA, "")
        self.channelB = QWidget()
        self.channelB.setObjectName(u"channelB")
        self.verticalLayout_4 = QVBoxLayout(self.channelB)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ChannelBStartSourceFrame = QFrame(self.channelB)
        self.ChannelBStartSourceFrame.setObjectName(u"ChannelBStartSourceFrame")
        self.ChannelBStartSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelBStartSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.ChannelBStartSourceFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.channelBStartSourceLabel = QLabel(self.ChannelBStartSourceFrame)
        self.channelBStartSourceLabel.setObjectName(u"channelBStartSourceLabel")

        self.horizontalLayout_4.addWidget(self.channelBStartSourceLabel)

        self.channelBStartSourceComboBox = QComboBox(self.ChannelBStartSourceFrame)
        self.channelBStartSourceComboBox.addItem("")
        self.channelBStartSourceComboBox.addItem("")
        self.channelBStartSourceComboBox.setObjectName(u"channelBStartSourceComboBox")

        self.horizontalLayout_4.addWidget(self.channelBStartSourceComboBox)


        self.verticalLayout_4.addWidget(self.ChannelBStartSourceFrame)

        self.ChannelBStopSourceFrame = QFrame(self.channelB)
        self.ChannelBStopSourceFrame.setObjectName(u"ChannelBStopSourceFrame")
        self.ChannelBStopSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelBStopSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.ChannelBStopSourceFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.channelBStopSourceLabel = QLabel(self.ChannelBStopSourceFrame)
        self.channelBStopSourceLabel.setObjectName(u"channelBStopSourceLabel")

        self.horizontalLayout_5.addWidget(self.channelBStopSourceLabel)

        self.channelBStopSourceComboBox = QComboBox(self.ChannelBStopSourceFrame)
        self.channelBStopSourceComboBox.addItem("")
        self.channelBStopSourceComboBox.addItem("")
        self.channelBStopSourceComboBox.setObjectName(u"channelBStopSourceComboBox")

        self.horizontalLayout_5.addWidget(self.channelBStopSourceComboBox)


        self.verticalLayout_4.addWidget(self.ChannelBStopSourceFrame)

        self.tabChannelsWidget.addTab(self.channelB, "")
        self.channelC = QWidget()
        self.channelC.setObjectName(u"channelC")
        self.verticalLayout_5 = QVBoxLayout(self.channelC)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.ChannelCStartSourceFrame = QFrame(self.channelC)
        self.ChannelCStartSourceFrame.setObjectName(u"ChannelCStartSourceFrame")
        self.ChannelCStartSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelCStartSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.ChannelCStartSourceFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.channelCStartSourceLabel = QLabel(self.ChannelCStartSourceFrame)
        self.channelCStartSourceLabel.setObjectName(u"channelCStartSourceLabel")

        self.horizontalLayout_6.addWidget(self.channelCStartSourceLabel)

        self.channelCStartSourceComboBox = QComboBox(self.ChannelCStartSourceFrame)
        self.channelCStartSourceComboBox.addItem("")
        self.channelCStartSourceComboBox.addItem("")
        self.channelCStartSourceComboBox.setObjectName(u"channelCStartSourceComboBox")

        self.horizontalLayout_6.addWidget(self.channelCStartSourceComboBox)


        self.verticalLayout_5.addWidget(self.ChannelCStartSourceFrame)

        self.ChannelCStopSourceFrame = QFrame(self.channelC)
        self.ChannelCStopSourceFrame.setObjectName(u"ChannelCStopSourceFrame")
        self.ChannelCStopSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelCStopSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.ChannelCStopSourceFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.channelCStopSourceLabel = QLabel(self.ChannelCStopSourceFrame)
        self.channelCStopSourceLabel.setObjectName(u"channelCStopSourceLabel")

        self.horizontalLayout_7.addWidget(self.channelCStopSourceLabel)

        self.channelCStopSourceComboBox = QComboBox(self.ChannelCStopSourceFrame)
        self.channelCStopSourceComboBox.addItem("")
        self.channelCStopSourceComboBox.addItem("")
        self.channelCStopSourceComboBox.setObjectName(u"channelCStopSourceComboBox")

        self.horizontalLayout_7.addWidget(self.channelCStopSourceComboBox)


        self.verticalLayout_5.addWidget(self.ChannelCStopSourceFrame)

        self.tabChannelsWidget.addTab(self.channelC, "")
        self.channelD = QWidget()
        self.channelD.setObjectName(u"channelD")
        self.verticalLayout_6 = QVBoxLayout(self.channelD)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.ChannelDStartSourceFrame = QFrame(self.channelD)
        self.ChannelDStartSourceFrame.setObjectName(u"ChannelDStartSourceFrame")
        self.ChannelDStartSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelDStartSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.ChannelDStartSourceFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.channelDStartSourceLabel = QLabel(self.ChannelDStartSourceFrame)
        self.channelDStartSourceLabel.setObjectName(u"channelDStartSourceLabel")

        self.horizontalLayout_8.addWidget(self.channelDStartSourceLabel)

        self.channelDStartSourceComboBox = QComboBox(self.ChannelDStartSourceFrame)
        self.channelDStartSourceComboBox.addItem("")
        self.channelDStartSourceComboBox.addItem("")
        self.channelDStartSourceComboBox.setObjectName(u"channelDStartSourceComboBox")

        self.horizontalLayout_8.addWidget(self.channelDStartSourceComboBox)


        self.verticalLayout_6.addWidget(self.ChannelDStartSourceFrame)

        self.ChannelDStopSourceFrame = QFrame(self.channelD)
        self.ChannelDStopSourceFrame.setObjectName(u"ChannelDStopSourceFrame")
        self.ChannelDStopSourceFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelDStopSourceFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.ChannelDStopSourceFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.channelDStopSourceLabel = QLabel(self.ChannelDStopSourceFrame)
        self.channelDStopSourceLabel.setObjectName(u"channelDStopSourceLabel")

        self.horizontalLayout_9.addWidget(self.channelDStopSourceLabel)

        self.channelDStopSourceComboBox = QComboBox(self.ChannelDStopSourceFrame)
        self.channelDStopSourceComboBox.addItem("")
        self.channelDStopSourceComboBox.addItem("")
        self.channelDStopSourceComboBox.setObjectName(u"channelDStopSourceComboBox")

        self.horizontalLayout_9.addWidget(self.channelDStopSourceComboBox)


        self.verticalLayout_6.addWidget(self.ChannelDStopSourceFrame)

        self.tabChannelsWidget.addTab(self.channelD, "")

        self.verticalLayout.addWidget(self.tabChannelsWidget)

        self.GeneratorFrequencyFrame = QFrame(Dialog)
        self.GeneratorFrequencyFrame.setObjectName(u"GeneratorFrequencyFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.GeneratorFrequencyFrame.sizePolicy().hasHeightForWidth())
        self.GeneratorFrequencyFrame.setSizePolicy(sizePolicy1)
        self.GeneratorFrequencyFrame.setFrameShape(QFrame.StyledPanel)
        self.GeneratorFrequencyFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.GeneratorFrequencyFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.FrequencyFrame = QFrame(self.GeneratorFrequencyFrame)
        self.FrequencyFrame.setObjectName(u"FrequencyFrame")
        self.FrequencyFrame.setFrameShape(QFrame.StyledPanel)
        self.FrequencyFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.FrequencyFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.generatorFrequencyLabel = QLabel(self.FrequencyFrame)
        self.generatorFrequencyLabel.setObjectName(u"generatorFrequencyLabel")

        self.horizontalLayout.addWidget(self.generatorFrequencyLabel)

        self.generatorFrequencySpinBox = QSpinBox(self.FrequencyFrame)
        self.generatorFrequencySpinBox.setObjectName(u"generatorFrequencySpinBox")
        self.generatorFrequencySpinBox.setMinimum(10)
        self.generatorFrequencySpinBox.setMaximum(10000000)
        self.generatorFrequencySpinBox.setAlignment(Qt.AlignRight)

        self.horizontalLayout.addWidget(self.generatorFrequencySpinBox)


        self.verticalLayout_3.addWidget(self.FrequencyFrame)


        self.verticalLayout.addWidget(self.GeneratorFrequencyFrame)

        self.applyChangesButton = QPushButton(Dialog)
        self.applyChangesButton.setObjectName(u"applyChangesButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.applyChangesButton.sizePolicy().hasHeightForWidth())
        self.applyChangesButton.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.applyChangesButton)


        self.retranslateUi(Dialog)

        self.tabChannelsWidget.setCurrentIndex(0)
        self.applyChangesButton.clicked.connect(self.applyChanges)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Signal generator settings", None))
        self.channelAStartSourceLabel.setText(QCoreApplication.translate("Dialog", u"Start source:", None))
        self.channelAStartSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelAStartSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.channelAStopSourceLabel.setText(QCoreApplication.translate("Dialog", u"Stop source:", None))
        self.channelAStopSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelAStopSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.tabChannelsWidget.setTabText(self.tabChannelsWidget.indexOf(self.channelA), QCoreApplication.translate("Dialog", u"Channel A", None))
        self.channelBStartSourceLabel.setText(QCoreApplication.translate("Dialog", u"Start source:", None))
        self.channelBStartSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelBStartSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.channelBStopSourceLabel.setText(QCoreApplication.translate("Dialog", u"Stop source:", None))
        self.channelBStopSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelBStopSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.tabChannelsWidget.setTabText(self.tabChannelsWidget.indexOf(self.channelB), QCoreApplication.translate("Dialog", u"Channel B", None))
        self.channelCStartSourceLabel.setText(QCoreApplication.translate("Dialog", u"Start source:", None))
        self.channelCStartSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelCStartSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.channelCStopSourceLabel.setText(QCoreApplication.translate("Dialog", u"Stop source:", None))
        self.channelCStopSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelCStopSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.tabChannelsWidget.setTabText(self.tabChannelsWidget.indexOf(self.channelC), QCoreApplication.translate("Dialog", u"Channel C", None))
        self.channelDStartSourceLabel.setText(QCoreApplication.translate("Dialog", u"Start source:", None))
        self.channelDStartSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelDStartSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.channelDStopSourceLabel.setText(QCoreApplication.translate("Dialog", u"Stop source:", None))
        self.channelDStopSourceComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"External", None))
        self.channelDStopSourceComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Internal", None))

        self.tabChannelsWidget.setTabText(self.tabChannelsWidget.indexOf(self.channelD), QCoreApplication.translate("Dialog", u"Channel D", None))
        self.generatorFrequencyLabel.setText(QCoreApplication.translate("Dialog", u"Generator frequency:", None))
        self.generatorFrequencySpinBox.setSuffix(QCoreApplication.translate("Dialog", u" Hz", None))
        self.applyChangesButton.setText(QCoreApplication.translate("Dialog", u"Apply changes", None))
    # retranslateUi


    
    def getGeneratorSettings(self):
        #General
        self.generatorFrequency=self.device.getGeneratorFrequency()
        self.generatorFrequencySpinBox.setValue(int(self.generatorFrequency))
        #Channel A
        self.startSourceChannelA=self.device.getStartSource(1)
        self.stopSourceChannelA=self.device.getStopSource(1)
        if self.startSourceChannelA=="EXTERNAL":
            self.channelAStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelAStartSourceComboBox.setCurrentIndex(1)
        if self.stopSourceChannelA=="EXTERNAL":
            self.channelAStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelAStopSourceComboBox.setCurrentIndex(1)
        #Channel B
        self.startSourceChannelB=self.device.getStartSource(2)
        self.stopSourceChannelB=self.device.getStopSource(2)
        if self.startSourceChannelB=="EXTERNAL":
            self.channelBStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelBStartSourceComboBox.setCurrentIndex(1)
        if self.stopSourceChannelB=="EXTERNAL":
            self.channelBStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelBStopSourceComboBox.setCurrentIndex(1)
        #Channel C
        self.startSourceChannelC=self.device.getStartSource(3)
        self.stopSourceChannelC=self.device.getStopSource(3)
        if self.startSourceChannelC=="EXTERNAL":
            self.channelCStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelCStartSourceComboBox.setCurrentIndex(1)
        if self.stopSourceChannelC=="EXTERNAL":
            self.channelCStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelCStopSourceComboBox.setCurrentIndex(1)
        #Channel D
        self.startSourceChannelD=self.device.getStartSource(4)
        self.stopSourceChannelD=self.device.getStopSource(4)
        if self.startSourceChannelD=="EXTERNAL":
            self.channelDStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelDStartSourceComboBox.setCurrentIndex(1)
        if self.stopSourceChannelD=="EXTERNAL":
            self.channelDStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelDStopSourceComboBox.setCurrentIndex(1)
    
    
    def onlyRead(self):
        #General configs
        self.generatorFrequencySpinBox.setEnabled(False)
        #Channel A configs
        self.channelAStartSourceComboBox.setEnabled(False)
        self.channelAStopSourceComboBox.setEnabled(False)
        #Channel B configs
        self.channelBStartSourceComboBox.setEnabled(False)
        self.channelBStopSourceComboBox.setEnabled(False)
        #Channel C configs
        self.channelCStartSourceComboBox.setEnabled(False)
        self.channelCStopSourceComboBox.setEnabled(False)
        #Channel D configs
        self.channelDStartSourceComboBox.setEnabled(False)
        self.channelDStopSourceComboBox.setEnabled(False)
    
    def enableValues(self):
        #General configs
        self.generatorFrequencySpinBox.setEnabled(True)
        #Channel A configs
        self.channelAStartSourceComboBox.setEnabled(True)
        self.channelAStopSourceComboBox.setEnabled(True)
        #Channel B configs
        self.channelBStartSourceComboBox.setEnabled(True)
        self.channelBStopSourceComboBox.setEnabled(True)
        #Channel C configs
        self.channelCStartSourceComboBox.setEnabled(True)
        self.channelCStopSourceComboBox.setEnabled(True)
        #Channel D configs
        self.channelDStartSourceComboBox.setEnabled(True)
        self.channelDStopSourceComboBox.setEnabled(True)
    
    def applyChanges(self):
        needDiscrepanceDialog=False
        generatorFrequency=self.generatorFrequencySpinBox.value()
        if float(generatorFrequency)!= self.generatorFrequency:
            self.device.setGeneratorFrequency(generatorFrequency)
        frequencyApplied=self.device.getGeneratorFrequency()
        if generatorFrequency!=frequencyApplied:
            needDiscrepanceDialog=True
        #Channel A
        startSourceChannelA=self.channelAStartSourceComboBox.currentIndex()
        stopSourceChannelA=self.channelAStopSourceComboBox.currentIndex()
        if startSourceChannelA==0 and self.startSourceChannelA!="EXTERNAL":
            self.device.setStartExternalSource(1)
        elif startSourceChannelA==1 and self.startSourceChannelA!="INTERNAL":
            self.device.setStartInternalSource(1)
        
        if stopSourceChannelA==0 and self.stopSourceChannelA!="EXTERNAL":
            self.device.setStopExternalSource(1)
        elif stopSourceChannelA==1 and self.stopSourceChannelA!="INTERNAL":
            self.device.setStopInternalSource(1)
        #Channel B
        startSourceChannelB=self.channelBStartSourceComboBox.currentIndex()
        stopSourceChannelB=self.channelBStopSourceComboBox.currentIndex()
        
        if startSourceChannelB==0 and self.startSourceChannelB!="EXTERNAL":
            self.device.setStartExternalSource(2)
        elif startSourceChannelB==1 and self.startSourceChannelB!="INTERNAL":
            self.device.setStartInternalSource(2)
        
        if stopSourceChannelB==0 and self.stopSourceChannelB!="EXTERNAL":
            self.device.setStopExternalSource(2)
        elif stopSourceChannelB==1 and self.stopSourceChannelB!="INTERNAL":
            self.device.setStopInternalSource(2)
        #Channel C
        startSourceChannelC=self.channelCStartSourceComboBox.currentIndex()
        stopSourceChannelC=self.channelCStopSourceComboBox.currentIndex()
        
        if startSourceChannelC==0 and self.startSourceChannelC!="EXTERNAL":
            self.device.setStartExternalSource(3)
        elif startSourceChannelC==1 and self.startSourceChannelC!="INTERNAL":
            self.device.setStartInternalSource(3)
        
        if stopSourceChannelC==0 and self.stopSourceChannelC!="EXTERNAL":
            self.device.setStopExternalSource(3)
        elif stopSourceChannelC==1 and self.stopSourceChannelC!="INTERNAL":
            self.device.setStopInternalSource(3)
        #Channel D
        startSourceChannelD=self.channelDStartSourceComboBox.currentIndex()
        stopSourceChannelD=self.channelDStopSourceComboBox.currentIndex()
        
        if startSourceChannelD==0 and self.startSourceChannelD!="EXTERNAL":
            self.device.setStartExternalSource(4)
        elif startSourceChannelD==1 and self.startSourceChannelD!="INTERNAL":
            self.device.setStartInternalSource(4)
        
        if stopSourceChannelD==0 and self.stopSourceChannelD!="EXTERNAL":
            self.device.setStopExternalSource(4)
        elif stopSourceChannelD==1 and self.stopSourceChannelD!="INTERNAL":
            self.device.setStopInternalSource(4)
        self.dialog.accept()
        if needDiscrepanceDialog:
            self.dialogMessageWithDiscrepances(int(frequencyApplied))
    

    
    def dialogMessageWithDiscrepances(self, appliedValue):

        message = (
            "The generator signal could not be set to the exact requested value;\n"
            f"however, the closest possible value was applied: {appliedValue} Hz."
        )

        msg_box = QMessageBox(self.dialog.parent())
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Generator Configuration Notice")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def setConfigOnlyRead(self, valuesList):
        #General
        self.generatorFrequencySpinBox.setValue(valuesList[0])
        #Channel A
        if valuesList[1]=="EXTERNAL":
            self.channelAStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelAStartSourceComboBox.setCurrentIndex(1)
        if valuesList[2]=="EXTERNAL":
            self.channelAStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelAStopSourceComboBox.setCurrentIndex(1)
        #Channel B
        if valuesList[3]=="EXTERNAL":
            self.channelBStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelBStartSourceComboBox.setCurrentIndex(1)
        if valuesList[4]=="EXTERNAL":
            self.channelBStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelBStopSourceComboBox.setCurrentIndex(1)
        #Channel C
        if valuesList[5]=="EXTERNAL":
            self.channelCStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelCStartSourceComboBox.setCurrentIndex(1)
        if valuesList[6]=="EXTERNAL":
            self.channelCStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelCStopSourceComboBox.setCurrentIndex(1)
        #Channel D
        if valuesList[7]=="EXTERNAL":
            self.channelDStartSourceComboBox.setCurrentIndex(0)
        else:
            self.channelDStartSourceComboBox.setCurrentIndex(1)
        if valuesList[8]=="EXTERNAL":
            self.channelDStopSourceComboBox.setCurrentIndex(0)
        else:
            self.channelDStopSourceComboBox.setCurrentIndex(1)
        self.onlyRead()
        
    
        