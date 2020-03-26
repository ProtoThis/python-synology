"""Classe to interact with Synology DSM."""
# -*- coding:utf-8 -*-
import urllib3
import requests
from requests.compat import json
import six

from .api.core.utilization import SynoCoreUtilization
from .api.dsm.information import SynoDSMInformation
from .api.storage.storage import SynoStorage

if six.PY2:
    from future.moves.urllib.parse import urlencode
else:
    from urllib.parse import urlencode


class SynologyDSM(object):
    """Class containing the main Synology DSM functions."""

    def __init__(
        self,
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        debugmode=False,
        dsm_version=6,
    ):
        # Store Variables
        self.username = username
        self.password = password

        # Class Variables
        self.access_token = None
        self._information = None
        self._utilisation = None
        self._storage = None
        self._debugmode = debugmode
        self._use_https = use_https

        # Define Session
        self._session_error = False
        self._session = None

        # adding DSM Version
        self._dsm_version = dsm_version

        # Build Variables
        if self._use_https:
            # https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
            # disable SSL warnings due to the auto-genenerated cert
            urllib3.disable_warnings()

            self.base_url = "https://%s:%s/webapi" % (dsm_ip, dsm_port)
        else:
            self.base_url = "http://%s:%s/webapi" % (dsm_ip, dsm_port)

        if self._dsm_version == 5:
            if self._use_https:
                self.storage_url = (
                    "https://%s:%s/webman/modules/StorageManager/storagehandler.cgi"
                    % (dsm_ip, dsm_port)
                )
            else:
                self.storage_url = (
                    "http://%s:%s/webman/modules/StorageManager/storagehandler.cgi"
                    % (dsm_ip, dsm_port)
                )

    def _debuglog(self, message):
        """Outputs message if debug mode is enabled."""
        if self._debugmode:
            print("DEBUG: " + message)

    def _encode_credentials(self):
        """Encode user credentials to support special characters.."""
        # encoding special characters
        auth = {
            "account": self.username,
            "passwd": self.password,
        }
        return urlencode(auth)

    def login(self):
        """Create a logged session.."""
        # First reset the session
        if self._session:
            self._session = None
        self._debuglog("Creating new Session")
        self._session = requests.Session()
        self._session.verify = False

        api_path = "%s/auth.cgi?api=SYNO.API.Auth&version=2" % (self.base_url,)

        login_path = "method=login&%s" % (self._encode_credentials())

        url = "%s&%s&session=Core&format=cookie" % (api_path, login_path)
        result = self._execute_get_url(url, False)

        # Parse result if valid
        if result:
            self.access_token = result["data"]["sid"]
            self._debuglog(
                "Authentication Succesfull, token: " + str(self.access_token)
            )
            return True

        self.access_token = None
        self._debuglog("Authentication Failed")
        return False

    def _get_url(self, url, retry_on_error=True):
        """Function to handle sessions for a GET request."""
        # Check if we failed to request the url or need to login
        if self.access_token is None or self._session is None or self._session_error:
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

    def _execute_get_url(self, request_url, append_sid=True):
        """Function to execute and handle a GET request."""
        # Prepare Request
        self._debuglog("Requesting URL: '" + request_url + "'")
        if append_sid:
            self._debuglog(
                "Appending access_token (SID: " + self.access_token + ") to url"
            )
            request_url = "%s&_sid=%s" % (request_url, self.access_token)

        # Execute Request
        try:
            resp = self._session.get(request_url)
            self._debuglog("Request executed: " + str(resp.status_code))
            if resp.status_code == 200:
                # We got a response
                json_data = json.loads(resp.text)

                if json_data["success"]:
                    self._debuglog("Succesfull returning data")
                    self._debuglog(str(json_data))
                    return json_data

                if json_data["error"]["code"] in {105, 106, 107, 119}:
                    self._debuglog("Session error: " + str(json_data["error"]["code"]))
                    self._session_error = True
                else:
                    self._debuglog("Failed: " + resp.text)
            # We got a 404 or 401
            return None
        except:  # pylint: disable=bare-except
            return None

    def update(self, with_information=False):
        """Updates the various instanced modules."""
        if self._information and with_information:
            api = "SYNO.DSM.Info"
            version = 1
            if self._dsm_version >= 6:
                version = 2
            url = "%s/entry.cgi?api=%s&version=%s&method=getinfo" % (
                self.base_url,
                api,
                version,
            )
            self._information.update(self._get_url(url))

        if self._utilisation:
            api = "SYNO.Core.System.Utilization"
            url = "%s/entry.cgi?api=%s&version=1&method=get&_sid=%s" % (
                self.base_url,
                api,
                self.access_token,
            )
            self._utilisation.update(self._get_url(url))

        if self._storage:
            if self._dsm_version != 5:
                api = "SYNO.Storage.CGI.Storage"
                url = "%s/entry.cgi?api=%s&version=1&method=load_info&_sid=%s" % (
                    self.base_url,
                    api,
                    self.access_token,
                )
                self._storage.update(self._get_url(url))
            else:
                url = "%s?action=load_info&_sid=%s" % (
                    self.storage_url,
                    self.access_token,
                )
                output = self._get_url(url)["data"]
                self._storage.update(output)

    @property
    def information(self):
        """Getter for various Information variables."""
        if self._information is None:
            api = "SYNO.DSM.Info"
            version = 1
            if self._dsm_version >= 6:
                version = 2
            url = "%s/entry.cgi?api=%s&version=%s&method=getinfo" % (
                self.base_url,
                api,
                version,
            )
            self._information = SynoDSMInformation(self._get_url(url))
        return self._information

    @property
    def utilisation(self):
        """Getter for various Utilisation variables."""
        if self._utilisation is None:
            api = "SYNO.Core.System.Utilization"
            url = "%s/entry.cgi?api=%s&version=1&method=get" % (self.base_url, api)
            self._utilisation = SynoCoreUtilization(self._get_url(url))
        return self._utilisation

    @property
    def storage(self):
        """Getter for various Storage variables."""
        if self._storage is None:
            if self._dsm_version != 5:
                api = "SYNO.Storage.CGI.Storage"
                url = "%s/entry.cgi?api=%s&version=1&method=load_info" % (
                    self.base_url,
                    api,
                )
            else:
                url = "%s?action=load_info" % self.storage_url

            output = self._get_url(url)
            if self._dsm_version == 5:
                output["data"] = output
            self._storage = SynoStorage(output)

        return self._storage
