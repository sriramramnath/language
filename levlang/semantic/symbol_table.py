"""Symbol table for scope management in semantic analysis."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

from levlang.core.source_location import SourceLocation


class SymbolKind(Enum):
    """Types of symbols that can be declared."""
    GAME = "game"
    SPRITE = "sprite"
    SCENE = "scene"
    VARIABLE = "variable"
    PARAMETER = "parameter"
    METHOD = "method"


@dataclass
class Symbol:
    """Represents a declared symbol in the program."""
    name: str
    kind: SymbolKind
    location: SourceLocation
    type_info: Optional[str] = None  # For type checking
    scope_level: int = 0


class Scope:
    """Represents a lexical scope in the program."""
    
    def __init__(self, parent: Optional['Scope'] = None, level: int = 0):
        """Initialize a new scope.
        
        Args:
            parent: The parent scope (None for global scope)
            level: The nesting level of this scope
        """
        self.parent = parent
        self.level = level
        self.symbols: Dict[str, Symbol] = {}
    
    def declare(self, symbol: Symbol) -> bool:
        """Declare a symbol in this scope.
        
        Args:
            symbol: The symbol to declare
            
        Returns:
            True if declaration succeeded, False if symbol already exists
        """
        if symbol.name in self.symbols:
            return False
        
        symbol.scope_level = self.level
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope only.
        
        Args:
            name: The symbol name to look up
            
        Returns:
            The symbol if found, None otherwise
        """
        return self.symbols.get(name)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope and parent scopes.
        
        Args:
            name: The symbol name to look up
            
        Returns:
            The symbol if found, None otherwise
        """
        symbol = self.lookup_local(name)
        if symbol is not None:
            return symbol
        
        if self.parent is not None:
            return self.parent.lookup(name)
        
        return None
    
    def has_symbol(self, name: str) -> bool:
        """Check if a symbol exists in this scope or parent scopes.
        
        Args:
            name: The symbol name to check
            
        Returns:
            True if symbol exists, False otherwise
        """
        return self.lookup(name) is not None


class SymbolTable:
    """Manages symbol tables and scopes for semantic analysis."""
    
    def __init__(self):
        """Initialize the symbol table with a global scope."""
        self.global_scope = Scope(parent=None, level=0)
        self.current_scope = self.global_scope
        self.scope_stack: List[Scope] = [self.global_scope]
    
    def enter_scope(self):
        """Enter a new nested scope."""
        new_level = self.current_scope.level + 1
        new_scope = Scope(parent=self.current_scope, level=new_level)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """Exit the current scope and return to parent scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
    
    def declare(self, name: str, kind: SymbolKind, location: SourceLocation, 
                type_info: Optional[str] = None) -> bool:
        """Declare a symbol in the current scope.
        
        Args:
            name: The symbol name
            kind: The kind of symbol
            location: The source location of the declaration
            type_info: Optional type information
            
        Returns:
            True if declaration succeeded, False if symbol already exists
        """
        symbol = Symbol(
            name=name,
            kind=kind,
            location=location,
            type_info=type_info,
            scope_level=self.current_scope.level
        )
        return self.current_scope.declare(symbol)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol starting from the current scope.
        
        Args:
            name: The symbol name to look up
            
        Returns:
            The symbol if found, None otherwise
        """
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current scope only.
        
        Args:
            name: The symbol name to look up
            
        Returns:
            The symbol if found in current scope, None otherwise
        """
        return self.current_scope.lookup_local(name)
    
    def has_symbol(self, name: str) -> bool:
        """Check if a symbol exists in any accessible scope.
        
        Args:
            name: The symbol name to check
            
        Returns:
            True if symbol exists, False otherwise
        """
        return self.current_scope.has_symbol(name)
    
    def get_all_symbols_of_kind(self, kind: SymbolKind) -> List[Symbol]:
        """Get all symbols of a specific kind from all scopes.
        
        Args:
            kind: The kind of symbols to retrieve
            
        Returns:
            A list of symbols matching the kind
        """
        symbols = []
        for scope in self.scope_stack:
            for symbol in scope.symbols.values():
                if symbol.kind == kind:
                    symbols.append(symbol)
        return symbols
