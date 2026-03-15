import pytest

import server


@pytest.fixture()
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as c:
        yield c


def test_index_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"BeermannBot" in res.data


def test_list_commands_returns_known_commands(client):
    res = client.get("/commands")
    assert res.status_code == 200
    data = res.get_json()
    assert "commands" in data
    assert "help" in data["commands"]
    assert "hello" in data["commands"]
    assert data["commands"] == sorted(data["commands"])


def test_run_known_command(client):
    res = client.post("/run", json={"command": "hello"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["output"] == "Hello, world!\n"


def test_run_unknown_command_returns_output(client):
    res = client.post("/run", json={"command": "nonexistent"})
    assert res.status_code == 200
    data = res.get_json()
    assert "Unknown command" in data["output"]


def test_run_missing_command_returns_400(client):
    res = client.post("/run", json={})
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data


def test_run_empty_command_returns_400(client):
    res = client.post("/run", json={"command": "   "})
    assert res.status_code == 400


def test_run_version_command(client):
    res = client.post("/run", json={"command": "version"})
    assert res.status_code == 200
    data = res.get_json()
    assert "BeermannBot" in data["output"]
