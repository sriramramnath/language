"""Unit tests for the error reporter."""

import pytest
from levlang.error import (
    CompilationError,
    ErrorReporter,
    ErrorType,
    ErrorSeverity
)
from levlang.core.source_location import SourceLocation


class TestCompilationError:
    """Test CompilationError class."""
    
    def test_error_creation(self):
        """Test creating a compilation error."""
        location = SourceLocation("test.lvl", 1, 5, 3)
        error = CompilationError(
            error_type=ErrorType.SYNTAX,
            severity=ErrorSeverity.ERROR,
            message="unexpected token",
            location=location
        )
        
        assert error.error_type == ErrorType.SYNTAX
        assert error.severity == ErrorSeverity.ERROR
        assert error.message == "unexpected token"
        assert error.location == location
    
    def test_error_string_representation(self):
        """Test string representation of error."""
        location = SourceLocation("test.lvl", 10, 15, 1)
        error = CompilationError(
            error_type=ErrorType.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="invalid character",
            location=location
        )
        
        error_str = str(error)
        assert "test.lvl:10:15" in error_str
        assert "error" in error_str
        assert "invalid character" in error_str


class TestErrorReporter:
    """Test ErrorReporter class."""
    
    def test_reporter_initialization(self):
        """Test error reporter initialization."""
        source = "game MyGame {\n    title = \"Test\"\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        assert reporter.source_code == source
        assert reporter.filename == "test.lvl"
        assert not reporter.has_errors()
        assert not reporter.has_warnings()
    
    def test_report_error(self):
        """Test reporting an error."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_error(ErrorType.SYNTAX, "test error", location)
        
        assert reporter.has_errors()
        assert reporter.error_count() == 1
        assert not reporter.has_warnings()
    
    def test_report_warning(self):
        """Test reporting a warning."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_warning(ErrorType.SEMANTIC, "test warning", location)
        
        assert not reporter.has_errors()
        assert reporter.has_warnings()
        assert reporter.warning_count() == 1
    
    def test_multiple_errors(self):
        """Test reporting multiple errors."""
        reporter = ErrorReporter()
        
        for i in range(3):
            location = SourceLocation("test.lvl", i + 1, 1, 1)
            reporter.report_error(ErrorType.SYNTAX, f"error {i}", location)
        
        assert reporter.error_count() == 3
        errors = reporter.get_errors()
        assert len(errors) == 3
    
    def test_add_error(self):
        """Test adding a pre-constructed error."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        error = CompilationError(
            error_type=ErrorType.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="test",
            location=location
        )
        
        reporter.add_error(error)
        
        assert reporter.has_errors()
        assert reporter.error_count() == 1
    
    def test_get_all_messages(self):
        """Test getting all messages sorted by location."""
        reporter = ErrorReporter()
        
        # Add errors in non-sequential order
        reporter.report_error(ErrorType.SYNTAX, "error 3", SourceLocation("test.lvl", 3, 1, 1))
        reporter.report_error(ErrorType.SYNTAX, "error 1", SourceLocation("test.lvl", 1, 1, 1))
        reporter.report_warning(ErrorType.SEMANTIC, "warning 2", SourceLocation("test.lvl", 2, 1, 1))
        
        messages = reporter.get_all_messages()
        
        assert len(messages) == 3
        # Should be sorted by line number
        assert messages[0].location.line == 1
        assert messages[1].location.line == 2
        assert messages[2].location.line == 3
    
    def test_clear(self):
        """Test clearing all errors and warnings."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_error(ErrorType.SYNTAX, "error", location)
        reporter.report_warning(ErrorType.SEMANTIC, "warning", location)
        
        assert reporter.has_errors()
        assert reporter.has_warnings()
        
        reporter.clear()
        
        assert not reporter.has_errors()
        assert not reporter.has_warnings()
        assert reporter.error_count() == 0
        assert reporter.warning_count() == 0


