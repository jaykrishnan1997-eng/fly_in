UV := uv
MAIN := main.py
VENV := .venv
MAP ?= maps/medium/02_circular_loop.txt
PYTHON := python

.PHONY: install activate run debug clean fclean lint lint-strict

install:
	$(UV) sync
	@echo "Virtual environment ready: $(VENV)"

activate: install
	@SHELL_NAME=$$(basename "$$SHELL"); \
	if [ -f "$(VENV)/bin/activate.$$SHELL_NAME" ]; then \
		echo "Run: source $(VENV)/bin/activate.$$SHELL_NAME"; \
	else \
		echo "Run: source $(VENV)/bin/activate"; \
	fi

run: install
	$(UV) run $(PYTHON) $(MAIN) $(MAP)

debug: install
	$(UV) run $(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# used if u want to remove venv
fclean: clean
	rm -rf $(VENV)
# 	rm -f uv.lock

lint:
	$(UV) run flake8 . --exclude=.venv,venv
	$(UV) run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(UV) run flake8 . --exclude=.venv,venv
	$(UV) run mypy . --strict
