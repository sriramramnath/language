# LevLang Error Codes Reference

This document provides a comprehensive reference for all error codes used in LevLang, helping developers understand and troubleshoot issues.

## Error Code Format

Error codes follow the pattern: `[Category][Number]`

- **V** = Validation errors (V001-V099)
- **R** = Runtime errors (R001-R099)
- **L** = Lexical errors (L001-L099)
- **S** = Syntax errors (S001-S099)
- **E** = Semantic errors (E001-E099)
- **C** = Code generation errors (C001-C099)

---

## Validation Errors (V001-V099)

### V001: Empty Block Name
**Message:** `Block name must be a non-empty string`

**Cause:** A block was declared with an empty or null name.

**Solution:** Ensure all blocks have valid names:
```levlang
// ❌ Wrong
{
    color: red
}

// ✅ Correct
player {
    color: red
}
```

---

### V002: Block Name with Whitespace
**Message:** `Block name cannot have leading or trailing whitespace: '{name}'`

**Cause:** Block name contains leading or trailing spaces.

**Solution:** Remove whitespace from block names:
```levlang
// ❌ Wrong
 player {
    color: red
}

// ✅ Correct
player {
    color: red
}
```

---

### V003: Invalid Block Name Format
**Message:** `Invalid block name '{name}'. Must be a valid identifier`

**Cause:** Block name contains invalid characters or doesn't start with letter/underscore.

**Solution:** Use only letters, numbers, and underscores:
```levlang
// ❌ Wrong
123block {
    color: red
}

// ✅ Correct
block123 {
    color: red
}
```

---

### V004: Reserved Block Name
**Message:** `Block name '{name}' is reserved and cannot be used`

**Cause:** Attempted to use a reserved keyword as a block name.

**Solution:** Choose a different name:
```levlang
// ❌ Wrong
game {
    title: "My Game"
}

// ✅ Correct
my_game {
    title: "My Game"
}
```

---

### V005-V008: File Path Errors
**V005:** `File path must be a non-empty string`  
**V006:** `Invalid file path: {error}`  
**V007:** `File does not exist: {path}`  
**V008:** `Path is not a file: {path}`

**Cause:** Invalid or missing file path.

**Solution:** Ensure the file path is correct and the file exists.

---

### V009: Invalid Coordinate
**Message:** `Invalid {name}: must be a number or rand() expression`

**Cause:** Coordinate value is not a number or valid rand() expression.

**Solution:** Use numeric values or rand() expressions:
```levlang
// ❌ Wrong
player {
    x: "100"
    y: invalid
}

// ✅ Correct
player {
    x: 100
    y: rand(50, 750)
}
```

---

### V010: Negative Size Dimension
**Message:** `Size dimensions must be positive, got ({width}, {height})`

**Cause:** Size value is zero or negative.

**Solution:** Use positive values:
```levlang
// ❌ Wrong
player {
    size: -10
}

// ✅ Correct
player {
    size: 30
}
```

---

### V011: Size Too Large
**Message:** `Size dimensions too large (max 10000), got ({width}, {height})`

**Cause:** Size exceeds maximum allowed dimension (10000 pixels).

**Solution:** Reduce size to reasonable values.

---

### V012-V014: Size Format Errors
**V012:** `Size must be two integers, got {value}`  
**V013:** `Invalid size format '{value}'. Expected 'WxH'`  
**V014:** `Invalid size value: must be int, tuple, or 'WxH' string`

**Cause:** Invalid size format.

**Solution:** Use valid formats:
```levlang
// ✅ All valid
player {
    size: 30
    size: 50x50
    size: [100, 200]
}
```

---

### V015-V016: Color Format Errors
**V015:** `Invalid hex color: {value}`  
**V016:** `Invalid RGB color tuple: {value}`

**Cause:** Invalid color format.

**Solution:** Use valid color formats:
```levlang
// ✅ All valid
player {
    color: red
    color: #FF0000
    color: [255, 0, 0]
}
```

---

### V017: Negative Speed
**Message:** `Speed cannot be negative, got {speed}`

**Cause:** Speed value is negative.

**Solution:** Use non-negative speed:
```levlang
// ❌ Wrong
player {
    speed: -5
}

// ✅ Correct
player {
    speed: 5
}
```

---

### V018: Speed Too Large
**Message:** `Speed value too large (max 1000), got {speed}`

**Cause:** Speed exceeds maximum (1000 pixels per frame).

**Solution:** Reduce speed to reasonable values.

---

### V019: Invalid Speed Format
**Message:** `Invalid speed value: must be a number or rand() expression`

**Cause:** Speed is not a number or valid rand() expression.

**Solution:** Use numeric values or rand():
```levlang
// ✅ Valid
player {
    speed: 5
    speed: rand(3, 8)
}
```

---

## Runtime Errors (R001-R099)

### R001: Pygame Initialization Failure
**Message:** `Failed to initialize pygame: {error}`

**Cause:** Pygame failed to initialize (usually display-related).

**Solution:**
- Check if display is available (for headless systems, set `DISPLAY` environment variable)
- Ensure pygame is properly installed: `pip install pygame`
- Check system graphics drivers

---

### R002: Pygame Module Initialization Failure
**Message:** `Failed to initialize pygame: {error}`

**Cause:** Specific pygame modules failed to initialize.

**Solution:** Check pygame installation and system dependencies.

---

### R003: Display Surface Creation Failure
**Message:** `Failed to create display surface: {error}`

**Cause:** Cannot create pygame display window.

**Solution:**
- Check display permissions
- Verify screen resolution settings
- Try smaller window size

---

## Troubleshooting Guide

### Common Issues

1. **"File not found" errors**
   - Verify file path is correct
   - Check file permissions
   - Ensure file extension is `.lvl`

2. **"Invalid block name" errors**
   - Check for reserved keywords
   - Ensure no special characters
   - Verify no leading/trailing spaces

3. **"Pygame initialization failed"**
   - Install pygame: `pip install pygame`
   - Check display server (X11 on Linux)
   - Verify graphics drivers

4. **"Size too large" errors**
   - Reduce dimensions to < 10000 pixels
   - Use reasonable game window sizes

### Getting Help

If you encounter an error not listed here:

1. Check the error message for context
2. Review the source code at the reported location
3. Check [LevLang Documentation](syntax.md)
4. Report issues with error code and full error message

---

## Error Reporting

When reporting errors, please include:

- **Error Code:** (e.g., V001)
- **Full Error Message:** Complete error text
- **Source Code:** Relevant `.lvl` file snippet
- **Environment:** OS, Python version, LevLang version
- **Steps to Reproduce:** How to trigger the error

