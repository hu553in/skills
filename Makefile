.DEFAULT_GOAL := check

PREK ?= prek
ACTIONLINT := bunx --minimum-release-age 259200 github-actionlint
RUFF := uvx --exclude-newer 3d ruff
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
	uv run --exclude-newer 3d --with pyyaml python -m unittest discover -s scripts

.PHONY: check-config
check-config:
	$(PREK) validate-config prek.toml
	DISABLE_TELEMETRY=1 bunx --minimum-release-age 259200 skills add . --list
	uvx --exclude-newer 3d check-jsonschema --schemafile https://skills.sh/schemas/skills.sh.schema.json skills.sh.json
	uv run --exclude-newer 3d --with pyyaml python scripts/check_skills.py

.PHONY: check-workflows
check-workflows:
	$(ACTIONLINT)

.PHONY: check
check: lint test check-config check-workflows

.PHONY: check-fix
check-fix: lint-fix
	$(MAKE) check
