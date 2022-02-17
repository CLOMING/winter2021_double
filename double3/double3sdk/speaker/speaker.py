from double3sdk.double_api import _DoubleAPI


class _Speaker:
    def enable(self) -> None:
        '''
        speaker.enable
            스피커 실행
        '''
        double_api = _DoubleAPI()
        double_api.send_command('speaker.enable')

    def disable(self) -> None:
        '''
        speaker.disable
            스피커 끄기
        '''
        double_api = _DoubleAPI()
        double_api.send_command('speaker.disable')

    def set_volume(self, percent: float) -> None:
        '''
        speaker.setVolume
            percent
                0-1 사이의 실수
                스피커의 볼륨을 (percent)*100 %로 설정
        '''
        double_api = _DoubleAPI()
        double_api.send_command(
            'speaker.setVolume',
            {"percent": percent}
        )

    def request_volume(self) -> None:
        '''
        speaker.requestVolume
            event: DRSpeaker.volume
        '''
        double_api = _DoubleAPI()
        double_api.send_command('speaker.requestVolume')
