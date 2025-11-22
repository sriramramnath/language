# Why I Made LevLang

**By Sriram Ramnath | November 2025**

---

## The Problem

When I started learning game development, I faced a frustrating dilemma: visual game engines like Unity were overwhelming with their complex interfaces and hundreds of features I didn't need, while coding games from scratch in Python/Pygame required writing mountains of boilerplate code just to get a simple square moving on screen.

I remember spending hours writing the same setup code over and over again:

```python
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Finally, I can start writing my actual game logic!
    # ...but I'm already exhausted
```

**There had to be a better way.**

## The Spark of an Idea

I wanted something that felt like describing a game to a friend:

> "There's a blue player at the center who can move with arrow keys, and a red enemy that follows the player."

Why couldn't I just *write* that and have it work? Why did I need to manage event loops, clock ticks, sprite groups, and collision detection manually every single time?

That's when the idea for LevLang was born.

## The Philosophy

LevLang is built on three core principles:

### 1. **Simplicity First**

Your first game should take 5 lines, not 50. No classes, no inheritance hierarchies, no design patterns—just describe what you want:

```levlang
game "My First Game"

player {
    color: blue
    speed: 5
}

start()
```

That's it. You have a game.

### 2. **Progressive Complexity**

As you grow, LevLang grows with you. Need raw Pygame access? Use the `blockname[]` syntax:

```levlang
game_loop[
    # Write any Python/Pygame code here
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)
]
```

You're not locked into a "beginner" language. LevLang is Pygame—just with the boring parts automated.

### 3. **Instant Feedback**

Games are fun because of the rapid iteration cycle. LevLang embraces this with:

- **Fast transpilation** (milliseconds, not seconds)
- **Watch mode** (auto-recompile on save)
- **Clear error messages** (with line numbers and suggestions)

Change a color, save the file, see it instantly. That's how learning should feel.

## Who It's For

LevLang is for:

- **Students** learning their first programming language
- **Teachers** who want to make CS education more engaging
- **Hobbyists** prototyping game ideas over a weekend
- **Game jam participants** who need to move fast
- **Anyone** who wants to make games without the ceremony

## Why Not Just Use X?

**"Why not just use Pygame?"**  
You should! LevLang *is* Pygame. It just removes the boilerplate so you can focus on the fun parts.

**"Why not use Scratch/Blockly?"**  
Visual programming is great for absolute beginners, but text-based coding teaches you skills that transfer to real-world programming.

**"Why not use Unity/Godot?"**  
Those are professional engines for serious projects. LevLang is a learning tool that gets out of your way.

## The Journey

Building LevLang has been an incredible learning experience. I've:

- Designed and implemented a complete programming language
- Built a lexer, parser, and code generator from scratch
- Created a transpiler that generates clean, readable Python
- Learned about language design trade-offs
- Connected with educators and students who found it useful

## What's Next

LevLang is still evolving. Future plans include:

- More built-in game patterns (collision detection, scoring, levels)
- Physics integration
- Sound and music support
- More comprehensive documentation
- A community gallery of games
- VS Code extension improvements

## The Real Reason

Here's the honest truth: I made LevLang because **I wish it had existed when I was learning**.

I spent too many hours fighting with boilerplate, getting lost in documentation, and feeling like I was "doing it wrong" because my simple games required so much complex code.

If LevLang helps even one person skip that frustration and get straight to the joy of creating games, then every hour I've spent building it was worth it.

## Try It Yourself

```bash
pip install levlang
```

Make something fun. Share it with others. Teach someone else. That's what LevLang is all about.

---

**Questions? Ideas? Found a bug?**  
Open an issue on [GitHub](https://github.com/sriramramnath/language) or reach out at sriramramnath2011@gmail.com

**License:** MIT (see why in my other blog post!)

---

*This post was written in November 2025, documenting the creation of LevLang v0.1.0. The language continues to evolve based on community feedback.*

