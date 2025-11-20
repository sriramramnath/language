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


class CLI:
    """Command-line interface for the LevLang transpiler."""
    
    # Transpiler version - update when behavior changes to invalidate cache
    VERSION = "0.3.1"
    
    BANNER = """
 ╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸
 ┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓
 ┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛
-----------------------
    Levelium Inc.
-----------------------

"""
    
    def __init__(self):
        """Initialize the CLI."""
        self.cache_dir = Path.home() / '.levlang' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def print_banner(self):
        """Print the CLI banner."""
        print(self.BANNER)
        print(">> CLI version 0.3.0\n")
    
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
            print(f"Error: File not found: {input_path}", file=sys.stderr)
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
            print(f"log: Successfully transpiled {input_path} -> {output_path}")
            return 0
        except IOError as e:
            print(f"Error writing file {output_path}: {e}", file=sys.stderr)
            return 1

    def run_file(self, input_path: str) -> int:
        """Transpile and execute a LevLang file, handling level chaining."""
        self.print_banner()
        
        current_level_path = input_path
        
        while current_level_path:
            print(f"log: Loading level: {current_level_path}")

            if not Path(current_level_path).exists():
                print(f"Error: File not found: {current_level_path}", file=sys.stderr)
                return 1

            try:
                with open(current_level_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
            except IOError as e:
                print(f"Error reading file {current_level_path}: {e}", file=sys.stderr)
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

        print("log: Game sequence finished.")
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
        """Detect generalized block syntax (name { ... })."""
        # Block syntax should NOT match reserved keywords (dynamically built from lexer)
        # Build negative lookahead pattern from RESERVED_KEYWORDS
        keyword_pattern = '|'.join(rf'{kw}\b' for kw in sorted(RESERVED_KEYWORDS))
        block_pattern = rf'^\s*(?!{keyword_pattern})([A-Za-z_]\w*)\s*\{{'
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
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            return 1
        
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.py'))
        
        print(f"Watching {input_path} for changes...")
        print(f"Output: {output_path}")
        print("Press Ctrl+C to stop.\n")
        
        # Initial transpile
        last_mtime = Path(input_path).stat().st_mtime
        result = self.transpile_file(input_path, output_path, show_banner=False)
        if result == 0:
            print(f"[{time.strftime('%H:%M:%S')}] Transpiled successfully")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Transpilation failed", file=sys.stderr)
        
        # Watch for changes
        try:
            while True:
                time.sleep(0.5)  # Check every 500ms
                
                if not Path(input_path).exists():
                    print(f"Error: File {input_path} no longer exists", file=sys.stderr)
                    return 1
                
                current_mtime = Path(input_path).stat().st_mtime
                if current_mtime != last_mtime:
                    last_mtime = current_mtime
                    print(f"\n[{time.strftime('%H:%M:%S')}] File changed, retranspiling...")
                    result = self.transpile_file(input_path, output_path, show_banner=False)
                    if result == 0:
                        print(f"[{time.strftime('%H:%M:%S')}] Transpiled successfully")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] Transpilation failed", file=sys.stderr)
        except KeyboardInterrupt:
            print("\n\nWatch mode stopped.")
            return 0
