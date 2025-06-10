# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CountHistBfTPQE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CountsEstimated(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(941, 739)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GraphicSettingFrame = QFrame(Form)
        self.GraphicSettingFrame.setObjectName(u"GraphicSettingFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.GraphicSettingFrame.sizePolicy().hasHeightForWidth())
        self.GraphicSettingFrame.setSizePolicy(sizePolicy)
        self.GraphicSettingFrame.setAutoFillBackground(True)
        self.GraphicSettingFrame.setFrameShape(QFrame.StyledPanel)
        self.GraphicSettingFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.GraphicSettingFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SettingsFrame = QFrame(self.GraphicSettingFrame)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy1)
        self.SettingsFrame.setFrameShape(QFrame.Panel)
        self.SettingsFrame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.SettingsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.channelLabel = QLabel(self.SettingsFrame)
        self.channelLabel.setObjectName(u"channelLabel")

        self.verticalLayout_2.addWidget(self.channelLabel)

        self.frame_7 = QFrame(self.SettingsFrame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.channelACheckBox = QCheckBox(self.frame_7)
        self.channelACheckBox.setObjectName(u"channelACheckBox")

        self.horizontalLayout_3.addWidget(self.channelACheckBox)

        self.channelCCheckBox = QCheckBox(self.frame_7)
        self.channelCCheckBox.setObjectName(u"channelCCheckBox")

        self.horizontalLayout_3.addWidget(self.channelCCheckBox)

        self.channelBCheckBox = QCheckBox(self.frame_7)
        self.channelBCheckBox.setObjectName(u"channelBCheckBox")

        self.horizontalLayout_3.addWidget(self.channelBCheckBox)

        self.channelDCheckBox = QCheckBox(self.frame_7)
        self.channelDCheckBox.setObjectName(u"channelDCheckBox")

        self.horizontalLayout_3.addWidget(self.channelDCheckBox)


        self.verticalLayout_2.addWidget(self.frame_7)

        self.StartStopButtonsFrame = QFrame(self.SettingsFrame)
        self.StartStopButtonsFrame.setObjectName(u"StartStopButtonsFrame")
        self.StartStopButtonsFrame.setFrameShape(QFrame.StyledPanel)
        self.StartStopButtonsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.StartStopButtonsFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.startMeasurementButton = QPushButton(self.StartStopButtonsFrame)
        self.startMeasurementButton.setObjectName(u"startMeasurementButton")

        self.horizontalLayout_4.addWidget(self.startMeasurementButton)

        self.stopMeasurementButton = QPushButton(self.StartStopButtonsFrame)
        self.stopMeasurementButton.setObjectName(u"stopMeasurementButton")

        self.horizontalLayout_4.addWidget(self.stopMeasurementButton)


        self.verticalLayout_2.addWidget(self.StartStopButtonsFrame)

        self.grapLabel = QLabel(self.SettingsFrame)
        self.grapLabel.setObjectName(u"grapLabel")

        self.verticalLayout_2.addWidget(self.grapLabel)

        self.SelectGraphFrame = QFrame(self.SettingsFrame)
        self.SelectGraphFrame.setObjectName(u"SelectGraphFrame")
        self.SelectGraphFrame.setFrameShape(QFrame.StyledPanel)
        self.SelectGraphFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.SelectGraphFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.mergeGraphicButton = QRadioButton(self.SelectGraphFrame)
        self.mergeGraphicButton.setObjectName(u"mergeGraphicButton")

        self.horizontalLayout_5.addWidget(self.mergeGraphicButton)

        self.separateGraphicButton = QRadioButton(self.SelectGraphFrame)
        self.separateGraphicButton.setObjectName(u"separateGraphicButton")

        self.horizontalLayout_5.addWidget(self.separateGraphicButton)
        
        self.apartDialogGraphicButton = QRadioButton(self.SelectGraphFrame)
        self.apartDialogGraphicButton.setObjectName(u"apartDialogGraphicButton")
        self.horizontalLayout_5.addWidget(self.apartDialogGraphicButton)


        self.verticalLayout_2.addWidget(self.SelectGraphFrame)
        self.tableLabel= QLabel(self.SettingsFrame)
        self.tableLabel.setText("Detached:")
        self.verticalLayout_2.addWidget(self.tableLabel)

        #FrameDeatached
        self.tableDeatachedFrame= QFrame(self.SettingsFrame)
        self.verticalLayout_2.addWidget(self.tableDeatachedFrame)
        #Horizontallayout
        self.horizontalLayoutDeatached= QHBoxLayout(self.tableDeatachedFrame)
        
        #CheckBoxDeatached Table 
        self.tableCheckBox= QCheckBox()
        self.tableCheckBox.setText("Detached table")
        self.horizontalLayoutDeatached.addWidget(self.tableCheckBox)
        #CheckBoxDeatached Labels
        self.labelCheckBox= QCheckBox()
        self.labelCheckBox.setText("Detached current mearument")
        self.horizontalLayoutDeatached.addWidget(self.labelCheckBox)
        ###
        self.timeRangeLabel = QLabel(self.SettingsFrame)
        self.timeRangeLabel.setObjectName(u"timeRangeLabel")

        self.verticalLayout_2.addWidget(self.timeRangeLabel)

        self.ComboBoxTimeRangeFrame = QFrame(self.SettingsFrame)
        self.ComboBoxTimeRangeFrame.setObjectName(u"ComboBoxTimeRangeFrame")
        self.ComboBoxTimeRangeFrame.setFrameShape(QFrame.StyledPanel)
        self.ComboBoxTimeRangeFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.ComboBoxTimeRangeFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.comboBoxTimeRange = QComboBox(self.ComboBoxTimeRangeFrame)
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.addItem("")
        self.comboBoxTimeRange.setObjectName(u"comboBoxTimeRange")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxTimeRange.sizePolicy().hasHeightForWidth())
        self.comboBoxTimeRange.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.comboBoxTimeRange)


        self.verticalLayout_2.addWidget(self.ComboBoxTimeRangeFrame)

        self.clearLabel = QLabel(self.SettingsFrame)
        self.clearLabel.setObjectName(u"clearLabel")

        self.verticalLayout_2.addWidget(self.clearLabel)

        self.ChannelABButtonFrame = QFrame(self.SettingsFrame)
        self.ChannelABButtonFrame.setObjectName(u"ChannelABButtonFrame")
        self.ChannelABButtonFrame.setFrameShape(QFrame.StyledPanel)
        self.ChannelABButtonFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.ChannelABButtonFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.channelAClearButton = QPushButton(self.ChannelABButtonFrame)
        self.channelAClearButton.setObjectName(u"channelAClearButton")

        self.horizontalLayout_7.addWidget(self.channelAClearButton)

        self.channelBClearButton = QPushButton(self.ChannelABButtonFrame)
        self.channelBClearButton.setObjectName(u"channelBClearButton")

        self.horizontalLayout_7.addWidget(self.channelBClearButton)

        self.channelCClearButton = QPushButton(self.ChannelABButtonFrame)
        self.channelCClearButton.setObjectName(u"channelCClearButton")

        self.horizontalLayout_7.addWidget(self.channelCClearButton)

        self.channelDClearButton = QPushButton(self.ChannelABButtonFrame)
        self.channelDClearButton.setObjectName(u"channelDClearButton")

        self.horizontalLayout_7.addWidget(self.channelDClearButton)


        self.verticalLayout_2.addWidget(self.ChannelABButtonFrame)

        self.SaveDataPlotsFrame = QFrame(self.SettingsFrame)
        self.SaveDataPlotsFrame.setObjectName(u"SaveDataPlotsFrame")
        self.SaveDataPlotsFrame.setFrameShape(QFrame.StyledPanel)
        self.SaveDataPlotsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.SaveDataPlotsFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.saveDataButton = QPushButton(self.SaveDataPlotsFrame)
        self.saveDataButton.setObjectName(u"saveDataButton")

        self.horizontalLayout_9.addWidget(self.saveDataButton)

        self.savePlotsButton = QPushButton(self.SaveDataPlotsFrame)
        self.savePlotsButton.setObjectName(u"savePlotsButton")

        self.horizontalLayout_9.addWidget(self.savePlotsButton)


        self.verticalLayout_2.addWidget(self.SaveDataPlotsFrame)


        self.horizontalLayout.addWidget(self.SettingsFrame)

        self.GraphicsFrame = QFrame(self.GraphicSettingFrame)
        self.GraphicsFrame.setObjectName(u"GraphicsFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(7)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.GraphicsFrame.sizePolicy().hasHeightForWidth())
        self.GraphicsFrame.setSizePolicy(sizePolicy3)
        self.GraphicsFrame.setFrameShape(QFrame.Panel)
        self.GraphicsFrame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.GraphicsFrame)


        self.verticalLayout.addWidget(self.GraphicSettingFrame)

        self.CountTableFrame = QFrame(Form)
        self.CountTableFrame.setObjectName(u"CountTableFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(3)
        sizePolicy4.setHeightForWidth(self.CountTableFrame.sizePolicy().hasHeightForWidth())
        self.CountTableFrame.setSizePolicy(sizePolicy4)
        self.CountTableFrame.setAutoFillBackground(True)
        self.CountTableFrame.setFrameShape(QFrame.StyledPanel)
        self.CountTableFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.CountTableFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scrollArea= QScrollArea(self.CountTableFrame)
        sizePolicyScrollArea= QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicyScrollArea.setHorizontalStretch(4)
        sizePolicyScrollArea.setVerticalStretch(3)
        sizePolicyScrollArea.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(sizePolicyScrollArea)
        self.scrollArea.setFrameShape(QFrame.Panel)
        self.scrollArea.setFrameShadow(QFrame.Sunken)
        self.CountsFrame = QFrame(self.scrollArea)
        self.CountsFrame.setObjectName(u"CountsFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(4)
        sizePolicy5.setVerticalStretch(3)
        sizePolicy5.setHeightForWidth(self.CountsFrame.sizePolicy().hasHeightForWidth())
        self.CountsFrame.setSizePolicy(sizePolicy5)
        self.verticalLayout_3 = QVBoxLayout(self.CountsFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.TitleCountsFrame = QFrame(self.CountsFrame)
        self.TitleCountsFrame.setObjectName(u"TitleCountsFrame")
        self.TitleCountsFrame.setFrameShape(QFrame.StyledPanel)
        self.TitleCountsFrame.setFrameShadow(QFrame.Raised)
        self.TitleCountsFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_10 = QHBoxLayout(self.TitleCountsFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.titleCounts = QLabel(self.TitleCountsFrame)
        self.titleCounts.setObjectName(u"titleCounts")

        self.horizontalLayout_10.addWidget(self.titleCounts)

        self.titleUncertainty = QLabel(self.TitleCountsFrame)
        self.titleUncertainty.setObjectName(u"titleUncertainty")

        self.horizontalLayout_10.addWidget(self.titleUncertainty)


        self.verticalLayout_3.addWidget(self.TitleCountsFrame)

        self.ChannelACountValues = QFrame(self.CountsFrame)
        self.ChannelACountValues.setObjectName(u"ChannelACountValues")
        self.ChannelACountValues.setFrameShape(QFrame.StyledPanel)
        self.ChannelACountValues.setFrameShadow(QFrame.Raised)
        self.ChannelACountValues.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_11 = QHBoxLayout(self.ChannelACountValues)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.channelAValuesCount = QLabel(self.ChannelACountValues)
        self.channelAValuesCount.setObjectName(u"channelAValuesCount")

        self.horizontalLayout_11.addWidget(self.channelAValuesCount)

        self.channelAUncertaintyCount = QLabel(self.ChannelACountValues)
        self.channelAUncertaintyCount.setObjectName(u"channelAUncertaintyCount")

        self.horizontalLayout_11.addWidget(self.channelAUncertaintyCount)


        self.verticalLayout_3.addWidget(self.ChannelACountValues)

        self.ChannelBCountValues = QFrame(self.CountsFrame)
        self.ChannelBCountValues.setObjectName(u"ChannelBCountValues")
        self.ChannelBCountValues.setFrameShape(QFrame.StyledPanel)
        self.ChannelBCountValues.setFrameShadow(QFrame.Raised)
        self.ChannelBCountValues.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_12 = QHBoxLayout(self.ChannelBCountValues)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.channelBValuesCount = QLabel(self.ChannelBCountValues)
        self.channelBValuesCount.setObjectName(u"channelBValuesCount")

        self.horizontalLayout_12.addWidget(self.channelBValuesCount)

        self.channelBUncertaintyCount = QLabel(self.ChannelBCountValues)
        self.channelBUncertaintyCount.setObjectName(u"channelBUncertaintyCount")

        self.horizontalLayout_12.addWidget(self.channelBUncertaintyCount)


        self.verticalLayout_3.addWidget(self.ChannelBCountValues)

        self.ChannelCCountValues = QFrame(self.CountsFrame)
        self.ChannelCCountValues.setObjectName(u"ChannelCCountValues")
        self.ChannelCCountValues.setFrameShape(QFrame.StyledPanel)
        self.ChannelCCountValues.setFrameShadow(QFrame.Raised)
        self.ChannelCCountValues.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_13 = QHBoxLayout(self.ChannelCCountValues)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.channelCValuesCount = QLabel(self.ChannelCCountValues)
        self.channelCValuesCount.setObjectName(u"channelCValuesCount")

        self.horizontalLayout_13.addWidget(self.channelCValuesCount)

        self.channelCUncertaintyCount = QLabel(self.ChannelCCountValues)
        self.channelCUncertaintyCount.setObjectName(u"channelCUncertaintyCount")

        self.horizontalLayout_13.addWidget(self.channelCUncertaintyCount)


        self.verticalLayout_3.addWidget(self.ChannelCCountValues)

        self.ChannelDCountValues = QFrame(self.CountsFrame)
        self.ChannelDCountValues.setObjectName(u"ChannelDCountValues")
        self.ChannelDCountValues.setFrameShape(QFrame.StyledPanel)
        self.ChannelDCountValues.setFrameShadow(QFrame.Raised)
        self.ChannelDCountValues.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_14 = QHBoxLayout(self.ChannelDCountValues)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.channelDValuesCount = QLabel(self.ChannelDCountValues)
        self.channelDValuesCount.setObjectName(u"channelDValuesCount")

        self.horizontalLayout_14.addWidget(self.channelDValuesCount)

        self.channelDUncertaintyCount = QLabel(self.ChannelDCountValues)
        self.channelDUncertaintyCount.setObjectName(u"channelDUncertaintyCount")

        self.horizontalLayout_14.addWidget(self.channelDUncertaintyCount)


        self.verticalLayout_3.addWidget(self.ChannelDCountValues)


        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.scrollArea.setWidget(self.CountsFrame)

        self.TableFrame = QFrame(self.CountTableFrame)
        self.TableFrame.setObjectName(u"TableFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(6)
        sizePolicy6.setVerticalStretch(9)
        sizePolicy6.setHeightForWidth(self.TableFrame.sizePolicy().hasHeightForWidth())
        self.TableFrame.setSizePolicy(sizePolicy6)
        self.TableFrame.setFrameShape(QFrame.Panel)
        self.TableFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_15 = QVBoxLayout(self.TableFrame)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.countValuesTable = QTableWidget(self.TableFrame)
        if (self.countValuesTable.columnCount() < 5):
            self.countValuesTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.countValuesTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.countValuesTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.countValuesTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.countValuesTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.countValuesTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.countValuesTable.setObjectName(u"countValuesTable")
        self.countValuesTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.countValuesTable.setAlternatingRowColors(False)
        self.countValuesTable.setShowGrid(True)
        self.countValuesTable.setSortingEnabled(False)
        self.countValuesTable.horizontalHeader().setVisible(True)
        self.countValuesTable.horizontalHeader().setCascadingSectionResizes(False)
        self.countValuesTable.horizontalHeader().setProperty("showSortIndicator", False)
        self.countValuesTable.horizontalHeader().setStretchLastSection(True)
        self.countValuesTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.countValuesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


       
        self.statusFrame=QFrame(self.TableFrame)
        self.statusFrame.setFrameShape(QFrame.Panel)
        self.statusFrame.setFrameShadow(QFrame.Sunken)
        self.statusLayout = QHBoxLayout(self.statusFrame)
        sizePolicyStatus = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicyStatus.setHorizontalStretch(6)
        sizePolicyStatus.setVerticalStretch(1)
        sizePolicyStatus.setHeightForWidth(self.statusFrame.sizePolicy().hasHeightForWidth())
        self.statusFrame.setSizePolicy(sizePolicyStatus)

        # Crear los labels
        self.labelStatus = QLabel("Status:", self.statusFrame)
        self.labelState = QLabel("No running", self.statusFrame)
        self.labelColor = QLabel("N", self.statusFrame)

        # Opcional: puedes ajustar estilos si quieres negrita, tamaño, etc.

        # Añadir elementos alineados a la izquierda
        self.statusLayout.addWidget(self.labelStatus)
        self.statusLayout.addWidget(self.labelState)

        # Espaciador para empujar el siguiente label hacia la derecha
        self.statusLayout.addStretch()

        # Añadir el label alineado a la derecha
        self.statusLayout.addWidget(self.labelColor)
        self.horizontalLayout_15.addWidget(self.countValuesTable)
        self.horizontalLayout_15.addWidget(self.statusFrame)


        self.horizontalLayout_2.addWidget(self.TableFrame)
        


        self.verticalLayout.addWidget(self.CountTableFrame)

                # Asegurar que los botones no se aplasten
        botones = [
            self.startMeasurementButton,
            self.stopMeasurementButton,
            self.channelAClearButton,
            self.channelBClearButton,
            self.channelCClearButton,
            self.channelDClearButton,
            self.saveDataButton,
            self.savePlotsButton,
        ]
        for boton in botones:
            boton.setMinimumHeight(21)
            boton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.retranslateUi(Form)
        self.comboBoxTimeRange.setMinimumHeight(21)
        self.ChannelACountValues.setVisible(False)
        self.ChannelBCountValues.setVisible(False)
        self.ChannelCCountValues.setVisible(False)
        self.ChannelDCountValues.setVisible(False)
        self.setFontSizeToLabels(12,
        self.titleCounts,
        self.channelAValuesCount,
        self.channelBValuesCount,
        self.channelCValuesCount,
        self.channelDValuesCount,
        self.channelAUncertaintyCount,
        self.channelBUncertaintyCount,
        self.channelCUncertaintyCount,
        self.channelDUncertaintyCount,
        self.titleUncertainty
        )
        self.verticalLayout_3.setSpacing(2)  # Espacio vertical entre filas
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)  # Márgenes del layout general
        
        # Channel A
        left, _, right, _ = self.horizontalLayout_11.getContentsMargins()
        self.horizontalLayout_11.setContentsMargins(left, 0, right, 0)

        # Channel B
        left, _, right, _ = self.horizontalLayout_12.getContentsMargins()
        self.horizontalLayout_12.setContentsMargins(left, 0, right, 0)

        # Channel C
        left, _, right, _ = self.horizontalLayout_13.getContentsMargins()
        self.horizontalLayout_13.setContentsMargins(left, 0, right, 0)

        # Channel D
        left, _, right, _ = self.horizontalLayout_14.getContentsMargins()
        self.horizontalLayout_14.setContentsMargins(left, 0, right, 0)
        
        #Title
        left, top, right, _ = self.horizontalLayout_14.getContentsMargins()
        self.horizontalLayout_10.setContentsMargins(left, top, right, 0)
        

        QMetaObject.connectSlotsByName(Form)
        self.drawColorPoint()
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.channelLabel.setText(QCoreApplication.translate("Form", u"Channels:", None))
        self.channelACheckBox.setText(QCoreApplication.translate("Form", u"A", None))
        self.channelCCheckBox.setText(QCoreApplication.translate("Form", u"B", None))
        self.channelBCheckBox.setText(QCoreApplication.translate("Form", u"C", None))
        self.channelDCheckBox.setText(QCoreApplication.translate("Form", u"D", None))
        self.startMeasurementButton.setText(QCoreApplication.translate("Form", u"Start Measurement", None))
        self.stopMeasurementButton.setText(QCoreApplication.translate("Form", u"Stop Measurement", None))
        self.grapLabel.setText(QCoreApplication.translate("Form", u"Graph:", None))
        self.mergeGraphicButton.setText(QCoreApplication.translate("Form", u"Merge graphics", None))
        self.separateGraphicButton.setText(QCoreApplication.translate("Form", u"Separate graphics", None))
        self.apartDialogGraphicButton.setText(QCoreApplication.translate("Form", u"Detached Graphics", None))
        self.timeRangeLabel.setText(QCoreApplication.translate("Form", u"Time range:", None))
        self.comboBoxTimeRange.setItemText(0, QCoreApplication.translate("Form", u"10 seconds", None))
        self.comboBoxTimeRange.setItemText(1, QCoreApplication.translate("Form", u"20 seconds", None))
        self.comboBoxTimeRange.setItemText(2, QCoreApplication.translate("Form", u"50 seconds", None))
        self.comboBoxTimeRange.setItemText(3, QCoreApplication.translate("Form", u"100 seconds", None))
        self.comboBoxTimeRange.setItemText(4, QCoreApplication.translate("Form", u"200 seconds", None))
        self.comboBoxTimeRange.setItemText(5, QCoreApplication.translate("Form", u"500 seconds", None))
        self.comboBoxTimeRange.setItemText(6, QCoreApplication.translate("Form", u"1000 seconds", None))

        self.clearLabel.setText(QCoreApplication.translate("Form", u"Clear data channels:", None))
        self.channelAClearButton.setText(QCoreApplication.translate("Form", u"A", None))
        self.channelBClearButton.setText(QCoreApplication.translate("Form", u"B", None))
        self.channelCClearButton.setText(QCoreApplication.translate("Form", u"C", None))
        self.channelDClearButton.setText(QCoreApplication.translate("Form", u"D", None))
        self.saveDataButton.setText(QCoreApplication.translate("Form", u"Save data", None))
        self.savePlotsButton.setText(QCoreApplication.translate("Form", u"Save Plots", None))
        self.titleCounts.setText(QCoreApplication.translate("Form", u" <b>Est. counts (cps)<\b>", None))
        self.titleUncertainty.setText(QCoreApplication.translate("Form", u"<b>Uncertainty<\b>", None))
        self.channelAValuesCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelAUncertaintyCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelBValuesCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelBUncertaintyCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelCValuesCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelCUncertaintyCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelDValuesCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        self.channelDUncertaintyCount.setText(QCoreApplication.translate("Form", u"Not estimated yet", None))
        font_bold = QFont()
        font_bold.setBold(True)

        ___qtablewidgetitem = QTableWidgetItem()
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Date", None))
        ___qtablewidgetitem.setFont(font_bold)
        self.countValuesTable.setHorizontalHeaderItem(0, ___qtablewidgetitem)

        ___qtablewidgetitem1 = QTableWidgetItem()
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"A", None))
        ___qtablewidgetitem1.setFont(font_bold)
        self.countValuesTable.setHorizontalHeaderItem(1, ___qtablewidgetitem1)

        ___qtablewidgetitem2 = QTableWidgetItem()
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"B", None))
        ___qtablewidgetitem2.setFont(font_bold)
        self.countValuesTable.setHorizontalHeaderItem(2, ___qtablewidgetitem2)

        ___qtablewidgetitem3 = QTableWidgetItem()
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"C", None))
        ___qtablewidgetitem3.setFont(font_bold)
        self.countValuesTable.setHorizontalHeaderItem(3, ___qtablewidgetitem3)

        ___qtablewidgetitem4 = QTableWidgetItem()
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"D", None))
        ___qtablewidgetitem4.setFont(font_bold)
        self.countValuesTable.setHorizontalHeaderItem(4, ___qtablewidgetitem4)
        self.separateGraphicButton.setChecked(True)
        self.mergeGraphicButton.setChecked(False)
    # retranslateUi
    def drawColorPoint(self):
        pixmap = QPixmap(self.labelColor.size())
        pixmap.fill(Qt.transparent)  

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing) 
        painter.setBrush(QColor(128, 128, 128))  
        painter.setPen(Qt.NoPen)

        # Definir el tamaño del punto (círculo)
        point_size = min(self.labelColor.width(), self.labelColor.height()) // 2

        # Calcular la posición del círculo para que quede centrado
        x = (self.labelColor.width() - point_size) // 2
        y = (self.labelColor.height() - point_size) // 2

        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.labelColor.setPixmap(pixmap)
    
    def setFontSizeToLabels(self,size, *labels):
        font = QFont()
        font.setPointSize(size)
        for label in labels:
            label.setFont(font)
    


        


#Listener to dinamically change the interface according the selection of the checkbox


    