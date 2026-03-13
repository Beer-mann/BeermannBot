BeermannBot
===========

BeermannBot is a small Python application that exposes a shared command registry through both a
CLI and a Flask web UI. The same commands can be executed locally from the terminal or remotely
through JSON endpoints.

Features
--------

- Command registry with reusable handlers
- CLI output in text or JSON
- Flask UI for browsing and executing commands
- JSON API for health checks and command execution
- Automated tests covering CLI and HTTP behavior

Requirements
------------

- Python 3.10 or newer

Setup
-----

1. Clone the repository:

   `git clone https://github.com/Beer-mann/BeermannBot.git`

2. Install dependencies:

   `./setup.sh`

CLI Usage
---------

- Run a command:

  `./run_cli.sh hello`

- List commands:

  `./run_cli.sh --list`

- Emit JSON:

  `./run_cli.sh hello --json`

Web UI
------

Start the Flask app:

`./run_ui.sh`

The default address is `http://127.0.0.1:5011`.

API Endpoints
-------------

- `GET /api/health`
- `GET /api/commands`
- `GET /api/commands/<command>`
- `POST /api/commands/<command>`

Testing
-------

Run the test suite with:

`python -m unittest discover -s tests`
