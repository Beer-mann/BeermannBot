import sys
from typing import Callable

VERSION = "1.0.0"


def _show_help() -> None:
    available = sorted(k for k in commands)
    print("Available commands: " + ", ".join(available))


def _show_version() -> None:
    print(f"BeermannBot v{VERSION}")


commands: dict[str, Callable[[], None]] = {
    "hello": lambda: print("Hello, world!"),
    "goodbye": lambda: print("Goodbye, world!"),
    "status": lambda: print("BeermannBot is running."),
    "version": _show_version,
    "help": _show_help,
}


def handle_command(command: str) -> None:
    if command in commands:
        commands[command]()
    else:
        available = ", ".join(sorted(commands.keys()))
        print(f"Unknown command: {command}. Available: {available}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_command(sys.argv[1])
    else:
        print("No command provided")
