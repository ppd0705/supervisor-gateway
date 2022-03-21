from fastapi import APIRouter

from supervisor_gateway.local_state import state
from supervisor_gateway.schema import LocalProcesses

router = APIRouter()


@router.get("/processes", response_model=LocalProcesses)
async def list_processes(
    keywords: str = "",
    page: int = 1,
    limit: int = 50,
):
    processes = sorted(state.processes.items())
    for keyword in keywords.split("|"):
        processes = [(name, process) for name, process in processes if keyword in name]
    total = len(processes)
    start = max((page - 1) * limit, 0)
    end = start + limit
    return {"total": total, "processes": [p for _, p in processes[start:end]]}
