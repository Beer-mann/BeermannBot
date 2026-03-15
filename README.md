 BeermannBot
===========

A simple command-dispatcher bot with a web UI and CLI interface.

Description
------------

BeermannBot is a Python application that exposes a registry of named commands
runnable from the command line or through a browser-based web UI backed by
Flask.

Installation
------------

```bash
./setup.sh        # creates .venv and installs dependencies
```

Usage
-----

**CLI**

```bash
./run_cli.sh hello      # prints "Hello, world!"
./run_cli.sh goodbye    # prints "Goodbye, world!"
```

**Web UI**

```bash
./run_ui.sh             # starts Flask on http://localhost:5011
```

Open `http://localhost:5011` in your browser.  Click any command chip or type
a command name and press **Run** / Enter to execute it live.

The UI also exposes a small REST API:

| Endpoint | Description |
|---|---|
| `GET /api/commands` | JSON list of all registered commands |
| `GET /api/command/<name>` | Execute a command and return its output as JSON |

Structure
---------

```
BeermannBot/
├── app.py                      # command registry + CLI entry point
├── app_ui.py                   # Flask web server
├── frontend/
│   └── templates/index.html    # browser UI
├── tests/
│   ├── test_app.py             # CLI / command-dispatch tests
│   └── test_no_todo_fixme.py   # code-quality guard
├── run_cli.sh                  # CLI launcher
├── run_ui.sh                   # UI launcher
├── setup.sh                    # virtualenv + dependency setup
└── requirements.txt
```

Adding Commands
---------------

Open `app.py` and add an entry to the `commands` dict:

```python
commands = {
    'hello':   lambda: print('Hello, world!'),
    'goodbye': lambda: print('Goodbye, world!'),
    'ping':    lambda: print('pong'),            # new command
}
```

The new command is immediately available in both the CLI and the web UI.

Running Tests
-------------

```bash
source .venv/bin/activate
pytest tests/
```
