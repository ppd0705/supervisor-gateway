from typing import List

from pydantic import BaseModel


class SupervisorState(BaseModel):
    state: str


class ProcessInfo(BaseModel):
    name: str
    state: str
    from_state: str = ""
    update_time: int = 0

    def __repr__(self):
        return f"{self.name} {self.from_state} --> {self.state}"


class LocalProcesses(BaseModel):
    total: int
    processes: List[ProcessInfo]


class ProcessConfState(BaseModel):
    added: List[str]
    changed: List[str]
    removed: List[str]
