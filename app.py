import io
import sys
from contextlib import redirect_stdout


def cmd_hello():
    print("Hello, world!")


def cmd_goodbye():
    print("Goodbye, world!")


def cmd_help():
    print("Available commands:")
    for name in sorted(commands):
        print(f"- {name}")


commands = {
    "goodbye": cmd_goodbye,
    "hello": cmd_hello,
    "help": cmd_help,
}


def get_command_names():
    return sorted(commands)


def execute_command(command):
    handler = commands.get(command)
    if handler is None:
        return {
            "command": command,
            "known": False,
            "output": f"Unknown command: {command}",
        }

    buf = io.StringIO()
    with redirect_stdout(buf):
        handler()

    return {
        "command": command,
        "known": True,
        "output": buf.getvalue().strip(),
    }


def handle_command(command):
    result = execute_command(command)
    print(result["output"])
    return result["known"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ok = handle_command(sys.argv[1])
        sys.exit(0 if ok else 1)

    print("Usage: app.py <command>")
    print(f"Available commands: {', '.join(get_command_names())}")
    sys.exit(1)
