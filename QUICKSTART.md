# Quick Start Guide for Mail Automation Tool

## First Time Setup (5 minutes)

### 1. Install Requirements
```bash
cd "G:\WEB DEVELOPMENT\mail-automation"
pip install -r requirements.txt
```

### 2. Download ChromeDriver
- Check Chrome version: Chrome Menu → Help → About Google Chrome
- Download matching version from: https://googlechromelabs.github.io/chrome-for-testing/
- Extract and place `chromedriver.exe` in the project folder OR add to system PATH

### 3. Login to Gmail
- Open Google Chrome
- Go to https://gmail.com
- Login with your email account
- **Keep this session active** - the tool uses this logged-in session

## Running the Tool

**Windows**: Double-click `run.bat` OR run in CMD:
```bash
python main.py
```

**Mac/Linux**: Run in terminal:
```bash
python3 main.py
```

## Complete Workflow Example

1. **Paste Emails**
   ```
   john.doe@gmail.com
   jane.smith@gmail.com
   mike.johnson@company.com
   ```

2. **Set Subject**
   ```
   Job Application - Software Engineer Position
   ```

3. **Write Body**
   ```
   I am writing to express my strong interest in the Software Engineer position at your organization.

   With my 5 years of experience in Python and JavaScript development, I believe I can make a significant contribution to your team.

   Please find my resume attached for your review.

   Thank you for considering my application.

   Best regards,
   [Your Name]
   ```

4. **Select Resume** → Browse and pick your CV/Resume file

5. **Click "Preview Emails"** → Review the table:
   - John receives: "Dear John Doe, I am writing..."
   - Jane receives: "Dear Jane Smith, I am writing..."
   - Mike receives: "Dear Mike Johnson, I am writing..."

6. **Make Edits** (if needed) → Modify inputs and click Preview again

7. **Click "Send All Emails"** → Confirm → Tool sends all emails!

## Important Reminders ⚠️

✓ Gmail MUST be open in Chrome and logged in
✓ Don't close Chrome while emails are being sent
✓ Tool automates the browser - you'll see it working
✓ Check logs if anything goes wrong: `logs/mail_automation.log`
✓ For best results, use 20-30 emails per batch

## If Something Goes Wrong

1. Check the log file: `logs/mail_automation.log`
2. Try refreshing Gmail manually
3. Test with one email first
4. Restart Chrome and try again
5. Check that ChromeDriver version matches Chrome version

---

**Version**: 1.0.0 | **Last Updated**: March 2026
