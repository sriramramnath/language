# LevCode IDE

```
╻  ┏━╸╻ ╻┏━╸┏━┓╻┏━┓┏━╸
┃  ┣╸ ┃┏┛┃  ┃ ┃┃┃ ┃┣╸ 
┗━╸┗━╸┗┛ ┗━╸┗━┛╺┻━┛┗━╸
```

**The Official IDE for LevLang Game Development**

Create games in minutes with an intuitive, powerful, and beautiful development environment.

---

## 🎮 What is LevCode?

LevCode is a specialized IDE designed exclusively for LevLang game development. It combines a modern code editor with live game preview, visual tools, and instant feedback to make game creation effortless.

### ✨ Key Features

- **🎨 Live Preview** - See your game running as you code
- **⚡ Instant Compilation** - Changes appear in real-time
- **🎯 Smart Editor** - Syntax highlighting, auto-completion, error detection
- **🖼️ Asset Manager** - Drag-and-drop sprites, sounds, and more
- **🐛 Integrated Debugger** - Step through code, inspect variables
- **📦 Project Templates** - Start with pre-built game templates
- **🎨 Visual Tools** - Scene editor, sprite editor, animation timeline

---

## 📸 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│  File  Edit  View  Run  Tools  Help              [- □ ×]    │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌──────────────────────────────────────┐   │
│ │   Files     │ │         Code Editor                  │   │
│ │             │ │                                       │   │
│ │ 📁 assets   │ │  game "Space Shooter" 800x600        │   │
│ │   🖼️ player │ │                                       │   │
│ │   🖼️ enemy  │ │  player moves with arrows            │   │
│ │   🔊 shoot  │ │  player shoots with space            │   │
│ │ 📁 scenes   │ │                                       │   │
│ │ 📄 game.lvl │ │  enemies spawn every 2sec            │   │
│ │             │ │  enemies move down                   │   │
│ └─────────────┘ └──────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────┐ ┌────────────────────────┐│
│ │      Live Preview            │ │    Properties          ││
│ │   ┌────────────────────┐     │ │                        ││
│ │   │                    │     │ │  🎮 Player             ││
│ │   │   [Game Running]   │     │ │    Speed: 5            ││
│ │   │                    │     │ │    Position: 400,300   ││
│ │   └────────────────────┘     │ │                        ││
│ │   ▶ Run  ⏸ Pause  ⏹ Stop   │ │  👾 Enemies            ││
│ │   FPS: 60  Score: 150       │ │    Count: 5            ││
│ └──────────────────────────────┘ └────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

### Step 1: Create a Project

Open LevCode and choose:
- New Project → Select a template (e.g., Space Shooter) or start blank
- Open Project → Load an existing project

Your project structure appears in the Files panel on the left.

---

### Step 2: Write Your Game Code

Edit the .lvl file in the Code Editor. Here's a minimal example:

```levlang
game "My Game" 800x600

player sprite "player.png" at 400, 300
player moves with arrows

enemy sprite "enemy.png" at 100, 100
enemy moves down 2px per frame
```

The editor highlights syntax and offers auto-completion as you type.

---

### Step 3: Run

Press **F5** or click **▶ Run**

Your game appears in the Live Preview panel!

---

## 🎨 Features in Detail

### 1. Smart Code Editor

**Syntax Highlighting**
- Keywords in red
- Strings in cyan
- Numbers in green
- Comments in gray

**Auto-Completion**
```levlang
player mo[TAB]  →  player moves with arrows
```

**Error Detection**
```levlang
player move with arrows  // ❌ Error: Did you mean "moves"?
```

**Quick Documentation**
Hover over any keyword to see documentation.

---

### 2. Live Preview

**Real-time Updates**
- Changes appear instantly
- No need to restart
- Hot-reload assets

**Debug Overlay**
- FPS counter
- Entity count
- Collision boxes
- Performance metrics

**Controls**
- **F5** - Run game
- **F6** - Pause/Resume
- **F7** - Stop
- **F8** - Restart

---

### 3. Asset Manager

**Drag & Drop**
```
Drag image → Assets folder → Auto-imported!
```

**Supported Formats**
- **Images**: PNG, JPG, GIF
- **Audio**: WAV, MP3, OGG
- **Fonts**: TTF, OTF

**Asset Preview**
- Click any asset to preview
- Edit properties
- Organize in folders

---

### 4. Visual Tools

#### Scene Editor
- Drag entities onto canvas
- Position with mouse
- Snap to grid
- Layer management

#### Sprite Editor
- Crop and resize
- Animation frames
- Collision boxes
- Export sprite sheets

#### Animation Timeline
- Keyframe animation
- Easing curves
- Preview playback
- Export to code

---

### 5. Debugger

**Breakpoints**
```levlang
when player hits enemy game over  // 🔴 Click to add breakpoint
```

