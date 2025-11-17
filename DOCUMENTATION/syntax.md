# LevLang Syntax Reference

LevLang uses a simple, block-based syntax to declare game elements.

## Top-Level Declarations

### `game "Title"`
Sets the title of the game window.
```levlang
game "My Awesome Game"
```

### `spawn_rate: <time>`
Sets how often enemies appear. Time can be in seconds (`s` or `sec`) and can be a decimal.
```levlang
spawn_rate: 2.5sec
```

### `start()`
Tells the transpiler to generate the main loop and run the game. This should be at the end of the file.

## Blocks

Blocks are defined by a name followed by `{ ... }`.

### `player { ... }`
Defines the player character.

**Properties:**
- `shape`: `rectangle`, `circle`, `triangle`. Used if `frames` is not set.
- `color`: `blue`, `red`, `green`, `white`, `black`, `random`, etc.
- `size`: `widthxheight` (e.g., `50x80`).
- `frames`: Path to a directory of images for animation (e.g., `"assets/player/"`). This overrides shape properties.
- `speed`: A number representing movement speed.
- `movement`: `wasd_arrows` (default).

### `enemy { ... }`
Defines the enemy/obstacle characters.

**Properties:**
- All `player` properties.
- `spawn`: `random_lane` (for top-down games).
- `move`: `down` (moves from top to bottom).
- `offscreen`: Action to take when offscreen. e.g., `destroy, score+10`.
- `collide`: Action to take on collision with player. e.g., `gameover`.

### `road { ... }`
Defines the road for racing games.

**Properties:**
- `lanes`: Number of lanes (e.g., `3`).
- `scrolling`: `true` to make the lane lines move.

### `ui { ... }`
Defines user interface text.

**Syntax:**
`"Text"` at `position`
- `position`: `topleft`, `topright`, `center`.
- You can use `{score}` to display the player's score.

### `gameover { ... }`
Defines the text to show on the game over screen. You can also specify the next level to load.

**Properties:**
- `"Text"`: A string to display on separate lines.
- `next_level`: `"path/to/next.lvl"` (optional). When the game ends, this level will be loaded.
