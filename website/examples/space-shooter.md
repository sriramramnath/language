# Example: Space Shooter (Future Feature)

This `.lvl` documents upcoming runtime goals: projectile systems, generic enemy spawners, and player fire events.

```levlang
component "ship" {
    shape: "triangle"
    size: "60x50"
    speed: 9
}

component "bullet" {
    shape: "rectangle"
    size: "5x15"
    speed: 12
    color: "yellow"
    behavior: "move_up"
}

entities {
    player: "ship" {
        color: "white"
        position: "bottom_center"
        controls: "horizontal"
    }
}

game {
    background: "black"
    // Future: spawn enemies with scripted patterns
    // Future: on_event(player.presses("space")) => create(bullet)
}
```

### Notes
- Requires runtime support for projectiles and scripted spawners (currently in-progress).
- Keep this file as a living spec when implementing those systems.
