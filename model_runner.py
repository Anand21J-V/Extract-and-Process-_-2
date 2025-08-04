# # model_runner.py
# import ollama

# def run_ollama_prompt(prompt: str, model: str = "mistral") -> str:
#     """
#     Sends a prompt to the local Ollama server using the specified model.

#     Args:
#         prompt (str): The user's input prompt.
#         model (str): The name of the model to use (e.g., "mistral").

#     Returns:
#         str: The generated response from the model.
#     """
#     try:
#         # Check if the Ollama server is running and the model is available
#         response = ollama.chat(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             options={"temperature": 0.3}
#         )
        
#         return response["message"]["content"]
    
#     except ollama.ResponseError as e:
#         print(f"❌ Error from Ollama: {e.error}")
#         if "model '" + model + "' not found" in e.error:
#             print(f"Please pull the model with 'ollama pull {model}'")
#         raise ConnectionError("Failed to connect to Ollama server or model not found.") from e
#     except Exception as e:
#         raise ConnectionError(f"An unexpected error occurred with Ollama: {e}") from e


import subprocess
import sys
import json

def call_ollama(prompt: str) -> str:
    process = subprocess.Popen(
        ["ollama", "run", "mistral"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'  # 🔥 Explicit encoding
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("⚠️ Ollama STDERR:", stderr, file=sys.stderr)
    return stdout

def extract_json_from_response(response: str) -> dict:
    start = response.find('{')
    end = response.rfind('}') + 1
    json_str = response[start:end]
    return json.loads(json_str)
