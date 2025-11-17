"""CLI class for the LevLang v3 transpiler."""

import sys
import os
import time
import hashlib
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from levlang.parser.simple_parser import SimpleParser
from levlang.codegen.simple_generator import SimpleCodeGenerator
from levlang.error.error_reporter import ErrorReporter, ErrorType


class CLI:
    """Command-line interface for the LevLang transpiler."""
    
    BANNER = """
╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸
┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓
┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛ v3.0
-----------------------
  Component Architecture
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
        
        success, generated_code, errors = self._transpile(source_code, input_path)
        
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
            
            success, generated_code, errors = self._transpile(source_code, current_level_path)
            
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

                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    if line.startswith('__NEXT_LEVEL__'):
                        next_level_path = line.split(':', 1)[1]
                        print(f"log: Transitioning to next level: {next_level_path}")
                        process.terminate()
                        break
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

    def _transpile(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        """Run the new component-based transpilation pipeline."""
        error_reporter = ErrorReporter(source_code, filename)
        
        parser = SimpleParser(source_code, error_reporter)
        ast = parser.parse()
        
        if error_reporter.has_errors():
            return False, "", error_reporter.format_all()
        
        generator = SimpleCodeGenerator(ast)
        generated_code = generator.generate()
        
        return True, generated_code, ""
