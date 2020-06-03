"""DSM 6 SYNO.SurveillanceStation.Camera data."""

DSM_6_SURVEILLANCE_STATION_CAMERA_LIST = {
    "data": {
        "cameras": [
            {
                "DINum": 0,
                "DONum": 0,
                "audioCodec": 6,
                "channel": "1",
                "dsId": 0,
                "enableLowProfile": True,
                "enableRecordingKeepDays": True,
                "enableRecordingKeepSize": False,
                "fov": "",
                "highProfileStreamNo": 1,
                "id": 1,
                "idOnRecServer": 0,
                "ip": "192.168.1.10",
                "lowProfileStreamNo": 1,
                "mediumProfileStreamNo": 1,
                "model": "Define",
                "newName": "Camera1",
                "port": 554,
                "postRecordTime": 5,
                "preRecordTime": 5,
                "recordTime": 30,
                "recordingKeepDays": 30,
                "recordingKeepSize": "10",
                "status": 1,
                "stream1": {
                    "bitrateCtrl": 0,
                    "constantBitrate": "1000",
                    "fps": 0,
                    "quality": "",
                    "resolution": "1920x1080",
                },
                "tvStandard": 0,
                "vendor": "User",
                "videoCodec": 3,
                "videoMode": "",
            }
        ]
    },
    "success": True,
}

DSM_6_SURVEILLANCE_STATION_CAMERA_EVENT_MOTION_ENUM = {
    "data": {
        "DVAParam": None,
        "MDParam": {
            "camRoi": {"channel": "", "type": 0},
            "enhanceMDWithPD": {"value": False},
            "history": {
                "camCap": False,
                "maxValue": 99,
                "minValue": 1,
                "ssCap": False,
                "value": 90,
            },
            "keep": True,
            "mode": 0,
            "objectSize": {
                "camCap": False,
                "maxValue": 99,
                "minValue": 1,
                "ssCap": False,
                "value": 50,
            },
            "percentage": {
                "camCap": False,
                "maxValue": 99,
                "minValue": 1,
                "ssCap": False,
                "value": 50,
            },
            "region": "000000000000000000000000000000000000000001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100111111111111111111111111111111111111110011111111111111111111111111111111111111001111111111111111111111111111111111111100000000000000000000000000000000000000000",
            "relatedEvents": [],
            "sensitivity": {
                "camCap": False,
                "maxValue": 99,
                "minValue": 1,
                "ssCap": True,
                "value": 90,
            },
            "shortLiveSecond": {"camCap": False, "ssCap": True, "value": 0},
            "source": 1,
            "threshold": {
                "camCap": False,
                "maxValue": 99,
                "minValue": 1,
                "ssCap": True,
                "value": 10,
            },
        },
        "PDParam": {
            "keep": True,
            "sensitivity": {"cap": False, "maxValue": 0, "minValue": 0, "value": 0},
            "source": -1,
            "triggerMotion": False,
        },
    },
    "success": True,
}

DSM_6_SURVEILLANCE_STATION_CAMERA_GET_LIVE_VIEW_PATH = {
    "data": [
        {
            "id": 1,
            "mjpegHttpPath": 'http://192.168.1.100:5000/webapi/entry.cgi?api=SYNO.SurveillanceStation.Stream.VideoStreaming&version=1&method=Stream&format=mjpeg&cameraId=1&StmKey="stmkey1234567890"',
            "multicstPath": "rtsp://syno:stmkey1234567890@192.168.1.100:554/Sms=1.multicast",
            "mxpegHttpPath": 'http://192.168.1.100:5000/webapi/entry.cgi?api=SYNO.SurveillanceStation.Stream.VideoStreaming&version=1&method=Stream&format=mxpeg&cameraId=1&StmKey="stmkey1234567890"',
            "rtspOverHttpPath": "rtsp://192.168.1.100:5000/webman/3rdparty/SurveillanceStation/cgi/rtsp.cgi?Sms=1.unicast&DsId=0&StmKey=stmkey1234567890",
            "rtspPath": "rtsp://syno:stmkey1234567890@192.168.1.100:554/Sms=1.unicast",
        }
    ],
    "success": True,
}
