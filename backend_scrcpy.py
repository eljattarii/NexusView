# =============================================================================
# backend_scrcpy.py
# =============================================================================
#
# Enterprise Scrcpy Backend Manager
# -----------------------------------------------------------------------------
# Features:
#   - Streaming management
#   - Recording support
#   - Modern + Legacy engine support
#   - Multi-device process tracking
#   - Safe process termination
#   - Cross-platform compatibility
#   - Duplicate stream prevention
#   - Advanced parameter support
#
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

import subprocess
import platform


# =============================================================================
# SCRCPY MANAGER
# =============================================================================

class ScrcpyManager:
    """
    Enterprise Scrcpy process manager.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(self):
        """
        Initialize active process tracker.
        """

        self.active_streams = {}

    # =========================================================================
    # INTERNAL PROCESS CREATOR
    # =========================================================================

    def _create_process(self, command):
        """
        Create subprocess safely.

        Parameters:
            command (list):
                Scrcpy command list.

        Returns:
            subprocess.Popen
        """

        creation_flags = 0

        if platform.system() == "Windows":

            creation_flags = subprocess.CREATE_NO_WINDOW

        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creation_flags
        )

    # =========================================================================
    # BUILD SCRCPY COMMAND
    # =========================================================================

    def build_command(
        self,
        device_id,
        engine_version,
        bitrate=None,
        max_fps=None,
        max_size=None,
        record_path=None
    ):
        """
        Build scrcpy command dynamically.
        """

        cmd = [
            "scrcpy",
            "-s",
            str(device_id)
        ]

        # ---------------------------------------------------------------------
        # ENGINE TYPE
        # ---------------------------------------------------------------------

        is_modern = (
            "Modern" in engine_version
        )

        # ---------------------------------------------------------------------
        # BITRATE
        # ---------------------------------------------------------------------

        if bitrate:

            if is_modern:

                cmd.extend([
                    "--video-bit-rate",
                    str(bitrate)
                ])

            else:

                cmd.extend([
                    "-b",
                    str(bitrate)
                ])

        # ---------------------------------------------------------------------
        # FPS
        # ---------------------------------------------------------------------

        if max_fps:

            cmd.extend([
                "--max-fps",
                str(max_fps)
            ])

        # ---------------------------------------------------------------------
        # MAX SIZE
        # ---------------------------------------------------------------------

        if max_size:

            cmd.extend([
                "--max-size",
                str(max_size)
            ])

        # ---------------------------------------------------------------------
        # RECORDING
        # ---------------------------------------------------------------------

        if record_path:

            cmd.extend([
                "--record",
                str(record_path)
            ])

        return cmd

    # =========================================================================
    # START STREAM
    # =========================================================================

    def start_stream(
        self,
        device_id,
        engine_version,
        bitrate=None,
        max_fps=None,
        max_size=None,
        record_path=None
    ):
        """
        Start scrcpy stream or recording.
        """

        try:

            # -----------------------------------------------------------------
            # PREVENT DUPLICATE STREAMS
            # -----------------------------------------------------------------

            if device_id in self.active_streams:

                old_process = self.active_streams[device_id]

                if old_process.poll() is None:

                    old_process.terminate()

                    old_process.wait(timeout=3)

            # -----------------------------------------------------------------
            # BUILD COMMAND
            # -----------------------------------------------------------------

            cmd = self.build_command(
                device_id=device_id,
                engine_version=engine_version,
                bitrate=bitrate,
                max_fps=max_fps,
                max_size=max_size,
                record_path=record_path
            )

            # -----------------------------------------------------------------
            # DEBUG OUTPUT
            # -----------------------------------------------------------------

            print("\n================ SCRCPY COMMAND ================")

            print(" ".join(cmd))

            print("================================================\n")

            # -----------------------------------------------------------------
            # START PROCESS
            # -----------------------------------------------------------------

            process = self._create_process(cmd)

            # -----------------------------------------------------------------
            # STORE PROCESS
            # -----------------------------------------------------------------

            self.active_streams[device_id] = process

            print(
                f"[SCRCPY] Stream started for {device_id}"
            )

            return True

        except FileNotFoundError:

            print(
                "[SCRCPY ERROR] scrcpy executable not found."
            )

            return False

        except Exception as error:

            print(
                f"[SCRCPY ERROR] {error}"
            )

            return False

    # =========================================================================
    # STOP STREAM
    # =========================================================================

    def stop_stream(self, device_id):
        """
        Stop active stream.
        """

        try:

            if device_id not in self.active_streams:

                print(
                    "[SCRCPY] No active stream found."
                )

                return False

            process = self.active_streams[device_id]

            # -----------------------------------------------------------------
            # TERMINATE PROCESS
            # -----------------------------------------------------------------

            if process.poll() is None:

                process.terminate()

                try:

                    process.wait(timeout=5)

                except subprocess.TimeoutExpired:

                    process.kill()

            # -----------------------------------------------------------------
            # REMOVE TRACKING
            # -----------------------------------------------------------------

            del self.active_streams[device_id]

            print(
                f"[SCRCPY] Stream stopped for {device_id}"
            )

            return True

        except Exception as error:

            print(
                f"[STOP STREAM ERROR] {error}"
            )

            return False

    # =========================================================================
    # STOP ALL STREAMS
    # =========================================================================

    def stop_all_streams(self):
        """
        Stop every active scrcpy process.
        """

        devices = list(
            self.active_streams.keys()
        )

        for device_id in devices:

            self.stop_stream(device_id)

    # =========================================================================
    # CHECK STREAM STATUS
    # =========================================================================

    def is_stream_running(self, device_id):
        """
        Check if device stream is active.
        """

        if device_id not in self.active_streams:

            return False

        process = self.active_streams[device_id]

        return process.poll() is None

    # =========================================================================
    # GET ACTIVE DEVICES
    # =========================================================================

    def get_active_devices(self):
        """
        Return active streaming devices.
        """

        active = []

        for device_id, process in (
            self.active_streams.items()
        ):

            if process.poll() is None:

                active.append(device_id)

        return active