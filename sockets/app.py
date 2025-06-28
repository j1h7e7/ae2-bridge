import importlib
import logging
import socket
import socketserver
from typing import NoReturn

from keepalive import set as set_keepalive

import sockets.routes
from sockets.event_handler import EventHandlerInstance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class App(socketserver.BaseRequestHandler):
    event_handler: EventHandlerInstance

    def setup(self):
        logger.info("starting new connection")
        req: socket.socket = self.request
        set_keepalive(req, after_idle_sec=60 * 10)
        importlib.reload(sockets.routes)
        self.event_handler = sockets.routes.event_handler.new_instance(self)

    def handle(self):
        logger.info("handling connection")
        self.event_handler.handle()


def start_server(host: str = "localhost", port: int = 9999) -> NoReturn:
    with socketserver.ThreadingTCPServer((host, port), App) as server:
        server.daemon_threads = True
        logger.info("starting server")
        server.serve_forever()
    raise Exception("done")


if __name__ == "__main__":
    start_server()
