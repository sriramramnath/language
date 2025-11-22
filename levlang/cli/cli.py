"""CLI class for the LevLang v3 transpiler."""

import sys
import os
import time
import hashlib
import subprocess
import tempfile
import re
from pathlib import Path
from typing import Optional

from levlang.parser.simple_parser import SimpleParser
from levlang.parser.block_parser import BlockParser
from levlang.codegen.simple_generator import SimpleCodeGenerator
from levlang.codegen.block_generator import BlockCodeGenerator
from levlang.error.error_reporter import ErrorReporter, ErrorType
from levlang.lexer import Lexer
from levlang.parser import Parser
from levlang.semantic import SemanticAnalyzer
from levlang.codegen import CodeGenerator

# Import reserved keywords for parser detection
RESERVED_KEYWORDS = set(Lexer.KEYWORDS.keys()) | {'component', 'entities'}

# ANSI Color Codes for modern CLI
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_CYAN = '\033[46m'
    BG_MAGENTA = '\033[45m'
    
    @staticmethod
    def gradient_text(text: str) -> str:
        """Create a gradient effect on text."""
        colors = [Colors.BRIGHT_CYAN, Colors.CYAN, Colors.BRIGHT_BLUE, Colors.BLUE]
        result = []
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result.append(f"{color}{char}")
        return ''.join(result) + Colors.RESET
    
    @staticmethod
    def rainbow_text(text: str) -> str:
        """Create a rainbow effect on text."""
        colors = [Colors.BRIGHT_RED, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN, 
                  Colors.BRIGHT_CYAN, Colors.BRIGHT_BLUE, Colors.BRIGHT_MAGENTA]
        result = []
        for i, char in enumerate(text):
            if char != ' ':
                color = colors[i % len(colors)]
                result.append(f"{color}{char}")
            else:
                result.append(char)
        return ''.join(result) + Colors.RESET


