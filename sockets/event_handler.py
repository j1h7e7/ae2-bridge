import logging
import socket
import socketserver
import time
from typing import Callable

from pydantic import BaseModel

CallbackType = Callable[[str], str | None]


logger = logging.getLogger(__name__)


class EventPayload(BaseModel):
    event_type: str
    data: str | None = None


class SizedBufferWrapper:
    def __init__(self):
        self.buf = bytearray()

    @property
    def size(self):
        return len(self.buf)

    def readline(self) -> bytes:
        idx = self.buf.find(b"\n")
        outpt = self.buf[:idx]
        del self.buf[: idx + 1]
        return bytes(outpt)

    def write(self, inpt: bytes, /):
        self.buf.extend(inpt)


class EventHandler:
    def __init__(self):
        self.callbacks: dict[str, CallbackType] = {}
        self.default_callback: CallbackType | None = None
        self.buffer = SizedBufferWrapper()

        # TODO: this is a hack
        self.req_handler: socketserver.BaseRequestHandler | None = None

        self.closed = False
        self.callbacks["close"] = lambda _: self.close()

    @property
    def req(self) -> socket.socket:
        if self.req_handler is None:
            raise ValueError()
        return self.req_handler.request

    def close(self):
        logger.info(f"Closing socket {self.req_handler}")
        self.closed = True

    def register(self, event_name: str) -> Callable[[CallbackType], CallbackType]:
        def _decorator(fn: CallbackType):
            self.callbacks[event_name] = fn
            return fn

        return _decorator

    def emit(self, data: str, /, *, newline: bool = True) -> None:
        bytes_data = bytes(data, encoding="utf-8") + b"\n" if newline else b""
        self.req.send(bytes_data)

    def handle_single_event(self, payload: EventPayload):
        event_name = payload.event_type
        event_data = payload.data
        callback = self.callbacks.get(event_name, self.default_callback)
        if not callback:
            raise ValueError(f"No callback for event {event_name}")
        output = callback(event_data)
        if output is not None:
            self.emit(output)

    def _fill_buffer(self):
        while self.buffer.size < 10000:
            chunk = self.req.recv(1024)
            self.buffer.write(chunk)
            if b"\n" in chunk:
                break

    def handle(self):
        while not self.closed:
            self._fill_buffer()
            while line := self.buffer.readline():
                payload = EventPayload.model_validate_json(line)
                self.handle_single_event(payload)
            time.sleep(0.1)
