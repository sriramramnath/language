"""Semantic error definitions."""

from dataclasses import dataclass
from enum import Enum

from levlang.core.source_location import SourceLocation


class ErrorType(Enum):
    """Types of semantic errors."""
    UNDEFINED_REFERENCE = "undefined_reference"
    DUPLICATE_DECLARATION = "duplicate_declaration"
    TYPE_MISMATCH = "type_mismatch"
    INVALID_EVENT_HANDLER = "invalid_event_handler"
    INVALID_OPERATION = "invalid_operation"


@dataclass
class SemanticError:
    """Represents a semantic error in the program."""
    error_type: ErrorType
    message: str
    location: SourceLocation
    
    def __str__(self) -> str:
        """Format the error as a string."""
        return f"{self.location}: {self.error_type.value}: {self.message}"
