# Game Language Syntax Documentation

## Overview

The Game Language is a simplified programming language designed for game development that transpiles to Python code using pygame. This document describes all language constructs, keywords, and syntax rules.

## File Extension

Game Language source files use the `.game` extension.

## Keywords

The following keywords are reserved and cannot be used as identifiers:

- `game` - Declares game configuration
- `sprite` - Declares a sprite class
- `scene` - Declares a game scene
- `on` - Declares an event handler
- `when` - Conditional event trigger
- `update` - Scene update block
- `draw` - Scene draw block
- `if` - Conditional statement
- `else` - Alternative conditional branch
- `while` - Loop statement
- `for` - Iteration statement
- `return` - Return from function
- `true` - Boolean literal
- `false` - Boolean literal
- `and` - Logical AND operator
- `or` - Logical OR operator
- `not` - Logical NOT operator

## Comments

```
// Single-line comment

/* 
   Multi-line comment
   spans multiple lines
*/
```

## Game Declaration

Declares the game configuration including window properties.

### Syntax

```
game <identifier> {
    <property> = <value>
    ...
}
```

### Properties

- `title` (string) - Window title
- `width` (number) - Window width in pixels
- `height` (number) - Window height in pixels

### Example

**Game Language:**
```
game MyGame {
    title = "My Awesome Game"
    width = 800
    height = 600
}
```

**Equivalent pygame:**
```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Awesome Game")
```

## Sprite Declaration

Declares a sprite class with properties and event handlers.

### Syntax

```
sprite <identifier> {
    <property> = <value>
    ...
    
    on <event>(<parameters>) {
        <statements>
    }
}
```

### Built-in Properties

- `image` (string) - Path to sprite image file
- `x` (number) - X coordinate
- `y` (number) - Y coordinate
- Custom properties can be added as needed

### Example

**Game Language:**
```
sprite Player {
    image = "player.png"
    x = 100
    y = 100
    speed = 5
    health = 100
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
    }
}
```

**Equivalent pygame:**
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 100
        self.speed = 5
        self.health = 100
        self.rect.center = (self.x, self.y)
    
    def handle_keydown(self, key):
        if key == pygame.K_LEFT:
            self.x = self.x - self.speed
            self.rect.center = (self.x, self.y)
```

## Scene Declaration

Declares a game scene with update and draw logic.

### Syntax

```
scene <identifier> {
    <variable> = <value>
    ...
    
    update {
        <statements>
    }
    
    draw {
        <statements>
    }
}
```

### Blocks

- `update` - Called every frame for game logic
- `draw` - Called every frame for rendering

### Example

**Game Language:**
```
scene Main {
    player = Player()
    enemy = Enemy()
    
    update {
        player.update()
        enemy.update()
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
        enemy.draw()
    }
}
```

**Equivalent pygame:**
```python
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    player = Player()
    enemy = Enemy()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        player.update()
        enemy.update()
        
        # Draw
        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
```

## Event Handlers

Event handlers respond to user input and game events.

### Syntax

```
on <event_type>(<parameters>) {
    <statements>
}
```

### Event Types

#### keydown(key)
Triggered when a key is pressed.

**Parameters:**
- `key` (string) - Key name (e.g., "LEFT", "RIGHT", "SPACE", "A", "B")

**Example:**
```
on keydown(key) {
    if key == "SPACE" {
        jump()
    }
}
```

#### keyup(key)
Triggered when a key is released.

**Parameters:**
- `key` (string) - Key name

**Example:**
```
on keyup(key) {
    if key == "SHIFT" {
        stop_running()
    }
}
```

#### mousedown(button, mx, my)
Triggered when a mouse button is pressed.

**Parameters:**
- `button` (number) - Mouse button (1=left, 2=middle, 3=right)
- `mx` (number) - Mouse X coordinate
- `my` (number) - Mouse Y coordinate

**Example:**
```
on mousedown(button, mx, my) {
    if button == 1 {
        shoot_at(mx, my)
    }
}
```

#### mouseup(button, mx, my)
Triggered when a mouse button is released.

**Parameters:**
- `button` (number) - Mouse button
- `mx` (number) - Mouse X coordinate
- `my` (number) - Mouse Y coordinate

#### mousemove(mx, my)
Triggered when the mouse moves.

**Parameters:**
- `mx` (number) - Mouse X coordinate
- `my` (number) - Mouse Y coordinate

**Example:**
```
on mousemove(mx, my) {
    crosshair_x = mx
    crosshair_y = my
}
```

## Expressions

### Literals

```
42              // Integer
3.14            // Float
"hello"         // String
true            // Boolean
false           // Boolean
```

### Operators

#### Arithmetic
```
a + b           // Addition
a - b           // Subtraction
a * b           // Multiplication
a / b           // Division
```

#### Comparison
```
a == b          // Equal
a != b          // Not equal
a < b           // Less than
a > b           // Greater than
a <= b          // Less than or equal
a >= b          // Greater than or equal
```

#### Logical
```
a and b         // Logical AND
a or b          // Logical OR
not a           // Logical NOT
```

### Member Access

```
sprite.property         // Access property
sprite.method()         // Call method
```

### Function Calls

```
function_name(arg1, arg2)
```

## Statements

### Assignment

```
variable = expression
sprite.property = expression
```

### Conditional (if/else)

```
if condition {
    statements
}

