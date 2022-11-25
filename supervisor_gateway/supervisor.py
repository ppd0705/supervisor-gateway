from enum import IntEnum

READY = "READY\n"
ACKNOWLEDGED = "RESULT 2\nOK"


class ProcessStates(IntEnum):
    STOPPED = 0
    STARTING = 10
    RUNNING = 20
    BACKOFF = 30
    STOPPING = 40
    EXITED = 100
    FATAL = 200
    UNKNOWN = 1000


class Faults:
    UNKNOWN_METHOD = 1
    INCORRECT_PARAMETERS = 2
    BAD_ARGUMENTS = 3
    SIGNATURE_UNSUPPORTED = 4
    SHUTDOWN_STATE = 6
    BAD_NAME = 10
    BAD_SIGNAL = 11
    NO_FILE = 20
    NOT_EXECUTABLE = 21
    FAILED = 30
    ABNORMAL_TERMINATION = 40
    SPAWN_ERROR = 50
    ALREADY_STARTED = 60
    NOT_RUNNING = 70
    SUCCESS = 80
    ALREADY_ADDED = 90
    STILL_RUNNING = 91
    CANT_REREAD = 92


def get_state_time(process_info: dict) -> int:
    if process_info["state"] in (
        ProcessStates.RUNNING,
        ProcessStates.STARTING,
    ):
        return process_info["start"]
    return process_info["stop"]


def format_process_info(process_info: dict) -> dict:
    return {
        "name": process_info["name"],
        "state": process_info["statename"],
        "update_time": get_state_time(process_info),
    }
