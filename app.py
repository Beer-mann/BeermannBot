import io
import sys
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Callable

VERSION = "1.0.0"


@dataclass
class CommandSpec:
    name: str
    description: str
    handler: Callable[[], None]


@dataclass
class CommandResult:
    command: str
    ok: bool
    output: str
    exit_code: int


def cmd_hello():
    print("Hello, world!")


def cmd_goodbye():
    print("Goodbye, world!")


def cmd_help():
    print("Available commands:")
    for spec in get_command_specs():
        print(f"- {spec.name}: {spec.description}")


def cmd_version():
    print(f"BeermannBot v{VERSION}")


def cmd_status():
    print("Status: ok")


_commands: dict[str, CommandSpec] = {
    "goodbye": CommandSpec("goodbye", "Print a farewell message", cmd_goodbye),
    "hello": CommandSpec("hello", "Print a greeting message", cmd_hello),
    "help": CommandSpec("help", "List all available commands", cmd_help),
    "status": CommandSpec("status", "Show bot status", cmd_status),
    "version": CommandSpec("version", "Show version information", cmd_version),
}


def get_command_names() -> list[str]:
    return sorted(_commands)


def get_command_specs() -> list[CommandSpec]:
    return [_commands[name] for name in sorted(_commands)]


def normalize_command(command: object) -> str:
    if command is None:
        return ""
    if isinstance(command, str):
        return command.strip()
    return str(command).strip()


def execute_command(command: object) -> CommandResult:
    cmd = normalize_command(command)

    if not cmd:
        return CommandResult(
            command="",
            ok=False,
            output="No command provided",
            exit_code=2,
        )

    spec = _commands.get(cmd)
    if spec is None:
        return CommandResult(
            command=cmd,
            ok=False,
            output=f"Unknown command: {cmd}",
            exit_code=1,
        )

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            spec.handler()
    except Exception as exc:
        return CommandResult(
            command=cmd,
            ok=False,
            output=f"Error executing '{cmd}': {exc}",
            exit_code=1,
        )

    return CommandResult(
        command=cmd,
        ok=True,
        output=buf.getvalue(),
        exit_code=0,
    )


def handle_command(command: str) -> bool:
    result = execute_command(command)
    output = result.output if result.output.endswith("\n") else result.output + "\n"
    sys.stdout.write(output)
    return result.ok


if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = execute_command(sys.argv[1])
        output = result.output if result.output.endswith("\n") else result.output + "\n"
        sys.stdout.write(output)
        sys.exit(result.exit_code)

    print("Usage: app.py <command>")
    print(f"Available commands: {', '.join(get_command_names())}")
    sys.exit(1)