**Variable Inspector**
```
player.x: 400
player.y: 300
player.speed: 5
score: 150
```

**Step Through**
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out

---

### 6. Project Templates

**Available Templates:**

1. **🎯 Space Shooter**
   - Top-down shooting
   - Enemy waves
   - Power-ups

2. **🐦 Flappy Bird**
   - Jumping mechanics
   - Obstacle generation
   - Score tracking

3. **🏃 Endless Runner**
   - Auto-scrolling
   - Procedural obstacles
   - Speed progression

4. **🎮 Platformer**
   - Gravity and jumping
   - Platform collision
   - Collectibles

5. **🧱 Breakout**
   - Paddle mechanics
   - Ball physics
   - Brick destruction

6. **👾 Space Invaders**
   - Grid enemies
   - Formation movement
   - Shield mechanics

7. **🎪 Catch Game**
   - Mouse control
   - Falling objects
   - Time limit

---

## ⌨️ Keyboard Shortcuts

### General
- **Ctrl+N** - New project
- **Ctrl+O** - Open project
- **Ctrl+S** - Save
- **Ctrl+Shift+S** - Save all
- **Ctrl+W** - Close file
- **Ctrl+Q** - Quit

### Editing
- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Ctrl+X** - Cut
- **Ctrl+C** - Copy
- **Ctrl+V** - Paste
- **Ctrl+F** - Find
- **Ctrl+H** - Replace
- **Ctrl+/** - Toggle comment

### Running
- **F5** - Run game
- **F6** - Pause/Resume
- **F7** - Stop
- **F8** - Restart
- **Ctrl+F5** - Run without debugging

### Debugging
- **F9** - Toggle breakpoint
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out

### View
- **Ctrl+B** - Toggle sidebar
- **Ctrl+J** - Toggle console
- **Ctrl+Shift+P** - Command palette
- **Ctrl+`** - Toggle terminal

---

## 🎨 Customization

### Themes

**Built-in Themes:**
- Dark (default)
- Light
- Monokai
- Dracula
- Nord
- Solarized

**Change Theme:**
```
Settings → Appearance → Theme
```

### Keybindings

**Customize Shortcuts:**
```
Settings → Keyboard Shortcuts
```

### Extensions

**Install Extensions:**
```
Extensions → Browse → Install
```

**Popular Extensions:**
- Git integration
- Sprite packer
- Sound editor
- Tilemap editor

---

## 🔧 Settings

### Editor Settings

```json
{
  "editor.fontSize": 14,
  "editor.fontFamily": "JetBrains Mono",
  "editor.tabSize": 2,
  "editor.autoSave": true,
  "editor.minimap": true,
  "editor.lineNumbers": true
}
```

### Game Settings

```json
{
  "game.autoRun": true,
  "game.showFPS": true,
  "game.showColliders": false,
  "game.targetFPS": 60
}
```

### Preview Settings

```json
{
  "preview.scale": 1.0,
  "preview.showControls": true,
  "preview.showStats": true
}
```

---

## 📦 Project Structure

```
my-game/
├── assets/
│   ├── sprites/
│   │   ├── player.png
│   │   └── enemy.png
│   ├── sounds/
│   │   ├── shoot.wav
│   │   └── explosion.wav
│   └── music/
│       └── bgm.mp3
├── scenes/
│   ├── menu.lvl
│   ├── game.lvl
│   └── gameover.lvl
├── game.lvl          # Main game file
└── project.json      # Project settings
```

---




## 🏢 About

**Created by Levelium Inc.**

LevCode is developed and maintained by Levelium Inc., dedicated to making game development accessible to everyone.

### Team
- **Founder**: Sriram Ramnath


## 🗺️ Roadmap

### Features
- ✅ Code editor with syntax highlighting
- ✅ Live preview
- ✅ Asset manager
- ✅ Project templates
- ✅ Basic debugging
- 🔄 Visual scene editor
- 🔄 Sprite editor
- 🔄 Animation timeline
- 🔄 Git integration
- 🔄 Cloud sync
- 🔄 Particle editor
- 🔄 Sound editor
- 🔄 Performance profiler
- 🔄 Collaborative editing

---


## 🎉 Acknowledgments

LevCode is built with amazing open-source technologies:

- **Electron** - Cross-platform desktop apps
- **Monaco Editor** - VSCode's editor
- **React** - UI framework
- **Phaser.js** - Game preview
- **Tauri** - Lightweight alternative to Electron

Special thanks to all contributors and the LevLang community!


Made with ❤️ by Levelium Inc.

```
╻  ┏━╸╻ ╻┏━╸┏━┓╻┏━┓┏━╸
┃  ┣╸ ┃┏┛┃  ┃ ┃┃┃ ┃┣╸ 
┗━╸┗━╸┗┛ ┗━╸┗━┛╺┻━┛┗━╸

Level Up Your Game Development
```
