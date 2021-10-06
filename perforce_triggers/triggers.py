import typing

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
