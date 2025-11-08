# Game Language Transpiler - Design Document

## Overview

The Game Language Transpiler is a source-to-source compiler that converts simplified game development syntax into Python code using pygame. The system follows a traditional compiler pipeline architecture: lexical analysis → parsing → semantic analysis → code generation. The design prioritizes simplicity, clear error messages, and maintainability.

## Architecture

### High-Level Architecture

```
Source File (.game) → Lexer → Parser → AST → Code Generator → Python File (.py)
                                ↓
                         Semantic Analyzer
                                ↓
                          Error Reporter
```

### Component Overview

1. **Lexer (Tokenizer)**: Converts raw source text into tokens
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
3. **Semantic Analyzer**: Validates the AST and enriches it with type information
4. **Code Generator**: Traverses the AST and emits Python/pygame code
5. **Error Reporter**: Collects and formats error messages with source locations
6. **CLI Interface**: Provides command-line access to transpilation functionality

## Components and Interfaces

### 1. Lexer

**Purpose**: Tokenize source code into a stream of tokens

**Interface**:
```python
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str, filename: str)
    def tokenize(self) -> List[Token]
    def peek_char(self) -> str
    def advance(self) -> str
```

**Key Responsibilities**:
- Recognize keywords, identifiers, literals, operators
- Track line and column numbers for error reporting
- Handle whitespace and comments
- Detect invalid characters

**Token Types**:
- Keywords: `game`, `sprite`, `scene`, `on`, `when`, `update`, `draw`, `input`
- Identifiers: Variable and function names
- Literals: Numbers, strings, booleans
- Operators: `=`, `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, etc.
- Delimiters: `{`, `}`, `(`, `)`, `,`, `:`, `.`

### 2. Parser

**Purpose**: Build an Abstract Syntax Tree from tokens

**Interface**:
```python
class ASTNode:
    node_type: str
    location: SourceLocation

class Parser:
    def __init__(self, tokens: List[Token])
    def parse(self) -> ProgramNode
    def parse_statement(self) -> ASTNode
    def parse_expression(self) -> ASTNode
```

**AST Node Types**:
- `ProgramNode`: Root node containing all top-level declarations
- `GameNode`: Game configuration and initialization
- `SpriteNode`: Sprite definition with properties and methods
- `SceneNode`: Scene definition with update/draw logic
- `EventHandlerNode`: Input event handlers
- `ExpressionNode`: Expressions (binary ops, function calls, literals)
- `StatementNode`: Statements (assignments, conditionals, loops)

**Grammar Highlights** (simplified):
```
program := declaration*
declaration := game_decl | sprite_decl | scene_decl | python_block
game_decl := 'game' identifier '{' game_property* '}'
sprite_decl := 'sprite' identifier '{' sprite_member* '}'
scene_decl := 'scene' identifier '{' scene_member* '}'
```

### 3. Semantic Analyzer

**Purpose**: Validate AST semantics and enrich with type information

**Interface**:
```python
class SemanticAnalyzer:
    def __init__(self, ast: ProgramNode)
    def analyze(self) -> AnalyzedAST
    def check_types(self, node: ASTNode) -> None
    def resolve_symbols(self, node: ASTNode) -> None
```

**Key Validations**:
- Undefined variable/sprite/scene references
- Type compatibility in expressions
- Duplicate declarations
- Invalid event handler signatures
- Scope resolution

### 4. Code Generator

**Purpose**: Generate Python/pygame code from validated AST

**Interface**:
```python
class CodeGenerator:
    def __init__(self, ast: AnalyzedAST)
    def generate(self) -> str
    def emit_imports(self) -> str
    def emit_class(self, node: SpriteNode) -> str
    def emit_game_loop(self, node: SceneNode) -> str
```

**Code Generation Strategy**:
- Sprites → Python classes inheriting from `pygame.sprite.Sprite`
- Scenes → Functions containing game loop logic
- Event handlers → Conditional blocks in event loop
- Game config → Initialization code with pygame.init(), display setup
- Expressions → Direct Python expressions

**Template Structure**:
```python
# Generated file header
import pygame
import sys

# Generated sprite classes
class GeneratedSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # ... generated initialization

# Generated game initialization
def main():
    pygame.init()
    # ... generated setup
    
    # Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        # Event handling
        for event in pygame.event.get():
            # ... generated event handlers
        
        # Update logic
        # ... generated update code
        
        # Draw logic
        # ... generated draw code
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

### 5. Error Reporter

**Purpose**: Collect and format compilation errors

**Interface**:
```python
class CompilationError:
    message: str
    location: SourceLocation
    error_type: ErrorType

class ErrorReporter:
    def report_error(self, error: CompilationError) -> None
    def has_errors(self) -> bool
    def format_errors(self) -> str
```

