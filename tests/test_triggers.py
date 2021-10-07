import pytest

from perforce_triggers import triggers
from perforce_triggers import exceptions


trigger_script_data = {
    "name": "trigger_1",
    "type": "script",
    "event": "change-commit",
    "include_paths": ["//path/..."],
    "command": "python3 %//trigger/main.py%",
}

command_script_data = {
    "name": "trigger_2",
    "type": "command",
    "event": "pre-user-move",
    "command": "python3 %//trigger/main_2.py%",
}

test_script_trigger = triggers.ScriptTrigger(
    "trigger_1",
    "change-commit",
    ["//path/..."],
    "python3 %//trigger/main.py%"
)

test_command_trigger = triggers.CommandTrigger(
    "trigger_2",
     "pre-user-move",
      "python3 %//trigger/main_2.py%"

)
raise_exception = True
no_exception = False


class TestScriptTrigger:
    def test_get_p4_trigger_lines(self):
        # Basic script trigger
        test_script_trigger = triggers.ScriptTrigger(
            name="test",
            event="content-change",
            include_paths=[
                "//depot/branch/path_1/..."
            ],
            command="python //scripts/my_script.py"
        )

        expected = [
            'test content-change //depot/branch/path_1/... "python //scripts/my_script.py"'
        ]
        res = test_script_trigger.get_p4_trigger_lines()
        assert res == expected

        # script trigger with multiple include paths
        test_script_trigger.include_paths = [
            "//depot/branch/path_1/...",
            "//depot/branch/path_2/..."
        ]

        expected = [
            'test content-change //depot/branch/path_1/... "python //scripts/my_script.py"',
            'test content-change //depot/branch/path_2/... "python //scripts/my_script.py"'
        ]

        res = test_script_trigger.get_p4_trigger_lines()
        assert res == expected

        # trigger script with a single exclude path
        test_script_trigger.exclude_paths = [
            "//depot/branch/path_3/..."
        ]

        expected = [
            'test content-change //depot/branch/path_1/... "python //scripts/my_script.py"',
            'test content-change //depot/branch/path_2/... "python //scripts/my_script.py"',
            'test content-change -//depot/branch/path_3/... "python //scripts/my_script.py"'
        ]
        res = test_script_trigger.get_p4_trigger_lines()
        assert res == expected

        # trigger script with argument
        test_script_trigger = triggers.ScriptTrigger(
            name="test",
            event="content-change",
            include_paths=[
                "//depot/branch/path_1/..."
            ],
            command="python //scripts/my_script.py",
            args=["arg_1", "arg_2"]
        )

        expected = [
            'test content-change //depot/branch/path_1/... "python //scripts/my_script.py arg_1 arg_2"'
        ]
        res = test_script_trigger.get_p4_trigger_lines()
        assert res == expected


class TestCommandTrigger:
    def test_get_p4_trigger_lines(self):
        # Basic command trigger
        test_command_trigger = triggers.CommandTrigger(
            name="test",
            event="pre-cmd",
            command="python my_script"
        )

        expected = [
            'test command pre-cmd "python my_script"'
        ]

        res = test_command_trigger.get_p4_trigger_lines()
        assert expected == res

        # Command trigger with args
        test_command_trigger = triggers.CommandTrigger(
            name="test",
            event="pre-cmd",
            command="python my_script",
            args=["arg_1", "arg_2"]
        )

        expected = [
            'test command pre-cmd "python my_script arg_1 arg_2"'
        ]

        res = test_command_trigger.get_p4_trigger_lines()
        assert expected == res


@pytest.mark.parametrize(
    "trigger_config, expected, raise_exception",
    [
        (
            [trigger_script_data],
            [test_script_trigger],
            no_exception
        ),
        (
            [ trigger_script_data, command_script_data],
            [test_script_trigger, test_command_trigger],
            no_exception
        ),
        (
            [
                {
                    "name": "trigger_1",
                    "type": "something"
                }
            ],
            [],
            raise_exception
        ),
    ],
)
def test_get_triggers(trigger_config, expected, raise_exception, mocker):
    mocker.patch("perforce_triggers.config.get_config", return_value={
            "triggers": trigger_config
        })
    if raise_exception:
        with pytest.raises(exceptions.PerforceTriggersError):
            triggers.get_triggers()
    else:
        res = triggers.get_triggers()
        assert all(trigger_ in expected for trigger_ in res)
