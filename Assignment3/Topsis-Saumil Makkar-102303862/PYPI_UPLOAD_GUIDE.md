# Step-by-Step Guide: Upload Your TOPSIS Package to PyPI

## ⚠️ IMPORTANT: What You Need to Change

Before uploading, you MUST replace **one thing**:

### In These 4 Files:

1. **setup.py** (line 7)
2. **pyproject.toml** (line 6) 
3. **README.md** (line 1)
4. **topsis/__init__.py** (comments)

**FIND:** `Topsis-Saumil-YourRoll`
**REPLACE WITH:** `Topsis-Saumil-102203123` (your actual roll number)

**Example:** If your roll number is 102203456:
- Change to: `Topsis-Saumil-102203456`

### Also Update Your Email (Optional but Recommended):

**FIND:** `saumil.makkar@example.com`
**REPLACE WITH:** Your real email (e.g., `saumil@thapar.edu`)

In files:
- setup.py (line 9)
- pyproject.toml (line 13)
- topsis/__init__.py (line 20)

---

## Prerequisites

- Python 3.7 or higher installed
- A PyPI account → https://pypi.org/account/register/
- A TestPyPI account (optional) → https://test.pypi.org/account/register/

---

## Step 1: Install Required Tools

```bash
pip install --upgrade pip setuptools wheel twine
```

---

## Step 2: Navigate to Your Package

```bash
cd Topsis-Saumil-YourRoll
```

---

## Step 3: Build the Package

```bash
# Clean any previous builds
rm -rf build/ dist/ *.egg-info/
# On Windows: rmdir /s build dist *.egg-info

# Build distributions
python setup.py sdist bdist_wheel
```

You should see:
```
running sdist
running bdist_wheel
```

This creates:
- `dist/Topsis_Saumil_YourRoll-1.0.0-py3-none-any.whl`
- `dist/Topsis-Saumil-YourRoll-1.0.0.tar.gz`

---

## Step 4: Verify the Build

```bash
twine check dist/*
```

Expected output:
```
Checking dist/Topsis_Saumil_YourRoll-1.0.0-py3-none-any.whl: PASSED
Checking dist/Topsis-Saumil-YourRoll-1.0.0.tar.gz: PASSED
```

---

## Step 5: Get Your PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click **"Add API token"**
3. Token name: `TOPSIS Package`
4. Scope: `Entire account` (or specific to this project after first upload)
5. **Copy the token** (starts with `pypi-...`)

⚠️ **IMPORTANT**: Save this token! You won't see it again.

---

## Step 6: Configure PyPI Credentials

Create or edit `~/.pypirc`:

**On Windows:** `C:\Users\YourUsername\.pypirc`
**On Mac/Linux:** `~/.pypirc`

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_ACTUAL_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```

Replace `pypi-YOUR_ACTUAL_TOKEN_HERE` with your actual token!

---

## Step 7: Upload to PyPI

```bash
twine upload dist/*
```

You'll see:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading Topsis_Saumil_YourRoll-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━ 15.2/15.2 kB
Uploading Topsis-Saumil-YourRoll-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━ 12.1/12.1 kB

View at:
https://pypi.org/project/Topsis-Saumil-YourRoll/1.0.0/
```

🎉 **Success! Your package is now on PyPI!**

---

## Step 8: Test Installation

Open a **NEW terminal** (or create a virtual environment):

```bash
# Create fresh environment
python -m venv test_env

# Activate
# Windows:
test_env\Scripts\activate
# Mac/Linux:
source test_env/bin/activate

# Install your package
pip install Topsis-Saumil-YourRoll

# Test it
topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv

# Check output
cat result.csv
```

✅ If it works, you're done!

---

## Common Errors & Solutions

### Error: "Package name already exists"
**Solution:** Someone already used that name. Change your roll number in the package name.
```python
# In all 4 files, change:
Topsis-Saumil-102203456 → Topsis-Saumil-102203456-v2
```

### Error: "Invalid credentials"
**Solution:** Check your `~/.pypirc` file:
- Token must start with `pypi-`
- No extra spaces
- Username must be `__token__` (with two underscores)

### Error: "File already exists"
**Solution:** You can't re-upload the same version. Either:
- Increment version: `1.0.0` → `1.0.1`
- Delete from PyPI and re-upload (need to wait 24 hours)

### Error: "HTTPError: 403 Forbidden"
**Solution:** 
- Your token doesn't have upload permissions
- Create a new token with proper scope

---

## Updating Your Package (Future Versions)

When you need to update:

### Step 1: Update Version Number

In **3 files**:
- `setup.py` → `version="1.0.1"`
- `pyproject.toml` → `version = "1.0.1"`
- `topsis/__init__.py` → `__version__ = "1.0.1"`

### Step 2: Rebuild and Upload

```bash
rm -rf build/ dist/ *.egg-info/
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## Quick Command Reference

```bash
# Build
python setup.py sdist bdist_wheel

# Check
twine check dist/*

# Upload
twine upload dist/*

# Test install
pip install Topsis-Saumil-YourRoll

# Uninstall
pip uninstall Topsis-Saumil-YourRoll
```

---

## Assignment Submission Checklist

✅ Roll number updated in package name  
✅ Package uploaded to PyPI  
✅ Can install via `pip install`  
✅ Command `topsis` works  
✅ README visible on PyPI page  
✅ Screenshot of PyPI page  
✅ Screenshot of installation  
✅ Screenshot of command execution  

---

## Your Package URL

After upload, your package will be at:
```
https://pypi.org/project/Topsis-Saumil-YourRoll/
```

Replace `YourRoll` with your actual roll number!

---

## Need Help?

- PyPI Documentation: https://packaging.python.org
- Twine Documentation: https://twine.readthedocs.io
- Your GitHub: https://github.com/SaumilMakkar/UCS654

Good luck! 🚀
