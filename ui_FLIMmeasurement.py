# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FLIMmeasurementLNLkHv.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import matplotlib.pyplot as plt
import io


class UiFLIM(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(922, 772)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ConfigurationRunParameters = QFrame(Form)
        self.ConfigurationRunParameters.setObjectName(u"ConfigurationRunParameters")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConfigurationRunParameters.sizePolicy().hasHeightForWidth())
        self.ConfigurationRunParameters.setSizePolicy(sizePolicy)
        self.ConfigurationRunParameters.setAutoFillBackground(True)
        self.ConfigurationRunParameters.setFrameShape(QFrame.StyledPanel)
        self.ConfigurationRunParameters.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.ConfigurationRunParameters)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.configurationParameters = QFrame(self.ConfigurationRunParameters)
        self.configurationParameters.setObjectName(u"configurationParameters")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(6)
        sizePolicy1.setHeightForWidth(self.configurationParameters.sizePolicy().hasHeightForWidth())
        self.configurationParameters.setSizePolicy(sizePolicy1)
        self.configurationParameters.setFrameShape(QFrame.Panel)
        self.configurationParameters.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.configurationParameters)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.startChannelLabel = QLabel(self.configurationParameters)
        self.startChannelLabel.setObjectName(u"startChannelLabel")

        self.verticalLayout_3.addWidget(self.startChannelLabel)

        self.startChannelComboBox = QComboBox(self.configurationParameters)
        self.startChannelComboBox.addItem("")
        self.startChannelComboBox.addItem("")
        self.startChannelComboBox.addItem("")
        self.startChannelComboBox.addItem("")
        self.startChannelComboBox.addItem("")
        self.startChannelComboBox.setObjectName(u"startChannelComboBox")

        self.verticalLayout_3.addWidget(self.startChannelComboBox)

        self.stopChannelLabel = QLabel(self.configurationParameters)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")

        self.verticalLayout_3.addWidget(self.stopChannelLabel)

        self.stopChannelComboBox = QComboBox(self.configurationParameters)
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.addItem("")
        self.stopChannelComboBox.setObjectName(u"stopChannelComboBox")

        self.verticalLayout_3.addWidget(self.stopChannelComboBox)

        self.binWidthLabel = QLabel(self.configurationParameters)
        self.binWidthLabel.setObjectName(u"binWidthLabel")

        self.verticalLayout_3.addWidget(self.binWidthLabel)

        self.binWidthComboBox = QComboBox(self.configurationParameters)
        self.binWidthComboBox.setObjectName(u"binWidthComboBox")
        self.powers_of_two = [ "480 ps", "960 ps", "2 ns", "4 ns", "8 ns", 
                              "16 ns", "32 ns", "64 ns", "128 ns", "256 ns",
                              "512 ns", "1 µs", "2 µs", "4 µs", "8 µs", "16 µs",
                              "32 µs", "64 µs", "100 µs"]
        self.binWidthComboBox.addItems(self.powers_of_two)

        self.verticalLayout_3.addWidget(self.binWidthComboBox)

        self.numberMeasurementsLabel = QLabel(self.configurationParameters)
        self.numberMeasurementsLabel.setObjectName(u"numberMeasurementsLabel")

        self.verticalLayout_3.addWidget(self.numberMeasurementsLabel)

        self.numberMeasurementsSpinBox = QSpinBox(self.configurationParameters)
        self.numberMeasurementsSpinBox.setObjectName(u"numberMeasurementsSpinBox")
        self.numberMeasurementsSpinBox.setMinimum(1000)
        self.numberMeasurementsSpinBox.setMaximum(20000)

        self.verticalLayout_3.addWidget(self.numberMeasurementsSpinBox)

        self.startStopClearFrame = QFrame(self.configurationParameters)
        self.startStopClearFrame.setObjectName(u"startStopClearFrame")
        self.startStopClearFrame.setFrameShape(QFrame.StyledPanel)
        self.startStopClearFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.startStopClearFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.startButton = QPushButton(self.startStopClearFrame)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_2.addWidget(self.startButton)

        self.stopButton = QPushButton(self.startStopClearFrame)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_2.addWidget(self.stopButton)

        self.clearButton = QPushButton(self.startStopClearFrame)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout_2.addWidget(self.clearButton)


        self.verticalLayout_3.addWidget(self.startStopClearFrame)

        self.saveDataPlotFrame = QFrame(self.configurationParameters)
        self.saveDataPlotFrame.setObjectName(u"saveDataPlotFrame")
        self.saveDataPlotFrame.setFrameShape(QFrame.StyledPanel)
        self.saveDataPlotFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.saveDataPlotFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.saveDataFileButton = QPushButton(self.saveDataPlotFrame)
        self.saveDataFileButton.setObjectName(u"saveDataFileButton")

        self.horizontalLayout_3.addWidget(self.saveDataFileButton)

        self.savePlotButton = QPushButton(self.saveDataPlotFrame)
        self.savePlotButton.setObjectName(u"savePlotButton")

        self.horizontalLayout_3.addWidget(self.savePlotButton)


        self.verticalLayout_3.addWidget(self.saveDataPlotFrame)

        self.binWidthComboBox.raise_()
        self.startChannelLabel.raise_()
        self.startChannelComboBox.raise_()
        self.stopChannelLabel.raise_()
        self.stopChannelComboBox.raise_()
        self.binWidthLabel.raise_()
        self.numberMeasurementsLabel.raise_()
        self.numberMeasurementsSpinBox.raise_()
        self.startStopClearFrame.raise_()
        self.saveDataPlotFrame.raise_()

        self.verticalLayout.addWidget(self.configurationParameters)

        self.runParameters = QFrame(self.ConfigurationRunParameters)
        self.runParameters.setObjectName(u"runParameters")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.runParameters.sizePolicy().hasHeightForWidth())
        self.runParameters.setSizePolicy(sizePolicy2)
        self.runParameters.setFrameShape(QFrame.Panel)
        self.runParameters.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_4 = QVBoxLayout(self.runParameters)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.totalMeasurementsFrame = QFrame(self.runParameters)
        self.totalMeasurementsFrame.setObjectName(u"totalMeasurementsFrame")
        self.totalMeasurementsFrame.setFrameShape(QFrame.StyledPanel)
        self.totalMeasurementsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.totalMeasurementsFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.totalMeasurementsLabel = QLabel(self.totalMeasurementsFrame)
        self.totalMeasurementsLabel.setObjectName(u"totalMeasurementsLabel")

        self.horizontalLayout_5.addWidget(self.totalMeasurementsLabel)

        self.totalMeasurementsValue = QLabel(self.totalMeasurementsFrame)
        self.totalMeasurementsValue.setObjectName(u"totalMeasurementsValue")

        self.horizontalLayout_5.addWidget(self.totalMeasurementsValue)


        self.verticalLayout_4.addWidget(self.totalMeasurementsFrame)

        self.totalStartsFrame = QFrame(self.runParameters)
        self.totalStartsFrame.setObjectName(u"totalStartsFrame")
        self.totalStartsFrame.setFrameShape(QFrame.StyledPanel)
        self.totalStartsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.totalStartsFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.totalStartsLabel = QLabel(self.totalStartsFrame)
        self.totalStartsLabel.setObjectName(u"totalStartsLabel")

        self.horizontalLayout_6.addWidget(self.totalStartsLabel)

        self.totalStartsValue = QLabel(self.totalStartsFrame)
        self.totalStartsValue.setObjectName(u"totalStartsValue")

        self.horizontalLayout_6.addWidget(self.totalStartsValue)


        self.verticalLayout_4.addWidget(self.totalStartsFrame)

        self.totalStopsFrame = QFrame(self.runParameters)
        self.totalStopsFrame.setObjectName(u"totalStopsFrame")
        self.totalStopsFrame.setFrameShape(QFrame.StyledPanel)
        self.totalStopsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.totalStopsFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.totalStopsLabel = QLabel(self.totalStopsFrame)
        self.totalStopsLabel.setObjectName(u"totalStopsLabel")

        self.horizontalLayout_7.addWidget(self.totalStopsLabel)

        self.totalStopsValue = QLabel(self.totalStopsFrame)
        self.totalStopsValue.setObjectName(u"totalStopsValue")

        self.horizontalLayout_7.addWidget(self.totalStopsValue)


        self.verticalLayout_4.addWidget(self.totalStopsFrame)


        self.verticalLayout.addWidget(self.runParameters)


        self.horizontalLayout.addWidget(self.ConfigurationRunParameters)

        self.fitGraphicStatusFrame = QFrame(Form)
        self.fitGraphicStatusFrame.setObjectName(u"fitGraphicStatusFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(7)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.fitGraphicStatusFrame.sizePolicy().hasHeightForWidth())
        self.fitGraphicStatusFrame.setSizePolicy(sizePolicy3)
        self.fitGraphicStatusFrame.setAutoFillBackground(True)
        self.fitGraphicStatusFrame.setFrameShape(QFrame.StyledPanel)
        self.fitGraphicStatusFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.fitGraphicStatusFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.fitFrame = QFrame(self.fitGraphicStatusFrame)
        self.fitFrame.setObjectName(u"fitFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(20)
        sizePolicy4.setHeightForWidth(self.fitFrame.sizePolicy().hasHeightForWidth())
        self.fitFrame.setSizePolicy(sizePolicy4)
        self.fitFrame.setFrameShape(QFrame.Panel)
        self.fitFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_8 = QHBoxLayout(self.fitFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.fitFunctionFrame = QFrame(self.fitFrame)
        self.fitFunctionFrame.setObjectName(u"fitFunctionFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(6)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.fitFunctionFrame.sizePolicy().hasHeightForWidth())
        self.fitFunctionFrame.setSizePolicy(sizePolicy5)
        self.fitFunctionFrame.setFrameShape(QFrame.Panel)
        self.fitFunctionFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_5 = QVBoxLayout(self.fitFunctionFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.functionFrame = QFrame(self.fitFunctionFrame)
        self.functionFrame.setObjectName(u"functionFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(3)
        sizePolicy6.setHeightForWidth(self.functionFrame.sizePolicy().hasHeightForWidth())
        self.functionFrame.setSizePolicy(sizePolicy6)
        self.functionFrame.setFrameShape(QFrame.Panel)
        self.functionFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_9 = QHBoxLayout(self.functionFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.functionLabel = QLabel(self.functionFrame)
        self.functionLabel.setObjectName(u"functionLabel")

        self.horizontalLayout_9.addWidget(self.functionLabel)

        self.functionComboBox = QComboBox(self.functionFrame)
        self.functionComboBox.setObjectName(u"functionComboBox")
        self.functionsFit = ["Exponential","Kohlrausch","Shifted exponencial"]
        self.functionComboBox.addItems(self.functionsFit)

        self.horizontalLayout_9.addWidget(self.functionComboBox)
        self.functionComboBox.currentIndexChanged.connect(self.functionChange)


        self.verticalLayout_5.addWidget(self.functionFrame)

        self.equationFrame = QFrame(self.fitFunctionFrame)
        self.equationFrame.setObjectName(u"equationFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(7)
        sizePolicy7.setHeightForWidth(self.equationFrame.sizePolicy().hasHeightForWidth())
        self.equationFrame.setSizePolicy(sizePolicy7)
        self.equationFrame.setFrameShape(QFrame.Panel)
        self.equationFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_6 = QVBoxLayout(self.equationFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.equationLabel = QLabel(self.equationFrame)
        self.applyButtton = QPushButton(self.equationFrame)
        self.applyButtton.setText("Apply")
        self.equationLabel.setObjectName(u"equationLabel")
        self.verticalLayout_6.addWidget(self.equationLabel, 0, Qt.AlignHCenter)
        self.verticalLayout_6.addWidget(self.applyButtton)
        self.verticalLayout_5.addWidget(self.equationFrame)


        self.horizontalLayout_8.addWidget(self.fitFunctionFrame)

        self.fitParametersFrame = QFrame(self.fitFrame)
        self.fitParametersFrame.setObjectName(u"fitParametersFrame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(4)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.fitParametersFrame.sizePolicy().hasHeightForWidth())
        self.fitParametersFrame.setSizePolicy(sizePolicy8)
        self.fitParametersFrame.setFrameShape(QFrame.Panel)
        self.fitParametersFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_7 = QVBoxLayout(self.fitParametersFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.fitParametersLabelFrame = QFrame(self.fitParametersFrame)
        self.fitParametersLabelFrame.setObjectName(u"fitParametersLabelFrame")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(2)
        sizePolicy9.setHeightForWidth(self.fitParametersLabelFrame.sizePolicy().hasHeightForWidth())
        self.fitParametersLabelFrame.setSizePolicy(sizePolicy9)
        self.fitParametersLabelFrame.setFrameShape(QFrame.StyledPanel)
        self.fitParametersLabelFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.fitParametersLabelFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.fitParametersLabel = QLabel(self.fitParametersLabelFrame)
        self.fitParametersLabel.setObjectName(u"fitParametersLabel")

        self.horizontalLayout_10.addWidget(self.fitParametersLabel)


        self.verticalLayout_7.addWidget(self.fitParametersLabelFrame)

        self.parametersFrame = QFrame(self.fitParametersFrame)
        self.parametersFrame.setObjectName(u"parametersFrame")
        sizePolicy2.setHeightForWidth(self.parametersFrame.sizePolicy().hasHeightForWidth())
        self.parametersFrame.setSizePolicy(sizePolicy2)
        self.parametersFrame.setFrameShape(QFrame.StyledPanel)
        self.parametersFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.parametersFrame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.firstParameterFrame = QFrame(self.parametersFrame)
        self.firstParameterFrame.setObjectName(u"firstParameterFrame")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(5)
        sizePolicy10.setHeightForWidth(self.firstParameterFrame.sizePolicy().hasHeightForWidth())
        self.firstParameterFrame.setSizePolicy(sizePolicy10)
        self.firstParameterFrame.setFrameShape(QFrame.StyledPanel)
        self.firstParameterFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.firstParameterFrame)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.firstParameterLabel = QLabel(self.firstParameterFrame)
        self.firstParameterLabel.setObjectName(u"firstParameterLabel")

        self.horizontalLayout_12.addWidget(self.firstParameterLabel)

        self.firstParameterValue = QLabel(self.firstParameterFrame)
        self.firstParameterValue.setObjectName(u"firstParameterValue")

        self.horizontalLayout_12.addWidget(self.firstParameterValue)


        self.verticalLayout_8.addWidget(self.firstParameterFrame)

        self.secondParameterFrame = QFrame(self.parametersFrame)
        self.secondParameterFrame.setObjectName(u"secondParameterFrame")
        sizePolicy10.setHeightForWidth(self.secondParameterFrame.sizePolicy().hasHeightForWidth())
        self.secondParameterFrame.setSizePolicy(sizePolicy10)
        self.secondParameterFrame.setFrameShape(QFrame.StyledPanel)
        self.secondParameterFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.secondParameterFrame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.secondParameterLabel = QLabel(self.secondParameterFrame)
        self.secondParameterLabel.setObjectName(u"secondParameterLabel")

        self.horizontalLayout_13.addWidget(self.secondParameterLabel)

        self.secondParameterValue = QLabel(self.secondParameterFrame)
        self.secondParameterValue.setObjectName(u"secondParameterValue")

        self.horizontalLayout_13.addWidget(self.secondParameterValue)


        self.verticalLayout_8.addWidget(self.secondParameterFrame)
        
        #Begin third parameter
        
        self.thirdParameterFrame = QFrame(self.parametersFrame)
        self.thirdParameterFrame.setObjectName(u"secondParameterFrame")
        sizePolicy10.setHeightForWidth(self.thirdParameterFrame.sizePolicy().hasHeightForWidth())
        self.thirdParameterFrame.setSizePolicy(sizePolicy10)
        self.thirdParameterFrame.setFrameShape(QFrame.StyledPanel)
        self.thirdParameterFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_thirdParameter = QHBoxLayout(self.thirdParameterFrame)
        self.horizontalLayout_thirdParameter.setObjectName(u"horizontalLayout_thirdParameter")
        self.thirdParameterLabel = QLabel(self.thirdParameterFrame)
        self.thirdParameterLabel.setObjectName(u"thirdParameterLabel")

        self.horizontalLayout_thirdParameter.addWidget(self.thirdParameterLabel)

        self.thirdParameterValue = QLabel(self.thirdParameterFrame)
        self.thirdParameterFrame.setObjectName(u"secondParameterValue")

        self.horizontalLayout_thirdParameter.addWidget(self.thirdParameterValue)


        self.verticalLayout_8.addWidget(self.thirdParameterFrame)
        
        #End third parameter
        
        
        #Begin fourth parameter
        self.fourthParameterFrame = QFrame(self.parametersFrame)
        self.fourthParameterFrame.setObjectName(u"secondParameterFrame")
        sizePolicy10.setHeightForWidth(self.thirdParameterFrame.sizePolicy().hasHeightForWidth())
        self.fourthParameterFrame.setSizePolicy(sizePolicy10)
        self.fourthParameterFrame.setFrameShape(QFrame.StyledPanel)
        self.fourthParameterFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_fourthParameter = QHBoxLayout(self.fourthParameterFrame)
        self.horizontalLayout_fourthParameter.setObjectName(u"horizontalLayout_fourthParameter")
        self.fourthParameterLabel = QLabel(self.fourthParameterFrame)
        self.fourthParameterLabel.setObjectName(u"fourthParameterLabel")

        self.horizontalLayout_fourthParameter.addWidget(self.fourthParameterLabel)

        self.fourthParameterValue = QLabel(self.fourthParameterFrame)
        self.fourthParameterFrame.setObjectName(u"secondParameterValue")

        self.horizontalLayout_fourthParameter.addWidget(self.fourthParameterValue)


        self.verticalLayout_8.addWidget(self.fourthParameterFrame)
        
        #End fourth parameter

        self.verticalLayout_7.addWidget(self.parametersFrame)


        self.horizontalLayout_8.addWidget(self.fitParametersFrame)


        self.verticalLayout_2.addWidget(self.fitFrame)

        self.graphicFrame = QFrame(self.fitGraphicStatusFrame)
        self.graphicFrame.setObjectName(u"graphicFrame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(76)
        sizePolicy11.setHeightForWidth(self.graphicFrame.sizePolicy().hasHeightForWidth())
        self.graphicFrame.setSizePolicy(sizePolicy11)
        self.graphicFrame.setFrameShape(QFrame.Panel)
        self.graphicFrame.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.graphicFrame)

        self.statusFrame = QFrame(self.fitGraphicStatusFrame)
        self.statusFrame.setObjectName(u"statusFrame")
        sizePolicy2.setHeightForWidth(self.statusFrame.sizePolicy().hasHeightForWidth())
        self.statusFrame.setSizePolicy(sizePolicy2)
        self.statusFrame.setFrameShape(QFrame.Panel)
        self.statusFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_11 = QHBoxLayout(self.statusFrame)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.statusLabel = QLabel(self.statusFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(16)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy12)

        self.horizontalLayout_11.addWidget(self.statusLabel)

        self.statusValue = QLabel(self.statusFrame)
        self.statusValue.setObjectName(u"statusValue")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(75)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.statusValue.sizePolicy().hasHeightForWidth())
        self.statusValue.setSizePolicy(sizePolicy13)

        self.horizontalLayout_11.addWidget(self.statusValue)

        self.drawPointLabel = QLabel(self.statusFrame)
        self.drawPointLabel.setObjectName(u"drawPointLabel")
        sizePolicy14 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(9)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.drawPointLabel.sizePolicy().hasHeightForWidth())
        self.drawPointLabel.setSizePolicy(sizePolicy14)

        self.horizontalLayout_11.addWidget(self.drawPointLabel, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.statusFrame)


        self.horizontalLayout.addWidget(self.fitGraphicStatusFrame)


        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
        self.drawColorPoint()
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.startChannelLabel.setText(QCoreApplication.translate("Form", u"Start Channel:", None))
        self.set_latex_to_label(r'$I_0 e^{\frac{-t}{\tau_0}}$')
        self.startChannelComboBox.setItemText(0, QCoreApplication.translate("Form", u"Start channel", None))
        self.startChannelComboBox.setItemText(1, QCoreApplication.translate("Form", u"Channel A", None))
        self.startChannelComboBox.setItemText(2, QCoreApplication.translate("Form", u"Channel B", None))
        self.startChannelComboBox.setItemText(3, QCoreApplication.translate("Form", u"Channel C", None))
        self.startChannelComboBox.setItemText(4, QCoreApplication.translate("Form", u"Channel D", None))

        self.stopChannelLabel.setText(QCoreApplication.translate("Form", u"Stop Channel:", None))
        self.stopChannelComboBox.setItemText(0, QCoreApplication.translate("Form", u"Channel A", None))
        self.stopChannelComboBox.setItemText(1, QCoreApplication.translate("Form", u"Channel B", None))
        self.stopChannelComboBox.setItemText(2, QCoreApplication.translate("Form", u"Channel C", None))
        self.stopChannelComboBox.setItemText(3, QCoreApplication.translate("Form", u"Channel D", None))

        self.binWidthLabel.setText(QCoreApplication.translate("Form", u"Bin width:", None))
        self.numberMeasurementsLabel.setText(QCoreApplication.translate("Form", u"Number of measurements:", None))
        self.startButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.clearButton.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.saveDataFileButton.setText(QCoreApplication.translate("Form", u"Save data file", None))
        self.savePlotButton.setText(QCoreApplication.translate("Form", u"Save Plot", None))
        self.totalMeasurementsLabel.setText(QCoreApplication.translate("Form", u"Total measurements:", None))
        self.totalMeasurementsValue.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.totalStartsLabel.setText(QCoreApplication.translate("Form", u"Total Starts:", None))
        self.totalStartsValue.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.totalStopsLabel.setText(QCoreApplication.translate("Form", u"Total Time:", None))
        self.totalStopsValue.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.functionLabel.setText(QCoreApplication.translate("Form", u"Function:", None))
        self.fitParametersLabel.setText(QCoreApplication.translate("Form", u"Fit parameters:", None))
        self.firstParameterLabel.setText(QCoreApplication.translate("Form", u"I_0:", None))
        self.firstParameterValue.setText(QCoreApplication.translate("Form", u"Undefined", None))
        self.secondParameterLabel.setText(QCoreApplication.translate("Form", u"Tau_0:", None))
        self.secondParameterValue.setText(QCoreApplication.translate("Form", u"Undefined", None))
        self.statusLabel.setText(QCoreApplication.translate("Form", u"Status:", None))
        self.statusValue.setText(QCoreApplication.translate("Form", u"No measurement running", None))
        self.drawPointLabel.setText("")
    # retranslateUi

    def drawColorPoint(self):
        pixmap = QPixmap(self.drawPointLabel.size())
        pixmap.fill(Qt.transparent)  

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        painter.setBrush(QColor(128, 128, 128))  
        painter.setPen(Qt.NoPen)

        # Definir el tamaño del punto (círculo)
        point_size = min(self.drawPointLabel.width(), self.drawPointLabel.height()) // 2

        # Calcular la posición del círculo para que quede centrado
        x = (self.drawPointLabel.width() - point_size) // 2
        y = (self.drawPointLabel.height() - point_size) // 2

        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.drawPointLabel.setPixmap(pixmap)
        
    def set_latex_to_label(self, latex):
        fig, ax = plt.subplots(figsize=(3, 1))
        ax.text(0.5, 0.5, latex, fontsize=20, ha='center', va='center')
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.equationLabel.setPixmap(pixmap)
    

    
    def functionChange(self):
        if self.functionComboBox.currentText()=="Exponential":
            self.set_latex_to_label(r'$I_0 e^{\frac{-t}{\tau_0}}$')
            self.thirdParameterLabel.setText("")
            self.thirdParameterValue.setText("")
            self.fourthParameterLabel.setText("")
            self.fourthParameterValue.setText("")
        elif self.functionComboBox.currentText()=="Kohlrausch":
            self.set_latex_to_label(r'$I_0 e^{(\frac{-t}{\tau_0})^{\beta}}$')
            self.thirdParameterLabel.setText("Beta:")
            self.thirdParameterValue.setText("Undefined")
            self.fourthParameterLabel.setText("")
            self.fourthParameterValue.setText("")
        elif self.functionComboBox.currentText()=="Shifted exponencial":
            self.set_latex_to_label(r'$I_0 e^{\frac{-t+\alpha}{\tau_0}}+b$')
            self.thirdParameterLabel.setText("Alpha:")
            self.thirdParameterValue.setText("Undefined")
            self.fourthParameterLabel.setText("b:")
            self.fourthParameterValue.setText("Undefined")
            
        