from flask import Flask, jsonify, render_template

from app import execute_command, get_command_names

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

PROJECT_NAME = "BeermannBot"


@app.route("/")
def index():
    return render_template("index.html", project_name=PROJECT_NAME)


@app.route("/api/commands")
def list_commands():
    return jsonify({"commands": get_command_names()})


@app.route("/api/command/<cmd>")
def run_command(cmd):
    result = execute_command(cmd)
    status_code = 200 if result["known"] else 404
    return jsonify(result), status_code


@app.route("/api/health")
def healthcheck():
    return jsonify({"status": "ok", "project": PROJECT_NAME})


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
