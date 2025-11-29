"""
Runtime helpers for LevLang's component syntax.

The SimpleCodeGenerator emits compact scripts that feed their AST into
`run_component_game`. All of the heavy lifting—pygame setup, entity management,
UI drawing, and scoring rules—lives here so that generated files stay tiny and
easy to audit.
"""

from __future__ import annotations

import os
import random
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from levlang.core.exceptions import PygameInitializationError


COLOR_MAP = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (220, 20, 60),
    "green": (34, 197, 94),
    "blue": (59, 130, 246),
    "cyan": (6, 182, 212),
    "magenta": (232, 121, 249),
    "yellow": (250, 204, 21),
    "orange": (251, 146, 60),
    "purple": (168, 85, 247),
}


def parse_size(value: Any, default: tuple[int, int] = (40, 40)) -> tuple[int, int]:
    if isinstance(value, (tuple, list)) and len(value) == 2:
        return int(value[0]), int(value[1])
    if isinstance(value, str) and "x" in value.lower():
        left, right = value.lower().split("x", 1)
        try:
            return int(left.strip()), int(right.strip())
        except ValueError:
            return default
    try:
        number = int(value)
        return number, number
    except (TypeError, ValueError):
        return default


def parse_color(value: Any, fallback: tuple[int, int, int] = (255, 255, 255)) -> tuple[int, int, int]:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in COLOR_MAP:
            return COLOR_MAP[normalized]
        if normalized.startswith("#") and len(normalized) in (7, 9):
            try:
                r = int(normalized[1:3], 16)
                g = int(normalized[3:5], 16)
                b = int(normalized[5:7], 16)
                return r, g, b
            except ValueError:
                return fallback
    if isinstance(value, (tuple, list)) and len(value) >= 3:
        try:
            return tuple(int(min(255, max(0, v))) for v in value[:3])
        except (TypeError, ValueError):
            return fallback
    return fallback


def parse_position(rule: Optional[str], rect: pygame.Rect, screen_rect: pygame.Rect) -> None:
    if not rule:
        rect.center = screen_rect.center
        return

    rule = str(rule).strip().lower()
    synonyms = {
        "center_bottom": "bottom_center",
        "bottomcenter": "bottom_center",
        "center_top": "top_center",
        "centertop": "top_center",
    }
    rule = synonyms.get(rule, rule)

    def clamp_y():
        if rect.top < screen_rect.top:
            rect.top = screen_rect.top
        if rect.bottom > screen_rect.bottom:
            rect.bottom = screen_rect.bottom

    if rule == "center":
        rect.center = screen_rect.center
    elif rule == "bottom_center":
        rect.midbottom = screen_rect.centerx, screen_rect.bottom
    elif rule == "top_center":
        rect.midtop = screen_rect.centerx, screen_rect.top
    elif rule.startswith("left(") and rule.endswith(")"):
        try:
            offset = int(rule[5:-1])
        except ValueError:
            offset = 20
        rect.midleft = screen_rect.left + offset, screen_rect.centery
        clamp_y()
    elif rule.startswith("right(") and rule.endswith(")"):
        try:
            offset = int(rule[6:-1])
        except ValueError:
            offset = 20
        rect.midright = screen_rect.right - offset, screen_rect.centery
        clamp_y()
    elif rule.startswith("top(") and rule.endswith(")"):
        try:
            offset = int(rule[4:-1])
        except ValueError:
            offset = 20
        rect.midtop = screen_rect.centerx, screen_rect.top + offset
    elif rule.startswith("bottom(") and rule.endswith(")"):
        try:
            offset = int(rule[7:-1])
        except ValueError:
            offset = 20
        rect.midbottom = screen_rect.centerx, screen_rect.bottom - offset
    else:
        rect.center = screen_rect.center


