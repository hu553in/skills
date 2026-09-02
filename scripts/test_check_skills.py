import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from check_skills import load_frontmatter


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
