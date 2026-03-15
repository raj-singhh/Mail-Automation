"""
Utility functions for email processing
"""
import re
from typing import Tuple

def extract_name_from_email(email: str) -> str:
    """
    Extract a proper name from email address
    Examples: 
        john.doe@gmail.com -> John Doe
        john_smith@company.com -> John Smith
        jsmith@company.com -> J Smith
    """
    # Get the part before @
    local_part = email.split('@')[0]
    
    # Replace common separators with space
    name = re.sub(r'[._\-]', ' ', local_part)
    
    # Capitalize each word
    words = name.split()
    capitalized = [word.capitalize() for word in words]
    
    return ' '.join(capitalized)


def format_email_body(body: str, recipient_email: str) -> str:
    """
    Format email body with personalized greeting
    """
    name = extract_name_from_email(recipient_email)
    
    # Add greeting if not already present
    if not body.strip().lower().startswith('dear') and not body.strip().lower().startswith('hi'):
        greeting = f"Dear {name},\n\n"
        return greeting + body
    
    return body


def validate_email(email: str) -> bool:
    """
    Simple email validation
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def sanitize_email(email: str) -> str:
    """
    Clean and normalize email address
    """
    return email.strip().lower()


def parse_email_list(email_input: str) -> list:
    """
    Parse email input (supports comma or newline separated)
    
    Args:
        email_input: String with emails separated by comma or newline
        
    Returns:
        List of valid email addresses
    """
    # Replace newlines with commas for uniform processing
    email_input = email_input.replace('\n', ',')
    
    # Split by comma
    emails = [email.strip() for email in email_input.split(',')]
    
    # Filter empty strings and validate
    emails = [sanitize_email(email) for email in emails if email.strip()]
    valid_emails = [email for email in emails if validate_email(email)]
    
    return valid_emails
