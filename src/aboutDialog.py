# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerLRyfBj.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
#from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QDesktopServices, QPixmap
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QVBoxLayout, QFrame, QSizePolicy, QLabel, QPushButton
from PySide2.QtCore import Qt, QCoreApplication, QMetaObject


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        tausand = '<a href="https://www.tausand.com/"> https://www.tausand.com </a>'
        pages =  '<a href="https://github.com/Tausand-dev/TempicoSoftware"> https://github.com/Tausand-dev/TempicoSoftware </a>'
        AboutDialog.resize(642, 323)
        self.dialog=AboutDialog
        self.dialog.setWindowTitle("About")
        self.verticalLayout = QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descriptionFrame = QFrame(AboutDialog)
        self.descriptionFrame.setObjectName(u"descriptionFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.descriptionFrame.sizePolicy().hasHeightForWidth())
        self.descriptionFrame.setSizePolicy(sizePolicy)
        self.descriptionFrame.setFrameShape(QFrame.StyledPanel)
        self.descriptionFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.descriptionFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.descriptionLabel = QLabel(self.descriptionFrame)
        self.descriptionLabel.setObjectName(u"descriptionLabel")
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.descriptionLabel)


        self.verticalLayout.addWidget(self.descriptionFrame)

        self.specificationsFrame = QFrame(AboutDialog)
        self.specificationsFrame.setObjectName(u"specificationsFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.specificationsFrame.sizePolicy().hasHeightForWidth())
        self.specificationsFrame.setSizePolicy(sizePolicy1)
        self.specificationsFrame.setFrameShape(QFrame.StyledPanel)
        self.specificationsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.specificationsFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.softwareLabel = QLabel(self.specificationsFrame)
        self.softwareLabel.setObjectName(u"softwareLabel")

        self.verticalLayout_3.addWidget(self.softwareLabel)

        self.tempicoLabel = QLabel(self.specificationsFrame)
        self.tempicoLabel.setObjectName(u"tempicoLabel")

        self.verticalLayout_3.addWidget(self.tempicoLabel)


        self.verticalLayout.addWidget(self.specificationsFrame)

        self.pictureFrame = QFrame(AboutDialog)
        self.pictureFrame.setObjectName(u"pictureFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(5)
        sizePolicy2.setHeightForWidth(self.pictureFrame.sizePolicy().hasHeightForWidth())
        self.pictureFrame.setSizePolicy(sizePolicy2)
        self.pictureFrame.setFrameShape(QFrame.StyledPanel)
        self.pictureFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.pictureFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.imageLabel = QLabel(self.pictureFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        image = QPixmap('Sources/splash.png')
        image = image.scaled(500, 320, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(image)
        self.imageLabel.setFixedSize(300,150)

        self.verticalLayout_4.addWidget(self.imageLabel, 0, Qt.AlignCenter)
        


        self.verticalLayout.addWidget(self.pictureFrame)

        self.linkFrame = QFrame(AboutDialog)
        self.linkFrame.setObjectName(u"linkFrame")
        sizePolicy.setHeightForWidth(self.linkFrame.sizePolicy().hasHeightForWidth())
        self.linkFrame.setSizePolicy(sizePolicy)
        self.linkFrame.setFrameShape(QFrame.StyledPanel)
        self.linkFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.linkFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.linkTausand = QLabel(self.linkFrame)
        self.linkTausand.setObjectName(u"linkTausand")

        self.verticalLayout_5.addWidget(self.linkTausand)

        self.linkGitHub = QLabel(self.linkFrame)
        self.linkGitHub.setObjectName(u"linkGitHub")

        self.verticalLayout_5.addWidget(self.linkGitHub)


        self.verticalLayout.addWidget(self.linkFrame)

        self.buttonFrame = QFrame(AboutDialog)
        self.buttonFrame.setObjectName(u"buttonFrame")
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.buttonFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton = QPushButton(self.buttonFrame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_6.addWidget(self.pushButton, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.buttonFrame)

        self.pushButton.clicked.connect(self.acceptButton)
        
        

        # Cargar la imagen desde el archivo
        pixmap = QPixmap('Sources/splash.png')
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.linkTausand.setOpenExternalLinks(True)
        self.linkGitHub.setOpenExternalLinks(True)
        ##translateFuncion
        self.descriptionLabel.setText(QCoreApplication.translate("AboutDialog", u"Tempico Software is a suite of tools build to ensure your experience with Tausand's time to digital.", None))
        self.softwareLabel.setText(QCoreApplication.translate("AboutDialog", u"Software Version: 1.1.0", None))
        self.tempicoLabel.setText(QCoreApplication.translate("AboutDialog", u"PyTempico Version: 1.0.0", None))
        #self.imageLabel.setText(QCoreApplication.translate("AboutDialog", u"Picture Label", None))
        self.linkTausand.setText(QCoreApplication.translate("AboutDialog", u"Visit us at: %s "%tausand, None))
        self.linkGitHub.setText(QCoreApplication.translate("AboutDialog", u"More information on Tempico Software implementation can be found at: %s"%pages, None))
        self.pushButton.setText(QCoreApplication.translate("AboutDialog", u"Ok", None))
        self.softwareLabel.linkActivated.connect(self.open_link)
        self.tempicoLabel.linkActivated.connect(self.open_link)
        ##EndtranslateFuncion

        QMetaObject.connectSlotsByName(AboutDialog)
    
    def acceptButton(self):
        self.dialog.accept()
        
        
    
    def open_link(self, url):
        """
        Opens a specified URL in the default web browser.

        This function is triggered when a link is clicked and opens the provided URL 
        using the system's default web browser.

        :param link: The URL to be opened.
        :type link: str
        :returns: None
        """
        
        QDesktopServices.openUrl(QUrl(url))
    