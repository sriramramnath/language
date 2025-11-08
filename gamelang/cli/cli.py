"""CLI class for the game language transpiler."""

import sys
import os
import time
import hashlib
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from gamelang.lexer.lexer import Lexer
from gamelang.parser.parser import Parser
from gamelang.semantic.semantic_analyzer import SemanticAnalyzer
from gamelang.codegen.code_generator import CodeGenerator
from gamelang.error.error_reporter import ErrorReporter, ErrorType


class CLI:
    """Command-line interface for the game language transpiler."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.cache_dir = Path.home() / '.gamelang' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def transpile_file(self, input_path: str, output_path: Optional[str] = None) -> int:
        """Transpile a game language file to Python.
        
        Args:
            input_path: Path to the input .game file
            output_path: Path to the output .py file (optional)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        # Determine output path if not specified
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(input_file.with_suffix('.py'))
        
        # Read source file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            return 1
        except IOError as e:
            print(f"Error reading file {input_path}: {e}", file=sys.stderr)
            return 1
        
        # Run transpilation pipeline
        success, generated_code, errors = self._transpile(source_code, input_path)
        
        # Display errors if compilation failed
        if not success:
            print(errors, file=sys.stderr)
            return 1
        
        # Write generated code to output file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            print(f"Successfully transpiled {input_path} -> {output_path}")
            return 0
        except IOError as e:
            print(f"Error writing file {output_path}: {e}", file=sys.stderr)
            return 1
    
    def watch_mode(self, input_path: str, output_path: Optional[str] = None) -> int:
        """Watch a game language file and automatically retranspile on changes.
        
        Args:
            input_path: Path to the input .game file to watch
            output_path: Path to the output .py file (optional)
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        # Determine output path if not specified
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(input_file.with_suffix('.py'))
        
        # Check if input file exists
        if not os.path.exists(input_path):
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            return 1
        
        print(f"Watching {input_path} for changes...")
        print("Press Ctrl+C to stop")
        
        last_mtime = None
        
        try:
            while True:
                try:
                    # Get file modification time
                    current_mtime = os.path.getmtime(input_path)
                    
                    # Check if file has been modified
                    if last_mtime is None or current_mtime > last_mtime:
                        last_mtime = current_mtime
                        
                        # Read source file
                        try:
                            with open(input_path, 'r', encoding='utf-8') as f:
                                source_code = f.read()
                        except IOError as e:
                            print(f"Error reading file: {e}", file=sys.stderr)
                            time.sleep(1)
                            continue
                        
                        # Run transpilation
                        print(f"\n[{time.strftime('%H:%M:%S')}] Transpiling...")
                        success, generated_code, errors = self._transpile(source_code, input_path)
                        
                        if success:
                            # Write output file
                            try:
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    f.write(generated_code)
                                print(f"[{time.strftime('%H:%M:%S')}] ✓ Successfully transpiled to {output_path}")
                            except IOError as e:
                                print(f"Error writing file: {e}", file=sys.stderr)
                        else:
                            print(f"[{time.strftime('%H:%M:%S')}] ✗ Transpilation failed:")
                            print(errors, file=sys.stderr)
                    
                    # Sleep before checking again
                    time.sleep(0.5)
                    
                except FileNotFoundError:
                    print(f"Warning: File {input_path} not found, waiting...", file=sys.stderr)
                    time.sleep(1)
                    last_mtime = None
                    
        except KeyboardInterrupt:
            print("\nStopped watching")
            return 0
    
    def run_file(self, input_path: str) -> int:
        """Transpile and execute a game language file.
        
        Args:
            input_path: Path to the input .game file
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        # Read source file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            return 1
        except IOError as e:
            print(f"Error reading file {input_path}: {e}", file=sys.stderr)
            return 1
        
        # Run transpilation pipeline
        success, generated_code, errors = self._transpile(source_code, input_path)
        
        # Display errors if compilation failed
        if not success:
            print(errors, file=sys.stderr)
            return 1
        
        # Write generated code to temporary file
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as temp_file:
                temp_file.write(generated_code)
                temp_path = temp_file.name
            
            # Execute the generated Python code
            try:
                result = subprocess.run(
                    [sys.executable, temp_path],
                    check=False
                )
                return result.returncode
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
                    
        except IOError as e:
            print(f"Error creating temporary file: {e}", file=sys.stderr)
            return 1
    
    def get_cache_key(self, source_code: str, filename: str) -> str:
        """Generate a cache key for the source code.
        
        Args:
            source_code: The source code content
            filename: The source filename
            
        Returns:
            A hash string to use as cache key
        """
        content = f"{filename}:{source_code}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get_cached_output(self, cache_key: str) -> Optional[str]:
        """Retrieve cached transpilation output.
        
        Args:
            cache_key: The cache key
            
        Returns:
            The cached output, or None if not found
        """
        cache_file = self.cache_dir / f"{cache_key}.py"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except IOError:
                return None
        return None
    
    def save_to_cache(self, cache_key: str, output: str) -> None:
        """Save transpilation output to cache.
        
        Args:
            cache_key: The cache key
            output: The generated code to cache
        """
        cache_file = self.cache_dir / f"{cache_key}.py"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(output)
        except IOError:
            # Silently fail if we can't write to cache
            pass
    
    def _transpile(self, source_code: str, filename: str) -> tuple[bool, str, str]:
        """Run the transpilation pipeline.
        
        Args:
            source_code: The source code to transpile
            filename: The source filename for error reporting
            
        Returns:
            A tuple of (success, generated_code, error_messages)
        """
        # Check cache
        cache_key = self.get_cache_key(source_code, filename)
        cached_output = self.get_cached_output(cache_key)
        if cached_output is not None:
            return True, cached_output, ""
        
        # Create error reporter
        error_reporter = ErrorReporter(source_code, filename)
        
        # Lexical analysis
        lexer = Lexer(source_code, filename)
        tokens = lexer.tokenize()
        
        if lexer.has_errors():
            for error_msg in lexer.get_errors():
                # Parse error message to extract location info
                # Format: filename:line:column: error: message
                parts = error_msg.split(': ', 3)
                if len(parts) >= 4:
                    location_parts = parts[0].split(':')
                    if len(location_parts) >= 3:
                        try:
                            from gamelang.core.source_location import SourceLocation
                            location = SourceLocation(
                                filename=filename,
                                line=int(location_parts[1]),
                                column=int(location_parts[2]),
                                length=1
                            )
                            error_reporter.report_error(ErrorType.LEXICAL, parts[3], location)
                        except (ValueError, IndexError):
                            pass
            
            return False, "", error_reporter.format_all()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        if parser.has_errors():
            for parse_error in parser.get_errors():
                error_reporter.report_error(
                    ErrorType.SYNTAX,
                    parse_error.message,
                    parse_error.location
                )
            
            return False, "", error_reporter.format_all()
        
        # Semantic analysis
        analyzer = SemanticAnalyzer(ast)
        analyzer.analyze()
        
        if analyzer.has_errors():
            for semantic_error in analyzer.get_errors():
                error_reporter.report_error(
                    semantic_error.error_type,
                    semantic_error.message,
                    semantic_error.location
                )
            
            return False, "", error_reporter.format_all()
        
        # Code generation
        generator = CodeGenerator(ast)
        generated_code = generator.generate()
        
        # Save to cache
        self.save_to_cache(cache_key, generated_code)
        
        return True, generated_code, ""
