#!/usr/bin/env python3
"""
API Module - Handles Eleven Labs API communication
This module manages API calls and audio playback functionality.
"""

import os
import tempfile
from typing import Optional, List
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

# Load environment variables
load_dotenv()
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# API Configuration
API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Default voice
DEFAULT_MODEL = "eleven_multilingual_v2"
MAX_CHARS_PER_CHUNK = 4000  # Safe limit to stay under the 10,000 credit limit

def split_text(text: str) -> List[str]:
    """
    Split text into chunks that respect sentence boundaries and API limits.
    
    Args:
        text (str): The text to split
        
    Returns:
        List[str]: List of text chunks
    """
    # Split text into sentences (basic implementation)
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        # Add period back and space for readability
        sentence = sentence.strip() + '. '
        sentence_length = len(sentence)
        
        if current_length + sentence_length > MAX_CHARS_PER_CHUNK:
            if current_chunk:  # Save current chunk if it exists
                chunks.append(''.join(current_chunk))
                current_chunk = []
                current_length = 0
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(''.join(current_chunk))
    
    return chunks

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

    # Split text into manageable chunks
    chunks = split_text(text)
    total_chunks = len(chunks)
    
    if total_chunks > 1:
        print(f"\n📝 Text will be processed in {total_chunks} parts...")
    
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }

    # Store all audio segments
    all_audio_segments = []
    
    for i, chunk in enumerate(chunks, 1):
        if total_chunks > 1:
            print(f"\n🔄 Processing part {i} of {total_chunks}...")
        
        payload = {
            "text": chunk,
            "model_id": DEFAULT_MODEL,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        try:
            print("\n📡 Sending request to Eleven Labs API...")
            response = requests.post(
                f"{API_URL}/{DEFAULT_VOICE_ID}",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 400:
                error_data = response.json()
                print(f"\n❌ API Error: {error_data}")
                return None
                
            response.raise_for_status()

            # Create a temporary file for the audio chunk
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            # Load the audio segment
            audio_segment = AudioSegment.from_mp3(temp_file_path)
            all_audio_segments.append(audio_segment)
            
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

        except requests.exceptions.RequestException as e:
            print(f"\n❌ API Error: {str(e)}")
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    print(f"Details: {error_data}")
                except:
                    pass
            return None
        except Exception as e:
            print(f"\n❌ Error processing audio: {str(e)}")
            return None

    try:
        # Combine all audio segments
        if all_audio_segments:
            print("\n🔊 Playing generated audio...")
            combined_audio = sum(all_audio_segments)
            play(combined_audio)
            return True
        return None

    except Exception as e:
        print(f"\n❌ Error playing audio: {str(e)}")
        return None 