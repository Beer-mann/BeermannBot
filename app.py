import argparse
import io
import json
import sys
from collections import deque
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Callable


APP_NAME = "BeermannBot"
APP_VERSION = "1.0.0"
MAX_HISTORY = 10


@dataclass(frozen=True)
class CommandSpec:
    name: str
    description: str
    handler: Callable[[], None]


COMMAND_HISTORY = deque(maxlen=MAX_HISTORY)


def _cmd_hello():
    print("Hello, world!")


def _cmd_goodbye():
    print("Goodbye, world!")


def _cmd_help():
    print("Available commands:")
    for command in get_commands():
        print(f"- {command.name}: {command.description}")


def _cmd_version():
    print(f"{APP_NAME} {APP_VERSION}")


def _cmd_history():
    if not COMMAND_HISTORY:
        print("No commands have been run yet.")
        return

    print("Recent commands:")
    for item in COMMAND_HISTORY:
        print(f"- {item}")


COMMANDS = {
    "goodbye": CommandSpec("goodbye", "Print a farewell message.", _cmd_goodbye),
    "hello": CommandSpec("hello", "Print a greeting.", _cmd_hello),
    "help": CommandSpec("help", "Show all available commands.", _cmd_help),
    "history": CommandSpec("history", "Show the most recent commands.", _cmd_history),
    "version": CommandSpec("version", "Show the application version.", _cmd_version),
}


def normalize_command_name(command):
    if command is None:
        return ""
    return str(command).strip().lower()


def get_commands():
    return [COMMANDS[name] for name in sorted(COMMANDS)]


def get_command_names():
    return [command.name for command in get_commands()]


def list_commands():
    return [
        {"name": command.name, "description": command.description}
        for command in get_commands()
    ]


def execute_command(command):
    normalized = normalize_command_name(command)
    if not normalized:
        return {
            "command": "",
            "known": False,
            "output": "No command provided",
        }

    spec = COMMANDS.get(normalized)
    if spec is None:
        return {
            "command": normalized,
            "known": False,
            "output": f"Unknown command: {normalized}",
        }

    COMMAND_HISTORY.appendleft(normalized)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        spec.handler()

    return {
        "command": normalized,
        "known": True,
        "output": buffer.getvalue().strip(),
    }


def handle_command(command):
    result = execute_command(command)
    print(result["output"])
    return result["known"]


def build_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?")
    parser.add_argument("--list", action="store_true", dest="list_commands_flag")
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--help", action="store_true", dest="show_help")
    return parser


def _print_command_listing():
    for name in get_command_names():
        print(name)


def _print_usage():
    print("Usage: app.py <command> [--json]")
    print("       app.py --list [--json]")
    print(f"Available commands: {', '.join(get_command_names())}")


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.show_help:
        _print_usage()
        return 0

    if args.list_commands_flag:
        if args.json_output:
            print(json.dumps({"commands": list_commands()}))
        else:
            _print_command_listing()
        return 0

    if not args.command:
        message = {"error": "No command provided"} if args.json_output else None
        if args.json_output:
            print(json.dumps(message))
        else:
            _print_usage()
        return 1

    result = execute_command(args.command)
    if args.json_output:
        print(json.dumps(result))
    else:
        print(result["output"])
    return 0 if result["known"] else 1


if __name__ == "__main__":
    sys.exit(main())
