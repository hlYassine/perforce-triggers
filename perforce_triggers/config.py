import typing
import tempfile
import platform
import json

from os import getenv, path
from perforce_triggers import exceptions


P4_DEFAULT_WKS_ROOT = tempfile.gettempdir()
CONFIG_FILE_RELPATH = "perforce_triggers/config.json"
LOG_FILE_RELPATH = "perforce_triggers/log.txt"


DEBUG_CONFIG = {
    "auth": {
        "p4_port": "perforce:1666",
        "p4_user": "perforce",
        "p4_tickets": "/home/perforce/.p4tickets"
    },
    "triggers": [
        {
            "name": "my_trigger",
            "type": "script",
            "event": "change-commit",
            "include_paths": ["//depot/..."],
            "exclude_paths": [],
            "command": "/usr/bin/python3.6 %//triggers/on_submit.py%",
            "args": {}
        }
    ]
}


def get_config() -> typing.Dict:
    config_abspath = get_config_abspath()
    if path.exists(config_abspath):
        with open(config_abspath, "r", encoding="utf-8") as fd:
            return dict(json.load(fd))
    return DEBUG_CONFIG


def get_config_abspath() -> str:
    if platform.system() == "Linux":
        return path.join("/etc", CONFIG_FILE_RELPATH)

    if platform.system() == "Windows":
        return path.join(str(getenv("APPDATA")), CONFIG_FILE_RELPATH)

    raise exceptions.PerforceTriggersError(
        f"unsupported platform '{platform.system()}'!")


def get_log_dir() -> str:
    if platform.system() == "Linux":
        return "/etc/perforce_triggers"

    if platform.system() == "Windows":
        return path.join(str(getenv("APPDATA")), "perforce_triggers")

    raise exceptions.PerforceTriggersError(
        f"unsupported platform '{platform.system()}'!")
