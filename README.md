# Game Language Transpiler

A simplified game development language that transpiles to Python/pygame.

## Overview

LevLang provides an accessible syntax for game development that compiles to Python code using the pygame library. It reduces boilerplate while maintaining full pygame capabilities.

LevLang supports two syntax styles:

**Simple Block-Based Syntax** (Recommended for beginners):
- Minimal, configuration-style syntax
- Smart defaults for common game patterns
- Perfect for simple arcade games

**Advanced Declarative Syntax**:
- Full control over sprites and scenes
- Custom event handlers
- Direct pygame access when needed

## Quick Start

### Installation

1. Install Python 3.8 or higher
2. Install the Game Language transpiler:

```bash
pip install -e .
```

3. Install pygame (if not already installed):

```bash
pip install pygame
```

For development:
```bash
pip install -e ".[dev]"
```

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
levlang run hello.lvl
```

Or transpile to Python first:

```bash
levlang transpile hello.lvl -o hello.py
python hello.py
```

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

### Sprite Movement (`examples/sprite_movement.lvl`)

Basic sprite creation and keyboard-based movement with boundary checking.

```bash
levlang run examples/sprite_movement.lvl
```

### Event Handling (`examples/event_handling.lvl`)

Demonstrates keyboard and mouse event handlers including:
- Key press/release events
- Mouse click and drag
- Color changes based on input

```bash
levlang run examples/event_handling.lvl
```

### Collision Detection (`examples/collision_detection.lvl`)

Shows sprite collision detection between player, collectibles, and enemies.

```bash
levlang run examples/collision_detection.lvl
```

## Language Features

### Game Declaration

Define your game window properties:

```
game MyGame {
    title = "Game Title"
    width = 800
    height = 600
}
```

### Sprites

Create game objects with properties and event handlers:

```
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

### Scenes

Define game scenes with update and draw logic:

```
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

### Event Handlers

Respond to user input:

```
on keydown(key) { }          // Key pressed
on keyup(key) { }            // Key released
on mousedown(button, mx, my) { }  // Mouse button pressed
on mouseup(button, mx, my) { }    // Mouse button released
on mousemove(mx, my) { }     // Mouse moved
```

### Built-in Functions

- `screen.fill(color)` - Fill screen with color
- `draw_rect(color, x, y, width, height)` - Draw rectangle
- `draw_circle(color, x, y, radius)` - Draw circle
- `draw_text(text, x, y, color)` - Draw text
- `collides(sprite1, sprite2)` - Check collision
- `random(min, max)` - Random number

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
├── lexer/          # Tokenizer
├── parser/         # Parser and AST builder
├── semantic/       # Semantic analyzer
├── codegen/        # Code generator
└── cli/            # Command-line interface
```

## Development

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=levlang
```
