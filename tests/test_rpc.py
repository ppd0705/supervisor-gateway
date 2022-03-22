import pytest
from aiohttp_xmlrpc.exceptions import ServerError

from supervisor_gateway.supervisor import Faults
from supervisor_gateway.xml_rpc import rpc


class FakeClient:
    def __getattr__(self, item):
        if item in ("system", "supervisor"):
            return self
        raise AttributeError(item)

    async def list_methods(self):
        return ["1", "2", "3"]

    async def get_state(self):
        return {"statename": "RNUNNING"}

    async def operate_process(self, name: str) -> bool:
        return True

    async def operate_null_process(self, name: str) -> bool:
        err = ServerError()
        err.code = Faults.BAD_NAME
        raise err

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_list_methods():
    rpc.client = FakeClient()
    rpc.client.listMethods = rpc.client.list_methods
    methods = await rpc.list_methods()
    assert isinstance(methods, list)


@pytest.mark.asyncio
async def test_operate_process():
    rpc.client = FakeClient()
    for action, format_action in (
        ("start_process", "startProcess"),
        ("stop_process", "stopProcess"),
        ("restart_process", "restartProcess"),
        ("start_process", "startProcess"),
        ("stop_process_group", "stopProcessGroup"),
        ("add_process_group", "addProcessGroup"),
    ):
        setattr(rpc.client, format_action, rpc.client.operate_null_process)
        if action != "restart_process":
            func = getattr(rpc, action)
            with pytest.raises(ServerError) as e:
                await func("aaa")
            assert e.value.code == Faults.BAD_NAME
        setattr(rpc.client, format_action, rpc.client.operate_process)
        func = getattr(rpc, action)
        ret = await func("aaa")
        assert ret is True

    await rpc.client.close()
