import os
from PySide2.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QScrollArea, QWidget, QPushButton
)
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QIcon, QFont, QDesktopServices

HELP_CONTENT = {
    "1. Start-Stop Histogram": {
        "title": "1. Start-Stop Histogram",
        "body": (
            "Measures the time difference between a start pulse and stop pulses, "
            "producing a histogram of counts vs time delay (ns) per channel.\n\n"
            "Select the stop channels (A, B, C, D) and press Start. "
            "Press Stop to end the acquisition. Each channel produces its own histogram.\n\n"
        )
    },
    "2. Counts Estimation": {
        "title": "2. Counts Estimation",
        "body": (
            "Measures the photon count rate on each channel as a function of time. "
            "The graph shows count rate (kHz or MHz) vs elapsed time, one trace per channel.\n\n"
            "Press Start to begin. Useful for checking signal levels "
            "and optimizing alignment before a full measurement."
        )
    },
    "3. Time Stamping": {
        "title": "3. Time Stamping",
        "body": (
            "Records the absolute arrival time (ps) of every photon detected "
            "on all channels simultaneously, with no histogram or correlation computed.\n\n"
            "Select the output format (txt, csv, or dat) and press Start. "
            "The raw timestamps are saved directly to the configured folder.\n\n"
            "File naming: Prefix_Date_MultiChannel.ext."
        )
    },
    "4. Lifetime": {
        "title": "4. Lifetime",
        "body": (
            "Extracts the fluorescence lifetime τ by fitting a decay model "
            "to a start-stop histogram. The graph shows the histogram and the fitted curve overlaid.\n\n"
            "Select the stop channel and the fit model, then press Fit. "
            "The fitted parameters are displayed once the fit converges.\n\n"
            "Available fits: Exponential, Double exponential, Kohlrausch, Shifted exponential."
        )
    },
    "5. Autocorrelation (FCS)": {
        "title": "5. Autocorrelation (FCS)",
        "body": (
            "Computes the autocorrelation function G(τ) vs lag time τ from photon arrival times "
            "on a selected stop channel, using the multiple-tau algorithm.\n\n"
            "Set τ₀, stop channel, and duration, then press Start. Press Fit to fit the curve.\n\n"
            "Available fits: 3D Gaussian diffusion, Anomalous diffusion, "
            "Triplet state correction, Diffusion with flow, Two-component diffusion, "
            "and Chemical relaxation."
        )
    },
    "6. g2 (HBT)": {
    "title": "6. g2 (HBT)",
    "body": (
        "Computes the second-order correlation function g²(τ) from the time differences "
        "between photon detection events on a start and a stop channel.\n\n"
        "Select the stop channel (A–D), set the bin width, window ±, and duration, "
        "then press Start. The normalized coincidence histogram updates in real time. "
        "Press Stop to end the acquisition, or check 'Continuous measurement' to run until manually stopped.\n\n"
        "Press Fit to fit the curve with one of the available models: "
        "Antibunched Gaussian, Antibunched Lorentzian, "
        "Bunched Gaussian, Bunched Lorentzian, and Three-level system."
        )
    }
}


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tempico Software - User Manual (Help)")
        self.setMinimumSize(400, 450)
        self.setWindowIcon(QIcon('Sources/tausand_small.ico'))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        main_layout = QHBoxLayout(self)

        # ── Left panel: list ──────────────────────────────────────────
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(200)
        for key in HELP_CONTENT:
            item = QListWidgetItem(key)
            self.list_widget.addItem(item)
        main_layout.addWidget(self.list_widget)

        # ── Right panel: content ──────────────────────────────────────
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)

        self.title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        right_layout.addWidget(self.title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        right_layout.addWidget(separator)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.body_label = QLabel()
        self.body_label.setWordWrap(True)
        self.body_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.body_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        scroll_layout.addWidget(self.body_label)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        right_layout.addWidget(scroll)


        main_layout.addWidget(right_frame)

        # ── Connections ───────────────────────────────────────────────
        self.list_widget.currentItemChanged.connect(self._on_item_changed)
        

        # Select first item by default
        self.list_widget.setCurrentRow(0)

    def _on_item_changed(self, current, previous):
        if current is None:
            return
        data = HELP_CONTENT.get(current.text(), {})
        self.title_label.setText(data.get("title", ""))
        self.body_label.setText(data.get("body", ""))

    def _open_pdf(self):
        pdf_path = os.path.abspath("Sources/UserManual.pdf")
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))