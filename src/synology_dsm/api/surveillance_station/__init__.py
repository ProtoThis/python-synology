"""Synology SurveillanceStation API wrapper."""
from .camera import SynoCamera
from .const import MOTION_DETECTION_BY_SURVEILLANCE
from .const import MOTION_DETECTION_DISABLED


class SynoSurveillanceStation:
    """An implementation of a Synology SurveillanceStation."""

    API_KEY = "SYNO.SurveillanceStation.*"
    INFO_API_KEY = "SYNO.SurveillanceStation.Info"
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
        self._cameras_by_id = {}
        list_data = self._dsm.get(self.CAMERA_API_KEY, "List", max_version=7)["data"]
        for camera_data in list_data["cameras"]:
            if camera_data["id"] in self._cameras_by_id:
                self._cameras_by_id[camera_data["id"]].update(camera_data)
            else:
                self._cameras_by_id[camera_data["id"]] = SynoCamera(camera_data)

        for camera_id in self._cameras_by_id:
            self._cameras_by_id[camera_id].update_motion_detection(
                self._dsm.get(
                    self.CAMERA_EVENT_API_KEY, "MotionEnum", {"camId": camera_id}
                )["data"]
            )

        if not self._cameras_by_id:
            return

        live_view_datas = self._dsm.get(
            self.CAMERA_API_KEY,
            "GetLiveViewPath",
            {"idList": ",".join(str(k) for k in self._cameras_by_id)},
        )["data"]
        for live_view_data in live_view_datas:
            self._cameras_by_id[live_view_data["id"]].live_view.update(live_view_data)

    # Global
    def get_info(self):
        """Return general informations about the Surveillance Station instance."""
        return self._dsm.get(self.INFO_API_KEY, "GetInfo")

    # Camera
    def get_all_cameras(self):
        """Return a list of cameras."""
        return self._cameras_by_id.values()

    def get_camera(self, camera_id):
        """Return camera matching camera_id."""
        return self._cameras_by_id[camera_id]

    def get_camera_live_view_path(self, camera_id, video_format=None):
        """Return camera live view path matching camera_id.

        Args:
            camera_id: ID of the camera we want to get the live view path.
            video_format: mjpeg_http | multicast | mxpeg_http |  rtsp_http | rtsp.
        """
        if video_format:
            return getattr(self._cameras_by_id[camera_id].live_view, video_format)
        return self._cameras_by_id[camera_id].live_view

    def get_camera_image(self, camera_id):
        """Return bytes of camera image for camera matching camera_id."""
        return self._dsm.get(
            self.CAMERA_API_KEY, "GetSnapshot", {"id": camera_id, "cameraId": camera_id}
        )

    def enable_camera(self, camera_id):
        """Enable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._dsm.get(self.CAMERA_API_KEY, "Enable", {"idList": camera_id})[
            "success"
        ]

    def disable_camera(self, camera_id):
        """Disable camera(s) - multiple ID or single ex 1 or 1,2,3."""
        return self._dsm.get(self.CAMERA_API_KEY, "Disable", {"idList": camera_id})[
            "success"
        ]

    # Snapshot
    def capture_camera_image(self, camera_id, save=True):
        """Capture a snapshot for camera matching camera_id."""
        return self._dsm.get(
            self.SNAPSHOT_API_KEY,
            "TakeSnapshot",
            {
                "camId": camera_id,
                "blSave": int(save),  # API requires an integer instead of a boolean
            },
        )

    def download_snapshot(self, snapshot_id, snapshot_size):
        """Download snapshot image binary for a givent snapshot_id.

        Args:
            snapshot_id: ID of the snapshot we want to download.
            snapshot_size: SNAPSHOT_SIZE_ICON | SNAPSHOT_SIZE_FULL.
        """
        return self._dsm.get(
            self.SNAPSHOT_API_KEY,
            "LoadSnapshot",
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
        """Get the state of Home Mode."""
        return self._dsm.get(self.HOME_MODE_API_KEY, "GetInfo")["data"]["on"]

    def set_home_mode(self, state):
        """Set the state of Home Mode (state: bool)."""
        return self._dsm.get(
            self.HOME_MODE_API_KEY, "Switch", {"on": str(state).lower()}
        )["success"]
