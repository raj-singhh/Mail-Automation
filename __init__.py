# Mail Automation Tool
from .email_utils import (
    extract_name_from_email,
    format_email_body,
    validate_email,
    parse_email_list
)

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = [
    'extract_name_from_email',
    'format_email_body',
    'validate_email',
    'parse_email_list'
]
