from aiohttp.web import Request, RouteTableDef, json_response

local_routes = RouteTableDef()


@local_routes.get("/processes")
async def list_processes(request: Request):
    processes = sorted(request.app["processes"].items())
    keyword = request.query.get("keyword", "")
    page = int(request.query.get("page") or "1")
    limit = int(request.query.get("limit") or "50")
    if keyword:
        processes = [(name, process) for name, process in processes if keyword in name]
    total = len(processes)
    start = max((page - 1) * limit, 0)
    end = start + limit
    return json_response(
        {"total": total, "processes": [p for _, p in processes[start:end]]}
    )
