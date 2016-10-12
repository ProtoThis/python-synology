# -*- coding:utf-8 -*-
import requests
from requests.compat import json

# Define Static Variables


# Define Classes
class SynologyApi(object):
    def __init__(self, ip, port, username, password):
        # Store Variables
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        # Class Variables
        self.access_token = None

        # Build Variables
        self.base_url = "http://%s:%s" % (self.ip, self.port)

        # Login to get our access token
        self._login()

    def _login(self):
        # Build login url and request
        url = "%s/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=%s&passwd=%s&session=Core&format=cookie" % (self.base_url, self.username, self.password)
        result = self._getUrl(url)
        
        # Parse Result if valid
        if result != None:
            self.access_token = result["data"]["sid"]

    def _getUrl(self, url, retryOnError=True):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                json_data = json.loads(resp.text)
                if json_data["success"]:
                    return json_data
                else:
                    if retryOnError:
                        return self._getUrl(url, false)
                    else:
                        return None
        except:
            return None

