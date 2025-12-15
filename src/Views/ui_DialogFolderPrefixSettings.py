# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designeruIgInx.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QStyle
from Utils.createsavefile import createsavefile
import json
import os
from pathlib import Path


class Ui_DialogFolderPrefix(object):
    def setupUi(self, Dialog, mainWindow):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        self.createSaveFile=createsavefile()
        self.dialog=Dialog
        self.mainWIndow=mainWindow
        Dialog.resize(496, 336)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.FolderPathFrame = QFrame(Dialog)
        self.FolderPathFrame.setObjectName(u"FolderPathFrame")
        self.FolderPathFrame.setFrameShape(QFrame.StyledPanel)
        self.FolderPathFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.FolderPathFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.FolderPathFrame)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.folderPathLineEdit = QLineEdit(self.FolderPathFrame)
        self.folderPathLineEdit.setObjectName(u"folderPathLineEdit")
        self.folderPathLineEdit.setPlaceholderText("Select a folder...")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(7)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.folderPathLineEdit.sizePolicy().hasHeightForWidth())
        self.folderPathLineEdit.setSizePolicy(sizePolicy1)
        folder_icon = self.folderPathLineEdit.style().standardIcon(QStyle.SP_DirOpenIcon)
        self.folderAction = self.folderPathLineEdit.addAction(folder_icon, QLineEdit.TrailingPosition)
        self.horizontalLayout.addWidget(self.folderPathLineEdit)
        self.folderAction.triggered.connect(self.selectFolder)


        self.verticalLayout.addWidget(self.FolderPathFrame)

        self.StartStopHistogramFrame = QFrame(Dialog)
        self.StartStopHistogramFrame.setObjectName(u"StartStopHistogramFrame")
        self.StartStopHistogramFrame.setFrameShape(QFrame.StyledPanel)
        self.StartStopHistogramFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.StartStopHistogramFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.startStopHistogramPrefix = QLabel(self.StartStopHistogramFrame)
        self.startStopHistogramPrefix.setObjectName(u"startStopHistogramPrefix")
        sizePolicy.setHeightForWidth(self.startStopHistogramPrefix.sizePolicy().hasHeightForWidth())
        self.startStopHistogramPrefix.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.startStopHistogramPrefix)

        self.startStopHistogramLineEdit = QLineEdit(self.StartStopHistogramFrame)
        self.startStopHistogramLineEdit.setObjectName(u"startStopHistogramLineEdit")
        sizePolicy1.setHeightForWidth(self.startStopHistogramLineEdit.sizePolicy().hasHeightForWidth())
        self.startStopHistogramLineEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.startStopHistogramLineEdit)


        self.verticalLayout.addWidget(self.StartStopHistogramFrame)

        self.LifeTimeFrame = QFrame(Dialog)
        self.LifeTimeFrame.setObjectName(u"LifeTimeFrame")
        self.LifeTimeFrame.setFrameShape(QFrame.StyledPanel)
        self.LifeTimeFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.LifeTimeFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lifetimePrefix = QLabel(self.LifeTimeFrame)
        self.lifetimePrefix.setObjectName(u"lifetimePrefix")
        sizePolicy.setHeightForWidth(self.lifetimePrefix.sizePolicy().hasHeightForWidth())
        self.lifetimePrefix.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lifetimePrefix)

        self.lifetimeLineEdit = QLineEdit(self.LifeTimeFrame)
        self.lifetimeLineEdit.setObjectName(u"lifetimeLineEdit")
        sizePolicy1.setHeightForWidth(self.lifetimeLineEdit.sizePolicy().hasHeightForWidth())
        self.lifetimeLineEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.lifetimeLineEdit)


        self.verticalLayout.addWidget(self.LifeTimeFrame)

        self.CountsEstimationFrame = QFrame(Dialog)
        self.CountsEstimationFrame.setObjectName(u"CountsEstimationFrame")
        self.CountsEstimationFrame.setFrameShape(QFrame.StyledPanel)
        self.CountsEstimationFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.CountsEstimationFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.countsEstimationPrefix = QLabel(self.CountsEstimationFrame)
        self.countsEstimationPrefix.setObjectName(u"countsEstimationPrefix")
        sizePolicy.setHeightForWidth(self.countsEstimationPrefix.sizePolicy().hasHeightForWidth())
        self.countsEstimationPrefix.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.countsEstimationPrefix)

        self.countsEstimationLineEdit = QLineEdit(self.CountsEstimationFrame)
        self.countsEstimationLineEdit.setObjectName(u"countsEstimationLineEdit")
        sizePolicy1.setHeightForWidth(self.countsEstimationLineEdit.sizePolicy().hasHeightForWidth())
        self.countsEstimationLineEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.countsEstimationLineEdit)


        self.verticalLayout.addWidget(self.CountsEstimationFrame)

        self.TimeStampingFrame = QFrame(Dialog)
        self.TimeStampingFrame.setObjectName(u"TimeStampingFrame")
        self.TimeStampingFrame.setFrameShape(QFrame.StyledPanel)
        self.TimeStampingFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.TimeStampingFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.timeStampingLineEdit = QLabel(self.TimeStampingFrame)
        self.timeStampingLineEdit.setObjectName(u"timeStampingLineEdit")
        sizePolicy.setHeightForWidth(self.timeStampingLineEdit.sizePolicy().hasHeightForWidth())
        self.timeStampingLineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.timeStampingLineEdit)

        self.lineEdit = QLineEdit(self.TimeStampingFrame)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.lineEdit)


        self.verticalLayout.addWidget(self.TimeStampingFrame)

        self.ApplyChangesFrame = QFrame(Dialog)
        self.ApplyChangesFrame.setObjectName(u"ApplyChangesFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ApplyChangesFrame.sizePolicy().hasHeightForWidth())
        self.ApplyChangesFrame.setSizePolicy(sizePolicy2)
        self.ApplyChangesFrame.setFrameShape(QFrame.StyledPanel)
        self.ApplyChangesFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.ApplyChangesFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.applyChangesButton = QPushButton(self.ApplyChangesFrame)
        self.cancelButton = QPushButton(self.ApplyChangesFrame)
        self.defaultValuesButton = QPushButton(self.ApplyChangesFrame)
        self.applyChangesButton.setObjectName(u"applyChangesButton")
        self.cancelButton.setText("Cancel")
        self.defaultValuesButton.setText("Default values")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(7)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.applyChangesButton.sizePolicy().hasHeightForWidth())
        self.applyChangesButton.setSizePolicy(sizePolicy3)
        self.cancelButton.setSizePolicy(sizePolicy3)
        self.defaultValuesButton.setSizePolicy(sizePolicy3)
        self.cancelButton.clicked.connect(self.cancelChanges)
        self.defaultValuesButton.clicked.connect(self.defaultValues)

        self.horizontalLayout_6.addWidget(self.applyChangesButton)
        
        self.horizontalLayout_6.addWidget(self.defaultValuesButton)
        self.horizontalLayout_6.addWidget(self.cancelButton)


        self.verticalLayout.addWidget(self.ApplyChangesFrame)


        self.retranslateUi(Dialog)
        self.getSettings()
        self.applyChangesButton.clicked.connect(self.applySettings)

        QMetaObject.connectSlotsByName(Dialog)
        
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"File path settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Save folder path:", None))
        self.startStopHistogramPrefix.setText(QCoreApplication.translate("Dialog", u"Start-stop histogram prefix:", None))
        self.lifetimePrefix.setText(QCoreApplication.translate("Dialog", u"Lifetime prefix:", None))
        self.countsEstimationPrefix.setText(QCoreApplication.translate("Dialog", u"Counts estimation prefix:", None))
        self.timeStampingLineEdit.setText(QCoreApplication.translate("Dialog", u"Time stamping prefix:", None))
        self.applyChangesButton.setText(QCoreApplication.translate("Dialog", u"Apply changes", None))

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder:
            self.folderPathLineEdit.setText(folder)
    
    def getSettings(self):
        #Disable folder line edit
        self.folderPathLineEdit.setReadOnly(True)
        pathConstants=self.createSaveFile.getPathFolder()
        #get settings
        with open(pathConstants, "r", encoding="utf-8") as file:
            data = json.load(file)
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        default_save_folder = os.path.join(documents_folder, "TempicoSoftwareData")
        if data["saveFolder"]=="":
            self.folderPathLineEdit.setText(default_save_folder)
            self.initialFolderPath=default_save_folder
        else:
            self.folderPathLineEdit.setText(data["saveFolder"])
            self.initialFolderPath=data["saveFolder"]
        self.startStopHistogramLineEdit.setText(data["startStopHistogramPrefix"])
        self.lifetimeLineEdit.setText(data["lifetimePrefix"])
        self.countsEstimationLineEdit.setText(data["countsEstimationPrefix"])
        self.lineEdit.setText(data["timeStampingPrefix"])
        
        
        
    def applySettings(self):
        pathConstants=self.createSaveFile.getPathFolder()
        if any(c in self.startStopHistogramLineEdit.text() for c in r'\/:*?"<>|'):
            self.dialogShowingProblems("Start-stop histogram prefix")
        elif any(c in self.lifetimeLineEdit.text() for c in r'\/:*?"<>|'):
            self.dialogShowingProblems("Lifetime prefix")
        elif any(c in self.countsEstimationLineEdit.text() for c in r'\/:*?"<>|'):
            self.dialogShowingProblems("Counts estimation prefix")
        elif any(c in self.lineEdit.text() for c in r'\/:*?"<>|'):
            self.dialogShowingProblems("Time stamping prefix")
        else:
            with open(pathConstants, "r", encoding="utf-8") as file:
                data = json.load(file)
            data["saveFolder"]=self.folderPathLineEdit.text()
            data["startStopHistogramPrefix"]=self.startStopHistogramLineEdit.text()
            data["lifetimePrefix"]=self.lifetimeLineEdit.text()
            data["countsEstimationPrefix"]=self.countsEstimationLineEdit.text()
            data["timeStampingPrefix"]=self.lineEdit.text()
            with open(pathConstants, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if self.folderPathLineEdit!=self.initialFolderPath:
                self.mainWIndow.resetSaveSentinelsAllWindows()
            self.createSaveFile.createTempFileData()
            self.dialog.close()
            
    
    
    def defaultValues(self):
        documentsDir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        targetPath = Path(documentsDir) / "TempicoSoftwareData"
        self.folderPathLineEdit.setText(str(targetPath))
        documentsDir = Path.home() / "Documents"
        targetPath = documentsDir / "TempicoSoftwareData"
        self.startStopHistogramLineEdit.setText("StartStopHistogram")
        self.countsEstimationLineEdit.setText("CountsEstimation")
        self.lifetimeLineEdit.setText("Lifetime")
        self.lineEdit.setText("TimeStamping")
    
    def cancelChanges(self):
        self.dialog.close()
    
    def dialogShowingProblems(self, prefix):
        invalid_chars = r'\/:*?"<>|'
        QMessageBox.warning(
            self.dialog,
            f"Invalid Characters in prefix",
            f"The {prefix} contains invalid characters.\n\n"
            f"Please avoid using any of the following:\n\n"
            f"{invalid_chars}\n\n"
            f"These characters are not allowed in file names."
        )
    
    def onlyReading(self):
        self.folderPathLineEdit.setEnabled(False)
        self.startStopHistogramLineEdit.setEnabled(False)
        self.lifetimeLineEdit.setEnabled(False)
        self.countsEstimationLineEdit.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.applyChangesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        self.defaultValuesButton.setEnabled(False)
        

    def enableEditing(self):
        self.folderPathLineEdit.setEnabled(True)
        self.startStopHistogramLineEdit.setEnabled(True)
        self.lifetimeLineEdit.setEnabled(True)
        self.countsEstimationLineEdit.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.applyChangesButton.setEnabled(True)
        self.cancelButton.setEnabled(True)
        self.defaultValuesButton.setEnabled(True)
