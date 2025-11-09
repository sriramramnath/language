"""Unit tests for the parser."""

import pytest
from levlang.lexer import Lexer
from levlang.parser import Parser
from levlang.core.ast_node import (
    ProgramNode, GameNode, SpriteNode, SceneNode,
    EventHandlerNode, LiteralNode, IdentifierNode,
    BinaryOpNode, AssignmentNode, IfNode, WhileNode
)


class TestParserBasics:
    """Test basic parser functionality."""
    
    def test_empty_program(self):
        """Test parsing empty source code."""
        lexer = Lexer("", "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.declarations) == 0
        assert not parser.has_errors()
    
    def test_parser_error_recovery(self):
        """Test that parser can recover from errors."""
        source = "invalid game MyGame { }"
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert parser.has_errors()
        assert len(parser.get_errors()) > 0


class TestGameDeclaration:
    """Test game declaration parsing."""
    
    def test_simple_game_declaration(self):
        """Test parsing a simple game declaration."""
        source = """
        game MyGame {
            title = "My Game"
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        assert len(ast.declarations) == 1
        
        game_node = ast.declarations[0]
        assert isinstance(game_node, GameNode)
        assert game_node.name == "MyGame"
        assert "title" in game_node.properties
    
    def test_game_with_multiple_properties(self):
        """Test parsing game with multiple properties."""
        source = """
        game MyGame {
            title = "My Game"
            width = 800
            height = 600
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        game_node = ast.declarations[0]
        assert isinstance(game_node, GameNode)
        assert len(game_node.properties) == 3
        assert "title" in game_node.properties
        assert "width" in game_node.properties
        assert "height" in game_node.properties
    
    def test_game_property_values(self):
        """Test that game property values are parsed correctly."""
        source = """
        game MyGame {
            title = "Test"
            width = 800
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        game_node = ast.declarations[0]
        
        # Check title is a string literal
        title_expr = game_node.properties["title"]
        assert isinstance(title_expr, LiteralNode)
        assert title_expr.value == "Test"
        
        # Check width is a number literal
        width_expr = game_node.properties["width"]
        assert isinstance(width_expr, LiteralNode)
        assert width_expr.value == 800


class TestSpriteDeclaration:
    """Test sprite declaration parsing."""
    
    def test_simple_sprite_declaration(self):
        """Test parsing a simple sprite declaration."""
        source = """
        sprite Player {
            x = 100
            y = 200
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        assert len(ast.declarations) == 1
        
        sprite_node = ast.declarations[0]
        assert isinstance(sprite_node, SpriteNode)
        assert sprite_node.name == "Player"
        assert len(sprite_node.properties) == 2
        assert "x" in sprite_node.properties
        assert "y" in sprite_node.properties
    
    def test_sprite_with_event_handler(self):
        """Test parsing sprite with event handler."""
        source = """
        sprite Player {
            x = 100
            on keydown(key) {
                x = x + 5
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        sprite_node = ast.declarations[0]
        assert isinstance(sprite_node, SpriteNode)
        assert len(sprite_node.methods) == 1
        
        event_handler = sprite_node.methods[0]
        assert isinstance(event_handler, EventHandlerNode)
        assert event_handler.event_type == "keydown"
        assert len(event_handler.parameters) == 1
        assert event_handler.parameters[0] == "key"
        assert len(event_handler.body) > 0


class TestSceneDeclaration:
    """Test scene declaration parsing."""
    
    def test_simple_scene_declaration(self):
        """Test parsing a simple scene declaration."""
        source = """
        scene MainScene {
            player = Player()
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        assert len(ast.declarations) == 1
        
        scene_node = ast.declarations[0]
        assert isinstance(scene_node, SceneNode)
        assert scene_node.name == "MainScene"
    
    def test_scene_with_update_block(self):
        """Test parsing scene with update block."""
        source = """
        scene MainScene {
            update {
                x = x + 1
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        assert isinstance(scene_node, SceneNode)
        assert scene_node.update_block is not None
        assert len(scene_node.update_block) > 0
    
    def test_scene_with_draw_block(self):
        """Test parsing scene with draw block."""
        source = """
        scene MainScene {
            draw {
                screen.fill()
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        assert isinstance(scene_node, SceneNode)
        assert scene_node.draw_block is not None
        assert len(scene_node.draw_block) > 0
    
    def test_scene_with_update_and_draw(self):
        """Test parsing scene with both update and draw blocks."""
        source = """
        scene MainScene {
            update {
                x = x + 1
            }
            draw {
                screen.fill()
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        assert scene_node.update_block is not None
        assert scene_node.draw_block is not None


class TestExpressionParsing:
    """Test expression parsing."""
    
    def test_literal_expressions(self):
        """Test parsing literal expressions."""
        source = """
        game Test {
            num = 42
            str = "hello"
            bool = true
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        game_node = ast.declarations[0]
        
        # Number literal
        num_expr = game_node.properties["num"]
        assert isinstance(num_expr, LiteralNode)
        assert num_expr.value == 42
        
        # String literal
        str_expr = game_node.properties["str"]
        assert isinstance(str_expr, LiteralNode)
        assert str_expr.value == "hello"
        
        # Boolean literal
        bool_expr = game_node.properties["bool"]
        assert isinstance(bool_expr, LiteralNode)
        assert bool_expr.value is True
    
    def test_identifier_expression(self):
        """Test parsing identifier expressions."""
        source = """
        sprite Test {
            x = myVariable
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        sprite_node = ast.declarations[0]
        x_expr = sprite_node.properties["x"]
        assert isinstance(x_expr, IdentifierNode)
        assert x_expr.name == "myVariable"
    
    def test_binary_operations(self):
        """Test parsing binary operations."""
        source = """
        sprite Test {
            result = a + b
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        sprite_node = ast.declarations[0]
        result_expr = sprite_node.properties["result"]
        assert isinstance(result_expr, BinaryOpNode)
        assert result_expr.operator == "+"
        assert isinstance(result_expr.left, IdentifierNode)
        assert isinstance(result_expr.right, IdentifierNode)
    
    def test_operator_precedence(self):
        """Test that operator precedence is respected."""
        source = """
        sprite Test {
            result = a + b * c
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        sprite_node = ast.declarations[0]
        result_expr = sprite_node.properties["result"]
        
        # Should be: a + (b * c)
        assert isinstance(result_expr, BinaryOpNode)
        assert result_expr.operator == "+"
        assert isinstance(result_expr.right, BinaryOpNode)
        assert result_expr.right.operator == "*"
    
    def test_parenthesized_expression(self):
        """Test parsing parenthesized expressions."""
        source = """
        sprite Test {
            result = (a + b) * c
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        sprite_node = ast.declarations[0]
        result_expr = sprite_node.properties["result"]
        
        # Should be: (a + b) * c
        assert isinstance(result_expr, BinaryOpNode)
        assert result_expr.operator == "*"
        assert isinstance(result_expr.left, BinaryOpNode)
        assert result_expr.left.operator == "+"


class TestStatementParsing:
    """Test statement parsing."""
    
    def test_assignment_statement(self):
        """Test parsing assignment statements."""
        source = """
        scene Test {
            update {
                x = 10
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        assert len(scene_node.update_block) > 0
        
        stmt = scene_node.update_block[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.target == "x"
        assert isinstance(stmt.value, LiteralNode)
    
    def test_if_statement(self):
        """Test parsing if statements."""
        source = """
        scene Test {
            update {
                if x > 10 {
                    y = 5
                }
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        stmt = scene_node.update_block[0]
        
        assert isinstance(stmt, IfNode)
        assert isinstance(stmt.condition, BinaryOpNode)
        assert len(stmt.then_block) > 0
        assert stmt.else_block is None
    
    def test_if_else_statement(self):
        """Test parsing if-else statements."""
        source = """
        scene Test {
            update {
                if x > 10 {
                    y = 5
                } else {
                    y = 0
                }
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        stmt = scene_node.update_block[0]
        
        assert isinstance(stmt, IfNode)
        assert len(stmt.then_block) > 0
        assert stmt.else_block is not None
        assert len(stmt.else_block) > 0
    
    def test_while_statement(self):
        """Test parsing while statements."""
        source = """
        scene Test {
            update {
                while x < 100 {
                    x = x + 1
                }
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        scene_node = ast.declarations[0]
        stmt = scene_node.update_block[0]
        
        assert isinstance(stmt, WhileNode)
        assert isinstance(stmt.condition, BinaryOpNode)
        assert len(stmt.body) > 0


class TestErrorReporting:
    """Test error reporting and recovery."""
    
    def test_missing_brace(self):
        """Test error reporting for missing brace."""
        source = """
        game MyGame {
            title = "Test"
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert parser.has_errors()
        errors = parser.get_errors()
        assert len(errors) > 0
    
    def test_unexpected_token(self):
        """Test error reporting for unexpected token."""
        source = """
        invalid MyGame { }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert parser.has_errors()
    
    def test_error_message_format(self):
        """Test that error messages include location information."""
        source = """
        game MyGame {
            title =
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert parser.has_errors()
        errors = parser.get_errors()
        assert len(errors) > 0
        
        # Check that error has location
        error = errors[0]
        assert error.location is not None
        assert error.location.line > 0


class TestComplexPrograms:
    """Test parsing complete programs."""
    
    def test_complete_game_program(self):
        """Test parsing a complete game program."""
        source = """
        game MyGame {
            title = "Test Game"
            width = 800
            height = 600
        }
        
        sprite Player {
            x = 400
            y = 300
            speed = 5
            
            on keydown(key) {
                if key == "LEFT" {
                    x = x - speed
                }
            }
        }
        
        scene MainScene {
            player = Player()
            
            update {
                x = x + 1
            }
            
            draw {
                screen.fill()
            }
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        assert len(ast.declarations) == 3
        
        # Verify each declaration type
        assert isinstance(ast.declarations[0], GameNode)
        assert isinstance(ast.declarations[1], SpriteNode)
        assert isinstance(ast.declarations[2], SceneNode)
    
    def test_multiple_sprites(self):
        """Test parsing multiple sprite declarations."""
        source = """
        sprite Player {
            x = 100
        }
        
        sprite Enemy {
            x = 200
        }
        """
        lexer = Lexer(source, "test.lvl")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        ast = parser.parse()
        
        assert not parser.has_errors()
        assert len(ast.declarations) == 2
        assert all(isinstance(d, SpriteNode) for d in ast.declarations)
