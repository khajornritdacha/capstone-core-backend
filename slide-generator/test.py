import requests
import sys

# Configuration
URL = "http://localhost:5000/generate"
OUTPUT_FILE = "test_presentation.pdf"

# Sample Marp Markdown
markdown_payload = """---
marp: true
theme: default
paginate: true
backgroundColor: #f0f0f0
---

# 🟢 Integration Test Successful!
## The Slide Generator is Online

**Status:** Operational
**Service:** Python + Marp CLI (Dockerized)

---

# Why this works

If you are seeing this PDF, it means:

1. The Python server received your JSON request.
2. It saved the Markdown to a temporary file.
3. It successfully called the `marp` executable.
4. Chromium (headless) generated this PDF.
5. The binary data was streamed back to you.

---

# Next Steps

You can now connect this microservice to **n8n** using the HTTP Request Node.

```json
{
  "service": "slide_generator",
  "port": 5000,
  "endpoint": "/generate"
}```
"""

def run_test(): 
    print(f"🚀 Sending request to {URL}...")
    try:
        response = requests.post(
            URL, 
            json={"markdown": markdown_payload},
            timeout=30  # Wait up to 30 seconds for PDF generation
        )
        
        # Check if the request was successful (HTTP 200)
        if response.status_code == 200:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            print(f"✅ Success! PDF saved to: {OUTPUT_FILE}")
            print("   Please open the file to verify the content.")
        else:
            print(f"❌ Failed with Status Code: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the service.")
        print("   Is the Docker container running? Check with: docker ps")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__": 
    run_test()
