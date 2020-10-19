"""DSM 6 datas."""
from .const_6_api_info import DSM_6_API_INFO
from .const_6_api_auth import (
    DSM_6_AUTH_LOGIN,
    DSM_6_AUTH_LOGIN_2SA,
    DSM_6_AUTH_LOGIN_2SA_OTP,
)
from .core.const_6_core_utilization import (
    DSM_6_CORE_UTILIZATION,
    DSM_6_CORE_UTILIZATION_ERROR_1055,
)
from .core.const_6_core_security import (
    DSM_6_CORE_SECURITY,
    DSM_6_CORE_SECURITY_UPDATE_OUTOFDATE,
)
from .core.const_6_core_system import (
    DSM_6_CORE_SYSTEM_DS918_PLUS,
    DSM_6_CORE_SYSTEM_DS218_PLAY,
)
from .core.const_6_core_upgrade import DSM_6_CORE_UPGRADE
from .download_station.const_6_download_station_info import (
    DSM_6_DOWNLOAD_STATION_INFO_INFO,
    DSM_6_DOWNLOAD_STATION_INFO_CONFIG,
)
from .download_station.const_6_download_station_stat import (
    DSM_6_DOWNLOAD_STATION_STAT_INFO,
)
from .download_station.const_6_download_station_task import (
    DSM_6_DOWNLOAD_STATION_TASK_LIST,
)
from .dsm.const_6_dsm_info import DSM_6_DSM_INFORMATION
from .dsm.const_6_dsm_network import DSM_6_DSM_NETWORK
from .storage.const_6_storage_storage import (
    DSM_6_STORAGE_STORAGE_DS213_PLUS_SHR1_2DISKS_2VOLS,
    DSM_6_STORAGE_STORAGE_DS918_PLUS_RAID5_3DISKS_1VOL,
    DSM_6_STORAGE_STORAGE_DS1515_PLUS_SHR2_10DISKS_1VOL_WITH_EXPANSION,
    DSM_6_STORAGE_STORAGE_DS1819_PLUS_SHR2_8DISKS_1VOL,
)
from .surveillance_station.const_6_api_info import (
    DSM_6_API_INFO as DSM_6_API_INFO_SURVEILLANCE_STATION,
)
from .surveillance_station.const_6_surveillance_station_camera import (
    DSM_6_SURVEILLANCE_STATION_CAMERA_LIST,
    DSM_6_SURVEILLANCE_STATION_CAMERA_GET_LIVE_VIEW_PATH,
    DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MOTION_ENUM,
    DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MD_PARAM_SAVE,
)
from .core.const_6_core_share import DSM_6_CORE_SHARE
from .surveillance_station.const_6_surveillance_station_home_mode import (
    DSM_6_SURVEILLANCE_STATION_HOME_MODE_GET_INFO,
    DSM_6_SURVEILLANCE_STATION_HOME_MODE_SWITCH,
)
