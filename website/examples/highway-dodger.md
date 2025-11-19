# Example: Highway Dodger

- **Syntax style**: Block/shape-based DSL
- **Concepts**: lane locking, script spawner, overlay UI.

```levlang
game {
  shape: viewport
  title: "Highway Dodger"
  size: 900x520
  background: "#0c0f16"
}

road { lanes: 4 }

player {
  shape: rectangle
  color: cyan
  size: 50x80
  controls: wasd_arrows
  speed: 8
  start_position: center_bottom
  lane_lock: 4
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

enemy_spawner {
  shape: script
  target: enemy
  spawn_rate: 1sec
  spawn_lane: random
}

ui {
  "Score: {score}" at topleft offset 20,20
}

gameover {
  shape: overlay
  "CRASHED!"
  "Score: {score}"
  "Press SPACE to restart"
}
```

### Run It
```bash
levlang run useableexamples/car.lvl
```
