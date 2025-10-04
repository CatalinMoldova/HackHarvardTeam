#!/usr/bin/env python3
"""
Test script to check 11Labs API endpoints
"""

import requests
import os
from dotenv import load_dotenv

def test_api_endpoints():
    """Test different possible API endpoints"""
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: API key not found")
        return
    
    base_url = "https://api.elevenlabs.io/v1"
    headers = {"xi-api-key": api_key}
    
    # Test different endpoints
    endpoints = [
        "/models",
        "/user",
        "/speech-to-text",
        "/transcribe",
        "/speech-to-text/transcribe"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\nTesting: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Success! Response: {response.json()}")
            else:
                print(f"Error: {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_api_endpoints()
