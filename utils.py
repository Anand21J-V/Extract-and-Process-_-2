def build_prompt(text: str) -> str:
    return f"""
You are an expert medical information extractor.
Given the following unstructured OCR text, extract it into the predefined JSON structure described below.
If any field is missing, return it as an empty string or list.

--- Begin OCR Text ---
{text}
--- End OCR Text ---

Output a VALID JSON strictly matching this schema (ignore extra notes):

 {{
  "data": {{
    "hospital": {{
      "name": "", "registration_number": "", "address": "", "city": "", "state": "", "pin": "", "email": "", "phone": ""
    }},
    "doctor": {{
      "name": "", "registration_number": "", "department": "", "designation": "", "qualification": "", "email": "", "phone": ""
    }},
    "patient": {{
      "name": "", "dob": "", "address": "", "city": "", "state": "", "pin": "", "tpa_id": "", "employee_id": "", "company_name": "", "pan_card": "", "aadhar_card": "", "phone": "", "email": ""
    }},
    "claim": {{
      "doa": "", "dod": "", "total_claimed_amount": ""
    }},
    "invoices": [{{"invoice_date": "", "bill_group": "", "bill_category": "", "amount": "", "bill_number": "", "discount": "", "quantity": "", "remarks": ""}}],
    "medicalDetails": {{
      "dischargeType": "", "patientAddress": {{
        "address": "", "city": "", "state": "", "pinCode": ""
      }},
      "opd_details": {{
        "reportingComplaint": ["", ""],
        "diagnosis": ["", ""],
        "investigations": ["", ""],
        "pharmacy": [{{"name":"", "dosageFrequencyPerDay":0, "dosagefrequencyTotalDays":0, "count":0}}]
      }},
      "Patient_bankinfo": {{
        "bank_name": "", "account_number": "", "bank_address": "", "ifsi_code": ""
      }},
      "medicalhistory": {{"Disease1": "", "Disease2": ""}},
      "current_medications": {{}},
      "allergies": {{}},
      "diagnosis": [{{"name": "", "icd": ""}}],
      "symptoms": [""],
      "treatment_taken": ""
    }},
    "room_invoice": [{{"room_type": "", "room_category": "", "start_date": "", "end_date": "", "rate": "", "quantity": "", "discount": "", "total_days": "", "total_room_amount": ""}}]
  }},
  "message": "Success",
  "success": true
}}
"""
