PYTHON ?= .venv/bin/python
CXX = c++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Wpedantic -Werror
NOTE_DATE ?= 2026-09-28
.PHONY: check test lint types experiment purging-experiment manifest-experiment access-experiment fold-experiment ingestion-experiment calendar-audit cpp-savings cpp-check note
check: test lint types cpp-check

test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m ruff check src tests scripts
	$(PYTHON) -m ruff format --check src tests scripts
types:
	$(PYTHON) -m mypy
experiment:
	$(PYTHON) scripts/availability_experiment.py
purging-experiment:
	$(PYTHON) scripts/purging_experiment.py

manifest-experiment:
	$(PYTHON) scripts/manifest_experiment.py

access-experiment:
	$(PYTHON) scripts/access_experiment.py

fold-experiment:
	$(PYTHON) scripts/fold_experiment.py

ingestion-experiment:
	$(PYTHON) scripts/ingestion_experiment.py

calendar-audit:
	$(PYTHON) scripts/calendar_contract_audit.py

build/cpp/savings_growth/savings: cpp/projects/savings_growth/main.cpp Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

cpp-savings: build/cpp/savings_growth/savings
	./build/cpp/savings_growth/savings

cpp-check: build/cpp/savings_growth/savings
	./build/cpp/savings_growth/savings > build/cpp/savings_growth/actual.txt
	diff -u cpp/projects/savings_growth/expected.txt build/cpp/savings_growth/actual.txt

note:
	$(PYTHON) scripts/render_note.py research_log/$(NOTE_DATE).md reports/daily/$(NOTE_DATE)-learning-note.pdf
