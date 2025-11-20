# LevLang Beginner's Guide

Welcome to LevLang! This guide will teach you how to create games from scratch, even if you've never programmed before.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Your First Game](#your-first-game)
4. [Understanding the Basics](#understanding-the-basics)
5. [Adding Enemies](#adding-enemies)
6. [Scoring and UI](#scoring-and-ui)
7. [Game Over](#game-over)
8. [More Examples](#more-examples)
9. [Next Steps](#next-steps)

---

## Introduction

### What is LevLang?

LevLang is a **game development language** designed to make creating 2D games easy and fun. You write your game in LevLang (`.lvl` files), and it automatically generates Python code using pygame.

### Why LevLang?

- ✅ **Simple Syntax**: Write games with minimal code
- ✅ **Three Skill Levels**: Start simple, grow to advanced
- ✅ **Instant Results**: See your game running in seconds
- ✅ **Learn by Doing**: Clear examples and patterns
- ✅ **Powered by Pygame**: Battle-tested game engine underneath

### What You'll Learn

By the end of this guide, you'll be able to:
- Create a playable game from scratch
- Add players, enemies, and collectibles
- Handle collisions and scoring
- Design game over screens
- Understand the three syntax modes

---

## Getting Started

### Installation

1. **Install Python** (3.8 or higher)
   - Download from [python.org](https://python.org)

2. **Install LevLang**
   ```bash
   cd language
   pip install -e .
   ```

3. **Verify Installation**
   ```bash
   levlang --version
   ```

   You should see the LevLang banner!

### Your First Command

```bash
levlang run examples/01_pong.lvl
```

This runs the Pong example. Use arrow keys or W/S to play!

---

## Your First Game

Let's create a simple "Dodge the Falling Objects" game!

### Step 1: Create a File

Create a new file called `dodge.lvl`:

```levlang
game "Dodge Game"
```

That's it! You've declared a game. Let's add more.

### Step 2: Add a Player

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
}
```

**What does this mean?**
- `player { ... }` creates a player
- `shape: circle` makes it a circle
- `color: blue` makes it blue
- `size: 40x40` sets width and height
- `speed: 5` controls how fast it moves
- `movement: arrows` lets you control it with arrow keys

### Step 3: Start the Game

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
}

start()
```

The `start()` command launches the game.

### Step 4: Run It!

```bash
levlang run dodge.lvl
```

You should see a blue circle you can move with arrow keys! 🎉

---

## Understanding the Basics

### Blocks

LevLang uses **blocks** to define game objects:

```levlang
blockname {
    property: value
    property: value
}
```

### Common Blocks

```levlang
game "Title"        // Declares the game
player { ... }      // Creates the player
enemy { ... }       // Creates enemies
coin { ... }        // Creates collectibles
powerup { ... }     // Creates power-ups
ui { ... }          // Creates UI elements
gameover { ... }    // Creates game over screen
```

**You can create ANY block name!** The language is very flexible.

### Properties

Properties define how things behave:

```levlang
shape: circle          // What it looks like
color: red            // What color it is
size: 30x30           // How big it is
speed: 5              // How fast it moves
movement: arrows      // How to control it
```

### Comments

```levlang
// This is a comment - it's ignored by the compiler
// Use comments to explain your code!

/* 
   Multi-line comment
   for longer explanations
*/
```

---

## Adding Enemies

Let's make our game more interesting by adding falling enemies!

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
}

enemy {
    shape: rectangle
    color: red
    size: 30x30
    spawn: random
    move: down
    speed: 3
    offscreen: destroy
}

spawn_rate: 1sec

start()
```

**New concepts:**
- `spawn: random` - enemies appear at random positions at the top
- `move: down` - enemies move downward
- `offscreen: destroy` - enemies are removed when they leave the screen
- `spawn_rate: 1sec` - new enemy appears every second

### Testing

Run the game again:
```bash
levlang run dodge.lvl
```

You should now see red rectangles falling down!

---

## Collisions

Let's make something happen when the player touches an enemy:

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
    on_collide: enemy: gameover
}

enemy {
    shape: rectangle
    color: red
    size: 30x30
    spawn: random
    move: down
    speed: 3
    offscreen: destroy
}

spawn_rate: 1sec

start()
```

**New concept:**
- `on_collide: enemy: gameover` - when player touches enemy, game over!

---

## Scoring and UI

Let's add a score that increases when you avoid enemies:

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
    on_collide: enemy: gameover
}

enemy {
    shape: rectangle
    color: red
    size: 30x30
    spawn: random
    move: down
    speed: 3
    offscreen: destroy, score+1
}

spawn_rate: 1sec

ui {
    "Score: {score}" at topleft
    "Use ARROW KEYS" at topright
}

start()
```

**New concepts:**
- `offscreen: destroy, score+1` - when enemy leaves screen, add 1 to score
- `ui { ... }` - displays text on screen
- `"Score: {score}"` - shows the score variable
- `at topleft` - positions text at top-left corner

**Positions available:**
- `topleft`, `topcenter`, `topright`
- `left`, `center`, `right`
- `bottomleft`, `bottomcenter`, `bottomright`

---

## Game Over

Let's add a game over screen:

```levlang
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
    on_collide: enemy: gameover
}

enemy {
    shape: rectangle
    color: red
    size: 30x30
    spawn: random
    move: down
    speed: 3
    offscreen: destroy, score+1
}

spawn_rate: 1sec

ui {
    "Score: {score}" at topleft
    "Use ARROW KEYS" at topright
}

gameover {
    "GAME OVER!"
    "Final Score: {score}"
    "Press SPACE to restart"
}

start()
```

**New concept:**
- `gameover { ... }` - displays when game ends
- Each line in quotes becomes a line of text
- Can show score: `{score}`

---

## Complete Game!

Here's our complete game with all features:

```levlang
// Dodge Game - Avoid the falling enemies!
game "Dodge Game"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
    on_collide: enemy: gameover
}

enemy {
    shape: rectangle
    color: red
    size: 30x30
    spawn: random
    move: down
    speed: 3
    offscreen: destroy, score+1
}

spawn_rate: 1sec

ui {
    "Score: {score}" at topleft
    "Use ARROW KEYS to dodge!" at topcenter
    "Avoid the red rectangles!" at topright
}

gameover {
    "GAME OVER!"
    "Final Score: {score}"
    "Press SPACE to restart"
    "Press ESC to quit"
}

start()
```

**Congratulations!** You've created a complete game! 🎮

---

## More Examples

### Adding Collectibles

```levlang
coin {
    shape: circle
    color: yellow
    size: 20x20
    spawn: random
    move: down
    speed: 2
    on_collide: player: destroy, score+10
}
```

### Adding Lives

```levlang
lives: 3

player {
    // ... other properties
    on_collide: enemy: lose_life
}

ui {
    "Score: {score}" at topleft
    "Lives: {lives}" at topright
}
```

### Making it Harder Over Time

```levlang
enemy {
    // ... other properties
    speed: rand(2, 5)  // Random speed between 2 and 5
}

spawn_rate: 0.8sec  // Faster spawning (less time between spawns)
```

### Adding Power-ups

```levlang
powerup {
    shape: star
    color: green
    size: 25x25
    spawn: random
    move: down
    speed: 2
    on_collide: player: destroy, speed+2, invincible(3sec)
}
```

---

## Learning More Syntax Modes

LevLang has **three syntax modes**. You've been using the **Block Syntax** (simplest).

### Block Syntax (What You've Been Using)

```levlang
game "My Game"
player { movement: arrows }
enemy { spawn: random }
start()
```

**Best for:** Quick prototypes, learning, arcade games

### Component Syntax (Reusable Blueprints)

```levlang
component "ship" {
    shape: "triangle"
    size: "40x40"
    speed: 6
}

entities {
    player: "ship" {
        color: "blue"
        position: "center"
    }
    
    enemy: "ship" {
        color: "red"
        position: "top"
    }
}

game { title: "Space Game" }
```

**Best for:** When you need multiple similar objects

### Advanced Syntax (Full Programming)

```levlang
game SpaceGame {
    title = "Space Game"
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
    }
}

scene Main {
    player = Player()
    
    update {
        // Game logic
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
    }
}
```

**Best for:** Complex games, full control, advanced features

See [syntax.md](syntax.md) for complete syntax reference!

---

## Common Patterns

### Pattern 1: Dodge Game

```levlang
player { movement: arrows }
enemy { spawn: random, move: down, on_collide: player: gameover }
```

### Pattern 2: Collect Game

```levlang
player { movement: arrows }
coin { spawn: random, move: down, on_collide: player: destroy, score+10 }
goal: 100  // Win when score reaches 100
```

### Pattern 3: Shooter Game

```levlang
player { movement: arrows, shoot: space }
bullet { owner: player, speed: 10, move: up }
enemy { spawn: top, move: down, on_collide: bullet: destroy }
```

### Pattern 4: Side Scroller

```levlang
player { movement: wasd, jump: space, physics: gravity }
platform { solid: true }
camera { follow: player }
```

---

## Tips for Beginners

### 1. Start Small
Begin with just a player. Then add one feature at a time.

### 2. Test Often
After each change, run your game:
```bash
levlang run mygame.lvl
```

### 3. Use Comments
Explain what your code does:
```levlang
// This makes the enemy move faster
speed: 5
```

### 4. Copy and Modify
Start with an example and change it:
```bash
cp examples/01_pong.lvl my_pong.lvl
# Now edit my_pong.lvl
```

### 5. Experiment!
Try different values:
```levlang
speed: 3    // Too slow?
speed: 10   // Too fast?
speed: 6    // Just right!
```

### 6. Read Error Messages
If something goes wrong, read the error:
```
error: Invalid property 'spead'
Did you mean 'speed'?
```

### 7. Check the Examples
Look at the 10 example games for inspiration!

---

## Common Mistakes

### Mistake 1: Forgetting `start()`

❌ **Wrong:**
```levlang
game "My Game"
player { movement: arrows }
// Game won't run!
```

✅ **Correct:**
```levlang
game "My Game"
player { movement: arrows }
start()
```

### Mistake 2: Misspelled Properties

❌ **Wrong:**
```levlang
player {
    shap: circle     // Typo!
    colour: blue     // Wrong spelling
}
```

✅ **Correct:**
```levlang
player {
    shape: circle
    color: blue
}
```

### Mistake 3: Missing Colons

❌ **Wrong:**
```levlang
player {
    shape circle    // Missing colon
}
```

✅ **Correct:**
```levlang
player {
    shape: circle
}
```

### Mistake 4: Wrong Quote Types

❌ **Wrong:**
```levlang
game My Game    // No quotes
```

✅ **Correct:**
```levlang
game "My Game"
```

---

## Debugging Tips

### Problem: Game doesn't run

**Check:**
1. Did you call `start()`?
2. Is your file saved?
3. Any error messages when transpiling?

### Problem: Player doesn't move

**Check:**
1. Did you set `movement: arrows` or similar?
2. Did you set a `speed` value?

### Problem: Collisions don't work

**Check:**
1. Did you spell the target correctly? (e.g., `enemy` not `enmy`)
2. Are the objects actually touching? (check sizes)

### Problem: Nothing appears on screen

**Check:**
1. Are objects positioned on screen?
2. Did you set `size` and `color`?
3. Is the game actually running?

---

## Next Steps

### 1. Try the Examples

Explore all 10 example games:
```bash
levlang run examples/01_pong.lvl
levlang run examples/02_snake.lvl
# ... etc
```

### 2. Modify an Example

Copy an example and change it:
```bash
cp examples/02_snake.lvl my_snake.lvl
```

Then modify:
- Change colors
- Change speeds
- Add new features

### 3. Create Your Own Game

Pick a simple game idea:
- Catch falling objects
- Dodge moving obstacles
- Shoot targets
- Navigate a maze

### 4. Learn Advanced Features

Read the [Syntax Reference](syntax.md) for:
- Component syntax
- Advanced programming features
- Event handlers
- More complex examples

### 5. Share Your Game!

Once you've created something cool, share it with the community!

---

## Quick Reference Card

### Essential Blocks

```levlang
game "Title"                   // Declare game
player { ... }                 // Create player
enemy { ... }                  // Create enemy
ui { ... }                     // Create UI
gameover { ... }               // Game over screen
start()                        // Start game
```

### Common Properties

```levlang
shape: circle/rectangle/triangle
color: red/blue/green/"#FF0000"
size: 40x40
speed: 5
movement: arrows/wasd/mouse
```

### Movement

```levlang
movement: arrows               // Arrow keys
movement: wasd                // WASD keys
movement: wasd_arrows         // Both
movement: mouse_follow        // Follow mouse
```

### Collision

```levlang
on_collide: target: action
on_collide: enemy: gameover
on_collide: coin: destroy, score+10
```

### Spawning

```levlang
spawn: random                 // Random position
spawn: top/bottom/left/right  // Edge
spawn_rate: 1sec              // Every 1 second
```

### Movement Patterns

```levlang
move: up/down/left/right      // Direction
move: random                  // Random movement
offscreen: destroy            // Remove when off-screen
```

---

## Resources

- **Syntax Reference**: [syntax.md](syntax.md) - Complete syntax guide
- **Examples**: `examples/` folder - 10 complete games
- **Documentation**: `docs/` folder - Advanced topics
- **Community**: Share your creations!

---

## Conclusion

**Congratulations!** You've learned the basics of LevLang! 🎉

You now know how to:
- ✅ Create a game file
- ✅ Add players and enemies
- ✅ Handle collisions
- ✅ Add scoring and UI
- ✅ Create game over screens

**Keep creating, keep learning, and most importantly: have fun!** 🎮

---

**Made with ❤️ by Levelium Inc.**

Happy Game Development! 🚀

