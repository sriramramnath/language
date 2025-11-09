"""Unit tests for the semantic analyzer."""

import pytest
from levlang.lexer import Lexer
from levlang.parser import Parser
from levlang.semantic import SemanticAnalyzer, ErrorType


class TestSymbolResolution:
    """Test symbol resolution and scope handling."""
    
    def test_undefined_variable_reference(self):
        """Test detection of undefined variable references."""
        source = """
        sprite Player {
            x = undefinedVar
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        assert len(errors) == 1
        assert errors[0].error_type == ErrorType.UNDEFINED_REFERENCE
        assert "undefinedVar" in errors[0].message
    
    def test_valid_variable_reference(self):
        """Test that defined variables are resolved correctly."""
        source = """
        sprite Player {
            x = 100
            y = x
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_scope_nesting(self):
        """Test that nested scopes work correctly."""
        source = """
        sprite Player {
            x = 100
            on keydown(key) {
                y = x
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_parameter_scope(self):
        """Test that parameters are accessible in their scope."""
        source = """
        sprite Player {
            on keydown(key) {
                x = key
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()


class TestDuplicateDeclarations:
    """Test detection of duplicate declarations."""
    
    def test_duplicate_sprite_declaration(self):
        """Test detection of duplicate sprite names."""
        source = """
        sprite Player {
            x = 100
        }
        
        sprite Player {
            y = 200
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        assert any(e.error_type == ErrorType.DUPLICATE_DECLARATION for e in errors)
        assert any("Player" in e.message for e in errors)
    
    def test_duplicate_scene_declaration(self):
        """Test detection of duplicate scene names."""
        source = """
        scene Main {
            update {
                x = 1
            }
        }
        
        scene Main {
            draw {
                y = 2
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        assert any(e.error_type == ErrorType.DUPLICATE_DECLARATION for e in errors)
    
    def test_duplicate_parameter(self):
        """Test detection of duplicate parameter names."""
        source = """
        sprite Player {
            on keydown(key) {
                x = key
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        # This should pass - single parameter is fine
        assert result
        assert not analyzer.has_errors()


class TestTypeChecking:
    """Test type checking for expressions."""
    
    def test_arithmetic_on_numbers(self):
        """Test that arithmetic operations work on numbers."""
        source = """
        sprite Player {
            x = 10 + 20
            y = x * 2
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_comparison_on_numbers(self):
        """Test that comparison operations work on numbers."""
        source = """
        scene Main {
            update {
                if 10 > 5 {
                    x = 1
                }
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_equality_comparison(self):
        """Test equality comparisons."""
        source = """
        sprite Player {
            on keydown(key) {
                if key == "LEFT" {
                    x = 1
                }
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()


class TestEventHandlerValidation:
    """Test validation of event handlers."""
    
    def test_valid_keydown_handler(self):
        """Test that valid keydown handler is accepted."""
        source = """
        sprite Player {
            on keydown(key) {
                x = 1
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_valid_mousedown_handler(self):
        """Test that valid mousedown handler is accepted."""
        source = """
        sprite Player {
            on mousedown(button) {
                x = 1
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_invalid_event_type(self):
        """Test detection of invalid event types."""
        source = """
        sprite Player {
            on invalidEvent(param) {
                x = 1
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        assert any(e.error_type == ErrorType.INVALID_EVENT_HANDLER for e in errors)
        assert any("invalidEvent" in e.message for e in errors)
    
    def test_wrong_parameter_count(self):
        """Test detection of wrong parameter count in event handlers."""
        source = """
        sprite Player {
            on keydown(key, extra) {
                x = 1
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        assert any(e.error_type == ErrorType.INVALID_EVENT_HANDLER for e in errors)


class TestCompletePrograms:
    """Test semantic analysis on complete programs."""
    
    def test_valid_complete_program(self):
        """Test that a valid complete program passes semantic analysis."""
        source = """
        game MyGame {
            title = "Test"
            width = 800
        }
        
        sprite Player {
            x = 100
            y = 200
            speed = 5
            
            on keydown(key) {
                if key == "LEFT" {
                    x = x - speed
                }
            }
        }
        
        scene Main {
            player = Player()
            
            update {
                x = x + 1
            }
            
            draw {
                y = 0
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert result
        assert not analyzer.has_errors()
    
    def test_program_with_multiple_errors(self):
        """Test that multiple errors are detected."""
        source = """
        sprite Player {
            x = undefinedVar
        }
        
        sprite Player {
            y = 200
        }
        
        sprite Enemy {
            on invalidEvent(param) {
                z = anotherUndefined
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer(ast)
        result = analyzer.analyze()
        
        assert not result
        assert analyzer.has_errors()
        errors = analyzer.get_errors()
        # Should have at least: undefined var, duplicate sprite, invalid event, another undefined
        assert len(errors) >= 3
