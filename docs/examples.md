# LevLang Game Examples

Complete game examples to learn from and build upon.

---

## 🎮 Example Games

### 1. Simple Shooter
### 2. Flappy Bird Clone
### 3. Space Invaders
### 4. Endless Runner
### 5. Platformer
### 6. Catch Game
### 7. Breakout Clone

---

## 1. 🎯 Simple Shooter

**Difficulty**: Beginner  
**Concepts**: Movement, Shooting, Enemies, Score

```levlang
// Simple Shooter
game "Simple Shooter" 800x600 black

player moves with arrows
player shoots with space
player at bottom center
player speed 7

enemies spawn every 2sec at top
enemies move down
enemies speed 3

when bullet hits enemy score +10
when bullet hits enemy destroy enemy
when enemy hits player game over

show score at top center
show message "Shoot the enemies!" for 3sec

play sound "shoot.wav" when shoot
play sound "hit.wav" when bullet hits enemy
```

**What you'll learn:**
- Basic player movement
- Shooting mechanics
- Enemy spawning
- Collision detection
- Score tracking

---

## 2. 🐦 Flappy Bird Clone

**Difficulty**: Beginner  
**Concepts**: Jumping, Obstacles, Gravity

```levlang
// Flappy Bird
game "Flappy Bird" 400x600

player jumps with space
player has gravity
player sprite "bird.png"
player at left center

pipes spawn every 2sec at right
pipes move left
pipes have gap 150
pipes speed 3

when player hits pipe game over
when player hits ground game over
when player passes pipe score +1

show score at top center
show message "Tap SPACE to flap!" for 3sec

play sound "flap.wav" when jump
play sound "hit.wav" when player hits pipe
```

**What you'll learn:**
- Gravity physics
- Jumping mechanics
- Obstacle generation
- Gap management
- Endless scrolling

---

## 3. 👾 Space Invaders

**Difficulty**: Intermediate  
**Concepts**: Grid enemies, Shooting, Lives

```levlang
// Space Invaders
game "Space Invaders" 800x600 black

player moves with arrows
player shoots with space
player at bottom center
player speed 8

enemies spawn in grid 5x3 at top
enemies move left and right
enemies move down when hit edge
enemies shoot randomly
enemies speed 2

shields at bottom
shields block bullets
shields health 5

when bullet hits enemy score +10
when enemy bullet hits player lives -1
when enemy reaches bottom game over
when lives equals 0 game over
when all enemies destroyed next level

show score at top left
show lives at top right
show level at top center

play music "bgm.mp3" loop
play sound "shoot.wav" when shoot
play sound "explosion.wav" when enemy destroyed
```

**What you'll learn:**
- Grid-based enemy spawning
- Enemy formation movement
- Shield mechanics
- Lives system
- Level progression

---

## 4. 🏃 Endless Runner

**Difficulty**: Beginner  
**Concepts**: Auto-scrolling, Jumping, Obstacles

```levlang
// Endless Runner
game "Runner" 800x600

player at left center
player jumps with space
player has gravity
player sprite "runner.png"

ground scrolls left speed 5

obstacles spawn every 3sec at right
obstacles move left speed 5
obstacles random height

coins spawn every 2sec at right
coins move left speed 5
coins at random height

when player hits obstacle game over
when player hits coin score +10

every 1sec score +1
every 10sec increase speed

show score at top center
show message "Jump over obstacles!" for 3sec

play sound "jump.wav" when jump
play sound "coin.wav" when collect
play music "run.mp3" loop
```

**What you'll learn:**
- Auto-scrolling background
- Procedural obstacle generation
- Speed progression
- Endless gameplay
- Score over time

---

## 5. 🎮 Platformer

**Difficulty**: Advanced  
**Concepts**: Platforms, Gravity, Collectibles

