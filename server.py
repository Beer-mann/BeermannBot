import logging
import os
from collections import deque
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from app import execute_command, get_command_specs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="frontend/templates")
app.config["COMMAND_HISTORY_LIMIT"] = 10
CORS(app)

command_history: deque[dict[str, object]] = deque(maxlen=app.config["COMMAND_HISTORY_LIMIT"])


def serialize_command_history() -> list[dict[str, object]]:
    return list(command_history)


@app.route("/")
def index():
    return render_template("index.html", project_name="BeermannBot")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/commands")
def list_commands():
    items = [
        {"name": spec.name, "description": spec.description}
        for spec in get_command_specs()
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


@app.route("/run", methods=["POST"])
def run_command():
    data = request.get_json(silent=True) or {}
    cmd = data.get("command", "")
    logger.info("Running command: %s", cmd)

    try:
        result = execute_command(cmd)
    except Exception as exc:
        logger.exception("Command %r raised an exception", cmd)
        return jsonify({"error": f"Command failed: {exc}"}), 500

    history_item = {
        "command": result.command or cmd.strip(),
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

    if result.ok:
        return jsonify(payload)

    payload["error"] = result.output
    status_code = 400 if result.exit_code == 2 else 404
    return jsonify(payload), status_code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
