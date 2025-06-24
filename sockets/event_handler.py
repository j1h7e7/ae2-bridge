import functools
import inspect
import logging
import socket
import socketserver
import time
from typing import Callable, Type

from sqlalchemy.orm import Session

from sockets.db import sessions
from sockets.event_types import BaseEventPayload, EventPayload

CallbackType = (
    Callable[[EventPayload], str | None] | Callable[[EventPayload, Session], str | None]
)


logger = logging.getLogger(__name__)


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


class EventHandlerInstance:
    def __init__(
        self,
        req_handler: socketserver.BaseRequestHandler,
        callbacks: dict[str, CallbackType],
    ):
        self.callbacks: dict[str, CallbackType] = callbacks
        self.default_callback: CallbackType | None = None
        self.buffer = SizedBufferWrapper()

        self.req_handler = req_handler

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

    def emit(self, data: str, /, *, newline: bool = True) -> None:
        bytes_data = bytes(data, encoding="utf-8") + b"\n" if newline else b""
        self.req.send(bytes_data)

    def handle_single_event(self, payload: BaseEventPayload):
        logger.info(f"Handling event {payload=}")
        event_name = payload.event_type
        callback = self.callbacks.get(event_name, self.default_callback)
        if not callback:
            raise ValueError(f"No callback for event {event_name}")
        output = callback(payload) or "ack"
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
                self.handle_single_event(payload.root)
            time.sleep(0.01)


class EventHandlerManager:
    def __init__(self):
        self.callbacks: dict[str, CallbackType] = {}

    @staticmethod
    def _get_event_type(fn: CallbackType) -> str:
        argspec = inspect.getfullargspec(fn)
        payload_type: Type[BaseEventPayload] = argspec.annotations["payload"]
        event_type: type = payload_type.model_fields["event_type"].annotation
        return event_type.__args__[0]  # cursed

    @staticmethod
    def _takes_sqlalchemy_session(fn: CallbackType) -> bool:
        argspec = inspect.getfullargspec(fn)
        return "session" in argspec.annotations

    def register(
        self, arg: str | CallbackType | None = None
    ) -> Callable[[CallbackType], CallbackType]:
        event_name: str | None = None

        def _decorator(fn: CallbackType):
            event_name2: str = event_name or self._get_event_type(fn)
            takes_session: bool = self._takes_sqlalchemy_session(fn)

            @functools.wraps(fn)
            def wrapper(payload: BaseEventPayload):
                if takes_session:
                    with sessions() as session:
                        return fn(payload, session)
                return fn(payload)

            self.callbacks[event_name2] = wrapper
            return wrapper

        if callable(arg):
            return _decorator(arg)
        else:
            event_name = arg
            return _decorator

    def new_instance(
        self, req_handler: socketserver.BaseRequestHandler
    ) -> EventHandlerInstance:
        return EventHandlerInstance(req_handler=req_handler, callbacks=self.callbacks)
