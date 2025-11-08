# Game Language Transpiler

A simplified game development language that transpiles to Python/pygame.

## Overview

Game Language provides an accessible syntax for game development that compiles to Python code using the pygame library. It reduces boilerplate while maintaining full pygame capabilities.

Write games with simplified syntax:
- Declarative sprite and scene definitions
- Built-in event handlers for keyboard and mouse input
- Automatic game loop generation
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

### Your First Game

Create a file called `hello.game`:

```
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
gamelang run hello.game
```

Or transpile to Python first:

```bash
gamelang transpile hello.game -o hello.py
python hello.py
```

## CLI Usage

The `gamelang` command provides several modes of operation:

### Transpile Command

Convert a `.game` file to Python:

```bash
gamelang transpile <input.game> -o <output.py>
```

Example:
```bash
gamelang transpile game.game -o game.py
```

### Watch Mode

Automatically retranspile when the source file changes:

```bash
gamelang watch <input.game> -o <output.py>
```

Example:
```bash
gamelang watch game.game -o game.py
```

This is useful during development - keep this running in one terminal while you edit your game file, and it will automatically regenerate the Python code.

### Run Command

Transpile and execute in one step:

```bash
gamelang run <input.game>
```

Example:
```bash
gamelang run game.game
```

### Version

Check the transpiler version:

```bash
gamelang --version
```

## Examples

The `examples/` directory contains sample games demonstrating various features:

### Sprite Movement (`examples/sprite_movement.game`)

Basic sprite creation and keyboard-based movement with boundary checking.

```bash
gamelang run examples/sprite_movement.game
```

### Event Handling (`examples/event_handling.game`)

Demonstrates keyboard and mouse event handlers including:
- Key press/release events
- Mouse click and drag
- Color changes based on input

```bash
gamelang run examples/event_handling.game
```

### Collision Detection (`examples/collision_detection.game`)

Shows sprite collision detection between player, collectibles, and enemies.

```bash
gamelang run examples/collision_detection.game
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
gamelang/
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
pytest --cov=gamelang
```
