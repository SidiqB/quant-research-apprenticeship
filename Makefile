PYTHON ?= .venv/bin/python
.PHONY: check test lint types experiment note
check: test lint types

test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m ruff check src tests scripts
	$(PYTHON) -m ruff format --check src tests scripts
types:
	$(PYTHON) -m mypy
experiment:
	$(PYTHON) scripts/availability_experiment.py
note:
	$(PYTHON) scripts/render_note.py research_log/2026-09-21.md reports/daily/2026-09-21-learning-note.pdf
