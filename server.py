import io
import os
import sys
from contextlib import redirect_stdout

from flask import Flask, jsonify, render_template, request

sys.path.insert(0, os.path.dirname(__file__))
from app import commands, handle_command

app = Flask(__name__, template_folder="frontend/templates")


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
    buf = io.StringIO()
    with redirect_stdout(buf):
        handle_command(cmd)
    return jsonify({"output": buf.getvalue()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
