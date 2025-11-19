# Example: Pong

- **Syntax style**: Component/entities
- **Concepts**: reusable components, AI paddles, event-driven scoring.

```levlang
component "paddle" {
    shape: "rectangle"
    size: "15x100"
    speed: 7
}

component "ball" {
    shape: "circle"
    size: "20x20"
    speed: 7
    behavior: "bounce_on(\"paddle\")"
}

entities {
    player_paddle: "paddle" { position: "left(20)", controls: "vertical(\"w\", \"s\")" }
    opponent_paddle: "paddle" { position: "right(20)", controls: "ai_track(\"the_ball\")" }
    the_ball: "ball" { position: "center" }
}

game {
    background: "black"
    draw: "dashed_line(center)"
    on_event: "the_ball.offscreen_left -> opponent_paddle.score + 1"
    on_event: "the_ball.offscreen_right -> player_paddle.score + 1"
    ui {
        display: "player_paddle.score at (200, 50)"
        display: "opponent_paddle.score at (600, 50)"
    }
}
```

### How to Run
```bash
levlang run useableexamples/pong.lvl
```
