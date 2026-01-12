"""
Configuration Management Module
Handles environment variables and application settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUTS_DIR = BASE_DIR / "outputs"
    ASSETS_DIR = BASE_DIR / "assets"
    SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
    
    # Email configuration (loaded from .env file)
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USER = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    
    # Report settings
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Business Analytics Corp")
    REPORT_AUTHOR = os.getenv("REPORT_AUTHOR", "Analytics Team")
    
    # Supported file formats
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls']
    MAX_FILE_SIZE_MB = 50
    
    # UI Theme colors
    PRIMARY_COLOR = "#1f77b4"
    SUCCESS_COLOR = "#28a745"
    WARNING_COLOR = "#ffc107"
    DANGER_COLOR = "#dc3545"
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.OUTPUTS_DIR.mkdir(exist_ok=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True)
        cls.SAMPLE_DATA_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate_email_config(cls):
        """Check if email configuration is complete"""
        return bool(cls.EMAIL_USER and cls.EMAIL_PASSWORD)