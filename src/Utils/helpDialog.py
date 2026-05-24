from PySide2.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QScrollArea, QWidget, QPushButton
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFont


HELP_CONTENT = {
    "1. Start-Stop Histogram": {
        "title": "1. Start-Stop Histogram",
        "body": (
            "Measures the time difference between a start pulse and one or more stop pulses. "
            "The result is a histogram where the x-axis is the time delay (ns) and the y-axis is the number of counts at each delay.\n\n"
            "You can select any combination of stop channels (A, B, C, D). "
            "Each selected channel produces its own histogram plotted in the graph area.\n\n"
            "Available fits: single exponential, double exponential."
        )
    },
    "2. Lifetime Fitting": {
        "title": "2. Lifetime Fitting",
        "body": (
            "Fits a decay model to a start-stop histogram to extract the fluorescence lifetime τ. "
            "The graph shows the histogram and the fitted curve overlaid.\n\n"
            "Select the stop channel to analyze and the fit model. "
            "The fitted parameters τ and I₀ are displayed once the fit converges.\n\n"
            "Available fits: single exponential I(t) = I₀·e^(−t/τ), "
            "double exponential I(t) = I₁·e^(−t/τ₁) + I₂·e^(−t/τ₂)."
        )
    },
    "3. Counts Estimation": {
        "title": "3. Counts Estimation",
        "body": (
            "Displays the photon count rate on each channel as a function of time. "
            "The graph shows count rate (kHz or MHz) on the y-axis and elapsed time on the x-axis, "
            "with one trace per channel (A, B, C, D) plotted simultaneously.\n\n"
            "Useful for monitoring signal stability and optimizing optical alignment before a full measurement."
        )
    },
    "4. Time Stamping": {
        "title": "4. Time Stamping",
        "body": (
            "Records the absolute arrival time (in picoseconds) of every photon detected on all channels simultaneously. "
            "No histogram or correlation is computed — the raw timestamps are saved directly to disk.\n\n"
            "The output file contains one column per active channel. "
            "Select the output format (txt, csv, or dat) before starting. "
            "File naming follows the convention Prefix_Date_MultiChannel.ext."
        )
    },
    "5. Autocorrelation (FCS)": {
        "title": "5. Autocorrelation (FCS)",
        "body": (
            "Computes the autocorrelation function G(τ) of the photon arrival times recorded on a selected stop channel. "
            "The graph shows G(τ) on the y-axis and lag time τ on the x-axis. "
            "G(τ) quantifies how correlated the fluorescence signal is with itself at a given time lag.\n\n"
            "Set the base bin width τ₀ (time resolution), the stop channel, and the acquisition duration, "
            "then press Start. Once the measurement finishes, press Fit to fit the G(τ) curve.\n\n"
            "Available fits: 3D Gaussian diffusion G(τ) = (1/N)·(1 + τ/τD)⁻¹·(1 + τ/(κ²τD))⁻¹ᐟ², "
            "and Anomalous diffusion G(τ) = (1/N)·[(1 + (τ/τD)^α)·(1 + (τ/(κ²τD))^α)^0.5]⁻¹. "
            "An optional G(∞) offset can be included in both models."
        )
    },
}


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tempico Software - User Manual (Help)")
        self.setMinimumSize(400, 450)
        self.setWindowIcon(QIcon('Sources/tausand_small.ico'))

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
        from PySide2.QtGui import QDesktopServices
        from PySide2.QtCore import QUrl
        import os
        pdf_path = os.path.abspath("Sources/UserManual.pdf")
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))