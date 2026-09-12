import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import check_skills
from check_skills import load_frontmatter, require_text, validate_agent_metadata


class CatalogTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.enterContext(patch.object(check_skills, "ROOT", self.root))
        skill = self.root / "example"
        skill.mkdir()
        self.skill_file = skill / "SKILL.md"
        self.skill_file.write_text(
            "---\nname: example\ndescription: Example skill\n---\n# Example\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text(
            "- [`example`](example/SKILL.md)\n", encoding="utf-8"
        )
        self.write_groups(["example"])

    def write_groups(self, *groups):
        (self.root / "skills.sh.json").write_text(
            json.dumps({"groupings": [{"skills": group} for group in groups]}),
            encoding="utf-8",
        )

    def test_accepts_consistent_catalog(self):
        with redirect_stdout(StringIO()) as output:
            check_skills.main()
        self.assertEqual(output.getvalue(), "Validated 1 skills\n")

    def test_rejects_duplicate_slugs_across_groups(self):
        self.write_groups(["example"], ["example"])
        with self.assertRaisesRegex(ValueError, "duplicate skill slugs"):
            check_skills.main()

    def test_rejects_missing_and_unknown_slugs(self):
        for slugs, message in (
            ([], r"missing=\['example'\], unknown=\[\]"),
            (["example", "unknown"], r"missing=\[\], unknown=\['unknown'\]"),
        ):
            with self.subTest(slugs=slugs):
                self.write_groups(slugs)
                with self.assertRaisesRegex(ValueError, message):
                    check_skills.main()

    def test_rejects_mismatched_frontmatter_name(self):
        self.skill_file.write_text(
            "---\nname: other\ndescription: Example skill\n---\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "frontmatter name must be 'example'"):
            check_skills.main()

    def test_rejects_missing_readme_entry(self):
        (self.root / "README.md").write_text("# Skills\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "README.md does not list example"):
            check_skills.main()

    def test_rejects_empty_skill_catalog(self):
        self.skill_file.unlink()
        with self.assertRaisesRegex(ValueError, "no skills found"):
            check_skills.main()


class FrontmatterTests(unittest.TestCase):
    def test_preserves_separator_text_in_descriptions(self):
        descriptions = [
            ("Explain --- separators", "Explain --- separators"),
            ('"Explain --- separators"', "Explain --- separators"),
            ("'Explain --- separators'", "Explain --- separators"),
            (">-\n  Explain --- separators", "Explain --- separators"),
            ("|\n  Explain\n  ---\n  separators", "Explain\n---\nseparators\n"),
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            for description, expected in descriptions:
                with self.subTest(description=description):
                    path.write_text(
                        f"---\nname: example\ndescription: {description}\n---\n# Body\n",
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        load_frontmatter(path),
                        {"name": "example", "description": expected},
                    )

    def test_accepts_closing_delimiter_at_end_of_file_and_crlf(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_bytes(b"---\r\nname: example\r\n---")
            self.assertEqual(load_frontmatter(path), {"name": "example"})

    def test_rejects_missing_delimiters_and_non_mapping_metadata(self):
        cases = [
            ("name: example\n", ValueError, "missing YAML frontmatter"),
            ("---\nname: example\n", ValueError, "incomplete YAML frontmatter"),
            (
                "---\nname: example\n--- not a delimiter\n",
                ValueError,
                "incomplete YAML frontmatter",
            ),
            ("---\n- example\n---\n", TypeError, "frontmatter must be a mapping"),
            ("---\n---\n", TypeError, "frontmatter must be a mapping"),
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            for source, error_type, message in cases:
                with self.subTest(source=source):
                    path.write_text(source, encoding="utf-8")
                    with self.assertRaisesRegex(error_type, message):
                        load_frontmatter(path)


class MetadataTests(unittest.TestCase):
    def test_requires_non_empty_text(self):
        path = Path("SKILL.md")
        require_text("A useful description", path, "description")
        for value in (None, "", " \n", False, 42, ["text"], {"text": "value"}):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(
                    ValueError, "description must be a non-empty string"
                ),
            ):
                require_text(value, path, "description")

    def test_validates_agent_metadata_without_requiring_optional_fields(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "openai.yaml"
            for source in (
                "{}",
                "interface: {}",
                "interface:\n  display_name: Example",
            ):
                with self.subTest(source=source):
                    path.write_text(source, encoding="utf-8")
                    validate_agent_metadata(path)
            for source in ("", "[]", "interface: []", "interface: null"):
                with self.subTest(source=source):
                    path.write_text(source, encoding="utf-8")
                    with self.assertRaises(TypeError):
                        validate_agent_metadata(path)
            for field in ("display_name", "short_description", "default_prompt"):
                for value in ('" "', "null", "42", "true", "[text]", "{text: value}"):
                    with self.subTest(field=field, value=value):
                        path.write_text(
                            f"interface:\n  {field}: {value}\n", encoding="utf-8"
                        )
                        with self.assertRaisesRegex(ValueError, f"interface.{field}"):
                            validate_agent_metadata(path)
