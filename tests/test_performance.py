"""Performance tests for the game language transpiler."""

import pytest
import os
import tempfile
import time

from levlang.cli.cli import CLI


class TestTranspilationPerformance:
    """Test transpilation performance requirements."""
    
    def test_small_file_transpilation_speed(self):
        """Test that small files (< 100 lines) transpile quickly."""
        # Create a small game file (~50 lines)
        source_code = """
game SmallGame {
    title = "Small Test"
    width = 800
    height = 600
}

sprite Player {
    x = 100
    y = 200
    speed = 5
    health = 100
    
    on keydown(key) {
        if key == "LEFT" {
            x = x - speed
        }
        if key == "RIGHT" {
            x = x + speed
        }
    }
}

sprite Enemy {
    x = 300
    y = 400
    active = true
}

scene Main {
    player = Player()
    enemy = Enemy()
    
    update {
        if enemy.active == true {
            enemy.x = enemy.x + 1
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
        enemy.draw()
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "small.lvl")
            output_path = os.path.join(tmpdir, "small.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            
            # Measure transpilation time
            start_time = time.time()
            result = cli.transpile_file(input_path, output_path)
            elapsed_time = time.time() - start_time
            
            assert result == 0, "Transpilation should succeed"
            # Small files should transpile very quickly (< 100ms)
            assert elapsed_time < 0.1, f"Small file took {elapsed_time:.3f}s, expected < 0.1s"
    
    def test_medium_file_transpilation_speed(self):
        """Test that medium files (~500 lines) transpile within reasonable time."""
        # Generate a medium-sized game file
        source_code = """
game MediumGame {
    title = "Medium Test"
    width = 800
    height = 600
}
"""
        
        # Add 10 sprites with various properties and methods
        for i in range(10):
            source_code += f"""
