# Mail Automation Tool

A powerful desktop application to automate email sending through Gmail. This tool allows you to send personalized emails to multiple recipients with automatic name extraction and file attachments.

## Features

✅ **Batch Email Sending** - Send emails to multiple recipients at once
✅ **Auto Name Extraction** - Automatically extracts names from email addresses for personalized greetings
✅ **Email Preview** - Review all emails before sending
✅ **Attachment Support** - Attach resume or other documents
✅ **Chrome Automation** - Uses your logged-in Gmail account for sending
✅ **Local Only** - Runs entirely on your system, no cloud storage
✅ **Easy to Use** - Simple, intuitive GUI interface
✅ **Logging** - Keeps logs of all sending activities

## System Requirements

- Windows 10 or later
- Python 3.7+
- Google Chrome browser
- Gmail account (logged in on Chrome)

## Installation

### Step 1: Install Python Dependencies

Open Command Prompt (Windows) and navigate to the project folder:

```bash
cd "G:\WEB DEVELOPMENT\mail-automation"
pip install -r requirements.txt
```

### Step 2: Download ChromeDriver

The tool uses Selenium to automate Chrome. You need to download ChromeDriver:

1. Check your Chrome version:
   - Open Chrome → Click ⋮ (Menu) → Help → About Google Chrome
   - Note your version (e.g., 120.0.6099.00)

2. Download ChromeDriver:
   - Visit: https://googlechromelabs.github.io/chrome-for-testing/
   - Or: https://chromedriver.chromium.org/
   - Download the version matching your Chrome version

3. Copy `chromedriver.exe` to your system PATH or the project folder

### Step 3: Verify Chrome Profile Path

The tool uses your Chrome user data directory. By default, it uses:
```
C:\Users\[YourUsername]\AppData\Local\Google\Chrome\User Data
```

Make sure you're logged into Gmail in your default Chrome profile.

## Usage

### Running the Application

```bash
python main.py
```

Or double-click `run.bat` (if present)

### Using the Tool

1. **Enter Email Addresses**
   - Paste recipient emails (comma or newline separated)
   - Example: `john@example.com, jane@example.com` or one per line

2. **Set Subject**
   - Type the email subject line

3. **Write Email Body**
   - Type the email content
   - Don't worry about greetings - the tool adds them automatically!
   - Example: "I am interested in the position..." 
   - Will become: "Dear John,\n\nI am interested in the position..."

4. **Select Attachment (Optional)**
   - Click "Browse" and select your resume (PDF, DOCX, etc.)

5. **Preview Emails**
   - Click "Preview Emails" button
   - Review the table showing:
     - Recipients
     - Subject
     - Email body with personalized greetings

6. **Make Changes (If Needed)**
   - Edit in the table or go back and modify inputs
   - Click "Preview Emails" again to update

7. **Send Emails**
   - Click "Send All Emails"
   - **IMPORTANT**: Make sure Gmail is open in Chrome
   - Confirm the action
   - The tool will:
     - Open Chrome (if needed)
     - Log into Gmail with your credentials
     - Compose emails one by one
     - Send each email automatically

## Important Notes

⚠️ **Before Sending:**
- Make sure you're logged into Gmail in Chrome
- The browser will open during sending - don't close it
- The tool sends emails one by one with delays to avoid getting blocked

🔐 **Security:**
- This tool runs entirely on your local machine
- Passwords are NOT stored
- Uses your Chrome's existing Gmail login session
- No data is sent to external servers

📝 **Email Personalization:**
The tool automatically extracts names from email addresses:
- `john.doe@gmail.com` → "Dear John Doe,"
- `jane_smith@company.com` → "Dear Jane Smith,"
- `jsmith@gmail.com` → "Dear J Smith,"

## Troubleshooting

### Chrome doesn't open
- Make sure Chrome is installed
- Try opening Chrome manually then running the tool

### Gmail doesn't load
- Make sure you're logged into Gmail in Chrome
- Try logging in again manually
- Check your internet connection

### Emails not sending
- Check the logs in `logs/mail_automation.log`
- Make sure the Gmail interface hasn't changed
- Try sending to one email first

### ChromeDriver issues
- Download the correct ChromeDriver version for your Chrome
- Add it to system PATH or put it in the project folder

## File Structure

```
mail-automation/
├── main.py                 # Main application
├── email_utils.py          # Email processing utilities
├── chrome_handler.py       # Chrome automation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── run.bat                # Quick start batch file
├── email_templates/       # (For future template storage)
├── config/                # Configuration files
└── logs/                  # Application logs
```

## Advanced Configuration

### Custom Chrome Profile

If you want to use a specific Chrome profile, edit `chrome_handler.py`:

```python
options.add_argument('user-data-dir=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data')
# or
options.add_argument('profile-directory=Profile 1')  # For specific profile
```

### Headless Mode (Run in background)

To run Chrome in the background (no window visible):

In `main.py`, find the EmailSenderThread and change:
```python
self.chrome_handler = ChromeEmailHandler(headless=True)
```

## Performance Tips

1. **Batch Size**: Sending 50+ emails at once might trigger Gmail's rate limiting. Recommended: 20-30 per batch.

2. **Delays**: The tool automatically adds delays between emails to avoid being flagged.

3. **Attachments**: Smaller attachments (< 5MB) process faster.

4. **Time of Day**: Send emails during normal hours to avoid spam filters.

## Support & Debugging

- Check `logs/mail_automation.log` for detailed error messages
- Verify all inputs are correct before sending
- Test with a single recipient first
- Make sure your internet connection is stable

## License

For personal use only. Do not use for spam or any illegal activities.

---

**Created**: March 2026
**Version**: 1.0.0
