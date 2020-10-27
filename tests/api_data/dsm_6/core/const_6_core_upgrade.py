"""DSM 6 SYNO.Core.Upgrade data."""

DSM_6_CORE_UPGRADE_FALSE = {"data": {"update": {"available": False}}, "success": True}
DSM_6_CORE_UPGRADE_TRUE = {
    "data": {
        "update": {
            "available": True,
            "reboot": "now",
            "restart": "some",
            "type": "nano",
            "version": "DSM 6.2.3-25426 Update 2",
            "version_details": {
                "buildnumber": 25426,
                "major": 6,
                "micro": 3,
                "minor": 2,
                "nano": 2,
                "os_name": "DSM",
            },
        }
    },
    "success": True,
}
