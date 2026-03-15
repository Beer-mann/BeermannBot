import app


def test_execute_command_runs_registered_command():
    result = app.execute_command("hello")

    assert result.ok is True
    assert result.exit_code == 0
    assert result.output == "Hello, world!\n"


def test_handle_command_help_lists_commands(capsys):
    result = app.handle_command("help")

    captured = capsys.readouterr()

    assert result.ok is True
    for spec in app.get_command_specs():
        assert spec.name in captured.out
        assert spec.description in captured.out


def test_handle_command_reports_unknown_command(capsys):
    result = app.handle_command("missing")

    captured = capsys.readouterr()

    assert result.ok is False
    assert result.exit_code == 1
    assert captured.out.startswith("Unknown command: missing.")
    assert "Available:" in captured.out


def test_main_without_command_prints_message(capsys):
    exit_code = app.main([])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert captured.out.startswith("No command provided.")


def test_main_with_command_dispatches(capsys):
    exit_code = app.main(["hello"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Hello, world!\n"


def test_main_lists_commands(capsys):
    exit_code = app.main(["--list"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Available commands:" in captured.out
