# LevLang Examples

This folder contains 10 classic game examples plus comprehensive documentation.

---

## 📚 Documentation

- **[guide.md](guide.md)** - Beginner-friendly tutorial (start here!)
- **[syntax.md](syntax.md)** - Complete syntax reference

---

## 🎮 Game Examples

### 1. Pong (`01_pong.lvl`)
**Classic paddle game**
- Two paddles, one ball
- Simple physics and scoring
- AI opponent
- **Syntax**: Component-based

```bash
levlang run examples/01_pong.lvl
```

### 2. Snake (`02_snake.lvl`)
**Grow by eating food**
- Grid-based movement
- Growing trail mechanic
- Self-collision detection
- **Syntax**: Block-based

```bash
levlang run examples/02_snake.lvl
```

### 3. Breakout (`03_breakout.lvl`)
**Break bricks with a ball**
- Paddle controls with mouse
- Brick grid system
- Lives and victory conditions
- **Syntax**: Block-based

```bash
levlang run examples/03_breakout.lvl
```

### 4. Space Invaders (`04_space_invaders.lvl`)
**Shoot the alien army**
- Wave-based enemy movement
- Shooting mechanics
- Barriers and lives
- **Syntax**: Block-based

```bash
levlang run examples/04_space_invaders.lvl
```

### 5. Flappy Bird (`05_flappy_bird.lvl`)
**Tap to fly through pipes**
- Gravity physics
- Procedural pipe generation
- Score on passing obstacles
- **Syntax**: Block-based

```bash
levlang run examples/05_flappy_bird.lvl
```

### 6. Asteroids (`06_asteroids.lvl`)
**Shoot space rocks**
- Rotation + thrust controls
- Asteroids split when destroyed
- Screen wrapping
- **Syntax**: Block-based

```bash
levlang run examples/06_asteroids.lvl
```

### 7. Pac-Man (`07_pacman.lvl`)
**Collect dots, avoid ghosts**
- Maze navigation
- Ghost AI (chase/scatter)
- Power pellets
- **Syntax**: Block-based

```bash
levlang run examples/07_pacman.lvl
```

### 8. Tetris (`08_tetris.lvl`)
**Stack falling blocks**
- 7 tetromino shapes
- Line clearing
- Increasing difficulty
- **Syntax**: Block-based

```bash
levlang run examples/08_tetris.lvl
```

### 9. Platformer (`09_platformer.lvl`)
**Mario-style platformer**
- Gravity and jumping
- Platform collision
- Enemy bouncing
- Camera following
- **Syntax**: Block-based

```bash
levlang run examples/09_platformer.lvl
```

### 10. Galaga (`10_galaga.lvl`)
**Wave-based space shooter**
- Formation flying enemies
- Dive attack patterns
- Stage progression
- **Syntax**: Block-based

```bash
levlang run examples/10_galaga.lvl
```

---

## 🚀 Quick Start

### Run an Example

```bash
levlang run examples/01_pong.lvl
```

### Transpile to Python

```bash
levlang transpile examples/01_pong.lvl -o pong.py
python pong.py
```

### Modify an Example

```bash
# Copy an example
cp examples/02_snake.lvl my_snake.lvl

# Edit it
nano my_snake.lvl

# Run it
levlang run my_snake.lvl
```

---

## 📖 Learning Path

### Absolute Beginner
1. Read **[guide.md](guide.md)** first
2. Run `01_pong.lvl` to see a working game
3. Follow the guide to create your own dodge game
4. Try modifying `02_snake.lvl`

### Intermediate
1. Review **[syntax.md](syntax.md)** for all features
2. Study multiple examples to see different patterns
3. Create a game combining features from different examples
4. Experiment with the three syntax modes

### Advanced
1. Master all three syntax modes (Block, Component, Advanced)
2. Study the advanced syntax in `syntax.md`
3. Create complex games with custom logic
4. Contribute examples back to the community!

---

## 🎯 Example Complexity

