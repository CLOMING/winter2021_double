from double3sdk.api import _Api
from double3sdk.base import _Base
from double3sdk.bluetooth import _Bluetooth
from double3sdk.calibration import _Calibration
from double3sdk.camera import _Camera
from double3sdk.depth import _Depth
from double3sdk.dock_tracker import _DockTracker
from double3sdk.documentation import _Documentation
from double3sdk.endpoint import _Endpoint
from double3sdk.events import _Events
from double3sdk.grid_manager import _GridManager
from double3sdk.gui import _Gui
from double3sdk.imu import _Imu
from double3sdk.mics import _Mics
from double3sdk.navigate import _Navigate
from double3sdk.network import _Network
from double3sdk.pose import _Pose
from double3sdk.ptz import _Ptz
from double3sdk.screensaver import _Screensaver
from double3sdk.speaker import _Speaker
from double3sdk.system import _System
from double3sdk.tilt import _Tilt
from double3sdk.ultrasonic import _Ultrasonic
from double3sdk.updater import _Updater
from double3sdk.webrtc import _Webrtc

from double3sdk.double_api import _DoubleAPI


class Double3SDK:
    def __init__(self) -> None:
        self.api = _Api()
        self.base = _Base()
        self.bluetooth = _Bluetooth()
        self.calibaration = _Calibration()
        self.camera = _Camera()
        self.depth = _Depth()
        self.dock_tracker = _DockTracker()
        self.documentation = _Documentation()
        self.endpoint = _Endpoint()
        self.events = _Events()
        self.grid_manager = _GridManager()
        self.gui = _Gui()
        self.imu = _Imu()
        self.mics = _Mics()
        self.navigate = _Navigate()
        self.network = _Network()
        self.pose = _Pose()
        self.ptz = _Ptz()
        self.screensaver = _Screensaver()
        self.speaker = _Speaker()
        self.system = _System()
        self.tilt = _Tilt()
        self.ultrasonic = _Ultrasonic()
        self.updater = _Updater()
        self.webrtc = _Webrtc()

    def recv(self) -> str:
        double_api = _DoubleAPI()
        return str(double_api.recv())
