# Language Implementation Review

## Logical Errors Identified

### Lexer (`levlang/lexer/lexer.py`)

1.  **Incorrect String Literal Tokenization**:
    -   In `tokenize_string`, the loop condition `while not self.is_at_end():` combined with `char = self.peek_char()` and `if char == quote_char:` logic is slightly flawed. If the string contains an escaped quote (e.g., `\"`), the current logic handles it correctly by consuming the backslash and then the escaped character. However, if the file ends abruptly inside a string, `is_at_end()` becomes true, the loop terminates, and it falls through to "unterminated string literal" error, which is correct.
    -   **Issue**: The `escape_map` in `tokenize_string` maps `\r` to `\r`. While valid, it's redundant. More importantly, it doesn't handle other common escapes like `\b` or `\f` if they were intended to be supported, though this is minor.
    -   **Major Issue**: The `tokenize_number` method parses `.` followed by digits as a float. However, if a number is just `.` (e.g., `1.`), it might be tokenized as an integer `1` and then a dot token, or fail if `.` is not handled as a standalone token in that context. The rcurrent logic:
        ```python
        if not self.is_at_end() and self.peek_char() == '.' and self.peek_char(1).isdigit():
        ```
        This correctly requires a digit after the dot for it to be part of the number. So `1.` would be tokenized as `NUMBER(1)` followed by `DOT`. This seems intentional but might be unexpected if users expect `1.` to be a float.

2.  **Identifier Tokenization**:
    -   `tokenize_identifier` uses `char.isalnum() or char == '_'`. This allows digits at the start of identifiers if `tokenize` calls it. However, `tokenize` checks `if char.isalpha() or char == '_':` before calling `tokenize_identifier`, so identifiers must start with a letter or underscore. This is correct.

### Parser (`levlang/parser/parser.py`)

1.  **Operator Precedence in `parse_equality_expression`**:
    -   The parser implements precedence by nesting method calls.
    -   `parse_expression` -> `parse_or_expression` -> `parse_and_expression` -> `parse_equality_expression`.
    -   `parse_equality_expression` calls `parse_comparison_expression`.
    -   `parse_comparison_expression` calls `parse_additive_expression`.
    -   `parse_additive_expression` calls `parse_multiplicative_expression`.
    -   `parse_multiplicative_expression` calls `parse_unary_expression`.
    -   This hierarchy seems correct for standard operator precedence (OR < AND < EQUALITY < COMPARISON < ADDITIVE < MULTIPLICATIVE < UNARY).

2.  **`parse_for_statement` Logic**:
    -   The parser checks for `in` keyword:
        ```python
        in_token = self.expect(TokenType.IDENTIFIER, "Expected 'in' after variable name")
        if in_token.value != "in":
             self.report_error(...)
        ```
    -   Since `in` is in the `KEYWORDS` list in `Lexer` (`'in': TokenType.IN`), the lexer should produce a `TokenType.IN` token, not `TokenType.IDENTIFIER`.
    -   **Error**: The parser expects `TokenType.IDENTIFIER` for "in", but the lexer produces `TokenType.IN`. This will cause a parse error because `expect(TokenType.IDENTIFIER)` will fail when it encounters a `TokenType.IN` token.

3.  **`parse_return_statement`**:
    -   The method was truncated in the view, but assuming standard implementation.

4.  **`parse_scene_declaration`**:
    -   It parses `update` and `draw` blocks.
    -   It also handles property assignments.
    -   It allows statements directly in the scene body?
        ```python
        # Put the token back and parse as statement
        self.position -= 1
        stmt = self.parse_statement()
        ```
    -   This seems to allow arbitrary statements at the top level of a scene, which might not be intended or supported by the code generator.

### Semantic Analyzer (`levlang/semantic/semantic_analyzer.py`)

1.  **Type Inference for Binary Operations**:
    -   In `visit_binary_op`, for arithmetic operators (`+`, `-`, `*`, `/`, `%`):
        ```python
        if left_type != Type.UNKNOWN and left_type != Type.NUMBER:
            self.report_error(...)
        ```
    -   This enforces that operands must be numbers. It doesn't support string concatenation with `+`, which is a common feature. If this is intended, it's fine, but if string concatenation is desired, this is a logical limitation.

