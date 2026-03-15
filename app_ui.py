import io
import contextlib

from flask import Flask, jsonify, render_template

from app import commands, handle_command

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

PROJECT_NAME = "BeermannBot"


@app.route("/")
def index():
    return render_template("index.html", project_name=PROJECT_NAME)


@app.route("/api/commands")
def list_commands():
    return jsonify({"commands": sorted(commands.keys())})


@app.route("/api/command/<cmd>")
def run_command(cmd):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        handle_command(cmd)
    output = buf.getvalue()
    known = cmd in commands
    return jsonify({"command": cmd, "output": output.strip(), "known": known})


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
