# Guide: Contributing to LevLang

LevLang is open to community contributions—new syntax, runtime fixes, docs, you name it.

## 1. Fork & Clone
```bash
git clone https://github.com/<you>/language.git
cd language
pip install -e .
```

## 2. Run Tests
```bash
pytest tests/
```
(Add new cases when touching parser/runtime logic.)

## 3. Lint
- Use `ruff` or `flake8` if available.
- Keep files ASCII unless there’s a strong reason.

## 4. Branch & PR
```bash
git checkout -b feature/my-change
```
Push to your fork, open a PR against `main`, and include:
- Summary of changes
- Testing notes (`levlang run useableexamples/...`)
- Screenshots/GIFs when UI/runtime behaviour changes

## 5. Docs & Examples
When adding syntax/runtime capabilities, please update:
- `website/docs.md`
- `useableexamples/` or `examples/`
- `README.md` / `website/index.md` (if user-facing)

## Code Style
- Prefer data-driven solutions (parsers feed runtime tables).
- Avoid implicit defaults in the runtime—every behaviour should be opt-in via the `.lvl` file.

Thanks for helping Levelium keep LevLang vibrant! :rocket:
