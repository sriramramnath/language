# LevLang Changelog

## Version 0.1.0 - Initial Release

### Features

#### Language & Syntax
- **Simple Block-Based Syntax**: Configuration-style syntax for rapid game development
  - `game` declarations with properties
  - `player` blocks with movement and speed
  - `enemy` blocks with spawning and collision rules
  - `road` blocks for scrolling backgrounds
  - `ui` blocks for text display
  - `gameover` screens
  - `spawn_rate` configuration
  
- **Advanced Declarative Syntax**: Full-featured syntax for complex games
  - `game` declarations with properties
  - `sprite` definitions with event handlers
  - `scene` definitions with update/draw loops
  - Event handlers: `on keydown`, `on keyup`, `on mousedown`, etc.

#### Transpiler
- Lexer for tokenizing source code
- Parser for building Abstract Syntax Trees (AST)
- Semantic analyzer for validation
- Code generator for Python/pygame output
- Dual parser system (simple and advanced syntax)
- Smart syntax detection

#### CLI Tool
- `levlang transpile` - Convert .lvl files to Python
- `levlang watch` - Auto-transpile on file changes
- `levlang run` - Transpile and execute in one command
- `levlang --version` - Display version information
- Branded CLI with ASCII art banner
- Caching system for faster transpilation
- Clean log output with "log:" prefix

#### Code Generation
- Clean, readable Python/pygame code
- Automatic game loop generation
- Built-in collision detection
- Input handling (keyboard and mouse)
- Pygame welcome message suppression
- Smart defaults for common patterns

#### Examples
- `car_racing.lvl` - Complete racing game with lanes
- `sprite_movement.lvl` - Basic movement example
- `space_shooter.lvl` - Space shooter game
- `event_handling.lvl` - Advanced event handling
- `collision_detection.lvl` - Collision system demo

#### Documentation
- Comprehensive README with installation guide
- Language feature documentation
- Example descriptions
- Contributing guidelines
- Syntax comparison guide

### Technical Details

**Supported Python Versions**: 3.8+
**Dependencies**: pygame 2.0+

**Project Structure**:
```
levlang/
├── core/           # AST, tokens, source location
├── lexer/          # Tokenizer
├── parser/         # Simple and advanced parsers
├── semantic/       # Semantic analysis
├── codegen/        # Code generators
└── cli/            # Command-line interface
```

### Branding
- **Name**: LevLang (Level Language)
- **Company**: Levelium Inc.
- **File Extension**: .lvl
- **CLI Command**: levlang
- **Tagline**: "Level Up Your Game Development"

### Known Limitations
- Simple syntax currently supports arcade-style games
- Advanced syntax requires more implementation
- Limited built-in game patterns (expandable)

### Future Roadmap
- More game templates (platformer, puzzle, RPG)
- Asset management system
- Sound and music support
- Particle effects
- Animation system
- Tilemap support
- Physics engine integration
- Multiplayer networking
- Mobile export
- Web export (Pygame Zero/Pygbag)

---

**Release Date**: November 9, 2025
**Created by**: Levelium Inc.
