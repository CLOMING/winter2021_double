from enum import Enum
from typing import Any, Dict, Optional
from double3sdk.double_api import _DoubleAPI
from double3sdk.double_error import DoubleError


class Template(str, Enum):
    preheat = "preheat"
    screen = "screen"
    h264ForWebRTC = "h264ForWebRTC"
    v412 = "v412"


class _Camera:
    def enable(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        template: Optional[Template] = None,
        gstreamer: Optional[str] = None,
    ) -> None:
        '''
        camera.enable
            width, height
                정수
                기본 사이즈는 1152x720 또는 1728x1080

            template
                template 값으로 다음 문자열 중 하나가 올 수 있다.
                    "preheat" / "screen" /  "h264ForWebRTC" / "v412"

            gstreamer
                문자열 "appsrc name=d3src ! autovideosink"
        '''

        if (
            not (template is None)
            and not (gstreamer is None)
        ):
            raise DoubleError("Do not use templeate and gstreamer both")

        command: str = 'camera.enable'
        data: Dict[str, Any] = {}

        if not (width is None):
            data["width"] = width

        if not (height is None):
            data["height"] = height

        if not (template is None):
            data["template"] = str(template)

        if not (gstreamer is None):
            data["gstreamer"] = gstreamer

        double_api = _DoubleAPI()
        double_api.send_command(command, data)

    def disable(self) -> None:
        '''
        camera.disable
            카메라를 끔
        '''
        double_api = _DoubleAPI()
        double_api.send_command('camera.disable')

    def hit_test(
        self,
        x: float,
        y: float,
        highlight: bool,
    ) -> None:
        '''
        camera.hitTest
            event: DRCamera.hitResult
            x, y
                0-1 사이의 실수
                (0,0)은 좌측상단, (0.5,0.5)는 중앙, (1,1)은 우측하단 

            highlight
                True/False
                충전이나 QR 아이콘을 누르면 주변에 투명한 원형 빛이 나옴 
        '''

        command: str = 'camera.hitTest'
        data: Dict[str, Any] = {}

        data["x"] = x

        data["y"] = y

        data["highlight"] = highlight

        double_api = _DoubleAPI()
        double_api.send_command(command, data)

    def capture_photo(self) -> None:
        '''
        camera.capturePhoto
            event: DRCamera.photo
        '''
        double_api = _DoubleAPI()
        double_api.send_command('camera.capturePhoto')
