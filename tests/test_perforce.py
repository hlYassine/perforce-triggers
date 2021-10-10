from P4 import P4Exception
import pytest
from perforce_triggers import perforce, exceptions
import perforce_triggers


def test_connect_to_perforce(mocker):
    # Incorrect configuration
    config_ = {}
    mocker.patch("perforce_triggers.config.get_config", return_value=config_)

    with pytest.raises(exceptions.PerforceTriggersError) as error_:
        perforce.connect_to_perforce()
    assert "perforce login details are not configured correctly!" in str(error_)

    # missing p4 tickets path
    config_ = {
        "auth": {
            "p4_user": "jdoe",
            "p4_port": "perforce:1666"
        }
    }

    mocker.patch("perforce_triggers.config.get_config", return_value=config_)

    with pytest.raises(exceptions.PerforceTriggersError) as error_:
        perforce.connect_to_perforce()
    assert "perforce login details are not configured correctly!" in str(error_)

    # connection error
    config_ = {
        "auth": {
            "p4_user": "jdoe",
            "p4_port": "perforce:1666",
            "p4_tickets": "/home/jdoe/.p4tickets"
        }
    }
    mocker.patch("perforce_triggers.config.get_config", return_value=config_)

    class P4Mock:
        def connect():
            raise P4Exception("failed")
    mocker.patch("P4.P4", new=P4Mock())
    
    with pytest.raises(exceptions.PerforceTriggersError) as error_:
        perforce.connect_to_perforce()
    assert "Failed to connect to perforce server 'perforce:1666' as user 'jdoe'" in str(error_)
