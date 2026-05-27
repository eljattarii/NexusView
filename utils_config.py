# =============================================================================
# utils_config.py
# =============================================================================
#
# Enterprise Configuration Manager
# -----------------------------------------------------------------------------
# Features:
#   - Automatic config creation
#   - Safe JSON handling
#   - Default fallback system
#   - Corrupted file protection
#   - Future scalability
#   - Reset configuration support
#
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

import json
import os


# =============================================================================
# CONFIGURATION FILE
# =============================================================================

CONFIG_FILE = "config.json"


# =============================================================================
# DEFAULT CONFIGURATION
# =============================================================================

DEFAULT_CONFIG = {

    # -------------------------------------------------------------------------
    # STREAM SETTINGS
    # -------------------------------------------------------------------------

    "bitrate": "Default",

    "resolution": "Default",

    "fps": "Default",

    # -------------------------------------------------------------------------
    # UI SETTINGS
    # -------------------------------------------------------------------------

    "theme": "dark",

    "last_device": "",

    "window_width": 1100,

    "window_height": 700,

    # -------------------------------------------------------------------------
    # FILE MANAGER
    # -------------------------------------------------------------------------

    "last_local_directory": "",

    "last_phone_directory": "/sdcard/",
}


# =============================================================================
# ENSURE CONFIG FILE EXISTS
# =============================================================================

def ensure_config_exists():
    """
    Create config.json if missing.
    """

    if not os.path.exists(CONFIG_FILE):

        save_config(
            DEFAULT_CONFIG.copy()
        )


# =============================================================================
# SAVE CONFIG
# =============================================================================

def save_config(config_dict):
    """
    Save configuration safely.

    Parameters:
        config_dict (dict):
            Configuration values.
    """

    try:

        # ---------------------------------------------------------------------
        # MERGE WITH DEFAULTS
        # ---------------------------------------------------------------------

        final_config = DEFAULT_CONFIG.copy()

        final_config.update(config_dict)

        # ---------------------------------------------------------------------
        # WRITE FILE
        # ---------------------------------------------------------------------

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                final_config,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            "[CONFIG] Configuration saved successfully."
        )

    except Exception as error:

        print(
            f"[CONFIG SAVE ERROR] {error}"
        )


# =============================================================================
# LOAD CONFIG
# =============================================================================

def load_config():
    """
    Load configuration safely.

    Returns:
        dict:
            Configuration dictionary.
    """

    try:

        # ---------------------------------------------------------------------
        # ENSURE FILE EXISTS
        # ---------------------------------------------------------------------

        ensure_config_exists()

        # ---------------------------------------------------------------------
        # LOAD FILE
        # ---------------------------------------------------------------------

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # ---------------------------------------------------------------------
        # VALIDATE KEYS
        # ---------------------------------------------------------------------

        validated = DEFAULT_CONFIG.copy()

        validated.update(data)

        return validated

    except json.JSONDecodeError:

        print(
            "[CONFIG ERROR] Corrupted JSON detected."
        )

        # ---------------------------------------------------------------------
        # RESET CORRUPTED FILE
        # ---------------------------------------------------------------------

        save_config(
            DEFAULT_CONFIG.copy()
        )

        return DEFAULT_CONFIG.copy()

    except Exception as error:

        print(
            f"[CONFIG LOAD ERROR] {error}"
        )

        return DEFAULT_CONFIG.copy()


# =============================================================================
# RESET CONFIGURATION
# =============================================================================

def reset_config():
    """
    Restore default configuration.
    """

    save_config(
        DEFAULT_CONFIG.copy()
    )

    print(
        "[CONFIG] Configuration reset completed."
    )