 BeermannBot
===========

A command-line application with a web dashboard for running and managing bot commands.

Description
------------

BeermannBot is a Python CLI application with a Flask-powered web UI. It provides a simple
command registry pattern for dispatching named commands, with both a terminal interface and
a browser-based dashboard.

Installation
------------

1. Install Python 3.8 or higher.
2. Clone the repository:
   ```
   git clone https://github.com/Beer-mann/BeermannBot.git
   cd BeermannBot
   ```
3. Run setup to create the virtual environment and install dependencies:
   ```
   ./setup.sh
   ```

Usage
-----

**CLI mode:**
```
python app.py hello
python app.py goodbye
python app.py status
python app.py help
```

**Web UI mode:**
```
./run_ui.sh
```
Then open http://localhost:5011 in your browser. The port can be overridden with the `PORT` environment variable.

**Make targets:**
```
make setup   # install dependencies
make cli     # run help via CLI
make ui      # start web UI
make test    # run test suite
make smoke   # smoke-test the UI
```

Structure
---------

```
BeermannBot/
├── app.py                      # CLI entry point and command registry
├── server.py                   # Flask web server
├── frontend/
│   └── templates/
│       └── index.html          # Web dashboard template
├── tests/
│   ├── test_app.py             # Unit tests
│   └── test_no_todo_fixme.py   # Code quality guard
├── requirements.txt
├── Makefile
├── run_cli.sh
├── run_ui.sh
└── setup.sh
```

- `app.py` is the entry point for the CLI and contains the command registry.
- `server.py` runs the Flask web server that renders the dashboard.
- The `frontend/templates/` directory contains the Jinja2 HTML templates.
- `requirements.txt` lists all required Python packages.
