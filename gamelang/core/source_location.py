"""Source location tracking for error reporting."""

from dataclasses import dataclass


@dataclass
class SourceLocation:
    """Represents a location in source code for error reporting."""
    
    filename: str
    line: int
    column: int
    length: int = 1
    
    def __str__(self) -> str:
        """Format location as filename:line:column."""
        return f"{self.filename}:{self.line}:{self.column}"
