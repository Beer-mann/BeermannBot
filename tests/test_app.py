import runpy
import sys

import pytest

import app


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("hello", "Hello, world!\n"),
        ("goodbye", "Goodbye, world!\n"),
    ],
)
def test_handle_command_runs_registered_command(command, expected_output, capsys):
    app.handle_command(command)

    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_handle_command_reports_unknown_command(capsys):
    app.handle_command("missing")

    captured = capsys.readouterr()

    assert captured.out == "Unknown command: missing\n"


def test_main_without_command_prints_message(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py"])

    runpy.run_path("app.py", run_name="__main__")

    captured = capsys.readouterr()

    assert captured.out == "No command provided\n"


def test_main_with_command_dispatches(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["app.py", "hello"])

    runpy.run_path("app.py", run_name="__main__")

    captured = capsys.readouterr()

    assert captured.out == "Hello, world!\n"
