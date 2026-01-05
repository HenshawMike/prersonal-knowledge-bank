import os
import requests
from tqdm import tqdm

# Updated API endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L12-v2"
headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

def query(payload):
    try:
        with tqdm(desc="Querying API", unit="req") as pbar:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            pbar.update(1)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making request: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

# Test the API
test_payload = {
    "source_sentence": "That is a happy person",
    "sentences": [
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day"
    ]
}

print("🔍 Testing Hugging Face API...")
result = query(test_payload)

if result is not None:
    print("\n✅ Success! API Response:")
    print(result)
else:
    print("\n❌ Failed to get a valid response from the API")
    print("\nTroubleshooting steps:")
    print("1. Verify your HF_TOKEN is correct and has the right permissions")
    print("2. Check your internet connection")
    print("3. Try visiting: https://huggingface.co/settings/tokens to verify your token")
    print("4. Check if the model is available: https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2")