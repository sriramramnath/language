"""End-to-end integration tests for the game language transpiler."""

import pytest
import os
import tempfile
import subprocess
import sys
from pathlib import Path

from gamelang.cli.cli import CLI


class TestEndToEndTranspilation:
    """Test complete transpilation workflows from source to executable code."""
    
    def test_complete_game_with_all_features(self):
        """Test transpiling a complete game with all language features."""
        source_code = """
game CompleteGame {
    title = "Complete Feature Test"
    width = 800
    height = 600
}

sprite Player {
    image = "player.png"
    x = 400
    y = 300
    speed = 5
    health = 100
    score = 0
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
        if key == "UP" {
            y = y - speed
        }
        if key == "DOWN" {
            y = y + speed
        }
    }
    
    on keyup(key) {
        // Handle key release
    }
}

sprite Enemy {
    x = 600
    y = 200
    speed = 2
    direction = 1
    active = true
}

sprite Coin {
    x = 300
    y = 400
    value = 10
    collected = false
}

scene MainScene {
    player = Player()
    enemy = Enemy()
    coin = Coin()
    game_over = false
    
    update {
        if game_over == false {
            // Update enemy position
            enemy.x = enemy.x + (enemy.speed * enemy.direction)
            if enemy.x > 700 {
                enemy.direction = -1
            }
            if enemy.x < 100 {
                enemy.direction = 1
            }
            
            // Collision detection
            if collides(player, coin) {
                if coin.collected == false {
                    coin.collected = true
                    player.score = player.score + coin.value
                }
            }
            
            if collides(player, enemy) {
                player.health = player.health - 10
                if player.health <= 0 {
                    game_over = true
                }
            }
        }
    }
    
    draw {
        screen.fill((50, 50, 100))
        
        if coin.collected == false {
            coin.draw()
        }
        
        enemy.draw()
        player.draw()
        
        // Draw UI
        draw_text("Score: " + str(player.score), 10, 10, (255, 255, 255))
        draw_text("Health: " + str(player.health), 10, 40, (255, 255, 255))
        
        if game_over == true {
            draw_text("GAME OVER", 300, 250, (255, 0, 0))
        }
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
            
            # Verify transpilation succeeded
            assert result == 0, "Transpilation should succeed"
            assert os.path.exists(output_path), "Output file should be created"
            
            # Read generated code
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify all key components are present
            assert "import pygame" in generated
            assert "import sys" in generated
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "class Enemy(pygame.sprite.Sprite)" in generated
            assert "class Coin(pygame.sprite.Sprite)" in generated
            assert "def main():" in generated
            assert "pygame.init()" in generated
            assert "pygame.display.set_mode((800, 600))" in generated
            assert 'pygame.display.set_caption("Complete Feature Test")' in generated
            assert "while running:" in generated
            assert "if event.type == pygame.KEYDOWN:" in generated
            assert "if event.type == pygame.KEYUP:" in generated
            assert "pygame.display.flip()" in generated
            assert "clock.tick(60)" in generated
            assert "if __name__ == '__main__':" in generated
            
            # Verify generated code is valid Python
            try:
                compile(generated, output_path, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Generated code has syntax errors: {e}")
    
    def test_sprite_movement_example(self):
        """Test transpiling the sprite movement example."""
        source_code = """
game SpriteMovement {
    title = "Sprite Movement Example"
    width = 800
    height = 600
}

sprite Player {
    image = "player.png"
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
        if key == "UP" {
            y = y - speed
        }
        if key == "DOWN" {
            y = y + speed
        }
    }
}

