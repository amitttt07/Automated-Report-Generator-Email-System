"""
Automated Report Generator & Email System
Luxury Minimalist UI - Complete Application

A production-ready business intelligence automation tool
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from utils.config import Config
from utils.validators import Validator
from modules.data_processor import DataProcessor
from modules.report_generator import ReportGenerator
from modules.email_sender import EmailSender

# Initialize configuration
Config.create_directories()

# Page configuration
st.set_page_config(
    page_title="Data Analytics Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Luxury Minimalist CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #FDFBF7 0%, #F5F1EA 100%);
        padding: 2rem 4rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 0 4rem 0;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 600;
        color: #3E3530;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #8B7E74;
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Luxury Card */
    .luxury-card {
        background: white;
        border-radius: 24px;
        padding: 3rem 2rem;
        box-shadow: 0 8px 30px rgba(188, 157, 120, 0.12);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(188, 157, 120, 0.1);
        text-align: center;
        height: 100%;
    }
    
    .luxury-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #BC9D78 0%, #D4B896 100%);
        transform: scaleX(0);
        transition: transform 0.4s;
    }
    
    .luxury-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 50px rgba(188, 157, 120, 0.2);
    }
    
    .luxury-card:hover::before {
        transform: scaleX(1);
    }
    
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #3E3530;
        margin-bottom: 0.75rem;
    }
    
    .card-description {
        color: #8B7E74;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Luxury Button */
    .stButton > button {
        background: linear-gradient(135deg, #BC9D78 0%, #A68A65 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(188, 157, 120, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #A68A65 0%, #8F7454 100%);
        box-shadow: 0 6px 25px rgba(188, 157, 120, 0.4);
        transform: translateY(-2px);
    }
    
    /* Upload Area */
    .upload-container {
        background: white;
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 8px 30px rgba(188, 157, 120, 0.12);
        border: 2px dashed rgba(188, 157, 120, 0.3);
        text-align: center;
        transition: all 0.3s;
        margin: 2rem 0;
    }
    
    .upload-container:hover {
        border-color: #BC9D78;
        background: rgba(188, 157, 120, 0.02);
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #BC9D78;
        margin-bottom: 1rem;
    }
    
    .upload-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #3E3530;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtitle {
        color: #8B7E74;
        margin-bottom: 1.5rem;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid rgba(188, 157, 120, 0.2);
        border-radius: 12px;
        padding: 0.875rem 1rem;
        font-size: 1rem;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #BC9D78;
        box-shadow: 0 0 0 3px rgba(188, 157, 120, 0.1);
    }
    
    /* Section Title */
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #3E3530;
        margin: 3rem 0 1.5rem 0;
        font-weight: 600;
    }
    
    /* Metric Box */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #BC9D78;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8B7E74;
        font-weight: 500;
    }
    
    /* Data Table */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(188, 157, 120, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'report_files' not in st.session_state:
    st.session_state.report_files = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None


def navigate_to(page_name):
    """Helper function to navigate between pages"""
    st.session_state.page = page_name


def show_navigation():
    """Display navigation bar"""
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown('<div style="font-family: Playfair Display, serif; font-size: 1.8rem; color: #BC9D78; font-weight: 600;">Analytics Suite</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            navigate_to('home')
    
    with col3:
        if st.button("📤 Upload", key="nav_upload", use_container_width=True):
            navigate_to('upload')
    
    with col4:
        if st.button("📊 Generate", key="nav_generate", use_container_width=True):
            navigate_to('generate')
    
    with col5:
        if st.button("📧 Email", key="nav_email", use_container_width=True):
            navigate_to('email')
    
    with col6:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            navigate_to('settings')


def show_home_page():
    """Home page with luxury card-based design"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Data Into Insights</h1>
        <p class="hero-subtitle">Automate your reporting workflow with elegant precision. Upload, analyze, and share professional reports in seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards Grid
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="luxury-card">
            <span class="card-icon">🏠</span>
            <h3 class="card-title">Home</h3>
            <p class="card-description">View your dashboard and key insights at a glance</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Dashboard", key="btn_home", use_container_width=True):
            st.info("You're on the home page. Explore other sections using the navigation.")
    
    with col2:
        st.markdown("""
        <div class="luxury-card">
            <span class="card-icon">📤</span>
            <h3 class="card-title">Upload Data</h3>
            <p class="card-description">Upload your CSV or Excel files for instant analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Upload Now", key="btn_upload", use_container_width=True):
            navigate_to('upload')
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        st.markdown("""
        <div class="luxury-card">
            <span class="card-icon">📊</span>
            <h3 class="card-title">Generate Report</h3>
            <p class="card-description">Create professional Excel and PDF reports automatically</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate", key="btn_generate", use_container_width=True):
            if st.session_state.processed_data is not None:
                navigate_to('generate')
                st.rerun()
            else:
                st.warning("⚠️ Please upload and process data first")
    
    with col4:
        st.markdown("""
        <div class="luxury-card">
            <span class="card-icon">📧</span>
            <h3 class="card-title">Email Report</h3>
            <p class="card-description">Send reports directly to stakeholders via email</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Send Email", key="btn_email", use_container_width=True):
            if st.session_state.report_files is not None:
                navigate_to('email')
                st.rerun()
            else:
                st.warning("⚠️ Please generate reports first")
    
    # Quick Stats
    st.markdown('<h2 class="section-title">Quick Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.processed_data is not None:
            st.metric("Records", f"{len(st.session_state.processed_data):,}")
        else:
            st.metric("Records", "0")
    
    with col2:
        if st.session_state.processed_data is not None:
            st.metric("Features", len(st.session_state.processed_data.columns))
        else:
            st.metric("Features", "0")
    
    with col3:
        if st.session_state.report_files is not None:
            st.metric("Reports", "✓ Ready")
        else:
            st.metric("Reports", "Pending")
    
    with col4:
        if st.session_state.analysis_results is not None:
            st.metric("Quality", st.session_state.analysis_results['data_quality']['completeness'])
        else:
            st.metric("Quality", "N/A")


def show_upload_page():
    """Upload page with drag-and-drop interface"""
    
    st.markdown('<h1 class="hero-title">Upload Data</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Upload your CSV or Excel files for analysis. Maximum file size: 50MB</p>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Upload container
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls'],
        help="Drag and drop file here or click to browse",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Validate file
        is_valid, error_msg = Validator.validate_file(uploaded_file, Config.MAX_FILE_SIZE_MB)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        try:
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                is_valid, error_msg = Validator.validate_dataframe(df)
                
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                    return
                
                st.success(f"✅ File loaded: {len(df):,} rows × {len(df.columns)} columns")
                
                # Data Preview
                st.markdown('<h2 class="section-title">Data Preview</h2>', unsafe_allow_html=True)
                st.dataframe(df.head(10), use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Columns**")
                    st.write(df.columns.tolist())
                
                with col2:
                    st.markdown("**Data Types**")
                    st.write(df.dtypes.to_dict())
                
                # Process button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ Clean & Analyze Data", use_container_width=True):
                    with st.spinner("Processing..."):
                        processor = DataProcessor(df)
                        clean_df = processor.clean_data()
                        analysis = processor.analyze_data()
                        
                        st.session_state.processed_data = clean_df
                        st.session_state.analysis_results = analysis
                        st.session_state.data_processor = processor
                        
                        st.success("✅ Data processed successfully!")
                        st.text(processor.get_summary_insights())
                        st.info("👉 Navigate to 'Generate Report' to create reports")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    else:
        st.markdown("""
        <div class="upload-container">
            <div class="upload-icon">📁</div>
            <h3 class="upload-title">Drop your file here</h3>
            <p class="upload-subtitle">Supports CSV, XLSX, XLS files up to 50MB</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📥 Load Sample Data", use_container_width=True):
            sample_data = pd.DataFrame({
                'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
                'Product': ['Product A', 'Product B', 'Product C'] * 33 + ['Product A'],
                'Sales': [100 + i * 5 for i in range(100)],
                'Region': ['North', 'South', 'East', 'West'] * 25,
                'Quantity': [10 + i for i in range(100)]
            })
            
            processor = DataProcessor(sample_data)
            clean_df = processor.clean_data()
            analysis = processor.analyze_data()
            
            st.session_state.processed_data = clean_df
            st.session_state.analysis_results = analysis
            st.session_state.data_processor = processor
            
            st.success("✅ Sample data loaded!")
            st.rerun()


def show_generate_page():
    """Report generation page"""
    
    st.markdown('<h1 class="hero-title">Generate Reports</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Create professional Excel and PDF reports with one click</p>', unsafe_allow_html=True)
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload and process data first!")
        if st.button("Go to Upload", use_container_width=True):
            navigate_to('upload')
            st.rerun()
        return
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", value=Config.COMPANY_NAME)
    
    with col2:
        report_author = st.text_input("Report Author", value=Config.REPORT_AUTHOR)
    
    # Data Summary
    st.markdown('<h2 class="section-title">Data Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(st.session_state.processed_data):,}")
    with col2:
        st.metric("Features", len(st.session_state.processed_data.columns))
    with col3:
        st.metric("Data Quality", st.session_state.analysis_results['data_quality']['completeness'])
    with col4:
        st.metric("Duplicates Removed", st.session_state.analysis_results['duplicates_removed'])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Generate button
    if st.button("🎨 Generate Excel & PDF Reports", use_container_width=True):
        with st.spinner("Generating reports..."):
            try:
                generator = ReportGenerator(
                    st.session_state.processed_data,
                    st.session_state.analysis_results,
                    company_name
                )
                
                report_files = generator.generate_all_reports(Config.OUTPUTS_DIR)
                st.session_state.report_files = report_files
                
                st.success("✅ Reports generated successfully!")
                
                # Download buttons
                st.markdown('<h2 class="section-title">Download Reports</h2>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with open(report_files['excel'], 'rb') as f:
                        st.download_button(
                            label="📊 Download Excel Report",
                            data=f,
                            file_name=Path(report_files['excel']).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                
                with col2:
                    with open(report_files['pdf'], 'rb') as f:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=f,
                            file_name=Path(report_files['pdf']).name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def show_email_page():
    """Email automation page"""
    
    st.markdown('<h1 class="hero-title">Email Reports</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Send professional reports directly to stakeholders</p>', unsafe_allow_html=True)
    
    if st.session_state.report_files is None:
        st.warning("⚠️ Please generate reports first!")
        if st.button("Go to Generate", use_container_width=True):
            navigate_to('generate')
            st.rerun()
        return
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Email Configuration
    st.markdown('<h2 class="section-title">Email Configuration</h2>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ Email Setup Guide", expanded=False):
        st.markdown("""
        **For Gmail:**
        1. Enable 2-factor authentication
        2. Generate App Password: [Google Account](https://myaccount.google.com/apppasswords)
        3. Use the 16-character app password
        
        **For Outlook:** Use your regular password or app password
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("📨 Your Email", placeholder="your.email@company.com")
        smtp_provider = st.selectbox("📮 Email Provider", ["Gmail", "Outlook", "Office365", "Custom"])
    
    with col2:
        sender_password = st.text_input("🔒 Password/App Password", type="password")
        
        if smtp_provider == "Custom":
            smtp_host = st.text_input("SMTP Host", value="smtp.gmail.com")
            smtp_port = st.number_input("SMTP Port", value=587)
        else:
            smtp_config = EmailSender.get_smtp_config(smtp_provider)
            smtp_host = smtp_config['host']
            smtp_port = smtp_config['port']
    
    # Recipients
    st.markdown('<h2 class="section-title">Recipients</h2>', unsafe_allow_html=True)
    recipients = st.text_area(
        "To (comma-separated emails)",
        placeholder="john@company.com, jane@company.com",
        height=100
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Send button
    if st.button("📤 Send Email Reports", use_container_width=True):
        
        if not sender_email or not sender_password:
            st.error("❌ Please enter your email credentials")
            return
        
        if not Validator.validate_email(sender_email):
            st.error("❌ Invalid sender email")
            return
        
        is_valid, email_list, error_msg = Validator.validate_email_list(recipients)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
        
        with st.spinner("Sending email..."):
            try:
                email_sender = EmailSender(smtp_host, smtp_port, sender_email, sender_password)
                analysis_summary = st.session_state.data_processor.get_summary_insights()
                
                result = email_sender.send_report_email(
                    recipients=email_list,
                    company_name=Config.COMPANY_NAME,
                    analysis_summary=analysis_summary,
                    report_files=st.session_state.report_files
                )
                
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    st.balloons()
                    st.info(f"📧 Sent to: {', '.join(result['recipients'])}")
                else:
                    st.error(f"❌ {result['message']}")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def show_settings_page():
    """Settings page"""
    
    st.markdown('<h1 class="hero-title">Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Configure your application preferences</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Company Information
    st.markdown('<h2 class="section-title">Company Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", value=Config.COMPANY_NAME)
        report_author = st.text_input("Default Author", value=Config.REPORT_AUTHOR)
    
    with col2:
        max_file_size = st.number_input("Max File Size (MB)", value=Config.MAX_FILE_SIZE_MB, min_value=1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Information
    st.markdown('<h2 class="section-title">System Information</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Outputs Folder", "outputs/")
    with col2:
        st.metric("Supported Formats", "CSV, XLSX, XLS")
    with col3:
        if st.session_state.report_files:
            st.metric("Reports Status", "✓ Ready")
        else:
            st.metric("Reports Status", "Pending")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Data Management
    st.markdown('<h2 class="section-title">Data Management</h2>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear All Session Data", use_container_width=True):
        st.session_state.processed_data = None
        st.session_state.analysis_results = None
        st.session_state.report_files = None
        st.session_state.data_processor = None
        st.success("✅ Session data cleared!")
        st.rerun()


def main():
    """Main application function"""
    
    # Navigation
    show_navigation()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'upload':
        show_upload_page()
    elif st.session_state.page == 'generate':
        show_generate_page()
    elif st.session_state.page == 'email':
        show_email_page()
    elif st.session_state.page == 'settings':
        show_settings_page()


if __name__ == "__main__":
    main()