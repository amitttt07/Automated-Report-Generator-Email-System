# modules/__init__.py
"""
Modules package for automated report generation
"""

from .data_processor import DataProcessor
from .report_generator import ReportGenerator
from .email_sender import EmailSender

__all__ = ['DataProcessor', 'ReportGenerator', 'EmailSender']


