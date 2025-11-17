# LevLang v3 Best Practices Guide

This guide provides tips for designing games effectively with the new component-based version of LevLang.

---

### 1. Think in Components

Before you write any code, think about the "things" in your game. Are there paddles? Balls? Enemy ships? Player characters? Each of these is a **component**.

- **Keep components simple and reusable.** A `paddle` component should just define what a paddle looks like and how fast it moves. Don't give it player-specific controls.
- **Bad Example (less reusable):**
  ```levlang
  component "player_paddle" {
      controls: "vertical(\"w\", \"s\")" // Now it can only be a player paddle
  }
  ```
- **Good Example (more reusable):**
  ```levlang
  component "paddle" {
      shape: "rectangle"
      size: "15x100"
      speed: 7
  }
  ```

---

### 2. Compose Your Game with Entities

Once you have your component blueprints, use the `entities` block to build your game scene. This is where you give components a specific role.

- **Create instances** of your components and give them unique names.
- **Assign `controls` and `position`** to turn a generic component into a specific character (like the player or an AI opponent).

```levlang
entities {
    // The 'player' is an instance of the 'paddle' component
    player: "paddle" {
        position: "left(20)"
        controls: "vertical(\"w\", \"s\")" // Player controls are added here
    }

    // The 'opponent' is also an instance of the same 'paddle' component
    opponent: "paddle" {
        position: "right(20)"
        controls: "ai_track(\"the_ball\")" // AI controls are added here
    }
}
```

---

### 3. Use the `game` Block for Global Rules

The `game` block is for everything that isn't a specific entity. This includes:

- **Appearance:** Background color, static drawings like a center line.
- **Rules:** How scoring works, what happens on collisions (this part of the engine is still developing).
- **UI:** Displaying scores and other information.

By keeping these separate, your code becomes much cleaner and easier to understand.

---

### 4. Debugging

When you run `levlang run <your_game>.lvl`, read the output carefully.

- **Syntax Errors:** If you get a list of errors, it means the structure of your `.lvl` file is wrong. Check your block nesting (`{ ... }`) and property formats (`key: value`).
- **Runtime Errors (Tracebacks):** If you see a Python "Traceback", it means your `.lvl` file was syntactically correct, but the logic was flawed (or you found a bug in the engine!). Read the error message; it often tells you exactly what went wrong (e.g., `AttributeError`, `NameError`).

```