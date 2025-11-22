# LevLang

**A simplified game development language that transpiles to Python/Pygame**

LevLang is a domain-specific language designed for rapid game prototyping. Write game logic in a simple, declarative syntax and transpile it to clean Python/Pygame code.

## Features

- 🎮 **Simple Syntax** - Declarative blocks for game objects (player, enemies, etc.)
- 🐍 **Pure Pygame Mode** - Write raw Pygame code with `blockname[]` syntax
- ⚡ **Fast Iteration** - Watch mode for automatic re-transpilation
- 🎨 **Clean Output** - Generates readable Python code
- 🔧 **CLI Tools** - Run, transpile, and watch your games

## Installation

### Quick Install (One-liner)

```bash
curl -sSL https://raw.githubusercontent.com/sriramramnath/language/main/install.sh | bash
```

### From PyPI (Recommended)

```bash
pip install levlang
```

### From Source

```bash
git clone https://github.com/sriramramnath/language.git
cd language
pip install -e .
```

## Quick Start

### 1. Create a game file (e.g., `game.lvl`)

**Block Syntax:**
```levlang
game "My First Game"

player {
    speed: 5
    color: blue
}

start()
```

**Pygame Syntax:**
```levlang
game_loop[
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
]
```

### 2. Run your game

```bash
levlang run game.lvl
```

### 3. Transpile to Python

```bash
levlang transpile game.lvl -o game.py
python game.py
```

### 4. Watch mode for development

```bash
levlang watch game.lvl
```

## CLI Commands

- `levlang run <file.lvl>` - Transpile and run immediately
- `levlang transpile <file.lvl> -o <output.py>` - Transpile to Python
- `levlang watch <file.lvl>` - Auto-transpile on file changes
- `levlang --version` - Show version information

## Examples

Check out the `useableexamples/` directory for complete game examples:
- Pong
- Space Shooter
- Car Racing

## Requirements

- Python 3.8 or higher
- Pygame 2.0.0 or higher

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Links

- **GitHub**: https://github.com/sriramramnath/language
- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/sriramramnath/language/issues

## Credits

Created by Sriram Ramnath @ Levelium Inc.

