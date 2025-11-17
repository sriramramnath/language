# Using the LevLang Command-Line Interface (CLI)

The `levlang` CLI is the primary tool for transpiling and running your games.

## Commands

### `run`
This is the most common command. It transpiles your `.lvl` file into a Python script and immediately runs it.

**Usage:**
```bash
levlang run <path_to_your_game>.lvl
```
**Example:**
```bash
levlang run useableexamples/pong.lvl
```
This command also supports the **level-chaining** feature. If a game ends and has a `next_level` property, the CLI will automatically load and run the next level file.

### `transpile`
This command only converts your `.lvl` file into a `.py` file without running it. This is useful if you want to inspect the generated Python code.

**Usage:**
```bash
levlang transpile <input_file>.lvl -o <output_file>.py
```
- `-o` or `--output` is optional. If omitted, the output file will have the same name as the input file, but with a `.py` extension.

**Example:**
```bash
levlang transpile pong.lvl -o my_pong_game.py
```

### `watch`
The watch command monitors your `.lvl` file for changes and automatically re-transpiles it whenever you save. This is useful for rapid development.

**Usage:**
```bash
levlang watch <file_to_watch>.lvl
```
Press `Ctrl+C` to stop watching.

### `--version`
Displays the current version of the LevLang CLI.
```bash
levlang --version
```