2.  **Scope Management in `visit_sprite`**:
    -   It declares properties as variables in the sprite scope.
    -   It visits methods.
    -   In `visit_method` (and `visit_event_handler`), it enters a new scope.
    -   Standard scoping rules usually allow methods to access class/instance properties. The `SymbolTable` likely supports looking up in parent scopes.
    -   However, `visit_assignment` checks:
        ```python
        if not self.symbol_table.lookup_local(node.target):
            self.symbol_table.declare(node.target, SymbolKind.VARIABLE, node.location)
        ```
    -   This means if you assign to a variable inside a method, it declares a *new local variable* instead of assigning to the sprite property, unless `self.` is used. But the language syntax doesn't seem to require `self.` for access, only for the generated Python code.
    -   **Issue**: Assignments in methods will shadow sprite properties instead of updating them. The language design seems to imply implicit `this`/`self` access, but the semantic analyzer treats assignments as local declarations if not found locally. It should probably check if the variable exists in the parent (sprite) scope before declaring a new local one, or the language requires explicit `self`. The parser produces `AssignmentNode` with just a target string.

### Code Generator (`levlang/codegen/code_generator.py`)

1.  **`visit_assignment_statement`**:
    -   ```python
        self.emit(f"self.{node.target} = {value_code}")
        ```
    -   **Critical Error**: It *always* prefixes assignments with `self.`.
    -   This is incorrect for local variables defined inside methods (e.g., `var x = 1`).
    -   It assumes all assignments are to sprite properties.
    -   Combined with the Semantic Analyzer issue, this confirms a confusion between local variables and instance properties.
    -   If I write `x = 5` in a method:
        -   Semantic Analyzer: Declares local `x`.
        -   Code Generator: Generates `self.x = 5`.
    -   This forces all variables to be instance variables, which breaks local scoping logic (e.g., loop counters, temporary calculations).

2.  **`visit_identifier`**:
    -   ```python
        return node.name
        ```
    -   It returns the name as-is.
    -   If the identifier refers to a sprite property, it should probably be `self.name` in the generated Python code.
    -   **Critical Error**: The generator doesn't distinguish between local variables and instance properties when accessing them. It generates `x` for access but `self.x = ...` for assignment.
    -   This leads to broken code:
        ```levlang
        x = 10  // Generates: self.x = 10
        y = x   // Generates: self.y = x  (NameError: name 'x' is not defined, should be self.x)
        ```

3.  **`visit_for_statement`**:
    -   It generates `for variable in iterable:`.
    -   If `variable` is a loop variable, it should be a local variable.
    -   The `visit_assignment` logic doesn't apply here directly, but if the body contains assignments to the loop variable, they might be prefixed with `self.`.

4.  **Event Handler Calls**:
    -   In `emit_event_handler_calls`:
        ```python
        if event_type == 'keydown' or event_type == 'keyup':
            self.emit("key = pygame.key.name(event.key).upper()")
            self.emit(f"{sprite_var}.handle_{event_type}(key)")
        ```
    -   It passes `key` as a string.
    -   In `visit_event_handler_method`, it generates:
        ```python
        def handle_keydown(self, key):
        ```
    -   This matches.

5.  **Scene Logic**:
    -   Scenes have `update` and `draw` blocks.
    -   The code generator emits them in the main loop:
        ```python
        if self.scenes:
            scene = self.scenes[0]
            # ... emit update block statements ...
        ```
    -   It only handles the *first* scene (`self.scenes[0]`).
    -   **Issue**: If multiple scenes are defined, only the first one is used. There is no scene switching mechanism implemented in the generated code.

6.  **Game Loop & Display**:
    -   It uses `clock.tick(60)` hardcoded.
    -   It uses `pygame.display.flip()`.
    -   This is generally fine for a simple transpiler.

### Summary of Critical Logical Errors

1.  **Parser/Lexer Mismatch for `for` loop**: Parser expects `IDENTIFIER` for "in", Lexer produces `IN` token.
2.  **Variable Scoping & Code Generation**:
    -   Code generator prefixes *all* assignments with `self.`.
    -   Code generator *never* prefixes identifier access with `self.`.
    -   This makes it impossible to correctly use either local variables OR instance properties.
        -   Assigning `prop = 1` -> `self.prop = 1` (OK for prop, bad for local)
        -   Reading `val = prop` -> `self.val = prop` (Fails, `prop` is not defined, needs `self.prop`)
3.  **Single Scene Limitation**: Only the first scene is generated in the main loop; others are ignored.
