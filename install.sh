#!/bin/bash
# LevLang Quick Installer
# Usage: curl -sSL https://raw.githubusercontent.com/sriramramnath/language/main/install.sh | bash

set -e

echo "🚀 Installing LevLang..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher first:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - Windows: https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "Please install pip first"
    exit 1
fi

# Determine pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

# Install LevLang
echo "📦 Installing levlang package..."
$PIP_CMD install levlang

# Verify installation
if command -v levlang &> /dev/null; then
    echo ""
    echo "✅ LevLang installed successfully!"
    echo ""
    levlang --version
    echo ""
    echo "Try it out:"
    echo "  levlang --help"
    echo ""
    echo "Create your first game:"
    echo "  echo 'game \"My Game\"' > game.lvl"
    echo "  echo 'start()' >> game.lvl"
    echo "  levlang run game.lvl"
else
    echo ""
    echo "⚠️  Installation completed but 'levlang' command not found."
    echo "You may need to add pip's bin directory to your PATH."
    echo ""
    echo "Try running:"
    echo "  python3 -m levlang.cli.main --version"
fi

