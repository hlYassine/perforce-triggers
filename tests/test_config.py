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


