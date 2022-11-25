import logging
from logging.handlers import RotatingFileHandler

from supervisor_gateway.config import conf

formatter = logging.Formatter(
    "[%(asctime)s] (%(levelname)s):%(filename)s:%(funcName)s:%(lineno)d: %(message)s"
)
hdl = RotatingFileHandler(
    filename=conf.log_file,
    maxBytes=50 * 1024 * 1024,
    backupCount=3,
)
hdl.setFormatter(formatter)
logger = logging.getLogger("sg")
logger.setLevel(conf.log_level)
logger.addHandler(hdl)
