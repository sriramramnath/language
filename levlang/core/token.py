"""Token definitions for the lexer."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from levlang.core.source_location import SourceLocation


class TokenType(Enum):
    """Enumeration of all token types in the game language."""
    
    # Keywords
    GAME = auto()
    SPRITE = auto()
    SCENE = auto()
    ON = auto()
    WHEN = auto()
    UPDATE = auto()
    DRAW = auto()
    INPUT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()

    # Delimiters
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    INVALID = auto()


@dataclass
class Token:
    """Represents a single token from the source code."""
    
    type: TokenType
    value: Any
    location: SourceLocation
    
    def __str__(self) -> str:
        """Format token for debugging."""
        return f"Token({self.type.name}, {self.value!r}, {self.location})"
