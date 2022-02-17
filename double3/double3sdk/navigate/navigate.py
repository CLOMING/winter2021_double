from typing import Any, Dict, Optional
from double3sdk.double_api import _DoubleAPI


class _Navigate:
    def enable(self) -> None:
        '''
        navigate.enable
            navigate 실행
        '''
        double_api = _DoubleAPI()
        double_api.send_command('navigate.enable')

    def disable(self) -> None:
        '''
        navigate.disable
            navigate 종료
        '''
        double_api = _DoubleAPI()
        double_api.send_command('navigate.disable')

    def cancel_target(self) -> None:
        '''
        navigate.cancelTarget
            event: DRNavigateModule.cancelTarget
        '''
        double_api = _DoubleAPI()
        double_api.send_command('navigate.cancelTarget')

    def drive(
        self,
        throttle: float,
        turn: float,
        powerdrive: bool,
        disableturn: bool
    ) -> None:
        '''     
        navigate.drive
            throttle
                -1~1 사이의 실수
                양수이면 앞으로 일정거리만큼 직진, 음수이면 뒤로 일정거리만큼 후진
            turn 
                -1~1 사이의 실수
                양수이면 시계방향으로 일정 각도만큼 회전, 음수이면 반시계방향으로 일정 각도만큼 회전

            powerDirve
                True/False
                속도 증가 여부 
                False 권장

            disableTurn 
                True/False
                직선 주행 보정 여부
                False를 권장
        '''

        command: str = 'navigate.drive'
        data: Dict[str, Any] = {}

        data["throttle"] = throttle

        data["turn"] = turn

        data["powerDrive"] = powerdrive

        data["disableTurn"] = disableturn

        double_api = _DoubleAPI()
        double_api.send_command(command, data)

    def hit_result(
        self, data
    ) -> None:
        '''
        navigate.hitResult
            camera.hitTest의 이벤트 DRCamera.hitResult의 응답 중 data 파트를 변수로 받으면 navigate.target을 내부적으로 사용하여 해당 위치로 이동시킴
            따로 사용할 수도 있지만 그럴 경우 navigate.target 사용을 권장
        '''

        double_api = _DoubleAPI()

        command: str = 'navigate.hitResult'

        double_api.send_command(command, data)

    def target(
        self,
        x: float,
        y: float,
        angleradians: float,
        relative: bool,
        dock: bool,
        dockid: float,
        action: str
    ) -> None:
        '''
        navigate.target
            event: DRNavigateModule.target
            x
                실수
                앞으로 갈 거리(m단위)
            y
                실수
                좌/우로 갈 거리(m단위)

            angleradians
                실수
                목적지에 도착 후 회전할 각도

            relative
                True/False
                목적지를 현재 위치에서 상대적으로 계산할 것인지의 여부
                True로 설정해야 실제 우리가 생각하는 위치로 이동시킬 수 있음

            dock
                True/False
                dock으로 갈 때 사용
                False를 권장

            dockid
                dock으로 갈 때 ID 입력 시 사용
                0 을 권장

            action
                문자열
                dock에서 나올 때 사용
                ""을 권장
        '''
        command: str = 'navigate.target'
        data: Dict[str, Any] = {}

        data["x"] = x

        data["y"] = y

        data["angleRadians"] = angleradians

        data["relative"] = relative

        data["dock"] = dock

        data["dockId"] = dockid

        data["action"] = action

        double_api = _DoubleAPI()
        double_api.send_command(command, data)
