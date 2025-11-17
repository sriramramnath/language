"""
Parser for LevLang v3 - A component-based language.
Corrected implementation with proper state management for nested blocks.
"""
import re
from typing import Dict, Any

from levlang.core.source_location import SourceLocation
from levlang.error.error_reporter import ErrorReporter, ErrorType

class SimpleParser:
    def __init__(self, source: str, error_reporter: ErrorReporter):
        self.source = source
        self.lines = source.split('\n')
        self.error_reporter = error_reporter
        self.line_num = 0
        self.ast = {
            'components': {},
            'entities': {},
            'game': {}
        }
    
    def parse(self) -> Dict[str, Any]:
        """Parse the source code into a component-based AST."""
        # States: None (top-level), 'component', 'entities', 'entity_override', 'game', 'game_ui'
        state_stack = []
        
        for i, line_content in enumerate(self.lines):
            self.line_num = i + 1
            line = re.sub(r'//.*$', '', line_content).strip()
            if not line:
                continue

            current_state = state_stack[-1] if state_stack else None

            if line == '}':
                if not state_stack:
                    self._report_error("Found '}' without a matching opening block.")
                else:
                    state_stack.pop()
                continue

            if not current_state: # We are at the top level
                comp_match = re.match(r'component\s+"([^"]+)"\s*\{', line)
                if comp_match:
                    comp_name = comp_match.group(1)
                    state_stack.append(('component', comp_name))
                    self.ast['components'][comp_name] = {}
                elif line == 'entities {':
                    state_stack.append('entities')
                elif line == 'game {':
                    state_stack.append('game')
                else:
                    self._report_error(f"Invalid top-level statement: '{line}'")
                continue

            elif current_state == 'game':
                if line == 'ui {':
                    state_stack.append('game_ui')
                    self.ast['game']['ui'] = []
                else:
                    self._parse_property_line(line, self.ast['game'])
            
            elif current_state == 'game_ui':
                 self.ast['game']['ui'].append(line)

            elif current_state[0] == 'component':
                comp_name = current_state[1]
                self._parse_property_line(line, self.ast['components'][comp_name])

            elif current_state == 'entities':
                entity_match = re.match(r'(\w+)\s*:\s*"([^"]+)"\s*\{', line)
                if entity_match:
                    instance_name = entity_match.group(1)
                    comp_name = entity_match.group(2)
                    state_stack.append(('entity_override', instance_name))
                    self.ast['entities'][instance_name] = {
                        'component': comp_name,
                        'overrides': {}
                    }
                else:
                    self._report_error(f"Invalid entity definition. Expected 'name: \"component\" {{'.")
            
            elif current_state[0] == 'entity_override':
                instance_name = current_state[1]
                self._parse_property_line(line, self.ast['entities'][instance_name]['overrides'])

        if state_stack:
            self._report_error(f"Reached end of file with unclosed blocks: {state_stack}")

        return self.ast

    def _parse_property_line(self, line: str, target_dict: Dict):
        if ':' in line:
            key, value = line.split(':', 1)
            target_dict[key.strip()] = self._parse_value(value.strip())
        else:
            self._report_error(f"Invalid property format. Expected 'key: value', but got '{line}'.")

    def _parse_value(self, value: str) -> Any:
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        try:
            if '.' in value: return float(value)
            return int(value)
        except ValueError:
            return value

    def _report_error(self, message: str):
        location = SourceLocation(
            filename=self.error_reporter.filename,
            line=self.line_num,
            column=1,
            length=len(self.lines[self.line_num - 1]) if self.line_num > 0 else 0
        )
        self.error_reporter.report_error(ErrorType.SYNTAX, message, location)
