from perforce_triggers import triggers
from perforce_triggers.triggers import trigger


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
