"""Simple parser for block-based LevLang syntax."""

import re
from typing import Dict, List, Any, Optional


class SimpleParser:
    """Parser for the simplified block-based LevLang syntax."""
    
    def __init__(self, source: str):
        self.source = source
        self.lines = source.split('\n')
        self.ast = {
            'game': {},
            'player': {},
            'road': {},
            'enemy': {},
            'ui': [],
            'gameover': [],
            'spawn_rate': None,
            'start': False
        }
    
    def parse(self) -> Dict[str, Any]:
        """Parse the source code into an AST."""
        current_block = None
        block_content = []
        
        for line in self.lines:
            # Remove comments
            line = re.sub(r'//.*$', '', line).strip()
            if not line:
                continue
            
            # Check for block start
            if line.startswith('game '):
                current_block = 'game'
                # Parse game declaration
                match = re.match(r'game\s+"([^"]+)"(.*)$', line)
                if match:
                    self.ast['game']['title'] = match.group(1)
                    props = match.group(2).strip().split()
                    self.ast['game']['resizable'] = 'resizable' in props
                    self.ast['game']['auto_fps'] = 'auto_fps' in props
                    # Check for icon property
                    for prop in props:
                        if prop.startswith('icon:'):
                            self.ast['game']['icon'] = prop.split(':', 1)[1]
                continue
            
            elif line.startswith('player {'):
                current_block = 'player'
                continue
            
            elif line.startswith('road {'):
                current_block = 'road'
                continue
            
            elif line.startswith('enemy {'):
                current_block = 'enemy'
                continue
            
            elif line.startswith('ui {'):
                current_block = 'ui'
                continue
            
            elif line.startswith('gameover {'):
                current_block = 'gameover'
                continue
            
            elif line == '}':
                current_block = None
                continue
            
            elif line.startswith('spawn_rate:'):
                self.ast['spawn_rate'] = self._parse_value(line.split(':', 1)[1].strip())
                continue
            
            elif line == 'start()':
                self.ast['start'] = True
                continue
            
            # Parse block content
            if current_block:
                if current_block in ['ui', 'gameover']:
                    # Parse string lines
                    match = re.match(r'"([^"]+)"(?:\s+at\s+(\w+))?', line)
                    if match:
                        text = match.group(1)
                        position = match.group(2) if match.group(2) else 'center'
                        self.ast[current_block].append({'text': text, 'position': position})
                else:
                    # Parse property: value
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        self.ast[current_block][key] = self._parse_value(value)
        
        return self.ast
    
    def _parse_value(self, value: str) -> Any:
        """Parse a value string into appropriate Python type."""
        value = value.strip()
        
        # String
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        
        # Boolean
        if value == 'true':
            return True
        if value == 'false':
            return False
        
        # Number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Time value (e.g., "2sec")
        if value.endswith('sec'):
            return int(value[:-3])
        
        # Function call (e.g., "rand(3, 6)")
        if '(' in value:
            return value
        
        # Comma-separated list
        if ',' in value:
            return [self._parse_value(v.strip()) for v in value.split(',')]
        
        # Identifier
        return value
