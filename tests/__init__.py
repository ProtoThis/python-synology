"""Library tests."""
from json import JSONDecodeError
from urllib.parse import urlencode

from requests.exceptions import ConnectionError as ConnError
from requests.exceptions import RequestException
from requests.exceptions import SSLError

from .api_data.dsm_5 import DSM_5_API_INFO
from .api_data.dsm_5 import DSM_5_AUTH_LOGIN
from .api_data.dsm_5 import DSM_5_AUTH_LOGIN_2SA
from .api_data.dsm_5 import DSM_5_AUTH_LOGIN_2SA_OTP
from .api_data.dsm_5 import DSM_5_CORE_UTILIZATION
from .api_data.dsm_5 import DSM_5_DSM_INFORMATION
from .api_data.dsm_5 import DSM_5_DSM_NETWORK
from .api_data.dsm_5 import DSM_5_STORAGE_STORAGE_DS410J_RAID5_4DISKS_1VOL
from .api_data.dsm_6 import DSM_6_API_INFO
from .api_data.dsm_6 import DSM_6_API_INFO_SURVEILLANCE_STATION
from .api_data.dsm_6 import DSM_6_AUTH_LOGIN
from .api_data.dsm_6 import DSM_6_AUTH_LOGIN_2SA
from .api_data.dsm_6 import DSM_6_AUTH_LOGIN_2SA_OTP
from .api_data.dsm_6 import DSM_6_CORE_SECURITY
from .api_data.dsm_6 import DSM_6_CORE_SECURITY_UPDATE_OUTOFDATE
from .api_data.dsm_6 import DSM_6_CORE_SHARE
from .api_data.dsm_6 import DSM_6_CORE_SYSTEM_DS918_PLUS
from .api_data.dsm_6 import DSM_6_CORE_UPGRADE
from .api_data.dsm_6 import DSM_6_CORE_UTILIZATION
from .api_data.dsm_6 import DSM_6_CORE_UTILIZATION_ERROR_1055
from .api_data.dsm_6 import DSM_6_DOWNLOAD_STATION_INFO_CONFIG
from .api_data.dsm_6 import DSM_6_DOWNLOAD_STATION_INFO_INFO
from .api_data.dsm_6 import DSM_6_DOWNLOAD_STATION_STAT_INFO
from .api_data.dsm_6 import DSM_6_DOWNLOAD_STATION_TASK_LIST
from .api_data.dsm_6 import DSM_6_DSM_INFORMATION
from .api_data.dsm_6 import DSM_6_DSM_NETWORK
from .api_data.dsm_6 import (
    DSM_6_STORAGE_STORAGE_DS1515_PLUS_SHR2_10DISKS_1VOL_WITH_EXPANSION,
)
from .api_data.dsm_6 import DSM_6_STORAGE_STORAGE_DS1819_PLUS_SHR2_8DISKS_1VOL
from .api_data.dsm_6 import DSM_6_STORAGE_STORAGE_DS213_PLUS_SHR1_2DISKS_2VOLS
from .api_data.dsm_6 import DSM_6_STORAGE_STORAGE_DS918_PLUS_RAID5_3DISKS_1VOL
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MD_PARAM_SAVE
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MOTION_ENUM
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_CAMERA_GET_LIVE_VIEW_PATH
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_CAMERA_LIST
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_HOME_MODE_GET_INFO
from .api_data.dsm_6 import DSM_6_SURVEILLANCE_STATION_HOME_MODE_SWITCH
from .const import DEVICE_TOKEN
from .const import ERROR_AUTH_INVALID_CREDENTIALS
from .const import ERROR_AUTH_MAX_TRIES
from .const import ERROR_AUTH_OTP_AUTHENTICATE_FAILED
from .const import ERROR_INSUFFICIENT_USER_PRIVILEGE
from synology_dsm import SynologyDSM
from synology_dsm.api.core.security import SynoCoreSecurity
from synology_dsm.api.core.share import SynoCoreShare
from synology_dsm.api.core.system import SynoCoreSystem
from synology_dsm.api.core.upgrade import SynoCoreUpgrade
from synology_dsm.api.core.utilization import SynoCoreUtilization
from synology_dsm.api.download_station import SynoDownloadStation
from synology_dsm.api.dsm.information import SynoDSMInformation
from synology_dsm.api.dsm.network import SynoDSMNetwork
from synology_dsm.api.storage.storage import SynoStorage
from synology_dsm.api.surveillance_station import SynoSurveillanceStation
from synology_dsm.const import API_AUTH
from synology_dsm.const import API_INFO
from synology_dsm.exceptions import SynologyDSMRequestException

