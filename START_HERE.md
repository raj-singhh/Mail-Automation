# Mail Automation Tool

A complete email automation solution that runs locally on your Windows/Mac/Linux system.

## 🚀 Quick Start

### Windows Users:
```bash
# Step 1: Install dependencies
install.bat

# Step 2: Download ChromeDriver (match your Chrome version)
# https://googlechromelabs.github.io/chrome-for-testing/

# Step 3: Login to Gmail in Chrome

# Step 4: Run the tool
run.bat
```

### Mac/Linux Users:
```bash
chmod +x run.sh
./run.sh
```

## 📋 Features

✅ **Send Emails in Bulk** - Send to 30+ recipients at once
✅ **Auto Name Extraction** - Personalize emails automatically
✅ **Email Preview** - Review before sending
✅ **Attach Files** - Include resume or documents
✅ **Chrome Automation** - Uses your real Gmail account
✅ **Local Only** - No data sent anywhere
✅ **Easy GUI** - Beautiful, user-friendly interface

## 🛠️ Setup Verification

```bash
python check_setup.py
```

This will verify:
- Python version
- Chrome installation
- Required packages
- ChromeDriver availability
- Directory structure

## 📖 Usage Workflow

1. **Enter email addresses** (paste recipients)
2. **Write subject line** (same for all)
3. **Write email body** (auto-personalized for each recipient)
4. **Select resume** (optional attachment)
5. **Preview emails** (review personalized content)
6. **Edit if needed** (modify inputs and preview again)
7. **Send emails** (one click, all automated!)

## ⚙️ Configuration

Edit `config/config.ini` to customize:
- Delays between emails
- Gmail timeout settings
- Logging preferences
- File size limits

## 📝 Project Structure

```
mail-automation/
├── main.py                 # Main GUI application
├── email_utils.py          # Email processing
├── chrome_handler.py       # Chrome automation
├── check_setup.py          # Setup verification
├── requirements.txt        # Python dependencies
├── install.bat             # Windows installer
├── run.bat                 # Windows launcher
├── run.sh                  # Mac/Linux launcher
├── README.md               # Full documentation
├── QUICKSTART.md          # Quick start guide
├── config/
│   └── config.ini         # Configuration file
├── logs/                   # Application logs
└── email_templates/        # Template storage
```

## 🔧 Troubleshooting

### Chrome won't open
- Ensure Chrome is installed
- Try `check_setup.py` to diagnose

### Emails not sending
- Verify you're logged into Gmail
- Check `logs/mail_automation.log`
- Make sure ChromeDriver version matches Chrome

### ChromeDriver errors
- Download correct version from https://googlechromelabs.github.io/chrome-for-testing/
- Place in project folder or system PATH

## 💡 Pro Tips

1. **Batch Size**: Send 20-30 emails per batch
2. **Timing**: Avoid sending huge batches, space them out
3. **Testing**: Test with 1-2 emails first
4. **Gmail**: Keep Gmail logged in and window minimized

## 📦 System Requirements

- Python 3.7+
- Google Chrome
- 100 MB disk space
- Windows 10+, Mac OS 10.12+, or Linux

## 📄 License

For personal use only. Respect email regulations and anti-spam laws.

---

**Version**: 1.0.0  
**Created**: March 2026  
**Status**: Ready to Use ✓
