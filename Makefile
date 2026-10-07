PYTHON ?= .venv/bin/python
CXX = c++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Wpedantic -Werror
NOTE_DATE ?= 2026-10-07
.PHONY: check test lint types experiment purging-experiment manifest-experiment access-experiment fold-experiment ingestion-experiment calendar-audit calendar-experiment corporate-action-experiment membership-experiment terminal-experiment lagged-return-experiment cpp-savings cpp-check note
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

calendar-experiment:
	$(PYTHON) scripts/calendar_experiment.py

calendar-audit:
	$(PYTHON) scripts/calendar_contract_audit.py

corporate-action-experiment:
	$(PYTHON) scripts/corporate_action_experiment.py

membership-experiment:
	$(PYTHON) scripts/membership_experiment.py

terminal-experiment:
	$(PYTHON) scripts/terminal_experiment.py

lagged-return-experiment:
	$(PYTHON) scripts/lagged_return_experiment.py

SAVINGS_SRC = cpp/projects/savings_growth/savings.cpp
SAVINGS_HEADER = cpp/projects/savings_growth/savings.hpp

build/cpp/savings_growth/savings: cpp/projects/savings_growth/main.cpp $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(SAVINGS_SRC) -o $@

cpp-savings: build/cpp/savings_growth/savings
	./build/cpp/savings_growth/savings

.PHONY: cpp-text-years
build/cpp/savings_growth/text_vs_years: cpp/projects/savings_growth/text_vs_years.cpp $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(SAVINGS_SRC) -o $@

cpp-text-years: build/cpp/savings_growth/text_vs_years
	./build/cpp/savings_growth/text_vs_years

build/cpp/savings_growth/test_savings: cpp/projects/savings_growth/test_savings.cpp $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(SAVINGS_SRC) -o $@

.PHONY: cpp-conversion-contract
build/cpp/savings_growth/conversion_contract: cpp/projects/savings_growth/conversion_contract.cpp Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

cpp-conversion-contract: build/cpp/savings_growth/conversion_contract
	./build/cpp/savings_growth/conversion_contract

cpp-check: build/cpp/savings_growth/savings build/cpp/savings_growth/test_savings build/cpp/savings_growth/text_vs_years build/cpp/savings_growth/conversion_contract
	./build/cpp/savings_growth/test_savings
	./build/cpp/savings_growth/savings > build/cpp/savings_growth/actual.txt
	diff -u cpp/projects/savings_growth/expected.txt build/cpp/savings_growth/actual.txt
	./build/cpp/savings_growth/text_vs_years > build/cpp/savings_growth/text_vs_years_actual.txt
	diff -u cpp/projects/savings_growth/text_vs_years_expected.txt build/cpp/savings_growth/text_vs_years_actual.txt
	./build/cpp/savings_growth/conversion_contract > build/cpp/savings_growth/conversion_contract_actual.txt
	diff -u cpp/projects/savings_growth/conversion_contract_expected.txt build/cpp/savings_growth/conversion_contract_actual.txt

note:
	$(PYTHON) scripts/render_note.py research_log/$(NOTE_DATE).md reports/daily/$(NOTE_DATE)-learning-note.pdf
