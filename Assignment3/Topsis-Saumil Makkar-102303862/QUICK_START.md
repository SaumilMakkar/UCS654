# Quick Start Guide - Saumil

## 🎯 Before You Start

**YOU MUST CHANGE ONE THING:**

Replace `YourRoll` with your actual roll number in these 4 files:

1. `setup.py` (line 7)
2. `pyproject.toml` (line 6)
3. `README.md` (line 1)
4. `topsis/__init__.py` (comments)

**Example:** If your roll is 102203456, change:
```
Topsis-Saumil-YourRoll → Topsis-Saumil-102203456
```

---

## 🚀 Quick Test (Before PyPI Upload)

### Step 1: Install Locally

```bash
cd Topsis-Saumil-YourRoll
pip install -e .
```

### Step 2: Test Command

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv
```

### Step 3: Check Output

```bash
cat result.csv
```

You should see 8 mutual funds with scores and ranks!

---

## 📦 Upload to PyPI

### Full Commands:

```bash
# 1. Install tools
pip install --upgrade pip setuptools wheel twine

# 2. Build
python setup.py sdist bdist_wheel

# 3. Check
twine check dist/*

# 4. Upload (you'll need PyPI account + token)
twine upload dist/*
```

See `PYPI_UPLOAD_GUIDE.md` for detailed instructions!

---

## ✅ After PyPI Upload

Test that it works:

```bash
# Fresh install
pip install Topsis-Saumil-YourRoll

# Test
topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv

# Success! 🎉
```

---

## 📸 Screenshots for Assignment

Take these screenshots:

1. **PyPI page:** https://pypi.org/project/Topsis-Saumil-YourRoll/
2. **Installation:** `pip install Topsis-Saumil-YourRoll`
3. **Command:** `topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv`
4. **Output:** `cat result.csv`

---

## 🔗 Your Links

- **PyPI Package:** https://pypi.org/project/Topsis-Saumil-YourRoll/
- **GitHub:** https://github.com/SaumilMakkar/UCS654
- **Notebook:** https://github.com/SaumilMakkar/UCS654/blob/main/Assignment3/Assignment3UCS654.ipynb

---

## ⚡ One-Liner (After roll number is updated)

```bash
pip install -e . && topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv && python setup.py sdist bdist_wheel && twine upload dist/*
```

Done! 🎉