```levlang
// Platformer
game "Platformer" 800x600

player moves with arrows
player jumps with space
player has gravity
player sprite "hero.png"
player speed 5

platforms at 0,500 size 800x100
platforms at 200,400 size 200x20
platforms at 500,300 size 200x20
platforms at 100,250 size 150x20

coins spawn on platforms
coins worth 10

enemies patrol on platforms
enemies move left and right
enemies speed 2

spikes at 350,480 size 100x20

when player touches coin score +10
when player touches enemy lives -1
when player touches spikes lives -1
when player falls off screen lives -1
when score reaches 100 win game
when lives equals 0 game over

show score at top left
show lives at top right

play sound "jump.wav" when jump
play sound "coin.wav" when collect
play sound "hurt.wav" when hit
```

**What you'll learn:**
- Platform collision
- Gravity and jumping
- Enemy AI (patrol)
- Hazards (spikes)
- Win conditions

---

## 6. 🎪 Catch Game

**Difficulty**: Beginner  
**Concepts**: Mouse control, Falling objects

```levlang
// Catch Game
game "Catch" 600x800

player moves with mouse
player at bottom center
player sprite "basket.png"
player size 100x50

apples spawn every 1sec at top random
apples fall down
apples speed 3

bombs spawn every 3sec at top random
bombs fall down
bombs speed 4

when player catches apple score +10
when player catches bomb score -20
when apple hits ground lives -1
when lives equals 0 game over

after 60sec win game

show score at top center
show lives at top left
show timer at top right

countdown from 60

play sound "catch.wav" when catch apple
play sound "explosion.wav" when catch bomb
```

**What you'll learn:**
- Mouse-based movement
- Multiple object types
- Time limits
- Negative scoring
- Win conditions

---

## 7. 🧱 Breakout Clone

**Difficulty**: Intermediate  
**Concepts**: Paddle, Ball, Bricks

```levlang
// Breakout
game "Breakout" 600x800

paddle moves with mouse
paddle at bottom center
paddle size 100x20
paddle speed 10

ball starts on paddle
ball launches with space
ball bounces off walls
ball bounces off paddle
ball speed 5

bricks in grid 8x5 at top
bricks colors red blue green yellow
bricks worth 10

when ball hits brick destroy brick
when ball hits brick score +10
when ball falls off screen lives -1
when all bricks destroyed next level
when lives equals 0 game over

powerups spawn when brick destroyed
powerups give bigger paddle
powerups give extra ball
powerups give slower ball

show score at top left
show lives at top right
show level at top center

play sound "bounce.wav" when ball bounces
play sound "break.wav" when brick breaks
play music "bgm.mp3" loop
```

**What you'll learn:**
- Paddle mechanics
- Ball physics
- Brick grid
- Power-up system
- Level progression

---

## 🎯 Try These Challenges

### Challenge 1: Customize
- Change colors and sizes
- Add your own sprites
- Modify speeds and timings

### Challenge 2: Enhance
- Add new enemy types
- Create power-ups
- Add sound effects

### Challenge 3: Combine
- Mix mechanics from different games
- Create your own unique game
- Add multiple levels

---

## 📁 Example Files

All examples are available in the `examples/` folder:

```
examples/
├── simple_shooter.lvl
├── flappy_bird.lvl
├── space_invaders.lvl
├── endless_runner.lvl
├── platformer.lvl
├── catch_game.lvl
└── breakout.lvl
```

Run any example:
```bash
levlang run examples/simple_shooter.lvl
```

---

## 💡 Learning Tips

1. **Start with Simple Shooter** - Easiest to understand
2. **Modify Examples** - Change values and see what happens
3. **Combine Mechanics** - Mix features from different games
4. **Build Gradually** - Add one feature at a time
5. **Test Frequently** - Run your game after each change

---

## 🚀 Next Steps

- [Syntax Reference](syntax-reference.md) - Complete language reference
- [Tutorial: Space Shooter](tutorial-space-shooter.md) - Step-by-step guide
- [Built-in Functions](functions.md) - All available functions

---

**Ready to create your own game?** Start with an example and make it yours! 🎮

[← Back to Getting Started](getting-started.md) | [Syntax Reference →](syntax-reference.md)
