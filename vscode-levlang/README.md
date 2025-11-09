# LevLang for Visual Studio Code

Syntax highlighting and language support for LevLang (.lvl files).

## Features

- **Syntax Highlighting**: Full syntax highlighting for LevLang code
- **Auto-closing**: Automatic closing of brackets, quotes, and braces
- **Comment Support**: Line comments (`//`) and block comments (`/* */`)
- **Code Folding**: Fold code blocks for better organization
- **Smart Indentation**: Automatic indentation based on context

## Supported Syntax

### Keywords
- `game`, `player`, `enemy`, `road`, `ui`, `gameover`
- `sprite`, `scene`, `on`, `when`, `update`, `draw`
- `if`, `else`, `while`, `for`, `return`, `start`

### Properties
- `movement`, `speed`, `spawn`, `collide`, `offscreen`
- `lanes`, `scrolling`, `at`, `auto_fps`, `resizable`, `icon`

### Functions
- `rand()`, `random()`, `collides()`
- `draw_rect()`, `draw_circle()`, `draw_text()`
- `screen.fill()`, `start()`

### Values
- `wasd_arrows`, `arrows`, `wasd`
- `random_lane`, `random_top`, `gameover`, `destroy`
- `topleft`, `topright`, `center`, `bottomleft`, `bottomright`

## Installation

### From VSIX (Recommended)
1. Download the `.vsix` file from the releases
2. Open VSCode
3. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
4. Click the "..." menu at the top
5. Select "Install from VSIX..."
6. Choose the downloaded file

### From Source
1. Clone the repository
2. Copy the `vscode-levlang` folder to:
   - **Windows**: `%USERPROFILE%\.vscode\extensions`
   - **macOS/Linux**: `~/.vscode/extensions`
3. Restart VSCode

### Manual Installation
1. Open VSCode
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Developer: Install Extension from Location"
4. Select the `vscode-levlang` folder

## Usage

Once installed, any file with the `.lvl` extension will automatically use LevLang syntax highlighting.

### Example

```levlang
// Car Racing Game
game "Car Racing" auto_fps

player {
  movement: wasd_arrows
  speed: 7
}

enemy {
  spawn: random_lane
  speed: rand(3, 6)
  collide: gameover
}

spawn_rate: 2sec

ui {
  "Score: {score}" at topleft
}

start()
```

## Color Themes

The extension works with all VSCode color themes. For the best experience, we recommend:
- Dark themes: Dark+, Monokai, One Dark Pro
- Light themes: Light+, Solarized Light

## About LevLang

LevLang is a simplified game development language that transpiles to Python/pygame. 

- **Website**: [Coming Soon]
- **GitHub**: https://github.com/sriramramnath/language
- **Documentation**: https://github.com/sriramramnath/language/blob/main/README.md

## Release Notes

### 0.1.0
- Initial release
- Basic syntax highlighting
- Auto-closing pairs
- Comment support
- Code folding

## Contributing

Found a bug or want to contribute? Visit our [GitHub repository](https://github.com/sriramramnath/language).

## License

This extension is part of the LevLang project.

---

**Created by Levelium Inc.**
