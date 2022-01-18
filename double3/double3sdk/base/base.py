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
