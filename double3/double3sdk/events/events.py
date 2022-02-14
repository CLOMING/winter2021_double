from double3sdk.double_api import _DoubleAPI


class _Events:
    def subscribe(self, events: list) -> None:
        '''
        events.subscribe
            events
                [ "이벤트 이름" ]
        '''
        double_api = _DoubleAPI()
        double_api.send_command(
            'events.subscribe',
            {"events": events}
        )

    def unsubscribe(self, events: list) -> None:
        '''
        events.unsubscribe
            events
                [ "이벤트 이름" ]
        '''
        double_api = _DoubleAPI()
        double_api.send_command(
            'events.unsubscribe',
            {"events": events}
        )
