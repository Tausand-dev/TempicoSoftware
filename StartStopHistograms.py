from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import datetime as dt
import numpy as np
import pyTempico as tempico
import pyAbacus as abacus
from settings import SettingsWindow
from generalsettings import GeneralSettingsWindow
from aboutWindow import AboutWindow
from ui_StarStopHistogram import Ui_HistogramaStartStop
class StartStopHistogramsWindow(QTabWidget):

    def init(self, parent: QWidget):
        super().init(parent)

        self.ui = Ui_HistogramaStartStop()
        self.ui.setupUi(self)

        # Ajustar la política de tamaño del área de configuración
        self.ui.GraphConfigurationArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Agregar el área de configuración al layout central del widget principal
        central_widget = QWidget(parent)
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self.ui.GraphConfigurationArea)
        layout.addWidget(self.ui.GraphicArea)
        self.setCentralWidget(central_widget)
        self.addTab()