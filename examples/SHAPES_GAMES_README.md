# LevLang Games with Basic Shapes

Three classic games implemented in LevLang using only basic geometric shapes (rectangles, circles, triangles).

## Games Included

### 1. Space Shooter (`space_shooter_basic.lvl`)
- **Player**: Cyan triangle (spaceship)
- **Enemies**: Colored circles
- **Controls**: WASD or Arrow keys to move
- **Goal**: Dodge incoming enemies and rack up points

### 2. Flappy Bird (`flappy_shapes.lvl`)
- **Player**: Yellow circle (bird)
- **Obstacles**: Green rectangles (pipes)
- **Controls**: W or Up Arrow to jump/flap
- **Goal**: Navigate through gaps without hitting obstacles

### 3. Pong (`pong_shapes.lvl`)
- **Player**: White rectangle (paddle)
- **Enemies**: White rectangles (opponent paddles)
- **Controls**: W/S keys and Arrow keys
- **Goal**: Classic pong gameplay with basic shapes

## How to Run

### Transpile and Run
```bash
# Transpile a game to Python
python3 -c "from levlang.cli.cli import CLI; CLI().transpile_file('examples/space_shooter_basic.lvl', 'game.py', show_banner=False)"

# Run the generated Python file
python3 game.py
```

### Or use the pre-transpiled versions
```bash
python3 examples/space_shooter_basic.py
python3 examples/flappy_shapes.py
python3 examples/pong_shapes.py
```

## Shape Configuration

Each game uses the `shape`, `size`, and `color` properties in the player and enemy blocks:

```levlang
player {
  shape: triangle    # rectangle, circle, or triangle
  size: 40x50       # width x height
  color: cyan       # color name
}

enemy {
  shape: circle
  size: 35x35
  color: random     # or specific color
}
```

## Requirements
- Python 3.x
- pygame

Install pygame:
```bash
pip install pygame
```
