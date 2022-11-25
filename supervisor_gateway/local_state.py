from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from supervisor_gateway.config import conf
from supervisor_gateway.log import logger
from supervisor_gateway.supervisor import format_process_info
from supervisor_gateway.time import now


class LocalSate:
    def __init__(self, notify_states: Optional[List[str]] = None):
        self.processes: Dict[str, Dict] = {}
        self.supervisor: Dict[str, str] = {}
        self.notify_states = notify_states or []

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
        event_name = event.get("eventname", "")
        if event_name.startswith("SUPERVISOR_STATE_CHANGE_"):
            state_name = event_name[24:]
            self.update_supervisor(state_name)
        elif event_name.startswith("PROCESS_STATE_"):
            state_name = event_name[14:]
            name = event["payload"]["processname"]
            info = {
                "name": name,
                "state": state_name,
                "update_time": now(),
                "from_state": event["payload"].get("from_state", ""),
            }
            self.processes[name] = info
            if state_name in self.notify_states:
                logger.warning("new event: %s", info)
        elif event_name == "PROCESS_GROUP_REMOVED":
            name = event["payload"]["groupname"]
            try:
                del self.processes[name]
            except KeyError:
                logger.error(f"process {name} not found, event: {event}")
        else:
            logger.warning(f"unknown event: {event}")


state = LocalSate(conf.notify_states)
