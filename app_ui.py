import os

from flask import Flask, jsonify, render_template

from app import execute_command, get_command_specs

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

PROJECT_NAME = "BeermannBot"


@app.route("/")
def index():
    return render_template("index.html", project_name=PROJECT_NAME)


@app.route("/api/commands")
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


@app.route("/api/command/<cmd>")
def run_command(cmd):
    result = execute_command(cmd)
    status_code = 200 if result.ok else 400 if result.exit_code == 2 else 404
    return jsonify(
        {
            "command": result.command,
            "known": result.ok,
            "ok": result.ok,
            "output": result.output.strip(),
            "exit_code": result.exit_code,
        }
    ), status_code


@app.route("/api/health")
def healthcheck():
    return jsonify({"status": "ok", "project": PROJECT_NAME})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
