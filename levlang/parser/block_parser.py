"""
Generic block parser for LevLang's data-driven syntax.

The grammar is intentionally loose: any identifier followed by `{ ... }` becomes
an entry in the AST. Blocks contain simple `key: value` pairs (one per line) or
quoted text lines. The only reserved block name is `ui`, which captures HUD text
rules.
"""

from __future__ import annotations

import ast

import re
from typing import Any, Dict, List

from levlang.error.error_reporter import ErrorReporter, ErrorType
from levlang.core.source_location import SourceLocation


class BlockParser:
    """Parse generalized block syntax into a simple AST."""

    def __init__(self, source: str, error_reporter: ErrorReporter):
        self.source = source
        self.lines = source.splitlines()
        self.error_reporter = error_reporter
        self.ast: Dict[str, Any] = {
            "blocks": {},
            "globals": {},
            "ui": [],
        }
        self.state_stack: List[Dict[str, Any]] = []

    def parse(self) -> Dict[str, Any]:
        """Parse the source into the block AST."""
        for idx, raw_line in enumerate(self.lines):
            line = self._strip_comment(raw_line).strip()
            if not line:
                continue

            if line == "}":
                if not self.state_stack:
                    self._report_error(idx, "Found '}' without matching '{'.")
                else:
                    current = self.state_stack[-1]
                    if current["type"] == "pygame":
                        self._report_error(idx, "Found '}' but expected ']' to close pygame block.")
                    else:
                        self.state_stack.pop()
                continue

            # Check if we're in a pygame block before treating ] as block end
            if line == "]":
                if not self.state_stack:
                    self._report_error(idx, "Found ']' without matching '['.")
                elif self.state_stack[-1]["type"] != "pygame":
                    self._report_error(idx, "Found ']' but expected '}' to close regular block.")
                else:
                    self.state_stack.pop()
                continue

            if line.endswith("{"):
                self._handle_block_start(idx, line[:-1].strip())
                continue

            if line.endswith("["):
                self._handle_pygame_block_start(idx, line[:-1].strip())
                continue

            # Handle top-level commands like start()
            if not self.state_stack:
                self._handle_top_level_statement(idx, line)
                continue

            current = self.state_stack[-1]
            if current["type"] == "ui":
                self._handle_ui_line(idx, line, current)
            elif current["type"] == "pygame":
                self._handle_pygame_line(idx, raw_line, current)
            else:
                self._handle_property_line(idx, line, current["target"])

        if self.state_stack:
            self._report_error(
                len(self.lines) - 1,
                f"Reached end of file with unclosed blocks: "
                f"{[ctx['name'] for ctx in self.state_stack]}",
            )

        return self.ast

    # --------------------------------------------------------------------- #
    # Block handling
    # --------------------------------------------------------------------- #

    def _handle_block_start(self, line_idx: int, header: str):
        if not header:
            self._report_error(line_idx, "Empty block header.")
            return

        lower_header = header.lower()
        if lower_header == "ui":
            self.ast["ui"].append([])
            self.state_stack.append(
                {"type": "ui", "name": "ui", "target": self.ast["ui"][-1]}
            )
            return

        block_name = header
        target = self.ast["blocks"].setdefault(block_name, {})
        self.state_stack.append(
            {"type": "block", "name": block_name, "target": target}
        )

    def _handle_pygame_block_start(self, line_idx: int, header: str):
        """Handle pygame code blocks with blockname[] syntax."""
        if not header:
            self._report_error(line_idx, "Empty pygame block header.")
            return

        block_name = header
        # Mark this block as a pygame code block with raw code
        target = self.ast["blocks"].setdefault(block_name, {})
        target["_pygame_code"] = []
        self.state_stack.append(
            {"type": "pygame", "name": block_name, "target": target}
        )

    def _handle_pygame_line(self, line_idx: int, raw_line: str, context: Dict[str, Any]):
        """Handle a line of raw pygame code inside a pygame block."""
        # Store the raw line with its original indentation (but strip leading spaces from the block level)
        context["target"]["_pygame_code"].append(raw_line.rstrip())

    def _handle_top_level_statement(self, line_idx: int, line: str):
        if line.lower() == "start()":
            self.ast["globals"]["start"] = True
            return

        # Handle "game <title>" syntax - convert to game block with title property
        game_title_match = re.match(r'^\s*game\s+"([^"]+)"\s*$', line, re.IGNORECASE)
        if game_title_match:
            # Create an implicit game block with the title
            title = game_title_match.group(1)
            if "game" not in self.ast["blocks"]:
                self.ast["blocks"]["game"] = {}
            self.ast["blocks"]["game"]["title"] = title
            return

        if ":" in line:
            key, value = line.split(":", 1)
            parsed = self._parse_value(value.strip())
            self.ast["globals"][key.strip()] = parsed
            return

        # If we reach here, the statement is invalid at top level
        self._report_error(line_idx, f"Invalid top-level statement: '{line}'")

    # --------------------------------------------------------------------- #
    # Property parsing
    # --------------------------------------------------------------------- #

    def _handle_property_line(self, line_idx: int, line: str, target: Dict[str, Any]):
        if line.startswith('"') and line.endswith('"'):
            text = self._parse_string_literal(line)
            target.setdefault("_lines", []).append(text)
            return

        if ":" not in line:
            self._report_error(
                line_idx, f"Expected 'key: value' inside block, got '{line}'."
            )
            return

        pairs = self._split_key_value_pairs(line_idx, line)
        for key, raw_value in pairs:
            value = self._parse_value(raw_value)
            if key in target:
                if isinstance(target[key], list):
                    target[key].append(value)
                else:
                    target[key] = [target[key], value]
            else:
                target[key] = value

    def _handle_ui_line(self, line_idx: int, line: str, context: Dict[str, Any]):
        match = re.match(
            r'"([^"]+)"\s+at\s+(\w+)(?:\s+offset\s+(-?\d+),\s*(-?\d+))?',
            line,
            re.IGNORECASE,
        )
        if match:
            text, anchor, ox, oy = match.groups()
            context["target"].append(
                {
                    "text": text,
                    "anchor": anchor.lower(),
                    "offset": (
                        int(ox) if ox else 0,
                        int(oy) if oy else 0,
                    ),
                }
            )
        else:
            self._report_error(
                line_idx,
                "Invalid UI rule. Expected format "
                '"Text" at position [offset x,y].',
            )

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #

    def _split_key_value_pairs(
        self, line_idx: int, line: str
    ) -> List[tuple[str, str]]:
        """Split a line with potentially multiple key:value pairs."""
        pairs: List[tuple[str, str]] = []
        current_buffer = []
        in_quotes = False
        quote_char = None
        parsing_value = False
        current_key = ""

        i = 0
        while i < len(line):
            ch = line[i]
            
            # Count preceding backslashes for escape detection
            num_backslashes = 0
            j = i - 1
            while j >= 0 and line[j] == '\\':
                num_backslashes += 1
                j -= 1
            
            # Quote toggles only if even number of preceding backslashes
            if ch in ('"', "'") and num_backslashes % 2 == 0:
                if not in_quotes:
                    in_quotes = True
                    quote_char = ch
                elif ch == quote_char:
                    in_quotes = False
                    quote_char = None
            
            # Handle colons
            if ch == ":" and not in_quotes:
                if not parsing_value:
                    # First colon: transition from key to value
                    current_key = "".join(current_buffer).strip()
                    current_buffer = []
                    parsing_value = True
                else:
                    # Second colon: save current pair and start new key
                    value_str = "".join(current_buffer).strip()
                    if current_key:
                        pairs.append((current_key, value_str))
                    current_key = ""
                    current_buffer = []
                    parsing_value = False
            else:
                current_buffer.append(ch)
            
            i += 1

        # Flush final pair
        if parsing_value and current_key:
            value_str = "".join(current_buffer).strip()
            pairs.append((current_key, value_str))

        # Fall back to simple split if parser failed
        if not pairs and ":" in line:
            key, raw = line.split(":", 1)
            pairs.append((key.strip(), raw.strip()))

        return pairs

    def _parse_value(self, raw_value: str) -> Any:
        stripped = raw_value.strip()
        if stripped.lower() in {"true", "false"}:
            return stripped.lower() == "true"

        # Handle array literals like ["a", "b", "c"]
        if stripped.startswith('[') and stripped.endswith(']'):
            try:
                # Use ast.literal_eval for safe parsing of lists
                return ast.literal_eval(stripped)
            except (ValueError, SyntaxError):
                # If parsing fails, treat as string
                pass

        if stripped.startswith('"') and stripped.endswith('"'):
            return self._parse_string_literal(stripped)

        if re.match(r"^-?\d+$", stripped):
            try:
                return int(stripped)
            except ValueError:
                pass

        if re.match(r"^-?\d+\.\d+$", stripped):
            try:
                return float(stripped)
            except ValueError:
                pass

        return stripped

    def _parse_string_literal(self, token: str) -> str:
        """Parse a string literal using ast.literal_eval for safe parsing."""
        try:
            return ast.literal_eval(token)
        except (ValueError, SyntaxError) as e:
            # Only fallback for simple quoted strings with matching quotes
            if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
                return token[1:-1]
            # For truly malformed strings, raise error
            raise SyntaxError(f"Malformed string literal: {token}") from e

    def _strip_comment(self, line: str) -> str:
        """Strip // comments while preserving them inside quoted strings."""
        in_quotes = False
        quote_char = None
        i = 0
        while i < len(line):
            ch = line[i]
            
            # Handle escape sequences
            if i > 0 and line[i - 1] == '\\':
                # Count preceding backslashes
                num_backslashes = 0
                j = i - 1
                while j >= 0 and line[j] == '\\':
                    num_backslashes += 1
                    j -= 1
                # If odd number of backslashes, current char is escaped
                if num_backslashes % 2 == 1:
                    i += 1
                    continue
            
            # Toggle quote state
            if ch in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = ch
                i += 1
                continue
            elif ch == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                i += 1
                continue
            
            # Check for comment start
            if not in_quotes and ch == '/' and i + 1 < len(line) and line[i + 1] == '/':
                return line[:i]
            
            i += 1
        
        return line

    def _report_error(self, line_idx: int, message: str):
        location = SourceLocation(
            filename=self.error_reporter.filename,
            line=line_idx + 1,
            column=1,
            length=len(self.lines[line_idx]) if 0 <= line_idx < len(self.lines) else 0,
        )
        self.error_reporter.report_error(ErrorType.SYNTAX, message, location)

