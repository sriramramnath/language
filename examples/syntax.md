# LevLang Syntax Reference

Complete syntax documentation for LevLang - a game development language that transpiles to Python/pygame.

---

## Table of Contents

1. [Overview](#overview)
2. [Three Syntax Modes](#three-syntax-modes)
3. [Block Syntax (Simple)](#block-syntax-simple)
4. [Component Syntax](#component-syntax)
5. [Advanced Syntax](#advanced-syntax)
6. [Comments](#comments)
7. [Data Types](#data-types)
8. [Common Properties](#common-properties)
9. [Examples](#examples)

---

## Overview

LevLang supports **three distinct syntax modes** to accommodate different skill levels and use cases:

- **Block Syntax**: Simple, declarative blocks for rapid prototyping
- **Component Syntax**: Reusable components with entity instances
- **Advanced Syntax**: Full programming language with sprites, scenes, and event handlers

You can choose the syntax that best fits your needs, or even mix them in certain cases!

---

## Three Syntax Modes

### Quick Comparison

```levlang
// 1. BLOCK SYNTAX - Simplest, direct declarations
game "My Game"
player { movement: arrows, speed: 5 }
enemy { spawn: random, speed: 3 }
start()

// 2. COMPONENT SYNTAX - Reusable blueprints
component "ship" { speed: 5, color: "blue" }
entities {
    player: "ship" { position: "center" }
}
game { title: "My Game" }

// 3. ADVANCED SYNTAX - Full control
game MyGame { title = "My Game", width = 800 }
sprite Player { x = 400, on keydown(key) { ... } }
scene Main { update { ... }, draw { ... } }
```

---

## Block Syntax (Simple)

The simplest way to create games. Define blocks with `key: value` properties.

### Game Declaration

```levlang
game "Game Title"
// or with properties:
game "Game Title" 800x600 resizable
```

### Custom Blocks

**Any identifier can be a block!** There are no reserved block names (except `ui`).

```levlang
player {
    shape: rectangle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
}

enemy {
    shape: circle
    color: red
    spawn: random
    speed: 3
    move: down
}

powerup {
    shape: star
    effect: invincibility
    duration: 5sec
}
```

### Property Syntax

```levlang
// Single property per line
key: value

// Multiple properties (inline)
key1: value1 key2: value2

// Nested blocks
parent {
    child {
        property: value
    }
}
```

### Special Blocks

#### UI Block

```levlang
ui {
    "Text to display" at topleft
    "Score: {score}" at topcenter offset 0,20
    "Lives: {lives}" at topright
}
```

Positions: `topleft`, `topcenter`, `topright`, `left`, `center`, `right`, `bottomleft`, `bottomcenter`, `bottomright`

#### GameOver Block

```levlang
gameover {
    "GAME OVER!"
    "Score: {score}"
    "Press SPACE to restart"
    on_key(SPACE): restart()
}
```

### Common Properties

```levlang
// Movement
movement: arrows          // Arrow keys
movement: wasd           // WASD keys
movement: wasd_arrows    // Both
movement: mouse_follow   // Follow mouse
movement: grid_arrows    // Grid-based movement

// Collision
on_collide: enemy: gameover
on_collide: coin: destroy, score+10

// Spawning
spawn: random            // Random position
spawn: random_lane       // Random lane
spawn: top_center        // Specific position
spawn_rate: 2sec        // Spawn every 2 seconds

// Physics
speed: 5                 // Movement speed
gravity: 0.5            // Gravity force
friction: 0.98          // Friction coefficient

// Appearance
shape: rectangle         // rectangle, circle, triangle, polygon
color: red              // Color name or hex
size: 40x40             // Width x Height
```

### Start Command

```levlang
start()  // Start the game
```

---

## Component Syntax

Reusable component definitions with entity instantiation.

### Component Definition

```levlang
component "name" {
    property: value
    property: value
}
```

Example:
```levlang
component "paddle" {
    shape: "rectangle"
    size: "15x100"
    speed: 7
    color: "white"
}

component "ball" {
    shape: "circle"
    size: "20x20"
    speed: 7
    color: "white"
}
```

### Entity Instantiation

```levlang
entities {
    instance_name: "component_name" {
        property: override_value
    }
}
```

Example:
```levlang
entities {
    player_paddle: "paddle" {
        position: "left(20)"
        controls: "vertical(\"w\", \"s\")"
    }

    opponent_paddle: "paddle" {
        position: "right(20)"
        controls: "ai_track(\"the_ball\")"
    }

    the_ball: "ball" {
        position: "center"
    }
}
```

### Game Configuration

```levlang
game {
    title: "Game Title"
    background: "black"
    width: 800
    height: 600
    
    on_event: "condition -> action"
    
    ui {
        display: "text at position"
    }
}
```

---

## Advanced Syntax

Full programming language with explicit control structures.

### Game Declaration

```levlang
game GameName {
    title = "Game Title"
    width = 800
    height = 600
}
```

### Sprite Declaration

```levlang
sprite SpriteName {
    // Properties
    x = 100
    y = 200
    speed = 5
    health = 100
    
    // Event handlers
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
    }
    
    on mousedown(button, mx, my) {
        // Handle mouse clicks
    }
}
```

### Scene Declaration

```levlang
scene SceneName {
    // Entity instances
    player = Player()
    enemy = Enemy()
    
    // Variables
    score = 0
    game_over = false
    
    // Update logic (runs every frame)
    update {
        if game_over == false {
            player.update()
            enemy.update()
        }
    }
    
    // Draw logic (runs every frame)
    draw {
        screen.fill((0, 0, 0))
        player.draw()
        enemy.draw()
        draw_text("Score: " + str(score), 10, 10, (255, 255, 255))
    }
}
```

### Event Handlers

```levlang
on keydown(key) {
    // Key pressed
}

on keyup(key) {
    // Key released
}

on mousedown(button, mx, my) {
    // Mouse button pressed
}

on mouseup(button, mx, my) {
    // Mouse button released
}

on mousemove(mx, my) {
    // Mouse moved
}
```

### Control Structures

#### If Statement

```levlang
if condition {
    // statements
}

if condition {
    // statements
} else {
    // statements
}
```

#### While Loop

```levlang
while condition {
    // statements
}
```

#### For Loop

```levlang
for variable in range(start, end) {
    // statements
}
```

### Expressions

#### Operators

```levlang
// Arithmetic
a + b    // Addition
a - b    // Subtraction
a * b    // Multiplication
a / b    // Division
a % b    // Modulo

// Comparison
a == b   // Equal
a != b   // Not equal
a < b    // Less than
a > b    // Greater than
a <= b   // Less than or equal
a >= b   // Greater than or equal

// Logical
a and b  // Logical AND
a or b   // Logical OR
not a    // Logical NOT
```

#### Member Access

```levlang
sprite.property
sprite.method()
```

#### Function Calls

```levlang
function(arg1, arg2)
```

### Built-in Functions

```levlang
// Drawing
screen.fill(color)
draw_rect(color, x, y, width, height)
draw_circle(color, x, y, radius)
draw_text(text, x, y, color)

// Collision
collides(sprite1, sprite2)

// Utility
random(min, max)
str(value)
int(value)
```

---

## Comments

```levlang
// Single-line comment

/*
   Multi-line comment
   spans multiple lines
*/
```

---

## Data Types

### Numbers

```levlang
42        // Integer
3.14      // Float
-10       // Negative
```

### Strings

```levlang
"double quotes"
'single quotes'
"with \"escapes\""
```

### Booleans

```levlang
true
false
```

### Colors

```levlang
"red"              // Color name
"#FF0000"          // Hex color
(255, 0, 0)        // RGB tuple (advanced syntax)
random             // Random color
```

### Sizes

```levlang
40x40              // Width x Height
100x20             // Simplified notation
```

### Time

```levlang
2sec               // 2 seconds
0.5sec             // Half second
1000ms             // 1000 milliseconds
```

### Positions

```levlang
// Named positions
center
top_center
bottom_center
left
right
topleft
topright
bottomleft
bottomright

// Offset positions
left(20)           // 20 pixels from left
right(100)         // 100 pixels from right
center             // Exact center

// Coordinates (advanced)
x = 100
y = 200
```

---

## Common Properties

### Movement Properties

```levlang
movement: arrows            // Arrow key control
movement: wasd             // WASD control
movement: wasd_arrows      // Both arrow and WASD
movement: horizontal       // Horizontal only
movement: vertical         // Vertical only
movement: mouse_follow     // Follow mouse cursor
movement: mouse_x          // Follow mouse X only
movement: grid_arrows      // Grid-based movement
movement: ai_chase         // AI chase player
movement: ai_track         // AI tracking
movement: patrol           // Patrol back and forth

controls: "w", "s"         // Custom key controls
controls: tap_jump         // Tap to jump
controls: rotate_thrust    // Rotation + thrust (Asteroids-style)

speed: 5                   // Movement speed
max_speed: 10             // Maximum speed
```

### Physics Properties

```levlang
physics: gravity           // Apply gravity
physics: platformer        // Platformer physics
gravity: 0.5              // Gravity force
friction: 0.98            // Friction coefficient
jump_force: 12            // Jump strength
double_jump: enabled      // Allow double jump
rotation: enabled         // Enable rotation
wrap_edges: true          // Wrap around screen edges
```

### Collision Properties

```levlang
on_collide: target: action
on_collide: enemy: gameover
on_collide: coin: destroy, score+10
on_collide: powerup: collect, power_mode(5sec)
collide: gameover         // Simplified collision
solid: true               // Solid object (can't pass through)
```

### Spawning Properties

```levlang
spawn: random             // Random position
spawn: random_lane        // Random lane
spawn: random_edge        // Random edge of screen
spawn: random_grid        // Random grid position
spawn: top_center         // Named position
spawn: corners            // At corners
spawn_rate: 2sec         // Spawn every 2 seconds
count: 5                  // Number of instances
```

### Visual Properties

```levlang
shape: rectangle          // Shape type
shape: circle
shape: triangle
shape: polygon

color: red               // Color
color: blue
color: random
color: "#FF0000"

size: 40x40              // Width x Height
animation: spin          // Animation type
animation: chomp
blink: true              // Blinking effect
trail: growing           // Leave a trail
```

### Behavior Properties

```levlang
move: up                 // Move direction
move: down
move: left
move: right
move: aimed_at_player    // Move toward player
move: wave_descend       // Wave pattern

behavior: bounce_angle   // Bounce at angles
behavior: bounce_on("paddle")
behavior: dive_attack    // Dive at player

offscreen: destroy       // Destroy when off-screen
offscreen: wrap          // Wrap to other side
offscreen: bounce        // Bounce back
offscreen: lose_life     // Player loses life

respawn: true            // Respawn after destruction
lifetime: 2sec           // Exist for 2 seconds
```

### Game State

```levlang
score: 0                 // Score variable
lives: 3                 // Lives count
level: 1                 // Current level
timer: 60                // Timer
game_over: false         // Game over flag
```

---

## Examples

### Minimal Game

```levlang
game "Minimal"
player { movement: arrows, speed: 5 }
start()
```

### Simple Collision Game

```levlang
game "Dodge"

player {
    shape: circle
    color: blue
    movement: wasd_arrows
    speed: 6
    on_collide: enemy: gameover
}

enemy {
    shape: rectangle
    color: red
    spawn: random
    move: down
    speed: 3
    offscreen: destroy, score+1
}

spawn_rate: 1sec

ui {
    "Score: {score}" at topleft
}

gameover {
    "GAME OVER!"
    "Score: {score}"
    "SPACE=Restart"
}

start()
```

### Component-Based Game

```levlang
component "ship" {
    shape: "triangle"
    size: "40x40"
    speed: 6
}

entities {
    player: "ship" {
        color: "green"
        position: "bottom_center"
        controls: "arrows"
    }
    
    enemy: "ship" {
        color: "red"
        position: "top_center"
        behavior: "move_down"
    }
}

game {
    title: "Space Battle"
    background: "black"
}
```

### Advanced Game with Sprites

```levlang
game SpaceShooter {
    title = "Space Shooter"
    width = 800
    height = 600
}

sprite Player {
    x = 400
    y = 500
    speed = 5
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
        if key == "SPACE" {
            shoot()
        }
    }
}

sprite Enemy {
    x = 100
    y = 100
    speed = 2
    
    update {
        y = y + speed
        if y > 600 {
            y = 0
        }
    }
}

scene Main {
    player = Player()
    enemies = [Enemy(), Enemy(), Enemy()]
    score = 0
    
    update {
        for enemy in enemies {
            enemy.update()
            if collides(player, enemy) {
                score = score - 10
            }
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
        for enemy in enemies {
            enemy.draw()
        }
        draw_text("Score: " + str(score), 10, 10, (255, 255, 255))
    }
}
```

---

## Best Practices

1. **Start Simple**: Use block syntax for quick prototypes
2. **Use Components**: When you need reusable entities
3. **Go Advanced**: When you need full control and complex logic
4. **Comment Your Code**: Explain game mechanics
5. **Test Incrementally**: Transpile and test frequently
6. **Descriptive Names**: Use clear, descriptive identifiers
7. **Organize Properties**: Group related properties together

---

## Tips & Tricks

### Variable Interpolation

Use `{variable}` in strings:
```levlang
"Score: {score}"
"Lives: {lives}"
"Level {level}"
```

### Color Shortcuts

```levlang
color: random           // Random color each time
color: red             // Named colors
color: "#FF0000"       // Hex colors
color: by_type         // Different color per type
```

### Multiple Actions

```levlang
on_collide: coin: destroy, score+10, play_sound("coin")
offscreen: destroy, score+5, spawn_new
```

### Positioning

```levlang
position: center              // Exact center
position: left(20)           // 20px from left edge
position: bottom_center      // Bottom center
position: random             // Random position
position: corners            // At all corners
```

---

## Error Messages

LevLang provides helpful error messages:

```
error: Invalid top-level statement: 'invalid code'
  --> game.lvl:4:1
   |
4 | invalid code
  ^^^^^^^^^^^^

1 error generated
```

---

## Next Steps

- Check out the [Guide](guide.md) for a beginner-friendly tutorial
- Explore the 10 example games in the `examples/` folder
- Read the [full documentation](../docs/) for advanced features
- Join the community to share your games!

---

**Made with ❤️ by Levelium Inc.**

