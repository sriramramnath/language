# Publishing LevLang to PyPI

This guide walks you through publishing LevLang to the Python Package Index (PyPI) so anyone can install it with `pip install levlang`.

## Prerequisites

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Create an account
   - Verify your email

2. **Create API Token**
   - Go to https://pypi.org/manage/account/
   - Scroll to "API tokens"
   - Click "Add API token"
   - Name it "levlang" and set scope to "Entire account"
   - **SAVE THE TOKEN** - you won't see it again!

## Step-by-Step Publishing

### 1. Install Build Tools

```bash
pip install --upgrade build twine
```

### 2. Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info
```

### 3. Update Version Number

Edit `pyproject.toml` and increment the version:

```toml
version = "0.1.0"  # Change to 0.1.1, 0.2.0, etc.
```

Also update `setup.py` if you're using it:

```python
version="0.1.0",  # Change to match pyproject.toml
```

### 4. Build the Distribution

```bash
python -m build
```

This creates two files in the `dist/` directory:
- `levlang-0.1.0.tar.gz` (source distribution)
- `levlang-0.1.0-py3-none-any.whl` (wheel distribution)

### 5. Test on TestPyPI (Optional but Recommended)

First time only - register on https://test.pypi.org/

Upload to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ levlang
```

### 6. Upload to PyPI

```bash
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your API token, including the `pypi-` prefix)

### 7. Verify Installation

```bash
pip install levlang
levlang --version
```

## Using GitHub Actions (Automated Publishing)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

To use this:
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add a new secret named `PYPI_API_TOKEN` with your PyPI API token
3. Create a new release on GitHub, and it will automatically publish

## Creating a GitHub Release

1. **Commit and Push Changes**
   ```bash
   git add .
   git commit -m "Release v0.1.0"
   git push origin main
   ```

2. **Create a Git Tag**
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

3. **Create Release on GitHub**
   - Go to your repo on GitHub
   - Click "Releases" → "Create a new release"
   - Select your tag (v0.1.0)
   - Add release notes
   - Click "Publish release"

## Version Numbering Guide

Use [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.1.1): Bug fixes

## Checklist Before Publishing

- [ ] All tests pass (`pytest tests/`)
- [ ] README.md is up to date
- [ ] CHANGELOG.md documents changes
- [ ] Version number updated in `pyproject.toml` and `setup.py`
- [ ] LICENSE file exists
- [ ] `.gitignore` excludes build artifacts
- [ ] Tested installation from TestPyPI

## After Publishing

1. **Test Installation**
   ```bash
   pip install levlang
   levlang --version
   ```

2. **Announce**
   - Update GitHub README with installation instructions
   - Share on social media
   - Submit to Python Weekly, r/Python, etc.

3. **Monitor**
   - Check https://pypi.org/project/levlang/ for download stats
   - Watch for issues on GitHub

## Updating After Initial Release

1. Make changes to code
2. Update version number
3. Update CHANGELOG.md
4. Build: `python -m build`
5. Upload: `python -m twine upload dist/*`

## Troubleshooting

### Error: File already exists

You can't overwrite a version on PyPI. Increment the version number and rebuild.

### Error: Invalid username/password

Make sure you're using `__token__` as username and your full API token as password.

### Missing files in package

Update `MANIFEST.in` to include any missing files.

### Import errors after installation

Make sure `__init__.py` files exist in all package directories.

## Resources

- PyPI: https://pypi.org/
- Python Packaging Guide: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
- Setuptools Documentation: https://setuptools.pypa.io/

