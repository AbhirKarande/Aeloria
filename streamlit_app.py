import streamlit as st
import os
from dotenv import load_dotenv
from tnm_stage_calculator import process_medical_reports

# Load environment variables from .env file
load_dotenv()

def main():
    st.title("TNM Stage Calculator")
    st.write("Upload CT and PET scan reports to determine cancer staging")

    # Check if API key is configured
    if not os.getenv("GROQ_API_KEY"):
        st.error("Please configure GROQ_API_KEY in your environment variables or .env file")
        return

    uploaded_files = st.file_uploader(
        "Upload medical reports (CT scan, PET scan, etc.)", 
        accept_multiple_files=True,
        type=['txt', 'pdf']
    )

    if uploaded_files:
        all_reports = ""
        for file in uploaded_files:
            report_content = file.read().decode()
            all_reports += f"\n--- Report from {file.name} ---\n{report_content}\n"
            
        if st.button("Analyze Reports"):
            with st.spinner("Analyzing reports..."):
                try:
                    # Pass the API key from environment variables
                    result = process_medical_reports(
                        ct_report=all_reports,
                        pet_report=all_reports,
                        groq_api_key=os.getenv("GROQ_API_KEY")
                    )

                    # Access the results directly from the dictionary
                    tnm = result["tnm"]
                    cancer_stage = result["stage"]

                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(label="T Stage", value=tnm.t_stage)
                    
                    with col2:
                        st.metric(label="N Stage", value=tnm.n_stage)
                    
                    with col3:
                        st.metric(label="M Stage", value=tnm.m_stage)

                    # Display the final cancer stage
                    st.markdown("### Final Assessment")
                    st.markdown(f"**Cancer Stage:** {cancer_stage}")

                except Exception as e:
                    st.error(f"An error occurred while processing the reports: {str(e)}")
                    # Add more detailed error information in development
                    import traceback
                    st.error(traceback.format_exc())

    with st.expander("How to use"):
        st.write("""
        1. Upload one or more medical reports (CT scan, PET scan, etc.)
        2. Click 'Analyze Reports' to process the documents
        3. The system will display the TNM classification and final cancer stage
        
        Note: Currently supports .txt files only. Make sure reports contain clear TNM staging information.
        """)

if __name__ == "__main__":
    main() 