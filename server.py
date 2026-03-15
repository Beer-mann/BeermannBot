import io
import logging
import os
from contextlib import redirect_stdout

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from app import commands, handle_command

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="frontend/templates")
CORS(app)


@app.route("/")
def index():
    return render_template("index.html", project_name="BeermannBot")


@app.route("/commands")
def list_commands():
    return jsonify({"commands": sorted(commands.keys())})


@app.route("/run", methods=["POST"])
def run_command():
    data = request.get_json(silent=True) or {}
    cmd = data.get("command", "").strip()
    if not cmd:
        return jsonify({"error": "No command provided"}), 400
    logger.info("Running command: %s", cmd)
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            handle_command(cmd)
    except Exception as exc:
        logger.exception("Command %r raised an exception", cmd)
        return jsonify({"error": f"Command failed: {exc}"}), 500
    return jsonify({"output": buf.getvalue()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
