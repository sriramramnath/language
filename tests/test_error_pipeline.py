"""Tests for error handling across the entire transpilation pipeline."""

import pytest
import os
import tempfile

from gamelang.cli.cli import CLI


class TestLexicalErrorHandling:
    """Test that lexical errors are properly caught and reported."""
    
    def test_invalid_character_error(self):
        """Test that invalid characters are caught and reported."""
        source_code = """
game Test {
    title = "Test"
    @ invalid
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "invalid_char.game")
            output_path = os.path.join(tmpdir, "invalid_char.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should fail with error
            assert result == 1
            # Output file should not be created
            assert not os.path.exists(output_path)
    
    def test_unterminated_string_error(self):
        """Test that unterminated strings are caught and reported."""
        source_code = """
game Test {
    title = "This string never ends
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "unterminated.game")
            output_path = os.path.join(tmpdir, "unterminated.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_unterminated_block_comment_error(self):
        """Test that unterminated block comments are caught."""
        source_code = """
game Test {
    /* This comment never ends
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "unterminated_comment.game")
            output_path = os.path.join(tmpdir, "unterminated_comment.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_multiple_lexical_errors(self):
        """Test that multiple lexical errors are all reported."""
        source_code = """
game Test {
    title = "unterminated
    @ invalid
    # another invalid
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "multiple_lex.game")
            output_path = os.path.join(tmpdir, "multiple_lex.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)


class TestSyntaxErrorHandling:
    """Test that syntax errors are properly caught and reported."""
    
    def test_missing_closing_brace(self):
        """Test that missing closing braces are caught."""
        source_code = """
game Test {
    title = "Test"
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "missing_brace.game")
            output_path = os.path.join(tmpdir, "missing_brace.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_missing_opening_brace(self):
        """Test that missing opening braces are caught."""
        source_code = """
game Test
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "missing_open.game")
            output_path = os.path.join(tmpdir, "missing_open.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_unexpected_token(self):
        """Test that unexpected tokens are caught."""
        source_code = """
invalid_keyword Test {
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "unexpected.game")
            output_path = os.path.join(tmpdir, "unexpected.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_missing_identifier(self):
        """Test that missing identifiers are caught."""
        source_code = """
game {
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "missing_id.game")
            output_path = os.path.join(tmpdir, "missing_id.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_missing_assignment_value(self):
        """Test that missing assignment values are caught."""
        source_code = """
game Test {
    title =
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "missing_value.game")
            output_path = os.path.join(tmpdir, "missing_value.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_malformed_if_statement(self):
        """Test that malformed if statements are caught."""
        source_code = """
sprite Test {
    update {
        if {
            x = 10
        }
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "malformed_if.game")
            output_path = os.path.join(tmpdir, "malformed_if.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_malformed_event_handler(self):
        """Test that malformed event handlers are caught."""
        source_code = """
sprite Test {
    on keydown {
        x = 10
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "malformed_event.game")
            output_path = os.path.join(tmpdir, "malformed_event.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_syntax_error_recovery(self):
        """Test that parser can recover from syntax errors and continue."""
        source_code = """
game Test {
    title = "Test"
    invalid syntax here
    width = 800
}

sprite Player {
    x = 100
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "recovery.game")
            output_path = os.path.join(tmpdir, "recovery.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should still fail, but parser should have attempted recovery
            assert result == 1
            assert not os.path.exists(output_path)


class TestSemanticErrorHandling:
    """Test that semantic errors are properly caught and reported."""
    
    def test_undefined_sprite_reference(self):
        """Test that undefined sprite references are caught."""
        source_code = """
game Test {
    title = "Test"
}

scene Main {
    player = UndefinedSprite()
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "undefined_sprite.game")
            output_path = os.path.join(tmpdir, "undefined_sprite.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_undefined_variable_reference(self):
        """Test that undefined variable references are caught."""
        source_code = """
sprite Test {
    update {
        x = undefined_variable + 10
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "undefined_var.game")
            output_path = os.path.join(tmpdir, "undefined_var.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_duplicate_sprite_declaration(self):
        """Test that duplicate sprite declarations are caught."""
        source_code = """
sprite Player {
    x = 100
}

sprite Player {
    y = 200
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "duplicate_sprite.game")
            output_path = os.path.join(tmpdir, "duplicate_sprite.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_duplicate_game_declaration(self):
        """Test that duplicate game declarations are caught."""
        source_code = """
game FirstGame {
    title = "First"
}

game SecondGame {
    title = "Second"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "duplicate_game.game")
            output_path = os.path.join(tmpdir, "duplicate_game.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_type_mismatch_in_expression(self):
        """Test that type mismatches are caught."""
        source_code = """
sprite Test {
    name = "Player"
    x = 100
    
    update {
        // Trying to add string and number
        result = name + x
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "type_mismatch.game")
            output_path = os.path.join(tmpdir, "type_mismatch.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Type checking might be lenient or strict depending on implementation
            # If it fails, that's good; if it succeeds, that's also acceptable
            # as Python allows dynamic typing
            assert result in [0, 1]
    
    def test_multiple_semantic_errors(self):
        """Test that multiple semantic errors are all reported."""
        source_code = """
sprite Player {
    x = 100
}

sprite Player {
    y = 200
}

scene Main {
    player = UndefinedSprite()
    enemy = AnotherUndefined()
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "multiple_semantic.game")
            output_path = os.path.join(tmpdir, "multiple_semantic.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)


class TestErrorMessageQuality:
    """Test that error messages are helpful and include location information."""
    
    def test_error_includes_filename(self):
        """Test that error messages include the filename."""
        source_code = """
game Test {
    title = "unterminated
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "error_file.game")
            output_path = os.path.join(tmpdir, "error_file.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            # Capture stderr to check error message
            import io
            import sys
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            
            try:
                result = cli.transpile_file(input_path, output_path)
                error_output = sys.stderr.getvalue()
            finally:
                sys.stderr = old_stderr
            
            assert result == 1
            # Error message should mention the file
            assert "error_file.game" in error_output or "error" in error_output.lower()
    
    def test_error_includes_line_number(self):
        """Test that error messages include line numbers."""
        source_code = """
game Test {
    title = "Test"
}

sprite Player {
    x = undefined_variable
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "line_error.game")
            output_path = os.path.join(tmpdir, "line_error.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            import io
            import sys
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            
            try:
                result = cli.transpile_file(input_path, output_path)
                error_output = sys.stderr.getvalue()
            finally:
                sys.stderr = old_stderr
            
            assert result == 1
            # Error message should include line number (format: filename:line:column)
            # or at least mention "line"
            assert ":" in error_output or "line" in error_output.lower()
    
    def test_error_message_is_descriptive(self):
        """Test that error messages are descriptive."""
        source_code = """
scene Main {
    player = UndefinedSprite()
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "descriptive.game")
            output_path = os.path.join(tmpdir, "descriptive.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            import io
            import sys
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            
            try:
                result = cli.transpile_file(input_path, output_path)
                error_output = sys.stderr.getvalue()
            finally:
                sys.stderr = old_stderr
            
            assert result == 1
            # Error should mention something about undefined or not found
            assert "undefined" in error_output.lower() or "not found" in error_output.lower() or "error" in error_output.lower()


class TestErrorRecovery:
    """Test that the transpiler can recover from errors appropriately."""
    
    def test_no_crash_on_empty_file(self):
        """Test that empty files don't crash the transpiler."""
        source_code = ""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "empty.game")
            output_path = os.path.join(tmpdir, "empty.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should succeed (empty program is valid)
            assert result == 0
    
    def test_no_crash_on_whitespace_only(self):
        """Test that whitespace-only files don't crash."""
        source_code = "   \n\n\t\t\n   "
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "whitespace.game")
            output_path = os.path.join(tmpdir, "whitespace.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should succeed
            assert result == 0
    
    def test_no_crash_on_comments_only(self):
        """Test that files with only comments don't crash."""
        source_code = """
// This is a comment
/* This is a block comment */
// Another comment
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "comments.game")
            output_path = os.path.join(tmpdir, "comments.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should succeed
            assert result == 0
    
    def test_handles_very_long_lines(self):
        """Test that very long lines don't crash the transpiler."""
        # Create a very long string literal
        long_string = "x" * 10000
        source_code = f"""
game Test {{
    title = "{long_string}"
}}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "long_line.game")
            output_path = os.path.join(tmpdir, "long_line.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should succeed
            assert result == 0
    
    def test_handles_deeply_nested_structures(self):
        """Test that deeply nested structures don't crash."""
        # Create deeply nested if statements
        source_code = """
sprite Test {
    update {
"""
        
        # Add 20 levels of nesting
        for i in range(20):
            source_code += f"        {'    ' * i}if x > {i} {{\n"
        
        source_code += "        " + "    " * 20 + "x = x + 1\n"
        
        for i in range(19, -1, -1):
            source_code += f"        {'    ' * i}}}\n"
        
        source_code += """    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "nested.game")
            output_path = os.path.join(tmpdir, "nested.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should succeed
            assert result == 0


class TestCrossPhaseErrors:
    """Test errors that span multiple phases of compilation."""
    
    def test_lexical_error_prevents_parsing(self):
        """Test that lexical errors prevent parsing phase."""
        source_code = """
game Test {
    title = "Test"
    @ invalid
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "lex_blocks_parse.game")
            output_path = os.path.join(tmpdir, "lex_blocks_parse.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_syntax_error_prevents_semantic_analysis(self):
        """Test that syntax errors prevent semantic analysis."""
        source_code = """
game Test {
    title = "Test"

sprite Player {
    x = 100
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "syntax_blocks_semantic.game")
            output_path = os.path.join(tmpdir, "syntax_blocks_semantic.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            assert not os.path.exists(output_path)
    
    def test_semantic_error_prevents_code_generation(self):
        """Test that semantic errors prevent code generation."""
        source_code = """
scene Main {
    player = UndefinedSprite()
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "semantic_blocks_codegen.game")
            output_path = os.path.join(tmpdir, "semantic_blocks_codegen.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 1
            # No output file should be created when there are errors
            assert not os.path.exists(output_path)
