from os import environ
from P4 import P4, P4Exception

from perforce_triggers import config
from perforce_triggers import exceptions


def connect_to_perforce():
    try:
        auth_config = config.get_config()["auth"]
        environ["P4TICKETS"] = auth_config["p4_tickets"]
        environ["P4IGNORE"] = ".p4ignore"

        p4_conn = P4()
        p4_conn.user = auth_config["p4_user"]
        p4_conn.port = auth_config["p4_port"]
        p4_conn.connect()
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
