"""Semantic analyzer for validating AST."""

from typing import List, Optional, Any, Dict

from levlang.core.ast_node import (
    ASTNode, ProgramNode, GameNode, SpriteNode, SceneNode,
    EventHandlerNode, MethodNode, ExpressionNode, StatementNode,
    LiteralNode, IdentifierNode, BinaryOpNode, UnaryOpNode,
    CallNode, MemberAccessNode, AssignmentNode, IfNode,
    WhileNode, ForNode, ReturnNode, ExpressionStatementNode,
    PythonBlockNode
)
from levlang.semantic.symbol_table import SymbolTable, SymbolKind
from levlang.semantic.semantic_error import SemanticError, ErrorType


# Type inference helpers
class Type:
    """Represents a type in the type system."""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    UNKNOWN = "unknown"
    SPRITE = "sprite"
    SCENE = "scene"


class SemanticAnalyzer:
    """Analyzes AST for semantic correctness."""
    
    def __init__(self, ast: ProgramNode):
        """Initialize the semantic analyzer.
        
        Args:
            ast: The program AST to analyze
        """
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_sprite: Optional[str] = None
        self.current_scene: Optional[str] = None
        self.type_cache: Dict[int, str] = {}  # Cache inferred types using id(node)
        self.game_declared = False  # Track if a game has been declared
    
    def analyze(self) -> bool:
        """Perform semantic analysis on the AST.
        
        Returns:
            True if no errors were found, False otherwise
        """
        self.visit_program(self.ast)
        return len(self.errors) == 0
    
    def report_error(self, error_type: ErrorType, message: str, location):
        """Report a semantic error.
        
        Args:
            error_type: The type of error
            message: The error message
            location: The source location of the error
        """
        error = SemanticError(error_type, message, location)
        self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if any semantic errors were found.
        
        Returns:
            True if there are errors, False otherwise
        """
        return len(self.errors) > 0
    
    def get_errors(self) -> List[SemanticError]:
        """Get all semantic errors.
        
        Returns:
            A list of semantic errors
        """
        return self.errors
    
    # Visitor methods for each node type
    
    def visit_program(self, node: ProgramNode):
        """Visit a program node."""
        for declaration in node.declarations:
            self.visit(declaration)
    
    def visit_game(self, node: GameNode):
        """Visit a game node."""
        # Only allow one game declaration per program
        if self.game_declared:
            self.report_error(
                ErrorType.DUPLICATE_DECLARATION,
                f"Only one game can be declared per program. Found additional game '{node.name}'",
                node.location
            )
            return
        
        self.game_declared = True
        
        # Declare the game in the symbol table
        if not self.symbol_table.declare(node.name, SymbolKind.GAME, node.location):
            self.report_error(
                ErrorType.DUPLICATE_DECLARATION,
                f"Game '{node.name}' is already declared",
                node.location
            )
        
        # Visit property expressions
        for prop_name, prop_value in node.properties.items():
            if isinstance(prop_value, ExpressionNode):
                self.visit(prop_value)
    
    def visit_sprite(self, node: SpriteNode):
        """Visit a sprite node."""
        # Declare the sprite in the symbol table
        if not self.symbol_table.declare(node.name, SymbolKind.SPRITE, node.location):
            self.report_error(
                ErrorType.DUPLICATE_DECLARATION,
                f"Sprite '{node.name}' is already declared",
                node.location
            )
        
        # Enter sprite scope
        self.current_sprite = node.name
        self.symbol_table.enter_scope()
        
        # Visit property expressions
        for prop_name, prop_value in node.properties.items():
            # Declare property as variable in sprite scope
            self.symbol_table.declare(prop_name, SymbolKind.VARIABLE, node.location)
            if isinstance(prop_value, ExpressionNode):
                self.visit(prop_value)
        
        # Visit methods (event handlers)
        for method in node.methods:
            self.visit(method)
        
        # Exit sprite scope
        self.symbol_table.exit_scope()
        self.current_sprite = None
    
    def visit_scene(self, node: SceneNode):
        """Visit a scene node."""
        # Declare the scene in the symbol table
        if not self.symbol_table.declare(node.name, SymbolKind.SCENE, node.location):
            self.report_error(
                ErrorType.DUPLICATE_DECLARATION,
                f"Scene '{node.name}' is already declared",
                node.location
            )
        
        # Enter scene scope
        self.current_scene = node.name
        self.symbol_table.enter_scope()
        
        # Visit members (property assignments)
        for member in node.members:
            self.visit(member)
        
        # Visit update block
        if node.update_block:
            for stmt in node.update_block:
                self.visit(stmt)
        
        # Visit draw block
        if node.draw_block:
            for stmt in node.draw_block:
                self.visit(stmt)
        
        # Exit scene scope
        self.symbol_table.exit_scope()
        self.current_scene = None
    
    def visit_event_handler(self, node: EventHandlerNode):
        """Visit an event handler node."""
        # Validate event type
        valid_event_types = {
            'keydown': ['key'],
            'keyup': ['key'],
            'mousedown': ['button'],
            'mouseup': ['button'],
            'mousemove': ['x', 'y'],
            'click': ['x', 'y'],
        }
        
        if node.event_type not in valid_event_types:
            self.report_error(
                ErrorType.INVALID_EVENT_HANDLER,
                f"Unknown event type '{node.event_type}'. Valid types are: {', '.join(valid_event_types.keys())}",
                node.location
            )
        else:
            # Validate parameter names
            expected_params = valid_event_types[node.event_type]
            if len(node.parameters) != len(expected_params):
                self.report_error(
                    ErrorType.INVALID_EVENT_HANDLER,
                    f"Event handler '{node.event_type}' expects {len(expected_params)} parameter(s): {', '.join(expected_params)}, got {len(node.parameters)}",
                    node.location
                )
        
        # Enter event handler scope
        self.symbol_table.enter_scope()
        
        # Declare parameters
        for param in node.parameters:
            if not self.symbol_table.declare(param, SymbolKind.PARAMETER, node.location):
                self.report_error(
                    ErrorType.DUPLICATE_DECLARATION,
                    f"Parameter '{param}' is already declared",
                    node.location
                )
        
        # Visit body statements
        for stmt in node.body:
            self.visit(stmt)
        
        # Exit event handler scope
        self.symbol_table.exit_scope()
    
    def visit_method(self, node: MethodNode):
        """Visit a method node."""
        # Enter method scope
        self.symbol_table.enter_scope()
        
        # Declare parameters
        for param in node.parameters:
            if not self.symbol_table.declare(param, SymbolKind.PARAMETER, node.location):
                self.report_error(
                    ErrorType.DUPLICATE_DECLARATION,
                    f"Parameter '{param}' is already declared",
                    node.location
                )
        
        # Visit body statements
        for stmt in node.body:
            self.visit(stmt)
        
        # Exit method scope
        self.symbol_table.exit_scope()
    
    def visit_assignment(self, node: AssignmentNode):
        """Visit an assignment node."""
        # Check if variable exists in current scope or any parent scope
        # Only declare as new variable if it doesn't exist anywhere
        if not self.symbol_table.lookup(node.target):
            self.symbol_table.declare(node.target, SymbolKind.VARIABLE, node.location)
        
        # Visit the value expression
        if node.value:
            self.visit(node.value)
    
    def visit_if(self, node: IfNode):
        """Visit an if statement node."""
        # Visit condition
        if node.condition:
            self.visit(node.condition)
        
        # Visit then block
        self.symbol_table.enter_scope()
        for stmt in node.then_block:
            self.visit(stmt)
        self.symbol_table.exit_scope()
        
        # Visit else block if present
        if node.else_block:
            self.symbol_table.enter_scope()
            for stmt in node.else_block:
                self.visit(stmt)
            self.symbol_table.exit_scope()
    
    def visit_while(self, node: WhileNode):
        """Visit a while loop node."""
        # Visit condition
        if node.condition:
            self.visit(node.condition)
        
        # Visit body
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
    
    def visit_for(self, node: ForNode):
        """Visit a for loop node."""
        # Enter loop scope
        self.symbol_table.enter_scope()
        
        # Declare loop variable
        self.symbol_table.declare(node.variable, SymbolKind.VARIABLE, node.location)
        
        # Visit iterable expression
        if node.iterable:
            self.visit(node.iterable)
        
        # Visit body
        for stmt in node.body:
            self.visit(stmt)
        
        # Exit loop scope
        self.symbol_table.exit_scope()
    
    def visit_return(self, node: ReturnNode):
        """Visit a return statement node."""
        if node.value:
            self.visit(node.value)
    
    def visit_expression_statement(self, node: ExpressionStatementNode):
        """Visit an expression statement node."""
        if node.expression:
            self.visit(node.expression)
    
    def visit_literal(self, node: LiteralNode):
        """Visit a literal node."""
        # Infer type from literal value
        if isinstance(node.value, bool):
            self.type_cache[id(node)] = Type.BOOLEAN
        elif isinstance(node.value, (int, float)):
            self.type_cache[id(node)] = Type.NUMBER
        elif isinstance(node.value, str):
            self.type_cache[id(node)] = Type.STRING
        else:
            self.type_cache[id(node)] = Type.UNKNOWN
    
    def visit_identifier(self, node: IdentifierNode):
        """Visit an identifier node."""
        # Check if identifier is defined
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.report_error(
                ErrorType.UNDEFINED_REFERENCE,
                f"Undefined reference to '{node.name}'",
                node.location
            )
            self.type_cache[id(node)] = Type.UNKNOWN
        else:
            # Infer type from symbol
            if symbol.type_info:
                self.type_cache[id(node)] = symbol.type_info
            elif symbol.kind == SymbolKind.SPRITE:
                self.type_cache[id(node)] = Type.SPRITE
            elif symbol.kind == SymbolKind.SCENE:
                self.type_cache[id(node)] = Type.SCENE
            else:
                self.type_cache[id(node)] = Type.UNKNOWN
    
    def visit_binary_op(self, node: BinaryOpNode):
        """Visit a binary operation node."""
        # Visit operands
        if node.left:
            self.visit(node.left)
        if node.right:
            self.visit(node.right)
        
        # Type checking for binary operations
        left_type = self.type_cache.get(id(node.left), Type.UNKNOWN)
        right_type = self.type_cache.get(id(node.right), Type.UNKNOWN)
        
        # Arithmetic operators require numbers
        if node.operator in ['+', '-', '*', '/', '%']:
            if left_type != Type.UNKNOWN and left_type != Type.NUMBER:
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Operator '{node.operator}' requires number operands, got {left_type}",
                    node.location
                )
            if right_type != Type.UNKNOWN and right_type != Type.NUMBER:
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Operator '{node.operator}' requires number operands, got {right_type}",
                    node.location
                )
            self.type_cache[id(node)] = Type.NUMBER
        
        # Comparison operators
        elif node.operator in ['<', '<=', '>', '>=']:
            if left_type != Type.UNKNOWN and left_type != Type.NUMBER:
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Comparison operator '{node.operator}' requires number operands, got {left_type}",
                    node.location
                )
            if right_type != Type.UNKNOWN and right_type != Type.NUMBER:
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Comparison operator '{node.operator}' requires number operands, got {right_type}",
                    node.location
                )
            self.type_cache[id(node)] = Type.BOOLEAN
        
        # Equality operators
        elif node.operator in ['==', '!=']:
            # Equality works on any type, but types should match
            if (left_type != Type.UNKNOWN and right_type != Type.UNKNOWN and 
                left_type != right_type):
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Cannot compare {left_type} with {right_type}",
                    node.location
                )
            self.type_cache[id(node)] = Type.BOOLEAN
        
        # Logical operators
        elif node.operator in ['&&', '||']:
            self.type_cache[id(node)] = Type.BOOLEAN
        
        else:
            self.type_cache[id(node)] = Type.UNKNOWN
    
    def visit_unary_op(self, node: UnaryOpNode):
        """Visit a unary operation node."""
        if node.operand:
            self.visit(node.operand)
        
        # Type checking for unary operations
        operand_type = self.type_cache.get(id(node.operand), Type.UNKNOWN)
        
        if node.operator == '-':
            if operand_type != Type.UNKNOWN and operand_type != Type.NUMBER:
                self.report_error(
                    ErrorType.TYPE_MISMATCH,
                    f"Unary minus requires number operand, got {operand_type}",
                    node.location
                )
            self.type_cache[id(node)] = Type.NUMBER
        elif node.operator in ['not', '!']:
            self.type_cache[id(node)] = Type.BOOLEAN
        else:
            self.type_cache[id(node)] = Type.UNKNOWN
    
    def visit_call(self, node: CallNode):
        """Visit a function call node."""
        # Visit callee
        if node.callee:
            self.visit(node.callee)
        
        # Visit arguments
        for arg in node.arguments:
            self.visit(arg)
        
        # Check if calling a sprite constructor
        if isinstance(node.callee, IdentifierNode):
            symbol = self.symbol_table.lookup(node.callee.name)
            if symbol and symbol.kind == SymbolKind.SPRITE:
                self.type_cache[id(node)] = Type.SPRITE
            else:
                self.type_cache[id(node)] = Type.UNKNOWN
        else:
            self.type_cache[id(node)] = Type.UNKNOWN
    
    def visit_member_access(self, node: MemberAccessNode):
        """Visit a member access node."""
        # Visit the object
        if node.object:
            self.visit(node.object)
        
        # Member name checking would require type information
        # For now, we just visit the object
    
    def visit_python_block(self, node: PythonBlockNode):
        """Visit a Python block node."""
        # Python blocks are passed through without semantic checking
        pass
    
    def visit(self, node: ASTNode):
        """Generic visit method that dispatches to specific visit methods.
        
        Args:
            node: The AST node to visit
        """
        if node is None:
            return
        
        # Map node types to visit methods
        visit_methods = {
            "program": self.visit_program,
            "game": self.visit_game,
            "sprite": self.visit_sprite,
            "scene": self.visit_scene,
            "event_handler": self.visit_event_handler,
            "method": self.visit_method,
            "assignment": self.visit_assignment,
            "if": self.visit_if,
            "while": self.visit_while,
            "for": self.visit_for,
            "return": self.visit_return,
            "expression_statement": self.visit_expression_statement,
            "literal": self.visit_literal,
            "identifier": self.visit_identifier,
            "binary_op": self.visit_binary_op,
            "unary_op": self.visit_unary_op,
            "call": self.visit_call,
            "member_access": self.visit_member_access,
            "python_block": self.visit_python_block,
        }
        
        # Get the visit method for this node type
        visit_method = visit_methods.get(node.node_type)
        if visit_method:
            visit_method(node)
        else:
            # Generic visit for unknown node types
            pass
