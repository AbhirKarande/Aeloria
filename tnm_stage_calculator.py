from dataclasses import dataclass
from typing import Optional
from groq import Groq
import re

@dataclass
class TNMClassification:
    t_stage: str
    n_stage: str
    m_stage: str

class ReportParser:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        # Load TNM categorization rules
        self.tnm_rules = self._load_tnm_rules()

    def _load_tnm_rules(self) -> dict:
        with open("tnm-categorization-lung.txt", "r") as f:
            rules_text = f.read()
        return {
            "rules_text": rules_text
        }

    def parse_report(self, report_text: str) -> TNMClassification:
        prompt = f"""
        You are a medical report analyzer specializing in lung cancer staging. Using the TNM classification rules below, 
        analyze the medical report and determine the appropriate T, N, and M stages.

        TNM Classification Rules:
        {self.tnm_rules['rules_text']}

        Based on these rules, analyze the following medical report and extract or infer the TNM classification.
        Return only the T, N, and M stages in the format: T2b,N1,M0
        If you cannot determine a specific stage, use the most conservative (higher) stage that matches the description.

        Medical Report:
        {report_text}
        """

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical report analyzer specializing in lung cancer TNM staging."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0,
        )

        # Parse the response
        tnm_str = response.choices[0].message.content.strip()
        
        # Enhanced pattern to handle more variations
        tnm_pattern = r'([T][0-4][a-c]?|TX|T0|Tis),\s*([N][0-3]|NX),\s*([M][0-1][a-c]?|MX)'
        match = re.search(tnm_pattern, tnm_str)
        
        if match:
            t, n, m = match.groups()
            return TNMClassification(t_stage=t.strip(), n_stage=n.strip(), m_stage=m.strip())
        else:
            raise ValueError("Could not determine TNM classification from the report")

