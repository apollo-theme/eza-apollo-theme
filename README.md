# Apollo for eza

A standalone `theme.yml` for eza's current theme schema. It covers core file kinds and metadata while leaving filename/extension mappings alone. Existing `LS_COLORS`, `EZA_COLORS`, and `EXA_COLORS` retain eza's normal override behavior.

Repository: https://github.com/apollo-theme/eza-apollo-theme

## Install

Clone without replacing `~/.config/eza/theme.yml` or any existing color variables:

```sh
git clone https://github.com/apollo-theme/eza-apollo-theme "$HOME/.config/eza-apollo-theme"
```

## Activate

Use Apollo once through an isolated config directory:

```sh
EZA_CONFIG_DIR="$HOME/.config/eza-apollo-theme" eza --color=always -la
```

Or opt in for the current shell with:

```sh
export EZA_CONFIG_DIR="$HOME/.config/eza-apollo-theme"
```

No existing eza configuration or `LS_COLORS` value is modified.

## Uninstall

```sh
unset EZA_CONFIG_DIR
rm -rf "$HOME/.config/eza-apollo-theme"
```

## Visual check

Run the activation command in a directory containing folders, executable files, symlinks, and ordinary files. Directories should be bold blue, executables bold green, symlinks cyan, and ordinary files warm beige. Existing `LS_COLORS` may intentionally override these file-kind colors.

## Development

The native check uses a temporary `EZA_CONFIG_DIR` and verifies both theme parsing and `LS_COLORS` precedence with eza v0.23.5 or newer.

```sh
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```
