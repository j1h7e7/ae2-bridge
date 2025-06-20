import logging
import socket
import socketserver
from typing import NoReturn

from keepalive import set as set_keepalive

from sockets.event_handler import EventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


event_handler = EventHandler()


@event_handler.register("test")
def test(data: str):
    return data.capitalize()


class App(socketserver.BaseRequestHandler):
    def setup(self):
        logger.info("starting new connection")
        req: socket.socket = self.request
        set_keepalive(req, after_idle_sec=60 * 10)
        event_handler.req_handler = self

    def handle(self):
        logger.info("handling connection")
        event_handler.handle()


def start_server(host: str = "localhost", port: int = 9999) -> NoReturn:
    with socketserver.ThreadingTCPServer((host, port), App) as server:
        server.daemon_threads = True
        logger.info("starting server")
        server.serve_forever()
    raise Exception("done")


if __name__ == "__main__":
    start_server()
