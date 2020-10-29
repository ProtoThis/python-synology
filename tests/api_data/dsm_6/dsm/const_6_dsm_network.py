"""DSM 6 SYNO.DSM.Network data."""

DSM_6_DSM_NETWORK_1LAN = {
    "data": {
        "dns": ["192.168.0.35"],
        "gateway": "192.168.0.254",
        "hostname": "NAS_[NAME]",
        "interfaces": [
            {
                "id": "eth0",
                "ip": [{"address": "192.168.0.35", "netmask": "255.255.255.0"}],
                "ipv6": [
                    {
                        "address": "2a01:e35:2434:d420:211:32ff:fea6:ca59",
                        "prefix_length": 64,
                        "scope": "global",
                    },
                    {
                        "address": "fe80::211:32ff:fea6:ca59",
                        "prefix_length": 64,
                        "scope": "link",
                    },
                ],
                "mac": "00-11-32-XX-XX-59",
                "type": "lan",
            },
            {
                "id": "eth1",
                "ip": [{"address": "169.254.158.209", "netmask": "255.255.0.0"}],
                "mac": "00-11-32-XX-XX-5A",
                "type": "lan",
            },
        ],
        "workgroup": "WORKGROUP",
    },
    "success": True,
}

DSM_6_DSM_NETWORK_2LAN_1PPPOE = {
    "data": {
        "dns": ["192.168.0.35"],
        "gateway": "192.168.0.254",
        "hostname": "NAS_[NAME]",
        "interfaces": [
            {
                "id": "eth0",
                "ip": [{"address": "192.168.5.10", "netmask": "255.255.255.0"}],
                "ipv6": [
                    {
                        "address": "2001:b211:317c:147e:211:32ff:fe5d:fd11",
                        "prefix_length": 64,
                        "scope": "global",
                    },
                    {
                        "address": "fe80::211:32ff:fe5d:fd11",
                        "prefix_length": 64,
                        "scope": "link",
                    },
                ],
                "mac": "00-11-32-XX-XX-11",
                "type": "lan",
            },
            {
                "id": "eth1",
                "ip": [{"address": "192.168.1.100", "netmask": "255.255.255.0"}],
                "ipv6": [
                    {
                        "address": "2001:b011:300c:176c:211:11ff:fe5d:fd12",
                        "prefix_length": 64,
                        "scope": "global",
                    },
                    {
                        "address": "fe80::211:31ff:ff5d:fd12",
                        "prefix_length": 64,
                        "scope": "link",
                    },
                ],
                "mac": "00-11-32-XX-XX-12",
                "type": "lan",
            },
            {
                "id": "ppp0",
                "ip": [{"address": "114.45.2.158", "netmask": "255.255.255.255"}],
                "type": "pppoe",
            },
        ],
        "workgroup": "WORKGROUP",
    },
    "success": True,
}