def parse_vertical_controls(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    match = re.match(r'vertical\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', value)
    if not match:
        return None
    up_key, down_key = match.groups()
    return {
        "type": "vertical",
        "up": key_from_name(up_key),
        "down": key_from_name(down_key),
    }


def parse_ai_track(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    match = re.match(r'ai_track\(\s*"([^"]+)"\s*\)', value)
    if not match:
        return None
    target = match.group(1)
    return {"type": "ai_track", "target": target}


def parse_behavior(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    match = re.match(r'bounce_on\(\s*"([^"]+)"\s*\)', value)
    if match:
        return {"type": "bounce_on", "target_component": match.group(1)}
    return None


def key_from_name(name: str) -> int:
    name = (name or "").strip().lower()
    mapping = {
        "w": pygame.K_w,
        "s": pygame.K_s,
        "a": pygame.K_a,
        "d": pygame.K_d,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "space": pygame.K_SPACE,
    }
    return mapping.get(name, pygame.K_w)


@dataclass
class RuntimeEntity:
    name: str
    component: str
    rect: pygame.Rect
    color: tuple[int, int, int]
    speed: int
    controls: Optional[Dict[str, Any]]
    ai: Optional[Dict[str, Any]]
    behavior: Optional[Dict[str, Any]]
    shape: str = "rectangle"

    def update(self, pressed, world) -> None:
        return

    def draw(self, surface: pygame.Surface) -> None:
        if self.shape == "circle":
            pygame.draw.ellipse(surface, self.color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)


class PaddleEntity(RuntimeEntity):
    kind = "paddle"

    def update(self, pressed, world) -> None:
        dy = 0
        if self.controls and self.controls.get("type") == "vertical":
            if pressed[self.controls["up"]]:
                dy -= self.speed
            if pressed[self.controls["down"]]:
                dy += self.speed
        elif self.ai and self.ai.get("type") == "ai_track":
            target = world.entities.get(self.ai["target"])
            if target:
                if self.rect.centery < target.rect.centery - 5:
                    dy += self.speed
                elif self.rect.centery > target.rect.centery + 5:
                    dy -= self.speed

        self.rect.y += dy
        if self.rect.top < world.screen_rect.top:
            self.rect.top = world.screen_rect.top
        if self.rect.bottom > world.screen_rect.bottom:
            self.rect.bottom = world.screen_rect.bottom


class BallEntity(RuntimeEntity):
    kind = "ball"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_rect: Optional[pygame.Rect] = None
        self.velocity = pygame.Vector2(self.speed, self.speed)

    def attach_world(self, world) -> None:
        self.screen_rect = world.screen_rect
        self.reset()

    def reset(self) -> None:
        if self.screen_rect:
            self.rect.center = self.screen_rect.center
        speed = max(1, self.speed)
        self.velocity = pygame.Vector2(
            random.choice((-speed, speed)),
            random.choice((-speed, speed)),
        )

    def update(self, pressed, world) -> None:
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        if self.rect.top <= world.screen_rect.top or self.rect.bottom >= world.screen_rect.bottom:
            self.velocity.y *= -1
            if self.rect.top <= world.screen_rect.top:
                self.rect.top = world.screen_rect.top
            if self.rect.bottom >= world.screen_rect.bottom:
                self.rect.bottom = world.screen_rect.bottom

        allowed_components = None
        if self.behavior and self.behavior.get("type") == "bounce_on":
            allowed_components = {self.behavior.get("target_component")}

        for entity in world.entities.values():
            if entity is self or getattr(entity, "kind", None) != "paddle":
                continue
            if allowed_components and entity.component not in allowed_components:
                continue
            if self.rect.colliderect(entity.rect):
                if self.velocity.x > 0:
                    self.rect.right = entity.rect.left
                else:
                    self.rect.left = entity.rect.right
                self.velocity.x *= -1
                break

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(surface, self.color, self.rect)


def build_entities(
    components: Dict[str, Dict[str, Any]],
    entity_defs: Dict[str, Dict[str, Any]],
    screen_rect: pygame.Rect,
) -> Dict[str, RuntimeEntity]:
    instances: Dict[str, RuntimeEntity] = {}
    for name, data in entity_defs.items():
        component_name = data.get("component")
        comp_props = dict(components.get(component_name, {}))
        overrides = dict(data.get("overrides", {}))
        props = {**comp_props, **overrides}

        width, height = parse_size(props.get("size"), default=(40, 40))
        rect = pygame.Rect(0, 0, width, height)
        parse_position(props.get("position"), rect, screen_rect)

        controls_raw = props.get("controls")
        entity_kwargs = {
            "name": name,
            "component": component_name,
            "rect": rect,
            "color": parse_color(props.get("color", "white")),
            "speed": int(props.get("speed", 5) or 5),
            "controls": parse_vertical_controls(controls_raw),
            "ai": parse_ai_track(controls_raw),
            "behavior": parse_behavior(props.get("behavior")),
            "shape": props.get("shape", "rectangle"),
        }

        cls = BallEntity if entity_kwargs["behavior"] else PaddleEntity
        entity = cls(**entity_kwargs)
        instances[name] = entity

    return instances


def parse_event_rules(raw_rules: Any) -> List[Dict[str, Any]]:
    if not raw_rules:
        return []
    if isinstance(raw_rules, str):
        raw_rules = [raw_rules]

    parsed = []
    pattern = re.compile(
        r'(?P<subject>\w+)\.(?P<condition>offscreen_(?:left|right|top|bottom))\s*->\s*'
        r'(?P<target>\w+)\.(?P<attr>\w+)\s*\+\s*(?P<amount>\d+)'
    )
    for rule in raw_rules:
        if not isinstance(rule, str):
            continue
        match = pattern.search(rule.replace('"', ''))
        if match:
            parsed.append(
                {
                    "entity": match.group("subject"),
                    "condition": match.group("condition"),
                    "target": match.group("target"),
                    "attribute": match.group("attr"),
                    "amount": int(match.group("amount")),
                }
            )
    return parsed


def parse_ui_rules(ui_lines: Any) -> List[Dict[str, Any]]:
    if not ui_lines:
        return []
    rules = []
    if not isinstance(ui_lines, list):
        ui_lines = [ui_lines]

    pattern = re.compile(
        r'(?P<entity>[\w_]+)\.(?P<attr>\w+)\s+at\s*\((?P<x>-?\d+),\s*(?P<y>-?\d+)\)'
    )
    for line in ui_lines:
        if not line:
            continue
        parts = str(line)
        if parts.startswith("display"):
            _, payload = parts.split(":", 1)
            payload = payload.strip().strip('"')
            match = pattern.search(payload)
            if match:
                rules.append(
                    {
                        "mode": "entity_attr",
                        "entity": match.group("entity"),
                        "attribute": match.group("attr"),
                        "x": int(match.group("x")),
                        "y": int(match.group("y")),
                        "size": 48,
                    }
                )
            else:
                rules.append({"mode": "text", "text": payload, "size": 32})
    return rules


class GameWorld:
    def __init__(
        self,
        components: Dict[str, Dict[str, Any]],
        entity_defs: Dict[str, Dict[str, Any]],
        game_config: Dict[str, Any],
    ):
        pygame.init()
        self.game_config = game_config or {}
        self.width, self.height = self._resolve_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.game_config.get("title", "LevLang Game"))
        self.clock = pygame.time.Clock()
        self.background = parse_color(self.game_config.get("background", "black"), (0, 0, 0))
        self.screen_rect = self.screen.get_rect()

        self.entities = build_entities(components, entity_defs, self.screen_rect)
        self.ui_rules = parse_ui_rules(self.game_config.get("ui"))
        self.event_rules = parse_event_rules(self.game_config.get("on_event"))
        self.scores = {name: 0 for name in self.entities}

        for entity in self.entities.values():
            if isinstance(entity, BallEntity):
                entity.attach_world(self)

    def _resolve_size(self) -> tuple[int, int]:
        size = self.game_config.get("size", "800x600")
        width, height = parse_size(size, default=(800, 600))
        return width, height

    def run(self) -> None:
        running = True
        fps = int(self.game_config.get("fps", 60) or 60)
        while running:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            pressed = pygame.key.get_pressed()
            for entity in self.entities.values():
                entity.update(pressed, self)

            self._apply_event_rules()

            self.screen.fill(self.background)
            self._draw_center_line()
            for entity in self.entities.values():
                entity.draw(self.screen)
            self._draw_ui()
            pygame.display.flip()

        pygame.quit()

    def _draw_center_line(self) -> None:
        draw_cmd = self.game_config.get("draw", "")
        if not isinstance(draw_cmd, str):
            return
        normalized = draw_cmd.replace('"', "").strip().lower()
        if normalized.startswith("dashed_line"):
            step = 20
            x = self.screen_rect.centerx
            for y in range(0, self.screen_rect.height, step):
                pygame.draw.rect(self.screen, COLOR_MAP["white"], (x - 2, y + 5, 4, step // 2))

    def _draw_ui(self) -> None:
        if not self.ui_rules:
            return
        font_cache: Dict[int, pygame.font.Font] = {}

        def get_font(size: int) -> pygame.font.Font:
            if size not in font_cache:
                font_cache[size] = pygame.font.Font(None, size)
            return font_cache[size]

        for rule in self.ui_rules:
            if rule["mode"] == "entity_attr":
                value = ""
                entity = self.entities.get(rule["entity"])
                if rule["attribute"] == "score":
                    value = str(self.scores.get(rule["entity"], 0))
                elif entity and hasattr(entity, rule["attribute"]):
                    value = str(getattr(entity, rule["attribute"]))
                font = get_font(rule.get("size", 48))
                surf = font.render(value, True, COLOR_MAP["white"])
                rect = surf.get_rect(center=(rule["x"], rule["y"]))
                self.screen.blit(surf, rect)
            elif rule["mode"] == "text":
                font = get_font(rule.get("size", 32))
                surf = font.render(rule["text"], True, COLOR_MAP["white"])
                rect = surf.get_rect(center=(self.width // 2, 40))
                self.screen.blit(surf, rect)

    def _apply_event_rules(self) -> None:
        for rule in self.event_rules:
            entity = self.entities.get(rule["entity"])
            if not entity or getattr(entity, "kind", None) != "ball":
                continue
            triggered = False
            if rule["condition"] == "offscreen_left" and entity.rect.right <= self.screen_rect.left:
                triggered = True
            elif rule["condition"] == "offscreen_right" and entity.rect.left >= self.screen_rect.right:
                triggered = True
            elif rule["condition"] == "offscreen_top" and entity.rect.bottom <= self.screen_rect.top:
                triggered = True
            elif rule["condition"] == "offscreen_bottom" and entity.rect.top >= self.screen_rect.bottom:
                triggered = True

            if triggered:
                if rule["attribute"] == "score":
                    self.scores[rule["target"]] = self.scores.get(rule["target"], 0) + rule["amount"]
                if isinstance(entity, BallEntity):
                    entity.reset()


def run_component_game(
    components: Dict[str, Dict[str, Any]],
    entity_defs: Dict[str, Dict[str, Any]],
    game_config: Dict[str, Any],
) -> None:
    """Entry point used by generated scripts."""
    world = GameWorld(components, entity_defs, game_config)
    world.run()


# --------------------------------------------------------------------------- #
# Block-style runtime (generalized syntax)
# --------------------------------------------------------------------------- #


def parse_control_modes(value: Optional[str]) -> Set[str]:
    """Normalize textual control specs into a set of capability tokens."""
    modes: Set[str] = set()
    if not value:
        return modes
    raw = str(value).lower()
    tokens = re.split(r'[,\s]+|_', raw)
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in {"wasd", "wasdkeys"}:
            modes.add("wasd")
        elif token in {"arrows", "arrow", "arrowkeys"}:
            modes.add("arrows")
        elif token in {"horizontal"}:
            modes.add("horizontal")
        elif token in {"vertical"}:
            modes.add("vertical")
        elif token in {"wasdarrows", "wasd-arrows"}:
            modes.add("wasd")
            modes.add("arrows")
        elif token == "wasd_arrows":
            modes.add("wasd")
            modes.add("arrows")
        else:
            modes.add(token)

    # Note: Do NOT auto-add "wasd" or "arrows" for horizontal/vertical modes
    # This would cause horizontal mode to allow vertical movement and vice versa
    # Users should explicitly set "wasd" or "arrows" if they want full movement
    return modes


class BlockEntityDefinition:
    """Immutable definition for block-style entities."""

    def __init__(self, name: str, props: Dict[str, Any]):
        self.name = name
        self.props = props or {}
        self.shape = self.props.get("shape", "rectangle")
        self.size = parse_size(
            self.props.get("sprite_size") or self.props.get("size"), default=(48, 48)
        )
        self.color = parse_color(self.props.get("color", "white"))
        self.controls = self.props.get("controls") or self.props.get("movement")
        self.direction = (
            self.props.get("direction")
            or self.props.get("move")
            or self.props.get("movement_direction")
        )
        self.start_position = self.props.get("start_position")
        self.offscreen_actions = self._parse_offscreen(self.props.get("offscreen"))
        self.on_collide_rules = self._parse_collide_rules(self.props)
        self.spawn_rule = self.props.get("spawn")
        self.spawn_rate = self.props.get("spawn_rate")
        self.spawn_lane = self.props.get("spawn_lane", "random")
        self.lane_lock = self.props.get("lane_lock")
        self.collider_box = parse_size(self.props.get("collider_box"), self.size)
        self.speed_value = self.props.get("speed", 0)

    def _parse_offscreen(self, raw: Any) -> List[str]:
        if not raw:
            return []
        if isinstance(raw, list):
            tokens: List[str] = []
            for item in raw:
                tokens.extend(self._parse_offscreen(item))
            return tokens
        text = str(raw)
        parts = []
        for piece in re.split(r"[,\s]+", text):
            piece = piece.strip()
            if piece:
                parts.append(piece)
        return parts

    def _parse_collide_rules(self, props: Dict[str, Any]) -> Dict[str, List[str]]:
        rules: Dict[str, List[str]] = {}
        for key, value in props.items():
            if not key.lower().startswith("on_collide"):
                continue
            parts = key.split()
            target = parts[1] if len(parts) > 1 else "any"
            if isinstance(value, list):
                actions = [str(v).strip() for v in value]
            else:
                actions = [str(value).strip()]
            rules[target] = actions
        return rules

    def create_instance(self, runtime: "BlockStyleGame") -> "BlockEntityInstance":
        return BlockEntityInstance(self, runtime)


class BlockEntityInstance:
    """Live entity created from a block definition."""

    def __init__(self, definition: BlockEntityDefinition, runtime: "BlockStyleGame"):
        self.definition = definition
        self.runtime = runtime
        width, height = definition.collider_box
        self.rect = pygame.Rect(0, 0, width, height)
        self.color = definition.color
        self.shape = definition.shape
        self.control_modes = parse_control_modes(definition.controls)
        self.direction = (
            definition.direction.lower() if definition.direction else None
        )
        self.speed = self._resolve_speed(definition.speed_value)
        self.active = True
        self.dynamic = bool(self.control_modes or self.direction or definition.spawn_rule)
        self._apply_start_position()
        self.lane_lock = None
        self.lane_width = None
        self.lane_index = None
        self.lane_target_x = None
        self.lane_move_timer = 0.0
        self.lane_move_cooldown = 0.15
        if definition.lane_lock:
            try:
                count = max(1, int(definition.lane_lock))
            except (TypeError, ValueError):
                count = 0
            if count > 0:
                self.lane_lock = count
                self.lane_width = self.runtime.screen_rect.width / count
                self.lane_index = max(
                    0, min(count - 1, int(self.rect.centerx / self.lane_width))
                )
                self.lane_target_x = self._lane_center(self.lane_index)
                self.rect.centerx = int(self.lane_target_x)

    def _resolve_speed(self, value: Any) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            rand_match = re.match(
                r"rand\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", value
            )
            if rand_match:
                low = float(rand_match.group(1))
                high = float(rand_match.group(2))
                return random.uniform(low, high)
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

    def _resolve_coordinate(self, value: Any) -> int:
        """Parse coordinate value, including rand() expressions."""
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            rand_match = re.match(
                r"rand\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", value
            )
            if rand_match:
                low = int(float(rand_match.group(1)))
                high = int(float(rand_match.group(2)))
                return random.randint(low, high)
            try:
                return int(value)
            except ValueError:
                return 0
        return 0
    
    def _apply_start_position(self):
        screen_rect = self.runtime.screen_rect
        rect = self.rect
        
        # Check for explicit x, y coordinates first
        x = self.definition.props.get("x")
        y = self.definition.props.get("y")
        
        if x is not None or y is not None:
            # Use explicit coordinates (center the rect at these coords)
            if x is not None:
                rect.centerx = self._resolve_coordinate(x)
            if y is not None:
                rect.centery = self._resolve_coordinate(y)
        else:
            # Fall back to start_position rules
            rule = self.definition.start_position or "center"
            parse_position(rule, rect, screen_rect)

    def update(self, dt: float, pressed) -> None:
        if not self.active:
            return
        if self.lane_lock:
            self._handle_lane_controls(dt, pressed)
        elif self.control_modes:
            self._handle_controls(dt, pressed)
        elif self.direction == "down":
            self.rect.y += int(self.speed * dt)
        elif self.direction == "up":
            self.rect.y -= int(self.speed * dt)
        elif self.direction == "left":
            self.rect.x -= int(self.speed * dt)
        elif self.direction == "right":
            self.rect.x += int(self.speed * dt)

        if not self.lane_lock:
            self.rect.clamp_ip(self.runtime.screen_rect)

    def _lane_center(self, index: int) -> int:
        return int((index + 0.5) * self.lane_width)

    def _handle_lane_controls(self, dt: float, pressed) -> None:
        dx_dir, dy_dir = self._poll_axes(pressed)
        self.lane_move_timer = max(
            0.0, self.lane_move_timer - self.runtime.last_dt_seconds
        )
        # Use threshold comparison instead of exact equality for floating-point
        timer_ready = self.lane_move_timer <= 1e-6
        if dx_dir < 0 and timer_ready:
            if self.lane_index > 0:
                self.lane_index -= 1
                self.lane_target_x = self._lane_center(self.lane_index)
                self.lane_move_timer = self.lane_move_cooldown
        elif dx_dir > 0 and timer_ready:
            if self.lane_index < self.lane_lock - 1:
                self.lane_index += 1
                self.lane_target_x = self._lane_center(self.lane_index)
                self.lane_move_timer = self.lane_move_cooldown

        if self.lane_target_x is not None:
            self.rect.centerx = int(self.lane_target_x)

        if dy_dir != 0:
            step = self.speed * dt
            self.rect.y += int(step * dy_dir)
            self.rect.clamp_ip(self.runtime.screen_rect)

    def _handle_controls(self, dt: float, pressed) -> None:
        dx_dir, dy_dir = self._poll_axes(pressed)
        step = self.speed * dt
        self.rect.x += int(step * dx_dir)
        self.rect.y += int(step * dy_dir)
        self.rect.clamp_ip(self.runtime.screen_rect)

    def _poll_axes(self, pressed) -> tuple[int, int]:
        dx = 0
        dy = 0
        modes = self.control_modes
        
        # Handle WASD horizontal keys (A/D)
        # Only for wasd mode (allows all directions) OR horizontal mode (only left/right)
        # Do NOT allow A/D in vertical mode (vertical should only allow up/down)
        if "wasd" in modes or ("horizontal" in modes and "vertical" not in modes):
            if pressed[pygame.K_a]:
                dx -= 1
            if pressed[pygame.K_d]:
                dx += 1
        
        # Handle WASD vertical keys (W/S)
        # Only for wasd mode (allows all directions) OR vertical mode (only up/down)
        # Do NOT allow W/S in horizontal mode (horizontal should only allow left/right)
        if "wasd" in modes or ("vertical" in modes and "horizontal" not in modes):
            if pressed[pygame.K_w]:
                dy -= 1
            if pressed[pygame.K_s]:
                dy += 1
        
        # Handle arrow keys (only for arrows mode)
        if "arrows" in modes:
            if pressed[pygame.K_LEFT]:
                dx -= 1
            if pressed[pygame.K_RIGHT]:
                dx += 1
            if pressed[pygame.K_UP]:
                dy -= 1
            if pressed[pygame.K_DOWN]:
                dy += 1
        
        return dx, dy

    def draw(self, surface: pygame.Surface):
        if self.shape == "circle":
            pygame.draw.ellipse(surface, self.color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)


class BlockSpawner:
    """Simple timer-driven entity spawner."""

    def __init__(
        self,
        name: str,
        definition: BlockEntityDefinition,
        interval: float,
        lane_mode: str,
        runtime: "BlockStyleGame",
    ):
        self.name = name
        self.definition = definition
        self.interval = max(0.1, interval)
        self.timer = 0.0
        self.lane_mode = lane_mode
        self.runtime = runtime

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.interval:
            self.timer -= self.interval
            entity = self.definition.create_instance(self.runtime)
            self._place_entity(entity)
            self.runtime.spawn_queue.append(entity)

    def _place_entity(self, entity: BlockEntityInstance):
        rect = entity.rect
        screen_rect = self.runtime.screen_rect
        rect.midtop = (screen_rect.centerx, screen_rect.top - rect.height)
        if self.lane_mode == "random" and self.runtime.lane_count > 0:
            lane = random.randint(0, self.runtime.lane_count - 1)
            lane_width = screen_rect.width / self.runtime.lane_count
            rect.centerx = int((lane + 0.5) * lane_width)
        elif self.lane_mode == "center":
            rect.centerx = screen_rect.centerx


class BlockStyleGame:
    """Runtime for generalized block syntax."""

    def __init__(self, ast: Dict[str, Any]):
        """Initialize the block-style game runtime.
        
        Args:
            ast: The parsed AST dictionary containing game data
            
        Raises:
            PygameInitializationError: If pygame fails to initialize
            ValueError: If game configuration is invalid
        """
        import sys
        
        # Initialize pygame with error handling
        try:
            pygame_init_result = pygame.init()
            if pygame_init_result[1] > 0:
                print(f"Warning: {pygame_init_result[1]} pygame module(s) failed to initialize", file=sys.stderr)
        except Exception as e:
            raise PygameInitializationError(
                f"Failed to initialize pygame: {e}",
                error_code="R002"
            ) from e
        
        self.ast = ast or {}
        self.blocks = self.ast.get("blocks", {})
        self.globals = self.ast.get("globals", {})
        self.ui_rules = [rule for group in self.ast.get("ui", []) for rule in group]
        self.viewport = self._find_viewport()
        
        # Validate and set screen size
        try:
            size_str = self.viewport.get("size", "960x540")
            self.width, self.height = parse_size(size_str, default=(960, 540))
            if self.width <= 0 or self.height <= 0:
                raise ValueError(f"Invalid screen size: {self.width}x{self.height}")
        except (ValueError, TypeError) as e:
            print(f"Warning: Invalid size '{size_str}', using default 960x540", file=sys.stderr)
            self.width, self.height = 960, 540
        
        # Create display surface with error handling
        try:
            self.screen = pygame.display.set_mode((self.width, self.height))
        except pygame.error as e:
            raise PygameInitializationError(
                f"Failed to create display surface: {e}",
                error_code="R003"
            ) from e
        
        # Set window title
        title = self.viewport.get("title") or self.viewport.get("name") or "LevLang Game"
        try:
            pygame.display.set_caption(str(title))
        except Exception:
            pass  # Non-critical, continue
        
        self.clock = pygame.time.Clock()
        self.background = parse_color(self.viewport.get("background", "#101820"))
        self.screen_rect = self.screen.get_rect()
        self.fps = 60
        self.entities: List[BlockEntityInstance] = []
        self.spawn_queue: List[BlockEntityInstance] = []
        self.spawners: List[BlockSpawner] = []
        self.entity_definitions: Dict[str, BlockEntityDefinition] = {}
        self.overlay = self._find_overlay()
        self.score = 0
        self.game_over = False
        self.font_cache: Dict[int, pygame.font.Font] = {}
        self.lane_count = self._resolve_lane_count()
        self.last_dt_seconds = 0.0
        
        # Debug mode for pygame blocks (enables traceback on errors)
        self._debug_mode = self.globals.get("debug", False)
        
        # Build entity definitions with error handling
        try:
            self._build_definitions()
        except Exception as e:
            print(f"Warning: Error building entity definitions: {e}", file=sys.stderr)
            # Continue with empty definitions rather than crashing

    def _find_viewport(self) -> Dict[str, Any]:
        # First check for explicit viewport blocks
        for props in self.blocks.values():
            if props.get("shape") == "viewport":
                return props
        # Fall back to "game" block if it exists
        if "game" in self.blocks:
            return self.blocks["game"]
        return {}

    def _find_overlay(self) -> Optional[Dict[str, Any]]:
        for props in self.blocks.values():
            if props.get("shape") == "overlay":
                return props
        return None

    def _resolve_lane_count(self) -> int:
        lane_count = 0
        for props in self.blocks.values():
            if "lanes" in props:
                try:
                    lane_count = max(lane_count, int(props["lanes"]))
                except ValueError:
                    continue
        return lane_count

    def _build_definitions(self):
        for name, props in self.blocks.items():
            shape = props.get("shape")
            # Skip special blocks that aren't entities
            if shape in {"viewport", "overlay"} or name == "game":
                continue
            definition = BlockEntityDefinition(name, props)
            self.entity_definitions[name] = definition
            should_spawn = bool(
                definition.controls
                or definition.start_position
                or not definition.spawn_rule
            )
            if should_spawn and shape != "script":
                self.entities.append(definition.create_instance(self))

            if shape == "script" and props.get("target"):
                target_name = props["target"]
                target_def = self.entity_definitions.get(target_name)
                if target_def is None and target_name in self.blocks:
                    target_def = BlockEntityDefinition(target_name, self.blocks[target_name])
                    self.entity_definitions[target_name] = target_def
                if target_def:
                    interval = self._parse_time(props.get("spawn_rate", "2sec"))
                    lane_mode = props.get("spawn_lane", "random")
                    self.spawners.append(
                        BlockSpawner(name, target_def, interval, lane_mode, self)
                    )
            elif definition.spawn_rule or definition.spawn_rate:
                interval = self._parse_time(
                    definition.spawn_rate or self.globals.get("spawn_rate", "2sec")
                )
                lane_mode = definition.spawn_rule or "random"
                self.spawners.append(
                    BlockSpawner(name, definition, interval, lane_mode, self)
                )

    def _parse_time(self, raw: Any) -> float:
        if isinstance(raw, (int, float)):
            return float(raw)
        if isinstance(raw, str):
            match = re.match(r"(\d+(?:\.\d+)?)\s*(?:s|sec|secs)?", raw.lower())
            if match:
                return float(match.group(1))
            try:
                return float(raw)
            except ValueError:
                return 1.0
        return 1.0

    def run(self):
        running = True
        while running:
            elapsed_ms = self.clock.tick(self.fps)
            dt = elapsed_ms / 16.666
            self.last_dt_seconds = elapsed_ms / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            pressed = pygame.key.get_pressed()
            if not self.game_over:
                for spawner in self.spawners:
                    spawner.update(dt)
                if self.spawn_queue:
                    self.entities.extend(self.spawn_queue)
                    self.spawn_queue = []

                for entity in list(self.entities):
                    entity.update(dt, pressed)
                    if self._handle_offscreen(entity):
                        self.entities.remove(entity)

                self._handle_collisions()

            self._draw()

        pygame.quit()

    def _handle_offscreen(self, entity: BlockEntityInstance) -> bool:
        rect = entity.rect
        offscreen = (
            rect.top > self.screen_rect.bottom
            or rect.bottom < self.screen_rect.top
            or rect.right < self.screen_rect.left
            or rect.left > self.screen_rect.right
        )
        if not offscreen:
            return False

        for action in entity.definition.offscreen_actions:
            if action == "destroy":
                entity.active = False
            elif action.startswith("score+"):
                try:
                    delta = int(action.split("+", 1)[1])
                    self.score += delta
                except ValueError:
                    continue
        return True

    def _handle_collisions(self):
        for i, entity in enumerate(self.entities):
            for other in self.entities[i + 1 :]:
                if entity.rect.colliderect(other.rect):
                    self._apply_collision(entity, other)
                    self._apply_collision(other, entity)

    def _apply_collision(self, source: BlockEntityInstance, target: BlockEntityInstance):
        for key in (target.definition.name, "any"):
            actions = source.definition.on_collide_rules.get(key)
            if not actions:
                continue
            for action in actions:
                self._apply_action(action, source, target)

    def _apply_action(
        self, action: str, source: BlockEntityInstance, target: BlockEntityInstance
    ):
        normalized = (action or "").strip().lower().replace("_", "")
        if not normalized:
            return
        if normalized == "gameover":
            self.game_over = True
        elif normalized == "destroy":
            target.active = False
            if target in self.entities:
                self.entities.remove(target)
        elif normalized.startswith("score+"):
            try:
                delta = int(normalized.split("+", 1)[1])
                self.score += delta
            except ValueError:
                return

    def _draw_road(self):
        if self.lane_count <= 0:
            return
        lane_width = self.screen_rect.width / self.lane_count
        for lane in range(1, self.lane_count):
            x = int(lane * lane_width)
            pygame.draw.line(
                self.screen,
                COLOR_MAP["white"],
                (x, 0),
                (x, self.screen_rect.height),
                1,
            )

    def _draw_ui(self):
        for rule in self.ui_rules:
            text = rule.get("text", "")
            text = text.replace("{score}", str(self.score))
            size = rule.get("size", 28)
            font = self._get_font(size)
            surface = font.render(text, True, COLOR_MAP["white"])
            rect = surface.get_rect()
            anchor = rule.get("anchor", "topleft").lower()
            offset = rule.get("offset", (0, 0))

            if anchor == "topleft":
                rect.topleft = (10 + offset[0], 10 + offset[1])
            elif anchor == "topright":
                rect.topright = (
                    self.screen_rect.width - 10 + offset[0],
                    10 + offset[1],
                )
            elif anchor == "center":
                rect.center = (
                    self.screen_rect.centerx + offset[0],
                    self.screen_rect.centery + offset[1],
                )
            else:
                rect.topleft = (10 + offset[0], 10 + offset[1])

            self.screen.blit(surface, rect)

    def _draw_overlay(self):
        if not self.game_over or not self.overlay:
            return
        surface = pygame.Surface(self.screen_rect.size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 180))
        self.screen.blit(surface, (0, 0))
        lines = self.overlay.get("_lines", [])
        y = self.screen_rect.centery - len(lines) * 24
        for line in lines:
            text = line.replace("{score}", str(self.score))
            font = self._get_font(42)
            rendered = font.render(text, True, COLOR_MAP["white"])
            rect = rendered.get_rect(center=(self.screen_rect.centerx, y))
            self.screen.blit(rendered, rect)
            y += 48

    def _get_font(self, size: int) -> pygame.font.Font:
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]

    def _draw(self):
        self.screen.fill(self.background)
        self._draw_road()
        for entity in self.entities:
            entity.draw(self.screen)
        self._draw_ui()
        
        # Call pygame blocks if any are defined
        self._call_pygame_blocks()
        
        self._draw_overlay()
        pygame.display.flip()
    
    def _call_pygame_blocks(self):
        """Call any custom pygame code blocks defined in the game.
        
        Handles errors gracefully to prevent one bad block from crashing the game.
        """
        pygame_blocks = self.ast.get("pygame_blocks", [])
        if not pygame_blocks:
            return
        
        # Get the global namespace where pygame block functions are defined
        import sys
        import traceback
        
        # Try to get the caller's globals (where the pygame blocks are defined)
        frame = sys._getframe()
        while frame:
            if "BLOCK_DATA" in frame.f_globals and any(name in frame.f_globals for name in pygame_blocks):
                # Found the module with pygame blocks
                for block_name in pygame_blocks:
                    if block_name in frame.f_globals:
                        func = frame.f_globals[block_name]
                        try:
                            func(self.screen, self.clock, self.entities)
                        except pygame.error as e:
                            # Pygame-specific errors (e.g., display surface issues)
                            # Log each error independently - don't suppress subsequent errors
                            print(f"Warning: Pygame error in block '{block_name}': {e}", file=sys.stderr)
                        except Exception as e:
                            # Other errors - log each error independently
                            print(f"Error in pygame block '{block_name}': {e}", file=sys.stderr)
                            if self._debug_mode:
                                traceback.print_exc()
                break
            frame = frame.f_back


def run_block_game(ast: Dict[str, Any]) -> None:
    """Entry point for the generalized block syntax runtime.
    
    Args:
        ast: The parsed AST dictionary containing game data
        
    Raises:
        PygameInitializationError: If pygame fails to initialize
        RuntimeError: If game data is invalid or corrupted
    """
    import sys
    
    try:
        # Initialize pygame with error handling
        pygame_init_success = pygame.init()
        if pygame_init_success[1] > 0:  # Number of failed modules
            print(f"Warning: {pygame_init_success[1]} pygame module(s) failed to initialize", file=sys.stderr)
        
        # Validate AST structure
        if not isinstance(ast, dict):
            raise RuntimeError("Invalid AST: expected dictionary")
        
        if "blocks" not in ast:
            raise RuntimeError("Invalid AST: missing 'blocks' key")
        
        # Create and run game
        game = BlockStyleGame(ast)
        game.run()
        
    except pygame.error as e:
        raise PygameInitializationError(
            f"Failed to initialize pygame: {e}",
            error_code="R001"
        ) from e
    except KeyboardInterrupt:
        # User pressed Ctrl+C - graceful shutdown
        print("\nGame interrupted by user", file=sys.stderr)
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        # Unexpected error - log and re-raise
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        pygame.quit()
        raise