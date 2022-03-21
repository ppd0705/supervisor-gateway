import uvicorn

from supervisor_gateway.config import conf
from supervisor_gateway.main import app

if __name__ == "__main__":
    uvicorn.run(app, host=conf.host, port=conf.port)
