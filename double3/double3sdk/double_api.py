from socket import AF_UNIX, SOCK_STREAM, socket
from typing import Any, Dict, Optional
import json

from double3sdk.constants import CONST
from double3sdk.double_error import DoubleError


class _DoubleAPI:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(_DoubleAPI, cls).__new__(cls)
            cls.instance.open_socket()

        return cls.instance

    def __del__(self):
        self.close()

    def open_socket(self):
        if(hasattr(self, '_sock')):
            return

        self._sock = socket(AF_UNIX, SOCK_STREAM)
        self._sock.connect(CONST.api_path)

    def close(self):
        if(not hasattr(self, '_sock')):
            return

        self._sock.close()
        del self._sock

        del _DoubleAPI.instance

    def send_command(self, command: str, data=None):
        packet: Dict[str, Any] = {'c': command}
        if data is not None:
            packet['d'] = data
        jsonString: str = json.dumps(packet)
        self._sock.send(jsonString.encode(CONST.utf8))

    def recv(self) -> Any:
        packet: str = self._sock.recv(4096).decode(CONST.utf8)

        if not packet:
            raise DoubleError(
                message='received None from D3SDK'
            )

        object: Optional[Any]

        try:
            object = json.loads(packet)
        except ValueError as e:
            raise DoubleError(
                message='JSON Parse error',
                data={e, packet}
            )

        return object
