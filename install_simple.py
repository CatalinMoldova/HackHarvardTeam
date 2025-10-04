#!/usr/bin/env python3
"""
Simple installation script for 11Labs Speech-to-Text API
This script avoids the numpy compilation issues by using pre-built wheels
"""

import subprocess
import sys
import os

def install_core_packages():
    """Install core packages without problematic dependencies"""
    print("Installing core packages...")
    
    packages = [
        "elevenlabs",
        "python-dotenv", 
        "requests",
        "pydub"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Success: {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")
            return False
    
    return True

def install_audio_packages():
    """Install audio processing packages with fallbacks"""
    print("Installing audio processing packages...")
    
    # Try to install numpy with pre-built wheel
    try:
        print("Installing numpy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "--only-binary=all"])
        print("Success: numpy installed successfully")
    except subprocess.CalledProcessError:
        print("⚠ numpy installation failed, trying alternative...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.26.4", "--only-binary=all"])
            print("Success: numpy installed successfully (alternative version)")
        except subprocess.CalledProcessError:
            print("⚠ numpy installation failed, continuing without it...")
    
    # Try to install soundfile
    try:
        print("Installing soundfile...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "soundfile", "--only-binary=all"])
        print("Success: soundfile installed successfully")
    except subprocess.CalledProcessError:
        print("⚠ soundfile installation failed, continuing without it...")
    
    return True

def create_env_file():
    """Create .env file"""
    if not os.path.exists(".env"):
        print("Creating .env file...")
        try:
            with open(".env", "w") as f:
                f.write("ELEVENLABS_API_KEY=your_api_key_here\n")
            print("Success: .env file created")
            print("⚠ Please edit .env file and add your ELEVENLABS_API_KEY")
            return True
        except Exception as e:
            print(f"✗ Failed to create .env file: {e}")
            return False
    else:
        print("Success: .env file already exists")
        return True

def test_imports():
    """Test if core modules can be imported"""
    print("Testing imports...")
    try:
        import elevenlabs
        print("Success: elevenlabs imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import elevenlabs: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("Success: python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import requests
        print("Success: requests imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        return False
    
    return True

def main():
    """Main installation function"""
    print("=== 11Labs Speech-to-Text API Simple Setup ===\n")
    
    # Install core packages
    if not install_core_packages():
        print("Setup failed at core packages installation")
        return False
    
    print()
    
    # Install audio packages (with fallbacks)
    install_audio_packages()
    
    print()
    
    # Create .env file
    if not create_env_file():
        print("Setup failed at .env file creation")
        return False
    
    print()
    
    # Test imports
    if not test_imports():
        print("Setup completed with warnings - some packages may not be available")
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