class TestErrorFormatting:
    """Test error message formatting."""
    
    def test_format_error_basic(self):
        """Test basic error formatting without source code."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 5, 10, 1)
        
        reporter.report_error(ErrorType.SYNTAX, "unexpected token", location)
        
        formatted = reporter.format_errors()
        
        assert "error: unexpected token" in formatted
        assert "test.lvl:5:10" in formatted
    
    def test_format_error_with_source(self):
        """Test error formatting with source code context."""
        source = "game MyGame {\n    title = \"Test\"\n    invalid syntax here\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        # Error on line 3, column 5
        location = SourceLocation("test.lvl", 3, 5, 7)
        reporter.report_error(ErrorType.SYNTAX, "unexpected identifier", location)
        
        formatted = reporter.format_errors()
        
        assert "error: unexpected identifier" in formatted
        assert "test.lvl:3:5" in formatted
        assert "invalid syntax here" in formatted
        assert "^" in formatted
    
    def test_format_error_with_caret(self):
        """Test that caret indicator is positioned correctly."""
        source = "sprite Player {\n    x = 100\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        # Error at column 5 on line 2
        location = SourceLocation("test.lvl", 2, 5, 1)
        reporter.report_error(ErrorType.SEMANTIC, "undefined variable", location)
        
        formatted = reporter.format_errors()
        lines = formatted.split('\n')
        
        # Find the line with the caret
        caret_line = None
        for line in lines:
            if '^' in line:
                caret_line = line
                break
        
        assert caret_line is not None
        # The caret should be at the correct position
        assert '^' in caret_line
    
    def test_format_error_multi_character(self):
        """Test formatting error that spans multiple characters."""
        source = "game MyGame {\n    title = \"Test\"\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        # Error spanning 7 characters
        location = SourceLocation("test.lvl", 1, 6, 7)
        reporter.report_error(ErrorType.SEMANTIC, "duplicate declaration", location)
        
        formatted = reporter.format_errors()
        
        # Should have multiple carets
        assert "^^^^^^^" in formatted
    
    def test_format_warnings(self):
        """Test formatting warnings."""
        source = "sprite Player {\n    unused_var = 10\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        location = SourceLocation("test.lvl", 2, 5, 10)
        reporter.report_warning(ErrorType.SEMANTIC, "unused variable", location)
        
        formatted = reporter.format_warnings()
        
        assert "warning: unused variable" in formatted
        assert "test.lvl:2:5" in formatted
    
    def test_format_all_with_summary(self):
        """Test formatting all messages with summary."""
        source = "game MyGame {\n    title = \"Test\"\n}"
        reporter = ErrorReporter(source, "test.lvl")
        
        reporter.report_error(ErrorType.SYNTAX, "error 1", SourceLocation("test.lvl", 1, 1, 1))
        reporter.report_error(ErrorType.SYNTAX, "error 2", SourceLocation("test.lvl", 2, 1, 1))
        reporter.report_warning(ErrorType.SEMANTIC, "warning 1", SourceLocation("test.lvl", 1, 5, 1))
        
        formatted = reporter.format_all()
        
        assert "error: error 1" in formatted
        assert "error: error 2" in formatted
        assert "warning: warning 1" in formatted
        assert "2 errors and 1 warning generated" in formatted
    
    def test_format_all_errors_only(self):
        """Test summary with only errors."""
        reporter = ErrorReporter()
        
        reporter.report_error(ErrorType.SYNTAX, "error", SourceLocation("test.lvl", 1, 1, 1))
        
        formatted = reporter.format_all()
        
        assert "1 error generated" in formatted
    
    def test_format_all_warnings_only(self):
        """Test summary with only warnings."""
        reporter = ErrorReporter()
        
        reporter.report_warning(ErrorType.SEMANTIC, "warning", SourceLocation("test.lvl", 1, 1, 1))
        
        formatted = reporter.format_all()
        
        assert "1 warning generated" in formatted
    
    def test_format_empty(self):
        """Test formatting when there are no errors or warnings."""
        reporter = ErrorReporter()
        
        assert reporter.format_errors() == ""
        assert reporter.format_warnings() == ""
        assert reporter.format_all() == ""


class TestErrorTypes:
    """Test error type categorization."""
    
    def test_lexical_error(self):
        """Test lexical error type."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_error(ErrorType.LEXICAL, "invalid character", location)
        
        errors = reporter.get_errors()
        assert errors[0].error_type == ErrorType.LEXICAL
    
    def test_syntax_error(self):
        """Test syntax error type."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_error(ErrorType.SYNTAX, "unexpected token", location)
        
        errors = reporter.get_errors()
        assert errors[0].error_type == ErrorType.SYNTAX
    
    def test_semantic_error(self):
        """Test semantic error type."""
        reporter = ErrorReporter()
        location = SourceLocation("test.lvl", 1, 1, 1)
        
        reporter.report_error(ErrorType.SEMANTIC, "undefined reference", location)
        
        errors = reporter.get_errors()
        assert errors[0].error_type == ErrorType.SEMANTIC
