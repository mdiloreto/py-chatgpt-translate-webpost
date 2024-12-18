import os
import requests

ENDPOINT = os.getenv("TEST_ENDPOINT", "http://localhost:5000")
AZURE_ENDPOINT = os.getenv("TEST_AZURE_ENDPOINT")
AZURE_CREDENTIALS = os.getenv("TEST_AZURE_CREDENTIALS")
URL = os.getenv("TEST_URL", "https://madsblog.net/2024/10/29/kubernetes-networking-parte-2/")

def test_translate_missing_body():
    response = requests.post(f"{ENDPOINT}/api/translate", json=None)
    assert response.status_code == 400, f"Expected 400, but got {response.status_code}"

def test_translate_valid_translator():
    payload = {
        "url": URL,
        "translator_api": "azure",
        "azure_endpoint": AZURE_ENDPOINT,
        "azure_credentials": AZURE_CREDENTIALS,
    }
    response = requests.post(f"{ENDPOINT}/api/translate", json=payload, timeout=3600)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response: {response.text}"

def test_translate_unsupported_translator():
    payload = {
        "url": URL,
        "translator_api": "unsupported",
    }
    response = requests.post(f"{ENDPOINT}/api/translate", json=payload, timeout=3600)
    assert response.status_code == 400, f"Expected 400, but got {response.status_code}"
    assert response.json()["error"] == "Translator 'unsupported' not supported by the API.", "Unexpected error message"