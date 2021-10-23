import pytest
from unittest.mock import MagicMock
from click.testing import CliRunner
from perforce_triggers import cli
from perforce_triggers import perforce
from perforce_triggers import triggers



@pytest.fixture(autouse=True)
def mocked_config(mocker):
    config_ = {
        "auth": {
            "user": "john.doe"
        }
    }
    mocker.patch("perforce_triggers.config.get_config", return_value=config_)
    return mocker


def test_list_triggers(mocker):
    runner = CliRunner()

    # remote
    mocker.patch("perforce_triggers.perforce.get_triggers")
    result = runner.invoke(cli.list_triggers, ["remote"])
    assert result.exit_code == 0
    perforce.get_triggers.assert_called()

    mocker.patch("perforce_triggers.triggers.get_triggers_from_config")
    
    # local
    result = runner.invoke(cli.list_triggers, ["local"])
    assert result.exit_code == 0
    triggers.get_triggers_from_config.assert_called_once()

    # invalid argument
    result = runner.invoke(cli.list_triggers, ["invalid"])
    assert result.exit_code != 0
    assert "'invalid' is not one of 'remote', 'local'" in result.output


def test_show_config():
    runner = CliRunner()

    # unsupported argument
    result = runner.invoke(cli.show_config, ["invalid"])
    assert result.exit_code != 0
    assert "'invalid' is not one of 'auth', 'location'" in result.output

    # valid field
    result = runner.invoke(cli.show_config, ["auth", "user"])
    assert result.exit_code == 0
    assert "auth.user = john.doe" in result.output

    # invalid field
    result = runner.invoke(cli.show_config, ["auth", "password"])
    assert result.exit_code == 0
    assert "Unkonwn configuration 'auth' field 'password'" in result.output
