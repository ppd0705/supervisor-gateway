# supervisor-gateway

An RESTful supervisor gateway with paginated and cached process info

## Features
- RESTful API to `supevisord` support
- A `eventlistener` role for events subscription  
- Cached status API with pagination 

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

`supervisor-gateway` running as child process of supervisord, there is a [supervisor config_example](config/supervisor/supervisor_gateway.conf)

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
- SG_HOST
- SG_PORT
- SG_RPC
- SG_LOG_LEVEL
- SG_LOG_FILE

update supervisor conf
```shell
supervisorctl update supervisor_gateway
```

check it 
```shell
curl  http://localhost:$SG_PORT/rpc/state  
```

## TODO
- [] Add unit test
- [] Add more API
- [] Add API documents

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- [supervisor](https://github.com/Supervisor/supervisor)
- [multivisor](https://github.com/tiagocoutinho/multivisor)
- [aiofiles](https://github.com/Tinche/aiofiles)
- [aiohttp-xmlrpc](https://github.com/mosquito/aiohttp-xmlrpc)