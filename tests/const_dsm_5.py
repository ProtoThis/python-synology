# -*- coding: utf-8 -*-
"""Test constants for DSM 5 NAS."""
from .const import SERIAL, SID, UNIQUE_KEY  # pylint: disable=unused-import

# DSM 5 RAW DATA
DSM_5_LOGIN = {
    {'data': {'sid': SID}, 'success': True}
DSM_5_LOGIN = {'data': {'sid': SID}, 'success': True}

DSM_5_INFORMATION = {
    # Request failed
}

DSM_5_UTILIZATION = {
    {
        "data": {
            "cpu": {
                "15min_load": 53,
                "1min_load": 57,
                "5min_load": 56,
                "device": "System",
                "other_load": 63,
                "system_load": 10,
                "user_load": 27
            },
            "disk": {
                "disk": [
                    {
                        "device": "sda",
                        "display_name": "Disk 1",
                        "read_access": 21,
                        "read_byte": 645529,
                        "type": "internal",
                        "utilization": 46,
                        "write_access": 4,
                        "write_byte": 86220
                    },
                    {
                        "device": "sdb",
                        "display_name": "Disk 2",
                        "read_access": 23,
                        "read_byte": 711338,
                        "type": "internal",
                        "utilization": 33,
                        "write_access": 4,
                        "write_byte": 95641
                    },
                    {
                        "device": "sdc",
                        "display_name": "Disk 3",
                        "read_access": 21,
                        "read_byte": 786841,
                        "type": "internal",
                        "utilization": 31,
                        "write_access": 5,
                        "write_byte": 99874
                    },
                    {
                        "device": "sdd",
                        "display_name": "Disk 4",
                        "read_access": 21,
                        "read_byte": 729907,
                        "type": "internal",
                        "utilization": 32,
                        "write_access": 4,
                        "write_byte": 76663
                    },
                    {
                        "device": "sdq",
                        "display_name": "USB Disk 1",
                        "read_access": 0,
                        "read_byte": 0,
                        "type": "usb",
                        "utilization": 0,
                        "write_access": 0,
                        "write_byte": 0
                    }
                ],
                "total": {
                    "device": "total",
                    "read_access": 86,
                    "read_byte": 2873615,
                    "utilization": 28,
                    "write_access": 17,
                    "write_byte": 358398
                }
            },
            "memory": {
                "avail_real": 8188,
                "avail_swap": 1933436,
                "buffer": 3700,
                "cached": 25636,
                "device": "Memory",
                "memory_size": 131072,
                "real_usage": 68,
                "si_disk": 5,
                "so_disk": 3,
                "swap_usage": 7,
                "total_real": 118464,
                "total_swap": 2097080
            },
            "network": [
                {
                    "device": "total",
                    "rx": 1680,
                    "tx": 553
                },
                {
                    "device": "eth0",
                    "rx": 1680,
                    "tx": 553
                }
            ],
            "space": {
                "lun": [],
                "total": {
                    "device": "total",
                    "read_access": 261,
                    "read_byte": 1069875,
                    "utilization": 100,
                    "write_access": 51,
                    "write_byte": 208896
                },
                "volume": [
                    {
                        "device": "md2",
                        "display_name": "volume1",
                        "read_access": 261,
                        "read_byte": 1069875,
                        "utilization": 100,
                        "write_access": 51,
                        "write_byte": 208896
                    }
                ]
            },
            "time": 1586592505
        },
        "success": True
    }

}

DSM_5_STORAGE = {
    {
        "disks": [
            {
                "container": {
                    "order": 0,
                    "str": "DS410j",
                    "supportPwrBtnDisable": False,
                    "type": "internal"
                },
                "device": "/dev/sdd",
                "disable_secera": False,
                "diskType": "SATA",
                "erase_time": 374,
                "firm": "SC60",
                "has_system": True,
                "id": "sdd",
                "is4Kn": False,
                "isSsd": False,
                "is_erasing": False,
                "longName": "Disk 4",
                "model": "ST3000VN007-2E4166      ",
                "name": "Disk 4",
                "num_id": 4,
                "order": 4,
                "portType": "normal",
                "serial": "Z73095S2",
                "size_total": "3000592982016",
                "smart_status": "safe",
                "status": "normal",
                "support": False,
                "temp": 42,
                "used_by": "volume_1",
                "vendor": "Seagate"
            },
            {
                "container": {
                    "order": 0,
                    "str": "DS410j",
                    "supportPwrBtnDisable": False,
                    "type": "internal"
                },
                "device": "/dev/sdc",
                "disable_secera": False,
                "diskType": "SATA",
                "erase_time": 410,
                "firm": "80.00A80",
                "has_system": True,
                "id": "sdc",
                "is4Kn": False,
                "isSsd": False,
                "is_erasing": False,
                "longName": "Disk 3",
                "model": "WD30EZRZ-00Z5HB0        ",
                "name": "Disk 3",
                "num_id": 3,
                "order": 3,
                "portType": "normal",
                "serial": "WD-WCC4N0TEJ4F0",
                "size_total": "3000592982016",
                "smart_status": "safe",
                "status": "normal",
                "support": False,
                "temp": 42,
                "used_by": "volume_1",
                "vendor": "WDC     "
            },
            {
                "container": {
                    "order": 0,
                    "str": "DS410j",
                    "supportPwrBtnDisable": False,
                    "type": "internal"
                },
                "device": "/dev/sdb",
                "disable_secera": False,
                "diskType": "SATA",
                "erase_time": 408,
                "firm": "82.00A82",
                "has_system": True,
                "id": "sdb",
                "is4Kn": False,
                "isSsd": False,
                "is_erasing": False,
                "longName": "Disk 2",
                "model": "WD30EFRX-68EUZN0        ",
                "name": "Disk 2",
                "num_id": 2,
                "order": 2,
                "portType": "normal",
                "serial": "WD-WCC4N6LSVCVX",
                "size_total": "3000592982016",
                "smart_status": "safe",
                "status": "normal",
                "support": False,
                "temp": 43,
                "used_by": "volume_1",
                "vendor": "WDC     "
            },
            {
                "container": {
                    "order": 0,
                    "str": "DS410j",
                    "supportPwrBtnDisable": False,
                    "type": "internal"
                },
                "device": "/dev/sda",
                "disable_secera": False,
                "diskType": "SATA",
                "erase_time": 0,
                "firm": "82.00A82",
                "has_system": True,
                "id": "sda",
                "is4Kn": False,
                "isSsd": False,
                "is_erasing": False,
                "longName": "Disk 1",
                "model": "WD30EFRX-68N32N0        ",
                "name": "Disk 1",
                "num_id": 1,
                "order": 1,
                "portType": "normal",
                "serial": "WD-WCC7K5YA5H40",
                "size_total": "3000592982016",
                "smart_status": "90%",
                "status": "normal",
                "support": False,
                "temp": 44,
                "used_by": "volume_1",
                "vendor": "WDC     "
            }
        ],
        "env": {
            "batchtask": {
                "max_task": 64,
                "remain_task": 64
            },
            "bay_number": "4",
            "ebox": [],
            "fs_acting": False,
            "is_space_actioning": False,
            "isns": {
                "address": "",
                "enabled": False
            },
            "isns_server": "",
            "max_fs_bytes": "17592181850112",
            "max_fs_bytes_high_end": "219902325555200",
            "model_name": "DS410j",
            "ram_enough_for_fs_high_end": False,
            "ram_size": 0,
            "ram_size_required": 32,
            "settingSwap": False,
            "showpooltab": False,
            "status": {
                "system_crashed": False,
                "system_need_repair": False
            },
            "support": {
                "ebox": False,
                "raid_cross": False,
                "sysdef": True
            },
            "unique_key": UNIQUE_KEY
        },
        "hotSpares": [],
        "iscsiLuns": [
            {
                "can_do": {
                    "data_scrubbing": True,
                    "delete": True,
                    "expand_by_disk": 1,
                    "migrate": {
                        "to_raid5+spare": "1-1",
                        "to_raid6": 1
                    }
                },
                "id": "iscsilun_LUN-1",
                "is_actioning": False,
                "iscsi_lun": {
                    "blkNum": "19614744",
                    "device_type": "file",
                    "lid": 1,
                    "location": "volume_1",
                    "mapped_targets": [
                        1
                    ],
                    "name": "LUN-1",
                    "restored_time": "0",
                    "rootpath": "/volume1",
                    "size": "10737418240",
                    "thin_provision": False,
                    "uuid": "fcf3a450-681c-06cb-fbb9-0400bdbe0780",
                    "vaai_extent_size": "0",
                    "vaai_support": False
                },
                "num_id": 1,
                "progress": {
                    "percent": "-1",
                    "step": "none"
                },
                "status": "normal"
            }
        ],
        "iscsiTargets": [
            {
                "auth": {
                    "mutual_username": "",
                    "type": "none",
                    "username": ""
                },
                "data_chksum": 0,
                "enabled": True,
                "hdr_chksum": 0,
                "iqn": "iqn.2000-01.com.synology:DiskStation.name",
                "mapped_logical_unit_number": [
                    0
                ],
                "mapped_luns": [
                    1
                ],
                "masking": [
                    {
                        "iqn": "iqn.2000-01.com.synology:default.acl",
                        "permission": "rw"
                    }
                ],
                "multi_sessions": False,
                "name": "Target-1",
                "num_id": 1,
                "recv_seg_bytes": 262144,
                "remote": [],
                "send_seg_bytes": 4096,
                "status": "online",
                "tid": 1
            }
        ],
        "ports": [],
        "storagePools": [],
        "success": True,
        "volumes": [
            {
                "can_do": {
                    "data_scrubbing": True,
                    "delete": True,
                    "expand_by_disk": 1,
                    "migrate": {
                        "to_raid5+spare": "1-1",
                        "to_raid6": 1
                    }
                },
                "container": "internal",
                "device_type": "raid_5",
                "disk_failure_number": 0,
                "disks": [
                    "sda",
                    "sdb",
                    "sdc",
                    "sdd"
                ],
                "eppool_used": "10042748928",
                "fs_type": "ext3",
                "id": "volume_1",
                "is_acting": False,
                "is_actioning": False,
                "is_inode_full": False,
                "is_writable": True,
                "max_fs_size": "17592181850112",
                "maximal_disk_size": "0",
                "minimal_disk_size": "2995767869440",
                "num_id": 1,
                "pool_path": "",
                "progress": {
                    "percent": "-1",
                    "step": "none"
                },
                "size": {
                    "free_inode": "547237217",
                    "total": "8846249701376",
                    "total_device": "8987275100160",
                    "total_inode": "548544512",
                    "used": "5719795761152"
                },
                "space_path": "/dev/md2",
                "spares": [],
                "ssd_trim": {
                    "support": "not support"
                },
                "status": "normal",
                "suggestions": [],
                "timebackup": True,
                "used_by_gluster": False,
                "vol_path": "/volume1",
                "vspace_can_do": {
                    "drbd": {
                        "resize": {
                            "can_do": False,
                            "errCode": 53504,
                            "stopService": False
                        }
                    },
                    "flashcache": {
                        "apply": {
                            "can_do": False,
                            "errCode": 53504,
                            "stopService": False
                        },
                        "remove": {
                            "can_do": False,
                            "errCode": 53504,
                            "stopService": False
                        },
                        "resize": {
                            "can_do": False,
                            "errCode": 53504,
                            "stopService": False
                        }
                    },
                    "snapshot": {
                        "resize": {
                            "can_do": True,
                            "errCode": 0,
                            "stopService": False
                        }
                    }
                }
            }
        ]
    }

}
