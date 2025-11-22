# LevLang Distribution Quick Start

## 🎯 Goal
Make LevLang downloadable for anyone via `pip install levlang`

## ⚡ Quick Steps

### Option 1: Automated Script (Easiest)

```bash
./publish.sh
```

This script will:
1. ✅ Run tests
2. 📦 Build the package
3. 📤 Upload to PyPI or TestPyPI

### Option 2: Manual Publishing

```bash
# 1. Install tools
pip install --upgrade build twine

# 2. Clean old builds
rm -rf dist/ build/ *.egg-info

# 3. Build
python -m build

# 4. Upload to PyPI
python -m twine upload dist/*
```

## 📋 Before First Publish

### 1. Create PyPI Account
- Go to https://pypi.org/account/register/
- Verify your email

### 2. Get API Token
- Visit https://pypi.org/manage/account/
- Create API token
- Save it somewhere safe!

### 3. Configure Twine (Optional)
Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
```

## 🧪 Test First (Recommended)

Before publishing to real PyPI, test on TestPyPI:

```bash
# Upload to test
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ levlang
```

## 📊 Current Status

Your package is ready! Here's what's set up:

✅ `pyproject.toml` - Package metadata  
✅ `setup.py` - Installation script  
✅ `README.md` - Package description  
✅ `LICENSE` - MIT License  
✅ `MANIFEST.in` - Include extra files  
✅ `.gitignore` - Exclude build artifacts  
✅ `publish.sh` - Automated publish script  

## 🚀 Publishing Checklist

- [ ] Update version in `pyproject.toml` (e.g., `0.1.0` → `0.1.1`)
- [ ] Update version in `setup.py`
- [ ] Run tests: `pytest tests/`
- [ ] Build: `python -m build`
- [ ] Upload: `python -m twine upload dist/*`
- [ ] Test install: `pip install levlang`

## 📦 After Publishing

Once published, anyone can install with:

```bash
pip install levlang
```

Check your package at:
- https://pypi.org/project/levlang/

## 🔄 Updating

To release a new version:

1. Make code changes
2. Increment version number
3. Run `./publish.sh` or manual steps

**Note**: You cannot republish the same version number!

## 🆘 Need Help?

See `PUBLISHING_GUIDE.md` for detailed instructions.

## 📈 Version Numbers

Use [Semantic Versioning](https://semver.org/):

- `0.1.0` → `0.1.1` - Bug fix
- `0.1.0` → `0.2.0` - New feature
- `0.1.0` → `1.0.0` - Breaking change

## 🎉 Ready to Publish?

```bash
# Run the automated script
./publish.sh

# Or do it manually
python -m build
python -m twine upload dist/*
```

That's it! Your package will be live on PyPI! 🚀

