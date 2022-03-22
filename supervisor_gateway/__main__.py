import pathlib

import uvicorn
from uvicorn.main import LOGGING_CONFIG

from supervisor_gateway.config import conf
from supervisor_gateway.main import app

if __name__ == "__main__":
    path = pathlib.Path(conf.log_file)
    unicorn_path = path.parent / "unicorn.log"
    access_path = path.parent / "unicorn.access.log"
    LOGGING_CONFIG["handlers"] = {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(unicorn_path),
            "maxBytes": 50 * 1024 * 1024,
            "backupCount": 3,
        },
        "access": {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(access_path),
            "maxBytes": 50 * 1024 * 1024,
            "backupCount": 3,
        },
    }
    uvicorn.run(app, host=conf.host, port=conf.port)
