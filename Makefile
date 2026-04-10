.PHONY: setup ui cli test smoke
setup:
	./setup.sh

ui:
	./run_ui.sh

cli:
	./run_cli.sh --help

test:
	[ -f .venv/bin/activate ] || ./setup.sh
	.venv/bin/python -m pytest tests/ -v

smoke:
	[ -f .venv/bin/activate ] || ./setup.sh
	./scripts/smoke.sh
