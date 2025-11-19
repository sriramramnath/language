# Guide: Using LevLang in VS Code

This walkthrough doubles as a mini blog post for teams adopting LevLang inside VS Code.

## Install the Extension
1. Build the VSIX (optional): `npm install && npm run package` inside `vscode-levlang/`.
2. Install: `code --install-extension vscode-levlang/levlang.vsix`.
3. Reload VS Code; `.lvl` files now highlight automatically.

## Recommended Workspace Setup
- Open the repo folder.
- Pin the built-in terminal to run `levlang watch game.lvl`.
- Enable auto-save for instant feedback loops.

## Snippets & IntelliSense
- Type `playerblock` → scaffolds a `player { ... }` block.
- Type `component` → scaffolds a `component "Name" {}` skeleton.
- Hovering tokens displays runtime docs pulled from `docs/`.

## Debugging
- Use `levlang transpile` to generate Python, then run `Python: Current File` debug configuration.
- Set breakpoints inside the generated `.py` file for low-level troubleshooting.

## Bonus: Tasks
Add this to `.vscode/tasks.json` to run the current file:
```json
{
  "label": "Run LevLang",
  "type": "shell",
  "command": "levlang run ${file}"
}
```
Trigger via `Terminal → Run Task`.
