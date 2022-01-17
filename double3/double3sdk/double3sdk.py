from api import _Api
from base import _Base
from bluetooth import _Bluetooth
from calibration import _Calibration
from camera import _Camera
from depth import _Depth
from dock_tracker import _DockTracker
from documentation import _Documentation
from endpoint import _Endpoint
from events import _Events
from grid_manager import _GridManager
from gui import _Gui
from imu import _Imu
from mics import _Mics
from navigate import _Navigate
from network import _Network
from pose import _Pose
from ptz import _Ptz
from screensaver import _Screensaver
from speaker import _Speaker
from system import _System
from tilt import _Tilt
from ultrasonic import _Ultrasonic
from updater import _Updater
from webrtc import _Webrtc

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
