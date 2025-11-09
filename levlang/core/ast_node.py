"""Abstract Syntax Tree node definitions."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from levlang.core.source_location import SourceLocation


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    
    node_type: str
    location: SourceLocation
    
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        method_name = f"visit_{self.node_type}"
        method = getattr(visitor, method_name, visitor.generic_visit)
        return method(self)


@dataclass
class ProgramNode(ASTNode):
    """Root node containing all top-level declarations."""
    
    declarations: List[ASTNode] = field(default_factory=list)
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "program"


@dataclass
class GameNode(ASTNode):
    """Game configuration and initialization."""
    
    name: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "game"


@dataclass
class SpriteNode(ASTNode):
    """Sprite definition with properties and methods."""
    
    name: str = ""
    properties: Dict[str, 'ExpressionNode'] = field(default_factory=dict)
    methods: List['MethodNode'] = field(default_factory=list)
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "sprite"


@dataclass
class SceneNode(ASTNode):
    """Scene definition with update/draw logic."""
    
    name: str = ""
    members: List[ASTNode] = field(default_factory=list)
    update_block: Optional[List['StatementNode']] = None
    draw_block: Optional[List['StatementNode']] = None
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "scene"


@dataclass
class EventHandlerNode(ASTNode):
    """Input event handler."""
    
    event_type: str = ""
    condition: Optional['ExpressionNode'] = None
    parameters: List[str] = field(default_factory=list)
    body: List['StatementNode'] = field(default_factory=list)
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "event_handler"


@dataclass
class MethodNode(ASTNode):
    """Method definition within a sprite or scene."""
    
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List['StatementNode'] = field(default_factory=list)
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "method"


@dataclass
class ExpressionNode(ASTNode):
    """Base class for expression nodes."""
    
    expr_type: str = ""
    value: Any = None
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "expression"


@dataclass
class LiteralNode(ExpressionNode):
    """Literal value (number, string, boolean)."""
    
    def __post_init__(self):
        self.node_type = "literal"
        self.expr_type = "literal"


@dataclass
class IdentifierNode(ExpressionNode):
    """Identifier reference."""
    
    name: str = ""
    
    def __post_init__(self):
        self.node_type = "identifier"
        self.expr_type = "identifier"


@dataclass
class BinaryOpNode(ExpressionNode):
    """Binary operation (e.g., a + b)."""
    
    operator: str = ""
    left: Optional[ExpressionNode] = None
    right: Optional[ExpressionNode] = None
    
    def __post_init__(self):
        self.node_type = "binary_op"
        self.expr_type = "binary_op"


@dataclass
class UnaryOpNode(ExpressionNode):
    """Unary operation (e.g., -x, not x)."""
    
    operator: str = ""
    operand: Optional[ExpressionNode] = None
    
    def __post_init__(self):
        self.node_type = "unary_op"
        self.expr_type = "unary_op"


@dataclass
class CallNode(ExpressionNode):
    """Function or method call."""
    
    callee: Optional[ExpressionNode] = None
    arguments: List[ExpressionNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = "call"
        self.expr_type = "call"


@dataclass
class MemberAccessNode(ExpressionNode):
    """Member access (e.g., obj.property)."""
    
    object: Optional[ExpressionNode] = None
    member: str = ""
    
    def __post_init__(self):
        self.node_type = "member_access"
        self.expr_type = "member_access"


@dataclass
class StatementNode(ASTNode):
    """Base class for statement nodes."""
    
    stmt_type: str = ""
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "statement"


@dataclass
class AssignmentNode(StatementNode):
    """Assignment statement."""
    
    target: str = ""
    value: Optional[ExpressionNode] = None
    
    def __post_init__(self):
        self.node_type = "assignment"
        self.stmt_type = "assignment"


@dataclass
class IfNode(StatementNode):
    """Conditional statement."""
    
    condition: Optional[ExpressionNode] = None
    then_block: List[StatementNode] = field(default_factory=list)
    else_block: Optional[List[StatementNode]] = None
    
    def __post_init__(self):
        self.node_type = "if"
        self.stmt_type = "if"


@dataclass
class WhileNode(StatementNode):
    """While loop statement."""
    
    condition: Optional[ExpressionNode] = None
    body: List[StatementNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = "while"
        self.stmt_type = "while"


@dataclass
class ForNode(StatementNode):
    """For loop statement."""
    
    variable: str = ""
    iterable: Optional[ExpressionNode] = None
    body: List[StatementNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = "for"
        self.stmt_type = "for"


@dataclass
class ReturnNode(StatementNode):
    """Return statement."""
    
    value: Optional[ExpressionNode] = None
    
    def __post_init__(self):
        self.node_type = "return"
        self.stmt_type = "return"


@dataclass
class ExpressionStatementNode(StatementNode):
    """Expression used as a statement."""
    
    expression: Optional[ExpressionNode] = None
    
    def __post_init__(self):
        self.node_type = "expression_statement"
        self.stmt_type = "expression_statement"


@dataclass
class PythonBlockNode(ASTNode):
    """Raw Python code block (passthrough)."""
    
    code: str = ""
    
    def __post_init__(self):
        if not hasattr(self, 'node_type') or self.node_type is None:
            self.node_type = "python_block"
