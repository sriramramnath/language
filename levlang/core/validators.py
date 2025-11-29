"""
Input validation utilities for LevLang.

This module provides validation functions to ensure inputs are safe,
well-formed, and within acceptable ranges before processing.
"""

import re
from pathlib import Path
from typing import Any, Optional, Tuple

from levlang.core.exceptions import ValidationError
from levlang.core.source_location import SourceLocation


# Reserved block names that cannot be used by users
RESERVED_BLOCK_NAMES = {
    'game', 'ui', 'overlay', 'viewport', 'start', 'component', 'entities',
    'python', 'pygame', 'import', 'from', 'def', 'class', 'if', 'while',
    'for', 'return', 'break', 'continue', 'pass', 'try', 'except', 'finally'
}

# Valid identifier pattern (alphanumeric + underscore, must start with letter/underscore)
VALID_IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

# Valid color formats
COLOR_HEX_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$|^#[0-9A-Fa-f]{8}$')


def validate_block_name(name: str, location: Optional[SourceLocation] = None) -> None:
    """Validate a block name.
    
    Args:
        name: The block name to validate
        location: Source location for error reporting
        
    Raises:
        ValidationError: If block name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationError(
            f"Block name must be a non-empty string",
            location=location,
            error_code="V001"
        )
    
    if name.strip() != name:
        raise ValidationError(
            f"Block name cannot have leading or trailing whitespace: '{name}'",
            location=location,
            error_code="V002"
        )
    
    if not VALID_IDENTIFIER_PATTERN.match(name):
        raise ValidationError(
            f"Invalid block name '{name}'. Must be a valid identifier (letters, numbers, underscore, starting with letter/underscore)",
            location=location,
            error_code="V003"
        )
    
    if name.lower() in RESERVED_BLOCK_NAMES:
        raise ValidationError(
            f"Block name '{name}' is reserved and cannot be used",
            location=location,
            error_code="V004"
        )


def validate_file_path(path: str, must_exist: bool = False) -> Path:
    """Validate a file path.
    
    Args:
        path: The file path to validate
        must_exist: If True, file must exist
        
    Returns:
        Path object if valid
        
    Raises:
        ValidationError: If path is invalid
    """
    if not path or not isinstance(path, str):
        raise ValidationError(
            "File path must be a non-empty string",
            error_code="V005"
        )
    
    try:
        path_obj = Path(path).resolve()
    except (OSError, ValueError) as e:
        raise ValidationError(
            f"Invalid file path: {e}",
            error_code="V006"
        )
    
    if must_exist and not path_obj.exists():
        raise ValidationError(
            f"File does not exist: {path}",
            error_code="V007"
        )
    
    if must_exist and not path_obj.is_file():
        raise ValidationError(
            f"Path is not a file: {path}",
            error_code="V008"
        )
    
    return path_obj


def validate_coordinate(value: Any, name: str = "coordinate") -> float:
    """Validate a coordinate value.
    
    Args:
        value: The coordinate value
        name: Name of the coordinate for error messages
        
    Returns:
        Validated float coordinate
        
    Raises:
        ValidationError: If coordinate is invalid
    """
    if isinstance(value, (int, float)):
        # Allow very large ranges but warn about extreme values
        if abs(value) > 1e6:
            # This is a warning, not an error - allow it but note it's unusual
            pass
        return float(value)
    
    if isinstance(value, str):
        # Check for rand() expressions - these are handled separately
        if value.strip().startswith('rand('):
            return value  # Return as-is for runtime evaluation
    
    raise ValidationError(
        f"Invalid {name}: must be a number or rand() expression, got {type(value).__name__}",
        error_code="V009"
    )


def validate_size(value: Any) -> Tuple[int, int]:
    """Validate a size value (width, height).
    
    Args:
        value: Size value (int, tuple, or "WxH" string)
        
    Returns:
        Tuple of (width, height) as integers
        
    Raises:
        ValidationError: If size is invalid
    """
    if isinstance(value, (tuple, list)) and len(value) == 2:
        try:
            width = int(value[0])
            height = int(value[1])
            if width <= 0 or height <= 0:
                raise ValidationError(
                    f"Size dimensions must be positive, got ({width}, {height})",
                    error_code="V010"
                )
            if width > 10000 or height > 10000:
                raise ValidationError(
                    f"Size dimensions too large (max 10000), got ({width}, {height})",
                    error_code="V011"
                )
            return (width, height)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Size must be two integers, got {value}",
                error_code="V012"
            )
    
    if isinstance(value, str) and 'x' in value.lower():
        try:
            parts = value.lower().split('x', 1)
            width = int(parts[0].strip())
            height = int(parts[1].strip())
            if width <= 0 or height <= 0:
                raise ValidationError(
                    f"Size dimensions must be positive, got {width}x{height}",
                    error_code="V010"
                )
            return (width, height)
        except (ValueError, IndexError):
            raise ValidationError(
                f"Invalid size format '{value}'. Expected 'WxH' (e.g., '800x600')",
                error_code="V013"
            )
    
    if isinstance(value, (int, float)):
        size = int(value)
        if size <= 0:
            raise ValidationError(
                f"Size must be positive, got {size}",
                error_code="V010"
            )
        return (size, size)
    
    raise ValidationError(
        f"Invalid size value: must be int, tuple, or 'WxH' string, got {type(value).__name__}",
        error_code="V014"
    )


def validate_color(value: Any) -> Tuple[int, int, int]:
    """Validate a color value.
    
    Args:
        value: Color value (string name, hex, or RGB tuple)
        
    Returns:
        RGB tuple (r, g, b)
        
    Raises:
        ValidationError: If color is invalid
    """
    if isinstance(value, str):
        # Check for hex color
        if COLOR_HEX_PATTERN.match(value):
            try:
                hex_color = value[1:]  # Remove #
                if len(hex_color) == 6:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return (r, g, b)
            except ValueError:
                raise ValidationError(
                    f"Invalid hex color: {value}",
                    error_code="V015"
                )
    
    if isinstance(value, (tuple, list)) and len(value) >= 3:
        try:
            r = max(0, min(255, int(value[0])))
            g = max(0, min(255, int(value[1])))
            b = max(0, min(255, int(value[2])))
            return (r, g, b)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Invalid RGB color tuple: {value}",
                error_code="V016"
            )
    
    # Color name validation is done in runtime
    return value  # Return as-is for runtime color map lookup


def validate_speed(value: Any) -> float:
    """Validate a speed value.
    
    Args:
        value: Speed value
        
    Returns:
        Validated speed as float
        
    Raises:
        ValidationError: If speed is invalid
    """
    if isinstance(value, (int, float)):
        speed = float(value)
        if speed < 0:
            raise ValidationError(
                f"Speed cannot be negative, got {speed}",
                error_code="V017"
            )
        if speed > 1000:
            raise ValidationError(
                f"Speed value too large (max 1000), got {speed}",
                error_code="V018"
            )
        return speed
    
    if isinstance(value, str) and value.strip().startswith('rand('):
        return value  # Return as-is for runtime evaluation
    
    raise ValidationError(
        f"Invalid speed value: must be a number or rand() expression, got {type(value).__name__}",
        error_code="V019"
    )


def sanitize_block_name(name: str) -> str:
    """Sanitize a block name to make it safe.
    
    Args:
        name: Block name to sanitize
        
    Returns:
        Sanitized block name
    """
    # Remove any non-identifier characters
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Ensure it starts with letter or underscore
    if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
        sanitized = '_' + sanitized
    # Ensure it's not empty
    if not sanitized:
        sanitized = 'block'
    return sanitized

