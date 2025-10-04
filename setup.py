#!/usr/bin/env python3
"""
Setup script for 11Labs Speech-to-Text API integration
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        # First, upgrade pip and setuptools to handle Python 3.13 compatibility
        print("Upgrading pip and setuptools for Python 3.13 compatibility...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        print("Trying alternative installation method...")
        try:
            # Try installing packages individually
            packages = [
                "elevenlabs>=1.0.0",
                "python-dotenv>=1.0.0", 
                "requests>=2.31.0",
                "pydub>=0.25.1",
                "soundfile>=0.12.1",
                "numpy>=1.26.0"
            ]
            for package in packages:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("✓ Requirements installed successfully (alternative method)")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"✗ Alternative installation also failed: {e2}")
            return False

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("Creating .env file from example...")
            try:
                with open(".env.example", "r") as src, open(".env", "w") as dst:
                    dst.write(src.read())
                print("✓ .env file created")
                print("⚠ Please edit .env file and add your ELEVENLABS_API_KEY")
                return True
            except Exception as e:
                print(f"✗ Failed to create .env file: {e}")
                return False
        else:
            print("⚠ .env.example not found, creating basic .env file...")
            try:
                with open(".env", "w") as f:
                    f.write("ELEVENLABS_API_KEY=your_api_key_here\n")
                print("✓ Basic .env file created")
                print("⚠ Please edit .env file and add your ELEVENLABS_API_KEY")
                return True
            except Exception as e:
                print(f"✗ Failed to create .env file: {e}")
                return False
    else:
        print("✓ .env file already exists")
        return True

def verify_setup():
    """Verify the setup is working"""
    print("Verifying setup...")
    try:
        from speech_to_text_service import SpeechToTextService
        from config import Config
        print("✓ Modules imported successfully")
        
        # Check if API key is configured
        if Config.ELEVENLABS_API_KEY and Config.ELEVENLABS_API_KEY != "your_api_key_here":
            print("✓ API key is configured")
            return True
        else:
            print("⚠ API key not configured - please set ELEVENLABS_API_KEY in .env file")
            return False
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Setup verification failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=== 11Labs Speech-to-Text API Setup ===\n")
    
    # Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation")
        return False
    
    print()
    
    # Create .env file
    if not create_env_file():
        print("Setup failed at .env file creation")
        return False
    
    print()
    
    # Verify setup
    if not verify_setup():
        print("Setup completed with warnings - please check configuration")
        return False
    
    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("1. Edit .env file and add your ELEVENLABS_API_KEY")
    print("2. Run: python example_usage.py")
    print("3. Start using the API!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