**Error Message Format**:
```
error: undefined sprite 'Player'
  --> game.game:15:10
   |
15 |     spawn Player at (100, 100)
   |           ^^^^^^
```

### 6. CLI Interface

**Purpose**: Provide command-line access to transpiler

**Interface**:
```python
class CLI:
    def transpile_file(self, input_path: str, output_path: str) -> int
    def watch_mode(self, input_path: str, output_path: str) -> None
    def version(self) -> str
```

**Commands**:
- `gamelang transpile <input.game> -o <output.py>`: Transpile single file
- `gamelang watch <input.game> -o <output.py>`: Watch mode with auto-transpile
- `gamelang run <input.game>`: Transpile and execute
- `gamelang --version`: Show version

## Data Models

### Source Location
```python
@dataclass
class SourceLocation:
    filename: str
    line: int
    column: int
    length: int
```

### Token
```python
@dataclass
class Token:
    type: TokenType
    value: str
    location: SourceLocation
```

### AST Nodes (Examples)

```python
@dataclass
class SpriteNode(ASTNode):
    name: str
    properties: Dict[str, ExpressionNode]
    methods: List[MethodNode]
    location: SourceLocation

@dataclass
class EventHandlerNode(ASTNode):
    event_type: str  # 'keydown', 'keyup', 'mousedown', etc.
    condition: Optional[ExpressionNode]  # e.g., key == 'SPACE'
    body: List[StatementNode]
    location: SourceLocation
```

## Language Syntax Examples

### Example 1: Simple Game with Sprite

**Game Language**:
```
game MyGame {
    title = "My First Game"
    width = 800
    height = 600
}

sprite Player {
    image = "player.png"
    x = 400
    y = 300
    speed = 5
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
    }
}

scene Main {
    player = Player()
    
    update {
        // Game logic here
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
    }
}
```

**Generated Python** (simplified):
```python
import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.x = 400
        self.y = 300
        self.speed = 5
        self.rect.center = (self.x, self.y)
    
    def handle_keydown(self, key):
        if key == pygame.K_LEFT:
            self.x = self.x - self.speed
        if key == pygame.K_RIGHT:
            self.x = self.x + self.speed
        self.rect.center = (self.x, self.y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My First Game")
    clock = pygame.time.Clock()
    
    player = Player()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.handle_keydown(pygame.key.name(event.key).upper())
        
        # Update
        pass
        
        # Draw
        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

## Error Handling

### Compilation Errors

**Strategy**: Collect all errors during each phase, report them together

**Error Categories**:
1. **Lexical Errors**: Invalid characters, unterminated strings
2. **Syntax Errors**: Unexpected tokens, missing delimiters
3. **Semantic Errors**: Undefined references, type mismatches
4. **Warning**: Unused variables, deprecated syntax

**Error Recovery**: 
- Lexer: Skip invalid character, continue tokenizing
- Parser: Synchronize at statement boundaries
- Semantic: Continue checking other nodes

### Runtime Errors

**Strategy**: Generated code should handle pygame errors gracefully

**Handled Cases**:
- Missing image files → Show error message, use placeholder
- Invalid display modes → Fall back to default
- Audio initialization failures → Disable audio, continue

## Testing Strategy

### Unit Tests

**Lexer Tests**:
- Tokenize valid keywords, identifiers, literals
- Handle whitespace and comments correctly
- Report invalid characters with correct location

**Parser Tests**:
- Parse valid game/sprite/scene declarations
- Build correct AST structure
- Report syntax errors with helpful messages

**Semantic Analyzer Tests**:
- Detect undefined references
- Validate type compatibility
- Check scope resolution

**Code Generator Tests**:
- Generate valid Python syntax
- Preserve semantic meaning
- Handle edge cases (empty blocks, nested structures)

### Integration Tests

**End-to-End Tests**:
- Transpile complete game files
- Execute generated Python code
- Verify game behavior matches intent

**Test Cases**:
1. Simple sprite movement
2. Collision detection
3. Multiple scenes
4. Event handling
5. Python code blocks (passthrough)

### Performance Tests

**Benchmarks**:
- Transpile 100-line file < 100ms
- Transpile 1000-line file < 2s
- Watch mode latency < 500ms

## Implementation Notes

### File Extensions
- Source files: `.game`
- Generated files: `.py`

### Dependencies
- Python 3.8+
- pygame 2.0+
- No additional runtime dependencies for generated code

### Future Enhancements (Out of Scope)
- IDE integration with syntax highlighting
- Debugger support
- Hot reload during development
- Visual scene editor
- Asset management system
