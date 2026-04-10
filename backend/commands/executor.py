import io
from contextlib import redirect_stdout

from .defaults import get_default_registry
from .models import CommandResult
from .registry import CommandRegistry
from .validation import normalize_command


def execute_command(command: object, registry: CommandRegistry | None = None) -> CommandResult:
    selected_registry = registry or get_default_registry()
    cmd = normalize_command(command)

    if not cmd:
        return CommandResult(
            command="",
            ok=False,
            output="No command provided",
            exit_code=2,
        )

    spec = selected_registry.get(cmd)
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
