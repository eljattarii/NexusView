# =============================================================================
# backend_adb.py
# =============================================================================
#
# Enterprise ADB Backend
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

import subprocess
import platform


# =============================================================================
# ADB MANAGER
# =============================================================================

class ADBManager:
    """
    Enterprise ADB backend manager.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(self):

        self.adb_binary = "adb"

    # =========================================================================
    # INTERNAL COMMAND RUNNER
    # =========================================================================

    def _run_command(self, cmd_list):

        try:

            creation_flags = 0

            if platform.system() == "Windows":

                creation_flags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                creationflags=creation_flags
            )

            stdout = result.stdout.strip()

            stderr = result.stderr.strip()

            success = result.returncode == 0

            return success, stdout, stderr

        except FileNotFoundError:

            return (
                False,
                "",
                "ADB executable not found."
            )

        except Exception as error:

            return (
                False,
                "",
                str(error)
            )

    # =========================================================================
    # GET CONNECTED DEVICES
    # =========================================================================

    def get_connected_devices(self):

        success, stdout, stderr = self._run_command(
            [self.adb_binary, "devices"]
        )

        if not success:

            print(f"[ADB ERROR] {stderr}")

            return []

        devices = []

        lines = stdout.splitlines()

        for line in lines[1:]:

            line = line.strip()

            if not line:
                continue

            if "\tdevice" in line:

                device_id = line.split("\t")[0]

                devices.append(device_id)

        return devices

    # =========================================================================
    # PAIR WIRELESS
    # =========================================================================

    def pair_wireless(self, ip, port, code):

        target = f"{ip}:{port}"

        success, stdout, stderr = self._run_command(
            [
                self.adb_binary,
                "pair",
                target,
                code
            ]
        )

        if success:

            print(f"[ADB] Pair successful -> {stdout}")

            return True

        print(f"[ADB ERROR] Pair failed -> {stderr}")

        return False

    # =========================================================================
    # CONNECT WIRELESS
    # =========================================================================

    def connect_wireless(self, ip, port):

        target = f"{ip}:{port}"

        success, stdout, stderr = self._run_command(
            [
                self.adb_binary,
                "connect",
                target
            ]
        )

        if success:

            print(f"[ADB] Connected -> {stdout}")

            return True

        print(f"[ADB ERROR] Connection failed -> {stderr}")

        return False

    # =========================================================================
    # REBOOT
    # =========================================================================

    def reboot(self, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        command.append("reboot")

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Device reboot initiated")

            return True

        print(f"[ADB ERROR] Reboot failed -> {stderr}")

        return False

    # =========================================================================
    # POWER OFF
    # =========================================================================

    def power_off(self, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        command.extend([
            "shell",
            "reboot",
            "-p"
        ])

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Power off command sent")

            return True

        print(f"[ADB ERROR] Power off failed -> {stderr}")

        return False

    # =========================================================================
    # VOLUME UP
    # =========================================================================

    def volume_up(self, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        command.extend([
            "shell",
            "input",
            "keyevent",
            "24"
        ])

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Volume up command sent")

            return True

        print(f"[ADB ERROR] Volume up failed -> {stderr}")

        return False

    # =========================================================================
    # VOLUME DOWN
    # =========================================================================

    def volume_down(self, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        command.extend([
            "shell",
            "input",
            "keyevent",
            "25"
        ])

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Volume down command sent")

            return True

        print(f"[ADB ERROR] Volume down failed -> {stderr}")

        return False

    # =========================================================================
    # WAKE / SLEEP
    # =========================================================================

    def wake_sleep(self, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        command.extend([
            "shell",
            "input",
            "keyevent",
            "26"
        ])

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Wake/Sleep command sent")

            return True

        print(f"[ADB ERROR] Wake/Sleep failed -> {stderr}")

        return False

    # =========================================================================
    # SHOW TOUCHES
    # =========================================================================

    def set_show_touches(self, enabled, device_id=None):

        command = [self.adb_binary]

        if device_id:

            command.extend(["-s", device_id])

        state = "1" if enabled else "0"

        command.extend([
            "shell",
            "settings",
            "put",
            "system",
            "show_touches",
            state
        ])

        success, stdout, stderr = self._run_command(command)

        if success:

            print(
                f"[ADB] Show Touches {'Enabled' if enabled else 'Disabled'}"
            )

            return True

        print(f"[ADB ERROR] Show Touches failed -> {stderr}")

        return False

    # =========================================================================
    # LIST PHONE FILES
    # =========================================================================

    def list_phone_files(
        self,
        device_id,
        path="/sdcard"
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "shell",
            "ls",
            "-la",
            path
        ]

        success, stdout, stderr = self._run_command(command)

        if not success:

            print(f"[ADB ERROR] List files failed -> {stderr}")

            return []

        files = []

        lines = stdout.splitlines()

        for line in lines:

            parts = line.split()

            if len(parts) < 8:
                continue

            name = " ".join(parts[7:])

            if name in [".", ".."]:
                continue

            is_dir = line.startswith("d")

            files.append({
                "name": name,
                "is_dir": is_dir,
                "path": f"{path}/{name}"
            })

        return files

    # =========================================================================
    # PUSH FILE TO PHONE
    # =========================================================================

    def push_file(
        self,
        device_id,
        local_path,
        remote_path="/sdcard/"
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "push",
            local_path,
            remote_path
        ]

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] File uploaded successfully")

            return True

        print(f"[ADB ERROR] Upload failed -> {stderr}")

        return False

    # =========================================================================
    # PULL FILE FROM PHONE
    # =========================================================================

    def pull_file(
        self,
        device_id,
        remote_path,
        local_path
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "pull",
            remote_path,
            local_path
        ]

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] File downloaded successfully")

            return True

        print(f"[ADB ERROR] Download failed -> {stderr}")

        return False

    # =========================================================================
    # DELETE PHONE FILE
    # =========================================================================

    def delete_phone_file(
        self,
        device_id,
        remote_path
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "shell",
            "rm",
            "-rf",
            remote_path
        ]

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] File deleted successfully")

            return True

        print(f"[ADB ERROR] Delete failed -> {stderr}")

        return False

    # =========================================================================
    # RENAME PHONE FILE
    # =========================================================================

    def rename_phone_file(
        self,
        device_id,
        old_path,
        new_path
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "shell",
            "mv",
            old_path,
            new_path
        ]

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] File renamed successfully")

            return True

        print(f"[ADB ERROR] Rename failed -> {stderr}")

        return False

    # =========================================================================
    # CREATE PHONE FOLDER
    # =========================================================================

    def create_phone_folder(
        self,
        device_id,
        folder_path
    ):

        command = [
            self.adb_binary,
            "-s",
            device_id,
            "shell",
            "mkdir",
            "-p",
            folder_path
        ]

        success, stdout, stderr = self._run_command(command)

        if success:

            print("[ADB] Folder created successfully")

            return True

        print(f"[ADB ERROR] Create folder failed -> {stderr}")

        return False