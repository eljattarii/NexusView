# =============================================================================
# ui_sidebar.py
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QComboBox,
    QPushButton,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QCheckBox,
)

from backend_adb import ADBManager


# =============================================================================
# SIDEBAR WIDGET
# =============================================================================

class SidebarWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------------------------------------------------------------
        # BACKEND
        # ---------------------------------------------------------------------

        self.adb = ADBManager()

        # ---------------------------------------------------------------------
        # OBJECT NAME
        # ---------------------------------------------------------------------

        self.setObjectName("sidebarWidget")

        # ---------------------------------------------------------------------
        # MAIN LAYOUT
        # ---------------------------------------------------------------------

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setSpacing(18)

        self.main_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        # ---------------------------------------------------------------------
        # BUILD UI
        # ---------------------------------------------------------------------

        self.build_engine_section()

        self.build_connection_section()

        self.build_pairing_section()

        self.build_controls_section()

        # ---------------------------------------------------------------------
        # FINAL STRETCH
        # ---------------------------------------------------------------------

        self.main_layout.addStretch()

    # =========================================================================
    # ENGINE SECTION
    # =========================================================================

    def build_engine_section(self):

        group = QGroupBox(
            "Engine Compatibility"
        )

        layout = QVBoxLayout()

        layout.setSpacing(10)

        self.engine_selector = QComboBox()

        self.engine_selector.addItems([
            "Modern Engine (v2.0+)",
            "Legacy Engine (v1.25 & below)"
        ])

        layout.addWidget(
            self.engine_selector
        )

        group.setLayout(layout)

        self.main_layout.addWidget(group)

    # =========================================================================
    # DEVICE CONNECTION SECTION
    # =========================================================================

    def build_connection_section(self):

        group = QGroupBox(
            "Device Connection"
        )

        layout = QVBoxLayout()

        layout.setSpacing(10)

        self.combo_devices = QComboBox()

        self.combo_devices.addItem(
            "No devices connected..."
        )

        self.button_refresh = QPushButton(
            "Refresh Devices"
        )

        self.button_refresh.clicked.connect(
            self.refresh_devices
        )

        layout.addWidget(
            self.combo_devices
        )

        layout.addWidget(
            self.button_refresh
        )

        group.setLayout(layout)

        self.main_layout.addWidget(group)

    # =========================================================================
    # WIRELESS PAIRING SECTION
    # =========================================================================

    def build_pairing_section(self):

        group = QGroupBox(
            "Wireless Pairing (Android 11+)"
        )

        layout = QVBoxLayout()

        layout.setSpacing(10)

        self.input_ip = QLineEdit()

        self.input_ip.setPlaceholderText(
            "IP Address"
        )

        self.input_port = QLineEdit()

        self.input_port.setPlaceholderText(
            "Port"
        )

        self.input_code = QLineEdit()

        self.input_code.setPlaceholderText(
            "Pairing Code"
        )

        self.button_pair = QPushButton(
            "Pair Device"
        )

        self.button_pair.setObjectName(
            "pairButton"
        )

        self.button_pair.clicked.connect(
            self.pair_device
        )

        layout.addWidget(self.input_ip)

        layout.addWidget(self.input_port)

        layout.addWidget(self.input_code)

        layout.addWidget(self.button_pair)

        group.setLayout(layout)

        self.main_layout.addWidget(group)

    # =========================================================================
    # QUICK CONTROLS
    # =========================================================================

    def build_controls_section(self):

        group = QGroupBox(
            "Quick Hardware Controls"
        )

        layout = QGridLayout()

        layout.setHorizontalSpacing(10)

        layout.setVerticalSpacing(10)

        self.button_reboot = QPushButton(
            "Reboot"
        )

        self.button_power = QPushButton(
            "Power Off"
        )

        self.button_vol_up = QPushButton(
            "Vol +"
        )

        self.button_vol_down = QPushButton(
            "Vol -"
        )

        self.button_wake = QPushButton(
            "Wake/Sleep"
        )

        # ---------------------------------------------------------------------
        # SIGNALS
        # ---------------------------------------------------------------------

        self.button_reboot.clicked.connect(
            self.reboot_device
        )

        self.button_power.clicked.connect(
            self.power_off_device
        )

        self.button_vol_up.clicked.connect(
            self.volume_up
        )

        self.button_vol_down.clicked.connect(
            self.volume_down
        )

        self.button_wake.clicked.connect(
            self.wake_sleep
        )

        # ---------------------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------------------

        layout.addWidget(
            self.button_reboot,
            0,
            0
        )

        layout.addWidget(
            self.button_power,
            0,
            1
        )

        layout.addWidget(
            self.button_vol_up,
            1,
            0
        )

        layout.addWidget(
            self.button_vol_down,
            1,
            1
        )

        layout.addWidget(
            self.button_wake,
            2,
            0,
            1,
            2
        )

        # ---------------------------------------------------------------------
        # SHOW TOUCHES
        # ---------------------------------------------------------------------

        self.checkbox_show_touches = QCheckBox(
            "Show Touches"
        )

        self.checkbox_show_touches.stateChanged.connect(
            self.toggle_show_touches
        )

        layout.addWidget(
            self.checkbox_show_touches,
            3,
            0,
            1,
            2
        )

        group.setLayout(layout)

        self.main_layout.addWidget(group)

    # =========================================================================
    # HELPERS
    # =========================================================================

    def get_selected_device(self):

        device = self.combo_devices.currentText()

        if (
            not device or
            device == "No devices connected..."
        ):
            return None

        return device

    # =========================================================================
    # REFRESH DEVICES
    # =========================================================================

    def refresh_devices(self):

        try:

            devices = self.adb.get_connected_devices()

            self.combo_devices.clear()

            if not devices:

                self.combo_devices.addItem(
                    "No devices connected..."
                )

                QMessageBox.warning(
                    self,
                    "Connection",
                    "No devices found.\n"
                    "Please check USB/ADB."
                )

                return

            self.combo_devices.addItems(
                devices
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "ADB Error",
                f"Failed to refresh devices:\n{error}"
            )

    # =========================================================================
    # PAIR DEVICE
    # =========================================================================

    def pair_device(self):

        try:

            ip = self.input_ip.text().strip()

            port = self.input_port.text().strip()

            code = self.input_code.text().strip()

            if not ip or not port or not code:

                QMessageBox.warning(
                    self,
                    "Missing Information",
                    "Please enter IP, Port, and Pairing Code."
                )

                return

            success = self.adb.pair_wireless(
                ip,
                port,
                code
            )

            if success:

                QMessageBox.information(
                    self,
                    "Success",
                    "Device paired successfully."
                )

            else:

                QMessageBox.critical(
                    self,
                    "Pair Failed",
                    "Unable to pair device."
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Pairing failed:\n{error}"
            )

    # =========================================================================
    # HARDWARE CONTROLS
    # =========================================================================

    def reboot_device(self):

        try:

            device = self.get_selected_device()

            if not device:
                return

            self.adb.reboot(device)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to reboot device:\n{error}"
            )

    def power_off_device(self):

        try:

            device = self.get_selected_device()

            if not device:
                return

            self.adb.power_off(device)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to power off device:\n{error}"
            )

    def volume_up(self):

        try:

            device = self.get_selected_device()

            if not device:
                return

            self.adb.volume_up(device)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to increase volume:\n{error}"
            )

    def volume_down(self):

        try:

            device = self.get_selected_device()

            if not device:
                return

            self.adb.volume_down(device)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to decrease volume:\n{error}"
            )

    def wake_sleep(self):

        try:

            device = self.get_selected_device()

            if not device:
                return

            self.adb.wake_sleep(device)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to execute command:\n{error}"
            )

    # =========================================================================
    # SHOW TOUCHES
    # =========================================================================

    def toggle_show_touches(self):

        try:

            device = self.get_selected_device()

            if not device:

                QMessageBox.warning(
                    self,
                    "No Device",
                    "Please connect/select a device first."
                )

                self.checkbox_show_touches.setChecked(
                    False
                )

                return

            enabled = (
                self.checkbox_show_touches.isChecked()
            )

            success = self.adb.set_show_touches(
                enabled,
                device
            )

            if not success:

                QMessageBox.critical(
                    self,
                    "ADB Error",
                    "Failed to toggle Show Touches."
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Show Touches failed:\n{error}"
            )