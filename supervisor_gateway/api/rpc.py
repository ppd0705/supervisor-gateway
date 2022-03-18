from aiohttp.web import Request
from aiohttp.web import RouteTableDef
from aiohttp.web import json_response

from supervisor_gateway.rpc import RPC

rpc_routes = RouteTableDef()


@rpc_routes.get("/rpc/state")
async def get_rpc_state(request: Request):
    rpc: RPC = request.app["rpc"]
    data = await rpc.get_state()
    return json_response(data)


@rpc_routes.get("/rpc/processes")
async def list_rpc_processes(request: Request):
    rpc: RPC = request.app["rpc"]
    data = await rpc.get_all_process_info()
    return json_response(data)


@rpc_routes.get("/rpc/processes/{name}")
async def get_rpc_process(request: Request):
    rpc: RPC = request.app["rpc"]
    name = request.match_info["name"]
    data = await rpc.get_process_info(name)
    return json_response(data)


@rpc_routes.post("/rpc/processes/{name}/stop")
async def stop_rpc_process(request: Request):
    rpc: RPC = request.app["rpc"]
    name = request.match_info["name"]
    data = await rpc.stop_process(name)
    return json_response(data)


@rpc_routes.post("/rpc/processes/{name}/restart")
async def restart_rpc_process(request: Request):
    rpc: RPC = request.app["rpc"]
    name = request.match_info["name"]
    data = await rpc.restart_process(name)
    return json_response(data)


@rpc_routes.post("/rpc/processes/{name}/add")
async def add_rpc_process(request: Request):
    rpc: RPC = request.app["rpc"]
    name = request.match_info["name"]
    data = await rpc.add_process_group(name)
    return json_response(data)


@rpc_routes.post("/rpc/processes/{name}/remove")
async def remove_rpc_process(request: Request):
    rpc: RPC = request.app["rpc"]
    name = request.match_info["name"]
    data = await rpc.remove_process_group(name)
    return json_response(data)
