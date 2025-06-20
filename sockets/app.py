import socket
import socketserver
from typing import NoReturn

from sockets.event_handler import EventHandler

event_handler = EventHandler()


@event_handler.register("test")
def test(data: str):
    return data.capitalize()


class App(socketserver.BaseRequestHandler):
    def setup(self):
        req: socket.socket = self.request
        req.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        req.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 1000 * 60 * 2, 3000))
        event_handler.req_handler = self

    def handle(self):
        event_handler.handle()


def start_server() -> NoReturn:
    with socketserver.ThreadingTCPServer(("localhost", 9999), App) as server:
        server.serve_forever()
    raise Exception("done")


if __name__ == "__main__":
    start_server()
