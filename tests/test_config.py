import pytest
from perforce_triggers import config, exceptions


def test_get_config(mocker):
    
    mocker.patch("perforce_triggers.config.get_config_abspath")

    debug_config_ = {"source": "debug config"}
    prod_config = {"source": "config_file"}
    
    # config file exists
    mocker.patch(f"{__name__}.open")
    mocker.patch("json.load", return_value=prod_config)
    mocker.patch("os.path.exists", return_value=True)
    
    config_ = config.get_config()
    assert config_ == prod_config

    # config file does not exist
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("perforce_triggers.config.DEBUG_CONFIG", debug_config_)

    config_ = config.get_config()
    assert config_ == debug_config_


def test_get_config_abspath(mocker):
    # Windows
    mocker.patch("platform.system", return_value="Windows")
    mocker.patch("os.environ", {"APPDATA": "C:/appdata"})
    expected = "C:/appdata/perforce_triggers/config.json"
    assert config.get_config_abspath() == expected

    # Linux
    mocker.patch("platform.system", return_value="Linux")
    expected = "/etc/perforce_triggers/config.json"
    assert config.get_config_abspath() == expected

    # Unsupported platform
    mocker.patch("platform.system", return_value="Unknown")
    with pytest.raises(exceptions.PerforceTriggersError) as e:
        config.get_config_abspath()
    assert "unsupported platform" in str(e)


def test_get_log_dir(mocker):
    # Windows
    mocker.patch("platform.system", return_value="Windows")
    mocker.patch("os.environ", {"APPDATA": "C:/appdata"})
    expected = "C:/appdata/perforce_triggers"
    assert config.get_log_dir() == expected

    # Linux
    mocker.patch("platform.system", return_value="Linux")
    expected = "/etc/perforce_triggers"
    assert config.get_log_dir() == expected

    # Unsupported platform
    mocker.patch("platform.system", return_value="Unknown")
    with pytest.raises(exceptions.PerforceTriggersError) as e:
        config.get_log_dir()
    assert "unsupported platform" in str(e)