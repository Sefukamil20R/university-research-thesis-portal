# Environment Variables Setup Guide

## 📍 Where to Place the .env File

The `.env` file should be placed in the **root directory** of your project, at the same level as `main.py`.

```
university-research-thesis-portal/
├── .env                 ← PLACE IT HERE (same level as main.py)
├── main.py
├── database.py
├── requirements.txt
├── env.example
└── ...
```

## 🚀 Quick Setup Steps

1. **Copy the example file:**
   ```bash
   # Windows (PowerShell or Command Prompt):
   copy env.example .env
   
   # Or on Linux/Mac:
   cp env.example .env
   ```

2. **Edit the `.env` file** with your actual values (see below)

## 📝 Required Variables (MUST FILL IN)

### 1. DATABASE_URL ⚠️ REQUIRED
This is the **ONLY required** variable. Get it from your Neon PostgreSQL dashboard.

**How to get it:**
1. Go to [Neon Console](https://console.neon.tech)
2. Select your project/database
3. Click on "Connection Details" or "Connection String"
4. Copy the connection string

**Format:**
```
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**Example (yours will be different):**
```
DATABASE_URL=postgresql://myuser:mypass123@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Note:** If your connection string doesn't have `?sslmode=require`, the code will add it automatically.

---

## 🔐 Recommended Variables (IMPORTANT FOR SECURITY)

### 2. SECRET_KEY ⚠️ CHANGE FOR PRODUCTION
Used to sign JWT tokens. **You MUST change this for production!**

**How to generate a secure key:**
```bash
# Windows (PowerShell):
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Or use Python:
python -c "import secrets; print(secrets.token_hex(32))"

# Or use OpenSSL (if installed):
openssl rand -hex 32
```

**Example:**
```
SECRET_KEY=a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456
```

**Default value:** There's a default in the code for development, but **change it for any real use!**

---

## ⚙️ Optional Variables (Have Defaults)

These have default values, so you can leave them as-is for now:

### 3. ACCESS_TOKEN_EXPIRE_MINUTES
How long JWT tokens are valid (in minutes).

**Default:** `30` (30 minutes)

**Example:**
```
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. MAX_LOGIN_ATTEMPTS
Number of failed login attempts before account lockout.

**Default:** `5`

**Example:**
```
MAX_LOGIN_ATTEMPTS=5
```

### 5. LOCKOUT_DURATION_MINUTES
How long to lock an account after too many failed attempts (in minutes).

**Default:** `30` (30 minutes)

**Example:**
```
LOCKOUT_DURATION_MINUTES=30
```

---

## 📧 Email Variables (NOT USED YET - Placeholder)

These are placeholders for future email verification feature. You can ignore them for now:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Leave these as-is** or remove them - they won't affect the current system.

---

## ✅ Complete .env File Example

Here's what a minimal working `.env` file looks like:

```env
# REQUIRED - Get from Neon dashboard
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# RECOMMENDED - Generate a new one
SECRET_KEY=your-generated-secret-key-here-32-chars-minimum

# Optional (these are the defaults)
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
```

**Minimum to get started:** Just `DATABASE_URL` is enough! The rest have defaults.

---

## 🔍 How to Verify Your .env File

1. **Check the file exists:**
   ```bash
   # Windows:
   dir .env
   
   # Linux/Mac:
   ls -la .env
   ```

2. **Check the location:**
   - Should be in the same folder as `main.py`
   - Should NOT be in a subfolder

3. **Check the format:**
   - No quotes around values (unless the value itself contains spaces)
   - No spaces around the `=` sign
   - Each variable on its own line

**Correct:**
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=abc123
```

**Wrong:**
```
DATABASE_URL = "postgresql://user:pass@host/db"  ❌ (spaces and quotes)
DATABASE_URL=postgresql://user:pass@host/db SECRET_KEY=abc  ❌ (two on one line)
```

---

## 🚨 Common Issues

### "DATABASE_URL environment variable is not set"
- Make sure the file is named `.env` (with the dot at the start)
- Make sure it's in the root directory (same folder as `main.py`)
- Check for typos in the variable name

### "Could not connect to database"
- Check your `DATABASE_URL` is correct
- Make sure you copied the full connection string from Neon
- Verify SSL is enabled (`sslmode=require` in the URL)

---

## 📋 Quick Checklist

- [ ] Created `.env` file in root directory
- [ ] Added `DATABASE_URL` from Neon dashboard
- [ ] Generated and added `SECRET_KEY` (or using default for testing)
- [ ] File is named exactly `.env` (not `env.example` or `.env.txt`)
- [ ] No spaces around `=` signs
- [ ] Each variable on its own line

Once you complete these steps, you can run `python main.py` and it should connect to your database!

