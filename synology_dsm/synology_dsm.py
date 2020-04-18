# -*- coding: utf-8 -*-
"""Class to interact with Synology DSM."""
import socket
import urllib3
from requests import Session
from requests.compat import json
from requests.exceptions import RequestException
from simplejson.errors import JSONDecodeError
import six

from .exceptions import (
    SynologyDSMAPINotExistsException,
    SynologyDSMRequestException,
    SynologyDSMLoginFailedException,
    SynologyDSMLoginInvalidException,
    SynologyDSMLoginDisabledAccountException,
    SynologyDSMLoginPermissionDeniedException,
    SynologyDSMLogin2SARequiredException,
    SynologyDSMLogin2SAFailedException,
)
from .api.core.utilization import SynoCoreUtilization
from .api.dsm.information import SynoDSMInformation
from .api.storage.storage import SynoStorage

if six.PY2:
    from future.moves.urllib.parse import urlencode
else:
    from urllib.parse import urlencode  # pylint: disable=import-error,no-name-in-module

import logging
_LOGGER = logging.getLogger(__name__)

class SynologyDSM(object):
    """Class containing the main Synology DSM functions."""

    API_INFO = "SYNO.API.Info"
    API_AUTH = "SYNO.API.Auth"

    def __init__(
        self,
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        device_token=None,
        debugmode=False,
    ):
        self.username = username
        self._password = password
        self._debugmode = debugmode

        # Session
        self._session_error = False
        self._session = None

        # Login
        self._session_id = None
        self._syno_token = None
        self._device_token = device_token

        # Services
        self._apis = {}
        self._information = None
        self._utilisation = None
        self._storage = None

        # Build variables
        if use_https:
            # https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
            # disable SSL warnings due to the auto-genenerated cert
            urllib3.disable_warnings()

            self._base_url = "https://%s:%s" % (dsm_ip, dsm_port)
        else:
            self._base_url = "http://%s:%s" % (dsm_ip, dsm_port)

    def _debuglog(self, message):
        """Outputs message if debug mode is enabled."""
        if self._debugmode:
            print("DEBUG: " + message)

    def _build_url(self, api, method, params=None):
        if api == self.API_INFO:
            return "%s/webapi/query.cgi?api=%s&version=1&method=query&query=ALL" % (
                self._base_url,
                api,
            )

        self._discover_apis()

        _LOGGER.warning(api)
        _LOGGER.warning(self.apis.get(api))
        if not self.apis.get(api):
            raise SynologyDSMAPINotExistsException(api)

        if params is None:
            params = {}
        params = {
            **{"api": api, "version": self.apis[api]["maxVersion"], "method": method},
            **params,
        }

        if api == SynoStorage.API_KEY and self.information and self.information.version and int(self.information.version) < 7321: # < DSM 6
            return "%s/webman/modules/StorageManager/storagehandler.cgi?action=%s" % (self._base_url, method)

        return "%s/webapi/%s?%s" % (self._base_url, self.apis[api]["path"], urlencode(params))

    def _discover_apis(self):
        
        _LOGGER.warning("_discover_apis")
        if self._apis:
            _LOGGER.warning("PAS_BESION")
            return
        url = self._build_url(self.API_INFO, None)
        self._apis = self._execute_get_url(url)["data"]

    @property
    def apis(self):
        return self._apis

    # def request_api(self, api, method):
    #     return None

    def login(self, otp_code=None):
        """Create a logged session."""
        # First reset the session
        if self._session:
            self._session = None
        self._debuglog("Creating new Session")
        self._session = Session()
        self._session.verify = False
        _LOGGER.warning("login")

        # self._discover_apis()

        params = {
            "account": self.username,
            "passwd": self._password,
            "enable_syno_token": "yes",
            "enable_device_token": "yes",
            "device_name": socket.gethostname(),
            "format": "sid",
        }

        if otp_code:
            params["otp_code"] = otp_code
        if self._device_token:
            params["device_id"] = self._device_token

        url = self._build_url(self.API_AUTH, "login", params)

        result = self._execute_get_url(url)

        if not result:
            self._session_id = None
            self._syno_token = None
            self._device_token = None
            self._debuglog("Authentication Failed")
            return False

        if result.get("error"):
            switcher = {
                400: SynologyDSMLoginInvalidException(self.username),
                401: SynologyDSMLoginDisabledAccountException(self.username),
                402: SynologyDSMLoginPermissionDeniedException(self.username),
                403: SynologyDSMLogin2SARequiredException(self.username),
                404: SynologyDSMLogin2SAFailedException,
            }
            raise switcher.get(result["error"]["code"], SynologyDSMLoginFailedException)

        # Parse result if valid
        self._session_id = result["data"]["sid"]
        if result["data"].get("synotoken"):
            # Not available on API version < 3
            self._syno_token = result["data"]["synotoken"]
        if result["data"].get("did"):
            # Not available on API version < 6 && device token is given once per device_name
            self._device_token = result["data"]["did"]
        self._debuglog("Authentication Succesfull, token: " + str(self._session_id))

        return True

    @property
    def device_token(self):
        """Gets the device token to remember the 2SA access was granted on this device."""
        return self._device_token

    def _get_url(self, url, retry_on_error=True):
        """Function to handle sessions for a GET request."""
        # Check if we failed to request the url or need to login
        if self._session_id is None or self._session is None or self._session_error:
            # Reset session error
            self._session_error = False

            # Created a new logged session
            if self.login() is False:
                self._session_error = True
                self._debuglog("Login Failed, unable to process request")
                return None

        # Now request the data
        response = self._execute_get_url(url)
        if (self._session_error or response is None) and retry_on_error:
            self._debuglog("Error occured, retrying...")
            return self._get_url(url, False)

        return response

    def _execute_get_url(self, request_url):
        """Function to execute and handle a GET request."""
        # Prepare Request
        self._debuglog("Requesting URL: '" + request_url + "'")
        if self._session_id:
            self._debuglog(
                "Appending access_token (SESSION_ID: " + self._session_id + ") to url"
            )
            request_url = "%s&_sid=%s" % (request_url, self._session_id)
        if self._syno_token:
            self._debuglog(
                "Appending access_token (SYNO_TOKEN: " + self._syno_token + ") to url"
            )
            request_url = "%s&SynoToken=%s" % (request_url, self._syno_token)

        # Execute Request
        try:
            resp = self._session.get(request_url)
            self._debuglog("Request executed: " + str(resp.status_code))
            if resp.status_code == 200:
                # We got a response
                json_data = json.loads(resp.text)

                if json_data.get("error"):
                    self._debuglog("Session error: " + str(json_data["error"]["code"]))
                    if json_data["error"]["code"] in {106, 107, 119}:
                        self._session_error = True
                        raise RequestException(resp)

                self._debuglog("Successful returning data")
                self._debuglog(str(json_data))
                return json_data
            # We got a 400, 401 or 404 ...
            raise RequestException(resp)
        except (RequestException, JSONDecodeError) as exp:
            raise SynologyDSMRequestException(exp)

    def update(self, with_information=False):
        """Updates the various instanced modules."""
        if self._information and with_information:
            url = self._build_url(SynoDSMInformation.API_KEY, "getinfo")
            self._information.update(self._get_url(url))

        if self._utilisation:
            url = self._build_url(SynoCoreUtilization.API_KEY, "get")
            self._utilisation.update(self._get_url(url))

        if self._storage:
            url = self._build_url(SynoStorage.API_KEY, "load_info")
            self._storage.update(self._get_url(url))

    @property
    def information(self):
        """Gets NAS informations."""
        if self._information is None and self._session_id:
            url = self._build_url(SynoDSMInformation.API_KEY, "getinfo")
            self._information = SynoDSMInformation(self._get_url(url))
        return self._information

    @property
    def utilisation(self):
        """Getter for various Utilisation variables."""
        if self._utilisation is None:
            url = self._build_url(SynoCoreUtilization.API_KEY, "get")
            self._utilisation = SynoCoreUtilization(self._get_url(url))
        return self._utilisation

    @property
    def storage(self):
        """Getter for various Storage variables."""
        if self._storage is None:
            url = self._build_url(SynoStorage.API_KEY, "load_info")
            self._storage = SynoStorage(self._get_url(url))

        return self._storage
