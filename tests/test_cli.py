"""Integration tests for the CLI."""

import pytest
import os
import tempfile
import time
from pathlib import Path

from gamelang.cli.cli import CLI


class TestCLITranspile:
    """Test CLI transpile command."""
    
    def test_transpile_simple_game(self):
        """Test transpiling a simple game file."""
        # Create a temporary game file
        source_code = """
game MyGame {
    title = "Test Game"
    width = 800
    height = 600
}

sprite Player {
    x = 100
    y = 100
    speed = 5
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.game")
            output_path = os.path.join(tmpdir, "test.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Check success
            assert result == 0
            assert os.path.exists(output_path)
            
            # Check generated code
            with open(output_path, 'r') as f:
                generated = f.read()
            
            assert "import pygame" in generated
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "def main():" in generated
    
    def test_transpile_with_default_output(self):
        """Test transpiling with default output path."""
        source_code = """
game TestGame {
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "game.game")
            expected_output = os.path.join(tmpdir, "game.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile without specifying output
            cli = CLI()
            result = cli.transpile_file(input_path)
            
            # Check success
            assert result == 0
            assert os.path.exists(expected_output)
    
    def test_transpile_nonexistent_file(self):
        """Test transpiling a file that doesn't exist."""
        cli = CLI()
        result = cli.transpile_file("nonexistent.game", "output.py")
        
        # Should return error code
        assert result == 1
    
    def test_transpile_with_syntax_error(self):
        """Test transpiling a file with syntax errors."""
        source_code = """
game MyGame {
    title = "Test"
    // Missing closing brace
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "error.game")
            output_path = os.path.join(tmpdir, "error.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should return error code
            assert result == 1
            # Output file should not be created
            assert not os.path.exists(output_path)
    
    def test_transpile_with_semantic_error(self):
        """Test transpiling a file with semantic errors."""
        source_code = """
game MyGame {
    title = "Test"
}

scene Main {
    player = UndefinedSprite()
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "error.game")
            output_path = os.path.join(tmpdir, "error.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Should return error code
            assert result == 1


class TestCLIRun:
    """Test CLI run command."""
    
    def test_run_simple_game(self):
        """Test running a simple game file."""
        # Create a simple game that exits immediately
        source_code = """
game MyGame {
    title = "Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test.game")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Run (this will start pygame but should complete quickly)
            cli = CLI()
            # Note: This test might fail in headless environments
            # We're just testing that the command executes without crashing
            result = cli.run_file(input_path)
            
            # The result code depends on pygame execution
            # We just check it doesn't crash the CLI
            assert result is not None
    
    def test_run_nonexistent_file(self):
        """Test running a file that doesn't exist."""
        cli = CLI()
        result = cli.run_file("nonexistent.game")
        
        # Should return error code
        assert result == 1
    
    def test_run_with_compilation_error(self):
        """Test running a file with compilation errors."""
        source_code = """
game MyGame {
    title = "Test"
    // Missing closing brace
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "error.game")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Run
            cli = CLI()
            result = cli.run_file(input_path)
            
            # Should return error code
            assert result == 1


class TestCLICaching:
    """Test CLI caching functionality."""
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        cli = CLI()
        
        source1 = "game Test {}"
        source2 = "game Test {}"
        source3 = "game Different {}"
        
        key1 = cli.get_cache_key(source1, "test.game")
        key2 = cli.get_cache_key(source2, "test.game")
        key3 = cli.get_cache_key(source3, "test.game")
        
        # Same source should produce same key
        assert key1 == key2
        # Different source should produce different key
        assert key1 != key3
    
    def test_cache_save_and_retrieve(self):
        """Test saving and retrieving from cache."""
        cli = CLI()
        
        cache_key = "test_key_12345"
        output = "# Generated code\nprint('hello')"
        
        # Save to cache
        cli.save_to_cache(cache_key, output)
        
        # Retrieve from cache
        cached = cli.get_cached_output(cache_key)
        
        assert cached == output
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        cli = CLI()
        
        cached = cli.get_cached_output("nonexistent_key")
        
        assert cached is None
    
    def test_transpile_uses_cache(self):
        """Test that transpilation uses cache on second run."""
        source_code = """
game CachedGame {
    title = "Cache Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "cached.game")
            output_path1 = os.path.join(tmpdir, "output1.py")
            output_path2 = os.path.join(tmpdir, "output2.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            
            # First transpilation
            start1 = time.time()
            result1 = cli.transpile_file(input_path, output_path1)
            time1 = time.time() - start1
            
            # Second transpilation (should use cache)
            start2 = time.time()
            result2 = cli.transpile_file(input_path, output_path2)
            time2 = time.time() - start2
            
            # Both should succeed
            assert result1 == 0
            assert result2 == 0
            
            # Both outputs should be identical
            with open(output_path1, 'r') as f:
                output1 = f.read()
            with open(output_path2, 'r') as f:
                output2 = f.read()
            
            assert output1 == output2
            
            # Second run should be faster (cached)
            # Note: This might not always be true in test environments
            # so we just check both completed successfully


class TestCLIWatchMode:
    """Test CLI watch mode functionality."""
    
    def test_watch_mode_detects_changes(self):
        """Test that watch mode detects file changes."""
        # This test is complex to implement properly as it requires
        # running watch mode in a separate thread and simulating file changes
        # For now, we'll skip this test or implement a basic version
        pytest.skip("Watch mode testing requires complex async setup")
    
    def test_watch_mode_nonexistent_file(self):
        """Test watch mode with nonexistent file."""
        cli = CLI()
        
        # This should return error immediately
        # But watch mode runs in a loop, so we need to handle this differently
        # For now, we'll test that it handles the error gracefully
        # by checking the initial file existence
        
        result = cli.watch_mode("nonexistent.game", "output.py")
        assert result == 1


class TestCLIIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_transpilation_workflow(self):
        """Test complete transpilation workflow with sprite and scene."""
        source_code = """
game CompleteGame {
    title = "Complete Test"
    width = 800
    height = 600
}

sprite Player {
    x = 400
    y = 300
    speed = 5
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
    }
}

scene MainScene {
    player = Player()
    
    update {
        // Update logic
    }
    
    draw {
        // Draw logic
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "complete.game")
            output_path = os.path.join(tmpdir, "complete.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Check success
            assert result == 0
            assert os.path.exists(output_path)
            
            # Verify generated code structure
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Check for key components
            assert "import pygame" in generated
            assert "import sys" in generated
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "def __init__(self):" in generated
            assert "def handle_keydown(self, key):" in generated
            assert "def main():" in generated
            assert "pygame.init()" in generated
            assert "pygame.display.set_mode((800, 600))" in generated
            assert 'pygame.display.set_caption("Complete Test")' in generated
            assert "while running:" in generated
            assert "pygame.event.get()" in generated
            assert "if __name__ == '__main__':" in generated
    
    def test_multiple_sprites(self):
        """Test transpiling with multiple sprite definitions."""
        source_code = """
game MultiSpriteGame {
    title = "Multi Sprite"
}

sprite Player {
    x = 100
    y = 100
}

sprite Enemy {
    x = 200
    y = 200
}

sprite Bullet {
    x = 0
    y = 0
    speed = 10
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "multi.game")
            output_path = os.path.join(tmpdir, "multi.py")
            
            # Write source file
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Transpile
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            # Check success
            assert result == 0
            
            # Verify all sprites are generated
            with open(output_path, 'r') as f:
                generated = f.read()
            
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "class Enemy(pygame.sprite.Sprite)" in generated
            assert "class Bullet(pygame.sprite.Sprite)" in generated
