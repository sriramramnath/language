# CodeRabbit Analysis - Round 2 Fixes

## Summary
After fixing the initial 10 issues, CodeRabbit identified 4 additional issues in the second analysis. All have been successfully fixed.

---

## Fixed Issues (Round 2)

### 1. ✅ Path Inconsistency in Documentation
**File**: `website/docs.md` (line 56)

**Issue**: Documentation referenced `useableexamples/pong.lvl` but later sections referenced `examples/` directory.

**Fix**: Updated reference to use consistent path:
```markdown
# Before
For deeper control, use the component/entity model (see `useableexamples/pong.lvl`).

# After
For deeper control, use the component/entity model (see `examples/pong_complete.lvl`).
```

---

### 2. ✅ AST Serialization Validation
**File**: `levlang/codegen/simple_generator.py` (lines 34-36)

**Issue**: Using `repr()` on AST data assumes only basic Python types. Non-serializable objects would produce invalid code like `<MyObject at 0x...>`.

**Fix**: Added JSON serialization validation before code generation:
```python
import json

def generate(self) -> str:
    """Return a python script that invokes the shared runtime."""
    # Validate that AST data is serializable
    try:
        json.dumps(self.components)
        json.dumps(self.entities)
        json.dumps(self.game)
    except (TypeError, ValueError) as e:
        raise ValueError(f"AST data is not serializable: {e}") from e
    
    script = dedent(...)
    return script + "\n"
```

**Impact**: Catches non-serializable AST data early with clear error message instead of generating invalid Python code.

---

### 3. ✅ Non-Numeric Tuple Value Handling
**File**: `levlang/runtime/simple_runtime.py` (lines 66-68)

**Issue**: Parsing color tuples with non-numeric values would raise `ValueError`, preventing the fallback from being reached.

**Fix**: Added try-except to handle non-numeric values gracefully:
```python
# Before
if isinstance(value, (tuple, list)) and len(value) >= 3:
    return tuple(int(min(255, max(0, v))) for v in value[:3])
return fallback

# After
if isinstance(value, (tuple, list)) and len(value) >= 3:
    try:
        return tuple(int(min(255, max(0, v))) for v in value[:3])
    except (TypeError, ValueError):
        return fallback
return fallback
```

**Impact**: Malformed color tuples now gracefully return fallback color instead of crashing.

---

### 4. ✅ String Literal Error Handling
**File**: `levlang/parser/block_parser.py` (lines 251-257)

**Issue**: Fallback for failed `ast.literal_eval` would silently strip quotes from malformed strings, masking syntax errors.

**Fix**: Added validation to only fallback for properly quoted strings:
```python
def _parse_string_literal(self, token: str) -> str:
    """Parse a string literal using ast.literal_eval for safe parsing."""
    try:
        return ast.literal_eval(token)
    except (ValueError, SyntaxError) as e:
        # Only fallback for simple quoted strings with matching quotes
        if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
            return token[1:-1]
        # For truly malformed strings, raise error
        raise SyntaxError(f"Malformed string literal: {token}") from e
```

**Impact**: Malformed string literals now raise clear syntax errors instead of silently producing incorrect data.

---

### 5. ✅ Cache Key Versioning and Pipeline Tracking
**File**: `levlang/cli/cli.py` (lines 160-183, 242-263)

**Issue**: Cache key based only on filename and source code had two risks:
1. Stale cache after transpiler updates
2. Incorrect cache hits after routing changes

**Fix**: Added version and pipeline to cache key:

**Part 1**: Added VERSION constant to CLI class:
```python
class CLI:
    """Command-line interface for the LevLang transpiler."""
    
    # Transpiler version - update when behavior changes to invalidate cache
    VERSION = "0.3.1"
```

**Part 2**: Updated `get_cache_key` to include version and pipeline:
```python
def get_cache_key(self, source_code: str, filename: str, pipeline: str = "") -> str:
    """Generate a deterministic cache key for a source file.
    
    Args:
        source_code: The source code content
        filename: The source file name
        pipeline: The transpiler pipeline identifier (component/blocks/advanced)
        
    Returns:
        A hex digest cache key
    """
    hasher = hashlib.sha256()
    # Include version to invalidate cache when transpiler changes
    hasher.update(self.VERSION.encode("utf-8"))
    hasher.update(b"\0")
    # Include pipeline to invalidate cache when routing changes
    hasher.update(pipeline.encode("utf-8"))
    hasher.update(b"\0")
    hasher.update(filename.encode("utf-8"))
    hasher.update(b"\0")
    hasher.update(source_code.encode("utf-8"))
    return hasher.hexdigest()
```

**Part 3**: Updated `_generate_code` to determine and pass pipeline:
```python
def _generate_code(
    self, source_code: str, filename: str, use_cache: bool = True
) -> tuple[bool, str, str]:
    # Determine pipeline for cache key
    if self._is_component_syntax(source_code):
        pipeline = "component"
    elif self._is_block_syntax(source_code):
        pipeline = "blocks"
    else:
        pipeline = "advanced"
    
    cache_key = None
    if use_cache:
        cache_key = self.get_cache_key(source_code, filename, pipeline)
        cached = self.get_cached_output(cache_key)
        if cached is not None:
            return True, cached, ""

    success, generated_code, errors = self._transpile(source_code, filename)

    if success and use_cache and cache_key:
        self.save_to_cache(cache_key, generated_code)

    return success, generated_code, errors
```

**Impact**: 
- Cache is automatically invalidated when transpiler version changes
- Cache correctly handles files that might be routed to different pipelines
- Prevents using stale or misrouted cached output

---

## Testing

All fixes have been tested:
- ✅ No linter errors in modified files
- ✅ `useableexamples/pong.lvl` transpiles successfully
- ✅ All previous functionality remains intact
- ✅ Cache invalidation works correctly with new version

## Summary Statistics (Round 2)

| Category | Count |
|----------|-------|
| Files Modified | 4 |
| Issues Fixed | 5 |
| Critical Issues | 2 |
| Potential Issues | 3 |
| Linter Errors | 0 |

## Files Modified (Round 2)

1. `website/docs.md` - Path consistency fix
2. `levlang/codegen/simple_generator.py` - AST serialization validation
3. `levlang/runtime/simple_runtime.py` - Non-numeric tuple error handling
4. `levlang/parser/block_parser.py` - String literal error handling
5. `levlang/cli/cli.py` - Cache versioning and pipeline tracking

## Combined Statistics (Both Rounds)

| Metric | Round 1 | Round 2 | Total |
|--------|---------|---------|-------|
| Issues Fixed | 10 | 5 | 15 |
| Files Modified | 5 | 5 | 8 (unique) |
| Critical Issues | 3 | 2 | 5 |
| Potential Issues | 7 | 3 | 10 |

## Version Update

Transpiler version updated from `0.3.0` to `0.3.1` to reflect these fixes and invalidate old cache entries.

