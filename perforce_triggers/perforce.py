import typing
import logging

from os import environ
from P4 import P4, P4Exception

from perforce_triggers import config
from perforce_triggers import exceptions

log = logging.getLogger(__name__)


def get_perforce_connection() -> P4:
    try:
        auth_config = config.get_config()["auth"]
        environ["P4TICKETS"] = auth_config["p4_tickets"]
        environ["P4IGNORE"] = ".p4ignore"

        p4_conn = P4()
        p4_conn.user = auth_config["p4_user"]
        p4_conn.port = auth_config["p4_port"]
        p4_conn.connect()

        return p4_conn
    except KeyError as config_error:
        raise exceptions.PerforceTriggersError(
            "perforce login details are not configured correctly!\n"
            f"error: missing key {config_error}"
        )
    except P4Exception as p4_error:
        raise exceptions.PerforceTriggersError(
            f"Failed to connect to perforce server '{auth_config['p4_port']}' "
            f"as user '{auth_config['p4_user']}'!\nerror: {p4_error}"
        )


def create_local_client(name, root_abspath, view_list):
    p4_conn = get_perforce_connection()
    client = p4_conn.fetch_client(name)
    client["Root"] = root_abspath
    client["Options"] = "allwrite clobber nocompress unlocked modtime rmdir"
    client["View"] = view_list
    client["Host"] = ""
    client["LineEnd"] = "local"
    try:
        p4_conn.save_client(client)
    except P4Exception as e:
        raise exceptions.PerforceTriggersError(
            f"Failed to create client '{name}':\n{e.value}"
        )


def get_triggers() -> typing.Optional[typing.List[str]]:
    try:
        p4_conn = get_perforce_connection()
        p4_triggers_output = p4_conn.run_triggers("-o")
        return (
            p4_triggers_output[0].get("Triggers", [])
            if p4_triggers_output else []
        )
    except Exception as e:
        raise exceptions.PerforceTriggersError(str(e))
