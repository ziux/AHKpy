import secrets
from threading import Condition


class Event:
    def __init__(self, uuid=None):
        if not uuid:
            uuid = secrets.token_hex(24)
        self.uuid = uuid
        self._result = None
        self.status = 0
        self._condition = Condition()

    def result(self, timeout=10):
        with self._condition:
            self._condition.wait(timeout)
            return self._result

    def set_result(self, result):
        with self._condition:
            self._result = result
            self.status = 1
            self._condition.notify_all()
