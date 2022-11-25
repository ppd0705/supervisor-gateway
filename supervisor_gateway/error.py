class BaseError(Exception):
    code: int = 50000
    message: str = "UNKNOWN_ERROR"
    detail: str = ""

    def __init__(self, detail: str = ""):
        self.detail = detail

    @property
    def http_code(self) -> int:
        return self.code // 100

    def dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
        }


class BadRequestError(BaseError):
    code: int = 40000
    message: str = "BAD_REQUEST"


class InvalidParameterError(BaseError):
    code: int = 40001
    message: str = "INVALID_PARAMETER"


class NotFoundError(BaseError):
    code: int = 40400
    message: str = "PATH_NOT_FOUND"


class ProcessNotFoundError(BaseError):
    code: int = 40401
    message: str = "PROCESS_NOT_FOUND"


class MethodNotAllowedError(BaseError):
    code: int = 40500
    message: str = "METHOD_NOT_ALLOWED"


class InternalError(BaseError):
    message: str = "INTERNAL_ERROR"


class SupervisordError(BaseError):
    code: int = 50001
    message: str = "SUPERVISORD_ERROR"
