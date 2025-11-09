# LevLang - Level Up Your Game Development

```
╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸
┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓
┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛ 
```

A simplified game development language that transpiles to Python/pygame.
Created by **Levelium Inc.**

## Overview

LevLang is a game development language that transpiles to Python/pygame, designed to make game creation accessible and fun. Write games with minimal code while maintaining the power of pygame underneath.

### Why LevLang?

**🎮 Two Syntax Styles for Every Skill Level:**
- **Simple Syntax**: Configuration-style blocks perfect for beginners and rapid prototyping
- **Advanced Syntax**: Full control with declarative sprites, scenes, and event handlers

**⚡ Fast Development:**
- Smart defaults reduce boilerplate
- Auto-generated game loops
- Built-in collision detection and input handling

**🔧 Powered by Pygame:**
- Compiles to clean, readable Python code
- Full pygame compatibility
- Easy to extend and customize

**🚀 Developer-Friendly:**
- Watch mode for instant feedback
- Clear error messages
- Comprehensive examples

## Quick Start

### Installation

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)

**Install LevLang:**

```bash
# Clone the repository
git clone https://github.com/sriramramnath/language.git
cd language

# Install in development mode
pip install -e .
```

This will install:
- The `levlang` command-line tool
- pygame (automatically installed as a dependency)

**Verify installation:**

```bash
levlang --version
```

You should see the LevLang banner with version information.

### Your First Game (Simple Syntax)

Create a file called `racing.lvl`:

```levlang
// Car Racing Game
game "Car Racing" resizable auto_fps

player {
  movement: wasd_arrows
  speed: 7
}

road {
  lanes: 3
  scrolling: true
}

enemy {
  spawn: random_lane
  speed: rand(3, 6)
  move: down
  offscreen: destroy, score+10
  collide: gameover
}

spawn_rate: 2sec

ui {
  "Score: {score}" at topleft
  "Move: WASD/Arrows" at topright
}

gameover {
  "GAME OVER!"
  "Score: {score}"
  "SPACE=Play  ESC=Quit"
}

start()
```

### Your First Game (Advanced Syntax)

Create a file called `hello.lvl`:

```levlang
game HelloGame {
    title = "My First Game"
    width = 800
    height = 600
}

sprite Player {
    x = 400
    y = 300
    speed = 5
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
        if key == "UP" {
            y = y - speed
        }
        if key == "DOWN" {
            y = y + speed
        }
    }
}

scene Main {
    player = Player()
    
    update {
        // Game logic here
    }
    
    draw {
        screen.fill((50, 50, 100))
        draw_rect((255, 200, 0), player.x - 25, player.y - 25, 50, 50)
    }
}
```

### Run Your Game

Transpile and run in one command:

```bash
levlang run racing.lvl
```

Or transpile to Python first:

```bash
levlang transpile racing.lvl -o racing.py
python racing.py
```

### Simple vs Advanced Syntax

**Simple Syntax** - Perfect for arcade games:
```levlang
game "My Game" auto_fps
player { movement: wasd_arrows, speed: 5 }
enemy { spawn: random, speed: 3, collide: gameover }
start()
```

**Advanced Syntax** - Full control:
```levlang
game MyGame { title = "My Game", width = 800 }
sprite Player { x = 400, on keydown(key) { ... } }
scene Main { update { ... }, draw { ... } }
```

Choose the style that fits your needs - or mix both!

## CLI Usage

The `levlang` command provides several modes of operation:

### Transpile Command

Convert a `.lvl` file to Python:

```bash
levlang transpile <input.lvl> -o <output.py>
```

Example:
```bash
levlang transpile game.lvl -o game.py
```

### Watch Mode

Automatically retranspile when the source file changes:

```bash
levlang watch <input.lvl> -o <output.py>
```

Example:
```bash
levlang watch game.lvl -o game.py
```

This is useful during development - keep this running in one terminal while you edit your game file, and it will automatically regenerate the Python code.

### Run Command

Transpile and execute in one step:

```bash
levlang run <input.lvl>
```

Example:
```bash
levlang run game.lvl
```

### Version

Check the transpiler version:

```bash
levlang --version
```

## Examples

The `examples/` directory contains sample games demonstrating various features:

### Car Racing (`examples/car_racing.lvl`)

A complete car racing game with lane-based movement and obstacle avoidance.

