# Installing LevLang VSCode Extension

## Method 1: Direct Installation (Easiest)

1. **Copy the extension folder**:
   ```bash
   # On macOS/Linux
   cp -r vscode-levlang ~/.vscode/extensions/
   
   # On Windows (PowerShell)
   Copy-Item -Recurse vscode-levlang "$env:USERPROFILE\.vscode\extensions\"
   ```

2. **Restart VSCode**

3. **Verify installation**:
   - Open a `.lvl` file
   - You should see syntax highlighting!

## Method 2: Build and Install VSIX

If you want to create a distributable package:

1. **Install vsce** (VSCode Extension Manager):
   ```bash
   npm install -g @vscode/vsce
   ```

2. **Navigate to the extension folder**:
   ```bash
   cd vscode-levlang
   ```

3. **Package the extension**:
   ```bash
   vsce package
   ```
   This creates a `.vsix` file.

4. **Install the VSIX**:
   - Open VSCode
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Extensions: Install from VSIX"
   - Select the generated `.vsix` file

## Method 3: Development Mode

For testing and development:

1. **Open the extension folder in VSCode**:
   ```bash
   code vscode-levlang
   ```

2. **Press F5** to launch a new VSCode window with the extension loaded

3. **Test with a `.lvl` file**

## Verifying Installation

1. Create a test file: `test.lvl`
2. Add some LevLang code:
   ```levlang
   game "Test" auto_fps
   player { speed: 5 }
   start()
   ```
3. Check if keywords are highlighted in different colors

## Troubleshooting

### Extension not loading
- Make sure the folder is in the correct extensions directory
- Restart VSCode completely
- Check VSCode's Output panel (View → Output → Extensions)

### No syntax highlighting
- Verify the file has `.lvl` extension
- Try reloading the window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Colors look wrong
- The extension uses your current theme's colors
- Try a different color theme: `Ctrl+K Ctrl+T`

## Uninstalling

To remove the extension:

```bash
# On macOS/Linux
rm -rf ~/.vscode/extensions/levlang-*

# On Windows (PowerShell)
Remove-Item -Recurse "$env:USERPROFILE\.vscode\extensions\levlang-*"
```

Then restart VSCode.

## Publishing to Marketplace (Future)

To publish this extension to the VSCode Marketplace:

1. Create a publisher account at https://marketplace.visualstudio.com/
2. Get a Personal Access Token from Azure DevOps
3. Login with vsce: `vsce login <publisher-name>`
4. Publish: `vsce publish`

---

**Need help?** Open an issue at https://github.com/sriramramnath/language/issues
