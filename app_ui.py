import os

from flask import Flask, jsonify, render_template

from app import APP_NAME, COMMAND_HISTORY, execute_command, list_commands


def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static",
    )

    @app.route("/")
    def index():
        return render_template("index.html", project_name=APP_NAME)

    @app.route("/api/commands")
    def commands():
        return jsonify({"commands": list_commands()})

    @app.route("/api/command/<command>")
    def run_command(command):
        result = execute_command(command)
        status_code = 200 if result["known"] else 404
        return jsonify(result), status_code

    @app.route("/api/history")
    def history():
        return jsonify({"history": list(COMMAND_HISTORY)})

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "project": APP_NAME})

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port)