class CLI:
    """Command-line interface for the LevLang transpiler."""
    
    # Transpiler version - update when behavior changes to invalidate cache
    VERSION = "0.3.1"
    
    def __init__(self):
        """Initialize the CLI."""
        self.cache_dir = Path.home() / '.levlang' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_color = sys.stdout.isatty()  # Only use colors in terminal
    
    def print_banner(self):
        """Print the CLI banner with colors."""
        if not self.use_color:
            print(" ╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸")
            print(" ┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓")
            print(" ┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛")
            print("-----------------------")
            print("    Levelium Inc.")
            print("-----------------------")
            print(f">> v{self.VERSION} | Pygame Integration\n")
            return
        
        c = Colors
        print()
        print(f"{c.BRIGHT_CYAN} ╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸{c.RESET}")
        print(f"{c.BRIGHT_CYAN} ┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓{c.RESET}")
        print(f"{c.BRIGHT_CYAN} ┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛{c.RESET}")
        print(f"{c.DIM}-----------------------{c.RESET}")
        print(f"{c.BRIGHT_WHITE}    Levelium Inc.{c.RESET}")
        print(f"{c.DIM}-----------------------{c.RESET}")
        print(f"{c.BRIGHT_GREEN}>> v{self.VERSION}{c.RESET} {c.DIM}| Block Syntax • Pygame Code Injection{c.RESET}\n")
    
    def log_success(self, message: str):
        """Print a success message with styling."""
        if self.use_color:
            print(f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} {Colors.BRIGHT_WHITE}{message}{Colors.RESET}")
        else:
            print(f"✓ {message}")
    
    def log_info(self, message: str):
        """Print an info message with styling."""
        if self.use_color:
            print(f"{Colors.BRIGHT_CYAN}•{Colors.RESET} {Colors.WHITE}{message}{Colors.RESET}")
        else:
            print(f"• {message}")
    
    def log_error(self, message: str):
        """Print an error message with styling."""
        if self.use_color:
            print(f"{Colors.BRIGHT_RED}✗{Colors.RESET} {Colors.RED}{message}{Colors.RESET}", file=sys.stderr)
        else:
            print(f"✗ {message}", file=sys.stderr)
    
    def log_warning(self, message: str):
        """Print a warning message with styling."""
        if self.use_color:
            print(f"{Colors.BRIGHT_YELLOW}⚠{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}")
        else:
            print(f"⚠ {message}")
    
    def transpile_file(self, input_path: str, output_path: Optional[str] = None, show_banner: bool = True) -> int:
        """Transpile a LevLang file to Python."""
        if show_banner:
            self.print_banner()
        
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.py'))
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except FileNotFoundError:
            self.log_error(f"File not found: {input_path}")
            return 1
        
        success, generated_code, errors = self._generate_code(
            source_code, input_path, use_cache=True
        )
        
        if not success:
            print(errors, file=sys.stderr)
            return 1
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            self.log_success(f"Transpiled {input_path} → {output_path}")
            return 0
        except IOError as e:
            self.log_error(f"Failed to write file {output_path}: {e}")
            return 1

    def run_file(self, input_path: str) -> int:
        """Transpile and execute a LevLang file, handling level chaining."""
        self.print_banner()
        
        current_level_path = input_path
        
        while current_level_path:
            self.log_info(f"Loading level: {current_level_path}")

            if not Path(current_level_path).exists():
                self.log_error(f"File not found: {current_level_path}")
                return 1

            try:
                with open(current_level_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
            except IOError as e:
                self.log_error(f"Failed to read file {current_level_path}: {e}")
                return 1
            
            success, generated_code, errors = self._generate_code(
                source_code, current_level_path, use_cache=True
            )
            
            if not success:
                print(errors, file=sys.stderr)
                return 1
            
            next_level_path = None
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
                    temp_file.write(generated_code)
                    temp_path = temp_file.name
                
                process = subprocess.Popen(
                    [sys.executable, temp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )

                if process.stdout:
                    for line in iter(process.stdout.readline, ''):
                        line = line.strip()
                        if line.startswith('__NEXT_LEVEL__'):
                            parts = line.split(':', 1)
                            if len(parts) == 2 and parts[1].strip():
                                next_level_path = parts[1].strip()
                                print(f"log: Transitioning to next level: {next_level_path}")
                                process.terminate()
                                break
                            else:
                                print(f"warning: Malformed level transition marker: {line}", file=sys.stderr)
                        elif line:
                            print(line)

                try:
                    stdout, stderr = process.communicate(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                if stderr and "pygame.error: display Surface quit" not in stderr:
                    print(stderr, file=sys.stderr)

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

            current_level_path = next_level_path

        self.log_success("Game sequence finished!")
        return 0

    def _generate_code(
        self, source_code: str, filename: str, use_cache: bool = True
    ) -> tuple[bool, str, str]:
        # Determine pipeline for cache key
        if self._is_component_syntax(source_code):
            pipeline = "component"
        elif self._is_block_syntax(source_code):
            pipeline = "blocks"
        else:
            pipeline = "advanced"
        
        cache_key = None
        if use_cache:
            cache_key = self.get_cache_key(source_code, filename, pipeline)
            cached = self.get_cached_output(cache_key)
            if cached is not None:
                return True, cached, ""

        success, generated_code, errors = self._transpile(source_code, filename)

        if success and use_cache and cache_key:
            self.save_to_cache(cache_key, generated_code)

        return success, generated_code, errors

    def _transpile(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        """Route source code through the appropriate transpilation pipeline."""
        if self._is_component_syntax(source_code):
            return self._transpile_component(source_code, filename)
        if self._is_block_syntax(source_code):
            return self._transpile_blocks(source_code, filename)
        return self._transpile_advanced(source_code, filename)

    def _is_component_syntax(self, source_code: str) -> bool:
        """Heuristically detect the component (SimpleParser) syntax."""
        patterns = (
            r'^\s*component\s+"',
            r'^\s*entities\s*\{',
        )
        return any(re.search(pattern, source_code, re.MULTILINE) for pattern in patterns)

    def _is_block_syntax(self, source_code: str) -> bool:
        """Detect generalized block syntax (name { ... } or name [ ... ])."""
        # Block syntax should NOT match reserved keywords (dynamically built from lexer)
        # Build negative lookahead pattern from RESERVED_KEYWORDS
        keyword_pattern = '|'.join(rf'{kw}\b' for kw in sorted(RESERVED_KEYWORDS))
        # Match both { and [ for block starts
        block_pattern = rf'^\s*(?!{keyword_pattern})([A-Za-z_]\w*)\s*[\{{\[]'
        return re.search(block_pattern, source_code, re.MULTILINE) is not None

    def _transpile_component(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        error_reporter = ErrorReporter(source_code, filename)
        parser = SimpleParser(source_code, error_reporter)
        ast = parser.parse()

        if error_reporter.has_errors():
            return False, "", error_reporter.format_all()

        generator = SimpleCodeGenerator(ast)
        return True, generator.generate(), ""

    def _transpile_blocks(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        error_reporter = ErrorReporter(source_code, filename)
        parser = BlockParser(source_code, error_reporter)
        ast = parser.parse()

        if error_reporter.has_errors():
            return False, "", error_reporter.format_all()

        generator = BlockCodeGenerator(ast)
        return True, generator.generate(), ""

    def _transpile_advanced(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        lexer = Lexer(source_code, filename)
        tokens = lexer.tokenize()
        if lexer.errors:
            return False, "", "\n".join(lexer.errors)

        parser = Parser(tokens)
        ast = parser.parse()
        if parser.has_errors():
            return False, "", parser.format_all_errors(source_code.splitlines())

        analyzer = SemanticAnalyzer(ast)
        if not analyzer.analyze():
            messages = "\n".join(str(err) for err in analyzer.get_errors())
            return False, "", messages

        generator = CodeGenerator(ast)
        return True, generator.generate(), ""

    def get_cache_key(self, source_code: str, filename: str, pipeline: str = "") -> str:
        """Generate a deterministic cache key for a source file.
        
        Args:
            source_code: The source code content
            filename: The source file name
            pipeline: The transpiler pipeline identifier (component/blocks/advanced)
            
        Returns:
            A hex digest cache key
        """
        hasher = hashlib.sha256()
        # Include version to invalidate cache when transpiler changes
        hasher.update(self.VERSION.encode("utf-8"))
        hasher.update(b"\0")
        # Include pipeline to invalidate cache when routing changes
        hasher.update(pipeline.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(filename.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(source_code.encode("utf-8"))
        return hasher.hexdigest()

    def get_cached_output(self, cache_key: str) -> Optional[str]:
        """Return cached Python code for the given cache key, if available."""
        cache_path = self.cache_dir / cache_key
        if not cache_path.exists():
            return None
        try:
            return cache_path.read_text(encoding="utf-8")
        except IOError:
            return None

    def save_to_cache(self, cache_key: str, generated_code: str) -> None:
        """Persist generated Python code in the cache directory."""
        cache_path = self.cache_dir / cache_key
        try:
            cache_path.write_text(generated_code, encoding="utf-8")
        except IOError:
            # Cache failures should not stop the transpilation flow.
            pass

    def watch_mode(self, input_path: str, output_path: Optional[str] = None) -> int:
        """Watch a LevLang file and automatically retranspile on changes."""
        self.print_banner()
        
        if not Path(input_path).exists():
            self.log_error(f"File not found: {input_path}")
            return 1
        
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.py'))
        
        if self.use_color:
            print(f"{Colors.BRIGHT_YELLOW}👁{Colors.RESET}  {Colors.BOLD}Watching:{Colors.RESET} {Colors.CYAN}{input_path}{Colors.RESET}")
            print(f"{Colors.BRIGHT_YELLOW}📄{Colors.RESET}  {Colors.BOLD}Output:{Colors.RESET}   {Colors.CYAN}{output_path}{Colors.RESET}")
            print(f"{Colors.DIM}Press Ctrl+C to stop{Colors.RESET}\n")
        else:
            print(f"👁  Watching: {input_path}")
            print(f"📄  Output:   {output_path}")
            print("Press Ctrl+C to stop\n")
        
        # Initial transpile
        last_mtime = Path(input_path).stat().st_mtime
        result = self.transpile_file(input_path, output_path, show_banner=False)
        timestamp = time.strftime('%H:%M:%S')
        if result == 0:
            if self.use_color:
                print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.BRIGHT_GREEN}✓{Colors.RESET} Ready")
            else:
                print(f"[{timestamp}] ✓ Ready")
        
        # Watch for changes
        try:
            while True:
                time.sleep(0.5)  # Check every 500ms
                
                if not Path(input_path).exists():
                    self.log_error(f"File {input_path} no longer exists")
                    return 1
                
                current_mtime = Path(input_path).stat().st_mtime
                if current_mtime != last_mtime:
                    last_mtime = current_mtime
                    timestamp = time.strftime('%H:%M:%S')
                    if self.use_color:
                        print(f"\n{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.BRIGHT_YELLOW}↻{Colors.RESET} File changed, retranspiling...")
                    else:
                        print(f"\n[{timestamp}] ↻ File changed, retranspiling...")
                    
                    result = self.transpile_file(input_path, output_path, show_banner=False)
                    timestamp = time.strftime('%H:%M:%S')
                    if result == 0:
                        if self.use_color:
                            print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.BRIGHT_GREEN}✓{Colors.RESET} Done")
                        else:
                            print(f"[{timestamp}] ✓ Done")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW if self.use_color else ''}Watch mode stopped.{Colors.RESET if self.use_color else ''}")
            return 0
