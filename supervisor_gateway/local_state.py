from typing import Any
from typing import Dict
from typing import List

from supervisor_gateway.log import logger
from supervisor_gateway.supervisor import format_process_info
from supervisor_gateway.time import now


class LocalSate:
    def __init__(self):
        self.processes: Dict[str, Dict] = {}
        self.supervisor: Dict[str, str] = {}

    def update_supervisor(self, running_state: str):
        self.supervisor["state"] = running_state

    def add_process(self, process: Dict):
        self.processes[process["name"]] = format_process_info(process)

    def add_processes(self, processes: List[Dict]):
        for p in processes:
            self.add_process(p)

    def clean(self):
        self.processes = {}
        self.supervisor = {}

    def event_handler(self, event: Dict[str, Any]):
        if "eventname" not in event:
            return
        if event["eventname"].startswith("SUPERVISOR_STATE_CHANGE_"):
            state_name = event["eventname"][24:]
            self.update_supervisor(state_name)
        elif event["eventname"].startswith("PROCESS_STATE_"):
            state_name = event["eventname"][14:]
            name = event["payload"]["processname"]
            info = {
                "name": name,
                "state": state_name,
                "update_time": now(),
            }
            self.processes[name] = info
        elif event["eventname"] == "PROCESS_GROUP_REMOVED":
            name = event["payload"]["groupname"]
            try:
                del self.processes[name]
            except KeyError:
                logger.error(f"process {name} not found, event: {event}")
        else:
            logger.warning(f"unknown event: {event}")


state = LocalSate()
