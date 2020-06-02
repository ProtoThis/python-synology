"""Synology SurveillanceStation API wrapper."""
import urllib

from .camera import SynoCamera
from .const import MOTION_DETECTION_BY_SURVEILLANCE, MOTION_DETECTION_DISABLED


class SynoSurveillanceStation(object):
    """An implementation of a Synology SurveillanceStation."""

    API_KEY = "SYNO.SurveillanceStation.*"
    CAMERA_API_KEY = "SYNO.SurveillanceStation.Camera"
    CAMERA_EVENT_API_KEY = "SYNO.SurveillanceStation.Camera.Event"
    HOME_MODE_API_KEY = "SYNO.SurveillanceStation.HomeMode"
    SNAPSHOT_API_KEY = "SYNO.SurveillanceStation.SnapShot"

    def __init__(self, dsm):
        """Initialize a Surveillance Station."""
        self._dsm = dsm
        self._cameras_by_id = {}

    def update(self):
        """Update cameras and motion settings with latest from API."""
        response = self._dsm.get(self.CAMERA_API_KEY, "list")
        for data in response["data"]["cameras"]:
            if data["id"] in self._cameras_by_id:
                self._cameras_by_id[data["id"]].update(data)
            else:
                self._cameras_by_id[data["id"]] = SynoCamera(data)

        for camera_id in self._cameras_by_id:
            self._cameras_by_id[camera_id].update_motion_detection(
                self._dsm.get(
                    self.CAMERA_EVENT_API_KEY, "MotionEnum", {"camId": camera_id}
                )["data"]
            )

        live_view_response = self._dsm.get(
            self.CAMERA_API_KEY,
            "getLiveViewPath",
            {"idList", self._cameras_by_id.keys()},
        )
        for live_view_data in live_view_response["data"]:
            self._cameras_by_id[live_view_data["id"]].live_view.update(live_view_data)

    # Camera
    def get_all_cameras(self):
        """Return a list of cameras."""
        return self._cameras_by_id.values()

    def get_camera(self, camera_id):
        """Return camera matching camera_id."""
        return self._cameras_by_id[camera_id]

    def get_camera_live_view_path(self, camera_id, video_format=None):
        """Return camera live view path matching camera_id (video_format: mjpeg_http | multicast | mxpeg_http | rtsp_http | rtsp)."""
        if video_format:
            return getattr(self._cameras_by_id[camera_id].live_view, video_format)
        return self._cameras_by_id[camera_id].live_view

    def get_camera_image(self, camera_id):
        """Return bytes of camera image for camera matching camera_id."""
        return self._dsm.get(
            self.CAMERA_API_KEY, "getSnapshot", {"cameraId": camera_id}
        )

    def enable_camera(self, camera_id):
        """Enable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._dsm.get(self.CAMERA_API_KEY, "enable", {"idList": camera_id})[
            "success"
        ]

    def disable_camera(self, camera_id):
        """Disable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._dsm.get(self.CAMERA_API_KEY, "disable", {"idList": camera_id})[
            "success"
        ]

    # Snapshot
    def capture_camera_image(self, camera_id, save=True):
        """Capture a snapshot for camera matching camera_id."""
        return self._dsm.get(
            self.SNAPSHOT_API_KEY, "takeSnapshot", {"camId": camera_id, "blSave": save},
        )

    def download_snapshot(self, snapshot_id, snapshot_size):
        """Download snapshot image binary for a givent snapshot_id (snapshot_size: SNAPSHOT_SIZE_ICON | SNAPSHOT_SIZE_FULL)."""
        return self._dsm.get(
            self.SNAPSHOT_API_KEY,
            "loadSnapshot",
            {"id": snapshot_id, "imgSize": snapshot_size},
        )

    # Motion
    def is_motion_detection_enabled(self, camera_id):
        """Return motion setting matching camera_id."""
        return self._cameras_by_id[camera_id].is_motion_detection_enabled

    def enable_motion_detection(self, camera_id):
        """Enable motion detection for camera matching camera_id."""
        return self._dsm.get(
            self.CAMERA_EVENT_API_KEY,
            "MDParamSave",
            {"camId": camera_id, "source": MOTION_DETECTION_BY_SURVEILLANCE},
        )

    def disable_motion_detection(self, camera_id):
        """Disable motion detection for camera matching camera_id."""
        return self._dsm.get(
            self.CAMERA_EVENT_API_KEY,
            "MDParamSave",
            {"camId": camera_id, "source": MOTION_DETECTION_DISABLED},
        )

    # Home mode
    def get_home_mode_status(self):
        """Get the state of Home Mode"""
        return self._dsm.get(self.HOME_MODE_API_KEY, "getinfo")["data"]["on"]

    def set_home_mode(self, state):
        """Set the state of Home Mode (state: bool)"""
        return self._dsm.get(self.HOME_MODE_API_KEY, "switch", {"on": state})["success"]
