import streamlit as st
import os
from dotenv import load_dotenv
from tnm_stage_calculator import process_medical_reports

# Load environment variables from .env file
load_dotenv()

def main():
    st.title("TNM Stage Calculator")
    st.write("Paste your medical report text below to determine cancer staging")

    # Check if API key is configured
    if not os.getenv("GROQ_API_KEY"):
        st.error("Please configure GROQ_API_KEY in your environment variables or .env file")
        return

    # Replace file uploader with text area
    report_text = st.text_area(
        "Medical Report Text",
        height=300,
        placeholder="Paste your medical report text here..."
    )

    if report_text:
        if st.button("Analyze Report"):
            with st.spinner("Analyzing report..."):
                try:
                    # Pass the same report text for both parameters since we're analyzing a single report
                    result = process_medical_reports(
                        ct_report=report_text,
                        pet_report=report_text,
                        groq_api_key=os.getenv("GROQ_API_KEY")
                    )

                    # Display results
                    tnm = result["tnm"]
                    cancer_stage = result["stage"]

                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(label="T Stage", value=tnm.t_stage)
                    
                    with col2:
                        st.metric(label="N Stage", value=tnm.n_stage)
                    
                    with col3:
                        st.metric(label="M Stage", value=tnm.m_stage)

                    st.markdown("### Final Assessment")
                    st.markdown(f"**Cancer Stage:** {cancer_stage}")

                except Exception as e:
                    st.error(f"An error occurred while processing the report: {str(e)}")
                    if st.secrets.get("development_mode"):
                        import traceback
                        st.error(traceback.format_exc())

    with st.expander("How to use"):
        st.write("""
        1. Paste your medical report text into the text area
        2. Click 'Analyze Report' to process the text
        3. The system will display the TNM classification and final cancer stage
        
        Note: Make sure the report contains clear TNM staging information.
        """)

if __name__ == "__main__":
    main() 