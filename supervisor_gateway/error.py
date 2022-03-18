from aiohttp.web import Response
from aiohttp.web import json_response


class BaseError(Exception):
    _CODE: int = 50000
    _MSG: str = "unknown error"

    def __init__(self, extra_msg: str = ""):
        self._extra_msg = extra_msg

    @property
    def code(self) -> str:
        return self.code

    @property
    def msg(self) -> str:
        if not self._extra_msg:
            return self._MSG
        return f"{self._MSG}: {self._extra_msg}"

    @property
    def http_code(self) -> int:
        return self._CODE // 100

    def dict(self) -> dict:
        return {
            "code": self.code,
            "msg": self.msg,
        }

    def json_response(self) -> Response:
        return json_response(data=self.dict(), status=self.http_code)


class BadQuestError(BaseError):
    _CODE: int = 40000
    _MSG: str = "bad request"


class InvalidParameterError(BaseError):
    _CODE: int = 40001
    _MSG: str = "invalid parameters"


class NotFoundError(BaseError):
    _CODE: int = 40400
    _MSG: str = "path not found"


class ProcessNotFoundError(BaseError):
    _CODE: int = 40401
    _MSG: str = "process not found"


class MethodNotAllowedError(BaseError):
    _CODE: int = 40501
    _MSG: str = "method not allowed"


class InternalError(BaseError):
    _MSG: str = "internal error"


class SupervisordError(BaseError):
    _CODE: int = 50001
    _MSG: str = "supervisord error"
