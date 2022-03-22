from typing import List

from fastapi import APIRouter

from supervisor_gateway.schema import ProcessInfo
from supervisor_gateway.schema import SupervisorState
from supervisor_gateway.supervisor import format_process_info
from supervisor_gateway.xml_rpc import rpc

router = APIRouter()


@router.get("/state", response_model=SupervisorState)
async def get_rpc_state():
    data = await rpc.get_state()
    return {"state": data["statename"]}


@router.get("/processes", response_model=List[ProcessInfo])
async def list_rpc_processes():
    data = await rpc.get_all_process_info()
    processes = [format_process_info(item) for item in data]
    return processes


@router.get("/processes/{name}", response_model=ProcessInfo)
async def get_rpc_process(name: str):
    item = await rpc.get_process_info(name)
    return format_process_info(item)


@router.post("/processes/{name}/stop")
async def stop_rpc_process(name: str):
    await rpc.stop_process(name)


@router.post("/processes/{name}/start")
async def start_rpc_process(name: str):
    await rpc.start_process(name)


@router.post("/processes/{name}/restart")
async def restart_rpc_process(name: str):
    await rpc.restart_process(name)


@router.post("/processes/{name}/add")
async def add_rpc_process(name: str):
    await rpc.add_process_group(name)


@router.post("/processes/{name}/remove")
async def remove_rpc_process(name: str):
    await rpc.remove_process_group(name)
