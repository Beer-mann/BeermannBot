import argparse
import json
import os
import sys
from typing import Callable

from flask import Flask, jsonify, render_template


CommandHandler = Callable[[], str]


def _message_handler(message: str) -> CommandHandler:
    return lambda: message


commands: dict[str, CommandHandler] = {
    "hello": _message_handler("Hello, world!"),
    "goodbye": _message_handler("Goodbye, world!"),
}


def available_commands() -> list[str]:
    return sorted(commands)


def run_command(command: str) -> str:
    handler = commands.get(command.lower())
    if handler is None:
        raise KeyError(command)
    return handler()


def handle_command(command: str) -> int:
    try:
        print(run_command(command))
        return 0
    except KeyError:
        print(f"Unknown command: {command}")
        return 1


def create_app() -> Flask:
    app = Flask(__name__, template_folder="frontend/templates")

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            project_name="BeermannBot",
            commands=available_commands(),
        )

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "commands": available_commands()})

    @app.get("/api/commands")
    def list_commands():
        return jsonify({"commands": available_commands()})

    @app.route("/api/commands/<command>", methods=["GET", "POST"])
    def execute_command(command: str):
        try:
            output = run_command(command)
        except KeyError:
            return jsonify({"error": f"Unknown command: {command}"}), 404
        return jsonify({"command": command.lower(), "output": output})

    return app


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run BeermannBot commands.")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_commands",
        help="List available commands",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit machine-readable JSON",
    )
    return parser


def build_serve_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the BeermannBot web UI.")
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "5011")))
    parser.add_argument("--debug", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args and args[0] == "serve":
        serve_args = build_serve_parser().parse_args(args[1:])
        create_app().run(host=serve_args.host, port=serve_args.port, debug=serve_args.debug)
        return 0

    parsed = build_cli_parser().parse_args(args)

    if parsed.list_commands:
        payload = {"commands": available_commands()}
        print(json.dumps(payload) if parsed.as_json else "\n".join(payload["commands"]))
        return 0

    if not parsed.command:
        print("No command provided")
        return 1

    if parsed.as_json:
        try:
            output = run_command(parsed.command)
        except KeyError:
            print(json.dumps({"error": f"Unknown command: {parsed.command}"}))
            return 1
        print(json.dumps({"command": parsed.command.lower(), "output": output}))
        return 0

    return handle_command(parsed.command)


if __name__ == "__main__":
    raise SystemExit(main())
