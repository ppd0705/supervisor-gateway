<p align="center">
<a href="https://github.com/ppd0705/supervisor-gateway/actions">
    <img src="https://github.com/ppd0705/supervisor-gateway/workflows/Test%20Suite/badge.svg" alt="Test Suite">
</a>
<a href="https://pypi.org/project/supervisor-gateway" target="_blank">
    <img src="https://img.shields.io/pypi/v/supervisor-gateway?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/supervisor-gateway" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/supervisor-gateway.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

# supervisor-gateway

An RESTful supervisor gateway with paginated and cached process info

## Features
- RESTful API to `supevisord` support
- A `eventlistener` role for events subscription  
- Cached status API with pagination 

## Architecture

<a href="https://github.com/ppd0705/supervisor-gateway">
    <img src="https://raw.githubusercontent/ppd0705/supervisor-gateway/master/architecture.png" alt="supervisor-gateway">
</a>

## Install

from pypi

```shell
pip install supervisor-gateway
```

or install locally

```shell
make install
```

## Usage

`supervisor-gateway` running as child process of supervisord, there is a [supervisor config example](config/supervisor/supervisor_gateway.conf)

```ini
[eventlistener:supervisor_gateway]
command = python -m supervisor_gateway
events = PROCESS_STATE,SUPERVISOR_STATE_CHANGE,PROCESS_GROUP
environment = SG_LOG_LEVEL="DEBUG",SG_RPC="http://localhost:9011/RPC2",SG_LOG_FILE=
              "supervisor_gateway.log",SG_HOST="localhost",SG_PORT="1234"
stderr_logfile = supervisor_gateway.err.log
stderr_logfile_maxbytes = 10MB
stderr_logfile_backups = 2
buffer_size = 1024
```

some supported environments blow:
- SG_HOST: listen host
- SG_PORT: listen port
- SG_RPC: supervisord rpc url
- SG_LOG_LEVEL: log level
- SG_LOG_FILE: log file

update supervisor conf
```shell
supervisorctl update supervisor_gateway
```

check it 
```shell
curl  http://localhost:1234/rpc/state  
```

interact with api document in the browser [http://localhost:1234/docs](http://localhost:1234/docs)

## TODO
- [x] Add unit test
- [x] Add more API
- [x] Add API documents

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- [supervisor](https://github.com/Supervisor/supervisor)
- [multivisor](https://github.com/tiagocoutinho/multivisor)
- [aioconsole](https://github.com/vxgmichel/aioconsole)
- [aiohttp-xmlrpc](https://github.com/mosquito/aiohttp-xmlrpc)
- [fastapi](https://github.com/tiangolo/fastapi)