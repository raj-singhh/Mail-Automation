# SETUP INSTRUCTIONS - Mail Automation Tool

## 📦 What Has Been Created

Your complete mail automation tool with:
- ✅ Desktop GUI application (PyQt5)
- ✅ Chrome automation tools (Selenium)
- ✅ Email personalization system
- ✅ Resume attachment support
- ✅ Email preview & review system
- ✅ Complete documentation

## 🚀 5-MINUTE QUICK START

### Step 1: Install Python Packages (2 minutes)

Open Command Prompt and run:
```bash
cd "G:\WEB DEVELOPMENT\mail-automation"
pip install -r requirements.txt
```

Or simply double-click: **install.bat**

### Step 2: Download ChromeDriver (1 minute)

1. **Find your Chrome version:**
   - Open Chrome → Click ⋮ (three dots) at top right
   - Select "Help" → "About Google Chrome"
   - Note the version number (e.g., `120.0.6099.00`)

2. **Download ChromeDriver:**
   - Visit: https://googlechromelabs.github.io/chrome-for-testing/
   - Find your version and download `chromedriver.exe`
   - Extract it to: `G:\WEB DEVELOPMENT\mail-automation\`

3. **Verify:**
   - Open Command Prompt in the folder
   - **Windows PowerShell**: Type `.\chromedriver --version`
   - **Command Prompt/CMD**: Type `chromedriver --version`
   - Should show: `ChromeDriver X.X.X.X`

### Step 3: Login to Gmail (1 minute)

1. Open Google Chrome
2. Go to https://gmail.com
3. Login with your email account
4. **Keep this window open** - the tool uses this session

### Step 4: Run the Application (1 minute)

**Windows:**
- Double-click: **run.bat** OR
- In Command Prompt: `python main.py`

**Mac/Linux:**
- In Terminal: `python3 main.py`

## 📋 USING THE TOOL

### Complete Workflow:

1. **Enter Email Addresses**
   - Paste one per line or comma-separated
   - Example:
     ```
     john.doe@company.com
     jane.smith@company.com
     mike@example.com
     ```

2. **Enter Subject**
   - Same subject for all emails
   - Example: "Job Application - Software Engineer"

3. **Write Email Body**
   - Write your message
   - Names will be auto-added to greeting!
   - Example:
     ```
     I am writing to express my interest in the position.
     
     With my 5 years of experience...
     
     Thank you for your time.
     ```
   - **Result:** Each recipient gets:
     - john.doe → "Dear John Doe, I am writing..."
     - jane.smith → "Dear Jane Smith, I am writing..."

4. **Select Resume (Optional)**
   - Click "Browse"
   - Select your resume/CV file (PDF, DOCX, etc.)

5. **Click "Preview Emails"**
   - Review the table showing all emails
   - Each email shows personalized content

6. **Make Changes (If Needed)**
   - Edit any of the inputs (emails, subject, body)
   - Click "Preview Emails" again

7. **Click "Send All Emails"**
   - Confirm the action
   - Tool opens Chrome and sends emails automatically
   - Watch the progress bar

## 🎯 FEATURES IN DETAIL

### ✅ Auto Name Extraction
Your tool intelligently extracts names from emails:
- `john.doe@gmail.com` → "Dear John Doe,"
- `jane_smith@company.com` → "Dear Jane Smith,"
- `m.johnson@example.com` → "Dear M Johnson,"

### ✅ Email Preview
Before sending, you see:
- Recipient email address
- Email subject
- Full personalized body

### ✅ Attachment Support
- Upload resume/CV with each email
- Automatically attached to all emails
- Supports: PDF, DOCX, DOC, PPTX, TXT

### ✅ Chrome Automation
- Uses your real Gmail account
- Sends from your email address
- Appears as sent by you
- All emails from your inbox

### ✅ Email Review
- Change emails before sending
- Edit inputs and click Preview again
- Full control over content

## 📁 PROJECT STRUCTURE

```
mail-automation/
├── main.py                 ← Main application (run this!)
├── email_utils.py          ← Email utilities
├── chrome_handler.py       ← Chrome automation
├── email_templates/        ← Sample templates
│   └── sample_job_application_template.txt
├── config/
│   └── config.ini         ← Settings
├── logs/                   ← Application logs
└── [Setup files]
    ├── install.bat         ← Auto installer
    ├── run.bat             ← Quick launcher
    ├── setup.py            ← Setup wizard
    ├── test_tool.py        ← Test suite
    └── check_setup.py      ← Verify setup
```

## ⚠️ IMPORTANT NOTES

✓ **Gmail must be open and logged in** - The tool uses your Chrome's Gmail session
✓ **Don't close Chrome while sending** - Let it complete automatically
✓ **First test with 1-2 emails** - Make sure everything works
✓ **Batch size recommendation** - Send 20-30 per batch (avoid rate limiting)
✓ **Check logs if errors** - Logs saved in `logs/mail_automation.log`

## 🔧 TROUBLESHOOTING

### "Chrome not found"
- Make sure Chrome is installed
- Run: `check_setup.py` to diagnose

### "ChromeDriver version mismatch"
- Check your Chrome version
- Download matching ChromeDriver
- Replace in the folder

### "Gmail didn't load"
- Login to Gmail manually in Chrome
- Make sure you're on the correct profile
- Check internet connection

### "Emails not sending"
- Look in `logs/mail_automation.log`
- Check that Gmail interface is accessible
- Try refreshing Gmail manually

### "Module not found error"
- Run: `pip install -r requirements.txt`
- Or: double-click `install.bat`

## 📚 DOCUMENTATION

| File | Purpose |
|------|---------|
| README.md | Complete documentation |
| QUICKSTART.md | Quick start guide |
| START_HERE.md | Overview & features |
| SETUP_INSTRUCTIONS.md | This file |

## 🧪 TEST YOUR SETUP

Before sending real emails, run:
```bash
python test_tool.py
```

This will test:
- Name extraction
- Email parsing
- Email formatting
- Chrome connection (optional)

## 📞 COMMON QUESTIONS

**Q: Will people know emails are automated?**
A: No! It's sent from your real Gmail account, looks completely normal.

**Q: Can I send to different emails with different messages?**
A: Currently the body is the same for all (with personalized greetings). You can manually edit after preview.

**Q: What if Gmail updates its interface?**
A: The tool might need XPath updates in `chrome_handler.py`. Contact support or update selectors.

**Q: Can emails be scheduled?**
A: Currently sends immediately. You can modify to add scheduling in `main.py`.

**Q: Is my password stored?**
A: No! Uses Chrome's existing Gmail session. No passwords saved.

## 🎓 NEXT STEPS

1. ✅ Run `setup.py` (interactive setup)
2. ✅ Run `test_tool.py` (verify everything)
3. ✅ Open the application: `main.py`
4. ✅ Test with 1-2 emails first
5. ✅ Send to your full list

## 📧 EMAIL TEMPLATE

Use the sample template in `email_templates/sample_job_application_template.txt` as a starting point.

---

**Version**: 1.0.0  
**Status**: Ready to Use ✓  
**Last Updated**: March 2026

**Happy mailing! 🚀**
