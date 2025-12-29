# ✅ Next Steps - Setup Complete!

## Your .env File is Ready ✅

I can see your `.env` file exists and contains:
- ✅ DATABASE_URL (from Neon)
- ✅ SECRET_KEY (generated)
- ✅ Other default values

## 🚀 Installation Steps

### Step 1: Install Python Dependencies

Run this command to install all required packages:

```powershell
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- psycopg2-binary (PostgreSQL driver)
- bcrypt (password hashing)
- JWT libraries
- And other dependencies

**Expected output:** You'll see packages being installed. Wait until it completes.

---

### Step 2: Initialize the Database

After dependencies are installed, run this to create database tables and add default data:

```powershell
python scripts/init_db.py
```

**What this does:**
- Creates all database tables (users, roles, departments, theses)
- Adds default roles: student, advisor, department_head, admin
- Adds sample departments: Computer Science, Electrical Engineering, Mathematics, Physics

**Expected output:**
```
Initializing database...
Created role: student
Created role: advisor
Created role: department_head
Created role: admin
Created department: Computer Science (CS)
...
Database initialization complete!
```

---

### Step 3: Run the Application

Start the FastAPI server:

```powershell
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Step 4: Access the Application

Open your web browser and go to:

- **Main Page:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative Docs:** http://localhost:8000/redoc

---

## 🧪 Test the System

### Quick Test:

1. **Register a User:**
   - Go to http://localhost:8000/auth/register
   - Fill in: email, password (min 8 chars), select role, clearance level
   - Click "Register"

2. **Login:**
   - Go to http://localhost:8000/auth/login
   - Enter your email and password
   - You'll be redirected to the dashboard

3. **Test API:**
   - Go to http://localhost:8000/docs
   - Click "Authorize" button
   - Enter: `Bearer YOUR_JWT_TOKEN`
   - Try the endpoints!

---

## 🐛 Troubleshooting

### If Step 1 fails (pip install):
- Make sure Python 3.10+ is installed: `python --version`
- Try: `python -m pip install -r requirements.txt`
- If you get permission errors, use: `pip install -r requirements.txt --user`

### If Step 2 fails (database init):
- Check your `.env` file has correct `DATABASE_URL`
- Verify you can connect to Neon database
- Check internet connection
- Look at the error message - it will tell you what's wrong

### If Step 3 fails (running app):
- Make sure port 8000 is not in use
- Check for syntax errors (the error message will show)
- Verify all dependencies installed correctly

### Common Errors:

**"DATABASE_URL environment variable is not set"**
→ Make sure `.env` file exists in root directory (same folder as main.py)

**"Could not connect to database"**
→ Check your DATABASE_URL is correct
→ Verify Neon database is running
→ Check if your IP is allowed (Neon should allow all by default)

**"ModuleNotFoundError: No module named 'fastapi'"**
→ Run `pip install -r requirements.txt` again

---

## 📋 Complete Command Sequence

Copy and paste these commands one by one:

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python scripts/init_db.py

# 3. Run the application
python main.py
```

Then open http://localhost:8000 in your browser!

---

**You're all set! 🎉** Once you run these commands, your University Research Thesis Portal will be up and running!

