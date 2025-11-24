# LevLang Syntax Reference

Complete reference for LevLang block syntax, including all features, defaults, and automatic behaviors.

## Table of Contents

1. [Basic Structure](#basic-structure)
2. [Block Properties](#block-properties)
3. [Pygame Code Blocks](#pygame-code-blocks)
4. [Collision Detection](#collision-detection)
5. [Random Values](#random-values)
6. [Spawning System](#spawning-system)
7. [Game Over Overlay](#game-over-overlay)
8. [Default Values](#default-values)
9. [Automatic Behaviors](#automatic-behaviors)
10. [Complete Examples](#complete-examples)

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

## Pygame Code Blocks

LevLang allows you to write **raw Python/Pygame code** directly in your game using square brackets `[]`. This gives you complete control when you need features beyond the declarative syntax.

### Syntax

```levlang
blockname[
    # Your Python/Pygame code here
    # You have access to: screen, clock, entities
    pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)
]
```

**IMPORTANT:** Pygame code blocks use **square brackets `[ ]`**, not curly braces `{ }`.

### Available Variables

Inside pygame blocks, you have access to:
- `screen` - The pygame display surface
- `clock` - The pygame clock object  
- `entities` - List of all game entities (when in mixed mode)
- All pygame modules and functions

### Two Modes

#### 1. Mixed Mode (Pygame blocks + Regular blocks)

When you combine pygame blocks with regular LevLang blocks, the pygame code runs **every frame** during rendering:

```levlang
game "My Game" {
    width: 800
    height: 600
}

player {
    color: cyan
    size: 30
    controls: arrows
}

// Custom particle effects
particles[
    import math
    for i in range(10):
        angle = (pygame.time.get_ticks() / 1000 + i * 0.6) % (2 * math.pi)
        x = int(400 + 200 * math.cos(angle))
        y = int(300 + 200 * math.sin(angle))
        pygame.draw.circle(screen, (100, 150, 255), (x, y), 5)
]

// Display custom stats
stats[
    font = pygame.font.Font(None, 24)
    fps = int(clock.get_fps())
    text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
]

start()
```

**How it works:** The runtime creates entities from regular blocks, then calls your pygame blocks each frame.

#### 2. Pure Pygame Mode (Only pygame blocks)

When your `.lvl` file contains **only** pygame blocks (no regular blocks), LevLang generates a standalone pygame program:

```levlang
// Pure pygame mode - no regular blocks

main[
    # Setup display
    pygame.display.set_caption("My Custom Game")
    
    # Draw
    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 150))
    pygame.draw.circle(screen, (0, 255, 0), (400, 300), 75)
    
    # Custom text
    font = pygame.font.Font(None, 48)
    text = font.render("Pure Pygame!", True, (255, 255, 255))
    screen.blit(text, (250, 450))
]
```

**How it works:** LevLang generates a complete pygame game loop with window creation, event handling, and clock management.

### Common Use Cases

**1. Custom Rendering**
```levlang
trail[
    # Draw a trail behind entities
    if entities:
        player = entities[0]
        pygame.draw.circle(screen, (100, 100, 255), player.rect.center, 15, 2)
]
```

**2. Advanced Effects**
```levlang
glow[
    import math
    time = pygame.time.get_ticks() / 1000
    intensity = int(128 + 127 * math.sin(time * 2))
    pygame.draw.circle(screen, (intensity, intensity, 255), (400, 300), 100, 3)
]
```

**3. Debug Information**
```levlang
debug[
    font = pygame.font.Font(None, 20)
    if entities:
        for i, entity in enumerate(entities):
            text = font.render(f"{entity.name}: {entity.rect.center}", True, (255, 255, 0))
            screen.blit(text, (10, 30 + i * 20))
]
```

**4. Custom Input Handling**
```levlang
input[
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw mouse cursor highlight
    pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 10, 2)
]
```

### Tips & Best Practices

1. **Pygame blocks are called every frame** - avoid heavy computations
2. **Use meaningful block names** - `particles`, `ui_custom`, `debug`, etc.
3. **Keep code organized** - one block per logical feature
4. **Empty blocks are ignored** - no error if block has no code
5. **Import inside blocks** - imports like `math` should be inside the block
6. **Mix with declarative syntax** - use regular blocks for simple entities, pygame blocks for complex effects

### Limitations

- Pygame blocks **cannot** modify LevLang entity properties directly
- Pygame blocks run in render phase, not update phase
- Variables defined in one block are not accessible in another
- Pygame blocks do not support LevLang collision detection syntax

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

