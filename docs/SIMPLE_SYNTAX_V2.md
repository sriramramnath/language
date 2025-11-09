# LevLang Ultra-Simple Syntax v2.0

## Philosophy: Zero Boilerplate, Maximum Fun

Write games in plain English-like commands. No complex syntax, just describe what you want!

---

## 🎮 Complete Game in 5 Lines

```levlang
game "Space Shooter"
player moves with arrows shoots with space
enemies spawn every 2sec move down
when enemy hits player game over
when bullet hits enemy score +10
```

---

## 📖 Core Concepts

### 1. Game Setup (One Line!)

```levlang
game "Title"                          // Basic game
game "Title" 800x600                  // Custom size
game "Title" fullscreen               // Fullscreen
game "Title" 800x600 black            // With background color
```

### 2. Player (Natural Language)

```levlang
player moves with arrows              // Arrow keys only
player moves with wasd                // WASD only
player moves with arrows and wasd     // Both
player moves with mouse               // Follow mouse
player shoots with space              // Shooting
player jumps with space               // Jumping
player speed 5                        // Set speed
player at 400,300                     // Starting position
player sprite "player.png"            // Custom sprite
player size 50x50                     // Custom size
```

### 3. Enemies (Super Simple)

```levlang
enemies spawn every 2sec              // Auto spawn
enemies spawn at top                  // Spawn location
enemies spawn at random               // Random position
enemies move down                     // Movement
enemies move towards player           // Follow player
enemies move randomly                 // Random movement
enemies speed 3                       // Set speed
enemies sprite "enemy.png"            // Custom sprite
enemies health 3                      // Health points
```

### 4. Collectibles

```levlang
coins spawn every 5sec                // Spawn coins
coins worth 10                        // Points value
coins sprite "coin.png"               // Custom sprite
powerups spawn every 10sec            // Power-ups
powerups give speed                   // Speed boost
powerups give shield                  // Shield
powerups give weapon                  // Better weapon
```

### 5. Events (When/If)

```levlang
when player hits enemy lose life      // Collision
when player hits coin score +10       // Collect
when bullet hits enemy destroy enemy  // Destroy
when score reaches 100 next level     // Level up
when lives equals 0 game over         // Game over
if score > 50 spawn boss              // Conditional
```

### 6. UI (One-Liners)

```levlang
show score at top left                // Display score
show lives at top right               // Display lives
show timer at top center              // Display timer
show message "Get Ready!" for 3sec    // Temporary message
show health bar at bottom             // Health bar
```

### 7. Levels

```levlang
level 1 background "bg1.png"          // Level setup
level 1 music "music1.mp3"            // Background music
level 2 enemies speed 5               // Harder level
next level when score > 100           // Level progression
```

### 8. Audio

```levlang
play sound "shoot.wav" when shoot     // Sound effect
play sound "coin.wav" when collect    // Collect sound
play music "bgm.mp3" loop             // Background music
play sound "explosion.wav" when hit   // Hit sound
```

---

## 🎯 Built-in Functions

### Movement Functions
```levlang
move player left                      // Move direction
move player to 400,300                // Move to position
move player towards mouse             // Follow mouse
move player away from enemy           // Flee
rotate player towards mouse           // Rotate sprite
bounce player off walls               // Wall bounce
```

### Spawn Functions
```levlang
spawn enemy at 400,100                // Spawn at position
spawn enemy at random                 // Random spawn
spawn coin at player                  // Spawn at player
spawn explosion at enemy              // Visual effect
spawn 5 enemies                       // Spawn multiple
```

### Collision Functions
```levlang
when player touches enemy             // Touch detection
when player overlaps coin             // Overlap
when bullet hits enemy                // Hit detection
when player near enemy                // Proximity
```

### Game Control
```levlang
pause game                            // Pause
resume game                           // Resume
restart game                          // Restart
game over                             // End game
next level                            // Progress
win game                              // Victory
```

### Score & Stats
```levlang
score +10                             // Add score
score -5                              // Subtract
lives +1                              // Add life
lives -1                              // Lose life
health +20                            // Add health
health -10                            // Damage
```

