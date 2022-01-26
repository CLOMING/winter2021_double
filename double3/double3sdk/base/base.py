from double3sdk.double_api import _DoubleAPI


class _Base:
    def pole_set_target(self, percent: float) -> None:
        '''
        base.pole.setTarget
            percent
                0-100 사이의 실수
                pole의 높이를 (percent)%로 설정
        '''
        double_api = _DoubleAPI()
        double_api.send_command(
            'base.pole.setTarget',
            {"percent": percent}
        )

    def kickstand_deploy(self) -> None:
        '''
        base.kickstand.deploy
            베이스의 받침다리를 펼침
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.kickstand.deploy')

    def kickstand_retract(self) -> None:
        '''
        base.kickstand.retract
            베이스의 받침다리를 접음
            주변 상황이 받침다리를 접기에 좋지 않으면 다음 이벤트가 발생
                event: DRBase.kickstandAngleError
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.kickstand.retract')

    def request_status(self) -> None:
        '''
        base.requestStatus
            event: DRBase.status
            이 이벤트를 subscirbe 해야 base의 api를 쓸 수 있음
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.requestStatus')

    def pole_stand(self) -> None:
        '''
        base.pole.stand
            폴 높이기
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.pole.stand')

    def pole_sit(self) -> None:
        '''
        base.pole.sit
            폴 낮추기
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.pole.sit')

    def pole_stop(self) -> None:
        '''
        base.pole.stop
            폴 조절 중지
        '''
        double_api = _DoubleAPI()
        double_api.send_command('base.pole.stop')
