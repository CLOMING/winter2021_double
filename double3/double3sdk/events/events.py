from double3sdk.double_api import _DoubleAPI


class _Events:
    def subscribe(self, events: list) -> None:
        '''
        events.subscribe
            events
                [ "DRBase.status" ]
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
                [ "DRBase.status" ]
        '''
        double_api = _DoubleAPI()
        double_api.send_command(
            'events.unsubscribe',
            {"events": events}
        )
