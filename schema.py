from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Hospital(BaseModel):
    name: str = ""
    registration_number: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    pin: str = ""
    email: str = ""
    phone: str = ""

class Doctor(BaseModel):
    name: str = "doctor"
    registration_number: str = ""
    department: str = ""
    designation: str = "doctor"
    qualification: str = "MBBS"
    email: str = ""
    phone: str = ""

class Patient(BaseModel):
    name: str = ""
    dob: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    pin: str = ""
    tpa_id: str = ""
    employee_id: str = ""
    company_name: str = ""
    pan_card: str = ""
    aadhar_card: str = ""
    phone: str = ""
    email: str = ""

class Claim(BaseModel):
    doa: str = ""
    dod: str = ""
    total_claimed_amount: str = ""

class Invoice(BaseModel):
    invoice_date: str = ""
    bill_group: str = ""
    bill_category: str = ""
    amount: str = ""
    bill_number: str = ""
    discount: str = ""
    quantity: str = ""
    remarks: str = ""

class PatientAddress(BaseModel):
    address: str = ""
    city: str = ""
    state: str = ""
    pinCode: str = ""

class OPDDetails(BaseModel):
    reportingComplaint: List[str] = ["", ""]
    diagnosis: List[str] = ["", ""]
    investigations: List[str] = ["", ""]
    pharmacy: List[dict] = Field(default_factory=lambda: [
        {"name": "", "dosageFrequencyPerDay": 0, "dosagefrequencyTotalDays": 0, "count": 0},
        {"name": "", "dosageFrequencyPerDay": 0, "dosagefrequencyTotalDays": 0, "count": 0}
    ])

class PatientBankInfo(BaseModel):
    bank_name: str = ""
    account_number: str = ""
    bank_address: str = ""
    ifsi_code: str = ""

class MedicalHistory(BaseModel):
    Disease1: str = ""
    Disease2: str = ""

class DiagnosisItem(BaseModel):
    name: str
    icd: str

class RoomInvoice(BaseModel):
    room_type: str = ""
    room_category: str = ""
    start_date: str = ""
    end_date: str = ""
    rate: str = ""
    quantity: str = ""
    discount: str = ""
    total_days: str = ""
    total_room_amount: str = ""

class MedicalDetails(BaseModel):
    dischargeType: str = ""
    patientAddress: PatientAddress = PatientAddress()
    opd_details: OPDDetails = OPDDetails()
    Patient_bankinfo: PatientBankInfo = PatientBankInfo()
    medicalhistory: MedicalHistory = MedicalHistory()
    current_medications: Dict = Field(default_factory=dict)
    allergies: Dict = Field(default_factory=dict)
    diagnosis: List[DiagnosisItem] = []
    symptoms: List[str] = []
    treatment_taken: str = ""

class ExtractedData(BaseModel):
    hospital: Hospital = Hospital()
    doctor: Doctor = Doctor()
    patient: Patient = Patient()
    claim: Claim = Claim()
    invoices: List[Invoice] = []
    medicalDetails: MedicalDetails = MedicalDetails()
    room_invoice: List[RoomInvoice] = []

class ResponseJSON(BaseModel):
    data: ExtractedData
    message: str = "Success"
    success: bool = True
