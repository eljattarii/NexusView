# =============================================================================
# ui_workspace.py
# =============================================================================

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QGroupBox,
)

from backend_scrcpy import ScrcpyManager

from utils_config import (
    save_config,
    load_config,
)

from ui_file_browser import FileBrowserWidget


# =============================================================================
# WORKSPACE WIDGET
# =============================================================================

class WorkspaceWidget(QWidget):

    def __init__(self, sidebar_widget, parent=None):

        super().__init__(parent)

        self.sidebar = sidebar_widget

        self.scrcpy_manager = ScrcpyManager()

        self.setObjectName("workspaceWidget")

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.setSpacing(0)

        self.build_tab_widget()

        self.apply_saved_configuration()

    # =========================================================================
    # TAB WIDGET
    # =========================================================================

    def build_tab_widget(self):

        self.tabs = QTabWidget()

        self.tabs.setObjectName("mainTabWidget")

        # ---------------------------------------------------------------------
        # TABS
        # ---------------------------------------------------------------------

        self.streaming_tab = QWidget()

        self.recording_tab = QWidget()

        self.advanced_tab = QWidget()

        self.file_browser_tab = QWidget()

        # ---------------------------------------------------------------------
        # INIT TABS
        # ---------------------------------------------------------------------

        self.init_streaming_tab()

        self.init_recording_tab()

        self.init_advanced_tab()

        self.init_file_browser_tab()

        # ---------------------------------------------------------------------
        # ADD TABS
        # ---------------------------------------------------------------------

        self.tabs.addTab(
            self.streaming_tab,
            "Streaming"
        )

        self.tabs.addTab(
            self.recording_tab,
            "Recording"
        )

        self.tabs.addTab(
            self.advanced_tab,
            "Advanced Settings"
        )

        self.tabs.addTab(
            self.file_browser_tab,
            "File Browser"
        )

        self.main_layout.addWidget(self.tabs)

    # =========================================================================
    # STREAMING TAB
    # =========================================================================

    def init_streaming_tab(self):

        layout = QVBoxLayout(self.streaming_tab)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(16)

        # ---------------------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------------------

        button_layout = QHBoxLayout()

        self.button_start_stream = QPushButton(
            "▶ Start Stream"
        )

        self.button_start_stream.setObjectName(
            "startStreamButton"
        )

        self.button_start_stream.clicked.connect(
            self.handle_start_stream
        )

        self.button_stop_stream = QPushButton(
            "⏹ Stop Stream"
        )

        self.button_stop_stream.setObjectName(
            "stopStreamButton"
        )

        self.button_stop_stream.clicked.connect(
            self.handle_stop_stream
        )

        button_layout.addWidget(
            self.button_start_stream
        )

        button_layout.addWidget(
            self.button_stop_stream
        )

        # ---------------------------------------------------------------------
        # PLACEHOLDER
        # ---------------------------------------------------------------------

        self.streaming_placeholder = QLabel(
            "Streaming controls and video feed will go here"
        )

        self.streaming_placeholder.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.streaming_placeholder.setObjectName(
            "streamingPlaceholder"
        )

        # ---------------------------------------------------------------------
        # ADD
        # ---------------------------------------------------------------------

        layout.addLayout(button_layout)

        layout.addWidget(self.streaming_placeholder)

    # =========================================================================
    # RECORDING TAB
    # =========================================================================

    def init_recording_tab(self):

        layout = QVBoxLayout(self.recording_tab)

        layout.setContentsMargins(40, 40, 40, 40)

        layout.setSpacing(20)

        layout.addStretch()

        title_label = QLabel("Screen Recording")

        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #cdd6f4;
        """)

        self.recording_filename_input = QLineEdit()

        self.recording_filename_input.setPlaceholderText(
            "Enter filename (e.g., recording.mp4)"
        )

        self.recording_filename_input.setMinimumHeight(40)

        self.button_start_recording = QPushButton(
            "🔴 Start Recording"
        )

        self.button_start_recording.clicked.connect(
            self.handle_start_recording
        )

        self.button_stop_recording = QPushButton(
            "⏹ Stop Recording"
        )

        self.button_stop_recording.clicked.connect(
            self.handle_stop_recording
        )

        layout.addWidget(title_label)

        layout.addWidget(self.recording_filename_input)

        layout.addWidget(self.button_start_recording)

        layout.addWidget(self.button_stop_recording)

        layout.addStretch()

    # =========================================================================
    # ADVANCED TAB
    # =========================================================================

    def init_advanced_tab(self):

        layout = QVBoxLayout(self.advanced_tab)

        layout.setContentsMargins(30, 30, 30, 30)

        settings_group = QGroupBox(
            "Advanced Stream Configuration"
        )

        form_layout = QFormLayout()

        self.combo_bitrate = QComboBox()

        self.combo_bitrate.addItems([
            "Default",
            "2 Mbps",
            "4 Mbps",
            "8 Mbps",
            "16 Mbps",
            "32 Mbps"
        ])

        self.combo_resolution = QComboBox()

        self.combo_resolution.addItems([
            "Default",
            "1920 (1080p)",
            "1280 (720p)",
            "1024",
            "800"
        ])

        self.combo_fps = QComboBox()

        self.combo_fps.addItems([
            "Default",
            "60 FPS",
            "45 FPS",
            "30 FPS",
            "20 FPS"
        ])

        self.combo_bitrate.currentIndexChanged.connect(
            self.save_current_configuration
        )

        self.combo_resolution.currentIndexChanged.connect(
            self.save_current_configuration
        )

        self.combo_fps.currentIndexChanged.connect(
            self.save_current_configuration
        )

        form_layout.addRow(
            "Video Bitrate:",
            self.combo_bitrate
        )

        form_layout.addRow(
            "Max Resolution:",
            self.combo_resolution
        )

        form_layout.addRow(
            "Max FPS:",
            self.combo_fps
        )

        settings_group.setLayout(form_layout)

        info_label = QLabel(
            "Settings are automatically saved."
        )

        info_label.setStyleSheet("""
            color: #7f849c;
            font-size: 12px;
        """)

        layout.addWidget(settings_group)

        layout.addWidget(info_label)

        layout.addStretch()

    # =========================================================================
    # FILE BROWSER TAB
    # =========================================================================

    def init_file_browser_tab(self):

        layout = QVBoxLayout(self.file_browser_tab)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        self.file_browser_widget = FileBrowserWidget()

        layout.addWidget(self.file_browser_widget)

    # =========================================================================
    # CONFIG METHODS
    # =========================================================================

    def save_current_configuration(self):

        config = {
            "bitrate": self.combo_bitrate.currentText(),
            "resolution": self.combo_resolution.currentText(),
            "fps": self.combo_fps.currentText(),
        }

        save_config(config)

    def apply_saved_configuration(self):

        config = load_config()

        bitrate = config.get("bitrate", "Default")

        index = self.combo_bitrate.findText(bitrate)

        if index >= 0:
            self.combo_bitrate.setCurrentIndex(index)

        resolution = config.get(
            "resolution",
            "Default"
        )

        index = self.combo_resolution.findText(
            resolution
        )

        if index >= 0:
            self.combo_resolution.setCurrentIndex(index)

        fps = config.get("fps", "Default")

        index = self.combo_fps.findText(fps)

        if index >= 0:
            self.combo_fps.setCurrentIndex(index)

    # =========================================================================
    # ADVANCED PARAMETERS
    # =========================================================================

    def get_advanced_parameters(self):

        bitrate_text = self.combo_bitrate.currentText()

        bitrate = None

        if bitrate_text != "Default":

            value = bitrate_text.split()[0]

            bitrate = f"{value}M"

        resolution_text = (
            self.combo_resolution.currentText()
        )

        max_size = None

        if resolution_text != "Default":

            max_size = resolution_text.split()[0]

        fps_text = self.combo_fps.currentText()

        max_fps = None

        if fps_text != "Default":

            max_fps = fps_text.split()[0]

        return {
            "bitrate": bitrate,
            "max_size": max_size,
            "max_fps": max_fps,
        }

    # =========================================================================
    # STREAM HANDLERS
    # =========================================================================

    def handle_start_stream(self):

        device_id = self.sidebar.get_selected_device()

        engine_version = (
            self.sidebar.engine_selector.currentText()
        )

        if not device_id:

            QMessageBox.warning(
                self,
                "No Device",
                "Please connect/select a device first."
            )

            return

        self.start_mirroring(
            device_id,
            engine_version
        )

    def handle_stop_stream(self):

        device_id = self.sidebar.get_selected_device()

        if not device_id:
            return

        self.stop_mirroring(device_id)

    # =========================================================================
    # RECORDING
    # =========================================================================

    def handle_start_recording(self):

        device_id = self.sidebar.get_selected_device()

        engine_version = (
            self.sidebar.engine_selector.currentText()
        )

        if not device_id:

            QMessageBox.warning(
                self,
                "No Device",
                "Please connect/select a device first."
            )

            return

        filename = (
            self.recording_filename_input.text().strip()
        )

        if not filename:
            filename = "screen_record.mp4"

        advanced = self.get_advanced_parameters()

        success = self.scrcpy_manager.start_stream(
            device_id=device_id,
            engine_version=engine_version,
            bitrate=advanced["bitrate"],
            max_fps=advanced["max_fps"],
            max_size=advanced["max_size"],
            record_path=filename
        )

        if success:

            QMessageBox.information(
                self,
                "Recording Started",
                f"Recording saved to:\n{filename}"
            )

    def handle_stop_recording(self):

        device_id = self.sidebar.get_selected_device()

        if not device_id:
            return

        self.scrcpy_manager.stop_stream(device_id)

    # =========================================================================
    # SCRCPY
    # =========================================================================

    def start_mirroring(
        self,
        device_id,
        engine_version
    ):

        advanced = self.get_advanced_parameters()

        success = self.scrcpy_manager.start_stream(
            device_id=device_id,
            engine_version=engine_version,
            bitrate=advanced["bitrate"],
            max_fps=advanced["max_fps"],
            max_size=advanced["max_size"]
        )

        if success:

            QMessageBox.information(
                self,
                "Stream Started",
                f"Streaming started for:\n{device_id}"
            )

    def stop_mirroring(self, device_id):

        self.scrcpy_manager.stop_stream(device_id)