from aiohttp.web import run_app

from supervisor_gateway.config import conf
from supervisor_gateway.log import logger
from supervisor_gateway.main import application

if __name__ == "__main__":
    run_app(application, host=conf.host, port=conf.port, print=logger.info)
