from typing import Dict
from typing import List
from typing import Union


class BaseError(Exception):
    code: int = 50000
    name: str = "UNKNOWN_ERROR"
    detail: Union[str, List[Dict]] = ""

    def __init__(self, detail: Union[str, List[Dict]] = ""):
        self.detail = detail

    @property
    def http_code(self) -> int:
        return self.code // 100

    def dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "detail": self.detail,
        }


class BadRequestError(BaseError):
    code: int = 40000
    name: str = "BAD_REQUEST"


class InvalidParameterError(BaseError):
    code: int = 40001
    name: str = "INVALID_PARAMETER"


class NotFoundError(BaseError):
    code: int = 40400
    name: str = "PATH_NOT_FOUND"


class ProcessNotFoundError(BaseError):
    code: int = 40401
    name: str = "PROCESS_NOT_FOUND"


class MethodNotAllowedError(BaseError):
    code: int = 40500
    name: str = "METHOD_NOT_ALLOWED"


class InternalError(BaseError):
    name: str = "INTERNAL_ERROR"


class SupervisordError(BaseError):
    code: int = 50001
    name: str = "SUPERVISORD_ERROR"
