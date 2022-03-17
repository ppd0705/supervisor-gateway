from asyncio import get_event_loop
from typing import Any, Dict

from aiohttp.web import Application

from supervisor_gateway.api.local import local_routes
from supervisor_gateway.api.rpc import rpc_routes
from supervisor_gateway.config import conf
from supervisor_gateway.event_listener import Listener
from supervisor_gateway.log import logger
from supervisor_gateway.rpc import RPC
from supervisor_gateway.time import now


async def on_startup(app: Application):
    app["processes"] = processes = {}

    def event_handler(event: Dict[str, Any]):
        if not event:
            return
        if event["eventname"].startswith("PROCESS_STATE_"):
            state = event["eventname"][14:]
            name = event["payload"]["processname"]
            if name not in processes:
                logger.error(f"process {name} not found, event: {event}")
                return
            processes[name]["statename"] = state
            processes[name]["update_time"] = now()

        elif event["eventname"] == "PROCESS_GROUP_REMOVED":
            name = event["payload"]["groupname"]
            if name not in processes:
                logger.error(f"process {name} not found, event: {event}")
                return
            del processes[name]
        else:
            logger.warning(f"unknown event: {event}")

    rpc = RPC(conf.rpc_url)
    process_list = await rpc.get_all_process_info()
    for p in process_list:
        processes[p["name"]] = p
    app["rpc"]: RPC = rpc
    listener = Listener(event_handler)
    loop = get_event_loop()
    loop.create_task(listener.start())
    app["listener"]: Listener = listener
    logger.debug("on_startup finished")


async def on_shutdown(app: Application):
    app["listener"].stop()
    await app["rpc"].close()
    logger.debug("on_shutdown finished")


def get_app() -> Application:
    app = Application()
    app["processes"]: Dict[str, Dict[str, Any]] = {}
    app.add_routes(rpc_routes)
    app.add_routes(local_routes)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


application = get_app()
