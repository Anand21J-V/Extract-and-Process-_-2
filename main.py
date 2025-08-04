import json
import os
import re
from utils import build_prompt
from model_runner import call_ollama
from schema import ResponseJSON


def sanitize_types(data: dict) -> dict:
    # Fix numeric values in invoices
    for bill in data.get("invoices", []):
        for key in ["amount", "discount", "quantity", "bill_number"]:
            if key in bill and not isinstance(bill[key], str):
                bill[key] = str(bill[key])

    # Fix room_invoice numbers
    for room in data.get("room_invoice", []):
        for key in ["rate", "quantity", "discount", "total_days", "total_room_amount"]:
            if key in room and not isinstance(room[key], str):
                room[key] = str(room[key])

    # Convert pharmacy dosage/count fields to strings
    pharmacy_items = (
        data.get("medicalDetails", {})
        .get("opd_details", {})
        .get("pharmacy", [])
    )
    for med in pharmacy_items:
        for key in ["dosageFrequencyPerDay", "dosagefrequencyTotalDays", "count"]:
            if key in med and not isinstance(med[key], str):
                med[key] = str(med[key])

    return data


def ensure_required_fields(data: dict) -> dict:
    # Ensure doctor.qualification exists
    if "qualification" not in data.get("doctor", {}):
        data["doctor"]["qualification"] = ""

    # Ensure room_invoice exists
    if "room_invoice" not in data:
        data["room_invoice"] = []

    # Ensure allergies is dict
    if isinstance(data.get("medicalDetails", {}).get("allergies"), list):
        data["medicalDetails"]["allergies"] = {}

    # Ensure current_medications is dict
    if isinstance(data.get("medicalDetails", {}).get("current_medications"), list):
        data["medicalDetails"]["current_medications"] = {}

    # Ensure opd_details is dict (not list)
    if isinstance(data.get("medicalDetails", {}).get("opd_details"), list):
        opd = data["medicalDetails"]["opd_details"]
        data["medicalDetails"]["opd_details"] = opd[0] if opd else {}

    return data


# Step 1: Read OCR Text
with open("ritika/output.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
print("📄 OCR Text Sample:\n", raw_text[:500])

# Step 2: Build Prompt
prompt = build_prompt(raw_text)
print("\n🧾 Prompt Sample:\n", prompt[:500])
print("📏 Prompt length:", len(prompt))

# Step 3: Send to Ollama LLM
print("\n🧠 Sending prompt to Ollama...")
try:
    response = call_ollama(prompt)
except ConnectionError as e:
    print(f"❌ Failed to get a response from Ollama: {e}")
    exit()

# Step 4: Clean up LLM response and extract JSON
response_cleaned = response.strip()

# Remove Markdown-like code fences
response_cleaned = re.sub(r"^```(?:json)?", "", response_cleaned, flags=re.IGNORECASE)
response_cleaned = re.sub(r"```$", "", response_cleaned, flags=re.IGNORECASE)

# Remove intros like "Here is the JSON:"
response_cleaned = re.sub(
    r"(?i)^Here is (the )?(extracted )?(data|json|structured output)[^:{\[]*[:\-\n]+", "", 
    response_cleaned
).strip()

# Fix malformed LLM constructs before JSON parsing
# Convert Python-style set to JSON array for 'allergies'
response_cleaned = re.sub(r'"allergies"\s*:\s*{([^}]+)}', r'"allergies": [\1]', response_cleaned)

# Convert treatment_taken from list to flat string if needed
response_cleaned = re.sub(
    r'"treatment_taken"\s*:\s*\[(.*?)\]',
    lambda m: '"treatment_taken": ' + json.dumps(" ".join(re.findall(r'"(.*?)"', m.group(1)))),
    response_cleaned,
    flags=re.DOTALL
)

# Try to extract JSON block
match = re.search(r"({.*})", response_cleaned, flags=re.DOTALL)
if match:
    response_cleaned = match.group(1)
else:
    print("❌ Failed to extract JSON block.")
    print("🔍 Raw response:\n", response)
    exit()

print("\n🧠 Cleaned LLM JSON Preview:\n", response_cleaned[:500])

# Step 5: Check if response is still empty
if not response_cleaned:
    print("❌ Empty response from LLM after cleaning. Exiting.")
    exit()

# Step 6: Parse and Validate using Pydantic
try:
    json_data = json.loads(response_cleaned)
    json_data["data"] = sanitize_types(json_data["data"])
    json_data["data"] = ensure_required_fields(json_data["data"])
    validated = ResponseJSON(**json_data)
except json.JSONDecodeError as jde:
    print("❌ JSON Decode Error:", jde)
    print("🔍 Raw cleaned response:\n", response_cleaned)
    exit()
except Exception as e:
    print("❌ Pydantic Validation Failed:", e)
    print("🔍 JSON block that failed:\n", json_data if 'json_data' in locals() else response_cleaned)
    exit()

# Step 7: Save structured JSON
output_path = "ritika/result_ritika.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(validated.dict(), f, indent=2)
print("\n✅ Final structured JSON saved to", output_path)
