"""Lexer for the game language."""

from typing import List, Optional

from gamelang.core.token import Token, TokenType
from gamelang.core.source_location import SourceLocation


class Lexer:
    """Tokenizes game language source code into a stream of tokens."""
    
    # Keyword mapping
    KEYWORDS = {
        'game': TokenType.GAME,
        'sprite': TokenType.SPRITE,
        'scene': TokenType.SCENE,
        'on': TokenType.ON,
        'when': TokenType.WHEN,
        'update': TokenType.UPDATE,
        'draw': TokenType.DRAW,
        'input': TokenType.INPUT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
    }
    
    def __init__(self, source: str, filename: str = "<input>"):
        """Initialize the lexer with source code.
        
        Args:
            source: The source code to tokenize
            filename: The name of the source file for error reporting
        """
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []
    
    def peek_char(self, offset: int = 0) -> str:
        """Peek at a character without consuming it.
        
        Args:
            offset: How many characters ahead to peek (0 = current)
            
        Returns:
            The character at position + offset, or empty string if at end
        """
        pos = self.position + offset
        if pos >= len(self.source):
            return ''
        return self.source[pos]
    
    def advance(self) -> str:
        """Consume and return the current character.
        
        Returns:
            The current character, or empty string if at end
        """
        if self.position >= len(self.source):
            return ''
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char

    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the source."""
        return self.position >= len(self.source)
    
    def make_token(self, token_type: TokenType, value: any, start_line: int, start_column: int, length: int = 1) -> Token:
        """Create a token with location information.
        
        Args:
            token_type: The type of token
            value: The token's value
            start_line: The line where the token starts
            start_column: The column where the token starts
            length: The length of the token in characters
            
        Returns:
            A new Token instance
        """
        location = SourceLocation(
            filename=self.filename,
            line=start_line,
            column=start_column,
            length=length
        )
        return Token(type=token_type, value=value, location=location)
    
    def add_error(self, message: str, line: int, column: int):
        """Add a lexical error.
        
        Args:
            message: The error message
            line: The line where the error occurred
            column: The column where the error occurred
        """
        error = f"{self.filename}:{line}:{column}: error: {message}"
        self.errors.append(error)
    
    def skip_whitespace(self):
        """Skip whitespace characters while maintaining position tracking."""
        while not self.is_at_end():
            char = self.peek_char()
            if char in ' \t\r\n':
                self.advance()
            else:
                break
    
    def skip_line_comment(self):
        """Skip a single-line comment (// ...)."""
        # Skip the '//' characters
        self.advance()
        self.advance()
        
        # Skip until end of line or end of file
        while not self.is_at_end() and self.peek_char() != '\n':
            self.advance()
    
    def skip_block_comment(self):
        """Skip a multi-line comment (/* ... */)."""
        start_line = self.line
        start_column = self.column
        
        # Skip the '/*' characters
        self.advance()
        self.advance()
        
        # Skip until we find '*/' or reach end of file
        while not self.is_at_end():
            if self.peek_char() == '*' and self.peek_char(1) == '/':
                self.advance()  # Skip '*'
                self.advance()  # Skip '/'
                return
            self.advance()
        
        # If we reach here, the comment was not terminated
        self.add_error("unterminated block comment", start_line, start_column)
    
    def tokenize_identifier(self) -> Token:
        """Tokenize an identifier or keyword.
        
        Returns:
            A token representing an identifier or keyword
        """
        start_line = self.line
        start_column = self.column
        start_pos = self.position
        
        # Read alphanumeric characters and underscores
        while not self.is_at_end():
            char = self.peek_char()
            if char.isalnum() or char == '_':
                self.advance()
            else:
                break
        
        # Extract the identifier text
        value = self.source[start_pos:self.position]
        length = self.position - start_pos
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
        
        # For boolean keywords, convert to actual boolean values
        if token_type == TokenType.TRUE:
            return self.make_token(token_type, True, start_line, start_column, length)
        elif token_type == TokenType.FALSE:
            return self.make_token(token_type, False, start_line, start_column, length)
        
        return self.make_token(token_type, value, start_line, start_column, length)
    
    def tokenize_number(self) -> Token:
        """Tokenize a number literal (integer or float).
        
        Returns:
            A token representing a number
        """
        start_line = self.line
        start_column = self.column
        start_pos = self.position
        
        # Read digits
        while not self.is_at_end() and self.peek_char().isdigit():
            self.advance()
        
        # Check for decimal point
        if not self.is_at_end() and self.peek_char() == '.' and self.peek_char(1).isdigit():
            # Consume the '.'
            self.advance()
            
            # Read fractional part
            while not self.is_at_end() and self.peek_char().isdigit():
                self.advance()
        
        # Extract the number text and convert to appropriate type
        value_str = self.source[start_pos:self.position]
        length = self.position - start_pos
        
        if '.' in value_str:
            value = float(value_str)
        else:
            value = int(value_str)
        
        return self.make_token(TokenType.NUMBER, value, start_line, start_column, length)
    
    def tokenize_string(self) -> Token:
        """Tokenize a string literal with escape sequence support.
        
        Returns:
            A token representing a string, or an INVALID token if unterminated
        """
        start_line = self.line
        start_column = self.column
        start_pos = self.position
        
        # Skip opening quote
        quote_char = self.advance()
        
        value_parts = []
        
        while not self.is_at_end():
            char = self.peek_char()
            
            # Check for closing quote
            if char == quote_char:
                self.advance()
                value = ''.join(value_parts)
                length = self.position - start_pos
                return self.make_token(TokenType.STRING, value, start_line, start_column, length)
            
            # Handle escape sequences
            if char == '\\':
                self.advance()
                if self.is_at_end():
                    break
                
                escape_char = self.advance()
                escape_map = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'",
                }
                value_parts.append(escape_map.get(escape_char, escape_char))
            else:
                value_parts.append(self.advance())
        
        # If we reach here, the string was not terminated
        self.add_error(f"unterminated string literal", start_line, start_column)
        length = self.position - start_pos
        return self.make_token(TokenType.INVALID, '', start_line, start_column, length)

    
    def tokenize_operator_or_delimiter(self) -> Optional[Token]:
        """Tokenize operators and delimiters.
        
        Returns:
            A token representing an operator or delimiter, or None if not recognized
        """
        start_line = self.line
        start_column = self.column
        char = self.peek_char()
        
        # Two-character operators
        if char == '=' and self.peek_char(1) == '=':
            self.advance()
            self.advance()
            return self.make_token(TokenType.EQUAL_EQUAL, '==', start_line, start_column, 2)
        
        if char == '!' and self.peek_char(1) == '=':
            self.advance()
            self.advance()
            return self.make_token(TokenType.BANG_EQUAL, '!=', start_line, start_column, 2)
        
        if char == '<' and self.peek_char(1) == '=':
            self.advance()
            self.advance()
            return self.make_token(TokenType.LESS_EQUAL, '<=', start_line, start_column, 2)
        
        if char == '>' and self.peek_char(1) == '=':
            self.advance()
            self.advance()
            return self.make_token(TokenType.GREATER_EQUAL, '>=', start_line, start_column, 2)
        
        if char == '&' and self.peek_char(1) == '&':
            self.advance()
            self.advance()
            return self.make_token(TokenType.AND, '&&', start_line, start_column, 2)
        
        if char == '|' and self.peek_char(1) == '|':
            self.advance()
            self.advance()
            return self.make_token(TokenType.OR, '||', start_line, start_column, 2)
        
        # Single-character tokens
        single_char_tokens = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '%': TokenType.PERCENT,
            '=': TokenType.EQUAL,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '!': TokenType.NOT,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
        }
        
        if char in single_char_tokens:
            self.advance()
            return self.make_token(single_char_tokens[char], char, start_line, start_column, 1)
        
        return None
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code.
        
        Returns:
            A list of tokens, ending with an EOF token
        """
        self.tokens = []
        self.errors = []
        
        while not self.is_at_end():
            # Skip whitespace
            self.skip_whitespace()
            
            if self.is_at_end():
                break
            
            start_line = self.line
            start_column = self.column
            char = self.peek_char()
            
            # Handle comments
            if char == '/' and self.peek_char(1) == '/':
                self.skip_line_comment()
                continue
            
            if char == '/' and self.peek_char(1) == '*':
                self.skip_block_comment()
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                token = self.tokenize_identifier()
                self.tokens.append(token)
                continue
            
            # Numbers
            if char.isdigit():
                token = self.tokenize_number()
                self.tokens.append(token)
                continue
            
            # Strings
            if char in '"\'':
                token = self.tokenize_string()
                self.tokens.append(token)
                continue
            
            # Operators and delimiters
            token = self.tokenize_operator_or_delimiter()
            if token:
                self.tokens.append(token)
                continue
            
            # Invalid character
            self.add_error(f"invalid character '{char}'", start_line, start_column)
            invalid_token = self.make_token(TokenType.INVALID, char, start_line, start_column, 1)
            self.tokens.append(invalid_token)
            self.advance()
        
        # Add EOF token
        eof_token = self.make_token(TokenType.EOF, None, self.line, self.column, 0)
        self.tokens.append(eof_token)
        
        return self.tokens
    
    def has_errors(self) -> bool:
        """Check if any lexical errors were encountered.
        
        Returns:
            True if there are errors, False otherwise
        """
        return len(self.errors) > 0
    
    def get_errors(self) -> List[str]:
        """Get all lexical errors.
        
        Returns:
            A list of error messages
        """
        return self.errors
