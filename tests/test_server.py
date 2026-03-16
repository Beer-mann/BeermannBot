import pytest

import server


@pytest.fixture(autouse=True)
def clear_history():
    server.command_history.clear()


@pytest.fixture()
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as c:
        yield c


def test_index_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"BeermannBot" in res.data


def test_health_returns_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_list_commands_returns_metadata(client):
    res = client.get("/commands")
    assert res.status_code == 200
    data = res.get_json()
    assert "commands" in data
    assert "items" in data
    assert data["commands"] == sorted(data["commands"])
    assert any(item["name"] == "help" for item in data["items"])
    assert all("description" in item for item in data["items"])


def test_run_known_command(client):
    res = client.post("/run", json={"command": "hello"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data["output"] == "Hello, world!\n"
    assert data["history"][0]["command"] == "hello"


def test_run_unknown_command_returns_404(client):
    res = client.post("/run", json={"command": "nonexistent"})
    assert res.status_code == 404
    data = res.get_json()
    assert data["ok"] is False
    assert "Unknown command" in data["error"]


def test_run_missing_command_returns_400(client):
    res = client.post("/run", json={})
    assert res.status_code == 400
    data = res.get_json()
    assert data["ok"] is False
    assert "No command provided" in data["error"]


def test_run_empty_command_returns_400(client):
    res = client.post("/run", json={"command": "   "})
    assert res.status_code == 400


def test_run_non_string_command_is_handled(client):
    res = client.post("/run", json={"command": 123})
    assert res.status_code == 404
    data = res.get_json()
    assert data["command"] == "123"
    assert data["ok"] is False
    assert data["error"] == "Unknown command: 123"


def test_run_version_command(client):
    res = client.post("/run", json={"command": "version"})
    assert res.status_code == 200
    data = res.get_json()
    assert "BeermannBot" in data["output"]


def test_history_returns_recent_runs(client):
    client.post("/run", json={"command": "hello"})
    client.post("/run", json={"command": "status"})

    res = client.get("/history")

    assert res.status_code == 200
    data = res.get_json()
    assert [item["command"] for item in data["items"]] == ["status", "hello"]
