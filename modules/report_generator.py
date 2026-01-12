"""
Report Generation Module
Creates professional Excel and PDF reports with charts and insights
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

class ReportGenerator:
    """
    Professional report generation with Excel and PDF export
    
    Features:
    - Multi-sheet Excel workbooks
    - PDF reports with tables and charts
    - Automatic chart generation
    - Professional formatting
    """
    
    def __init__(self, df: pd.DataFrame, analysis: dict, company_name: str = "Business Analytics"):
        """
        Initialize report generator
        
        Args:
            df: Cleaned DataFrame
            analysis: Analysis results dictionary
            company_name: Company name for branding
        """
        self.df = df
        self.analysis = analysis
        self.company_name = company_name
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def generate_excel_report(self, output_dir: Path) -> str:
        """
        Generate comprehensive Excel report with multiple sheets
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            Path to generated Excel file
        """
        filename = f"Report_{self.timestamp}.xlsx"
        filepath = output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#1f77b4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            # Sheet 1: Summary
            summary_df = pd.DataFrame({
                'Metric': [
                    'Report Generated',
                    'Company',
                    'Total Records',
                    'Total Columns',
                    'Data Quality',
                    'Duplicates Removed'
                ],
                'Value': [
                    self.analysis['timestamp'],
                    self.company_name,
                    self.analysis['total_rows'],
                    self.analysis['total_columns'],
                    self.analysis['data_quality']['completeness'],
                    self.analysis['duplicates_removed']
                ]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            worksheet = writer.sheets['Summary']
            worksheet.set_column('A:A', 25)
            worksheet.set_column('B:B', 30)
            
            # Sheet 2: Clean Data
            self.df.to_excel(writer, sheet_name='Clean Data', index=False)
            worksheet = writer.sheets['Clean Data']
            for i, col in enumerate(self.df.columns):
                worksheet.write(0, i, col, header_format)
                worksheet.set_column(i, i, 15)
            
            # Sheet 3: Numeric Analysis
            if self.analysis['numeric_summary']:
                numeric_data = []
                for col, stats in self.analysis['numeric_summary'].items():
                    numeric_data.append({
                        'Column': col,
                        'Mean': round(stats['mean'], 2),
                        'Median': round(stats['median'], 2),
                        'Std Dev': round(stats['std'], 2),
                        'Min': round(stats['min'], 2),
                        'Max': round(stats['max'], 2),
                        'Total': round(stats['total'], 2)
                    })
                numeric_df = pd.DataFrame(numeric_data)
                numeric_df.to_excel(writer, sheet_name='Numeric Analysis', index=False)
                worksheet = writer.sheets['Numeric Analysis']
                for i, col in enumerate(numeric_df.columns):
                    worksheet.write(0, i, col, header_format)
                    worksheet.set_column(i, i, 15)
            
            # Sheet 4: Categorical Analysis
            if self.analysis['categorical_summary']:
                cat_data = []
                for col, stats in self.analysis['categorical_summary'].items():
                    cat_data.append({
                        'Column': col,
                        'Unique Values': stats['unique_values'],
                        'Top Value': list(stats['top_5'].keys())[0] if stats['top_5'] else 'N/A',
                        'Top Count': list(stats['top_5'].values())[0] if stats['top_5'] else 0
                    })
                cat_df = pd.DataFrame(cat_data)
                cat_df.to_excel(writer, sheet_name='Categorical Analysis', index=False)
                worksheet = writer.sheets['Categorical Analysis']
                for i, col in enumerate(cat_df.columns):
                    worksheet.write(0, i, col, header_format)
                    worksheet.set_column(i, i, 20)
        
        return str(filepath)
    
    def _create_charts(self) -> list:
        """
        Create matplotlib charts for PDF report
        
        Returns:
            List of chart image paths
        """
        charts = []
        
        # Chart 1: Numeric columns distribution (if any)
        numeric_cols = self.df.select_dtypes(include=['number']).columns[:4]
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            axes = axes.flatten()
            
            for i, col in enumerate(numeric_cols):
                if i < 4:
                    self.df[col].hist(bins=20, ax=axes[i], color='#1f77b4', edgecolor='black')
                    axes[i].set_title(f'{col} Distribution', fontsize=10, fontweight='bold')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frequency')
            
            plt.tight_layout()
            chart1_path = BytesIO()
            plt.savefig(chart1_path, format='png', dpi=150, bbox_inches='tight')
            chart1_path.seek(0)
            charts.append(chart1_path)
            plt.close()
        
        return charts
    
    def generate_pdf_report(self, output_dir: Path) -> str:
        """
        Generate professional PDF report with tables and charts
        
        Args:
            output_dir: Directory to save report
            
        Returns:
            Path to generated PDF file
        """
        filename = f"Report_{self.timestamp}.pdf"
        filepath = output_dir / filename
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                                rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.75*inch, bottomMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph(f"{self.company_name}", title_style))
        story.append(Paragraph("Business Intelligence Report", styles['Heading2']))
        story.append(Paragraph(f"Generated: {self.analysis['timestamp']}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Records', f"{self.analysis['total_rows']:,}"],
            ['Features Analyzed', str(self.analysis['total_columns'])],
            ['Data Quality', self.analysis['data_quality']['completeness']],
            ['Duplicates Removed', str(self.analysis['duplicates_removed'])]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Numeric Analysis
        if self.analysis['numeric_summary']:
            story.append(Paragraph("Key Metrics Analysis", heading_style))
            numeric_data = [['Column', 'Mean', 'Median', 'Min', 'Max', 'Total']]
            
            for col, stats in list(self.analysis['numeric_summary'].items())[:5]:
                numeric_data.append([
                    col,
                    f"{stats['mean']:,.2f}",
                    f"{stats['median']:,.2f}",
                    f"{stats['min']:,.2f}",
                    f"{stats['max']:,.2f}",
                    f"{stats['total']:,.2f}"
                ])
            
            numeric_table = Table(numeric_data, colWidths=[1.5*inch]*6)
            numeric_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            story.append(numeric_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Add charts
        charts = self._create_charts()
        if charts:
            story.append(PageBreak())
            story.append(Paragraph("Data Visualizations", heading_style))
            for chart in charts:
                img = Image(chart, width=6*inch, height=4.5*inch)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        
        return str(filepath)
    
    def generate_all_reports(self, output_dir: Path) -> dict:
        """
        Generate both Excel and PDF reports
        
        Args:
            output_dir: Directory to save reports
            
        Returns:
            Dictionary with paths to generated files
        """
        return {
            'excel': self.generate_excel_report(output_dir),
            'pdf': self.generate_pdf_report(output_dir)
        }