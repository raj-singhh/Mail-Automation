"""
Mail Automation Tool - Main Application
Desktop application to automate email sending through Gmail
"""
import sys
import os
import logging
import threading
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QTable,
    QTableWidget, QTableWidgetItem, QSplitter, QMessageBox,
    QProgressBar, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon
from email_utils import parse_email_list, extract_name_from_email, format_email_body, validate_email
from chrome_handler import ChromeEmailHandler

# Configure logging
logging.basicConfig(
    filename='logs/mail_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailSenderThread(QThread):
    """Thread to handle email sending without blocking UI"""
    progress = pyqtSignal(int, str)  # Signal for progress updates
    finished = pyqtSignal(bool, str)  # Signal when finished
    
    def __init__(self, emails_data, attachment_path=None):
        super().__init__()
        self.emails_data = emails_data  # List of dicts: {email, subject, body}
        self.attachment_path = attachment_path
        self.chrome_handler = None
        
    def run(self):
        """Execute email sending"""
        try:
            self.chrome_handler = ChromeEmailHandler()
            
            if not self.chrome_handler.start_chrome():
                self.finished.emit(False, "Failed to start Chrome browser")
                return
            
            if not self.chrome_handler.wait_for_gmail_load():
                self.chrome_handler.close()
                self.finished.emit(False, "Gmail failed to load. Please ensure you're logged in.")
                return
            
            total = len(self.emails_data)
            successful = 0
            
            for index, email_data in enumerate(self.emails_data):
                progress_msg = f"Sending email {index + 1}/{total} to {email_data['email']}..."
                self.progress.emit(index + 1, progress_msg)
                
                success = self.chrome_handler.send_single_email(
                    email_data['email'],
                    email_data['subject'],
                    email_data['body'],
                    self.attachment_path
                )
                
                if success:
                    successful += 1
                else:
                    logger.warning(f"Failed to send email to {email_data['email']}")
            
            self.chrome_handler.close()
            message = f"Completed! Sent {successful}/{total} emails successfully."
            self.finished.emit(True, message)
            logger.info(message)
            
        except Exception as e:
            error_msg = f"Error during email sending: {str(e)}"
            logger.error(error_msg)
            if self.chrome_handler:
                self.chrome_handler.close()
            self.finished.emit(False, error_msg)


class MailAutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mail Automation Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_stylesheet())
        
        # Data storage
        self.emails_list = []
        self.emails_data = []  # Store formatted emails with personalized content
        self.resume_path = None
        self.sender_thread = None
        
        # Create UI
        self.create_ui()
        logger.info("Application started")
    
    def create_ui(self):
        """Create the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left panel - Input form
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Mail Automation Tool")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(title)
        
        # Email IDs section
        email_label = QLabel("Email IDs (comma or line separated):")
        email_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(email_label)
        
        self.email_input = QTextEdit()
        self.email_input.setPlaceholderText("john@example.com\njane@example.com\nor\njohn@example.com, jane@example.com")
        left_layout.addWidget(self.email_input)
        
        # Subject section
        subject_label = QLabel("Email Subject:")
        subject_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(subject_label)
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("e.g., Job Application")
        left_layout.addWidget(self.subject_input)
        
        # Body section
        body_label = QLabel("Email Body:")
        body_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(body_label)
        
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Write your email content here. Names will be automatically added in greeting.")
        left_layout.addWidget(self.body_input)
        
        # Resume section
        resume_label = QLabel("Attachment (Resume/CV):")
        resume_label.setFont(QFont("Arial", 10, QFont.Bold))
        left_layout.addWidget(resume_label)
        
        resume_layout = QHBoxLayout()
        self.resume_label = QLabel("No file selected")
        resume_layout.addWidget(self.resume_label)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        resume_layout.addWidget(browse_btn)
        
        left_layout.addLayout(resume_layout)
        
        # Preview button
        preview_btn = QPushButton("Preview Emails")
        preview_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        preview_btn.clicked.connect(self.preview_emails)
        left_layout.addWidget(preview_btn)
        
        left_panel.setLayout(left_layout)
        
        # Right panel - Preview table
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        preview_title = QLabel("Email Preview")
        preview_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(preview_title)
        
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(3)
        self.preview_table.setHorizontalHeaderLabels(["Recipient", "Subject", "Body Preview"])
        self.preview_table.setColumnWidth(0, 180)
        self.preview_table.setColumnWidth(1, 200)
        self.preview_table.setColumnWidth(2, 300)
        right_layout.addWidget(self.preview_table)
        
        # Progress bar
        progress_label = QLabel("Progress:")
        right_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setVisible(False)
        right_layout.addWidget(self.status_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.send_btn = QPushButton("Send All Emails")
        self.send_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.send_btn.clicked.connect(self.send_all_emails)
        self.send_btn.setEnabled(False)
        button_layout.addWidget(self.send_btn)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-weight: bold;")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)
        
        right_layout.addLayout(button_layout)
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
    
    def browse_file(self):
        """Browse and select resume file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Resume/CV",
            "",
            "PDF Files (*.pdf);;Word Documents (*.docx);;All Files (*.*)"
        )
        
        if file_path:
            self.resume_path = file_path
            self.resume_label.setText(f"Selected: {Path(file_path).name}")
            logger.info(f"Resume selected: {file_path}")
    
    def preview_emails(self):
        """Validate input and show email preview"""
        # Get and validate inputs
        email_input = self.email_input.toPlainText().strip()
        subject = self.subject_input.text().strip()
        body = self.body_input.toPlainText().strip()
        
        if not email_input:
            QMessageBox.warning(self, "Input Error", "Please enter at least one email address.")
            logger.warning("Preview attempted with empty email list")
            return
        
        if not subject:
            QMessageBox.warning(self, "Input Error", "Please enter email subject.")
            return
        
        if not body:
            QMessageBox.warning(self, "Input Error", "Please enter email body.")
            return
        
        # Parse emails
        self.emails_list = parse_email_list(email_input)
        
        if not self.emails_list:
            QMessageBox.warning(self, "Input Error", "No valid email addresses found.")
            logger.warning("No valid emails after parsing")
            return
        
        # Create formatted emails with personalized greetings
        self.emails_data = []
        for email in self.emails_list:
            personalized_body = format_email_body(body, email)
            self.emails_data.append({
                'email': email,
                'subject': subject,
                'body': personalized_body
            })
        
        # Display in table
        self.display_preview()
        self.send_btn.setEnabled(True)
        
        logger.info(f"Preview generated for {len(self.emails_list)} emails")
    
    def display_preview(self):
        """Display emails in preview table"""
        self.preview_table.setRowCount(0)
        
        for row, email_data in enumerate(self.emails_data):
            self.preview_table.insertRow(row)
            
            # Recipient
            recipient_item = QTableWidgetItem(email_data['email'])
            self.preview_table.setItem(row, 0, recipient_item)
            
            # Subject
            subject_item = QTableWidgetItem(email_data['subject'])
            self.preview_table.setItem(row, 1, subject_item)
            
            # Body preview (first 100 chars)
            body_preview = email_data['body'][:100] + "..." if len(email_data['body']) > 100 else email_data['body']
            body_item = QTableWidgetItem(body_preview)
            self.preview_table.setItem(row, 2, body_item)
    
    def send_all_emails(self):
        """Send all emails"""
        if not self.emails_data:
            QMessageBox.warning(self, "No Data", "Please preview emails first.")
            return
        
        # Confirm before sending
        reply = QMessageBox.question(
            self,
            "Confirm Send",
            f"Are you sure you want to send {len(self.emails_data)} emails?\n\n"
            "Note: Make sure Gmail is open and you are logged in with your account.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Disable input during sending
        self.email_input.setEnabled(False)
        self.subject_input.setEnabled(False)
        self.body_input.setEnabled(False)
        self.send_btn.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.emails_data))
        self.progress_bar.setValue(0)
        self.status_label.setVisible(True)
        
        # Start sending in separate thread
        self.sender_thread = EmailSenderThread(self.emails_data, self.resume_path)
        self.sender_thread.progress.connect(self.on_progress)
        self.sender_thread.finished.connect(self.on_sending_finished)
        self.sender_thread.start()
        
        logger.info(f"Starting to send {len(self.emails_data)} emails")
    
    def on_progress(self, value, message):
        """Handle progress update"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def on_sending_finished(self, success, message):
        """Handle sending completion"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(message)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_all()
        else:
            QMessageBox.critical(self, "Error", message)
        
        # Re-enable inputs
        self.email_input.setEnabled(True)
        self.subject_input.setEnabled(True)
        self.body_input.setEnabled(True)
    
    def clear_all(self):
        """Clear all inputs"""
        self.email_input.clear()
        self.subject_input.clear()
        self.body_input.clear()
        self.resume_label.setText("No file selected")
        self.resume_path = None
        self.preview_table.setRowCount(0)
        self.send_btn.setEnabled(False)
        self.status_label.setVisible(False)
        logger.info("Form cleared")
    
    @staticmethod
    def get_stylesheet():
        """Return custom stylesheet for the application"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel {
            color: #333;
        }
        QLineEdit, QTextEdit {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            font-size: 10pt;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #4CAF50;
        }
        QPushButton {
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            cursor: pointer;
        }
        QPushButton:hover {
            opacity: 0.9;
        }
        QTableWidget {
            background-color: white;
            border: 1px solid #ddd;
            gridline-color: #eee;
        }
        QHeaderView::section {
            background-color: #4CAF50;
            color: white;
            padding: 5px;
            border: none;
        }
        QProgressBar {
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: center;
            background-color: white;
        }
        """


def main():
    app = QApplication(sys.argv)
    window = MailAutomationApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
