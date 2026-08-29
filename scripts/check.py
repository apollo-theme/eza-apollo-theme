#!/usr/bin/env python3
"""Validate both eza themes through isolated EZA_CONFIG_DIR values."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "dark": ROOT / "theme.yml",
    "light": ROOT / "light" / "theme.yml",
}
RESTRICTED_DARK = "#665c54"
REQUIRED_SECTIONS = {"filekinds", "perms", "size", "users", "links", "git", "git_repo", "file_type"}
REQUIRED_FILE_KINDS = {"normal", "directory", "symlink", "pipe", "block_device", "char_device", "socket", "special", "executable", "mount_point"}
EXPECTED = {
    "dark": {
        "directory": "\x1b[1;38;2;131;165;152mfolder",
        "symlink": "\x1b[38;2;142;192;124mlink",
        "normal": "\x1b[38;2;207;188;151mplain",
        "executable": "\x1b[1;38;2;184;187;38mrun",
    },
    "light": {
        "directory": "\x1b[1;38;2;7;102;120mfolder",
        "symlink": "\x1b[38;2;53;107;77mlink",
        "normal": "\x1b[38;2;60;56;54mplain",
        "executable": "\x1b[1;38;2;107;103;0mrun",
    },
}


def run(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, text=True, capture_output=True, env=env)


def variant_for_path(theme_path: Path) -> str:
    for variant, path in THEMES.items():
        if theme_path == path:
            return variant
    raise ValueError(f"unknown theme path: {theme_path}")


def validate_static(theme_path: Path = THEMES["dark"]) -> None:
    text = theme_path.read_text(encoding="utf-8")
    variant = variant_for_path(theme_path)
    if variant == "dark" and RESTRICTED_DARK in text.lower():
        raise AssertionError(f"{RESTRICTED_DARK} remains restricted in Apollo Dark")
    top = {match.group(1) for match in re.finditer(r"^([a-z_]+):(?:\s|$)", text, re.MULTILINE)}
    if not REQUIRED_SECTIONS <= top:
        raise AssertionError(f"missing eza sections: {sorted(REQUIRED_SECTIONS - top)}")
    block = text.split("filekinds:\n", 1)[1].split("\nperms:", 1)[0]
    kinds = {match.group(1) for match in re.finditer(r"^  ([a-z_]+):", block, re.MULTILINE)}
    if kinds != REQUIRED_FILE_KINDS:
        raise AssertionError(f"file-kind coverage mismatch: {sorted(REQUIRED_FILE_KINDS ^ kinds)}")
    if "filenames:" in text or "extensions:" in text:
        raise AssertionError("theme must not replace filename/extension mappings")


def validate_eza(variant: str = "dark") -> None:
    executable = shutil.which("eza")
    if not executable:
        raise FileNotFoundError("eza")
    with tempfile.TemporaryDirectory(prefix=f"apollo-eza-{variant}-") as temp:
        base = Path(temp)
        config = base / "config"
        files = base / "files"
        config.mkdir()
        (files / "folder").mkdir(parents=True)
        shutil.copy2(THEMES[variant], config / "theme.yml")
        (files / "plain").write_text("plain\n", encoding="utf-8")
        executable_file = files / "run"
        executable_file.write_text("#!/bin/sh\n", encoding="utf-8")
        executable_file.chmod(0o755)
        (files / "link").symlink_to("plain")
        env = os.environ.copy()
        env["EZA_CONFIG_DIR"] = str(config)
        env.pop("LS_COLORS", None)
        env.pop("EZA_COLORS", None)
        env.pop("EXA_COLORS", None)
        result = run([executable, "--color=always", "--icons=never", "--classify=never", "--sort=name", "-1", str(files)], env)
        for kind, sequence in EXPECTED[variant].items():
            if sequence not in result.stdout:
                raise AssertionError(f"eza {variant} output lacks Apollo {kind} style")
        for variable in ("LS_COLORS", "EZA_COLORS", "EXA_COLORS"):
            override_env = env.copy()
            override_env[variable] = "di=38;2;251;73;52"
            overridden = run(
                [executable, "--color=always", "--icons=never", "--classify=never", "--list-dirs", "-1", str(files / "folder")],
                override_env,
            ).stdout
            if "38;2;251;73;52" not in overridden:
                raise AssertionError(f"existing {variable} did not retain precedence")


def main() -> int:
    run([sys.executable, str(ROOT / "scripts" / "generate.py"), "--check"])
    for theme_path in THEMES.values():
        validate_static(theme_path)
    if shutil.which("eza"):
        for variant in THEMES:
            validate_eza(variant)
        print("both isolated eza config directories and color-variable precedence passed")
    else:
        print("eza not installed; native schema validation skipped")
    print("eza Apollo theme checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
