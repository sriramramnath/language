"""Unit tests for the lexer."""

import pytest
from gamelang.lexer import Lexer
from gamelang.core.token import TokenType


class TestLexerBasics:
    """Test basic lexer functionality."""
    
    def test_empty_source(self):
        """Test lexing empty source code."""
        lexer = Lexer("", "test.game")
        tokens = lexer.tokenize()
        
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
        assert not lexer.has_errors()
    
    def test_whitespace_only(self):
        """Test lexing whitespace-only source."""
        lexer = Lexer("   \t\n  \r\n  ", "test.game")
        tokens = lexer.tokenize()
        
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
        assert not lexer.has_errors()


class TestKeywords:
    """Test keyword tokenization."""
    
    def test_game_keyword(self):
        """Test 'game' keyword."""
        lexer = Lexer("game", "test.game")
        tokens = lexer.tokenize()
        
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.GAME
        assert tokens[0].value == "game"
    
    def test_sprite_keyword(self):
        """Test 'sprite' keyword."""
        lexer = Lexer("sprite", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.SPRITE
        assert tokens[0].value == "sprite"
    
    def test_scene_keyword(self):
        """Test 'scene' keyword."""
        lexer = Lexer("scene", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.SCENE
    
    def test_control_flow_keywords(self):
        """Test control flow keywords."""
        lexer = Lexer("if else while for return", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.IF
        assert tokens[1].type == TokenType.ELSE
        assert tokens[2].type == TokenType.WHILE
        assert tokens[3].type == TokenType.FOR
        assert tokens[4].type == TokenType.RETURN
    
    def test_event_keywords(self):
        """Test event-related keywords."""
        lexer = Lexer("on when update draw input", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.ON
        assert tokens[1].type == TokenType.WHEN
        assert tokens[2].type == TokenType.UPDATE
        assert tokens[3].type == TokenType.DRAW
        assert tokens[4].type == TokenType.INPUT


class TestIdentifiers:
    """Test identifier tokenization."""
    
    def test_simple_identifier(self):
        """Test simple identifier."""
        lexer = Lexer("myVariable", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "myVariable"
    
    def test_identifier_with_underscore(self):
        """Test identifier with underscores."""
        lexer = Lexer("my_variable_name", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "my_variable_name"
    
    def test_identifier_with_numbers(self):
        """Test identifier with numbers."""
        lexer = Lexer("player1 sprite2d", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "player1"
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "sprite2d"
    
    def test_identifier_starting_with_underscore(self):
        """Test identifier starting with underscore."""
        lexer = Lexer("_private", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "_private"


class TestLiterals:
    """Test literal tokenization."""
    
    def test_integer_literal(self):
        """Test integer literals."""
        lexer = Lexer("42 0 999", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 0
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == 999
    
    def test_float_literal(self):
        """Test float literals."""
        lexer = Lexer("3.14 0.5 100.0", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 0.5
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == 100.0
    
    def test_string_literal_double_quotes(self):
        """Test string literals with double quotes."""
        lexer = Lexer('"hello world"', "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello world"
    
    def test_string_literal_single_quotes(self):
        """Test string literals with single quotes."""
        lexer = Lexer("'hello world'", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello world"
    
    def test_string_with_escape_sequences(self):
        """Test string with escape sequences."""
        lexer = Lexer(r'"hello\nworld\ttab"', "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello\nworld\ttab"
    
    def test_boolean_literals(self):
        """Test boolean literals."""
        lexer = Lexer("true false", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.TRUE
        assert tokens[0].value is True
        assert tokens[1].type == TokenType.FALSE
        assert tokens[1].value is False


class TestOperators:
    """Test operator tokenization."""
    
    def test_arithmetic_operators(self):
        """Test arithmetic operators."""
        lexer = Lexer("+ - * / %", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.PLUS
        assert tokens[1].type == TokenType.MINUS
        assert tokens[2].type == TokenType.STAR
        assert tokens[3].type == TokenType.SLASH
        assert tokens[4].type == TokenType.PERCENT
    
    def test_comparison_operators(self):
        """Test comparison operators."""
        lexer = Lexer("== != < <= > >=", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.EQUAL_EQUAL
        assert tokens[1].type == TokenType.BANG_EQUAL
        assert tokens[2].type == TokenType.LESS
        assert tokens[3].type == TokenType.LESS_EQUAL
        assert tokens[4].type == TokenType.GREATER
        assert tokens[5].type == TokenType.GREATER_EQUAL
    
    def test_logical_operators(self):
        """Test logical operators."""
        lexer = Lexer("&& || !", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.AND
        assert tokens[1].type == TokenType.OR
        assert tokens[2].type == TokenType.NOT
    
    def test_assignment_operator(self):
        """Test assignment operator."""
        lexer = Lexer("=", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.EQUAL


class TestDelimiters:
    """Test delimiter tokenization."""
    
    def test_braces(self):
        """Test braces."""
        lexer = Lexer("{ }", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.LEFT_BRACE
        assert tokens[1].type == TokenType.RIGHT_BRACE
    
    def test_parentheses(self):
        """Test parentheses."""
        lexer = Lexer("( )", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[1].type == TokenType.RIGHT_PAREN
    
    def test_brackets(self):
        """Test brackets."""
        lexer = Lexer("[ ]", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.LEFT_BRACKET
        assert tokens[1].type == TokenType.RIGHT_BRACKET
    
    def test_punctuation(self):
        """Test punctuation delimiters."""
        lexer = Lexer(", . : ;", "test.game")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.COMMA
        assert tokens[1].type == TokenType.DOT
        assert tokens[2].type == TokenType.COLON
        assert tokens[3].type == TokenType.SEMICOLON


class TestComments:
    """Test comment handling."""
    
    def test_single_line_comment(self):
        """Test single-line comments."""
        lexer = Lexer("game // this is a comment\nsprite", "test.game")
        tokens = lexer.tokenize()
        
        assert len(tokens) == 3  # game, sprite, EOF
        assert tokens[0].type == TokenType.GAME
        assert tokens[1].type == TokenType.SPRITE
    
    def test_block_comment(self):
        """Test block comments."""
        lexer = Lexer("game /* this is a\nmulti-line comment */ sprite", "test.game")
        tokens = lexer.tokenize()
        
        assert len(tokens) == 3  # game, sprite, EOF
        assert tokens[0].type == TokenType.GAME
        assert tokens[1].type == TokenType.SPRITE


class TestErrorReporting:
    """Test error reporting."""
    
    def test_invalid_character(self):
        """Test invalid character detection."""
        lexer = Lexer("game @ sprite", "test.game")
        tokens = lexer.tokenize()
        
        assert lexer.has_errors()
        assert len(lexer.get_errors()) == 1
        assert "invalid character" in lexer.get_errors()[0]
    
    def test_unterminated_string(self):
        """Test unterminated string detection."""
        lexer = Lexer('"hello world', "test.game")
        tokens = lexer.tokenize()
        
        assert lexer.has_errors()
        assert "unterminated string" in lexer.get_errors()[0]
    
    def test_unterminated_block_comment(self):
        """Test unterminated block comment detection."""
        lexer = Lexer("/* this comment never ends", "test.game")
        tokens = lexer.tokenize()
        
        assert lexer.has_errors()
        assert "unterminated block comment" in lexer.get_errors()[0]
    
    def test_error_location_tracking(self):
        """Test that errors include correct location information."""
        lexer = Lexer("game\n@", "test.game")
        tokens = lexer.tokenize()
        
        assert lexer.has_errors()
        error = lexer.get_errors()[0]
        assert "test.game:2:1" in error


class TestComplexScenarios:
    """Test complex tokenization scenarios."""
    
    def test_simple_game_declaration(self):
        """Test tokenizing a simple game declaration."""
        source = """
        game MyGame {
            title = "My Game"
            width = 800
        }
        """
        lexer = Lexer(source, "test.game")
        tokens = lexer.tokenize()
        
        assert not lexer.has_errors()
        assert tokens[0].type == TokenType.GAME
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "MyGame"
        assert tokens[2].type == TokenType.LEFT_BRACE
    
    def test_sprite_with_event_handler(self):
        """Test tokenizing sprite with event handler."""
        source = """
        sprite Player {
            x = 100
            on keydown {
                x = x + 5
            }
        }
        """
        lexer = Lexer(source, "test.game")
        tokens = lexer.tokenize()
        
        assert not lexer.has_errors()
        # Verify key tokens are present
        token_types = [t.type for t in tokens]
        assert TokenType.SPRITE in token_types
        assert TokenType.ON in token_types
        assert TokenType.IDENTIFIER in token_types
    
    def test_expression_with_operators(self):
        """Test tokenizing complex expression."""
        source = "x = (a + b) * c - d / 2"
        lexer = Lexer(source, "test.game")
        tokens = lexer.tokenize()
        
        assert not lexer.has_errors()
        assert tokens[0].type == TokenType.IDENTIFIER  # x
        assert tokens[1].type == TokenType.EQUAL
        assert tokens[2].type == TokenType.LEFT_PAREN
        assert tokens[3].type == TokenType.IDENTIFIER  # a
        assert tokens[4].type == TokenType.PLUS
