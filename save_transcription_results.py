#!/usr/bin/env python3
"""
Save 11Labs Speech-to-Text results to a file
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def save_transcription_to_file():
    """Transcribe audio and save results to a file"""
    print("=== 11Labs Speech-to-Text API - Save Results ===")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: ELEVENLABS_API_KEY not found in .env file")
        return
    
    # Check if audio file exists
    audio_file = "TestAudioFileAPI.m4a"
    if not os.path.exists(audio_file):
        print(f"ERROR: Audio file not found: {audio_file}")
        return
    
    print(f"Processing: {audio_file}")
    
    # Transcribe the audio
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": api_key}
    
    try:
        with open(audio_file, 'rb') as audio_file_obj:
            files = {'file': (audio_file, audio_file_obj, 'audio/mp4')}
            data = {
                'model_id': 'scribe_v1',
                'tag_audio_events': 'true',
                'language_code': 'eng',
                'diarize': 'true'
            }
            
            print("Transcribing audio...")
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # Create timestamp for filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save full results to JSON file
                json_filename = f"transcription_results_{timestamp}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                # Save just the text to a text file
                txt_filename = f"transcription_text_{timestamp}.txt"
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(f"Transcription Results - {datetime.now()}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Text: {result['text']}\n\n")
                    f.write(f"Language: {result['language_code']}\n")
                    f.write(f"Confidence: {result['language_probability']}\n")
                    f.write(f"Transcription ID: {result['transcription_id']}\n\n")
                    f.write("Word-level timestamps:\n")
                    f.write("-" * 30 + "\n")
                    for word in result['words']:
                        if word['type'] == 'word':
                            f.write(f"{word['start']:.3f}s - {word['end']:.3f}s: {word['text']} (Speaker: {word['speaker_id']})\n")
                
                print(f"✅ SUCCESS: Transcription completed!")
                print(f"📄 Full results saved to: {json_filename}")
                print(f"📝 Text saved to: {txt_filename}")
                print(f"📊 Transcribed text: {result['text']}")
                
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    save_transcription_to_file()