class CancerStageMapper:
    def __init__(self):
        # This mapping should be populated based on the TNM staging rules
        self.stage_mapping = {
            # Example mappings (these should be completed based on full staging rules)
            ('T1a', 'N0', 'M0'): 'IA1',
            ('T1b', 'N0', 'M0'): 'IA2',
            ('T2b', 'N1', 'M0'): 'IIB',
            ('T4', 'N2', 'M0'): 'IIIC',
            ('Any T', 'Any N', 'M1a'): 'IVA',
            ('Any T', 'Any N', 'M1b'): 'IVB',
            ('Any T', 'Any N', 'M1c'): 'IVB',
            ('T1a-c', 'N3', 'M0'): 'IIIB',
            ('T2a-b', 'N3', 'M0'): 'IIIB',
            ('T3', 'N2', 'M0'): 'IIIB',
            ('T4', 'N2', 'M0'): 'IIIB',
            ('T4', 'N3', 'M0'): 'IIIC',
            ('T1a-c', 'N2', 'M0'): 'IIIA',
            ('T2a-b', 'N2', 'M0'): 'IIIA',
            ('T3', 'N1', 'M0'): 'IIIA',
            ('T4', 'N0', 'M0'): 'IIIA',
            ('T4', 'N1', 'M0'): 'IIIA',
            ('T1a-c', 'N3', 'M0'): 'IIIB',
            ('T2a-b', 'N3', 'M0'): 'IIIB',
            ('T3', 'N2', 'M0'): 'IIIB',
            ('T4', 'N2', 'M0'): 'IIIB',
            ('T4', 'N3', 'M0'): 'IIIC',
            ('T1a', 'N0', 'M1a'): 'IVA',
            ('T1a', 'N0', 'M1b'): 'IVB',
            ('T1a', 'N0', 'M1c'): 'IVB',
            ('T1a', 'N1', 'M1a'): 'IVA',
            ('T1a', 'N1', 'M1b'): 'IVB',
            ('T1a', 'N1', 'M1c'): 'IVB',
            ('T1a', 'N2', 'M1a'): 'IVA',
            ('T1a', 'N2', 'M1b'): 'IVB',
            ('T1a', 'N2', 'M1c'): 'IVB',
            ('T1a', 'N3', 'M1a'): 'IVA',
            ('T1a', 'N3', 'M1b'): 'IVB',
            ('T1a', 'N3', 'M1c'): 'IVB',
            ('T1b', 'N0', 'M1a'): 'IVA',
            ('T1b', 'N0', 'M1b'): 'IVB',
            ('T1b', 'N0', 'M1c'): 'IVB',
            ('T1b', 'N1', 'M1a'): 'IVA',
            ('T1b', 'N1', 'M1b'): 'IVB',
            ('T1b', 'N1', 'M1c'): 'IVB',
            ('T1b', 'N2', 'M1a'): 'IVA',
            ('T1b', 'N2', 'M1b'): 'IVB',
            ('T1b', 'N2', 'M1c'): 'IVB',
            ('T1b', 'N3', 'M1a'): 'IVA',
            ('T1b', 'N3', 'M1b'): 'IVB',
            ('T1b', 'N3', 'M1c'): 'IVB',
            ('T1c', 'N0', 'M1a'): 'IVA',
            ('T1c', 'N0', 'M1b'): 'IVB',
            ('T1c', 'N0', 'M1c'): 'IVB',
            ('T1c', 'N1', 'M1a'): 'IVA',
            ('T1c', 'N1', 'M1b'): 'IVB',
            ('T1c', 'N1', 'M1c'): 'IVB',
            ('T1c', 'N2', 'M1a'): 'IVA',
            ('T1c', 'N2', 'M1b'): 'IVB',
            ('T1c', 'N2', 'M1c'): 'IVB',
            ('T1c', 'N3', 'M1a'): 'IVA',
            ('T1c', 'N3', 'M1b'): 'IVB',
            ('T1c', 'N3', 'M1c'): 'IVB',
            ('T2a', 'N0', 'M1a'): 'IVA',
            ('T2a', 'N0', 'M1b'): 'IVB',
            ('T2a', 'N0', 'M1c'): 'IVB',
            ('T2a', 'N1', 'M1a'): 'IVA',
            ('T2a', 'N1', 'M1b'): 'IVB',
            ('T2a', 'N1', 'M1c'): 'IVB',
            ('T2a', 'N2', 'M1a'): 'IVA',
            ('T2a', 'N2', 'M1b'): 'IVB',
            ('T2a', 'N2', 'M1c'): 'IVB',
            ('T2a', 'N3', 'M1a'): 'IVA',
            ('T2a', 'N3', 'M1b'): 'IVB',
            ('T2a', 'N3', 'M1c'): 'IVB',
            ('T2b', 'N0', 'M1a'): 'IVA',
            ('T2b', 'N0', 'M1b'): 'IVB',
            ('T2b', 'N0', 'M1c'): 'IVB',
            ('T2b', 'N1', 'M1a'): 'IVA',
            ('T2b', 'N1', 'M1b'): 'IVB',
            ('T2b', 'N1', 'M1c'): 'IVB',
            ('T2b', 'N2', 'M1a'): 'IVA',
            ('T2b', 'N2', 'M1b'): 'IVB',
            ('T2b', 'N2', 'M1c'): 'IVB',
            ('T2b', 'N3', 'M1a'): 'IVA',
            ('T2b', 'N3', 'M1b'): 'IVB',
            ('T2b', 'N3', 'M1c'): 'IVB',
            ('T3', 'N0', 'M1a'): 'IVA',
            ('T3', 'N0', 'M1b'): 'IVB',
            ('T3', 'N0', 'M1c'): 'IVB',
            ('T3', 'N1', 'M1a'): 'IVA',
            ('T3', 'N1', 'M1b'): 'IVB',
            ('T3', 'N1', 'M1c'): 'IVB',
            ('T3', 'N2', 'M1a'): 'IVA',
            ('T3', 'N2', 'M1b'): 'IVB',
            ('T3', 'N2', 'M1c'): 'IVB',
            ('T3', 'N3', 'M1a'): 'IVA',
            ('T3', 'N3', 'M1b'): 'IVB',
            ('T3', 'N3', 'M1c'): 'IVB',
            ('T4', 'N0', 'M1a'): 'IVA',
            ('T4', 'N0', 'M1b'): 'IVB',
            ('T4', 'N0', 'M1c'): 'IVB',
            ('T4', 'N1', 'M1a'): 'IVA',
            ('T4', 'N1', 'M1b'): 'IVB',
            ('T4', 'N1', 'M1c'): 'IVB',
            ('T4', 'N2', 'M1a'): 'IVA',
            ('T4', 'N2', 'M1b'): 'IVB',
            ('T4', 'N2', 'M1c'): 'IVB',
            ('T4', 'N3', 'M1a'): 'IVA',
            ('T4', 'N3', 'M1b'): 'IVB',
            ('T4', 'N3', 'M1c'): 'IVB',
        }

    def get_stage(self, tnm: TNMClassification) -> str:
        key = (tnm.t_stage, tnm.n_stage, tnm.m_stage)
        return self.stage_mapping.get(key, "Unknown")

def process_medical_reports(ct_report: str, pet_report: str, groq_api_key: str) -> dict:
    parser = ReportParser(groq_api_key)
    mapper = CancerStageMapper()

    # Parse both reports and combine the information
    ct_tnm = parser.parse_report(ct_report)
    pet_tnm = parser.parse_report(pet_report)

    # Combine the TNM classifications (taking the higher stage when there's a discrepancy)
    final_tnm = TNMClassification(
        t_stage=max(ct_tnm.t_stage, pet_tnm.t_stage),
        n_stage=max(ct_tnm.n_stage, pet_tnm.n_stage),
        m_stage=max(ct_tnm.m_stage, pet_tnm.m_stage)
    )

    # Map to cancer stage
    cancer_stage = mapper.get_stage(final_tnm)
    
    # Return a dictionary instead of a string
    return {
        "tnm": final_tnm,
        "stage": cancer_stage
    }

# Example usage:
if __name__ == "__main__":
    groq_api_key = "your-groq-api-key"
    
    with open("sample-ct-imaging-report.txt", "r") as f:
        ct_report = f.read()
    
    with open("sample-pet-scan-report.txt", "r") as f:
        pet_report = f.read()
    
    result = process_medical_reports(ct_report, pet_report, groq_api_key)
    print(result) 