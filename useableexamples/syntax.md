# LevLang v3 Syntax Reference

LevLang v3 is a component-based language designed for rapid prototyping of simple games. You define reusable **components**, create **entities** from those components, and set the **game** rules.

---

## 1. `component` Blocks

A component is a blueprint for a game object. You define its static properties here.

**Syntax:**
```levlang
component "component_name" {
    property: value
    ...
}
```

**Core Properties:**
- `shape`: The visual shape of the component.
  - *Values:* `"rectangle"`, `"circle"`.
- `size`: The dimensions of the component.
  - *Format:* `"widthxheight"` (e.g., `"50x80"`).
- `color`: The color of the shape.
  - *Values:* `"white"`, `"black"`, `"red"`, etc.
- `speed`: A number representing the default movement speed.
- `behavior`: Defines how the component acts on its own. This is key for creating balls and other dynamic objects.
  - *Values:* `"bounce_on(\"component_name\")"`, `"move_down"`.

---

## 2. `entities` Block

The entities block is where you create the actual objects that will appear in your game by instantiating your components.

**Syntax:**
```levlang
entities {
    instance_name: "component_name" {
        // Overrides
        property: value
    }
}
```
- `instance_name`: The unique name for this specific object in the game.
- `"component_name"`: The name of the component blueprint to use.
- `{ ... }`: An optional block to override properties for this specific instance.

**Instance-Specific Properties (Overrides):**
- `position`: Sets the starting position of the entity.
  - *Values:* `"center"`, `"left(pixels)"`, `"right(pixels)"`, `"bottom_center"`.
- `controls`: Defines how the player can control this entity.
  - *Values:* `"vertical(\"w\", \"s\")"`, `"horizontal"`, `"ai_track(\"entity_name\")"`.
- You can also override any property from the original component, like `color` or `speed`.

---

## 3. `game` Block

The game block defines the global rules, appearance, and UI for your game.

**Syntax:**
```levlang
game {
    property: value
    
    ui {
        // UI rules
    }
}
```

**Core Properties:**
- `background`: Sets the screen's background color.
  - *Values:* `"black"`, `"green"`, etc.
- `draw`: Renders background elements.
  - *Values:* `"dashed_line(center)"`.
- `on_event`: Defines game logic rules. The engine currently infers scoring logic for Pong based on entity names.
  - *Example:* `on_event: "the_ball.offscreen_left -> opponent_paddle.score + 1"
- `ui { ... }`: A sub-block for defining the user interface.
  - *Example:* `display: "player_paddle.score at (200, 50)"`

```