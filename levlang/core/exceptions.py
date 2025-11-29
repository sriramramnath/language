"""
Professional exception hierarchy for LevLang.

This module defines all custom exceptions used throughout the transpiler,
providing clear error categorization and better error handling.
"""

from typing import Optional
from levlang.core.source_location import SourceLocation


class LevLangError(Exception):
    """Base exception for all LevLang errors."""
    
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        error_code: Optional[str] = None
    ):
        """Initialize a LevLang error.
        
        Args:
            message: Human-readable error message
            location: Source location where error occurred
            error_code: Machine-readable error code (e.g., "E001")
        """
        super().__init__(message)
        self.message = message
        self.location = location
        self.error_code = error_code
    
    def __str__(self) -> str:
        """Format error with location if available."""
        if self.location:
            return f"{self.location}: {self.message}"
        return self.message


class TranspilationError(LevLangError):
    """Base class for transpilation errors."""
    pass


class LexicalError(TranspilationError):
    """Error during lexical analysis (tokenization)."""
    pass


class SyntaxError(TranspilationError):
    """Error during syntax analysis (parsing)."""
    pass


class SemanticError(TranspilationError):
    """Error during semantic analysis."""
    pass


class CodeGenerationError(TranspilationError):
    """Error during code generation."""
    pass


class RuntimeError(LevLangError):
    """Base class for runtime errors."""
    pass


class PygameInitializationError(RuntimeError):
    """Error initializing pygame."""
    pass


class ResourceNotFoundError(RuntimeError):
    """Required resource (file, image, etc.) not found."""
    pass


class ValidationError(LevLangError):
    """Input validation error."""
    pass


class FileSystemError(LevLangError):
    """File system operation error."""
    pass

