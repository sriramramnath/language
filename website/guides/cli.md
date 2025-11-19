# Guide: LevLang CLI in Practice

LevLang ships with a single command-line entry point: `levlang`. Below is a practical workflow you can reference or expand into a blog post.

## 1. Run an Example
```bash
levlang run useableexamples/pong.lvl
```
- Parses the `.lvl` file.
- Generates temporary Python.
- Launches pygame automatically.

## 2. Iterate Fast with Watch Mode
```bash
levlang watch game.lvl
```
- Watches the file for changes.
- Re-transpiles on save; close the pygame window to observe hot reloads.

## 3. Inspect Generated Python
```bash
levlang transpile game.lvl -o game.py
python3 game.py
```
Useful when debugging or when you want to ship a plain Python build.

## 4. Level Chaining
If your game prints `__NEXT_LEVEL__:path/to/next.lvl`, the CLI will auto-load it during `run`, letting you chain multiple `.lvl` files together.

## Tips
- Set `PYGAME_HIDE_SUPPORT_PROMPT=1` to silence pygame banners (already handled by the runtime, but helpful for custom scripts).
- Use `pip install -e .` for editable installs so CLI changes apply instantly.
