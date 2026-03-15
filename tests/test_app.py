import json
import runpy
import sys

import pytest

import app


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("hello", "Hello, world!\n"),
        ("goodbye", "Goodbye, world!\n"),
        ("help", "Available commands:\n- goodbye: Print a farewell message.\n- hello: Print a greeting.\n- help: Show all available commands.\n- history: Show the most recent commands.\n- version: Show the application version.\n"),
    ],
)
def test_handle_command_runs_registered_command(command, expected_output, capsys):
    result = app.handle_command(command)

    captured = capsys.readouterr()

    assert captured.out == expected_output
    assert result is True


def test_handle_command_reports_unknown_command(capsys):
    result = app.handle_command("missing")

    captured = capsys.readouterr()

    assert captured.out == "Unknown command: missing\n"
    assert result is False


def test_execute_command_normalizes_case_and_whitespace():
    result = app.execute_command("  HELLO ")

    assert result == {
        "command": "hello",
        "known": True,
        "output": "Hello, world!",
    }


def test_execute_command_reports_empty_command():
    result = app.execute_command("   ")

    assert result == {
        "command": "",
        "known": False,
        "output": "No command provided",
    }


def test_history_command_returns_recent_runs():
    app.COMMAND_HISTORY.clear()

    app.execute_command("hello")
    app.execute_command("version")
    result = app.execute_command("history")

    assert result == {
        "command": "history",
        "known": True,
        "output": "Recent commands:\n- history\n- version\n- hello",
    }


def run_main(args, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py", *args])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("app.py", run_name="__main__")

    return exc_info.value.code, capsys.readouterr().out


def test_main_without_command_prints_usage(capsys, monkeypatch):
    exit_code, output = run_main([], capsys, monkeypatch)

    assert exit_code == 1
    assert "Usage" in output
    assert "Available commands" in output


def test_main_lists_commands_as_text(capsys, monkeypatch):
    exit_code, output = run_main(["--list"], capsys, monkeypatch)

    assert exit_code == 0
    assert output == "goodbye\nhello\nhelp\nhistory\nversion\n"


def test_main_lists_commands_as_json(capsys, monkeypatch):
    exit_code, output = run_main(["--list", "--json"], capsys, monkeypatch)

    assert exit_code == 0
    assert json.loads(output) == {
        "commands": [
            {"name": "goodbye", "description": "Print a farewell message."},
            {"name": "hello", "description": "Print a greeting."},
            {"name": "help", "description": "Show all available commands."},
            {"name": "history", "description": "Show the most recent commands."},
            {"name": "version", "description": "Show the application version."},
        ]
    }


def test_main_runs_command_as_json(capsys, monkeypatch):
    exit_code, output = run_main(["hello", "--json"], capsys, monkeypatch)

    assert exit_code == 0
    assert json.loads(output) == {
        "command": "hello",
        "known": True,
        "output": "Hello, world!",
    }


def test_main_reports_unknown_command_as_json(capsys, monkeypatch):
    exit_code, output = run_main(["missing", "--json"], capsys, monkeypatch)

    assert exit_code == 1
    assert json.loads(output) == {
        "command": "missing",
        "known": False,
        "output": "Unknown command: missing",
    }
