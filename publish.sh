#!/bin/bash
# Quick publish script for LevLang

set -e  # Exit on error

echo "🚀 LevLang Publishing Script"
echo "=============================="
echo ""

# Check if build tools are installed
if ! command -v twine &> /dev/null; then
    echo "📦 Installing build tools..."
    pip install --upgrade build twine
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info levlang.egg-info/

# Run tests
echo "🧪 Running tests..."
if ! pytest tests/ -q; then
    echo "❌ Tests failed! Fix them before publishing."
    exit 1
fi

echo "✅ Tests passed!"
echo ""

# Ask for version
echo "Current version in pyproject.toml:"
grep "version = " pyproject.toml

echo ""
read -p "Is the version number correct? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "Please update version in pyproject.toml and setup.py, then run again."
    exit 0
fi

# Build
echo ""
echo "📦 Building distribution..."
python3 -m build

# Ask whether to upload to TestPyPI or PyPI
echo ""
echo "Where do you want to upload?"
echo "1) TestPyPI (test.pypi.org) - for testing"
echo "2) PyPI (pypi.org) - for real release"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "📤 Uploading to TestPyPI..."
    python3 -m twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Uploaded to TestPyPI!"
    echo "Test installation with:"
    echo "  pip install --index-url https://test.pypi.org/simple/ levlang"
elif [ "$choice" = "2" ]; then
    echo ""
    read -p "⚠️  This will publish to REAL PyPI. Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ Cancelled."
        exit 0
    fi
    
    echo ""
    echo "📤 Uploading to PyPI..."
    python3 -m twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo "Anyone can now install with:"
    echo "  pip install levlang"
else
    echo "❌ Invalid choice."
    exit 1
fi

echo ""
echo "🎉 Done!"

