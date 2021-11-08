import typing
import logging
import contextlib

from os import environ
from P4 import P4, P4Exception

from perforce_triggers import config
from perforce_triggers import exceptions

log = logging.getLogger(__name__)


@contextlib.contextmanager
def get_triggers_client():
    client_name = "p4_triggers_wks"

    loc_config = config.get_config().get("location", {})
    client_view = f"{loc_config['remote']} //{client_name}/..."

    client_root = loc_config["local"]

    p4_conn = create_local_client(
        client_name,
        client_root,
        client_view
    )
    try:
        yield p4_conn
    finally:
        p4_conn.disconnect()


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


def create_local_client(name, root_abspath, view_list) -> P4:
    p4_conn = get_perforce_connection()
    client = p4_conn.fetch_client(name)
    client["Root"] = root_abspath
    client["Options"] = "allwrite clobber nocompress unlocked modtime rmdir"
    client["View"] = view_list
    client["Host"] = ""
    client["LineEnd"] = "local"
    try:
        p4_conn.save_client(client)
        return p4_conn
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


def p4_reconcile(p4_conn: P4, p4_path: str):
    try:
        # pylint: disable=line-too-long
        p4_reconcile_args = [
            "-a",  # reconcile new files that are in root but not tracked by the client
            "-d",  # reconcile files that have been removed from root but are still in the depot
            "-e",  # reconcile files that have been modified outside of Perforce
            "-m",  # minimize costly digest computation on the client by checking file modification times
            # before checking digests to determine if files have been modified
            # outside of Perforce
            p4_path,
        ]
        log.info(f"p4 reconcile {' '.join(p4_reconcile_args)}")
        p4_conn.run_reconcile(p4_reconcile_args)
    except P4Exception as e:
        if "no file(s) to reconcile." in e.value:
            log.warn("no file(s) to reconcile.")
            pass
        else:
            raise exceptions.PerforceTriggersError(
                f"Failed to run p4 reconcile {e}"
            )
