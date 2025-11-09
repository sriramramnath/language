# LevLang Syntax Reference

Complete reference for all LevLang syntax and commands.

---

## 📋 Table of Contents

1. [Game Setup](#game-setup)
2. [Player](#player)
3. [Enemies](#enemies)
4. [Collectibles](#collectibles)
5. [Events](#events)
6. [UI Elements](#ui-elements)
7. [Audio](#audio)
8. [Levels](#levels)
9. [Advanced Features](#advanced-features)

---

## 🎮 Game Setup

### Basic Game Declaration

```levlang
game "Title"
```

### With Window Size

```levlang
game "Title" 800x600
game "Title" 1024x768
game "Title" 1920x1080
```

### With Background Color

```levlang
game "Title" black
game "Title" white
game "Title" blue
game "Title" red
game "Title" green
game "Title" gray
```

### Fullscreen Mode

```levlang
game "Title" fullscreen
```

### Combined Options

```levlang
game "Title" 800x600 black
game "Title" 1024x768 fullscreen
```

### Custom Icon

```levlang
game "Title" icon:assets/icon.png
```

---

## 🎯 Player

### Movement

```levlang
player moves with arrows          // Arrow keys only
player moves with wasd            // WASD keys only
player moves with arrows and wasd // Both control schemes
player moves with mouse           // Follow mouse cursor
```

### Actions

```levlang
player shoots with space          // Shooting mechanic
player jumps with space           // Jumping mechanic
```

### Properties

```levlang
player speed 5                    // Movement speed
player at 400,300                 // Starting position (x, y)
player sprite "player.png"        // Custom sprite image
player size 50x50                 // Custom size (width x height)
```

### Physics

```levlang
player has gravity                // Apply gravity
player bounces off walls          // Wall collision bounce
player friction 0.9               // Friction coefficient
```

---

## 👾 Enemies

### Spawning

```levlang
enemies spawn every 2sec          // Spawn interval
enemies spawn at top              // Spawn at top of screen
enemies spawn at bottom           // Spawn at bottom
enemies spawn at left             // Spawn at left
enemies spawn at right            // Spawn at right
enemies spawn at random           // Random spawn location
```

### Movement

```levlang
enemies move down                 // Move downward
enemies move up                   // Move upward
enemies move left                 // Move left
enemies move right                // Move right
enemies move towards player       // Follow player
enemies move randomly             // Random movement
enemies patrol                    // Patrol back and forth
```

### Properties

```levlang
enemies speed 3                   // Movement speed
enemies sprite "enemy.png"        // Custom sprite
enemies size 40x40                // Custom size
enemies health 3                  // Health points
```

### Advanced

```levlang
enemies shoot randomly            // Enemy shooting
enemies shoot at player           // Aim at player
```

---

## 💰 Collectibles

### Coins

```levlang
coins spawn every 5sec            // Spawn interval
coins worth 10                    // Point value
coins sprite "coin.png"           // Custom sprite
coins at random                   // Random position
```

### Power-ups

```levlang
powerups spawn every 10sec        // Spawn interval
powerups give speed               // Speed boost
powerups give shield              // Shield protection
powerups give weapon              // Weapon upgrade
powerups give health              // Health restore
powerups last 5sec                // Duration
```

---

## ⚡ Events

### Collision Events

```levlang
when player hits enemy game over
when player hits enemy lose life
when player hits coin score +10
when bullet hits enemy destroy enemy
when bullet hits enemy score +5
```

### Proximity Events

```levlang
when player near enemy alert
when enemy near player chase
```

### Score Events

```levlang
when score reaches 100 next level
when score reaches 50 spawn boss
when score > 100 win game
```

### Life Events

```levlang
when lives equals 0 game over
when lives < 3 show warning
```

### Time Events

```levlang
after 60sec game over
after 30sec spawn boss
```

---

## 🎨 UI Elements

### Display Score

```levlang
show score at top left
show score at top center
show score at top right
show score at bottom left
show score at bottom center
show score at bottom right
```

### Display Lives

```levlang
show lives at top left
show lives at top right
```

### Display Timer

```levlang
show timer at top center
countdown from 60
```

### Display Health

```levlang
show health bar at bottom
show health at top left
```

### Messages

```levlang
show message "Get Ready!" for 3sec
show message "Level Complete!" at center
show message "Game Over!" at center for 5sec
```

---

## 🔊 Audio

### Sound Effects

```levlang
play sound "shoot.wav" when shoot
play sound "coin.wav" when collect
play sound "explosion.wav" when hit
play sound "jump.wav" when jump
```

### Background Music

```levlang
play music "bgm.mp3" loop
play music "level1.mp3"
stop music
```

### Volume Control

```levlang
music volume 0.5                  // 50% volume
sound volume 0.8                  // 80% volume
```

---

## 🎚️ Levels

### Level Setup

```levlang
level 1 background "bg1.png"
level 1 music "music1.mp3"
level 2 enemies speed 5
level 2 background "bg2.png"
```

### Level Progression

```levlang
next level when score > 100
next level when enemies cleared
win game when level 5 complete
```

---

## 🚀 Advanced Features

### Variables

```levlang
set speed to 5
set lives to 3
increase speed by 1
decrease lives by 1
```

### Conditionals

```levlang
if score > 50 spawn boss
if lives < 2 show warning
if time < 10 play urgent music
```

### Custom Positions

```levlang
spawn enemy at 400,100
move player to 200,300
```

### Visual Effects

```levlang
shake screen
flash screen white
fade to black
particle explosion at enemy
```

### Game Control

```levlang
pause game
resume game
restart game
game over
win game
```

---

## 📝 Comments

```levlang
// This is a single-line comment

/* This is a
   multi-line comment */
```

---

## 🎯 Complete Example

```levlang
// Space Shooter Game
game "Space Shooter" 800x600 black

// Player setup
player moves with arrows
player shoots with space
player sprite "ship.png"
player at bottom center
player speed 7

// Enemy setup
enemies spawn every 2sec at top
enemies move down
enemies speed 3
enemies sprite "alien.png"
enemies shoot randomly

// Collectibles
powerups spawn every 10sec
powerups give shield
powerups last 5sec

coins spawn every 5sec
coins worth 10

// Events
when bullet hits enemy score +10
when enemy hits player lives -1
when player hits coin score +10
when lives equals 0 game over
when score reaches 100 next level

// UI
show score at top left
show lives at top right
show message "Destroy the aliens!" for 3sec

// Audio
play music "bgm.mp3" loop
play sound "shoot.wav" when shoot
play sound "explosion.wav" when hit
```

---

## 🔍 Keyword Reference

### Game Keywords
- `game` - Game declaration
- `player` - Player definition
- `enemies` - Enemy definition
- `coins` - Coin definition
- `powerups` - Power-up definition

### Action Keywords
- `moves` - Movement
- `shoots` - Shooting
- `jumps` - Jumping
- `spawn` - Spawning
- `show` - Display UI
- `play` - Play audio

### Event Keywords
- `when` - Event trigger
- `if` - Conditional
- `after` - Time delay

### Direction Keywords
- `up`, `down`, `left`, `right`
- `top`, `bottom`, `center`
- `random`, `towards`, `away`

### Property Keywords
- `speed` - Movement speed
- `sprite` - Image file
- `size` - Dimensions
- `health` - Health points
- `worth` - Point value

---

## 💡 Best Practices

1. **Use descriptive game titles**
2. **Comment your code**
3. **Start with simple mechanics**
4. **Test frequently**
5. **Use consistent spacing**
6. **Group related commands**
7. **Keep it readable**

---

## 🐛 Common Mistakes

### ❌ Wrong
```levlang
game My Game              // Missing quotes
player move with arrow    // Wrong keyword (moves, not move)
enemy spawn every 2sec    // Wrong keyword (enemies, not enemy)
```

### ✅ Correct
```levlang
game "My Game"
player moves with arrows
enemies spawn every 2sec
```

---

**Need more help?** Check out:
- [Getting Started Guide](getting-started.md)
- [Game Examples](examples.md)
- [Tutorial: Space Shooter](tutorial-space-shooter.md)

[← Back to Getting Started](getting-started.md) | [Examples →](examples.md)
