"""
Mail Automation Tool - Main Application (tkinter version)
Desktop application to automate email sending through Gmail
Compatible with Python 3.7+
"""
import sys
import os
import logging
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from email_utils import parse_email_list, extract_name_from_email, format_email_body
from chrome_handler import ChromeEmailHandler

# Configure logging
logging.basicConfig(
    filename='logs/mail_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MailAutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mail Automation Tool")
        self.geometry("1100x750")
        self.configure(bg="#f5f5f5")
        
        # Data storage
        self.emails_list = []
        self.emails_data = []
        self.resume_path = None
        self.sender_thread = None
        
        # Create UI
        self.create_ui()
        logger.info("Application started")
    
    def create_ui(self):
        """Create the main user interface"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = ttk.Label(main_frame, text="Mail Automation Tool", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Create PanedWindow for left and right sections
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # Email IDs
        ttk.Label(left_frame, text="Email IDs (comma or line separated):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.email_input = scrolledtext.ScrolledText(left_frame, height=5, width=40, wrap=tk.WORD)
        self.email_input.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        # Subject
        ttk.Label(left_frame, text="Email Subject:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.subject_input = ttk.Entry(left_frame, width=40)
        self.subject_input.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        # Body
        ttk.Label(left_frame, text="Email Body:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.body_input = scrolledtext.ScrolledText(left_frame, height=8, width=40, wrap=tk.WORD)
        self.body_input.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        # Resume
        ttk.Label(left_frame, text="Attachment (Resume/CV):", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        resume_frame = ttk.Frame(left_frame)
        resume_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        self.resume_label = ttk.Label(resume_frame, text="No file selected", foreground="gray")
        self.resume_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(resume_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Buttons frame
        button1_frame = ttk.Frame(left_frame)
        button1_frame.pack(fill=tk.X, padx=0, pady=(0, 5))
        
        test_chrome_btn = ttk.Button(button1_frame, text="Test Chrome", command=self.test_chrome)
        test_chrome_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Preview button
        preview_btn = ttk.Button(button1_frame, text="Preview Emails", command=self.preview_emails)
        preview_btn.pack(side=tk.LEFT)
        
        # Right panel
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="Email Preview", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Preview table (using Text widget)
        self.preview_text = scrolledtext.ScrolledText(right_frame, height=20, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(right_frame, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=0, pady=(0, 5))
        self.progress_bar.pack_forget()
        
        # Status label
        self.status_label = ttk.Label(right_frame, text="", foreground="blue")
        self.status_label.pack(anchor=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, padx=0, pady=(10, 0))
        
        self.send_btn = ttk.Button(button_frame, text="Send All Emails", command=self.send_all_emails, state=tk.DISABLED)
        self.send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT)
    
    def test_chrome(self):
        """Test Chrome connection"""
        self.status_label.config(text="Testing Chrome connection...", foreground="blue")
        self.progress_bar.pack(fill=tk.X, padx=0, pady=(0, 5))
        self.progress_var.set(0)
        self.update()
        
        # Run test in separate thread
        test_thread = threading.Thread(target=self._test_chrome_thread)
        test_thread.daemon = True
        test_thread.start()
    
    def _test_chrome_thread(self):
        """Test Chrome in separate thread"""
        try:
            self.status_label.config(text="Starting Chrome...", foreground="blue")
            self.update()
            
            handler = ChromeEmailHandler()
            self.progress_var.set(25)
            self.update()
            
            if not handler.start_chrome():
                self.status_label.config(
                    text="❌ Failed to start Chrome. Check logs for details.",
                    foreground="red"
                )
                self.progress_bar.pack_forget()
                self.update()
                return
            
            self.status_label.config(text="Chrome started! Waiting for Gmail to load...", foreground="blue")
            self.progress_var.set(50)
            self.update()
            
            if not handler.wait_for_gmail_load():
                handler.close()
                self.status_label.config(
                    text="⚠️  Gmail didn't load. Make sure you're logged in!",
                    foreground="orange"
                )
                self.progress_bar.pack_forget()
                self.update()
                return
            
            self.status_label.config(
                text="✓ Chrome and Gmail working! Ready to send emails.",
                foreground="green"
            )
            self.progress_var.set(100)
            self.update()
            
            messagebox.showinfo(
                "Success",
                "✓ Chrome is working correctly!\n\nGmail is loaded and ready.\n\nYou can now send emails."
            )
            
            handler.close()
            
        except Exception as e:
            error_msg = str(e)
            self.status_label.config(
                text=f"❌ Error: {error_msg[:50]}...",
                foreground="red"
            )
            logger.error(f"Chrome test error: {error_msg}")
            messagebox.showerror(
                "Chrome Error",
                f"Failed to test Chrome:\n\n{error_msg}\n\nCheck logs/mail_automation.log for details"
            )
        finally:
            self.progress_bar.pack_forget()
    
    def browse_file(self):
        """Browse and select resume file"""
        file_path = filedialog.askopenfilename(
            title="Select Resume/CV",
            filetypes=[("PDF Files", "*.pdf"), ("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.resume_path = file_path
            self.resume_label.config(text=f"Selected: {Path(file_path).name}")
            logger.info(f"Resume selected: {file_path}")
    
    def preview_emails(self):
        """Validate input and show email preview"""
        email_input = self.email_input.get("1.0", tk.END).strip()
        subject = self.subject_input.get().strip()
        body = self.body_input.get("1.0", tk.END).strip()
        
        if not email_input:
            messagebox.showwarning("Input Error", "Please enter at least one email address.")
            return
        
        if not subject:
            messagebox.showwarning("Input Error", "Please enter email subject.")
            return
        
        if not body:
            messagebox.showwarning("Input Error", "Please enter email body.")
            return
        
        # Parse emails
        self.emails_list = parse_email_list(email_input)
        
        if not self.emails_list:
            messagebox.showwarning("Input Error", "No valid email addresses found.")
            return
        
        # Create formatted emails
        self.emails_data = []
        for email in self.emails_list:
            personalized_body = format_email_body(body, email)
            self.emails_data.append({
                'email': email,
                'subject': subject,
                'body': personalized_body
            })
        
        # Display preview
        self.display_preview()
        self.send_btn.config(state=tk.NORMAL)
        logger.info(f"Preview generated for {len(self.emails_list)} emails")
    
    def display_preview(self):
        """Display emails in preview"""
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        
        for idx, email_data in enumerate(self.emails_data, 1):
            preview = f"""
═══════════════════════════════════════════════════════════
EMAIL {idx}
───────────────────────────────────────────────────────────
TO: {email_data['email']}
SUBJECT: {email_data['subject']}
───────────────────────────────────────────────────────────
{email_data['body']}
═══════════════════════════════════════════════════════════
"""
            self.preview_text.insert(tk.END, preview)
        
        self.preview_text.config(state=tk.DISABLED)
    
    def send_all_emails(self):
        """Send all emails"""
        if not self.emails_data:
            messagebox.showwarning("No Data", "Please preview emails first.")
            return
        
        # Confirm
        if messagebox.askyesno(
            "Confirm Send",
            f"Send {len(self.emails_data)} emails?\n\nMake sure Gmail is open and logged in.\n\nClick 'Test Chrome' first if unsure."
        ):
            # Disable button
            self.send_btn.config(state=tk.DISABLED)
            
            # Show progress
            self.progress_bar.pack(fill=tk.X, padx=0, pady=(0, 5))
            self.progress_var.set(0)
            self.status_label.config(text="Preparing to send emails...", foreground="blue")
            
            # Start sending in thread
            self.sender_thread = threading.Thread(target=self._send_emails_thread)
            self.sender_thread.daemon = True
            self.sender_thread.start()
    
    def _send_emails_thread(self):
        """Thread function to send emails"""
        try:
            handler = ChromeEmailHandler()
            
            if not handler.start_chrome():
                self.status_label.config(
                    text="❌ Failed to start Chrome",
                    foreground="red"
                )
                logger.error("Failed to start Chrome during send")
                self.send_btn.config(state=tk.NORMAL)
                messagebox.showerror(
                    "Chrome Error",
                    "Failed to start Chrome.\n\nMake sure:\n"
                    "1. Chrome is installed\n"
                    "2. ChromeDriver.exe is in this folder\n"
                    "3. Chrome version matches ChromeDriver version"
                )
                return
            
            if not handler.wait_for_gmail_load():
                handler.close()
                self.status_label.config(
                    text="❌ Gmail did not load",
                    foreground="red"
                )
                self.send_btn.config(state=tk.NORMAL)
                messagebox.showerror(
                    "Gmail Error",
                    "Gmail did not load.\n\nMake sure you are logged in to Gmail."
                )
                return
            
            total = len(self.emails_data)
            successful = 0
            
            for index, email_data in enumerate(self.emails_data, 1):
                # Update UI
                progress = (index / total) * 100
                self.progress_var.set(progress)
                self.status_label.config(
                    text=f"Sending {index}/{total} to {email_data['email']}...",
                    foreground="blue"
                )
                self.update()
                
                # Send email
                if handler.send_single_email(
                    email_data['email'],
                    email_data['subject'],
                    email_data['body'],
                    self.resume_path
                ):
                    successful += 1
            
            handler.close()
            
            # Success message
            message = f"✓ Sent {successful}/{total} emails successfully!"
            self.status_label.config(text=message, foreground="green")
            messagebox.showinfo("Success", message)
            self.clear_all()
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.status_label.config(text=error_msg, foreground="red")
            logger.error(f"Send error: {str(e)}")
            messagebox.showerror("Error", f"Failed to send emails:\n\n{str(e)}")
        finally:
            self.send_btn.config(state=tk.NORMAL)
            self.progress_bar.pack_forget()
    
    def clear_all(self):
        """Clear all inputs"""
        self.email_input.delete("1.0", tk.END)
        self.subject_input.delete(0, tk.END)
        self.body_input.delete("1.0", tk.END)
        self.resume_label.config(text="No file selected")
        self.resume_path = None
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.status_label.config(text="")
        self.progress_bar.pack_forget()
        logger.info("Form cleared")


def main():
    app = MailAutomationApp()
    app.mainloop()


if __name__ == '__main__':
    main()
