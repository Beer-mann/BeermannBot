import argparse
import sys
from dataclasses import dataclass
from typing import Callable

VERSION = "1.1.0"


@dataclass(frozen=True)
class CommandSpec:
    name: str
    description: str
    handler: Callable[[], None]


@dataclass(frozen=True)
class CommandResult:
    command: str
    ok: bool
    output: str
    exit_code: int


def _show_help() -> None:
    print("Available commands:")
    for spec in get_command_specs():
        print(f"- {spec.name}: {spec.description}")


def _show_version() -> None:
    print(f"BeermannBot v{VERSION}")


def _show_status() -> None:
    print("BeermannBot is running.")


commands: dict[str, CommandSpec] = {
    "goodbye": CommandSpec("goodbye", "Print a friendly sign-off.", lambda: print("Goodbye, world!")),
    "hello": CommandSpec("hello", "Print a friendly greeting.", lambda: print("Hello, world!")),
    "help": CommandSpec("help", "List all available commands.", _show_help),
    "status": CommandSpec("status", "Report the bot status.", _show_status),
    "version": CommandSpec("version", "Show the current BeermannBot version.", _show_version),
}


def get_command_specs() -> list[CommandSpec]:
    return sorted(commands.values(), key=lambda spec: spec.name)


def execute_command(command: str) -> CommandResult:
    normalized = command.strip()
    if not normalized:
        available = ", ".join(spec.name for spec in get_command_specs())
        return CommandResult(
            command="",
            ok=False,
            output=f"No command provided. Available: {available}",
            exit_code=2,
        )

    spec = commands.get(normalized)
    if spec is None:
        available = ", ".join(known.name for known in get_command_specs())
        return CommandResult(
            command=normalized,
            ok=False,
            output=f"Unknown command: {normalized}. Available: {available}",
            exit_code=1,
        )

    from contextlib import redirect_stdout
    import io

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.handler()
    return CommandResult(command=normalized, ok=True, output=buf.getvalue(), exit_code=0)


def handle_command(command: str) -> CommandResult:
    result = execute_command(command)
    if result.output:
        print(result.output, end="" if result.output.endswith("\n") else "\n")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run BeermannBot commands.",
        add_help=False,
    )
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("--list", action="store_true", dest="list_commands", help="List commands and exit")
    parser.add_argument("-h", "--help", action="store_true", dest="show_help", help="Show this help message")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.show_help:
        parser.print_help()
        print()
        handle_command("help")
        return 0

    if args.list_commands:
        handle_command("help")
        return 0

    if not args.command:
        result = handle_command("")
        return result.exit_code

    result = handle_command(args.command)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
