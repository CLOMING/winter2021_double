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
