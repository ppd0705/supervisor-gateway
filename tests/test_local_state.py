from supervisor_gateway.local_state import state


def test_clean():
    state.clean()
    assert not state.processes
    assert not state.supervisor


def test_update_state():
    state.clean()
    data = "RUNNING"
    state.update_supervisor(data)
    assert "state" in state.supervisor
    assert state.supervisor["state"] == data


def test_add_processes():
    state.clean()
    data = [
        {"name": "AAA", "statename": "RUNNING", "state": 20, "start": 1, "stop": 11},
        {"name": "BBB", "statename": "STARTING", "state": 10, "start": 2, "stop": 22},
        {"name": "CCC", "statename": "STOPPING", "state": 40, "start": 3, "stop": 33},
        {"name": "DDD", "statename": "STOPPED", "state": 0, "start": 4, "stop": 44},
    ]
    state.add_processes(data)
    assert len(state.processes) == len(data)
    assert sorted(state.processes) == [item["name"] for item in data]
    assert set(state.processes["AAA"]) == {"name", "state", "update_time"}
    assert sorted(item["update_time"] for item in state.processes.values()) == [
        1,
        2,
        33,
        44,
    ]


def test_state_event():
    state.clean()
    event = {"eventname": "SUPERVISOR_STATE_CHANGE_AAA"}
    state.event_handler(event)
    assert "state" in state.supervisor
    assert state.supervisor["state"] == event["eventname"].rsplit("_", 1)[1]


def test_process_event():
    state.clean()
    event = {
        "eventname": "PROCESS_STATE_BBB",
        "payload": {
            "processname": "aaa",
            "stop": 0,
        },
    }
    state.event_handler(event)
    assert len(state.processes) == 1
    assert "aaa" in state.processes
    _, info = state.processes.popitem()
    assert set(info) == {"name", "state", "from_state", "update_time"}
    assert info["state"] == "BBB"


def test_remove_process_event():
    state.clean()
    event = {
        "eventname": "PROCESS_GROUP_REMOVED",
        "payload": {
            "groupname": "aaa",
        },
    }
    state.event_handler(event)
    assert len(state.processes) == 0
    state.processes["aaa"] = {}
    assert len(state.processes) == 1
    state.event_handler(event)
    assert len(state.processes) == 0
