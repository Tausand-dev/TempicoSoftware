# -*- coding: utf-8 -*-
"""FCSLogic

    Orchestration layer for the FCS (Fluorescence Correlation Spectroscopy)
    measurement tab. Manages the pyqtgraph plot widget, button states, thread
    lifecycle, data saving, and status indicators.


    | @author: Miguelangel García Castillo, Tausand Electronics
    | mgarcia@tausand.com
    | https://www.tausand.com
"""

import os
import datetime

import numpy as np
import pyqtgraph as pg
from PySide2.QtCore  import QMetaObject, Qt
from PySide2.QtGui   import QPixmap, QPainter, QColor
from PySide2.QtWidgets import (
    QGridLayout, QDialog, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QMessageBox,
)

import pyTempico as Tempico
from Utils.createsavefile import createsavefile as savefile
from Threads.ThreadFCS import WorkerThreadFCS


class FCSLogic():
    """
    Orchestration layer for the FCS measurement tab.

    Creates and manages a single pyqtgraph ``PlotWidget`` that displays the
    normalized autocorrelation function G(τ) in real time. Instantiates and
    controls a ``WorkerThreadFCS`` during acquisition, and provides save
    (data + plot) functionality after the measurement finishes.

    Parameters
    ----------
    parent : QWidget
        The ``QFrame`` / ``QWidget`` inside the FCS tab where the plot is
        injected (equivalent to ``Graph3`` in ``StartStopLogic``).
    disconnectButton : QPushButton
        Main-window Disconnect button – disabled while measuring.
    device : Tempico.TempicoDevice
        Open Tempico device instance.
    startButton : QPushButton
        Starts the acquisition.
    stopButton : QPushButton
        Stops the acquisition.
    saveDataButton : QPushButton
        Saves the raw G(τ) curve to a text/csv/dat file.
    savePlotButton : QPushButton
        Saves the plot as an image file.
    clearButton : QPushButton
        Clears the accumulated curve without restarting the device.
    connectButton : QPushButton
        Main-window Connect button – re-enabled when disconnected.
    mainWindow : QMainWindow
        Reference to the application's main window (for tab management and
        ``activeMeasurement`` / ``noMeasurement`` coordination).
    statusValue : QLabel
        Label that shows the current acquisition status text.
    statusPoint : QLabel
        Small label used as a coloured status indicator (traffic-light dot).
    timerStatus : QTimer
        Shared timer that polls the device connection; stopped during
        measurement and restarted when idle.
    tau_0 : int, optional
        Base bin size in picoseconds. Default: 1 000 000 ps (1 ms).
    """

    def __init__(
        self,
        parent,
        disconnectButton,
        device: Tempico.TempicoDevice,
        startButton,
        stopButton,
        saveDataButton,
        savePlotButton,
        clearButton,
        connectButton,
        mainWindow,
        statusValue,
        statusPoint,
        timerStatus,
        tau_0 = 1_000_000_000,   # 1000 µs = 1 ms in picoseconds
    ):
        super().__init__()

        # ── Utility ──────────────────────────────────────────────────────────
        self.savefile = savefile()

        # ── Device ───────────────────────────────────────────────────────────
        self.device = device

        # ── Correlator parameters ─────────────────────────────────────────
        # tau_0 in ps; num_levels and m are fixed internally (not user-facing)
        self.tau_0      = tau_0
        self.num_levels = 16   # fixed: covers ~1 ms to ~32 s at tau_0=1ms
        self.m          = 16   # fixed: standard multi-tau value

        # ── Widget references ─────────────────────────────────────────────
        self.parent           = parent
        self.disconnectButton = disconnectButton
        self.connectButton    = connectButton
        self.mainWindow       = mainWindow
        self.statusValue      = statusValue
        self.statusPoint      = statusPoint
        self.timerConnection  = timerStatus

        self.startButton    = startButton
        self.stopButton     = stopButton
        self.saveDataButton = saveDataButton
        self.savePlotButton = savePlotButton
        self.clearButton    = clearButton

        # Stored as None until main.py sets them after constructing this object.
        # main.py calls set_parameter_widgets() right after instantiation.
        self.tau0SpinBox        = None
        self.durationSpinBox    = None
        self.indefiniteCheckBox = None

        # ── Button initial states ─────────────────────────────────────────
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)

        # ── Button connections ────────────────────────────────────────────
        self.startButton.clicked.connect(self.start_graphic)
        self.stopButton.clicked.connect(self.stop_graphic)
        self.saveDataButton.clicked.connect(self.save_data)
        self.savePlotButton.clicked.connect(self.save_plot)
        self.clearButton.clicked.connect(self.clear_curve)

        # ── Internal state ────────────────────────────────────────────────
        # Sentinel: True while the worker thread is alive
        self.threadCreatedSentinel = False
        # Set to True once the first measurement finishes (enables Save)
        self.hasMeasurementData    = False
        # Set to True when device disconnects mid-measurement
        self.withoutMeasurement    = False
        # Save-format sentinels (prevent re-saving the same data twice)
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0

        # Last emitted G(τ) arrays – kept so save works after stop
        self.last_taus_s = np.array([])
        self.last_g      = np.array([])

        # ── Build the plot ────────────────────────────────────────────────
        self._build_plot()

    # ── Plot construction ─────────────────────────────────────────────────────

    def _build_plot(self):
        """
        Create and inject the pyqtgraph plot widget into ``self.parent``.

        Sets up a logarithmic x-axis (standard FCS presentation), a dashed
        reference line at G = 1, and an empty scatter curve that will be
        updated in real time by ``update_plot``.

        :return: None
        """
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('w')
        self.plot = self.win.addPlot()

        self.plot.setTitle('Autocorrelation Function — FCS')
        self.plot.setLabel('left',   'G(τ)')
        self.plot.setLabel('bottom', 'τ (s)')
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        # Logarithmic x-axis: standard for FCS curves (ns to ms range)
        self.plot.setLogMode(x=True, y=False)
        self.plot.addLegend()

        # Dashed reference line at G = 1 (uncorrelated baseline)
        ref_line = pg.InfiniteLine(
            pos=1.0, angle=0,
            pen=pg.mkPen('gray', width=1,
                         style=pg.QtCore.Qt.DashLine)
        )
        self.plot.addItem(ref_line)

        # Scatter curve updated in real time
        self.curve = self.plot.plot(
            [], [],
            pen=None,
            symbol='o',
            symbolSize=5,
            symbolBrush='steelblue',
            symbolPen=None,
            name='G(τ) measured',
        )

        # Reuse the existing layout on graphicFrame if it already has one
        # (set by setupUi), otherwise create a new QGridLayout.
        existing_layout = self.parent.layout()
        if existing_layout is not None:
            self.gridlayout = existing_layout
        else:
            self.gridlayout = QGridLayout(self.parent)

        # Safely remove any widgets already in the layout
        while self.gridlayout.count():
            item = self.gridlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        self.gridlayout.addWidget(self.win, 0, 0)

    # ── Duration widget injection (called from main.py) ───────────────────────

    def set_parameter_widgets(self, tau0SpinBox, durationSpinBox, indefiniteCheckBox):
        """
        Provide references to the parameter widgets.

        Called by ``main.py`` immediately after constructing ``FCSLogic`` so
        that ``start_graphic`` can read the user-configured values at the
        moment the measurement starts — not at construction time.

        This is critical for ``tau0SpinBox``: if the user changes τ₀ after
        the tab is first opened, the new value must be picked up when
        "Begin measurement" is pressed.

        :param tau0SpinBox: QSpinBox with τ₀ in µs.
        :param durationSpinBox: QSpinBox with duration in seconds.
        :param indefiniteCheckBox: QCheckBox; when checked the measurement
            runs until the user presses Stop.
        :return: None
        """
        self.tau0SpinBox        = tau0SpinBox
        self.durationSpinBox    = durationSpinBox
        self.indefiniteCheckBox = indefiniteCheckBox

    # ── Start / Stop ──────────────────────────────────────────────────────────

    def start_graphic(self):
        """
        Start the FCS acquisition.

        Resets the curve, disables buttons that must not be used during
        measurement, stops the connection-polling timer, notifies the main
        window, and launches the ``WorkerThreadFCS``.

        :return: None
        """
        if self.device is None:
            return

        # Reset save sentinels so new data can be saved after this run
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0
        self.hasMeasurementData = False
        self.last_taus_s = np.array([])
        self.last_g      = np.array([])

        # Clear the curve visually
        self.curve.setData([], [])

        # Disable other tabs while measuring (mirrors StartStopLogic)
        self.mainWindow.tabs.setTabEnabled(0, False)  # Start-stop tab
        self.mainWindow.tabs.setTabEnabled(1, False)  # Lifetime tab
        self.mainWindow.tabs.setTabEnabled(2, False)  # Counts tab
        self.mainWindow.tabs.setTabEnabled(3, False)  # Time stamp tab
        self.disconnectButton.setEnabled(False)
        self.mainWindow.activeMeasurement()

        # Button states during measurement
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)

        self.statusValue.setText("Measurement running")
        self.changeStatusColor(1)

        # Stop the connection-polling timer while the thread owns the device
        self.stopTimerConnection()

        # Determine acquisition duration:
        # None = run indefinitely until Stop is pressed.
        total_seconds = None
        if (self.indefiniteCheckBox is not None
                and not self.indefiniteCheckBox.isChecked()
                and self.durationSpinBox is not None):
            total_seconds = self.durationSpinBox.value()

        # Read tau_0 from the spinbox at start time so any change the user
        # made after the tab was first opened is picked up correctly.
        # spinbox value is in µs → convert to picoseconds.
        if self.tau0SpinBox is not None:
            tau_0 = self.tau0SpinBox.value() * 1_000_000  # µs → ps
        else:
            tau_0 = self.tau_0  # fallback to constructor value

        # Instantiate and start the worker thread
        self.worker = WorkerThreadFCS(
            parent        = self.parent,
            device        = self.device,
            tau_0         = tau_0,
            num_levels    = self.num_levels,
            m             = self.m,
            total_seconds = total_seconds,
        )
        self.worker.dataReady.connect(self.update_plot)
        self.worker.statusUpdate.connect(self.changeStatusThread)
        self.worker.colorValue.connect(self.changeColorThread)
        self.worker.stringValue.connect(self.changeStatusThread)
        self.worker.threadCreated.connect(self.threadRunning)
        self.worker.finished.connect(self.threadComplete)
        self.worker.start()

    def stop_graphic(self):
        """
        Stop the acquisition and restore the UI to idle state.

        :return: None
        """
        if not self.withoutMeasurement:
            self.startTimerConnection()

        if self.threadCreatedSentinel:
            self.worker.stop()

        self.statusValue.setText("No measurement running")
        self.changeStatusColor(0)

        # Re-enable tabs
        self.mainWindow.tabs.setTabEnabled(0, True)
        self.mainWindow.tabs.setTabEnabled(1, True)
        self.mainWindow.tabs.setTabEnabled(2, True)
        self.mainWindow.tabs.setTabEnabled(3, True)
        self.disconnectButton.setEnabled(True)
        self.mainWindow.noMeasurement()

        self.stopButton.setEnabled(False)
        if not self.withoutMeasurement:
            self.startButton.setEnabled(True)

        if self.hasMeasurementData:
            self.saveDataButton.setEnabled(True)
            self.savePlotButton.setEnabled(True)
            self.clearButton.setEnabled(True)

    # ── Thread signal handlers ─────────────────────────────────────────────────

    def threadRunning(self, status):
        """
        Update ``threadCreatedSentinel`` from the ``threadCreated`` signal.

        Parameters
        ----------
        status : int
            0 → thread just started; 1 → thread just stopped.

        :return: None
        """
        if status == 0:
            self.threadCreatedSentinel = True
        elif status == 1:
            self.threadCreatedSentinel = False

    def threadComplete(self):
        """
        Called when the worker thread finishes naturally (``finished`` signal).

        :return: None
        """
        self.threadCreatedSentinel = False
        self.stop_graphic()

    def update_plot(self, taus_ps, g):
        """
        Update the G(τ) scatter plot with the latest correlation data.

        Converts lag times from picoseconds to seconds before plotting.
        Keeps a copy of the last arrays for the save functions.

        Parameters
        ----------
        taus_ps : numpy.ndarray
            Lag times in picoseconds (emitted by the thread).
        g : numpy.ndarray
            Normalized autocorrelation values G(τ).

        :return: None
        """
        taus_s = taus_ps * 1e-12
        # Pyqtgraph requires strictly positive x values in log mode
        mask = taus_s > 0
        self.curve.setData(taus_s[mask], g[mask])

        # Cache for saving
        self.last_taus_s = taus_s[mask]
        self.last_g      = g[mask]
        self.hasMeasurementData = True

    def changeStatusThread(self, new_text):
        """
        Update the status label text from a thread signal.

        :param new_text: Text to display (str).
        :return: None
        """
        self.statusValue.setText(new_text)

    def changeColorThread(self, color):
        """
        Update the status-indicator dot colour from a thread signal.

        Uses the same colour code as ``StartStopLogic``:
        0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    # ── Clear ─────────────────────────────────────────────────────────────────

    def clear_curve(self):
        """
        Clear the G(τ) curve and cached data without stopping the device.

        :return: None
        """
        self.last_taus_s = np.array([])
        self.last_g      = np.array([])
        self.hasMeasurementData = False
        self.curve.setData([], [])
        self.saveDataButton.setEnabled(False)
        self.savePlotButton.setEnabled(False)
        self.clearButton.setEnabled(False)

    # ── Save data ─────────────────────────────────────────────────────────────

    def save_data(self):
        """
        Save the last G(τ) curve to a text file chosen by the user.

        Opens a small dialog to pick the format (txt / csv / dat). The file
        contains two columns: lag time in seconds and G(τ). A header records
        the correlator parameters (tau_0, num_levels, m).

        Mirrors the save_graphic flow in ``StartStopLogic``.

        :return: None
        """
        if len(self.last_taus_s) == 0:
            return

        dataFolderPrefix = self.savefile.getDataFolderPrefix()
        folder_path      = dataFolderPrefix["saveFolder"]
        data_prefix      = dataFolderPrefix.get("fcsPrefix", "FCS_")

        current_date_str = (
            datetime.datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
            .replace(':', '').replace('-', '').replace(' ', '')
        )

        # ── Format selection dialog ───────────────────────────────────────
        dialog = QDialog(self.parent)
        dialog.setObjectName("TextFormat")
        dialog.resize(282, 105)
        dialog.setWindowTitle("Save")
        vlay = QVBoxLayout(dialog)
        lbl  = QLabel("Select the text format:")
        vlay.addWidget(lbl)
        fmt_box = QComboBox(dialog)
        fmt_box.addItem("txt")
        fmt_box.addItem("csv")
        fmt_box.addItem("dat")
        vlay.addWidget(fmt_box)
        accept_btn = QPushButton("Accept", dialog)
        vlay.addWidget(accept_btn)
        QMetaObject.connectSlotsByName(dialog)
        accept_btn.clicked.connect(dialog.accept)

        if dialog.exec_() != QDialog.Accepted:
            return

        selected_format = fmt_box.currentText()

        # Guard: avoid saving the same format twice in the same session
        condition_already_saved = (
            (selected_format == "txt" and self.sentinelsavetxt == 1) or
            (selected_format == "csv" and self.sentinelsavecsv == 1) or
            (selected_format == "dat" and self.sentinelsavedat == 1)
        )
        if condition_already_saved:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Already saved")
            msg.setText(
                f"The FCS data has already been saved in {selected_format} "
                "format during this session."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        filename = data_prefix + current_date_str + "_FCS"
        setting  = (
            f"tau_0 (ps):\t{self.tau_0}\n"
            f"num_levels:\t{self.num_levels}\n"
            f"m:\t{self.m}"
        )
        # Pack into the format expected by createsavefile
        data         = [list(self.last_taus_s), list(self.last_g)]
        filenames    = [filename]
        column_names = ["tau_s\tG(tau)"]
        settings     = [setting]

        try:
            self.savefile.save_lists_as_columns_txt(
                data, filenames, column_names,
                folder_path, settings, selected_format,
            )
            if selected_format == "txt":
                self.sentinelsavetxt = 1
            elif selected_format == "csv":
                self.sentinelsavecsv = 1
            elif selected_format == "dat":
                self.sentinelsavedat = 1

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"File saved in:\n\n{folder_path}\n\n"
                f"File: {filename}.{selected_format}"
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except Exception:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error saving")
            msg.setText("The file could not be saved.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    # ── Save plot ─────────────────────────────────────────────────────────────

    def save_plot(self):
        """
        Save the current G(τ) plot as an image file.

        Opens a format-selection dialog (png / tiff / jpg) and exports the
        pyqtgraph plot using ``pg.exporters.ImageExporter``.

        Mirrors ``save_plots`` in ``StartStopLogic``.

        :return: None
        """
        try:
            dataFolderPrefix = self.savefile.getDataFolderPrefix()
            folder_path      = dataFolderPrefix["saveFolder"]
            data_prefix      = dataFolderPrefix.get("fcsPrefix", "FCS_")

            dialog = QDialog(self.parent)
            dialog.setObjectName("ImageFormat")
            dialog.resize(282, 105)
            dialog.setWindowTitle("Save plot")
            vlay = QVBoxLayout(dialog)
            lbl  = QLabel("Select the image format:")
            vlay.addWidget(lbl)
            fmt_box = QComboBox(dialog)
            fmt_box.addItem("png")
            fmt_box.addItem("tiff")
            fmt_box.addItem("jpg")
            vlay.addWidget(fmt_box)
            accept_btn = QPushButton("Accept", dialog)
            vlay.addWidget(accept_btn)
            QMetaObject.connectSlotsByName(dialog)
            accept_btn.clicked.connect(dialog.accept)

            if dialog.exec_() != QDialog.Accepted:
                return

            selected_format  = fmt_box.currentText()
            current_date_str = (
                datetime.datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
                .replace(':', '').replace('-', '').replace(' ', '')
            )
            graph_name = data_prefix + "FCS_Plot_" + current_date_str

            exporter = pg.exporters.ImageExporter(self.plot)
            exporter.parameters()['width']  = 800
            exporter.parameters()['height'] = 600

            sep = '/' if os.name == 'posix' else '\\'
            exporter.export(
                folder_path + sep + graph_name + '.' + selected_format
            )

            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Successful save")
            msg.setText(
                f"Plot saved in:\n\n{folder_path}\n\n"
                f"File: {graph_name}.{selected_format}"
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        except Exception:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error saving")
            msg.setText(
                "The plot could not be saved. "
                "Check the folder path or system files."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    # ── Status dot helpers ────────────────────────────────────────────────────

    def changeStatusColor(self, color):
        """
        Set the status-indicator dot colour from Logic-layer code.

        Colour codes: 0 = grey, 1 = green, 2 = yellow, 3 = orange.

        :param color: Colour code (int).
        :return: None
        """
        self._draw_status_dot(color)

    def _draw_status_dot(self, color):
        """
        Draw a filled circle on ``statusPoint`` with the given colour.

        Internal helper shared by ``changeStatusColor`` and
        ``changeColorThread`` to avoid code duplication.

        :param color: Colour code (int). 0=grey, 1=green, 2=yellow, 3=orange.
        :return: None
        """
        pixmap = QPixmap(self.statusPoint.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if color == 0:
            painter.setBrush(QColor(128, 128, 128))
        elif color == 1:
            painter.setBrush(QColor(0, 255, 0))
        elif color == 2:
            painter.setBrush(QColor(255, 255, 0))
        elif color == 3:
            painter.setBrush(QColor(255, 165, 0))
        painter.setPen(Qt.NoPen)
        point_size = min(
            self.statusPoint.width(), self.statusPoint.height()
        ) // 2
        x = (self.statusPoint.width()  - point_size) // 2
        y = (self.statusPoint.height() - point_size) // 2
        painter.drawEllipse(x, y, point_size, point_size)
        painter.end()
        self.statusPoint.setPixmap(pixmap)

    # ── Timer helpers ─────────────────────────────────────────────────────────

    def stopTimerConnection(self):
        """
        Stop the shared connection-polling timer.

        Called when measurement starts so the timer does not interfere with
        the thread's exclusive use of the device.

        :return: None
        """
        self.timerConnection.stop()

    def startTimerConnection(self):
        """
        Restart the shared connection-polling timer at 500 ms.

        Called when the measurement finishes or is stopped.

        :return: None
        """
        self.timerConnection.start(500)

    # ── Device connect / disconnect (called from main.py) ─────────────────────

    def connectedDevice(self, device_new):
        """
        Update the device reference after a reconnection.

        Called by ``MainWindow.open_dialog`` when the user reconnects.

        :param device_new: New open ``TempicoDevice`` instance.
        :return: None
        """
        self.device = device_new
        self.startButton.setEnabled(True)

    def disconnectedDevice(self):
        """
        Handle a device disconnection event.

        Stops any running measurement, disables the start button, and resets
        the status indicator to grey.

        :return: None
        """
        self.withoutMeasurement = True
        if self.threadCreatedSentinel:
            self.worker.stop()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.disconnectButton.setEnabled(False)
        self.connectButton.setEnabled(True)
        self.statusValue.setText("Device disconnected")
        self.changeStatusColor(0)

    def hide_graphic2(self):
        """
        Disable start and stop buttons (called on disconnect from main.py).

        :return: None
        """
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)

    def show_graphic(self, device_new):
        """
        Re-enable the start button after a reconnection.

        :param device_new: New open ``TempicoDevice`` instance.
        :return: None
        """
        self.device = device_new
        self.startButton.setEnabled(True)

    # ── Save sentinel reset (called from main.py) ─────────────────────────────

    def resetSaveSentinels(self):
        """
        Reset the per-format save sentinels.

        Called by ``MainWindow.resetSaveSentinelsAllWindows`` so the user can
        re-save data in the same format after a new measurement.

        :return: None
        """
        self.sentinelsavetxt = 0
        self.sentinelsavecsv = 0
        self.sentinelsavedat = 0