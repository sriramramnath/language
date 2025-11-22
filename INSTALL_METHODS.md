# LevLang Installation Methods

Multiple ways to install LevLang, depending on your preference!

---

## 🚀 Method 1: Quick Install with curl (Easiest)

**One command to rule them all:**

```bash
curl -sSL https://raw.githubusercontent.com/sriramramnath/language/main/install.sh | bash
```

This will:
- ✅ Check for Python/pip
- ✅ Install LevLang via pip
- ✅ Verify the installation
- ✅ Show you next steps

**Note**: This requires the repo to be published on GitHub first!

---

## 📦 Method 2: pip install (Recommended)

**After publishing to PyPI:**

```bash
pip install levlang
```

Or with pip3:

```bash
pip3 install levlang
```

**Upgrade to latest version:**

```bash
pip install --upgrade levlang
```

---

## 💻 Method 3: Install from Source

**Clone and install:**

```bash
git clone https://github.com/sriramramnath/language.git
cd language
pip install -e .
```

The `-e` flag installs in "editable" mode - changes to the code take effect immediately.

**Without editable mode:**

```bash
pip install .
```

---

## 🌐 Method 4: Direct Download from PyPI (After Publishing)

**Download the wheel file directly:**

```bash
# Get the latest version number from https://pypi.org/project/levlang/
VERSION="0.1.0"

# Download the wheel
curl -O https://files.pythonhosted.org/packages/py3/l/levlang/levlang-${VERSION}-py3-none-any.whl

# Install it
pip install levlang-${VERSION}-py3-none-any.whl
```

**Or download the source tarball:**

```bash
curl -O https://files.pythonhosted.org/packages/source/l/levlang/levlang-${VERSION}.tar.gz
pip install levlang-${VERSION}.tar.gz
```

---

## 🐍 Method 5: Python Module Installation

**If `levlang` command doesn't work, you can run it as a Python module:**

```bash
python3 -m pip install levlang
python3 -m levlang.cli.main --version
```

---

## 🔧 Method 6: Virtual Environment (Recommended for Development)

**Create an isolated environment:**

```bash
# Create virtual environment
python3 -m venv levlang-env

# Activate it
source levlang-env/bin/activate  # On macOS/Linux
# or
levlang-env\Scripts\activate     # On Windows

# Install LevLang
pip install levlang

# Use it
levlang --version

# Deactivate when done
deactivate
```

---

## 📋 Verification

**After installation, verify it works:**

```bash
# Check version
levlang --version

# Get help
levlang --help

# Create a test file
echo 'game "Test"' > test.lvl
echo 'start()' >> test.lvl

# Try to transpile
levlang transpile test.lvl
```

---

## 🌍 Platform-Specific Instructions

### macOS

```bash
# Install Python (if needed)
brew install python3

# Install LevLang
pip3 install levlang
```

### Linux (Ubuntu/Debian)

```bash
# Install Python (if needed)
sudo apt update
sudo apt install python3 python3-pip

# Install LevLang
pip3 install levlang
```

### Windows

```powershell
# Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation

# Install LevLang
pip install levlang
```

---

## 🆘 Troubleshooting

### Command not found after installation

**The issue:** `levlang: command not found`

**Solutions:**

1. **Try running as a Python module:**
   ```bash
   python3 -m levlang.cli.main --version
   ```

2. **Add pip's bin directory to PATH:**
   ```bash
   # Find where pip installs scripts
   python3 -m site --user-base
   
   # Add to your ~/.bashrc or ~/.zshrc:
   export PATH="$HOME/.local/bin:$PATH"
   
   # Reload shell config
   source ~/.bashrc  # or source ~/.zshrc
   ```

3. **Install with --user flag:**
   ```bash
   pip install --user levlang
   ```

### Permission denied

**The issue:** Permission errors during installation

**Solution:** Use `--user` flag or virtual environment:

```bash
pip install --user levlang
```

### Python version too old

**The issue:** `ERROR: Package requires Python >=3.8`

**Solution:** Upgrade Python:

```bash
# macOS
brew upgrade python3

# Ubuntu/Debian
sudo apt install python3.9  # or higher
```

---

## 🎯 Quick Summary

| Method | Command | Best For |
|--------|---------|----------|
| **curl** | `curl -sSL https://...` | Quick one-liner installs |
| **pip** | `pip install levlang` | Most users (after PyPI publish) |
| **Source** | `git clone && pip install -e .` | Developers, contributors |
| **Direct** | `curl -O https://files.pythonhosted.org/...` | Offline installs, specific versions |
| **venv** | `python3 -m venv && pip install` | Isolated environments |

---

## 📝 Next Steps After Installation

1. **Verify installation:**
   ```bash
   levlang --version
   ```

2. **Create your first game:**
   ```bash
   echo 'game "My First Game"' > mygame.lvl
   echo 'player { speed: 5 }' >> mygame.lvl
   echo 'start()' >> mygame.lvl
   ```

3. **Run it:**
   ```bash
   levlang run mygame.lvl
   ```

4. **Try the example:**
   ```bash
   levlang run useableexamples/pygame_example.lvl
   ```

---

## 🔄 Updating LevLang

**To update to the latest version:**

```bash
pip install --upgrade levlang
```

**To install a specific version:**

```bash
pip install levlang==0.2.0
```

**To uninstall:**

```bash
pip uninstall levlang
```

---

**Need help?** Open an issue: https://github.com/sriramramnath/language/issues

