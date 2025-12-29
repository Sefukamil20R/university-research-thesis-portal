# ⚡ Quick Start Guide

## Step 1: Create Your .env File

**Location:** Place `.env` file in the **root directory** (same folder as `main.py`)

**Quick command:**
```bash
# Windows:
copy env.example .env

# Then edit .env with a text editor
notepad .env
```

## Step 2: Fill In Your .env File

### ✅ MINIMUM REQUIRED (just this one!):

```env
DATABASE_URL=your-neon-connection-string-here
```

**Where to get DATABASE_URL:**
1. Go to https://console.neon.tech
2. Select your database
3. Copy the connection string from "Connection Details"
4. It looks like: `postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname`

### 🔐 RECOMMENDED (add this for security):

```env
DATABASE_URL=your-neon-connection-string-here
SECRET_KEY=generate-a-random-key-here
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as your `SECRET_KEY` value.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Initialize Database

```bash
python scripts/init_db.py
```

This creates tables and adds default roles/departments.

## Step 5: Run the Application

```bash
python main.py
```

Then open: http://localhost:8000

---

**That's it!** See `SETUP_ENV.md` for detailed explanations.

