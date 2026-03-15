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
	bash -lc 'timeout 12s ./run_ui.sh >/tmp/BeermannBot_ui.log 2>&1 || true; tail -n 20 /tmp/BeermannBot_ui.log || true'
