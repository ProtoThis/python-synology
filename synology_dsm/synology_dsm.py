# -*- coding: utf-8 -*-
"""Class to interact with Synology DSM."""
import socket
import urllib3
from requests import Session
from requests.exceptions import RequestException
from simplejson.errors import JSONDecodeError

from .exceptions import (
    SynologyDSMAPIErrorException,
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
        self._session = Session()
        self._session.verify = False

        # Login
        self._session_id = None
        self._syno_token = None
        self._device_token = device_token

        # Services
        self._apis = {
            "SYNO.API.Info": {"maxVersion": 1, "minVersion": 1, "path": "query.cgi"}
        }
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

    def _build_url(self, api):
        if (
            api == SynoStorage.API_KEY
            and self._information
            and self._information.version
            and int(self._information.version) < 7321  # < DSM 6
        ):
            return (
                "%s/webman/modules/StorageManager/storagehandler.cgi?" % self._base_url
            )

        return "%s/webapi/%s?" % (self._base_url, self.apis[api]["path"])

    def discover_apis(self):
        """Retreives available API infos from the NAS."""
        if self._apis.get(self.API_AUTH):
            return
        self._apis = self.get(self.API_INFO, "query")["data"]

    @property
    def apis(self):
        """Gets available API infos from the NAS."""
        return self._apis

    def login(self, otp_code=None):
        """Create a logged session."""
        # First reset the session
        self._debuglog("Creating new session")
        self._session = Session()
        self._session.verify = False

        params = {
            "account": self.username,
            "passwd": self._password,
            # "enable_syno_token": "yes",
            "enable_device_token": "yes",
            "device_name": socket.gethostname(),
            "format": "sid",
        }

        if otp_code:
            params["otp_code"] = otp_code
        if self._device_token:
            params["device_id"] = self._device_token

        # Request login
        result = self.get(self.API_AUTH, "login", params)

        # Handle errors
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
        self._debuglog("Authentication successful, token: " + str(self._session_id))

        if not self._information:
            data = self.get(SynoDSMInformation.API_KEY, "getinfo")
            self._information = SynoDSMInformation(data)

        return True

    @property
    def device_token(self):
        """Gets the device token to remember the 2SA access was granted on this device."""
        return self._device_token

    def get(self, api, method, params=None, **kwargs):
        """Handles API GET request."""
        return self._request("GET", api, method, params, **kwargs)

    def post(self, api, method, params=None, data=None, json=None, **kwargs):
        """Handles API POST request."""
        return self._request(
            "POST", api, method, params, data=data, json=json, **kwargs
        )

    def _request(
        self, request_method, api, method, params=None, retry_once=True, **kwargs
    ):
        """Handles API request."""
        # Discover existing APIs
        if api != self.API_INFO:
            self.discover_apis()

        # Check if logged
        if not self._session_id and api not in [self.API_AUTH, self.API_INFO]:
            self.login()

        # Check if API is available
        if not self.apis.get(api):
            raise SynologyDSMAPINotExistsException(api)

        # Build request params
        if not params:
            params = {}
        params["api"] = api
        params["version"] = self.apis[api]["maxVersion"]
        params["method"] = method

        if api == SynoStorage.API_KEY:
            params["action"] = method
        if self._session_id:
            params["_sid"] = self._session_id
        if self._syno_token:
            params["SynoToken"] = self._syno_token
        self._debuglog("Request params: " + str(params))

        # Request data
        url = self._build_url(api)
        response = self._execute_request(request_method, url, params=params, **kwargs)
        self._debuglog("Successful returned data")
        self._debuglog("API: " + api)
        self._debuglog(str(response))

        # Handle data errors
        if response.get("error") and api != self.API_AUTH:
            self._debuglog("Session error: " + str(response["error"]["code"]))
            if response["error"]["code"] == 119 and retry_once:
                # Session ID not valid, see https://github.com/aerialls/synology-srm/pull/3
                self._session_id = None
                self._syno_token = None
                self._device_token = None
                return self._request(request_method, api, method, params, False)
            raise SynologyDSMAPIErrorException(api, response["error"]["code"])

        return response

    def _execute_request(self, method, url, **kwargs):
        """Function to execute and handle a request."""
        # Execute Request
        try:
            if method == "GET":
                resp = self._session.get(url, **kwargs)
            elif method == "POST":
                resp = self._session.post(url, **kwargs)

            self._debuglog("Request url: " + resp.url)
            self._debuglog("Request status_code: " + str(resp.status_code))
            self._debuglog("Request headers: " + str(resp.headers))

            if resp.status_code == 200:
                # We got a DSM response
                return resp.json()

            # We got a 400, 401 or 404 ...
            raise RequestException(resp)

        except (RequestException, JSONDecodeError) as exp:
            raise SynologyDSMRequestException(exp)

    def update(self, with_information=False):
        """Updates the various instanced modules."""
        if self._information and with_information:
            data = self.get(SynoDSMInformation.API_KEY, "getinfo")
            self._information.update(data)

        if self._utilisation:
            data = self.get(SynoCoreUtilization.API_KEY, "get")
            self._utilisation.update(data)

        if self._storage:
            data = self.get(SynoStorage.API_KEY, "load_info")
            self._storage.update(data)

    @property
    def information(self):
        """Gets NAS informations."""
        if not self._information:
            data = self.get(SynoDSMInformation.API_KEY, "getinfo")
            self._information = SynoDSMInformation(data)
        return self._information

    @property
    def utilisation(self):
        """Gets NAS utilisation informations."""
        if not self._utilisation:
            data = self.get(SynoCoreUtilization.API_KEY, "get")
            self._utilisation = SynoCoreUtilization(data)
        return self._utilisation

    @property
    def storage(self):
        """Gets NAS storage informations."""
        if not self._storage:
            data = self.get(SynoStorage.API_KEY, "load_info")
            self._storage = SynoStorage(data)
        return self._storage
