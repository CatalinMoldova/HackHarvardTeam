#!/usr/bin/env python3
"""
Minimal setup script for 11Labs Speech-to-Text API
This script installs only the essential packages to avoid Windows Long Path issues
"""

import subprocess
import sys
import os

def install_minimal_packages():
    """Install only the essential packages"""
    print("Installing minimal required packages...")
    
    # Install packages one by one with specific versions to avoid conflicts
    packages = [
        "requests>=2.31.0",
        "python-dotenv>=1.0.0"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--user", "--no-deps"
            ])
            print(f"Success: {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {package}: {e}")
            # Continue with other packages
    
    # Try to install elevenlabs with minimal dependencies
    try:
        print("Installing elevenlabs (minimal)...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "elevenlabs", "--user", "--no-deps"
        ])
        print("Success: elevenlabs installed")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to install elevenlabs: {e}")
        print("You may need to install it manually later")
    
    return True

def create_basic_env():
    """Create basic .env file"""
    if not os.path.exists(".env"):
        print("Creating .env file...")
        try:
            with open(".env", "w") as f:
                f.write("ELEVENLABS_API_KEY=your_api_key_here\n")
            print("Success: .env file created")
            print("Please edit .env file and add your ELEVENLABS_API_KEY")
            return True
        except Exception as e:
            print(f"Failed to create .env file: {e}")
            return False
    else:
        print("Success: .env file already exists")
        return True

def create_simple_client():
    """Create a simple client that works without complex dependencies"""
    print("Creating simple client...")
    
    client_code = '''import requests
import os
from typing import Dict, Any

class SimpleElevenLabsClient:
    """Simple 11Labs client without complex dependencies"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def speech_to_text(self, audio_file_path: str) -> Dict[str, Any]:
        """Convert speech to text using 11Labs API"""
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        url = f"{self.base_url}/speech-to-text"
        headers = {"xi-api-key": self.api_key}
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {'audio': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')}
                data = {'model': 'scribe_v1'}
                
                response = requests.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("text", ""),
                    "model": "scribe_v1",
                    "language": result.get("language", "en"),
                    "timestamps": result.get("timestamps", []),
                    "speakers": result.get("speakers", [])
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    client = SimpleElevenLabsClient()
    print("Simple 11Labs client created successfully!")
    print("Add your API key to .env file and test with an audio file.")
'''
    
    try:
        with open("simple_client.py", "w") as f:
            f.write(client_code)
        print("Success: simple_client.py created")
        return True
    except Exception as e:
        print(f"Failed to create simple client: {e}")
        return False

def main():
    """Main setup function"""
    print("=== 11Labs Speech-to-Text API Minimal Setup ===\\n")
    
    # Install minimal packages
    install_minimal_packages()
    print()
    
    # Create .env file
    create_basic_env()
    print()
    
    # Create simple client
    create_simple_client()
    print()
    
    print("=== Minimal Setup Complete ===")
    print("Next steps:")
    print("1. Edit .env file and add your ELEVENLABS_API_KEY")
    print("2. Test with: python simple_client.py")
    print("3. Use the SimpleElevenLabsClient class in your code")
    
    return True

if __name__ == "__main__":
    main()
