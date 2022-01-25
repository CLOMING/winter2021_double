from double3sdk.double_api import _DoubleAPI


class _Screensaver:
    def nudge(self) -> None:
        '''
        screensaver_nudge
            반응이 들어오면 화면을 킴
        '''
        double_api = _DoubleAPI()
        double_api.send_command('screensaver.nudge')
