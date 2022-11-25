from fastapi import APIRouter

from supervisor_gateway.error import ProcessNotFoundError
from supervisor_gateway.local_state import state
from supervisor_gateway.schema import LocalProcesses
from supervisor_gateway.schema import ProcessInfo

router = APIRouter()


@router.get("/processes", response_model=LocalProcesses)
async def list_processes(
    keywords: str = "",
    status: str = "",
    page: int = 1,
    limit: int = 50,
):
    processes = sorted(state.processes.items())
    for keyword in keywords.split(","):
        processes = [(name, process) for name, process in processes if keyword in name]
    if status:
        processes = [
            (name, process) for name, process in processes if status == process["state"]
        ]
    total = len(processes)
    start = max((page - 1) * limit, 0)
    end = start + limit
    return {"total": total, "processes": [p for _, p in processes[start:end]]}


@router.get("/processes/{name}", response_model=ProcessInfo)
async def get_rpc_process(name: str):
    item = state.processes.get(name)
    if item is None:
        raise ProcessNotFoundError()
    return item
