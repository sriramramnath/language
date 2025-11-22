# LevLang Syntax Reference

Complete reference for LevLang block syntax, including all features, defaults, and automatic behaviors.

## Table of Contents

1. [Basic Structure](#basic-structure)
2. [Block Properties](#block-properties)
3. [Collision Detection](#collision-detection)
4. [Random Values](#random-values)
5. [Spawning System](#spawning-system)
6. [Game Over Overlay](#game-over-overlay)
7. [Default Values](#default-values)
8. [Automatic Behaviors](#automatic-behaviors)
9. [Complete Examples](#complete-examples)

---

## Basic Structure

Every LevLang game has this basic structure:

```levlang
game "My Game Title"

player {
    // player properties
}

// other blocks...

start()
```

### Top-Level Commands

- `game "Title"` - Sets the game window title
- `start()` - Must be at the end to start the game

---

## Block Properties

### Position Properties

```levlang
blockname {
    x: 400                    // X coordinate (pixels from left)
    y: 300                    // Y coordinate (pixels from top)
    start_position: center    // Or: top_left, top_center, top_right,
                             //     bottom_left, bottom_center, bottom_right
}
```

**Defaults:**
- If `x` or `y` is provided, the block spawns at that exact position
- If neither is provided, `start_position` defaults to `center`

### Visual Properties

```levlang
blockname {
    color: blue          // Named colors: red, blue, green, cyan, magenta,
                        //   yellow, orange, purple, white, black, gray
    color: #FF5733      // Hex colors
    size: 50            // Single number = square (50x50)
    size: 50x30         // Width x Height
    shape: rectangle    // Or: circle, script, viewport, overlay
}
```

**Defaults:**
- `color`: white
- `size`: 48x48
- `shape`: rectangle

### Movement Properties

```levlang
blockname {
    speed: 5                // Movement speed (pixels per frame)
    speed: rand(3, 8)       // Random speed between 3 and 8
    
    controls: arrows        // Player control with arrow keys
    controls: wasd          // Player control with WASD keys
    controls: horizontal    // Only left/right movement
    controls: vertical      // Only up/down movement
    
    direction: down         // Automatic movement: down, up, left, right
}
```

**Defaults:**
- `speed`: 0 (no movement)
- `controls`: none (not player-controlled)
- `direction`: none (doesn't auto-move)

**Important:** Blocks need BOTH `speed` AND (`controls` OR `direction`) to actually move!

### Lane System

```levlang
viewport {
    lane_lock: 5     // Divides screen into 5 vertical lanes
}

player {
    lane_lock: 5     // Player snaps to lanes
    controls: horizontal   // Move left/right between lanes
}
```

Lanes divide the screen into vertical columns. Players can only move between lane centers.

---

## Collision Detection

### How Collision Works

**Collision is automatic!** The runtime checks every frame if any two blocks overlap. When they do, it triggers the `on_collide` actions.

```levlang
player {
    x: 400
    y: 500
    color: cyan
    size: 30
    on_collide: game_over    // What happens when player hits anything
}

obstacle {
    x: 200
    y: 200
    color: red
    size: 40
    // No controls, no direction = static obstacle
}
```

### How the Game Knows What's an Obstacle

**Any block can be an obstacle!** The game doesn't need blocks to be named "obstacle". Collision detection works between ANY two blocks that have:
1. A position (x, y coordinates or start_position)
2. A size
3. Are not special blocks (viewport, overlay, game)

In the example above:
- `player` can collide with `obstacle`
- Even though `obstacle` has no special properties, it's solid and detectable
- The name doesn't matter - you could call it `enemy`, `wall`, `danger`, etc.

### on_collide Actions

```levlang
blockname {
    on_collide: game_over     // End the game
    on_collide: destroy        // Destroy the OTHER block
    on_collide: score+10       // Add 10 to score
}
```

**Available Actions:**
- `game_over` or `gameover` - Ends the game, shows overlay
- `destroy` - Removes the block you collided with
- `score+N` - Adds N points to the score (e.g., `score+5`, `score+100`)

**Note:** You can write `game_over`, `gameover`, or `GAME_OVER` - all work!

---

## Random Values

Use `rand(min, max)` for random numbers:

```levlang
obstacle {
    x: rand(100, 700)      // Random X between 100 and 700
    y: rand(50, 400)       // Random Y between 50 and 400
    speed: rand(2, 6)      // Random speed between 2 and 6
    color: red
    size: 40
}
```

**Random values are generated ONCE when the block is created.**

---

## Spawning System

Create blocks that spawn continuously:

```levlang
// The template - defines what to spawn
asteroid {
    color: gray
    size: 40
    direction: down
    speed: rand(3, 7)
    offscreen: destroy       // Remove when it leaves the screen
}

// The spawner - creates new asteroids
spawner {
    shape: script           // Required for spawners
    target: asteroid        // What block to spawn
    spawn_rate: 1.5sec      // How often to spawn
    spawn_lane: random      // Where to spawn (if lanes enabled)
}
```

### Spawn Rate Format

```levlang
spawn_rate: 1sec          // Every 1 second
spawn_rate: 0.5sec        // Every half second
spawn_rate: 2sec          // Every 2 seconds
spawn_rate: 500ms         // Every 500 milliseconds
```

### Offscreen Actions

```levlang
blockname {
    offscreen: destroy     // Remove block when it leaves screen
}
```

---

## Game Over Overlay

Display text when the game ends:

```levlang
overlay {
    shape: overlay
    _lines: ["GAME OVER!", "Score: {score}", "Press ESC to quit"]
}
```

**Special Placeholders:**
- `{score}` - Replaced with the current score

The overlay appears automatically when `game_over` is triggered.

---

## Default Values

### Automatic Defaults Applied by the Runtime

| Property | Default Value | Notes |
|----------|--------------|-------|
| `x` | screen center | If no x/y provided |
| `y` | screen center | If no x/y provided |
| `start_position` | `"center"` | Used if no x/y coordinates |
| `color` | `white` | RGB (255, 255, 255) |
| `size` | `48x48` | Width x Height in pixels |
| `shape` | `"rectangle"` | Also: circle, script, viewport, overlay |
| `speed` | `0` | No movement |
| `controls` | `none` | Not player-controlled |
| `direction` | `none` | No automatic movement |
| `on_collide` | `none` | No collision response |
| `offscreen` | `none` | Blocks persist off-screen |

### Viewport Defaults

```levlang
viewport {
    size: 960x540          // Default window size
    background: #101820    // Default dark background
    title: "LevLang Game"  // Default if no game "title" set
}
```

---

## Automatic Behaviors

### 1. Entity Creation

**Automatically Created:**
- Any block with `controls`, `x`/`y`, or `start_position` becomes a game entity
- Entities are rendered and updated every frame

**Not Created as Entities:**
- Blocks named `game`
- Blocks with `shape: viewport`
- Blocks with `shape: overlay`
- Blocks with `shape: script` (spawners)

### 2. Movement

Movement requires BOTH:
1. A `speed` value > 0
2. EITHER `controls` OR `direction`

```levlang
// This WILL move (has speed + controls):
player {
    speed: 5
    controls: arrows
}

// This WON'T move (has controls but no speed):
player {
    speed: 0        // or missing!
    controls: arrows
}

// This WILL move (has speed + direction):
enemy {
    speed: 3
    direction: down
}
```

### 3. Collision Detection

**When:** Every frame, after all entities update positions

**How:** Uses pygame's `rect.colliderect()` to check overlaps

**Between:** ALL pairs of entities (player vs enemies, enemy vs enemy, etc.)

**Actions:** Both entities' `on_collide` rules are triggered

### 4. Screen Clamping

**Automatic:** Entities cannot move outside the screen boundaries

**Exception:** Entities with `offscreen: destroy` can leave and will be removed

### 5. Colors

**Named Colors Available:**
- `red`, `blue`, `green`, `cyan`, `magenta`, `yellow`
- `orange`, `purple`, `white`, `black`, `gray`, `dark_gray`

**Color Formats:**
```levlang
color: blue           // Named color
color: #FF5733        // Hex RGB
color: #FF5733AA      // Hex RGBA (with alpha/transparency)
```

---

## Complete Examples

### Example 1: Simple Game with Static Obstacles

```levlang
// Navigate through random obstacles!

game "Obstacle Course"

player {
    x: 400
    y: 500
    color: cyan
    size: 30
    speed: 6
    controls: arrows
    on_collide: game_over
}

obstacle1 {
    x: rand(100, 700)
    y: rand(100, 200)
    color: red
    size: 40
}

obstacle2 {
    x: rand(100, 700)
    y: rand(200, 300)
    color: orange
    size: 40
}

obstacle3 {
    x: rand(100, 700)
    y: rand(300, 400)
    color: yellow
    size: 40
}

overlay {
    shape: overlay
    _lines: ["GAME OVER!", "You hit an obstacle!", "Press ESC to quit"]
}

start()
```

### Example 2: Spawning Game with Score

```levlang
// Dodge falling asteroids!

game "Asteroid Dodger"

player {
    color: cyan
    size: 30
    speed: 8
    controls: arrows
    start_position: bottom_center
    on_collide: game_over
}

asteroid {
    color: gray
    size: 40
    direction: down
    speed: rand(3, 6)
    offscreen: destroy
}

coin {
    color: yellow
    size: 20
    direction: down
    speed: 4
    offscreen: destroy
    on_collide: score+10
}

asteroid_spawner {
    shape: script
    target: asteroid
    spawn_rate: 1sec
}

coin_spawner {
    shape: script
    target: coin
    spawn_rate: 2sec
}

overlay {
    shape: overlay
    _lines: ["GAME OVER!", "Final Score: {score}", "Press ESC to quit"]
}

start()
```

### Example 3: Lane-Based Game

```levlang
// Dodge cars in lanes!

game "Highway Dodge"

viewport {
    lane_lock: 5
}

player {
    color: blue
    size: 40
    speed: 300
    controls: horizontal
    start_position: bottom_center
    lane_lock: 5
    on_collide: game_over
}

car {
    color: red
    size: 50
    direction: down
    speed: rand(4, 8)
    offscreen: destroy
    on_collide: score+5
}

car_spawner {
    shape: script
    target: car
    spawn_rate: 0.8sec
    spawn_lane: random
}

overlay {
    shape: overlay
    _lines: ["GAME OVER!", "Cars Dodged: {score}", "Press ESC to quit"]
}

start()
```

---

## Special Blocks

### game Block

```levlang
game "My Game"    // Shorthand syntax

// Or full syntax:
game {
    title: "My Game"
}
```

### viewport Block

```levlang
viewport {
    size: 800x600
    background: #1a1a2e
    title: "My Game"      // Alternative to game "title"
    lane_lock: 5          // Enable lane system
}
```

### overlay Block

```levlang
overlay {
    shape: overlay
    _lines: ["Line 1", "Line 2", "Score: {score}"]
}
```

Displays when `game_over` is triggered.

---

## Tips and Best Practices

### Performance

1. **Use `offscreen: destroy`** on spawned entities to prevent memory buildup
2. **Limit spawn rates** - spawning every 0.1sec can cause lag
3. **Keep collision boxes reasonable** - huge sprites = more collision checks

### Game Design

1. **Test random ranges** - use `rand()` with reasonable min/max values
2. **Balance speed values** - player should be faster than obstacles for fairness
3. **Give feedback** - use overlays to show game over messages
4. **Start simple** - add complexity incrementally

### Debugging

1. **Check speed values** - blocks won't move if speed is 0 or missing
2. **Verify collision** - make sure blocks have `size` properties
3. **Test without cache** - bump VERSION in cli.py if behavior seems wrong
4. **Use distinct colors** - helps identify which blocks are which

---

## Pygame Code Injection

For advanced users, embed raw Pygame code:

```levlang
custom_logic[] {
    # Raw Python/Pygame code
    screen = pygame.display.get_surface()
    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 50)
}

start()
```

Blocks ending with `[]` instead of `{}` contain pure Pygame/Python code.

---

## Quick Reference Card

```levlang
// MINIMAL GAME TEMPLATE

game "Title"

player {
    x: 400
    y: 500
    color: cyan
    size: 30
    speed: 5           // Don't forget!
    controls: arrows   // Don't forget!
}

obstacle {
    x: 300
    y: 200
    color: red
    size: 40
    // Static - no speed/controls needed
}

start()
```

**Remember:**
- Movement needs: `speed` + (`controls` OR `direction`)
- Collision is automatic between all blocks
- Random values: `rand(min, max)`
- Arrays: `_lines: ["item1", "item2"]`
- Actions: `game_over`, `destroy`, `score+N`

---

## Version

This documentation is for **LevLang v0.3.2**

Last updated: 2025-11-22