**Features:**
- 3-lane road system
- Random enemy spawning
- Score tracking
- Game over and restart

```bash
levlang run examples/car_racing.lvl
```

### Sprite Movement (`examples/sprite_movement.lvl`)

Basic player movement with WASD and arrow keys.

**Features:**
- Dual input support (WASD + Arrows)
- Position tracking
- Boundary checking

```bash
levlang run examples/sprite_movement.lvl
```

### Space Shooter (`examples/space_shooter.lvl`)

Classic space shooter with enemies and shooting mechanics.

**Features:**
- Top-down shooting
- Enemy spawning
- Collision detection
- Score system

```bash
levlang run examples/space_shooter.lvl
```

### Advanced Examples

For more complex examples using the advanced syntax, see:
- `examples/event_handling.lvl` - Mouse and keyboard event handling
- `examples/collision_detection.lvl` - Detailed collision system

## Language Features

### Simple Syntax Features

**Game Configuration:**
```levlang
game "My Game" resizable auto_fps
```

**Player Setup:**
```levlang
player {
  movement: wasd_arrows    // Supports WASD and arrow keys
  speed: 5
}
```

**Enemy/Obstacle Setup:**
```levlang
enemy {
  spawn: random_lane
  speed: rand(3, 6)
  move: down
  offscreen: destroy, score+10
  collide: gameover
}
```

**Road/Background:**
```levlang
road {
  lanes: 3
  scrolling: true
}
```

**UI Elements:**
```levlang
ui {
  "Score: {score}" at topleft
  "Lives: {lives}" at topright
}
```

**Game Over Screen:**
```levlang
gameover {
  "GAME OVER!"
  "Final Score: {score}"
  "Press SPACE to restart"
}
```

**Spawn Rate:**
```levlang
spawn_rate: 2sec  // Spawn enemies every 2 seconds
```

### Advanced Syntax Features

**Game Declaration:**
```levlang
game MyGame {
    title = "Game Title"
    width = 800
    height = 600
}
```

**Sprites:**
```levlang
sprite Enemy {
    x = 100
    y = 100
    health = 50
    speed = 3
    
    on keydown(key) {
        // Handle input
    }
}
```

**Scenes:**
```levlang
scene Main {
    player = Player()
    
    update {
        // Update game state
    }
    
    draw {
        // Render graphics
        screen.fill((0, 0, 0))
        player.draw()
    }
}
```

**Event Handlers:**
```levlang
on keydown(key) { }          // Key pressed
on keyup(key) { }            // Key released
on mousedown(button, mx, my) { }  // Mouse button pressed
on mouseup(button, mx, my) { }    // Mouse button released
on mousemove(mx, my) { }     // Mouse moved
```

## Documentation

For complete language syntax and features, see:
- [Language Syntax Documentation](docs/SYNTAX.md) - Complete syntax reference with examples

## Requirements

- Python 3.8+
- pygame 2.0+

## Project Structure

```
levlang/
├── core/           # Core data structures (AST, tokens, source location)
├── lexer/          # Tokenizer for advanced syntax
├── parser/         # Parsers (simple and advanced)
│   ├── parser.py         # Advanced declarative syntax parser
│   └── simple_parser.py  # Simple block-based syntax parser
├── semantic/       # Semantic analyzer
├── codegen/        # Code generators
│   ├── code_generator.py        # Advanced syntax generator
│   └── simple_generator.py      # Simple syntax generator
└── cli/            # Command-line interface
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=levlang

# Run specific test file
pytest tests/test_parser.py
```

### Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with details about the problem
2. **Suggest Features**: Share your ideas for new language features
3. **Submit Pull Requests**: Fix bugs or add features
4. **Improve Documentation**: Help make LevLang easier to learn
5. **Share Examples**: Create cool games and share them!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sriramramnath/language.git
cd language

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is open source. See LICENSE file for details.

## Credits

**Created by Levelium Inc.**

LevLang is built on top of:
- [Pygame](https://www.pygame.org/) - Python game development library
- Python 3.8+ - Programming language

## Support

- **Issues**: [GitHub Issues](https://github.com/sriramramnath/language/issues)
- **Discussions**: Share your games and get help
- **Documentation**: [Full Syntax Guide](docs/SYNTAX.md)

---

**Happy Game Development! 🎮**

Made with ❤️ by Levelium Inc.
