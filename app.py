"""
Streamlit UI for the Legislative AI Agent.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import os
import json
import logging
from dotenv import load_dotenv
from agent import LegislativeAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Legislative AI Agent",
    page_icon="🏛️",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'text_extracted' not in st.session_state:
    st.session_state.text_extracted = False
if 'agent_run' not in st.session_state:
    st.session_state.agent_run = False
if 'results' not in st.session_state:
    st.session_state.results = {}

# Title
st.title("🏛️ Legislative AI Agent")
st.markdown("Process legislation PDFs and extract structured insights.")


st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password", 
                               value=os.getenv("GOOGLE_API_KEY", ""))
if api_key:
    st.session_state.agent = LegislativeAgent(api_key)
else:
    st.sidebar.warning("Please enter your Google Gemini API Key")
    st.info("👈 Enter your Google Gemini API Key in the sidebar to get started")


st.header("Upload Legislation PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded: {uploaded_file.name}")
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Extract Text", use_container_width=True):
            if st.session_state.agent:
                with st.spinner("Extracting text from PDF..."):
                    try:
                        logger.info("Extracting text from uploaded PDF")
                        raw_text = st.session_state.agent.extract_text("temp_pdf.pdf")
                        cleaned_text = st.session_state.agent.clean_text(raw_text)
                        st.session_state.cleaned_text = cleaned_text
                        st.session_state.text_extracted = True
                        st.success("Text extracted successfully!")
                        logger.info("Text extraction completed successfully")
                    except Exception as e:
                        st.error(f"Error extracting text: {str(e)}")
                        logger.error("Error extracting text: %s", str(e))
            else:
                st.warning("Please enter your API key first")
    
    with col2:
        if st.button("▶️ Run Agent", use_container_width=True):
            if st.session_state.agent and st.session_state.text_extracted:
                with st.spinner("Processing legislation with AI agent..."):
                    try:
                        logger.info("Running agent with legal document rule checks")
                        # Run complete processing pipeline
                        results = st.session_state.agent.process_legislation(
                            "temp_pdf.pdf", 
                            "legislation_analysis.json"
                        )
                        
                        
                        st.session_state.results = results
                        st.session_state.agent_run = True
                        st.success("Agent processing complete!")
                        logger.info("Agent processing completed successfully")
                    except Exception as e:
                        st.error(f"Error running agent: {str(e)}")
                        logger.error("Error running agent: %s", str(e))
            elif not st.session_state.agent:
                st.warning("Please enter your API key first")
            else:
                st.warning("Please extract text first")

# Display results if agent has run
if st.session_state.agent_run:
    st.header("Results")
    
    # Summary tab
    st.subheader("📋 Executive Summary")
    st.markdown(st.session_state.results["summary"])
    
    # Sections tab
    st.subheader("📂 Extracted Sections")
    sections = st.session_state.results["sections"]
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Definitions", "Obligations", "Responsibilities", 
        "Eligibility", "Payments", "Penalties", "Record Keeping"
    ])
    
    with tab1:
        st.write(sections.get("definitions", "Not found"))
    with tab2:
        st.write(sections.get("obligations", "Not found"))
    with tab3:
        st.write(sections.get("responsibilities", "Not found"))
    with tab4:
        st.write(sections.get("eligibility", "Not found"))
    with tab5:
        st.write(sections.get("payments", "Not found"))
    with tab6:
        st.write(sections.get("penalties", "Not found"))
    with tab7:
        st.write(sections.get("record_keeping", "Not found"))
    
    # Rule checks tab
    st.subheader("✅ Rule Compliance Check")
    rule_checks = st.session_state.results["rule_checks"]
    
    # Convert to DataFrame for better display
    import pandas as pd
    df = pd.DataFrame(rule_checks)
    st.dataframe(df, use_container_width=True)
    
    # Download JSON button
    st.subheader("💾 Export Results")
    json_str = json.dumps(st.session_state.results, indent=2)
    st.download_button(
        label="Download JSON Report",
        data=json_str,
        file_name="legislation_analysis.json",
        mime="application/json",
        use_container_width=True
    )

# Cleanup temporary file
if os.path.exists("temp_pdf.pdf"):
    os.remove("temp_pdf.pdf")