from double3sdk.double_api import _DoubleAPI


class _Api:
    def request_status(self) -> None:
        '''
        api.requestStatus
            event: DRAPI.status
        '''
        double_api = _DoubleAPI()
        double_api.send_command('api.requestStatus')
