import sys
from backend.commands import (
    VERSION,
    CommandResult,
    CommandSpec,
    execute_command as execute_domain_command,
    get_default_registry,
    normalize_command,
)


def get_command_names() -> list[str]:
    return get_default_registry().command_names()


def get_command_specs() -> list[CommandSpec]:
    return get_default_registry().command_specs()


def execute_command(command: object) -> CommandResult:
    return execute_domain_command(command, registry=get_default_registry())


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
