.DEFAULT_GOAL := check

PREK ?= prek
ACTIONLINT := bunx github-actionlint
RUFF := uvx ruff
PYTHON_FILES := scripts/*.py $(wildcard */scripts/*.py)

.PHONY: lint
lint:
	bun fmt --check
	$(RUFF) check $(PYTHON_FILES)
	$(RUFF) format --check $(PYTHON_FILES)

.PHONY: lint-fix
lint-fix:
	bun fmt
	$(RUFF) check --fix $(PYTHON_FILES)
	$(RUFF) format $(PYTHON_FILES)

.PHONY: test
test:
	uv run --with pyyaml python -m unittest discover -s scripts

.PHONY: check-config
check-config:
	$(PREK) validate-config prek.toml
	DISABLE_TELEMETRY=1 bunx skills add . --list
	uvx check-jsonschema --schemafile https://skills.sh/schemas/skills.sh.schema.json skills.sh.json
	uv run --with pyyaml python scripts/check_skills.py

.PHONY: check-renovate
check-renovate:
	bunx --package renovate renovate-config-validator --strict --no-global renovate.json

.PHONY: check-workflows
check-workflows:
	$(ACTIONLINT)

.PHONY: check
check: lint test check-config check-renovate check-workflows

.PHONY: check-fix
check-fix: lint-fix
	$(MAKE) check
