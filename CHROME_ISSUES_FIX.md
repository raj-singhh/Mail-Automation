# ⚠️ Chrome Startup Issues - Solution Guide

If you're getting "failed to start chrome" error, follow these steps:

## Quick Fix (Try This First)

1. **Close ALL Chrome windows** - including any in the background
   - Open Task Manager (Ctrl+Shift+Esc)
   - End all "chrome.exe" processes
   - Close Task Manager

2. **Verify Chrome is properly installed:**
   ```
   python diagnose_chrome.py
   ```
   - All checks should show ✓

3. **Run the troubleshooting tool:**
   ```
   python troubleshoot_chrome.py
   ```
   - This will identify what's wrong
   - Follow the solutions provided

4. **Try the GUI again:**
   ```
   python main_tkinter.py
   ```

5. **Use the "Test Chrome" button:**
   - Click the blue "Test Chrome" button in the GUI
   - This will test Chrome without sending emails
   - Shows detailed error messages

## How to Use the GUI

Once Chrome is working:

1. **Click "Test Chrome"** first - verify everything works
2. **Enter email addresses** (comma or line separated)
3. **Write subject and body** (names auto-personalized)
4. **Click "Preview Emails"** - review before sending
5. **Click "Send All Emails"** - to send batch

## If Problem Persists

Check the logs:
```
notepad logs/mail_automation.log
```

Common issues:
- ❌ **"Chrome not found"** → Install from https://google.com/chrome
- ❌ **"ChromeDriver not found"** → Download from https://googlechromelabs.github.io/chrome-for-testing/ (version 146)
- ❌ **"Chrome already running"** → Close all Chrome windows
- ❌ **"Gmail didn't load"** → Make sure you're logged in to Gmail in Chrome

## Still Stuck?

1. Make sure you opened Chrome **at least once** and logged into Gmail
2. Click "Test Chrome" button in GUI to see specific error
3. Check `logs/mail_automation.log` for detailed messages
4. Run `python troubleshoot_chrome.py` for complete diagnostic
