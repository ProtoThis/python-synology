# -*- coding: utf-8 -*-
"""Get datas to test Synology DSM library."""
from unittest import TestCase
from synology_dsm import SynologyDSM

NB_SEPARATOR = 20


#################################
# STEPS TO GET DATA FOR TESTERS #
#################################

# Fill constants DO NOT COMMIT THEM !
HOST = "host"
PORT = 443
USERNAME = "user"
PASSWORD = "password"
HTTPS = True
VERSION = 6

# Launch the data getter like this :
# py.test get_data_for_tests.py

# WARNING /!\
# If you have `AssertionError: assert False` at `assert api.login()`,
# its because the NAS is unreachable/can't connect to account with cconstants you gave

# It's gonna log data like :
# 1. Requested URL
# 2. Access token
# 3. Request response http code
# 4. Request response raw data (After "Succesfull returning data" log)

# The raw data is needed data to Python tests
# Use SERIAL, SID, UNIQUE_KEY constants for required fields, see const_dsm_6.py as exemple
# You can push your const_dsm_[dsm_version].py file
# Commit message can be "Add DSM [dsm_version] test constants"


class TestSynologyDSM(TestCase):
    """SynologyDSM test cases."""

    def test_get_all(self):  # pylint: disable=no-self-use
        """Launch data getter."""
        print("-" * NB_SEPARATOR + " INIT " + "-" * NB_SEPARATOR)
        api = SynologyDSM(
            HOST,
            PORT,
            USERNAME,
            PASSWORD,
            use_https=HTTPS,
            debugmode=True,
            dsm_version=VERSION,
        )

        print("-" * NB_SEPARATOR + " LOGIN " + "-" * NB_SEPARATOR)
        assert api.login()
        print("-" * NB_SEPARATOR + " LOGIN_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " INFORMATION " + "-" * NB_SEPARATOR)
        assert api.information
        print("-" * NB_SEPARATOR + " INFORMATION_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " UTILIZATION " + "-" * NB_SEPARATOR)
        assert api.utilisation
        print("-" * NB_SEPARATOR + " UTILIZATION_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " STORAGE " + "-" * NB_SEPARATOR)
        assert api.storage
        print("-" * NB_SEPARATOR + " STORAGE_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " END " + "-" * NB_SEPARATOR)
        assert False  # Stop the test with error, so we see logs
