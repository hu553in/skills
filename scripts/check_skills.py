from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path}: incomplete YAML frontmatter") from error
    metadata = yaml.safe_load("\n".join(lines[1:end]) + "\n")
    if not isinstance(metadata, dict):
        raise TypeError(f"{path}: frontmatter must be a mapping")
    return metadata


def main() -> None:
    skill_files = sorted(ROOT.glob("*/SKILL.md"))
    skills = {path.parent.name for path in skill_files}
    if not skills:
        raise ValueError("no skills found")

    config = json.loads((ROOT / "skills.sh.json").read_text(encoding="utf-8"))
    grouped = [slug for group in config["groupings"] for slug in group["skills"]]
    if len(grouped) != len(set(grouped)):
        raise ValueError("skills.sh.json contains duplicate skill slugs")
    if set(grouped) != skills:
        raise ValueError(
            f"skills.sh.json mismatch: missing={sorted(skills - set(grouped))}, "
            f"unknown={sorted(set(grouped) - skills)}"
        )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for path in skill_files:
        slug = path.parent.name
        metadata = load_frontmatter(path)
        if metadata.get("name") != slug:
            raise ValueError(f"{path}: frontmatter name must be {slug!r}")
        if not metadata.get("description"):
            raise ValueError(f"{path}: frontmatter description is required")
        if f"[`{slug}`]" not in readme:
            raise ValueError(f"README.md does not list {slug}")

        agent_metadata = path.parent / "agents/openai.yaml"
        if agent_metadata.is_file():
            load_yaml(agent_metadata)

    print(f"Validated {len(skills)} skills")


if __name__ == "__main__":
    main()
