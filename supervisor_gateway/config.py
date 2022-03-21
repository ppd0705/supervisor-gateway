import os


class Conf:
    def __init__(self):
        # listen addr
        self.host: str = os.environ.get("SG_HOST") or "localhost"
        self.port: int = int(os.environ.get("SG_PORT") or "1234")

        # supervisor rpc url
        self.rpc_url: str = os.environ.get("SG_RPC") or "http://localhost:9011/RPC2"

        # log
        self.log_level: str = os.environ.get("SG_LOG_LEVEL") or "DEBUG"
        self.log_file: str = os.environ.get("SG_LOG_FILE") or "supervisor_gateway.log"

        # std file
        self.stdin: str = os.environ.get("SG_STDIN") or "/dev/stdin"
        self.stdout: str = os.environ.get("SG_STDOUT") or "/dev/stdout"


conf = Conf()