API_SWITCHER = {
    5: {
        "API_INFO": DSM_5_API_INFO,
        "AUTH_LOGIN": DSM_5_AUTH_LOGIN,
        "AUTH_LOGIN_2SA": DSM_5_AUTH_LOGIN_2SA,
        "AUTH_LOGIN_2SA_OTP": DSM_5_AUTH_LOGIN_2SA_OTP,
        "DSM_INFORMATION": DSM_5_DSM_INFORMATION,
        "DSM_NETWORK": DSM_5_DSM_NETWORK,
        "CORE_UTILIZATION": DSM_5_CORE_UTILIZATION,
        "STORAGE_STORAGE": {
            "RAID": DSM_5_STORAGE_STORAGE_DS410J_RAID5_4DISKS_1VOL,
        },
    },
    6: {
        "API_INFO": DSM_6_API_INFO,
        "AUTH_LOGIN": DSM_6_AUTH_LOGIN,
        "AUTH_LOGIN_2SA": DSM_6_AUTH_LOGIN_2SA,
        "AUTH_LOGIN_2SA_OTP": DSM_6_AUTH_LOGIN_2SA_OTP,
        "DSM_INFORMATION": DSM_6_DSM_INFORMATION,
        "DSM_NETWORK": DSM_6_DSM_NETWORK,
        "CORE_SECURITY": DSM_6_CORE_SECURITY,
        "CORE_SHARE": DSM_6_CORE_SHARE,
        "CORE_SYSTEM": DSM_6_CORE_SYSTEM_DS918_PLUS,
        "CORE_UTILIZATION": DSM_6_CORE_UTILIZATION,
        "CORE_UPGRADE": DSM_6_CORE_UPGRADE,
        "STORAGE_STORAGE": {
            "RAID": DSM_6_STORAGE_STORAGE_DS918_PLUS_RAID5_3DISKS_1VOL,
            "SHR1": DSM_6_STORAGE_STORAGE_DS213_PLUS_SHR1_2DISKS_2VOLS,
            "SHR2": DSM_6_STORAGE_STORAGE_DS1819_PLUS_SHR2_8DISKS_1VOL,
            "SHR2_EXPANSION": DSM_6_STORAGE_STORAGE_DS1515_PLUS_SHR2_10DISKS_1VOL_WITH_EXPANSION,  # noqa: B950
        },
    },
}


VALID_HOST = "nas.mywebsite.me"
VALID_PORT = "443"
VALID_HTTPS = True
VALID_VERIFY_SSL = True
VALID_USER = "valid_user"
VALID_USER_2SA = "valid_user_2sa"
VALID_PASSWORD = "valid_password"
VALID_OTP = "123456"

USER_MAX_TRY = "user_max"


