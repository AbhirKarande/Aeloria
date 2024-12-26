import streamlit as st
import os
from tnm_stage_calculator import process_medical_reports

def main():
    st.title("TNM Stage Calculator")
    st.write("Upload CT and PET scan reports to determine cancer staging")

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
            
        groq_api_key = "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"

        if st.button("Analyze Reports"):
            with st.spinner("Analyzing reports..."):
                try:
                    # Process the reports
                    result = process_medical_reports(
                        ct_report=all_reports,
                        pet_report=all_reports,
                        groq_api_key=groq_api_key
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