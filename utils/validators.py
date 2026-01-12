"""
Input Validation Module
Validates file uploads, email addresses, and data structure
"""
import re
import pandas as pd
from pathlib import Path
from typing import Tuple, List

class Validator:
    """Input validation utility class"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format
        
        Args:
            email: Email address string
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    @staticmethod
    def validate_email_list(emails: str) -> Tuple[bool, List[str], str]:
        """
        Validate comma-separated list of emails
        
        Args:
            emails: Comma-separated email string
            
        Returns:
            Tuple of (is_valid, valid_emails, error_message)
        """
        email_list = [e.strip() for e in emails.split(',') if e.strip()]
        
        if not email_list:
            return False, [], "Please enter at least one email address"
        
        invalid_emails = [e for e in email_list if not Validator.validate_email(e)]
        
        if invalid_emails:
            return False, [], f"Invalid email(s): {', '.join(invalid_emails)}"
        
        return True, email_list, ""
    
    @staticmethod
    def validate_file(file, max_size_mb: int = 50) -> Tuple[bool, str]:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file object
            max_size_mb: Maximum file size in MB
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if file is None:
            return False, "No file uploaded"
        
        # Check file extension
        file_ext = Path(file.name).suffix.lower()
        if file_ext not in ['.csv', '.xlsx', '.xls']:
            return False, f"Unsupported file format: {file_ext}. Use CSV or Excel files."
        
        # Check file size
        file_size_mb = file.size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File too large ({file_size_mb:.1f}MB). Maximum: {max_size_mb}MB"
        
        return True, ""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate DataFrame structure
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if df is None or df.empty:
            return False, "Data file is empty"
        
        if len(df.columns) < 2:
            return False, "Data must have at least 2 columns"
        
        if len(df) < 1:
            return False, "Data must have at least 1 row"
        
        return True, ""