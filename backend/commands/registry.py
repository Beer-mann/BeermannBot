from .models import CommandSpec


class CommandRegistry:
    def __init__(self, commands: dict[str, CommandSpec] | None = None):
        self._commands: dict[str, CommandSpec] = dict(commands or {})

    def register(self, spec: CommandSpec) -> None:
        self._commands[spec.name] = spec

    def get(self, name: str) -> CommandSpec | None:
        return self._commands.get(name)

    def command_names(self) -> list[str]:
        return sorted(self._commands)

    def command_specs(self) -> list[CommandSpec]:
        return [self._commands[name] for name in sorted(self._commands)]