| Example | Difficulty | Features | Lines |
|---------|-----------|----------|-------|
| 01_pong | ⭐ Easy | Basic collision, AI | ~45 |
| 02_snake | ⭐⭐ Medium | Grid movement, growing | ~40 |
| 05_flappy_bird | ⭐⭐ Medium | Gravity, procedural | ~45 |
| 03_breakout | ⭐⭐⭐ Hard | Grid layout, lives | ~55 |
| 04_space_invaders | ⭐⭐⭐ Hard | Multiple systems | ~75 |
| 06_asteroids | ⭐⭐⭐ Hard | Rotation, splitting | ~60 |
| 07_pacman | ⭐⭐⭐⭐ Expert | AI, maze, states | ~70 |
| 08_tetris | ⭐⭐⭐⭐ Expert | Complex rotation | ~65 |
| 09_platformer | ⭐⭐⭐⭐ Expert | Physics, camera | ~75 |
| 10_galaga | ⭐⭐⭐⭐ Expert | Formations, patterns | ~80 |

---

## 🔧 Customization Ideas

### Pong
- Add power-ups that change ball speed
- Make paddle size change based on score
- Add visual effects for collisions

### Snake
- Add different food types (bonus points)
- Make walls that can be destroyed
- Add teleport portals

### Breakout
- Add power-ups (bigger paddle, multi-ball)
- Make bricks with different health
- Add moving bricks

### Flappy Bird
- Add moving pipes
- Add collectible coins
- Change gravity over time

### Space Invaders
- Add boss levels
- Power-ups from destroyed enemies
- Different enemy types with unique behaviors

---

## 💡 Common Patterns

### Player Movement
```levlang
player {
    movement: arrows      // Arrow keys
    movement: wasd       // WASD
    movement: mouse      // Mouse
    speed: 5
}
```

### Enemy Spawning
```levlang
enemy {
    spawn: random        // Random position
    spawn_rate: 2sec    // Every 2 seconds
    move: down          // Move direction
    speed: 3
}
```

### Collision Handling
```levlang
on_collide: enemy: gameover
on_collide: coin: destroy, score+10
on_collide: powerup: collect, speed+2
```

### UI Display
```levlang
ui {
    "Score: {score}" at topleft
    "Lives: {lives}" at topright
}
```

---

## 🐛 Troubleshooting

### Example won't run
```bash
# Make sure you're in the right directory
cd /path/to/language

# Try with full path
levlang run examples/01_pong.lvl
```

### Syntax errors
```bash
# Check the error message
levlang transpile examples/01_pong.lvl -o test.py
# Read the error output carefully
```

### Want to see generated Python
```bash
levlang transpile examples/01_pong.lvl -o pong.py
cat pong.py
```

---

## 📝 Example Template

Use this template to create your own games:

```levlang
// My Awesome Game
game "My Game Title"

player {
    shape: circle
    color: blue
    size: 40x40
    speed: 5
    movement: arrows
}

// Add more game objects here...

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

---

## 🎨 Style Guidelines

### Good Practices
```levlang
// Use descriptive comments
// Keep blocks organized
// Group related properties
// Use consistent indentation

player {
    // Appearance
    shape: circle
    color: blue
    size: 40x40
    
    // Behavior  
    speed: 5
    movement: arrows
}
```

### Naming Conventions
- Use `snake_case` for multi-word blocks: `enemy_bullet`
- Use clear, descriptive names: `player`, `enemy`, `coin`
- Use verbs for actions: `on_collide`, `offscreen`

---

## 🌟 Challenge Yourself

Try these modifications to learn more:

1. **Easy**: Change colors and speeds in any example
2. **Medium**: Combine features from two examples
3. **Hard**: Add a new enemy type with unique behavior
4. **Expert**: Create a completely new game from scratch

---

## 📚 Additional Resources

- **Main README**: `../README.md` - Project overview
- **Syntax Docs**: `../docs/SYNTAX.md` - Advanced syntax
- **Getting Started**: `../docs/getting-started.md` - Installation guide

---

## 🤝 Contributing Examples

Have a cool game? Share it!

1. Create your game
2. Test it thoroughly
3. Add comments explaining the code
4. Submit as a pull request

---

## ⚡ Quick Commands

```bash
# Run an example
levlang run examples/01_pong.lvl

# Transpile an example
levlang transpile examples/01_pong.lvl -o pong.py

# Watch mode (auto-retranspile on changes)
levlang watch examples/01_pong.lvl -o pong.py

# Check version
levlang --version
```

---

**Happy Game Development! 🎮**

Made with ❤️ by Levelium Inc.

