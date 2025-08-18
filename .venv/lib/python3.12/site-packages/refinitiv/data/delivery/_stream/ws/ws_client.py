import simplejson as json
import socket
from typing import Callable, List, Dict, Tuple

import websocket


class WebSocketClient:
    def __init__(self, on_message: Callable[[List[Dict]], None], *args, **kwargs) -> None:
        # set global timeout for WebSocketApp according documentation
        # https://websocket-client.readthedocs.io/en/latest/examples.html#setting-timeout-value
        websocket.setdefaulttimeout(5)

        self._on_message = on_message
        self.ws = websocket.WebSocketApp(on_message=self._on_ws_message, *args, **kwargs)

    def _on_ws_message(self, ws: websocket.WebSocketApp, s: str) -> None:
        try:
            messages = json.loads(s)
        except UnicodeDecodeError:
            messages = "".join(map(chr, bytearray(s)))
            messages = json.loads(messages)
        self._on_message(messages)

    def send(self, data: dict) -> None:
        self.ws.send(json.dumps(data))

    def run_forever(self, *args, **kwargs) -> None:
        self.ws.run_forever(*args, **kwargs)

    def close(self, **kwargs) -> None:
        self.ws.close(**kwargs)

    def get_socket_info(self) -> Tuple[str, str]:
        ip = self.ws.sock.sock.getsockname()[0]
        try:
            hostname = socket.gethostname()
        except socket.gaierror:
            hostname = "net"
        return ip, hostname
