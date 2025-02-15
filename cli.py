#!/usr/bin/env python3
"""
CLI Module - Handles user input and file operations
This module provides functionality for text input and file reading.
"""

import os
from typing import Optional

def get_text_input() -> Optional[str]:
    """Prompt the user for text input or file path and return extracted text."""
    
    while True:
        choice = input("\nChoose input method:\n1️⃣ Paste text\n2️⃣ Provide file path\n> ").strip()

        if choice == "1":
            text = input("\n📝 Paste your text here:\n> ").strip()
            return text if text else None

        elif choice == "2":
            file_path = input("\n📂 Enter the file path:\n> ").strip()
            result = read_file(file_path)
            if result:
                return result
            # If file reading fails, the loop will continue
        
        else:
            print("\n❌ Invalid choice. Please enter '1' or '2'.")

def read_file(file_path: str) -> Optional[str]:
    """Read text from a .txt, .md, or .docx file."""
    
    if not os.path.exists(file_path):
        print("\n❌ File not found. Please check the path and try again.")
        return None

    _, ext = os.path.splitext(file_path)
    supported_extensions = {".txt", ".md", ".docx"}

    if ext not in supported_extensions:
        print(f"\n❌ Unsupported file format. Use one of: {', '.join(supported_extensions)}")
        return None

    try:
        if ext in {".txt", ".md"}:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    print("\n❌ File is empty.")
                    return None
                return content
                
        elif ext == ".docx":
            try:
                from docx import Document
            except ImportError:
                print("\n❌ python-docx package is required for .docx files.")
                return None
                
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs]).strip()
            if not content:
                print("\n❌ Document is empty.")
                return None
            return content

    except Exception as e:
        print(f"\n❌ Error reading file: {str(e)}")
        return None 