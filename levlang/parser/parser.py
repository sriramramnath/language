"""Parser for the game language."""

from typing import List, Optional

from levlang.core.token import Token, TokenType
from levlang.core.ast_node import (
    ASTNode, ProgramNode, GameNode, SpriteNode, SceneNode,
    EventHandlerNode, MethodNode, ExpressionNode, StatementNode,
    LiteralNode, IdentifierNode, BinaryOpNode, UnaryOpNode,
    CallNode, MemberAccessNode, AssignmentNode, IfNode,
    WhileNode, ForNode, ReturnNode, ExpressionStatementNode,
    PythonBlockNode
)
from levlang.core.source_location import SourceLocation


class ParseError(Exception):
    """Exception raised during parsing."""
    
    def __init__(self, message: str, location: SourceLocation):
        self.message = message
        self.location = location
        super().__init__(f"{location}: {message}")


class Parser:
    """Parses tokens into an Abstract Syntax Tree."""
    
    def __init__(self, tokens: List[Token]):
        """Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.position = 0
        self.errors: List[ParseError] = []
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the token stream."""
        return self.peek().type == TokenType.EOF
    
    def peek(self, offset: int = 0) -> Token:
        """Peek at a token without consuming it.
        
        Args:
            offset: How many tokens ahead to peek (0 = current)
            
        Returns:
            The token at position + offset
        """
        pos = self.position + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Consume and return the current token.
        
        Returns:
            The current token
        """
        token = self.peek()
        if not self.is_at_end():
            self.position += 1
        return token
    
    def check(self, token_type: TokenType) -> bool:
        """Check if the current token is of the given type.
        
        Args:
            token_type: The token type to check
            
        Returns:
            True if current token matches the type, False otherwise
        """
        return self.peek().type == token_type
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if the current token matches any of the given types.
        
        Args:
            token_types: Token types to match against
            
        Returns:
            True if current token matches any type, False otherwise
        """
        for token_type in token_types:
            if self.check(token_type):
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consume a token of the expected type or raise an error.
        
        This is the expect() method mentioned in the requirements.
        
        Args:
            token_type: The expected token type
            message: Error message if token doesn't match
            
        Returns:
            The consumed token
            
        Raises:
            ParseError: If the current token doesn't match the expected type
        """
        if self.check(token_type):
            return self.advance()
        
        current = self.peek()
        error = ParseError(message, current.location)
        self.errors.append(error)
        raise error
    
    def expect(self, token_type: TokenType, message: str) -> Token:
        """Alias for consume() - expect a specific token type.
        
        Args:
            token_type: The expected token type
            message: Error message if token doesn't match
            
        Returns:
            The consumed token
        """
        return self.consume(token_type, message)
    
    def synchronize(self):
        """Synchronize parser state after an error for error recovery.
        
        This advances the parser to the next statement boundary to continue
        parsing after encountering an error.
        """
        self.advance()
        
        while not self.is_at_end():
            # Synchronize at statement boundaries
            if self.peek(-1).type == TokenType.SEMICOLON:
                return
            
            # Synchronize at declaration keywords
            if self.match(
                TokenType.GAME,
                TokenType.SPRITE,
                TokenType.SCENE,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.FOR,
                TokenType.RETURN
            ):
                return
            
            self.advance()
    
    def report_error(self, message: str, location: Optional[SourceLocation] = None):
        """Report a parse error without raising an exception.
        
        Args:
            message: The error message
            location: The source location of the error (uses current token if None)
        """
        if location is None:
            location = self.peek().location
        error = ParseError(message, location)
        self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if any parse errors were encountered.
        
        Returns:
            True if there are errors, False otherwise
        """
        return len(self.errors) > 0
    
    def get_errors(self) -> List[ParseError]:
        """Get all parse errors.
        
        Returns:
            A list of parse errors
        """
        return self.errors
    
    def parse_game_declaration(self) -> GameNode:
        """Parse a game declaration.
        
        Grammar:
            game_decl := 'game' identifier '{' game_property* '}'
            game_property := identifier '=' expression
        
        Returns:
            A GameNode representing the game declaration
        """
        start_token = self.expect(TokenType.GAME, "Expected 'game' keyword")
        name_token = self.expect(TokenType.IDENTIFIER, "Expected game name after 'game'")
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after game name")
        
        properties = {}
        
        # Parse game properties
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            # Parse property name
            prop_name_token = self.expect(TokenType.IDENTIFIER, "Expected property name")
            prop_name = prop_name_token.value
            
            self.expect(TokenType.EQUAL, f"Expected '=' after property name '{prop_name}'")
            
            # Parse property value (expression)
            prop_value = self.parse_expression()
            
            properties[prop_name] = prop_value
            
            # Optional comma or newline between properties
            if self.match(TokenType.COMMA, TokenType.NEWLINE):
                self.advance()
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after game properties")
        
        return GameNode(
            node_type="game",
            location=start_token.location,
            name=name_token.value,
            properties=properties
        )
    
    def parse_sprite_declaration(self) -> SpriteNode:
        """Parse a sprite declaration.
        
        Grammar:
            sprite_decl := 'sprite' identifier '{' sprite_member* '}'
            sprite_member := property_decl | event_handler
            property_decl := identifier '=' expression
        
        Returns:
            A SpriteNode representing the sprite declaration
        """
        start_token = self.expect(TokenType.SPRITE, "Expected 'sprite' keyword")
        name_token = self.expect(TokenType.IDENTIFIER, "Expected sprite name after 'sprite'")
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after sprite name")
        
        properties = {}
        methods = []
        
        # Parse sprite members (properties and event handlers)
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            # Check for event handler (starts with 'on')
            if self.check(TokenType.ON):
                event_handler = self.parse_event_handler()
                methods.append(event_handler)
            # Otherwise, parse as property
            elif self.check(TokenType.IDENTIFIER):
                prop_name_token = self.advance()
                prop_name = prop_name_token.value
                
                self.expect(TokenType.EQUAL, f"Expected '=' after property name '{prop_name}'")
                
                prop_value = self.parse_expression()
                properties[prop_name] = prop_value
                
                # Optional comma or newline
                if self.match(TokenType.COMMA, TokenType.NEWLINE):
                    self.advance()
            else:
                self.report_error(f"Expected property or event handler, got {self.peek().type.name}")
                self.synchronize()
                break
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after sprite members")
        
        return SpriteNode(
            node_type="sprite",
            location=start_token.location,
            name=name_token.value,
            properties=properties,
            methods=methods
        )
    
    def parse_scene_declaration(self) -> SceneNode:
        """Parse a scene declaration.
        
        Grammar:
            scene_decl := 'scene' identifier '{' scene_member* '}'
            scene_member := property_decl | update_block | draw_block
            update_block := 'update' '{' statement* '}'
            draw_block := 'draw' '{' statement* '}'
        
        Returns:
            A SceneNode representing the scene declaration
        """
        start_token = self.expect(TokenType.SCENE, "Expected 'scene' keyword")
        name_token = self.expect(TokenType.IDENTIFIER, "Expected scene name after 'scene'")
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after scene name")
        
        members = []
        update_block = None
        draw_block = None
        
        # Parse scene members
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            # Check for update block
            if self.check(TokenType.UPDATE):
                self.advance()
                self.expect(TokenType.LEFT_BRACE, "Expected '{' after 'update'")
                
                statements = []
                while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
                    stmt = self.parse_statement()
                    if stmt:
                        statements.append(stmt)
                
                self.expect(TokenType.RIGHT_BRACE, "Expected '}' after update block")
                update_block = statements
            
            # Check for draw block
            elif self.check(TokenType.DRAW):
                self.advance()
                self.expect(TokenType.LEFT_BRACE, "Expected '{' after 'draw'")
                
                statements = []
                while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
                    stmt = self.parse_statement()
                    if stmt:
                        statements.append(stmt)
                
                self.expect(TokenType.RIGHT_BRACE, "Expected '}' after draw block")
                draw_block = statements
            
            # Parse as property/statement
            elif self.check(TokenType.IDENTIFIER):
                # This could be a property assignment
                prop_name_token = self.advance()
                
                if self.check(TokenType.EQUAL):
                    self.advance()
                    prop_value = self.parse_expression()
                    
                    # Create an assignment statement
                    assignment = AssignmentNode(
                        node_type="assignment",
                        stmt_type="assignment",
                        location=prop_name_token.location,
                        target=prop_name_token.value,
                        value=prop_value
                    )
                    members.append(assignment)
                    
                    # Optional comma or newline
                    if self.match(TokenType.COMMA, TokenType.NEWLINE):
                        self.advance()
                else:
                    # Put the token back and parse as statement
                    self.position -= 1
                    stmt = self.parse_statement()
                    if stmt:
                        members.append(stmt)
            else:
                self.report_error(f"Expected scene member, got {self.peek().type.name}")
                self.synchronize()
                break
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after scene members")
        
        return SceneNode(
            node_type="scene",
            location=start_token.location,
            name=name_token.value,
            members=members,
            update_block=update_block,
            draw_block=draw_block
        )
    
    def parse_expression(self) -> ExpressionNode:
        """Parse an expression.
        
        This is the entry point for expression parsing.
        
        Returns:
            An ExpressionNode representing the expression
        """
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> ExpressionNode:
        """Parse logical OR expression (lowest precedence)."""
        left = self.parse_and_expression()
        
        while self.check(TokenType.OR):
            op_token = self.advance()
            right = self.parse_and_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator="or",
                left=left,
                right=right
            )
        
        return left
    
    def parse_and_expression(self) -> ExpressionNode:
        """Parse logical AND expression."""
        left = self.parse_equality_expression()
        
        while self.check(TokenType.AND):
            op_token = self.advance()
            right = self.parse_equality_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator="and",
                left=left,
                right=right
            )
        
        return left
    
    def parse_equality_expression(self) -> ExpressionNode:
        """Parse equality expression (==, !=)."""
        left = self.parse_comparison_expression()
        
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op_token = self.advance()
            right = self.parse_comparison_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator=op_token.value,
                left=left,
                right=right
            )
        
        return left
    
    def parse_comparison_expression(self) -> ExpressionNode:
        """Parse comparison expression (<, <=, >, >=)."""
        left = self.parse_additive_expression()
        
        while self.match(TokenType.LESS, TokenType.LESS_EQUAL, 
                         TokenType.GREATER, TokenType.GREATER_EQUAL):
            op_token = self.advance()
            right = self.parse_additive_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator=op_token.value,
                left=left,
                right=right
            )
        
        return left
    
    def parse_additive_expression(self) -> ExpressionNode:
        """Parse additive expression (+, -)."""
        left = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            right = self.parse_multiplicative_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator=op_token.value,
                left=left,
                right=right
            )
        
        return left
    
    def parse_multiplicative_expression(self) -> ExpressionNode:
        """Parse multiplicative expression (*, /, %)."""
        left = self.parse_unary_expression()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.parse_unary_expression()
            left = BinaryOpNode(
                node_type="binary_op",
                expr_type="binary_op",
                location=op_token.location,
                operator=op_token.value,
                left=left,
                right=right
            )
        
        return left
    
    def parse_unary_expression(self) -> ExpressionNode:
        """Parse unary expression (-, not)."""
        if self.match(TokenType.MINUS, TokenType.NOT):
            op_token = self.advance()
            operand = self.parse_unary_expression()
            return UnaryOpNode(
                node_type="unary_op",
                expr_type="unary_op",
                location=op_token.location,
                operator=op_token.value,
                operand=operand
            )
        
        return self.parse_postfix_expression()
    
    def parse_postfix_expression(self) -> ExpressionNode:
        """Parse postfix expression (function calls, member access)."""
        expr = self.parse_primary_expression()
        
        while True:
            # Function call
            if self.check(TokenType.LEFT_PAREN):
                self.advance()
                arguments = []
                
                if not self.check(TokenType.RIGHT_PAREN):
                    arguments.append(self.parse_expression())
                    
                    while self.check(TokenType.COMMA):
                        self.advance()
                        arguments.append(self.parse_expression())
                
                close_paren = self.expect(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
                
                expr = CallNode(
                    node_type="call",
                    expr_type="call",
                    location=close_paren.location,
                    callee=expr,
                    arguments=arguments
                )
            
            # Member access
            elif self.check(TokenType.DOT):
                self.advance()
                member_token = self.expect(TokenType.IDENTIFIER, "Expected member name after '.'")
                
                expr = MemberAccessNode(
                    node_type="member_access",
                    expr_type="member_access",
                    location=member_token.location,
                    object=expr,
                    member=member_token.value
                )
            
            else:
                break
        
        return expr
    
    def parse_primary_expression(self) -> ExpressionNode:
        """Parse primary expression (literals, identifiers, parenthesized expressions)."""
        # Number literal
        if self.check(TokenType.NUMBER):
            token = self.advance()
            return LiteralNode(
                node_type="literal",
                expr_type="literal",
                location=token.location,
                value=token.value
            )
        
        # String literal
        if self.check(TokenType.STRING):
            token = self.advance()
            return LiteralNode(
                node_type="literal",
                expr_type="literal",
                location=token.location,
                value=token.value
            )
        
        # Boolean literals
        if self.match(TokenType.TRUE, TokenType.FALSE):
            token = self.advance()
            return LiteralNode(
                node_type="literal",
                expr_type="literal",
                location=token.location,
                value=token.value
            )
        
        # Identifier
        if self.check(TokenType.IDENTIFIER):
            token = self.advance()
            return IdentifierNode(
                node_type="identifier",
                expr_type="identifier",
                location=token.location,
                name=token.value
            )
        
        # Parenthesized expression
        if self.check(TokenType.LEFT_PAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        # Error: unexpected token
        token = self.peek()
        self.report_error(f"Expected expression, got {token.type.name}", token.location)
        
        # Return a dummy literal to continue parsing
        return LiteralNode(
            node_type="literal",
            expr_type="literal",
            location=token.location,
            value=None
        )
    
    def parse_statement(self) -> Optional[StatementNode]:
        """Parse a statement.
        
        Returns:
            A StatementNode, or None if no statement could be parsed
        """
        # Skip newlines
        while self.check(TokenType.NEWLINE):
            self.advance()
        
        # If statement
        if self.check(TokenType.IF):
            return self.parse_if_statement()
        
        # While loop
        if self.check(TokenType.WHILE):
            return self.parse_while_statement()
        
        # For loop
        if self.check(TokenType.FOR):
            return self.parse_for_statement()
        
        # Return statement
        if self.check(TokenType.RETURN):
            return self.parse_return_statement()
        
        # Event handler (on keyword)
        if self.check(TokenType.ON):
            return self.parse_event_handler()
        
        # Assignment or expression statement
        if self.check(TokenType.IDENTIFIER):
            # Look ahead to determine if it's an assignment
            if self.peek(1).type == TokenType.EQUAL:
                return self.parse_assignment_statement()
            else:
                return self.parse_expression_statement()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_assignment_statement(self) -> AssignmentNode:
        """Parse an assignment statement.
        
        Grammar:
            assignment := identifier '=' expression
        
        Returns:
            An AssignmentNode
        """
        target_token = self.expect(TokenType.IDENTIFIER, "Expected identifier")
        self.expect(TokenType.EQUAL, "Expected '=' in assignment")
        value = self.parse_expression()
        
        # Optional semicolon or newline
        if self.match(TokenType.SEMICOLON, TokenType.NEWLINE):
            self.advance()
        
        return AssignmentNode(
            node_type="assignment",
            stmt_type="assignment",
            location=target_token.location,
            target=target_token.value,
            value=value
        )
    
    def parse_if_statement(self) -> IfNode:
        """Parse an if statement.
        
        Grammar:
            if_stmt := 'if' expression '{' statement* '}' ('else' '{' statement* '}')?
        
        Returns:
            An IfNode
        """
        start_token = self.expect(TokenType.IF, "Expected 'if'")
        condition = self.parse_expression()
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after if condition")
        
        then_block = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after if block")
        
        # Optional else block
        else_block = None
        if self.check(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.LEFT_BRACE, "Expected '{' after 'else'")
            
            else_block = []
            while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
            
            self.expect(TokenType.RIGHT_BRACE, "Expected '}' after else block")
        
        return IfNode(
            node_type="if",
            stmt_type="if",
            location=start_token.location,
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def parse_while_statement(self) -> WhileNode:
        """Parse a while loop statement.
        
        Grammar:
            while_stmt := 'while' expression '{' statement* '}'
        
        Returns:
            A WhileNode
        """
        start_token = self.expect(TokenType.WHILE, "Expected 'while'")
        condition = self.parse_expression()
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after while condition")
        
        body = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after while block")
        
        return WhileNode(
            node_type="while",
            stmt_type="while",
            location=start_token.location,
            condition=condition,
            body=body
        )
    
    def parse_for_statement(self) -> ForNode:
        """Parse a for loop statement.
        
        Grammar:
            for_stmt := 'for' identifier 'in' expression '{' statement* '}'
        
        Returns:
            A ForNode
        """
        start_token = self.expect(TokenType.FOR, "Expected 'for'")
        var_token = self.expect(TokenType.IDENTIFIER, "Expected variable name after 'for'")
        
        # Expect the 'in' keyword token (lexer produces TokenType.IN)
        in_token = self.expect(TokenType.IN, "Expected 'in' after variable name")
        
        iterable = self.parse_expression()
        
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after for expression")
        
        body = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after for block")
        
        return ForNode(
            node_type="for",
            stmt_type="for",
            location=start_token.location,
            variable=var_token.value,
            iterable=iterable,
            body=body
        )
    
    def parse_return_statement(self) -> ReturnNode:
        """Parse a return statement.
        
        Grammar:
            return_stmt := 'return' expression?
        
        Returns:
            A ReturnNode
        """
        start_token = self.expect(TokenType.RETURN, "Expected 'return'")
        
        # Optional return value
        value = None
        if not self.match(TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.RIGHT_BRACE):
            value = self.parse_expression()
        
        # Optional semicolon or newline
        if self.match(TokenType.SEMICOLON, TokenType.NEWLINE):
            self.advance()
        
        return ReturnNode(
            node_type="return",
            stmt_type="return",
            location=start_token.location,
            value=value
        )
    
    def parse_expression_statement(self) -> ExpressionStatementNode:
        """Parse an expression statement.
        
        Returns:
            An ExpressionStatementNode
        """
        expr = self.parse_expression()
        
        # Optional semicolon or newline
        if self.match(TokenType.SEMICOLON, TokenType.NEWLINE):
            self.advance()
        
        return ExpressionStatementNode(
            node_type="expression_statement",
            stmt_type="expression_statement",
            location=expr.location,
            expression=expr
        )
    
    def parse_event_handler(self) -> EventHandlerNode:
        """Parse an event handler declaration.
        
        Grammar:
            event_handler := 'on' identifier '(' parameter_list? ')' '{' statement* '}'
        
        Returns:
            An EventHandlerNode
        """
        start_token = self.expect(TokenType.ON, "Expected 'on'")
        event_type_token = self.expect(TokenType.IDENTIFIER, "Expected event type after 'on'")
        
        self.expect(TokenType.LEFT_PAREN, "Expected '(' after event type")
        
        # Parse parameters
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            param_token = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
            parameters.append(param_token.value)
            
            while self.check(TokenType.COMMA):
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
                parameters.append(param_token.value)
        
        self.expect(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        self.expect(TokenType.LEFT_BRACE, "Expected '{' after event handler signature")
        
        # Parse body
        body = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RIGHT_BRACE, "Expected '}' after event handler body")
        
        return EventHandlerNode(
            node_type="event_handler",
            location=start_token.location,
            event_type=event_type_token.value,
            parameters=parameters,
            body=body
        )
    
    def parse_python_block(self) -> PythonBlockNode:
        """Parse a Python code block (passthrough).
        
        Python blocks are delimited by special markers that the lexer should
        recognize. For now, we'll look for a pattern like:
        
        ```python
        # Python code here
        ```
        
        Or we could use a simpler delimiter like `python { ... }`
        
        Returns:
            A PythonBlockNode containing raw Python code
        """
        # For this implementation, we'll assume Python blocks are marked
        # with a special token or pattern. Since we don't have a specific
        # token type for Python blocks yet, we'll implement a simple approach:
        # Look for comments that start with "###python" and end with "###end"
        
        # This is a placeholder implementation that would need to be
        # coordinated with the lexer to properly capture Python blocks
        
        start_location = self.peek().location
        
        # Collect raw Python code
        # In a real implementation, the lexer would handle this
        code_parts = []
        
        # For now, return an empty Python block
        # This will be properly implemented when we add Python block
        # token support to the lexer
        
        return PythonBlockNode(
            node_type="python_block",
            location=start_location,
            code=""
        )
    
    def parse(self) -> ProgramNode:
        """Parse the token stream into an AST.
        
        Returns:
            A ProgramNode representing the entire program
        """
        declarations = []
        
        # Skip leading newlines
        while self.check(TokenType.NEWLINE):
            self.advance()
        
        while not self.is_at_end():
            try:
                # Parse top-level declarations
                if self.check(TokenType.GAME):
                    declarations.append(self.parse_game_declaration())
                elif self.check(TokenType.SPRITE):
                    declarations.append(self.parse_sprite_declaration())
                elif self.check(TokenType.SCENE):
                    declarations.append(self.parse_scene_declaration())
                else:
                    # Unexpected token at top level
                    token = self.peek()
                    self.report_error(
                        f"Unexpected token '{token.value}' at top level. "
                        f"Expected 'game', 'sprite', or 'scene' declaration.",
                        token.location
                    )
                    self.synchronize()
                
                # Skip newlines between declarations
                while self.check(TokenType.NEWLINE):
                    self.advance()
                    
            except ParseError:
                # Error already reported, synchronize and continue
                self.synchronize()
        
        # Create program node with first token location or a default
        location = self.tokens[0].location if self.tokens else SourceLocation("<input>", 1, 1, 0)
        
        return ProgramNode(
            node_type="program",
            location=location,
            declarations=declarations
        )
    
    def format_error(self, error: ParseError, source_lines: Optional[List[str]] = None) -> str:
        """Format a parse error with context.
        
        Args:
            error: The parse error to format
            source_lines: Optional list of source code lines for context
            
        Returns:
            A formatted error message with source context
        """
        location = error.location
        message = error.message
        
        # Basic format: filename:line:column: error: message
        result = f"{location.filename}:{location.line}:{location.column}: error: {message}\n"
        
        # Add source context if available
        if source_lines and 0 < location.line <= len(source_lines):
            line_text = source_lines[location.line - 1]
            result += f"   |\n"
            result += f"{location.line:3} | {line_text}\n"
            result += f"   | {' ' * (location.column - 1)}^\n"
        
        return result
    
    def format_all_errors(self, source_lines: Optional[List[str]] = None) -> str:
        """Format all parse errors with context.
        
        Args:
            source_lines: Optional list of source code lines for context
            
        Returns:
            A formatted string containing all error messages
        """
        if not self.errors:
            return ""
        
        result = []
        for error in self.errors:
            result.append(self.format_error(error, source_lines))
        
        return "\n".join(result)
