from __future__ import annotations

import hashlib
import importlib.util
import shutil
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate = load_module("eza_generate", ROOT / "scripts" / "generate.py")
check = load_module("eza_check", ROOT / "scripts" / "check.py")


class ApolloEzaThemeTests(unittest.TestCase):
    def test_both_variants_are_deterministic_and_cover_core_file_kinds(self) -> None:
        self.assertEqual(
            hashlib.sha256((ROOT / "palette" / "apollo-light.json").read_bytes()).hexdigest(),
            "b0dbdeb719ed1931c424e9590562689325ecac1609e2fed6406ec5c4d3dc5763",
        )
        expected = generate.render_outputs()
        self.assertEqual(set(expected), {ROOT / "theme.yml", ROOT / "light" / "theme.yml"})
        for path, text in expected.items():
            self.assertEqual(path.read_text(encoding="utf-8"), text)
            check.validate_static(path)

    def test_native_precedence_check_covers_all_supported_color_variables(self) -> None:
        source = (ROOT / "scripts" / "check.py").read_text(encoding="utf-8")
        self.assertIn('(\"LS_COLORS\", \"EZA_COLORS\", \"EXA_COLORS\")', source)

    @unittest.skipUnless(shutil.which("eza"), "eza is not installed")
    def test_isolated_eza_config_applies_both_variants_and_preserves_color_precedence(self) -> None:
        for variant in ("dark", "light"):
            with self.subTest(variant=variant):
                check.validate_eza(variant)


if __name__ == "__main__":
    unittest.main()
