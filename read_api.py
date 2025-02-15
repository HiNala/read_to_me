#!/usr/bin/env python3
"""
API Module - Handles Eleven Labs API communication
This module manages API calls and audio playback functionality.
"""

import os
import tempfile
import re
from typing import Optional, List, Tuple
from datetime import datetime
import json
from pathlib import Path
import requests
from urllib.parse import urlparse
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

# Output directory structure
BASE_OUTPUT_DIR = Path("outputs")

def process_urls(text: str) -> str:
    """
    Process URLs in text to make them more speech-friendly.
    
    Args:
        text (str): The input text containing URLs
        
    Returns:
        str: Text with processed URLs
    """
    # Regular expression for finding URLs
    url_pattern = r'https?://(?:www\.)?([^\s<>\[\]]+)'
    
    def url_replacer(match):
        url = match.group(0)
        parsed = urlparse(url)
        
        # Extract domain without www and extension
        domain = parsed.netloc.replace('www.', '')
        
        # Handle common domains specially
        if 'github.com' in domain:
            return f"GitHub at {domain}{parsed.path}"
        elif 'youtube.com' in domain or 'youtu.be' in domain:
            return f"YouTube video at {domain}{parsed.path}"
        elif 'linkedin.com' in domain:
            return f"LinkedIn profile at {domain}{parsed.path}"
        elif 'twitter.com' in domain or 'x.com' in domain:
            return f"Twitter post at {domain}{parsed.path}"
        
        # For other URLs, make them more readable
        if parsed.path and parsed.path != '/':
            return f"website {domain} at path {parsed.path}"
        else:
            return f"website {domain}"
    
    # Replace URLs in text
    processed_text = re.sub(url_pattern, url_replacer, text)
    
    # Make common web terms more speech-friendly
    replacements = {
        'http://': 'H T T P',
        'https://': 'H T T P S',
        '.com': ' dot com',
        '.org': ' dot org',
        '.net': ' dot net',
        '.edu': ' dot edu',
        '.gov': ' dot gov',
        '.io': ' dot I O',
        '/': ' slash ',
        '@': ' at ',
        '_': ' underscore '
    }
    
    for old, new in replacements.items():
        processed_text = processed_text.replace(old, new)
    
    return processed_text

def create_run_directory() -> Tuple[Path, str]:
    """
    Create a timestamped directory for this run.
    
    Returns:
        Tuple[Path, str]: (Path to run directory, timestamp string)
    """
    # Ensure base output directory exists
    BASE_OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Create timestamped directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = BASE_OUTPUT_DIR / f"run_{timestamp}"
    run_dir.mkdir(exist_ok=True)
    
    return run_dir, timestamp

def save_text_info(text: str, run_dir: Path, timestamp: str, audio_files: List[str]):
    """
    Save input text and metadata to a JSON file.
    
    Args:
        text (str): Original input text
        run_dir (Path): Directory for this run
        timestamp (str): Run timestamp
        audio_files (List[str]): List of generated audio files
    """
    info = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text_length": len(text),
        "audio_files": audio_files,
        "text_content": text
    }
    
    info_path = run_dir / "text_info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

def split_text(text: str) -> List[str]:
    """
    Split text into chunks that respect sentence boundaries and API limits.
    
    Args:
        text (str): The text to split
        
    Returns:
        List[str]: List of text chunks
    """
    # Process URLs before splitting
    text = process_urls(text)
    
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

    # Create run directory
    run_dir, timestamp = create_run_directory()
    print(f"\n📁 Created output directory: {run_dir}")

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

    # Store all audio segments and filenames
    all_audio_segments = []
    audio_files = []
    
    for i, chunk in enumerate(chunks, 1):
        if total_chunks > 1:
            print(f"\n🔄 Processing part {i} of {total_chunks}...")
            chunk_filename = f"part_{i:02d}.mp3"
        else:
            chunk_filename = "audio.mp3"
        
        audio_path = run_dir / chunk_filename
        audio_files.append(chunk_filename)
        
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

            # Save the audio chunk directly
            with open(audio_path, "wb") as f:
                f.write(response.content)

            # Load the audio segment for playback
            audio_segment = AudioSegment.from_mp3(audio_path)
            all_audio_segments.append(audio_segment)

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
        # Save text information
        save_text_info(text, run_dir, timestamp, audio_files)
        
        # Combine all audio segments if there are multiple chunks
        if len(all_audio_segments) > 1:
            print("\n🔄 Combining audio segments...")
            combined_audio = sum(all_audio_segments)
            combined_path = run_dir / "combined.mp3"
            combined_audio.export(combined_path, format="mp3")
            audio_files.append("combined.mp3")
            
            # Update the info file with the combined audio
            save_text_info(text, run_dir, timestamp, audio_files)
            
            print("\n🔊 Playing combined audio...")
            play(combined_audio)
        else:
            print("\n🔊 Playing audio...")
            play(all_audio_segments[0])
        
        print(f"\n💾 All files saved in: {run_dir}")
        return True

    except Exception as e:
        print(f"\n❌ Error playing audio: {str(e)}")
        return None 