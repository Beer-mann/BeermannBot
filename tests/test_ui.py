import pytest

import app
import app_ui


@pytest.fixture()
def client():
    app.COMMAND_HISTORY.clear()
    flask_app = app_ui.create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_index_renders_available_commands(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "BeermannBot" in body
    assert 'data-command="hello"' not in body
    assert "Run Command" in body


def test_commands_endpoint_returns_metadata(client):
    response = client.get("/api/commands")

    assert response.status_code == 200
    assert response.get_json() == {
        "commands": [
            {"name": "goodbye", "description": "Print a farewell message."},
            {"name": "hello", "description": "Print a greeting."},
            {"name": "help", "description": "Show all available commands."},
            {"name": "history", "description": "Show the most recent commands."},
            {"name": "version", "description": "Show the application version."},
        ]
    }


def test_run_known_command(client):
    response = client.get("/api/command/hello")

    assert response.status_code == 200
    assert response.get_json() == {
        "command": "hello",
        "known": True,
        "output": "Hello, world!",
    }


def test_run_missing_command_returns_404(client):
    response = client.get("/api/command/missing")

    assert response.status_code == 404
    payload = response.get_json()
    assert payload["known"] is False
    assert "Unknown command" in payload["output"]


def test_run_empty_command_returns_404(client):
    response = client.get("/api/command/%20%20")

    assert response.status_code == 404
    assert response.get_json() == {
        "command": "",
        "known": False,
        "output": "No command provided",
    }


def test_run_version_command(client):
    response = client.get("/api/command/version")

    assert response.status_code == 200
    assert response.get_json() == {
        "command": "version",
        "known": True,
        "output": "BeermannBot 1.0.0",
    }


def test_history_returns_recent_runs(client):
    client.get("/api/command/hello")
    client.get("/api/command/version")

    response = client.get("/api/history")

    assert response.status_code == 200
    assert response.get_json() == {"history": ["version", "hello"]}


def test_health_returns_project_status(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "project": "BeermannBot"}
