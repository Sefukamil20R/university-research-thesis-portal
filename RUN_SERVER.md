# 🚀 How to Run the Server and See Error Logs

## To See Error Messages:

**Run the server in the foreground** (not in background) so you can see the error logs:

### In PowerShell:
```powershell
python main.py
```

This will:
- Start the server on http://localhost:8000
- Show all error messages in the terminal
- Keep running until you press `Ctrl+C`

---

## What You'll See:

When you run `python main.py`, you should see output like:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**When you try to register**, if there's an error, you'll see it in the terminal:
- Database connection errors
- SQL errors
- Validation errors
- Any other exceptions

---

## Troubleshooting:

1. **Keep the terminal window open** - that's where errors appear
2. **Try registering again** - watch the terminal for error messages
3. **Copy the error message** - share it so we can fix the issue

---

## Quick Test:

1. Open a **NEW terminal/PowerShell window**
2. Navigate to your project:
   ```powershell
   cd C:\Users\Sefina\Desktop\University\university-research-thesis-portal
   ```
3. Run the server:
   ```powershell
   python main.py
   ```
4. **Keep this window open** and try registering from your browser
5. Watch the terminal for error messages!

---

**The server logs will show you exactly what's wrong!** 🔍

