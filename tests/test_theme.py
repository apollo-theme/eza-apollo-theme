from __future__ import annotations

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
    def test_theme_is_deterministic_and_covers_core_file_kinds(self) -> None:
        self.assertEqual((ROOT / "theme.yml").read_text(), generate.render(generate.load_palette()))
        check.validate_static()

    @unittest.skipUnless(shutil.which("eza"), "eza is not installed")
    def test_isolated_eza_config_applies_theme_and_preserves_ls_colors(self) -> None:
        check.validate_eza()


if __name__ == "__main__":
    unittest.main()