### Visual Effects
```levlang
shake screen                          // Screen shake
flash screen white                    // Flash effect
fade to black                         // Fade out
zoom in                               // Zoom effect
slow motion for 2sec                  // Slow-mo
particle explosion at enemy           // Particles
```

### Timers
```levlang
wait 2sec then spawn enemy            // Delay
every 5sec spawn coin                 // Repeat
after 10sec game over                 // Timeout
countdown from 60                     // Timer
```

---

## 🎨 Complete Examples

### Example 1: Flappy Bird Clone
```levlang
game "Flappy Bird" 400x600

player sprite "bird.png"
player jumps with space
player falls with gravity

pipes spawn every 2sec
pipes move left
pipes have gap 150

when player hits pipe game over
when player passes pipe score +1
when player hits ground game over

show score at top center
```

### Example 2: Space Shooter
```levlang
game "Space Shooter" 800x600 black

player moves with arrows
player shoots with space
player sprite "ship.png"
player at bottom center

enemies spawn every 2sec at top
enemies move down
enemies shoot randomly
enemies sprite "alien.png"

powerups spawn every 10sec
powerups give shield

when bullet hits enemy score +10
when enemy hits player lives -1
when lives equals 0 game over

show score at top left
show lives at top right
play music "bgm.mp3" loop
```

### Example 3: Platformer
```levlang
game "Platformer" 800x600

player moves with arrows
player jumps with space
player has gravity
player sprite "hero.png"

platforms at 0,500 size 800x100
platforms at 200,400 size 200x20
platforms at 500,300 size 200x20

coins spawn at random platforms
coins worth 10

enemies patrol on platforms
enemies move left and right

when player touches coin score +10
when player touches enemy lives -1
when player falls off screen lives -1
when score reaches 100 win game

show score at top left
show lives at top right
```

### Example 4: Endless Runner
```levlang
game "Runner" 800x600

player at left center
player jumps with space
player has gravity
player sprite "runner.png"

obstacles spawn every 3sec at right
obstacles move left speed 5
obstacles random height

ground scrolls left

when player hits obstacle game over
every 1sec score +1

show score at top center
show message "Jump!" for 2sec at start
```

### Example 5: Puzzle Match-3
```levlang
game "Match 3" 600x600

grid 8x8 with gems
gems types red blue green yellow
gems fall with gravity

when click gem select gem
when 3 gems match destroy gems
when gems destroyed score +10

show score at top
show moves at bottom
show timer at top right

when moves equals 0 game over
when score reaches 1000 win game
```

---

## 🚀 Advanced Features (Still Simple!)

### Variables
```levlang
set speed to 5                        // Create variable
increase speed by 1                   // Increment
decrease speed by 1                   // Decrement
if speed > 10 set speed to 10         // Conditional
```

### Custom Events
```levlang
on space pressed shoot bullet         // Custom action
on mouse click spawn explosion        // Mouse event
on score 100 unlock weapon            // Milestone
on level complete show victory        // Level event
```

### Animations
```levlang
player animate walk 4 frames          // Animation
player animate idle 2 frames          // Idle animation
enemy animate attack 3 frames         // Attack animation
coin animate spin 8 frames            // Spinning
```

### Physics
```levlang
player has gravity                    // Gravity
player bounces off walls              // Bounce
player friction 0.9                   // Friction
enemy pushes player                   // Push force
```

---

## 💡 Design Principles

1. **Natural Language**: Read like English
2. **No Symbols**: Minimal punctuation
3. **Smart Defaults**: Everything just works
4. **One Line = One Action**: Clear and simple
5. **Instant Results**: See it work immediately

---

## 🎯 Next Steps

This ultra-simple syntax will be implemented in LevLang v0.2.0!

**Benefits:**
- ✅ Beginners can start in minutes
- ✅ No programming knowledge needed
- ✅ Games in 10 lines or less
- ✅ Natural language commands
- ✅ Built-in game patterns
- ✅ Zero boilerplate

**Coming Soon:**
- Visual editor for this syntax
- Drag-and-drop game builder
- Template library
- Live preview
