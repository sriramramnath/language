# LevLang Documentation Hub

> Everything you need to build, ship, and share LevLang games—syntax, tooling, guides, and sample projects—collected in one long-form reference.

## Table of Contents
1. [Language Syntax](#language-syntax)
   - [Block Syntax](#block-syntax)
   - [Component Syntax](#component-syntax)
2. [Examples Library](#examples-library)
3. [Guides](#guides)
4. [CLI Reference](#cli-reference)
5. [VS Code Workflow](#vs-code-workflow)
6. [Contributing](#contributing)

---

## Language Syntax

### Block Syntax
LevLang's block syntax is ideal for arcade/racing/shooter prototypes. Each block is just a name with `{ ... }` properties; the runtime interprets the data directly.

```levlang
player {
  shape: rectangle
  color: cyan
  size: 50x80
  controls: wasd_arrows
  speed: 8
  start_position: center_bottom
}

enemy {
  shape: rectangle
  color: random
  size: 50x80
  direction: down
  speed: rand(4, 10)
  offscreen: destroy score+1
  on_collide player: gameover
}
```

**Supported blocks** (completely data-driven):
- Any identifier (`player`, `road`, `spawner`, `boss`, …)
- Each block can include primitive values, quoted strings, or sub-lines (e.g., gameover overlays)
- `ui { "Score: {score}" at topright offset -24,12 }` for overlay text
- `shape: script` blocks drive spawners or scripting hooks

Key properties interpreted by the runtime:
- `shape`, `color`, `size`, `sprite_sheet`, `controls`, `speed`, `lane_lock`, `direction`, `spawn_rate`, `spawn_lane`
- `start_position`: `center`, `bottom_center`, `center_bottom`, `left(20)`, etc.
- `on_collide target: action` (e.g., `on_collide enemy: gameover`)
- `offscreen: destroy score+10`

### Component Syntax
For deeper control, use the component/entity model (see `examples/pong_complete.lvl`). Structure:

```levlang
component "paddle" {
  shape: "rectangle"
  size: "15x100"
  speed: 7
}

entities {
  player_paddle: "paddle" {
    position: "left(20)"
    controls: "vertical(\"w\", \"s\")"
  }
}

game {
  background: "black"
  draw: "dashed_line(center)"
  on_event: "the_ball.offscreen_right -> player_paddle.score + 1"
}
```

- Components define reusable blueprints.
- Entities instantiate components with overrides.
- `game {}` holds rules, UI (`display: "player.score at (200, 50)"`), and draw instructions.

## Examples Library
Full walkthroughs live under [`examples/`](examples/). Highlight reel:

| Example | Genre | Highlights | File |
| --- | --- | --- | --- |
| Pong | Classic arcade | Component syntax, AI paddle tracking. | [examples/pong.md](examples/pong.md) |
| Highway Dodger | Racing | Block syntax, lane locking, spawner script. | [examples/highway-dodger.md](examples/highway-dodger.md) |
| Space Shooter | Shooter | Planned features: projectiles, generic spawners. | [examples/space-shooter.md](examples/space-shooter.md) |

_Add new markdown files per project; link them here._

## Guides
Reference guides live in [`guides/`](guides/):

- [Using the CLI](guides/cli.md)
- [Using LevLang in VS Code](guides/vscode.md)
- [Contributing](guides/contributing.md)

Each guide reads like a blog post/tutorial and can be expanded over time.

## CLI Reference
```
levlang run <game.lvl>   # transpile + execute
levlang transpile <in> -o <out.py>
levlang watch <game.lvl>
levlang --version
```

- `run`: caches transpiled output, handles level chaining automatically
- `transpile`: inspect generated Python
- `watch`: auto-regenerate on save (Ctrl+C to stop)

## VS Code Workflow
See [guides/vscode.md](guides/vscode.md) for full instructions. Quick hits:
1. Install the bundled extension (`vscode-levlang/`).
2. Use the integrated terminal for `levlang watch`.
3. Snippets: type `playerblock` or `spawner` to scaffold blocks.

## Contributing
Community contributions are welcome. Follow [guides/contributing.md](guides/contributing.md) for setup, linting, and pull-request etiquette.
