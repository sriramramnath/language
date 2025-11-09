"""Natural language parser for ultra-simple LevLang syntax."""

import re
from typing import Dict, List, Any, Optional


class NaturalParser:
    """Parser for natural language LevLang syntax."""
    
    def __init__(self, source: str):
        self.source = source
        self.lines = source.split('\n')
        self.ast = {
            'game': {},
            'player': {},
            'enemies': {},
            'coins': {},
            'powerups': {},
            'events': [],
            'ui': [],
            'audio': [],
            'levels': []
        }
    
    def parse(self) -> Dict[str, Any]:
        """Parse natural language commands."""
        for line in self.lines:
            # Remove comments
            line = re.sub(r'//.*$', '', line).strip()
            if not line:
                continue
            
            # Parse different command types
            self._parse_line(line)
        
        return self.ast
    
    def _parse_line(self, line: str):
        """Parse a single line."""
        line_lower = line.lower()
        
        # Game setup
        if line_lower.startswith('game '):
            self._parse_game(line)
        
        # Player commands
        elif line_lower.startswith('player '):
            self._parse_player(line)
        
        # Enemy commands
        elif line_lower.startswith('enemies '):
            self._parse_enemies(line)
        
        # Collectibles
        elif line_lower.startswith('coins '):
            self._parse_coins(line)
        elif line_lower.startswith('powerups '):
            self._parse_powerups(line)
        
        # Events
        elif line_lower.startswith('when '):
            self._parse_event(line)
        elif line_lower.startswith('if '):
            self._parse_event(line)
        
        # UI
        elif line_lower.startswith('show '):
            self._parse_ui(line)
        
        # Audio
        elif line_lower.startswith('play '):
            self._parse_audio(line)
        
        # Levels
        elif line_lower.startswith('level '):
            self._parse_level(line)
    
    def _parse_game(self, line: str):
        """Parse game declaration."""
        # game "Title" 800x600 black
        match = re.match(r'game\s+"([^"]+)"(?:\s+(.*))?', line, re.IGNORECASE)
        if match:
            self.ast['game']['title'] = match.group(1)
            rest = match.group(2) if match.group(2) else ''
            
            # Parse size
            size_match = re.search(r'(\d+)x(\d+)', rest)
            if size_match:
                self.ast['game']['width'] = int(size_match.group(1))
                self.ast['game']['height'] = int(size_match.group(2))
            
            # Parse fullscreen
            if 'fullscreen' in rest.lower():
                self.ast['game']['fullscreen'] = True
            
            # Parse background color
            colors = ['black', 'white', 'red', 'blue', 'green', 'gray']
            for color in colors:
                if color in rest.lower():
                    self.ast['game']['background'] = color
    
    def _parse_player(self, line: str):
        """Parse player commands."""
        line_lower = line.lower()
        
        # Movement
        if 'moves with' in line_lower:
            if 'arrows and wasd' in line_lower or 'wasd and arrows' in line_lower:
                self.ast['player']['movement'] = 'wasd_arrows'
            elif 'arrows' in line_lower:
                self.ast['player']['movement'] = 'arrows'
            elif 'wasd' in line_lower:
                self.ast['player']['movement'] = 'wasd'
            elif 'mouse' in line_lower:
                self.ast['player']['movement'] = 'mouse'
        
        # Actions
        if 'shoots with' in line_lower:
            if 'space' in line_lower:
                self.ast['player']['shoot'] = 'space'
        
        if 'jumps with' in line_lower:
            if 'space' in line_lower:
                self.ast['player']['jump'] = 'space'
        
        # Speed
        speed_match = re.search(r'speed\s+(\d+)', line_lower)
        if speed_match:
            self.ast['player']['speed'] = int(speed_match.group(1))
        
        # Position
        pos_match = re.search(r'at\s+(\d+),(\d+)', line_lower)
        if pos_match:
            self.ast['player']['x'] = int(pos_match.group(1))
            self.ast['player']['y'] = int(pos_match.group(2))
        
        # Sprite
        sprite_match = re.search(r'sprite\s+"([^"]+)"', line)
        if sprite_match:
            self.ast['player']['sprite'] = sprite_match.group(1)
        
        # Size
        size_match = re.search(r'size\s+(\d+)x(\d+)', line_lower)
        if size_match:
            self.ast['player']['width'] = int(size_match.group(1))
            self.ast['player']['height'] = int(size_match.group(2))
        
        # Physics
        if 'has gravity' in line_lower or 'gravity' in line_lower:
            self.ast['player']['gravity'] = True
    
    def _parse_enemies(self, line: str):
        """Parse enemy commands."""
        line_lower = line.lower()
        
        # Spawning
        if 'spawn every' in line_lower:
            time_match = re.search(r'every\s+(\d+)sec', line_lower)
            if time_match:
                self.ast['enemies']['spawn_rate'] = int(time_match.group(1))
        
        if 'spawn at' in line_lower:
            if 'top' in line_lower:
                self.ast['enemies']['spawn_location'] = 'top'
            elif 'random' in line_lower:
                self.ast['enemies']['spawn_location'] = 'random'
        
        # Movement
        if 'move down' in line_lower:
            self.ast['enemies']['movement'] = 'down'
        elif 'move towards player' in line_lower:
            self.ast['enemies']['movement'] = 'towards_player'
        elif 'move randomly' in line_lower:
            self.ast['enemies']['movement'] = 'random'
        
        # Speed
        speed_match = re.search(r'speed\s+(\d+)', line_lower)
        if speed_match:
            self.ast['enemies']['speed'] = int(speed_match.group(1))
        
        # Sprite
        sprite_match = re.search(r'sprite\s+"([^"]+)"', line)
        if sprite_match:
            self.ast['enemies']['sprite'] = sprite_match.group(1)
        
        # Health
        health_match = re.search(r'health\s+(\d+)', line_lower)
        if health_match:
            self.ast['enemies']['health'] = int(health_match.group(1))
    
    def _parse_coins(self, line: str):
        """Parse coin commands."""
        line_lower = line.lower()
        
        if 'spawn every' in line_lower:
            time_match = re.search(r'every\s+(\d+)sec', line_lower)
            if time_match:
                self.ast['coins']['spawn_rate'] = int(time_match.group(1))
        
        if 'worth' in line_lower:
            worth_match = re.search(r'worth\s+(\d+)', line_lower)
            if worth_match:
                self.ast['coins']['value'] = int(worth_match.group(1))
        
        sprite_match = re.search(r'sprite\s+"([^"]+)"', line)
        if sprite_match:
            self.ast['coins']['sprite'] = sprite_match.group(1)
    
    def _parse_powerups(self, line: str):
        """Parse powerup commands."""
        line_lower = line.lower()
        
        if 'spawn every' in line_lower:
            time_match = re.search(r'every\s+(\d+)sec', line_lower)
            if time_match:
                self.ast['powerups']['spawn_rate'] = int(time_match.group(1))
        
        if 'give' in line_lower:
            if 'speed' in line_lower:
                self.ast['powerups']['type'] = 'speed'
            elif 'shield' in line_lower:
                self.ast['powerups']['type'] = 'shield'
            elif 'weapon' in line_lower:
                self.ast['powerups']['type'] = 'weapon'
    
    def _parse_event(self, line: str):
        """Parse event/condition."""
        self.ast['events'].append({
            'condition': line,
            'raw': line
        })
    
    def _parse_ui(self, line: str):
        """Parse UI commands."""
        # show score at top left
        match = re.match(r'show\s+(\w+)\s+at\s+(.*)', line, re.IGNORECASE)
        if match:
            element = match.group(1)
            position = match.group(2).strip()
            self.ast['ui'].append({
                'element': element,
                'position': position
            })
    
    def _parse_audio(self, line: str):
        """Parse audio commands."""
        # play sound "file.wav" when shoot
        # play music "file.mp3" loop
        self.ast['audio'].append({
            'command': line
        })
    
    def _parse_level(self, line: str):
        """Parse level commands."""
        self.ast['levels'].append({
            'command': line
        })
