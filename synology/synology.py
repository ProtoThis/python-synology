# -*- coding:utf-8 -*-
import requests
from requests.compat import json

# Define Static Classes
class SynoFormatHelper(object):
    @staticmethod
    def bytesToReadable(num):
        if num < 512:
                return "0 Kb"
        elif num < 1024:
                return "1 Kb"
            
        for unit in ['','Kb','Mb','Gb','Tb','Pb','Eb','Zb']:
            if abs(num) < 1024.0:
                return "%3.1f%s" % (num, unit)
            num /= 1024.0
        return "%.1f%s" % (num, 'Yb')

# Define Classes
class SynoUtilization(object):
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)
        
    def update(self, raw_input):
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def cpu_other_load(self):
        if self._data is not None:
            return self._data["cpu"]["other_load"]

    @property
    def cpu_user_load(self):
        if self._data is not None:
            return self._data["cpu"]["user_load"]

    @property
    def cpu_system_load(self):
        if self._data is not None:
            return self._data["cpu"]["system_load"]

    @property
    def cpu_total_load(self):
        return self.cpu_system_load + self.cpu_user_load + self.cpu_other_load

    @property
    def cpu_1min_load(self):
        if self._data is not None:
            return self._data["cpu"]["1min_load"]

    @property
    def cpu_5min_load(self):
        if self._data is not None:
            return self._data["cpu"]["5min_load"]

    @property
    def cpu_15min_load(self):
        if self._data is not None:
            return self._data["cpu"]["15min_load"]

    @property
    def memory_real_usage(self):
        if self._data is not None:
            return str(self._data["memory"]["real_usage"]) + "%"

    @property
    def memory_size(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["memory_size"]) * 1024)

    @property
    def memory_available_swap(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["avail_swap"]) * 1024)

    @property
    def memory_cached(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["cached"]) * 1024)

    @property
    def memory_available_real(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["avail_real"]) * 1024)

    @property
    def memory_total_real(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["total_real"]) * 1024)

    @property
    def memory_total_swap(self):
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytesToReadable(int(self._data["memory"]["total_swap"]) * 1024)

    @property
    def network_up(self):
        #TODO: Check if we are looking at the total network interface (not eth0 or eth1 for example)
        if self._data is not None:
            return SynoFormatHelper.bytesToReadable(int(self._data["network"][0]["tx"]))

    @property
    def network_down(self):
        #TODO: Check if we are looking at the total network interface (not eth0 or eth1 for example)
        if self._data is not None:
            return SynoFormatHelper.bytesToReadable(int(self._data["network"][0]["rx"]))


class SynoStorage(object):
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)
        
    def update(self, raw_input):
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def volumes(self):
        if self._data is not None:
            volumes = []
            for volume in self._data["volumes"]:
                volumes.append(volume["id"])
            return volumes

    @property
    def disks(self):
        if self._data is not None:
            disks = []
            for disk in self._data["disks"]:
                disks.append(disk["id"])
            return disks

    def _get_volume(self, volume_id):
        if self._data is not None:
            for volume in self._data["volumes"]:
                if volume["id"] == volume_id:
                    return volume

    def volume_status(self, volume):
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["status"]

    def volume_device_type(self, volume):
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["device_type"]

    def volume_size_total(self, volume):
        volume = self._get_volume(volume)
        if volume is not None:
            return SynoFormatHelper.bytesToReadable(int(volume["size"]["total"]))

    def volume_size_used(self, volume):
        volume = self._get_volume(volume)
        if volume is not None:
            return SynoFormatHelper.bytesToReadable(int(volume["size"]["used"]))

class SynologyApi(object):
    def __init__(self, ip, port, username, password):
        # Store Variables
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        # Class Variables
        self.access_token = None
        self._utilisation = None
        self._storage = None

        # Build Variables
        self.base_url = "http://%s:%s" % (self.ip, self.port)

        # Login to get our access token
        self._login()

    def _login(self):
        # Build login url and request
        url = "%s/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=%s&passwd=%s&session=Core&format=cookie" % (self.base_url, self.username, self.password)
        result = self._getUrl(url)

        # Parse Result if valid
        if result is not None:
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
                        return self._getUrl(url, False)
                    else:
                        return None
        except:
            return None

    @property
    def Utilisation(self):
        if self._utilisation is None:
            url = "%s/webapi/entry.cgi?api=SYNO.Core.System.Utilization&version=1&method=get&_sid=%s" % (self.base_url, self.access_token)
            self._utilisation = SynoUtilization(self._getUrl(url))
            
        return self._utilisation

    @property
    def Storage(self):
        if self._storage is None:
            url = "%s/webapi/entry.cgi?api=SYNO.Storage.CGI.Storage&version=1&method=load_info&_sid=%s" % (self.base_url, self.access_token)
            self._storage = SynoStorage(self._getUrl(url))
            
        return self._storage