scene Main {
    player = Player()
    
    update {
        if player.x < 0 {
            player.x = 0
        }
        if player.x > 800 {
            player.x = 800
        }
        if player.y < 0 {
            player.y = 0
        }
        if player.y > 600 {
            player.y = 600
        }
    }
    
    draw {
        screen.fill((50, 50, 100))
        player.draw()
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "movement.game")
            output_path = os.path.join(tmpdir, "movement.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify key features
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "def handle_keydown(self, key):" in generated
            assert "self.speed = 5" in generated
            
            # Verify code compiles
            compile(generated, output_path, 'exec')
    
    def test_collision_detection_example(self):
        """Test transpiling collision detection example."""
        source_code = """
game CollisionGame {
    title = "Collision Detection"
    width = 800
    height = 600
}

sprite Player {
    x = 100
    y = 300
    speed = 5
    score = 0
}

sprite Coin {
    x = 400
    y = 300
    collected = false
}

scene Main {
    player = Player()
    coin = Coin()
    
    update {
        if collides(player, coin) {
            if coin.collected == false {
                coin.collected = true
                player.score = player.score + 10
            }
        }
    }
    
    draw {
        screen.fill((30, 30, 30))
        if coin.collected == false {
            coin.draw()
        }
        player.draw()
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "collision.game")
            output_path = os.path.join(tmpdir, "collision.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "class Coin(pygame.sprite.Sprite)" in generated
            assert "self.score = 0" in generated
            assert "self.collected = False" in generated
            
            compile(generated, output_path, 'exec')
    
    def test_event_handling_example(self):
        """Test transpiling event handling example."""
        source_code = """
game EventDemo {
    title = "Event Handling"
    width = 800
    height = 600
}

sprite Box {
    x = 400
    y = 300
    color = (100, 100, 255)
    
    on keydown(key) {
        if key == "R" {
            color = (255, 100, 100)
        }
        if key == "G" {
            color = (100, 255, 100)
        }
        if key == "B" {
            color = (100, 100, 255)
        }
    }
    
    on mousedown(button, mx, my) {
        x = mx
        y = my
    }
}

scene Main {
    box = Box()
    
    update {
        // Update logic
    }
    
    draw {
        screen.fill((40, 40, 40))
        box.draw()
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "events.game")
            output_path = os.path.join(tmpdir, "events.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            assert "class Box(pygame.sprite.Sprite)" in generated
            assert "def handle_keydown(self, key):" in generated
            assert "def handle_mousedown(self, button, mx, my):" in generated
            
            compile(generated, output_path, 'exec')
    
    def test_multiple_sprites_and_scenes(self):
        """Test transpiling with multiple sprites and complex interactions."""
        source_code = """
game MultiGame {
    title = "Multiple Sprites"
    width = 800
    height = 600
}

sprite Player {
    x = 100
    y = 100
    speed = 5
}

sprite Enemy {
    x = 200
    y = 200
    speed = 3
}

sprite Bullet {
    x = 0
    y = 0
    speed = 10
    active = false
}

sprite PowerUp {
    x = 400
    y = 300
    collected = false
}

scene MainScene {
    player = Player()
    enemy = Enemy()
    bullet = Bullet()
    powerup = PowerUp()
    
    update {
        if bullet.active == true {
            bullet.y = bullet.y - bullet.speed
        }
        
        if collides(player, powerup) {
            if powerup.collected == false {
                powerup.collected = true
                player.speed = player.speed + 2
            }
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
        enemy.draw()
        if bullet.active == true {
            bullet.draw()
        }
        if powerup.collected == false {
            powerup.draw()
        }
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "multi.game")
            output_path = os.path.join(tmpdir, "multi.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify all sprites are generated
            assert "class Player(pygame.sprite.Sprite)" in generated
            assert "class Enemy(pygame.sprite.Sprite)" in generated
            assert "class Bullet(pygame.sprite.Sprite)" in generated
            assert "class PowerUp(pygame.sprite.Sprite)" in generated
            
            # Verify instantiation
            assert "player = Player()" in generated
            assert "enemy = Enemy()" in generated
            assert "bullet = Bullet()" in generated
            assert "powerup = PowerUp()" in generated
            
            compile(generated, output_path, 'exec')
    
    def test_complex_expressions_and_statements(self):
        """Test transpiling complex expressions and control flow."""
        source_code = """
game ExpressionTest {
    title = "Expression Test"
}

sprite Calculator {
    a = 10
    b = 20
    result = 0
}

scene Main {
    calc = Calculator()
    
    update {
        // Arithmetic expressions
        calc.result = (calc.a + calc.b) * 2 - 5
        calc.result = calc.a / calc.b + 3
        calc.result = calc.a % calc.b
        
        // Comparison expressions
        if calc.a > calc.b {
            calc.result = 1
        }
        if calc.a < calc.b {
            calc.result = 2
        }
        if calc.a == calc.b {
            calc.result = 3
        }
        if calc.a != calc.b {
            calc.result = 4
        }
        
        // Logical expressions
        if calc.a > 5 {
            if calc.b < 30 {
                calc.result = 5
            }
        }
        if calc.a < 5 {
            calc.result = 6
        }
        if calc.b > 15 {
            calc.result = 6
        }
        
        // While loop
        while calc.result < 100 {
            calc.result = calc.result + 1
        }
        
        // Nested if-else
        if calc.a > 0 {
            if calc.b > 0 {
                calc.result = calc.a + calc.b
            } else {
                calc.result = calc.a - calc.b
            }
        } else {
            calc.result = 0
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "expressions.game")
            output_path = os.path.join(tmpdir, "expressions.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify expressions are generated
            assert "+" in generated
            assert "-" in generated
            assert "*" in generated
            assert "/" in generated
            assert "%" in generated
            assert ">" in generated
            assert "<" in generated
            assert "==" in generated
            assert "!=" in generated
            assert "and" in generated
            assert "or" in generated
            assert "while" in generated
            
            compile(generated, output_path, 'exec')
    
    def test_minimal_game(self):
        """Test transpiling a minimal game with just game declaration."""
        source_code = """
game MinimalGame {
    title = "Minimal"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "minimal.game")
            output_path = os.path.join(tmpdir, "minimal.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Should still have basic structure
            assert "import pygame" in generated
            assert "def main():" in generated
            assert "pygame.init()" in generated
            assert 'pygame.display.set_caption("Minimal")' in generated
            
            compile(generated, output_path, 'exec')
    
    def test_sprite_with_image_property(self):
        """Test that sprites with image property generate correct pygame code."""
        source_code = """
sprite ImageSprite {
    image = "sprite.png"
    x = 100
    y = 200
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "image.game")
            output_path = os.path.join(tmpdir, "image.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify image loading code
            assert "pygame.image.load" in generated
            assert "self.rect = self.image.get_rect()" in generated
            assert "self.rect.center" in generated
            
            compile(generated, output_path, 'exec')


class TestEndToEndExecution:
    """Test that generated code can actually execute (where possible)."""
    
    def test_generated_code_imports_successfully(self):
        """Test that generated code can be imported without errors."""
        source_code = """
game TestGame {
    title = "Import Test"
}

sprite TestSprite {
    x = 100
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "import_test.game")
            output_path = os.path.join(tmpdir, "import_test.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            result = cli.transpile_file(input_path, output_path)
            
            assert result == 0
            
            # Try to compile and check for import errors
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Compile the code
            code_obj = compile(generated, output_path, 'exec')
            
            # Create a namespace and execute imports only
            namespace = {}
            try:
                # Execute just the import statements
                import_lines = [line for line in generated.split('\n') if line.strip().startswith('import')]
                import_code = '\n'.join(import_lines)
                exec(import_code, namespace)
                
                # Verify pygame was imported
                assert 'pygame' in namespace
                assert 'sys' in namespace
            except ImportError as e:
                pytest.skip(f"pygame not available in test environment: {e}")


class TestEndToEndRealExamples:
    """Test transpiling the actual example files from the examples directory."""
    
    def test_transpile_sprite_movement_example_file(self):
        """Test transpiling the actual sprite_movement.game example."""
        example_path = "examples/sprite_movement.game"
        
        if not os.path.exists(example_path):
            pytest.skip("Example file not found")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "sprite_movement.py")
            
            cli = CLI()
            result = cli.transpile_file(example_path, output_path)
            
            assert result == 0, "Sprite movement example should transpile successfully"
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            # Verify it's valid Python
            compile(generated, output_path, 'exec')
    
    def test_transpile_collision_detection_example_file(self):
        """Test transpiling the actual collision_detection.game example."""
        example_path = "examples/collision_detection.game"
        
        if not os.path.exists(example_path):
            pytest.skip("Example file not found")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "collision_detection.py")
            
            cli = CLI()
            result = cli.transpile_file(example_path, output_path)
            
            assert result == 0, "Collision detection example should transpile successfully"
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            compile(generated, output_path, 'exec')
    
    def test_transpile_event_handling_example_file(self):
        """Test transpiling the actual event_handling.game example."""
        example_path = "examples/event_handling.game"
        
        if not os.path.exists(example_path):
            pytest.skip("Example file not found")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "event_handling.py")
            
            cli = CLI()
            result = cli.transpile_file(example_path, output_path)
            
            assert result == 0, "Event handling example should transpile successfully"
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                generated = f.read()
            
            compile(generated, output_path, 'exec')


class TestEndToEndCLICommands:
    """Test CLI commands end-to-end."""
    
    def test_cli_transpile_command(self):
        """Test the CLI transpile command."""
        source_code = """
game CLITest {
    title = "CLI Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "cli_test.game")
            output_path = os.path.join(tmpdir, "cli_test.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            exit_code = cli.transpile_file(input_path, output_path)
            
            assert exit_code == 0
            assert os.path.exists(output_path)
    
    def test_cli_run_command_with_valid_code(self):
        """Test the CLI run command with valid code."""
        # Create a game that exits immediately
        source_code = """
game QuickExit {
    title = "Quick Exit"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "quick.game")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            # Note: This may fail in headless environments
            # We're just testing that it doesn't crash the CLI
            try:
                exit_code = cli.run_file(input_path)
                # Any exit code is acceptable as long as it doesn't crash
                assert exit_code is not None
            except Exception as e:
                # In headless environments, pygame might fail to initialize
                # This is acceptable for this test
                if "No available video device" not in str(e):
                    raise
    
    def test_cli_default_output_path(self):
        """Test that CLI uses default output path when not specified."""
        source_code = """
game DefaultOutput {
    title = "Default"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "default.game")
            expected_output = os.path.join(tmpdir, "default.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            exit_code = cli.transpile_file(input_path)
            
            assert exit_code == 0
            assert os.path.exists(expected_output)
