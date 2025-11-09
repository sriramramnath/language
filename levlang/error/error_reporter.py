"""Error reporting for the game language transpiler."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from levlang.core.source_location import SourceLocation


class ErrorType(Enum):
    """Types of compilation errors."""
    LEXICAL = "lexical"
    SYNTAX = "syntax"
    SEMANTIC = "semantic"


class ErrorSeverity(Enum):
    """Severity levels for compilation messages."""
    ERROR = "error"
    WARNING = "warning"


@dataclass
class CompilationError:
    """Represents a compilation error or warning."""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    location: SourceLocation
    
    def __str__(self) -> str:
        """Format the error as a string."""
        return f"{self.location}: {self.severity.value}: {self.message}"


class ErrorReporter:
    """Collects and formats compilation errors and warnings."""
    
    def __init__(self, source_code: Optional[str] = None, filename: str = "<input>"):
        """Initialize the error reporter.
        
        Args:
            source_code: The source code being compiled (for context in error messages)
            filename: The name of the source file
        """
        self.source_code = source_code
        self.filename = filename
        self.errors: List[CompilationError] = []
        self.warnings: List[CompilationError] = []
        
        # Cache source lines for efficient access
        self._source_lines: Optional[List[str]] = None
        if source_code:
            self._source_lines = source_code.splitlines()
    
    def report_error(
        self,
        error_type: ErrorType,
        message: str,
        location: SourceLocation
    ) -> None:
        """Report a compilation error.
        
        Args:
            error_type: The type of error (lexical, syntax, semantic)
            message: The error message
            location: The source location where the error occurred
        """
        error = CompilationError(
            error_type=error_type,
            severity=ErrorSeverity.ERROR,
            message=message,
            location=location
        )
        self.errors.append(error)
    
    def report_warning(
        self,
        error_type: ErrorType,
        message: str,
        location: SourceLocation
    ) -> None:
        """Report a compilation warning.
        
        Args:
            error_type: The type of warning
            message: The warning message
            location: The source location where the warning occurred
        """
        warning = CompilationError(
            error_type=error_type,
            severity=ErrorSeverity.WARNING,
            message=message,
            location=location
        )
        self.warnings.append(warning)
    
    def add_error(self, error: CompilationError) -> None:
        """Add a pre-constructed compilation error.
        
        Args:
            error: The compilation error to add
        """
        if error.severity == ErrorSeverity.ERROR:
            self.errors.append(error)
        else:
            self.warnings.append(error)
    
    def has_errors(self) -> bool:
        """Check if any errors were reported.
        
        Returns:
            True if there are errors, False otherwise
        """
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if any warnings were reported.
        
        Returns:
            True if there are warnings, False otherwise
        """
        return len(self.warnings) > 0
    
    def get_errors(self) -> List[CompilationError]:
        """Get all compilation errors.
        
        Returns:
            A list of compilation errors
        """
        return self.errors.copy()
    
    def get_warnings(self) -> List[CompilationError]:
        """Get all compilation warnings.
        
        Returns:
            A list of compilation warnings
        """
        return self.warnings.copy()
    
    def get_all_messages(self) -> List[CompilationError]:
        """Get all compilation messages (errors and warnings).
        
        Returns:
            A list of all compilation messages, sorted by location
        """
        all_messages = self.errors + self.warnings
        # Sort by location (line, then column)
        all_messages.sort(key=lambda e: (e.location.line, e.location.column))
        return all_messages
    
    def error_count(self) -> int:
        """Get the number of errors.
        
        Returns:
            The count of errors
        """
        return len(self.errors)
    
    def warning_count(self) -> int:
        """Get the number of warnings.
        
        Returns:
            The count of warnings
        """
        return len(self.warnings)
    
    def clear(self) -> None:
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()
    
    def format_error(self, error: CompilationError) -> str:
        """Format a single error with source context.
        
        Args:
            error: The compilation error to format
            
        Returns:
            A formatted error message with source code snippet and caret indicator
        """
        location = error.location
        severity = error.severity.value
        message = error.message
        
        # Basic format: filename:line:column: severity: message
        result = f"{severity}: {message}\n"
        result += f"  --> {location.filename}:{location.line}:{location.column}\n"
        
        # Add source context if available
        if self._source_lines and 0 < location.line <= len(self._source_lines):
            line_text = self._source_lines[location.line - 1]
            line_num_width = len(str(location.line))
            
            result += f"   |\n"
            result += f"{location.line:>{line_num_width}} | {line_text}\n"
            
            # Add caret indicator under the error position
            # Calculate spaces needed: line number width + " | " + column position
            spaces_before_caret = line_num_width + 3 + (location.column - 1)
            caret_line = " " * spaces_before_caret + "^"
            
            # Add multiple carets if the error spans multiple characters
            if location.length > 1:
                caret_line += "^" * (location.length - 1)
            
            result += caret_line + "\n"
        
        return result
    
    def format_errors(self) -> str:
        """Format all errors with source context.
        
        Returns:
            A formatted string containing all error messages
        """
        if not self.has_errors():
            return ""
        
        result = []
        for error in self.errors:
            result.append(self.format_error(error))
        
        return "\n".join(result)
    
    def format_warnings(self) -> str:
        """Format all warnings with source context.
        
        Returns:
            A formatted string containing all warning messages
        """
        if not self.has_warnings():
            return ""
        
        result = []
        for warning in self.warnings:
            result.append(self.format_error(warning))
        
        return "\n".join(result)
    
    def format_all(self) -> str:
        """Format all errors and warnings with source context.
        
        Returns:
            A formatted string containing all messages, with a summary at the end
        """
        messages = self.get_all_messages()
        
        if not messages:
            return ""
        
        result = []
        for message in messages:
            result.append(self.format_error(message))
        
        # Add summary
        error_count = self.error_count()
        warning_count = self.warning_count()
        
        summary_parts = []
        if error_count > 0:
            error_word = "error" if error_count == 1 else "errors"
            summary_parts.append(f"{error_count} {error_word}")
        if warning_count > 0:
            warning_word = "warning" if warning_count == 1 else "warnings"
            summary_parts.append(f"{warning_count} {warning_word}")
        
        summary = " and ".join(summary_parts) + " generated"
        result.append(summary)
        
        return "\n".join(result)
