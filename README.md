BeermannBot
===========

A small Python command-dispatcher with both a CLI and a Flask web UI.

Description
-----------

BeermannBot exposes a registry of named commands that can be executed from the
terminal or through a browser. The app now includes:

- structured command metadata
- JSON-friendly CLI output
- a Flask API and browser UI
- recent command history
- a small test suite that covers CLI and HTTP behavior

Installation
------------

```bash
./setup.sh
```

Usage
-----

CLI examples:

```bash
./run_cli.sh hello
./run_cli.sh version
./run_cli.sh --list
./run_cli.sh hello --json
```

Web UI:

```bash
./run_ui.sh
```

Then open `http://localhost:5011`.

HTTP API:

| Endpoint | Description |
| --- | --- |
| `GET /api/commands` | Return all commands with descriptions |
| `GET /api/command/<name>` | Execute a command |
| `GET /api/history` | Return recent command history |
| `GET /api/health` | Healthcheck payload |

Project Layout
--------------

```text
BeermannBot/
├── app.py
├── app_ui.py
├── frontend/templates/index.html
├── tests/test_app.py
├── tests/test_ui.py
├── run_cli.sh
├── run_ui.sh
└── setup.sh
```

Running Tests
-------------

```bash
source .venv/bin/activate
pytest -q
```
