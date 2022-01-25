from enum import Enum
from typing import Any, Dict, Optional
from double3sdk.double_api import _DoubleAPI
from double3sdk.double_error import DoubleError


class _Template(str, Enum):
    preheat = "preheat"
    screen = "screen"
    h264ForWebRTC = "h264ForWebRTC"
    v412 = "v412"


class _Camera:
    def enable(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        template: Optional[_Template] = None,
        gstreamer: Optional[str] = None,
    ) -> None:
        '''
        camera.enable
            width, height
                정수
                기본 사이즈는 1152x720 또는 1728x1080

            template
                template 값으로 다음 문자열 중 하나가 올 수 있다.
                "preheat": 카메라를 켜지만 출력이 없음
                    _Template.preheat.value를 사용
                "screen": "nvoverlaysink"를 이용해서 화면에 보여준다.
                    _Template.screen.value를 사용
                "h264ForWebRTC": 하드웨어를 h264로 부호화하고 d3-webrtc 바이너리에 게시
                    _Template.h264ForWebRTC.value를 사용
                "v412": /dev/video9로 출력하고 Electron/Chromium에서 웹캠 "D3_Camera"으로 보여줌
                    _Template.v412.value를 사용
                주의: array of outputs를 보낼 때는 기본 사이즈만 가능

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
            data["template"] = template

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
        passToNavigate: bool
    ) -> None:
        '''
        event: DRCamera.hitResult
        x, y
            0-1 사이의 실수
            (0,0)은 좌측상단, (0.5,0.5)는 중앙, (1,1)은 우측하단 

        highlight
            충전이나 QR 아이콘을 누르면 주변에 투명한 원형 빛이 나옴

        passToNavigate
            실제 행동을 위해 navigate.hitResult 명령에 hit 결과를 보내줌 
        '''

        command: str = 'camera.hitTest'
        data: Dict[str, Any] = {}

        data["x"] = x

        data["y"] = y

        data["highlight"] = highlight

        data["passToNavigate"] = passToNavigate

        double_api = _DoubleAPI()
        double_api.send_command(command, data)

    def capture_photo(self) -> None:
        '''
        camera.capturePhoto
            event: DRCamera.photo
        '''
        double_api = _DoubleAPI()
        double_api.send_command('camera.capturePhoto')
