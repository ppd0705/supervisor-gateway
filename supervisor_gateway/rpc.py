from typing import Dict
from typing import List
from typing import Tuple

from aiohttp_xmlrpc.client import ServerProxy
from aiohttp_xmlrpc.exceptions import ServerError


class Faults:
    UNKNOWN_METHOD = 1
    INCORRECT_PARAMETERS = 2
    BAD_ARGUMENTS = 3
    SIGNATURE_UNSUPPORTED = 4
    SHUTDOWN_STATE = 6
    BAD_NAME = 10
    BAD_SIGNAL = 11
    NO_FILE = 20
    NOT_EXECUTABLE = 21
    FAILED = 30
    ABNORMAL_TERMINATION = 40
    SPAWN_ERROR = 50
    ALREADY_STARTED = 60
    NOT_RUNNING = 70
    SUCCESS = 80
    ALREADY_ADDED = 90
    STILL_RUNNING = 91
    CANT_REREAD = 92


class RPC:
    def __init__(self, url: str):
        self.client = ServerProxy(url)

    async def close(self):
        await self.client.close()

    async def list_methods(self) -> List[str]:
        return await self.client.system.listMethods()

    async def get_state(self) -> Dict:
        state = await self.client.supervisor.getState()
        return state

    async def reread(self) -> Tuple[List[str], List[str], List[str]]:
        data = await self.client.supervisor.reloadConfig()
        added, changed, dropped = data[0]
        return added, changed, dropped

    async def get_all_process_info(self) -> List[Dict]:
        return await self.client.supervisor.getAllProcessInfo()

    async def get_process_info(self, name: str) -> bool:
        if ":" not in name:
            name = f"{name}:{name}"
        return await self.client.supervisor.getProcessInfo(name)

    async def start_process(self, name: str) -> bool:
        if ":" not in name:
            name = f"{name}:{name}"
        try:
            return await self.client.supervisor.startProcess(name)
        except ServerError as e:
            if e.code == Faults.ALREADY_STARTED:
                return True
            raise

    async def restart_process(self, name: str) -> bool:
        await self.stop_process(name)
        return await self.start_process(name)

    async def stop_process(self, name: str) -> bool:
        if ":" not in name:
            name = f"{name}:{name}"
        try:
            return await self.client.supervisor.stopProcess(name)
        except ServerError as e:
            if e.code == Faults.NOT_RUNNING:
                return True
            raise

    async def stop_process_group(self, name: str) -> bool:
        return await self.client.supervisor.stopProcessGroup(name)

    async def add_process_group(self, name: str) -> bool:
        try:
            return await self.client.supervisor.addProcessGroup(name)
        except ServerError as e:
            if e.code == Faults.ALREADY_ADDED:
                return True
            raise

    async def remove_process_group(self, name: str) -> bool:
        await self.stop_process_group(name)
        return await self.client.supervisor.removeProcessGroup(name)
