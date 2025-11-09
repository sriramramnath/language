# Getting Started with LevLang

Welcome to LevLang! This guide will help you create your first game in minutes.

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install LevLang

```bash
# Clone the repository
git clone https://github.com/sriramramnath/language.git
cd language

# Install LevLang
pip install -e .

# Verify installation
levlang --version
```

You should see:
```
╻  ┏━╸╻ ╻╻  ┏━┓┏┓╻┏━╸
┃  ┣╸ ┃┏┛┃  ┣━┫┃┗┫┃╺┓
┗━╸┗━╸┗┛ ┗━╸╹ ╹╹ ╹┗━┛ 
-----------------------
     Levelium Inc.
-----------------------
>> CLI version 0.1.0
```

---

## 🎮 Your First Game

### Step 1: Create a Game File

Create a file called `mygame.lvl`:

```levlang
// My First Game
game "My First Game"

player moves with arrows
player speed 5

enemies spawn every 3sec
enemies move down
enemies speed 3

when player hits enemy game over

show score at top left
```

### Step 2: Run Your Game

```bash
levlang run mygame.lvl
```

That's it! Your game is running! 🎉

---

## 🎯 Understanding the Code

Let's break down what each line does:

```levlang
game "My First Game"              // Creates a game window with title
```

```levlang
player moves with arrows          // Player controlled by arrow keys
player speed 5                    // Player moves at speed 5
```

```levlang
enemies spawn every 3sec          // New enemy appears every 3 seconds
enemies move down                 // Enemies move downward
enemies speed 3                   // Enemies move at speed 3
```

```levlang
when player hits enemy game over  // Collision ends the game
```

```levlang
show score at top left            // Display score in top-left corner
```

---

## 🚀 Next Steps

### Add More Features

```levlang
// Add coins for scoring
coins spawn every 5sec
coins worth 10

when player hits coin score +10

// Add UI elements
show lives at top right
show message "Collect coins!" for 3sec
```

### Customize Your Game

```levlang
// Change window size
game "My Game" 1024x768

// Change background color
game "My Game" black

// Add custom sprites
player sprite "assets/player.png"
enemies sprite "assets/enemy.png"
```

---

## 📚 Learn More

- [Complete Syntax Reference](syntax-reference.md)
- [Game Examples](examples.md)
- [Built-in Functions](functions.md)
- [Tutorial: Space Shooter](tutorial-space-shooter.md)
- [Tutorial: Platformer](tutorial-platformer.md)

---

## 🎨 CLI Commands

### Transpile to Python
```bash
levlang transpile mygame.lvl -o mygame.py
```

### Watch Mode (Auto-transpile on save)
```bash
levlang watch mygame.lvl
```

### Run Game
```bash
levlang run mygame.lvl
```

### Get Help
```bash
levlang --help
```

---

## 💡 Tips for Beginners

1. **Start Simple** - Begin with basic movement and one enemy type
2. **Test Often** - Run your game frequently to see changes
3. **Use Comments** - Add `//` comments to explain your code
4. **Check Examples** - Look at example games in the `examples/` folder
5. **Experiment** - Try changing numbers and see what happens!

---

## 🐛 Troubleshooting

### Game won't run
- Check that the file has `.lvl` extension
- Make sure LevLang is installed: `levlang --version`
- Look for syntax errors in your code

### No window appears
- Check if pygame is installed: `pip install pygame`
- Try running the generated Python file directly: `python mygame.py`

### Syntax errors
- Check for typos in keywords
- Make sure quotes are closed: `"text"`
- Verify indentation is correct

---

## 🎓 Learning Path

### Beginner (Week 1)
- ✅ Install LevLang
- ✅ Create first game
- ✅ Add player movement
- ✅ Add enemies
- ✅ Add scoring

### Intermediate (Week 2)
- ✅ Add multiple enemy types
- ✅ Add power-ups
- ✅ Add sound effects
- ✅ Create multiple levels
- ✅ Add game over screen

### Advanced (Week 3+)
- ✅ Custom sprites and animations
- ✅ Complex collision detection
- ✅ Boss battles
- ✅ Save/load system
- ✅ Publish your game!

---

## 🤝 Get Help

- **Documentation**: [docs/](.)
- **Examples**: [examples/](../examples/)
- **GitHub Issues**: [Report bugs](https://github.com/sriramramnath/language/issues)
- **Community**: Coming soon!

---

**Ready to create amazing games? Let's go!** 🚀

[Next: Syntax Reference →](syntax-reference.md)
