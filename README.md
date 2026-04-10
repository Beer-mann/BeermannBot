 BeermannBot
===========

A simple command-dispatcher bot with a web UI and CLI interface.

Description
------------

BeermannBot is a Python application that exposes a registry of named commands
runnable from the command line or through a browser-based web UI backed by
one canonical Flask API surface (`server.py`).

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
./run_cli.sh help       # prints all available commands with descriptions
```

**Web UI**

```bash
./run_ui.sh             # starts Flask on http://localhost:5011
```

Open `http://localhost:5011` in your browser.  Click any command chip or type
a command name and press **Run** / Enter to execute it live.

The UI also exposes a REST API:

| Endpoint | Description |
|---|---|
| `GET /commands` | JSON list of all registered commands plus descriptions |
| `POST /run` | Execute a command (`{"command":"hello"}`) and return output + history |
| `GET /history` | List recent command executions |
| `DELETE /history/clear` | Clear in-memory command history |
| `GET /health` | Simple healthcheck payload for monitoring/smoke tests |
| `GET /contract` | Canonical backend contract metadata |

Legacy compatibility routes under `/api/*` remain temporarily available for older clients.

Migration Notes
---------------

Canonical route changes:

| Legacy route | Canonical route | Compatibility |
|---|---|---|
| `GET /api/health` | `GET /health` | supported (deprecated) |
| `GET /api/commands` | `GET /commands` | supported (deprecated) |
| `GET /api/command/<name>` | `POST /run` with JSON body | supported (deprecated) |

Compatibility behavior:
- Legacy `/api/command/<name>` responses keep the previous shape (`known`, trimmed `output`) to avoid breaking older callers.
- Canonical `POST /run` responses preserve `app.py` command semantics, including normalization and exit-code mapping (`0 -> 200`, `2 -> 400`, `1 -> 404`).

Structure
---------

```
BeermannBot/
├── app.py                      # command registry + CLI entry point
├── server.py                   # canonical Flask runtime + API contract
├── app_ui.py                   # legacy compatibility entrypoint (imports server app)
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

Open `app.py` and add an entry to the `_commands` registry:

```python
_commands = {
    "hello": CommandSpec("hello", "Print a greeting message", lambda: print("Hello, world!")),
    "goodbye": CommandSpec("goodbye", "Print a farewell message", lambda: print("Goodbye, world!")),
    "help": CommandSpec("help", "List all available commands", lambda: print("Available commands...")),
    "ping": CommandSpec("ping", "Reply with pong", lambda: print("pong")),
}
```

The new command is immediately available in both the CLI and the web UI. Unknown
commands now return HTTP `404` from the API while preserving the CLI's non-zero
exit code behavior.

Running Tests
-------------

```bash
source .venv/bin/activate
pytest tests/
```

Release-Quality Gates
---------------------

Run the same local quality checks expected by CI:

```bash
make test     # full pytest suite
make smoke    # CLI + HTTP happy-path gate
```

`make smoke` executes `scripts/smoke.sh`, which:
- validates CLI dispatch via `./run_cli.sh hello`
- starts the Flask server and waits for `/health`
- verifies `POST /run` returns a successful `hello` response
