from aiohttp.web import Request, RouteTableDef, json_response

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
