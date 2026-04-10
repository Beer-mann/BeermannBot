from dataclasses import dataclass


@dataclass(frozen=True)
class CommandDescriptor:
    name: str
    description: str


@dataclass(frozen=True)
class CommandExecutionResponse:
    command: str
    ok: bool
    output: str
    exit_code: int