if condition {
    statements
} else {
    statements
}
```

### While Loop

```
while condition {
    statements
}
```

### For Loop

```
for variable in range(start, end) {
    statements
}
```

## Built-in Functions

### Drawing Functions

```
screen.fill(color)                          // Fill screen with color
draw_rect(color, x, y, width, height)       // Draw rectangle
draw_circle(color, x, y, radius)            // Draw circle
draw_text(text, x, y, color)                // Draw text
```

### Collision Detection

```
collides(sprite1, sprite2)                  // Check if sprites collide
```

### Utility Functions

```
random(min, max)                            // Random number
str(value)                                  // Convert to string
int(value)                                  // Convert to integer
```

## Python Code Blocks

For advanced functionality, you can embed raw Python code using special delimiters.

### Syntax

```
```python
# Raw Python code here
import math
result = math.sqrt(value)
```
```

**Note:** Python code blocks are passed through unchanged to the generated code.

## Complete Example

**Game Language:**
```
game PongGame {
    title = "Pong"
    width = 800
    height = 600
}

sprite Paddle {
    x = 50
    y = 300
    width = 20
    height = 100
    speed = 7
    
    on keydown(key) {
        if key == "UP" {
            y = y - speed
        }
        if key == "DOWN" {
            y = y + speed
        }
    }
}

sprite Ball {
    x = 400
    y = 300
    radius = 10
    vx = 5
    vy = 3
    
    update {
        x = x + vx
        y = y + vy
        
        // Bounce off top/bottom
        if y < 0 or y > 600 {
            vy = -vy
        }
    }
}

scene Main {
    paddle = Paddle()
    ball = Ball()
    score = 0
    
    update {
        ball.update()
        
        // Check collision
        if collides(paddle, ball) {
            ball.vx = -ball.vx
            score = score + 1
        }
        
        // Reset if ball goes off screen
        if ball.x < 0 {
            ball.x = 400
            ball.y = 300
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
        draw_rect((255, 255, 255), paddle.x, paddle.y, paddle.width, paddle.height)
        draw_circle((255, 255, 255), ball.x, ball.y, ball.radius)
        draw_text("Score: " + str(score), 10, 10, (255, 255, 255))
    }
}
```

## Type System

The Game Language uses dynamic typing similar to Python:

- Numbers (integers and floats)
- Strings
- Booleans
- Sprites (object references)

Type checking is performed during semantic analysis to catch common errors before code generation.

## Scope Rules

- Game-level declarations are global
- Sprite properties are instance-scoped
- Scene variables are function-scoped
- Event handler parameters are local to the handler

## Error Messages

The transpiler provides clear error messages with source location:

```
error: undefined sprite 'Plyer'
  --> game.game:15:10
   |
15 |     player = Plyer()
   |              ^^^^^
   |
   Did you mean 'Player'?
```

## Best Practices

1. **Use descriptive names** for sprites and variables
2. **Keep event handlers simple** - delegate complex logic to methods
3. **Organize code** with clear separation between sprites and scenes
4. **Comment your code** to explain game logic
5. **Test incrementally** - transpile and run frequently during development

## Limitations

- No class inheritance (sprites are independent)
- No module system (single file programs)
- Limited standard library (pygame functions only)
- No async/await or threading

For advanced features beyond these limitations, use Python code blocks to access pygame directly.
