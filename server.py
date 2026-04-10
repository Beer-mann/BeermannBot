import logging
import os
from collections import deque
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from backend.commands import normalize_command
from backend.contract import build_service_contract
from backend.service import CommandService

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="frontend/templates")
app.config["COMMAND_HISTORY_LIMIT"] = 10
CORS(app)

command_history: deque[dict[str, object]] = deque(maxlen=app.config["COMMAND_HISTORY_LIMIT"])
command_service = CommandService()
PROJECT_NAME = "BeermannBot"


def status_code_for_result(exit_code: int) -> int:
    if exit_code == 0:
        return 200
    if exit_code == 2:
        return 400
    return 404


def serialize_command_history() -> list[dict[str, object]]:
    return list(command_history)


@app.route("/")
def index():
    return render_template("index.html", project_name=PROJECT_NAME)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/commands")
def list_commands():
    items = [
        {"name": spec.name, "description": spec.description}
        for spec in command_service.list_commands()
    ]
    return jsonify(
        {
            "commands": [item["name"] for item in items],
            "items": items,
        }
    )


@app.route("/history")
def history():
    return jsonify({"items": serialize_command_history()})


@app.route("/contract")
def contract():
    return jsonify(build_service_contract())


@app.route("/history/clear", methods=["DELETE"])
def clear_history():
    command_history.clear()
    return jsonify({"status": "ok", "message": "History cleared"})


@app.route("/run", methods=["POST"])
def run_command():
    data = request.get_json(silent=True) or {}
    cmd = data.get("command", "")
    logger.info("Running command: %s", cmd)

    result = command_service.execute(cmd)

    history_item = {
        "command": result.command or normalize_command(cmd),
        "ok": result.ok,
        "output": result.output,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    command_history.appendleft(history_item)

    payload = {
        "command": result.command,
        "ok": result.ok,
        "output": result.output,
        "exit_code": result.exit_code,
        "history": serialize_command_history(),
    }

    status_code = status_code_for_result(result.exit_code)
    if status_code == 200:
        return jsonify(payload)

    payload["error"] = result.output
    return jsonify(payload), status_code


@app.route("/api/health")
def legacy_api_health():
    return jsonify({"status": "ok", "project": PROJECT_NAME})


@app.route("/api/commands")
def legacy_api_commands():
    return list_commands()


@app.route("/api/command/<cmd>")
def legacy_api_run_command(cmd):
    logger.info("Running command via legacy route: %s", cmd)
    result = command_service.execute(cmd)
    return (
        jsonify(
            {
                "command": result.command,
                "known": result.ok,
                "ok": result.ok,
                "output": result.output.strip(),
                "exit_code": result.exit_code,
            }
        ),
        status_code_for_result(result.exit_code),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
