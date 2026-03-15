import pytest

import app_ui


@pytest.fixture()
def client():
    app_ui.app.config["TESTING"] = True
    with app_ui.app.test_client() as c:
        yield c


def test_index_renders_project_name(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"BeermannBot" in res.data


def test_list_commands_returns_json(client):
    res = client.get("/api/commands")
    assert res.status_code == 200
    data = res.get_json()
    assert "commands" in data
    assert "hello" in data["commands"]
    assert "goodbye" in data["commands"]
    assert "help" in data["commands"]
    assert data["commands"] == sorted(data["commands"])


def test_run_known_command(client):
    res = client.get("/api/command/hello")
    assert res.status_code == 200
    data = res.get_json()
    assert data["known"] is True
    assert data["output"] == "Hello, world!"


def test_run_unknown_command(client):
    res = client.get("/api/command/missing")
    assert res.status_code == 404
    data = res.get_json()
    assert data["known"] is False
    assert "missing" in data["output"]


def test_healthcheck_returns_ok(client):
    res = client.get("/api/health")

    assert res.status_code == 200
    assert res.get_json() == {"status": "ok", "project": "BeermannBot"}
