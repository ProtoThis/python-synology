# -*- coding: utf-8 -*-
"""Get datas to test Synology DSM library."""
from unittest import TestCase
from synology_dsm import SynologyDSM

NB_SEPARATOR = 40


#################################
# STEPS TO GET DATA FOR TESTERS #
#################################

# Fill constants DO NOT COMMIT THEM !
HOST = "host"
PORT = 443
USERNAME = "user"
PASSWORD = "password"
HTTPS = True

OTP_CODE = None  # If your account needs a two-step authentication (2SA)
DEVICE_TOKEN = None  # Only if already logged in with a 2SA account

# Launch the data getter like this :
# py.test get_data_for_tests.py

# WARNING /!\
# If you have `AssertionError: assert False` at `assert api.login()`,
# its because the NAS is unreachable/can't connect to account with constants you gave

# It's gonna log data like :
# 1. Requested URL
# 2. Access token
# 3. Request response http code
# 4. Request response raw data (After "Successful returned data" and "API: [X]" logs)

# The raw data is needed data to Python tests
# Use SERIAL, SESSION_ID, UNIQUE_KEY constants for required fields, see const_dsm_6.py as exemple
# You can push your const_dsm_[dsm_version].py file
# Commit message can be "Add DSM [dsm_version] test constants"

# pylint: disable=no-self-use
class TestSynologyDSM(TestCase):
    """SynologyDSM test cases."""

    def test_get_all(self):
        """Launch data getter."""
        print("-" * NB_SEPARATOR + " INIT " + "-" * NB_SEPARATOR)
        api = SynologyDSM(
            HOST,
            PORT,
            USERNAME,
            PASSWORD,
            use_https=HTTPS,
            device_token=DEVICE_TOKEN,
            debugmode=True,
        )

        print("-" * NB_SEPARATOR + " LOGIN " + "-" * NB_SEPARATOR)
        assert api.login(OTP_CODE)
        if api.device_token:
            print("DEVICE_TOKEN (do not publish): " + api.device_token)
        print("-" * NB_SEPARATOR + " LOGIN_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " API_INFORMATION " + "-" * NB_SEPARATOR)
        assert api.apis.get("SYNO.API.Auth")
        print("UP here, look for 'API: SYNO.API.Info'")
        print("-" * NB_SEPARATOR + " API_INFORMATION_END " + "-" * NB_SEPARATOR)

        # DSM
        print("-" * NB_SEPARATOR + " DSM_INFORMATION " + "-" * NB_SEPARATOR)
        assert api.information
        print("UP here, look for 'API: SYNO.DSM.Info'")
        print("-" * NB_SEPARATOR + " DSM_INFORMATION_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " DSM_NETWORK " + "-" * NB_SEPARATOR)
        assert api.network
        print("-" * NB_SEPARATOR + " DSM_NETWORK_END " + "-" * NB_SEPARATOR)

        # Core
        print("-" * NB_SEPARATOR + " CORE_SECURITY " + "-" * NB_SEPARATOR)
        assert api.security
        print("-" * NB_SEPARATOR + " CORE_SECURITY_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " CORE_UTILISATION " + "-" * NB_SEPARATOR)
        assert api.utilisation
        print("-" * NB_SEPARATOR + " CORE_UTILISATION_END " + "-" * NB_SEPARATOR)

        # Storage
        print("-" * NB_SEPARATOR + " STORAGE " + "-" * NB_SEPARATOR)
        assert api.storage
        print("-" * NB_SEPARATOR + " STORAGE_END " + "-" * NB_SEPARATOR)

        print("-" * NB_SEPARATOR + " END " + "-" * NB_SEPARATOR)
        assert False  # Stop the test with error, so we see logs
