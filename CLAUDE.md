# eza Apollo theme development

- `palette/apollo.json` is the exact canonical snapshot. Update the pinned SHA-256 in `scripts/generate.py` only when deliberately refreshing it.
- Edit `scripts/generate.py`, not generated `theme.yml`.
- Target eza's current `theme.yml` schema. Do not add filename/extension mappings or reset users' LS_COLORS behavior without an explicit requirement.
- Generate: `python3 scripts/generate.py`
- Check static coverage and isolated installed-eza behavior: `python3 scripts/check.py`
- Test all: `python3 -m unittest discover -s tests -v`
- Single native test: `python3 -m unittest -v tests.test_theme.ApolloEzaThemeTests.test_isolated_eza_config_applies_theme_and_preserves_ls_colors`
