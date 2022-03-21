from typing import List

from pydantic import BaseModel


class SupervisorState(BaseModel):
    state: str


class ProcessInfo(BaseModel):
    name: str
    state: str
    update_time: int = 0


class LocalProcesses(BaseModel):
    total: int
    processes: List[ProcessInfo]
