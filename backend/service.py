from backend.commands import execute_command, get_default_registry

from .models import CommandDescriptor, CommandExecutionResponse


class CommandService:
    """Thin backend service boundary around the command domain."""

    def list_commands(self) -> list[CommandDescriptor]:
        return [
            CommandDescriptor(name=spec.name, description=spec.description)
            for spec in get_default_registry().command_specs()
        ]

    def execute(self, command: object) -> CommandExecutionResponse:
        result = execute_command(command)
        return CommandExecutionResponse(
            command=result.command,
            ok=result.ok,
            output=result.output,
            exit_code=result.exit_code,
        )
