import runpy
import sys

import pytest

import app


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("hello", "Hello, world!\n"),
        ("goodbye", "Goodbye, world!\n"),
        (
            "help",
            "Available commands:\n"
            "- goodbye: Print a farewell message\n"
            "- hello: Print a greeting message\n"
            "- help: List all available commands\n"
            "- status: Show bot status\n"
            "- version: Show version information\n",
        ),
        ("version", "BeermannBot v1.0.0\n"),
        ("status", "Status: ok\n"),
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


def test_execute_command_returns_structured_result():
    result = app.execute_command("hello")

    assert result.command == "hello"
    assert result.ok is True
    assert result.output == "Hello, world!\n"
    assert result.exit_code == 0


def test_execute_command_reports_unknown_command():
    result = app.execute_command("missing")

    assert result.command == "missing"
    assert result.ok is False
    assert "Unknown command" in result.output
    assert result.exit_code == 1


def test_execute_command_empty_returns_exit_code_2():
    result = app.execute_command("")

    assert result.ok is False
    assert result.exit_code == 2
    assert "No command provided" in result.output


def test_execute_command_whitespace_returns_exit_code_2():
    result = app.execute_command("   ")

    assert result.ok is False
    assert result.exit_code == 2


def test_execute_command_normalizes_non_string_input():
    result = app.execute_command(123)

    assert result.command == "123"
    assert result.ok is False
    assert result.exit_code == 1
    assert result.output == "Unknown command: 123"


def test_main_without_command_prints_usage(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("app.py", run_name="__main__")

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Usage" in captured.out
    assert "Available commands" in captured.out


def test_main_with_command_dispatches(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py", "hello"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("app.py", run_name="__main__")

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"


def test_main_with_unknown_command_exits_nonzero(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py", "missing"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("app.py", run_name="__main__")

    assert exc_info.value.code == 1


def test_main_with_empty_command_preserves_exit_code(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py", "   "])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path("app.py", run_name="__main__")

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == "No command provided\n"
