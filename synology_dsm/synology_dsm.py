# -*- coding: utf-8 -*-
"""Class to interact with Synology DSM."""
import socket
import urllib3
from requests import Session
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
        self._session = Session()
        self._session.verify = False

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

        if not self.apis.get(api):
            raise SynologyDSMAPINotExistsException(api)

        if params is None:
            params = {}
        params = {
            **{"api": api, "version": self.apis[api]["maxVersion"], "method": method},
            **params,
        }

        if (
            api == SynoStorage.API_KEY
            and self._information
            and self._information.version
            and int(self._information.version) < 7321  # < DSM 6
        ):
            return "%s/webman/modules/StorageManager/storagehandler.cgi?action=%s" % (
                self._base_url,
                method,
            )

        return "%s/webapi/%s?%s" % (
            self._base_url,
            self.apis[api]["path"],
            urlencode(params),
        )

    def _discover_apis(self):
        """Retreives available API infos from the NAS."""
        if self._apis:
            return
        url = self._build_url(self.API_INFO, None)
        self._apis = self._execute_request(url)["data"]

    @property
    def apis(self):
        """Gets available API infos from the NAS."""
        return self._apis

    def login(self, otp_code=None):
        """Create a logged session."""
        # First reset the session
        self._debuglog("Creating new Session")
        self._session = Session()
        self._session.verify = False

        self._discover_apis()

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
        result = self._execute_request(url)

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

    def request(self, api, method, params=None):
        """Handles API request."""
        # Check if logged
        if not self._session_id:
            self.login()

        # Request the data
        url = self._build_url(api, method, params)
        response = self._execute_request(url)

        # Handle data errors

        return response

    def _execute_request(self, request_url):
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
                json_data = resp.json()

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
            data = self.request(SynoDSMInformation.API_KEY, "getinfo")
            self._information.update(data)

        if self._utilisation:
            data = self.request(SynoCoreUtilization.API_KEY, "get")
            self._utilisation.update(data)

        if self._storage:
            data = self.request(SynoStorage.API_KEY, "load_info")
            self._storage.update(data)

    @property
    def information(self):
        """Gets NAS informations."""
        if self._information is None:
            data = self.request(SynoDSMInformation.API_KEY, "getinfo")
            self._information = SynoDSMInformation(data)
        return self._information

    @property
    def utilisation(self):
        """Gets NAS utilisation informations."""
        if self._utilisation is None:
            data = self.request(SynoCoreUtilization.API_KEY, "get")
            self._utilisation = SynoCoreUtilization(data)
        return self._utilisation

    @property
    def storage(self):
        """Gets NAS storage informations."""
        if self._storage is None:
            data = self.request(SynoStorage.API_KEY, "load_info")
            self._storage = SynoStorage(data)

        return self._storage
