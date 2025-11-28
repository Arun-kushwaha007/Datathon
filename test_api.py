import requests
import json

def test_api():
    url = "http://localhost:8000/extract-bill-data"
    
    # Use one of the sample URLs from the prompt or a dummy one if we want to test local files
    # The prompt gave a sample request body with a URL.
    # We can also use a local file if we modify the API to accept bytes, but the requirement is a URL.
    # For testing, I'll use the URL from the prompt sample.
    payload = {
        "document": "http://localhost:8001/TRAINING_SAMPLES/train_sample_2.pdf"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
