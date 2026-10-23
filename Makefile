PYTHON ?= .venv/bin/python
CXX = c++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Wpedantic -Werror
NOTE_DATE ?= 2026-10-10
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

YEARS_SRC = cpp/projects/savings_growth/years.cpp
YEARS_HEADER = cpp/projects/savings_growth/years.hpp

build/cpp/savings_growth/test_years: cpp/projects/savings_growth/test_years.cpp $(YEARS_SRC) $(YEARS_HEADER) $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(YEARS_SRC) $(SAVINGS_SRC) -o $@

build/cpp/savings_growth/parse_years_demo: cpp/projects/savings_growth/parse_years_demo.cpp $(YEARS_SRC) $(YEARS_HEADER) $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(YEARS_SRC) $(SAVINGS_SRC) -o $@

.PHONY: cpp-parse-years
cpp-parse-years: build/cpp/savings_growth/parse_years_demo
	./build/cpp/savings_growth/parse_years_demo

build/cpp/savings_growth/years_probe: cpp/projects/savings_growth/years_probe.cpp $(YEARS_SRC) $(YEARS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(YEARS_SRC) -o $@

.PHONY: cpp-years-oracle
cpp-years-oracle: build/cpp/savings_growth/years_probe
	$(PYTHON) scripts/years_boundary_oracle.py

FRACTIONAL_SRC = cpp/projects/savings_growth/fractional_failure.cpp

build/cpp/savings_growth/fractional-correct: $(FRACTIONAL_SRC) $(YEARS_SRC) $(YEARS_HEADER) $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< $(YEARS_SRC) $(SAVINGS_SRC) -o $@

build/cpp/savings_growth/fractional-wrong: $(FRACTIONAL_SRC) $(YEARS_SRC) $(YEARS_HEADER) $(SAVINGS_SRC) $(SAVINGS_HEADER) Makefile
	mkdir -p build/cpp/savings_growth
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -DWRONG_ADAPTER $< $(YEARS_SRC) $(SAVINGS_SRC) -o $@

.PHONY: cpp-fractional-failure
cpp-fractional-failure: build/cpp/savings_growth/fractional-correct build/cpp/savings_growth/fractional-wrong
	$(PYTHON) scripts/verify_fractional_failure.py

cpp-check: cpp-years-readiness cpp-fractional-failure cpp-years-oracle build/cpp/savings_growth/savings build/cpp/savings_growth/test_savings build/cpp/savings_growth/text_vs_years build/cpp/savings_growth/conversion_contract build/cpp/savings_growth/test_years build/cpp/savings_growth/parse_years_demo
	./build/cpp/savings_growth/test_savings
	./build/cpp/savings_growth/test_years
	./build/cpp/savings_growth/savings > build/cpp/savings_growth/actual.txt
	diff -u cpp/projects/savings_growth/expected.txt build/cpp/savings_growth/actual.txt
	./build/cpp/savings_growth/text_vs_years > build/cpp/savings_growth/text_vs_years_actual.txt
	diff -u cpp/projects/savings_growth/text_vs_years_expected.txt build/cpp/savings_growth/text_vs_years_actual.txt
	./build/cpp/savings_growth/conversion_contract > build/cpp/savings_growth/conversion_contract_actual.txt
	diff -u cpp/projects/savings_growth/conversion_contract_expected.txt build/cpp/savings_growth/conversion_contract_actual.txt
	./build/cpp/savings_growth/parse_years_demo > build/cpp/savings_growth/parse_years_actual.txt
	diff -u cpp/projects/savings_growth/parse_years_expected.txt build/cpp/savings_growth/parse_years_actual.txt

note:
	$(PYTHON) scripts/render_note.py research_log/$(NOTE_DATE).md reports/daily/$(NOTE_DATE)-learning-note.pdf

.PHONY: cpp-years-readiness
cpp-years-readiness:
	$(PYTHON) scripts/verify_years_readiness.py

build/cpp/portfolio_accounting/marked_wealth: cpp/projects/portfolio_accounting/marked_wealth.cpp Makefile
	mkdir -p build/cpp/portfolio_accounting
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

.PHONY: cpp-marked-wealth
cpp-marked-wealth: build/cpp/portfolio_accounting/marked_wealth
	$(PYTHON) scripts/verify_marked_wealth.py

cpp-check: cpp-marked-wealth

build/cpp/portfolio_accounting/buy_equations: cpp/projects/portfolio_accounting/buy_equations.cpp Makefile
	mkdir -p build/cpp/portfolio_accounting
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@

.PHONY: cpp-buy-equations
cpp-buy-equations: build/cpp/portfolio_accounting/buy_equations
	$(PYTHON) scripts/verify_buy_equations.py

cpp-check: cpp-buy-equations

.PHONY: cpp-account-state
cpp-account-state:
	$(PYTHON) scripts/verify_account_state.py

cpp-check: cpp-account-state

.PHONY: cpp-validated-buy
cpp-validated-buy:
	$(PYTHON) scripts/verify_validated_buy.py

cpp-check: cpp-validated-buy

.PHONY: cpp-buy-boundaries
cpp-buy-boundaries:
	$(PYTHON) scripts/verify_buy_boundaries.py

cpp-check: cpp-buy-boundaries

.PHONY: cpp-accounting-reproduce
cpp-accounting-reproduce:
	$(PYTHON) scripts/reproduce_accounting.py

cpp-check: cpp-accounting-reproduce

.PHONY: decision-timeline
decision-timeline:
	$(PYTHON) scripts/verify_decision_timeline.py

check: decision-timeline

.PHONY: event-contract
event-contract:
	$(PYTHON) scripts/verify_event_contract.py

check: event-contract
