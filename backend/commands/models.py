from dataclasses import dataclass
from typing import Callable

CommandHandler = Callable[[], None]


@dataclass(frozen=True)
class CommandSpec:
    name: str
    description: str
    handler: CommandHandler


@dataclass(frozen=True)
class CommandResult:
    command: str
    ok: bool
    output: str
    exit_code: int