class SynologyDSMMock(SynologyDSM):
    """Mocked SynologyDSM."""

    API_URI = "api="

    def __init__(
        self,
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        verify_ssl=False,
        timeout=None,
        device_token=None,
        debugmode=False,
    ):
        """Constructor method."""
        SynologyDSM.__init__(
            self,
            dsm_ip,
            dsm_port,
            username,
            password,
            use_https,
            verify_ssl,
            timeout,
            device_token,
            debugmode,
        )

        self.verify_ssl = verify_ssl
        self.dsm_version = 6  # 5 or 6
        self.disks_redundancy = "RAID"  # RAID or SHR[number][_EXPANSION]
        self.error = False
        self.with_surveillance = False

    def _execute_request(self, method, url, params, **kwargs):
        url += urlencode(params or {})

        if "no_internet" in url:
            raise SynologyDSMRequestException(
                ConnError(
                    "<urllib3.connection.VerifiedHTTPSConnection object at "
                    "0x106c1f250>: Failed to establish a new connection: "
                    "[Errno 8] nodename nor servname provided, or not known"
                )
            )

        if VALID_HOST not in url:
            raise SynologyDSMRequestException(
                ConnError(
                    "<urllib3.connection.HTTPConnection object at 0x10d6f8090>:"
                    " Failed to establish a new connection: [Errno 8] nodename "
                    "nor servname provided, or not known"
                )
            )

        if VALID_PORT not in url and "https" not in url:
            raise SynologyDSMRequestException(
                JSONDecodeError("Expecting value", "<html>document</html>", 0)
            )

        if VALID_PORT not in url:
            raise SynologyDSMRequestException(
                SSLError(
                    "[SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1076)"
                )
            )

        if "https" not in url:
            raise SynologyDSMRequestException(RequestException("Bad request"))

        if not self.verify_ssl:
            raise SynologyDSMRequestException(
                SSLError(f"hostname '192.168.0.35' doesn't match '{VALID_HOST}'")
            )

        if API_INFO in url:
            if self.with_surveillance:
                return DSM_6_API_INFO_SURVEILLANCE_STATION
            return API_SWITCHER[self.dsm_version]["API_INFO"]

        if API_AUTH in url:
            if VALID_USER_2SA in url and VALID_PASSWORD in url:
                if "otp_code" not in url and "device_id" not in url:
                    return API_SWITCHER[self.dsm_version]["AUTH_LOGIN_2SA"]

                if "device_id" in url and DEVICE_TOKEN in url:
                    return API_SWITCHER[self.dsm_version]["AUTH_LOGIN"]

                if "otp_code" in url:
                    if VALID_OTP in url:
                        return API_SWITCHER[self.dsm_version]["AUTH_LOGIN_2SA_OTP"]
                    return ERROR_AUTH_OTP_AUTHENTICATE_FAILED

            if VALID_USER in url and VALID_PASSWORD in url:
                return API_SWITCHER[self.dsm_version]["AUTH_LOGIN"]

            if USER_MAX_TRY in url:
                return ERROR_AUTH_MAX_TRIES

            return ERROR_AUTH_INVALID_CREDENTIALS

        if self.API_URI in url:
            if not self._session_id:
                return ERROR_INSUFFICIENT_USER_PRIVILEGE

            if SynoCoreSecurity.API_KEY in url:
                if self.error:
                    return DSM_6_CORE_SECURITY_UPDATE_OUTOFDATE
                return API_SWITCHER[self.dsm_version]["CORE_SECURITY"]

            if SynoCoreShare.API_KEY in url:
                return API_SWITCHER[self.dsm_version]["CORE_SHARE"]

            if SynoCoreSystem.API_KEY in url:
                if SynoCoreUtilization.API_KEY in url:
                    if self.error:
                        return DSM_6_CORE_UTILIZATION_ERROR_1055
                    return API_SWITCHER[self.dsm_version]["CORE_UTILIZATION"]
                return API_SWITCHER[self.dsm_version]["CORE_SYSTEM"]

            if SynoCoreUpgrade.API_KEY in url:
                return API_SWITCHER[self.dsm_version]["CORE_UPGRADE"]

            if SynoDSMInformation.API_KEY in url:
                return API_SWITCHER[self.dsm_version]["DSM_INFORMATION"]

            if SynoDSMNetwork.API_KEY in url:
                return API_SWITCHER[self.dsm_version]["DSM_NETWORK"]

            if SynoDownloadStation.INFO_API_KEY in url:
                if "GetInfo" in url:
                    return DSM_6_DOWNLOAD_STATION_INFO_INFO
                if "GetConfig" in url:
                    return DSM_6_DOWNLOAD_STATION_INFO_CONFIG
            if SynoDownloadStation.STAT_API_KEY in url:
                if "GetInfo" in url:
                    return DSM_6_DOWNLOAD_STATION_STAT_INFO
            if SynoDownloadStation.TASK_API_KEY in url:
                if "List" in url:
                    return DSM_6_DOWNLOAD_STATION_TASK_LIST

            if SynoStorage.API_KEY in url:
                return API_SWITCHER[self.dsm_version]["STORAGE_STORAGE"][
                    self.disks_redundancy
                ]

            if SynoSurveillanceStation.CAMERA_API_KEY in url:
                if "GetLiveViewPath" in url:
                    return DSM_6_SURVEILLANCE_STATION_CAMERA_GET_LIVE_VIEW_PATH
                if "List" in url:
                    assert params["version"] == 7
                    return DSM_6_SURVEILLANCE_STATION_CAMERA_LIST
                if "MDParamSave" in url:
                    return DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MD_PARAM_SAVE
                if "MotionEnum" in url:
                    return DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MOTION_ENUM

            if SynoSurveillanceStation.HOME_MODE_API_KEY in url:
                if "GetInfo" in url:
                    return DSM_6_SURVEILLANCE_STATION_HOME_MODE_GET_INFO
                if "Switch" in url:
                    return DSM_6_SURVEILLANCE_STATION_HOME_MODE_SWITCH

            if (
                "SYNO.FileStation.Upload" in url
                and "upload" in url
                and "file_already_exists" in kwargs["files"]["file"]
            ):
                return {"error": {"code": 1805}, "success": False}

            if (
                "SYNO.DownloadStation2.Task" in url
                and "create" in url
                and "test_not_exists" in url
            ):
                return {"error": {"code": 408}, "success": False}

            return {"success": False}

        return None
