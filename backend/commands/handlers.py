from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .registry import CommandRegistry

VERSION = "1.0.0"


def cmd_hello() -> None:
    print("Hello, world!")


def cmd_goodbye() -> None:
    print("Goodbye, world!")


def cmd_version() -> None:
    print(f"BeermannBot v{VERSION}")


def cmd_ping() -> None:
    print("pong")


def cmd_status() -> None:
    print("Status: ok")


def cmd_time() -> None:
    print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))


def make_help_handler(registry: "CommandRegistry"):
    def cmd_help() -> None:
        print("Available commands:")
        for spec in registry.command_specs():
            print(f"- {spec.name}: {spec.description}")

    return cmd_help
