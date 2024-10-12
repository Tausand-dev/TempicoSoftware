import pyAbacus as pa
from PySide2 import QtCore, QtGui, QtWidgets
from about import Ui_Dialog as Ui_Dialog_about

class AboutWindow(QtWidgets.QDialog, Ui_Dialog_about):
    def __init__(self, parent = None):
        super(AboutWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.parent = parent

        image = QtGui.QPixmap('Sources/splash.png')
        image = image.scaled(220, 220, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(image)

        tausand = '<a href="https://www.tausand.com/"> https://www.tausand.com </a>'
        pages =  '<a href="https://github.com/Tausand-dev/TempicoSoftware"> https://github.com/Tausand-dev/TempicoSoftware </a>'
        message = "Tempico Software is a suite of tools build to ensure your experience with Tausand's time to digital converter. \n\nSoftware Version: %s\nPyTempico Version: %s\n\n"%("1.0.0", "1.0.0")
        self.message_label.setText(message)
        self.visit_label = QtWidgets.QLabel()
        self.github_label = QtWidgets.QLabel()
        self.pages_label = QtWidgets.QLabel()

        self.visit_label.setText("Visit us at: %s "%tausand)
        self.github_label.setText("More information on Tempico Software implementation can be found at: %s"%pages)
        self.verticalLayout.addWidget(self.visit_label)
        self.verticalLayout.addWidget(self.github_label)

        self.visit_label.linkActivated.connect(self.open_link)
        self.github_label.linkActivated.connect(self.open_link)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def open_link(self, link):
        """
        Opens a specified URL in the default web browser.

        This function is triggered when a link is clicked and opens the provided URL 
        using the system's default web browser.

        :param link: The URL to be opened.
        :type link: str
        :returns: None
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))