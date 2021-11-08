import typing
import logging

from perforce_triggers import config
from perforce_triggers import exceptions
from perforce_triggers import perforce

log = logging.getLogger(__name__)

TRIGGERS = {}


def trigger(cls):
    TRIGGERS[cls.trigger_type] = cls
    return cls


class Trigger:
    trigger_type = "base"

    def __init__(
        self,
        name: str,
        event: str,
        command: str,
        args: typing.List[str] = None
    ) -> None:
        self.name = name
        self.event = event
        self.command = command
        self.args = args
        self.script = f"{self.command} {' '.join(self.args)}" if self.args else f"{self.command}"

    def get_p4_trigger_lines(self) -> typing.List[str]:
        raise NotImplementedError

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, self.__class__):
            return False
        return self.__dict__ == obj.__dict__


@trigger
class ScriptTrigger(Trigger):
    trigger_type = "script"

    def __init__(
        self,
        name: str,
        event: str,
        include_paths: typing.List[str],
        command: str,
        exclude_paths: typing.List[str] = None,
        args: typing.List[str] = None
    ) -> None:
        super().__init__(name, event, command, args)
        self.include_paths = include_paths
        self.exclude_paths = exclude_paths if exclude_paths else []

    def get_p4_trigger_lines(self) -> typing.List[str]:
        inc_script_trigger_tpl = '{name} {event} {p4_path} "{script}"'
        exc_script_trigger_tpl = '{name} {event} -{p4_path} "{script}"'

        include_path_trigger_list = [
            inc_script_trigger_tpl.format(
                name=self.name,
                event=self.event,
                p4_path=p4_path,
                script=self.script
            )
            for p4_path in self.include_paths
        ]

        exclude_path_trigger_list = [
            exc_script_trigger_tpl.format(
                name=self.name,
                event=self.event,
                p4_path=p4_path,
                script=self.script
            )
            for p4_path in self.exclude_paths
        ]
        return include_path_trigger_list + exclude_path_trigger_list


@trigger
class CommandTrigger(Trigger):
    trigger_type = "command"

    def get_p4_trigger_lines(self) -> typing.List[str]:
        command_trigger_tpl = '{name} command {event} "{script}"'
        return [
            command_trigger_tpl.format(
                name=self.name,
                event=self.event,
                script=self.script)
        ]


def get_triggers_from_config() -> typing.List[Trigger]:
    config_ = config.get_config()
    trigger_config_list = config_.get("triggers", [])
    trigger_list = []
    for trigger_info in trigger_config_list:
        try:
            trigger_attrs = {
                attr: trigger_info[attr]
                for attr in trigger_info
                if attr != "type"
            }
            trigger_type = trigger_info["type"]
            trigger_list.append(
                TRIGGERS[trigger_type](**trigger_attrs)
            )
        except KeyError as error_:
            raise exceptions.PerforceTriggersError(
                f"Unsupported trigger type '{trigger_type}'"
            ) from error_
    return trigger_list


def submit_triggers():
    location_config = config.get_config().get("location", {})
    client_name = "p4_triggers"
    location_view_line = f"{location_config.get('local')} //{client_name}/..."
    try:
        with perforce.get_triggers_client() as p4_conn:
            sync_p4_path = f"//{p4_conn.client}/..."
            p4_conn.run_sync("-k", sync_p4_path)
            p4_conn.run_sync("-k", sync_p4_path)

            perforce.p4_reconcile(p4_conn, sync_p4_path)

            p4_conn.run_submit("-d", "Update perforce triggers")
    except exceptions.PerforceTriggersError as e:
        log.error(e)
