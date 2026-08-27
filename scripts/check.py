#!/usr/bin/env python3
"""Validate the eza theme and exercise it via an isolated EZA_CONFIG_DIR."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "theme.yml"
RESTRICTED = "#665c54"
REQUIRED_SECTIONS = {"filekinds", "perms", "size", "users", "links", "git", "git_repo", "file_type"}
REQUIRED_FILE_KINDS = {"normal", "directory", "symlink", "pipe", "block_device", "char_device", "socket", "special", "executable", "mount_point"}


def run(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, text=True, capture_output=True, env=env)


def validate_static() -> None:
    text = THEME.read_text(encoding="utf-8")
    if RESTRICTED in text.lower():
        raise AssertionError(f"{RESTRICTED} is restricted to ANSI bright black")
    top = {match.group(1) for match in re.finditer(r"^([a-z_]+):(?:\s|$)", text, re.MULTILINE)}
    if not REQUIRED_SECTIONS <= top:
        raise AssertionError(f"missing eza sections: {sorted(REQUIRED_SECTIONS - top)}")
    block = text.split("filekinds:\n", 1)[1].split("\nperms:", 1)[0]
    kinds = {match.group(1) for match in re.finditer(r"^  ([a-z_]+):", block, re.MULTILINE)}
    if kinds != REQUIRED_FILE_KINDS:
        raise AssertionError(f"file-kind coverage mismatch: {sorted(REQUIRED_FILE_KINDS ^ kinds)}")
    if "filenames:" in text or "extensions:" in text:
        raise AssertionError("theme must not replace filename/extension mappings")


def validate_eza() -> None:
    executable = shutil.which("eza")
    if not executable:
        raise FileNotFoundError("eza")
    with tempfile.TemporaryDirectory(prefix="apollo-eza-") as temp:
        base = Path(temp)
        config = base / "config"
        files = base / "files"
        config.mkdir()
        (files / "folder").mkdir(parents=True)
        shutil.copy2(THEME, config / "theme.yml")
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
        expected = {
            "directory": "\x1b[1;38;2;131;165;152mfolder",
            "symlink": "\x1b[38;2;142;192;124mlink",
            "normal": "\x1b[38;2;207;188;151mplain",
            "executable": "\x1b[1;38;2;184;187;38mrun",
        }
        for kind, sequence in expected.items():
            if sequence not in result.stdout:
                raise AssertionError(f"eza output lacks Apollo {kind} style")
        override_env = env.copy()
        override_env["LS_COLORS"] = "di=38;2;251;73;52"
        overridden = run([executable, "--color=always", "--icons=never", "--classify=never", "--list-dirs", "-1", str(files / "folder")], override_env).stdout
        if "38;2;251;73;52" not in overridden:
            raise AssertionError("existing LS_COLORS did not retain precedence")


def main() -> int:
    run([sys.executable, str(ROOT / "scripts" / "generate.py"), "--check"])
    validate_static()
    if shutil.which("eza"):
        validate_eza()
        print("isolated eza schema, colors, and LS_COLORS precedence passed")
    else:
        print("eza not installed; native schema validation skipped")
    print("eza Apollo theme checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