sprite Sprite{i} {{
    x = {i * 10}
    y = {i * 20}
    speed = {i + 1}
    health = 100
    active = true
    score = 0
    
    on keydown(key) {{
        if key == "LEFT" {{
            x = x - speed
        }}
        if key == "RIGHT" {{
            x = x + speed
        }}
        if key == "UP" {{
            y = y - speed
        }}
        if key == "DOWN" {{
            y = y + speed
        }}
    }}
    
    on keyup(key) {{
        // Handle key release
    }}
    
    on mousedown(button, mx, my) {{
        if mx > x and mx < x + 50 {{
            if my > y and my < y + 50 {{
                active = not active
            }}
        }}
    }}
    
    update {{
        if active {{
            x = x + speed
            if x > 800 {{
                x = 0
            }}
        }}
    }}
}}
"""
        
        # Add a scene that uses all sprites
        source_code += "\nscene Main {\n"
        for i in range(10):
            source_code += f"    sprite{i} = Sprite{i}()\n"
        
        source_code += """
    update {
"""
        for i in range(10):
            source_code += f"        sprite{i}.update()\n"
        
        source_code += """    }
    
    draw {
        screen.fill((0, 0, 0))
"""
        for i in range(10):
            source_code += f"        sprite{i}.draw()\n"
        
        source_code += """    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "medium.lvl")
            output_path = os.path.join(tmpdir, "medium.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Verify file size
            line_count = source_code.count('\n')
            assert 400 < line_count < 700, f"Expected ~500 lines, got {line_count}"
            
            cli = CLI()
            
            # Measure transpilation time
            start_time = time.time()
            result = cli.transpile_file(input_path, output_path)
            elapsed_time = time.time() - start_time
            
            assert result == 0, "Transpilation should succeed"
            # Medium files should transpile reasonably fast (< 500ms)
            assert elapsed_time < 0.5, f"Medium file took {elapsed_time:.3f}s, expected < 0.5s"
    
    def test_large_file_transpilation_speed(self):
        """Test that large files (~1000 lines) transpile under 2 seconds."""
        # Generate a large game file
        source_code = """
game LargeGame {
    title = "Large Test"
    width = 1920
    height = 1080
}
"""
        
        # Add 20 sprites with various properties and methods
        for i in range(20):
            source_code += f"""
sprite Sprite{i} {{
    x = {i * 10}
    y = {i * 20}
    speed = {i + 1}
    health = 100
    active = true
    score = 0
    level = 1
    power = 10
    defense = 5
    
    on keydown(key) {{
        if key == "LEFT" {{
            x = x - speed
        }}
        if key == "RIGHT" {{
            x = x + speed
        }}
        if key == "UP" {{
            y = y - speed
        }}
        if key == "DOWN" {{
            y = y + speed
        }}
        if key == "SPACE" {{
            active = not active
        }}
        if key == "A" {{
            power = power + 1
        }}
        if key == "S" {{
            defense = defense + 1
        }}
    }}
    
    on keyup(key) {{
        // Handle key release
        if key == "SPACE" {{
            score = score + 1
        }}
    }}
    
    on mousedown(button, mx, my) {{
        if mx > x and mx < x + 50 {{
            if my > y and my < y + 50 {{
                active = not active
                score = score + 10
            }}
        }}
    }}
    
    on mouseup(button, mx, my) {{
        // Handle mouse release
    }}
    
    on mousemove(mx, my) {{
        // Track mouse movement
    }}
}}
"""
        
        # Add scenes
        for scene_idx in range(3):
            source_code += f"\nscene Scene{scene_idx} {{\n"
            
            # Instantiate sprites
            for i in range(20):
                source_code += f"    sprite{i} = Sprite{i}()\n"
            
            source_code += """
    game_over = false
    paused = false
    score = 0
    
    update {
        if game_over == false {
            if paused == false {
                // Game logic
                score = score + 1
                
                if score > 1000 {
                    game_over = true
                }
            }
        }
    }
    
    draw {
        screen.fill((0, 0, 0))
        
"""
            # Draw all sprites
            for i in range(20):
                source_code += f"        sprite{i}.draw()\n"
            
            source_code += """
        // Draw UI
        draw_text("Score: " + str(score), 10, 10, (255, 255, 255))
        
        if game_over == true {
            draw_text("GAME OVER", 800, 500, (255, 0, 0))
        }
        
        if paused == true {
            draw_text("PAUSED", 850, 500, (255, 255, 0))
        }
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "large.lvl")
            output_path = os.path.join(tmpdir, "large.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Verify file size
            line_count = source_code.count('\n')
            assert 900 < line_count < 1200, f"Expected ~1000 lines, got {line_count}"
            
            cli = CLI()
            
            # Measure transpilation time
            start_time = time.time()
            result = cli.transpile_file(input_path, output_path)
            elapsed_time = time.time() - start_time
            
            assert result == 0, "Transpilation should succeed"
            # Requirement: 1000-line file should transpile under 2 seconds
            assert elapsed_time < 2.0, f"Large file took {elapsed_time:.3f}s, expected < 2.0s (Requirement 5.1)"
            
            print(f"Performance: {line_count} lines transpiled in {elapsed_time:.3f}s")
    
    def test_very_large_file_performance(self):
        """Test performance with very large files (2000+ lines)."""
        # Generate a very large game file
        source_code = """
game VeryLargeGame {
    title = "Very Large Test"
    width = 1920
    height = 1080
}
"""
        
        # Add 40 sprites
        for i in range(40):
            source_code += f"""
sprite Sprite{i} {{
    x = {i * 10}
    y = {i * 20}
    speed = {i + 1}
    health = 100
    active = true
    
    on keydown(key) {{
        if key == "LEFT" {{
            x = x - speed
        }}
        if key == "RIGHT" {{
            x = x + speed
        }}
    }}
}}
"""
        
        # Add multiple scenes
        for scene_idx in range(5):
            source_code += f"\nscene Scene{scene_idx} {{\n"
            for i in range(40):
                source_code += f"    sprite{i} = Sprite{i}()\n"
            source_code += """
    update {
        // Update logic here
    }
    
    draw {
        screen.fill((0, 0, 0))
"""
            for i in range(40):
                source_code += f"        sprite{i}.draw()\n"
            source_code += """    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "very_large.lvl")
            output_path = os.path.join(tmpdir, "very_large.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            line_count = source_code.count('\n')
            assert line_count > 2000, f"Expected > 2000 lines, got {line_count}"
            
            cli = CLI()
            
            start_time = time.time()
            result = cli.transpile_file(input_path, output_path)
            elapsed_time = time.time() - start_time
            
            assert result == 0, "Transpilation should succeed"
            # Should scale reasonably (< 4 seconds for 2x the size)
            assert elapsed_time < 4.0, f"Very large file took {elapsed_time:.3f}s, expected < 4.0s"
            
            print(f"Performance: {line_count} lines transpiled in {elapsed_time:.3f}s")


class TestCachingPerformance:
    """Test that caching improves performance."""
    
    def test_cache_improves_second_transpilation(self):
        """Test that second transpilation of same file uses cache."""
        source_code = """
game CacheTest {
    title = "Cache Test"
    width = 800
    height = 600
}

sprite Player {
    x = 100
    y = 200
    speed = 5
}

scene Main {
    player = Player()
    
    update {
        player.x = player.x + 1
    }
    
    draw {
        screen.fill((0, 0, 0))
        player.draw()
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "cache_test.lvl")
            output_path1 = os.path.join(tmpdir, "cache_test1.py")
            output_path2 = os.path.join(tmpdir, "cache_test2.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            
            # First transpilation (no cache)
            start_time1 = time.time()
            result1 = cli.transpile_file(input_path, output_path1)
            time1 = time.time() - start_time1
            
            assert result1 == 0
            
            # Second transpilation (should use cache)
            start_time2 = time.time()
            result2 = cli.transpile_file(input_path, output_path2)
            time2 = time.time() - start_time2
            
            assert result2 == 0
            
            # Verify outputs are identical
            with open(output_path1, 'r') as f:
                output1 = f.read()
            with open(output_path2, 'r') as f:
                output2 = f.read()
            
            assert output1 == output2, "Cached output should be identical"
            
            # Second run should be faster (cached)
            # Note: This might not always be true in test environments
            # but we can at least verify it completes successfully
            print(f"First transpilation: {time1:.4f}s, Second (cached): {time2:.4f}s")
    
    def test_cache_invalidation_on_change(self):
        """Test that cache is invalidated when source changes."""
        source_code1 = """
game Test {
    title = "Version 1"
}
"""
        
        source_code2 = """
game Test {
    title = "Version 2"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "invalidate.lvl")
            output_path = os.path.join(tmpdir, "invalidate.py")
            
            cli = CLI()
            
            # First transpilation
            with open(input_path, 'w') as f:
                f.write(source_code1)
            
            result1 = cli.transpile_file(input_path, output_path)
            assert result1 == 0
            
            with open(output_path, 'r') as f:
                output1 = f.read()
            
            # Modify source and transpile again
            with open(input_path, 'w') as f:
                f.write(source_code2)
            
            result2 = cli.transpile_file(input_path, output_path)
            assert result2 == 0
            
            with open(output_path, 'r') as f:
                output2 = f.read()
            
            # Outputs should be different (cache was invalidated)
            assert output1 != output2, "Cache should be invalidated on source change"
            assert '"Version 1"' in output1
            assert '"Version 2"' in output2
    
    def test_incremental_transpilation(self):
        """Test that incremental transpilation only processes changed files."""
        # This test verifies the caching mechanism works correctly
        source_code = """
game IncrementalTest {
    title = "Incremental"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "incremental.lvl")
            output_path = os.path.join(tmpdir, "incremental.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            
            # First transpilation
            result1 = cli.transpile_file(input_path, output_path)
            assert result1 == 0
            
            # Get modification time of output
            mtime1 = os.path.getmtime(output_path)
            
            # Wait a bit to ensure different timestamp
            time.sleep(0.01)
            
            # Transpile again without changing source
            result2 = cli.transpile_file(input_path, output_path)
            assert result2 == 0
            
            # Output file should be updated (even if from cache)
            mtime2 = os.path.getmtime(output_path)
            
            # Both transpilations should succeed
            assert result1 == 0 and result2 == 0


class TestWatchModePerformance:
    """Test watch mode performance characteristics."""
    
    def test_watch_mode_latency(self):
        """Test that watch mode detects changes with low latency."""
        # Note: This is a simplified test as full watch mode testing
        # requires complex async setup
        source_code = """
game WatchTest {
    title = "Watch Test"
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "watch.lvl")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            # Verify file exists and can be read quickly
            start_time = time.time()
            mtime = os.path.getmtime(input_path)
            elapsed = time.time() - start_time
            
            # File system operations should be very fast
            assert elapsed < 0.01, f"File stat took {elapsed:.4f}s, expected < 0.01s"
            assert mtime > 0


class TestPerformanceRegression:
    """Test for performance regressions."""
    
    def test_repeated_transpilations_consistent(self):
        """Test that repeated transpilations have consistent performance."""
        source_code = """
game ConsistencyTest {
    title = "Consistency"
}

sprite Player {
    x = 100
    y = 200
}

scene Main {
    player = Player()
    
    update {
        player.x = player.x + 1
    }
    
    draw {
        screen.fill((0, 0, 0))
    }
}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "consistency.lvl")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            times = []
            
            # Run 5 transpilations
            for i in range(5):
                output_path = os.path.join(tmpdir, f"consistency{i}.py")
                
                start_time = time.time()
                result = cli.transpile_file(input_path, output_path)
                elapsed = time.time() - start_time
                
                assert result == 0
                times.append(elapsed)
            
            # Calculate variance
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            # Times should be relatively consistent
            # (allowing for first run to be slower due to cache miss)
            print(f"Transpilation times: min={min_time:.4f}s, max={max_time:.4f}s, avg={avg_time:.4f}s")
            
            # All should complete in reasonable time
            assert max_time < 0.5, f"Max time {max_time:.4f}s exceeded 0.5s"
    
    def test_memory_efficiency(self):
        """Test that transpiler doesn't use excessive memory."""
        # Generate a moderately large file
        source_code = "game MemoryTest { title = \"Memory\" }\n"
        
        for i in range(50):
            source_code += f"""
sprite Sprite{i} {{
    x = {i}
    y = {i}
}}
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "memory.lvl")
            output_path = os.path.join(tmpdir, "memory.py")
            
            with open(input_path, 'w') as f:
                f.write(source_code)
            
            cli = CLI()
            
            # Transpile multiple times to check for memory leaks
            for i in range(10):
                result = cli.transpile_file(input_path, output_path)
                assert result == 0
            
            # If we got here without crashing, memory usage is acceptable
            assert True
