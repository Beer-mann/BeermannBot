from backend.commands import execute_command, get_default_registry


def test_default_registry_contains_expected_mvp_commands():
    registry = get_default_registry()

    assert registry.command_names() == [
        "goodbye",
        "hello",
        "help",
        "ping",
        "status",
        "time",
        "version",
    ]


def test_execute_command_parity_for_static_commands():
    cases = {
        "hello": "Hello, world!\n",
        "goodbye": "Goodbye, world!\n",
        "ping": "pong\n",
        "status": "Status: ok\n",
        "version": "BeermannBot v1.0.0\n",
    }

    for command, output in cases.items():
        result = execute_command(command)
        assert result.ok is True
        assert result.command == command
        assert result.exit_code == 0
        assert result.output == output


def test_execute_help_lists_all_registered_commands():
    result = execute_command("help")

    assert result.ok is True
    assert result.output.startswith("Available commands:\n")
    assert "- hello: Print a greeting message" in result.output
    assert "- goodbye: Print a farewell message" in result.output
    assert "- help: List all available commands" in result.output
    assert "- ping: Respond with pong" in result.output
    assert "- status: Show bot status" in result.output
    assert "- time: Show the current UTC time" in result.output
    assert "- version: Show version information" in result.output


def test_execute_time_returns_utc_suffix():
    result = execute_command("time")

    assert result.ok is True
    assert result.exit_code == 0
    assert result.output.endswith("UTC\n")
