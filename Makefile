
RUFF := $(shell command -v poetry >/dev/null 2>&1 && echo "poetry run ruff" || echo "python -m ruff")

.PHONY: fix format lint debug

fix:
	$(RUFF) check --fix . || true
	$(RUFF) format .

format:
	$(RUFF) format .

lint:
	$(RUFF) check .

debug:
	$(RUFF) check .
