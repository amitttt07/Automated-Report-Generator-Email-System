"""
Data Processing Module
Handles data cleaning, transformation, and analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from datetime import datetime

class DataProcessor:
    """
    Comprehensive data processing and analysis class
    
    Key Features:
    - Automatic data cleaning
    - Missing value handling
    - Duplicate removal
    - Statistical analysis
    - Trend detection
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize processor with DataFrame
        
        Args:
            df: Raw pandas DataFrame
        """
        self.raw_df = df.copy()
        self.clean_df = None
        self.summary = {}
        
    def clean_data(self) -> pd.DataFrame:
        """
        Comprehensive data cleaning pipeline
        
        Returns:
            Cleaned DataFrame
        """
        df = self.raw_df.copy()
        
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        
        # Handle missing values intelligently
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                # Fill numeric columns with median
                df[col].fillna(df[col].median(), inplace=True)
            else:
                # Fill text columns with 'Unknown'
                df[col].fillna('Unknown', inplace=True)
        
        # Strip whitespace from string columns
        string_cols = df.select_dtypes(include=['object']).columns
        df[string_cols] = df[string_cols].apply(lambda x: x.str.strip() if isinstance(x, pd.Series) else x)
        
        self.clean_df = df
        self.summary['duplicates_removed'] = duplicates_removed
        
        return df
    
    def analyze_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive data analysis
        
        Returns:
            Dictionary containing analysis results
        """
        if self.clean_df is None:
            self.clean_data()
        
        df = self.clean_df
        
        analysis = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'duplicates_removed': self.summary.get('duplicates_removed', 0),
            'columns': list(df.columns),
            'numeric_summary': {},
            'categorical_summary': {},
            'data_quality': {}
        }
        
        # Numeric column analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols:
                analysis['numeric_summary'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'total': float(df[col].sum())
                }
        
        # Categorical column analysis
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                value_counts = df[col].value_counts().head(5)
                analysis['categorical_summary'][col] = {
                    'unique_values': int(df[col].nunique()),
                    'top_5': value_counts.to_dict()
                }
        
        # Data quality metrics
        missing_pct = (self.raw_df.isnull().sum() / len(self.raw_df) * 100)
        analysis['data_quality'] = {
            'completeness': f"{100 - missing_pct.mean():.1f}%",
            'missing_by_column': missing_pct.to_dict()
        }
        
        return analysis
    
    def get_summary_insights(self) -> str:
        """
        Generate human-readable insights from analysis
        
        Returns:
            Formatted string with key insights
        """
        analysis = self.analyze_data()
        
        insights = [
            f"📊 Dataset Overview:",
            f"   • Total Records: {analysis['total_rows']:,}",
            f"   • Features: {analysis['total_columns']}",
            f"   • Data Quality: {analysis['data_quality']['completeness']}",
            f"   • Duplicates Removed: {analysis['duplicates_removed']}",
        ]
        
        # Add numeric insights
        if analysis['numeric_summary']:
            insights.append("\n💰 Key Metrics:")
            for col, stats in list(analysis['numeric_summary'].items())[:3]:
                insights.append(f"   • {col}:")
                insights.append(f"     - Total: {stats['total']:,.2f}")
                insights.append(f"     - Average: {stats['mean']:,.2f}")
        
        # Add categorical insights
        if analysis['categorical_summary']:
            insights.append("\n📋 Categories:")
            for col, stats in list(analysis['categorical_summary'].items())[:2]:
                insights.append(f"   • {col}: {stats['unique_values']} unique values")
        
        return '\n'.join(insights)
    
    def prepare_for_export(self) -> pd.DataFrame:
        """
        Prepare cleaned data for export
        
        Returns:
            Export-ready DataFrame
        """
        if self.clean_df is None:
            self.clean_data()
        
        return self.clean_df