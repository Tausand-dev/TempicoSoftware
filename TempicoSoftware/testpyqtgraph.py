import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication,QVBoxLayout, QWidget, QPushButton, QMainWindow, QCheckBox
from pyqtgraph import PlotWidget, GraphicsLayoutWidget

class Canvas:
    def __init__(self, parent, device, width, check1, check2, startbutton, stopbutton, *args, **kwargs):
        self.startbutton = startbutton
        self.stopbutton = stopbutton
        self.win = GraphicsLayoutWidget()
        self.win.setBackground('w')
        self.parent = parent
        self.data = []
        self.hist, self.bins = np.histogram(self.data, bins=100, range=(0, 10))  # Inicializar con 100 bins entre 0 y 10
        self.plot = self.win.addPlot()
        self.plot.showGrid(x=True, y=True)
        self.curve = self.plot.plot(self.bins, self.hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))
        self.plot.setTitle('Start-Stop Histogram')
        self.plot.setLabel('left', 'Frequency')
        self.plot.setLabel('bottom', 'Values (ms)')
        self.plot.setMouseEnabled(x=True, y=False)
        self.verticalLayout = QVBoxLayout(self.parent)
        self.verticalLayout.addWidget(self.win)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)
        self.startbutton.clicked.connect(self.start_graphic)
        self.stopbutton.clicked.connect(self.stop_graphic)
        self.checkA = check1
        self.checkB = check2
        self.sentinel = False
        self.plot.setMouseEnabled(x=True, y=False)
        self.channelA_enable = False
        self.channelA_disabled = True
        self.device = device
        
        # Configurar detección de eventos de zoom
        self.viewbox = self.plot.getViewBox()
        self.viewbox.sigRangeChanged.connect(self.zoom_changed)

    def start_graphic(self):
        self.sentinel = True

    def stop_graphic(self):
        self.sentinel = False
        self.data = []

    def graphics_channels(self):
        if not self.checkA.isChecked() and not self.channelA_disabled:
            self.plot.removeItem(self.curve)
            self.channelA_enable = False
            self.channelA_disabled = True
        elif self.checkA.isChecked() and not self.channelA_enable:
            self.plot.addItem(self.curve)
            self.channelA_enable = True
            self.channelA_disabled = False

    def update_plot(self):
        self.graphics_channels()
        new_data = self.get_new_data()
        self.data.append(new_data)
                
        self.hist, self.bins = np.histogram(self.data, bins=100, range=(0, 10))
        self.curve.setData(self.bins, self.hist)

    def get_new_data(self):
        random_float = np.random.uniform(1, 10)
        return random_float

    def zoom_changed(self):
        # Función llamada cuando cambia el rango de zoom en la gráfica
        x_range = self.viewbox.viewRange()[0]  # Obtener el rango visible en el eje x
        x_min, x_max = x_range[0], x_range[1]
        bin_width = (x_max - x_min) / 100.0  # Ancho de cada bin para tener 100 bins en el rango visible
        self.bins = np.linspace(x_min, x_max, num=101)  # Crear 101 puntos para definir los bordes de los bins
        self.hist, _ = np.histogram(self.data, bins=self.bins)
        self.curve.setData(self.bins, self.hist)

    def hide_graphic(self):
        self.win.close()
        self.verticalLayout.deleteLater()

# Ejemplo de uso de Canvas
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    start_button = QPushButton('Start')
    stop_button = QPushButton('Stop')
    check_box = QCheckBox('Enable Channel A')
    canvas = Canvas(central_widget, None, 800, check_box, None, start_button, stop_button)

    vertical_layout = QVBoxLayout(central_widget)
    vertical_layout.addWidget(start_button)
    vertical_layout.addWidget(stop_button)
    vertical_layout.addWidget(check_box)

    window.show()
    sys.exit(app.exec_())
