.DEFAULT_GOAL := check

PRETTIER := bunx prettier -u
ACTIONLINT := bunx github-actionlint
RUFF := uvx ruff
PYTHON_FILES := scripts/*.py

.PHONY: lint
lint:
	$(PRETTIER) -c .
	$(RUFF) check $(PYTHON_FILES)
	$(RUFF) format --check $(PYTHON_FILES)

.PHONY: lint-fix
lint-fix:
	$(PRETTIER) -w .
	$(RUFF) check --fix $(PYTHON_FILES)
	$(RUFF) format $(PYTHON_FILES)

.PHONY: check-config
check-config:
	git config --file .gitconfig --list >/dev/null
	DISABLE_TELEMETRY=1 bunx skills add . --list
	uvx check-jsonschema --schemafile https://skills.sh/schemas/skills.sh.schema.json skills.sh.json
	uv run --with pyyaml python -m unittest discover -s scripts
	uv run --with pyyaml python scripts/check_skills.py

.PHONY: check-workflows
check-workflows:
	$(ACTIONLINT)

.PHONY: check-renovate
check-renovate:
	bunx --package renovate renovate-config-validator --strict --no-global renovate.json

.PHONY: check
check: lint check-config check-renovate check-workflows

.PHONY: check-fix
check-fix: lint-fix
	$(MAKE) check
