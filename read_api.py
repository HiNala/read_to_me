#!/usr/bin/env python3
"""
API Module - Handles Eleven Labs API communication
This module manages API calls and audio playback functionality.
"""

import os
import tempfile
from typing import Optional
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

# Load environment variables
load_dotenv()
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# API Configuration
API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
DEFAULT_MODEL = "eleven_monolingual_v1"

def text_to_speech(text: str) -> Optional[bool]:
    """
    Send text to Eleven Labs API and play the generated audio.
    
    Args:
        text (str): The text to convert to speech
        
    Returns:
        Optional[bool]: True if successful, None if failed
    """
    
    if not ELEVEN_LABS_API_KEY:
        print("\n❌ API key missing! Set ELEVEN_LABS_API_KEY in your .env file.")
        return None

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": DEFAULT_MODEL,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    try:
        print("\n📡 Sending request to Eleven Labs API...")
        response = requests.post(
            f"{API_URL}/{DEFAULT_VOICE_ID}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        print("\n🔊 Playing generated audio...")
        try:
            audio = AudioSegment.from_mp3(temp_file_path)
            play(audio)
            return True
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {str(e)}")
        return None
    except Exception as e:
        print(f"\n❌ Error playing audio: {str(e)}")
        return None 