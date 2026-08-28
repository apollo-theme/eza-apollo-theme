<h1 align="center">eza Apollo Theme</h1>

<p align="center">Apollo gives eza warm, high-contrast file listings while preserving normal color-variable precedence.</p>

<p align="center">
  <a href="https://apollo-theme.github.io/#app-eza"><img alt="Preview" src="https://img.shields.io/badge/status-Preview-fabd2f?style=flat-square&labelColor=141617"></a>
  <a href="https://github.com/apollo-theme/eza-apollo-theme/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/apollo-theme/eza-apollo-theme/ci.yml?branch=main&style=flat-square&label=CI&labelColor=141617"></a>
  <a href="https://github.com/apollo-theme/eza-apollo-theme/releases/latest"><img alt="Latest Release" src="https://img.shields.io/github/v/release/apollo-theme/eza-apollo-theme?display_name=tag&sort=semver&style=flat-square&label=Release&color=d3869b&labelColor=141617"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-b8bb26?style=flat-square&labelColor=141617"></a>
  <a href="https://github.com/eza-community/eza"><img alt="eza 0.23.5 or newer" src="https://img.shields.io/badge/eza-0.23.5%2B-83a598?style=flat-square&labelColor=141617"></a>
  <a href="palette/apollo.json"><img alt="Canonical Apollo palette" src="https://img.shields.io/badge/palette-canonical-8ec07c?style=flat-square&labelColor=141617"></a>
</p>

<p align="center">
  <a href="https://apollo-theme.github.io/#app-eza"><img src="https://raw.githubusercontent.com/apollo-theme/apollo-theme.github.io/main/previews/eza.svg" alt="Simulated eza Apollo Theme preview"></a>
</p>
<p align="center"><em>Simulated preview. File metadata, terminal rendering, and color-variable overrides may vary.</em></p>

Apollo ships as a standalone `theme.yml` for eza's current theme schema. It styles core file kinds, permissions, sizes, users, links, Git state, and metadata without replacing filename or extension mappings.

## Install

Clone Apollo into its own directory without replacing `~/.config/eza/theme.yml` or changing existing color variables:

```sh
git clone https://github.com/apollo-theme/eza-apollo-theme "$HOME/.config/eza-apollo-theme"
```

## Activate

Use Apollo once through an isolated config directory:

```sh
EZA_CONFIG_DIR="$HOME/.config/eza-apollo-theme" eza --color=always -la
```

Or opt in for the current shell:

```sh
export EZA_CONFIG_DIR="$HOME/.config/eza-apollo-theme"
```

No existing eza configuration or `LS_COLORS` value is modified. Existing `LS_COLORS`, `EZA_COLORS`, and `EXA_COLORS` keep eza's normal precedence and may intentionally override Apollo's file-kind colors.

## Uninstall

```sh
unset EZA_CONFIG_DIR
rm -rf "$HOME/.config/eza-apollo-theme"
```

## Visual check

Run the activation command in a directory containing folders, executable files, symlinks, and ordinary files. Directories should be bold blue, executables bold green, symlinks cyan, and ordinary files warm beige. Existing `LS_COLORS` may intentionally override these file-kind colors.

## Development

The native check uses a temporary `EZA_CONFIG_DIR` and verifies theme parsing, rendered file kinds, and `LS_COLORS` precedence with eza v0.23.5 or newer.

```sh
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

`theme.yml` is deterministic generated output. Make mapping changes in `scripts/generate.py`, then regenerate rather than editing the theme directly.

## License

[MIT](LICENSE)
