#!/usr/bin/env python3
"""
Read to Me CLI - Main Entry Point
This script orchestrates the interaction between CLI and API modules.
"""

import cli
import read_api

def main():
    """Main entry point for the Read to Me CLI application."""
    print("\n📖 Welcome to 'Read to Me' CLI! 🎙️")
    
    try:
        # Get user input (text or file path)
        text = cli.get_text_input()
        
        if text:
            print("\n🔄 Processing text and sending to Eleven Labs API...")
            read_api.text_to_speech(text)
        else:
            print("\n❌ No valid input provided. Exiting.")
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Read to Me CLI!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 