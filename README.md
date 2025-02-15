# Read to Me CLI 🎙️

A command-line tool that converts text to speech using Eleven Labs' Text-to-Speech (TTS) API. Simply paste text or provide a file, and listen to it being read aloud!

## Features ✨

- 📝 Direct text input support
- 📂 File reading support (`.txt`, `.md`, `.docx`)
- 🎯 High-quality text-to-speech using Eleven Labs API
- 🔊 Instant audio playback
- 🛡️ Secure API key management
- ⚡ Simple and intuitive interface
- 📚 Support for large text files (automatic chunking)
- 💾 Organized output with timestamped directories
- 📋 Comprehensive metadata preservation
- 🔗 Smart URL and web reference processing

## Prerequisites 📋

- Python 3.8 or higher
- FFmpeg (required for audio playback)
- Eleven Labs API key

### Installing FFmpeg

#### Windows
1. Run the provided installation script:
   ```bash
   powershell -ExecutionPolicy Bypass -File install_ffmpeg.ps1
   ```
2. Restart your terminal after installation

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/HiNala/read_to_me.git
   cd read_to_me
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Eleven Labs API key:
   ```
   ELEVEN_LABS_API_KEY=your_api_key_here
   ```

## Usage 💡

1. Run the application:
   ```bash
   python main.py
   ```

2. Choose your input method:
   - Option 1: Paste text directly
   - Option 2: Provide a file path (`.txt`, `.md`, or `.docx`)

3. Listen to your text being read aloud!

### URL Processing 🔗

The application automatically processes URLs and web references to make them more natural for speech:

- **Common Platforms**
  ```
  https://github.com/user/repo -> "GitHub at github.com slash user slash repo"
  https://youtube.com/watch?v=123 -> "YouTube video at youtube.com slash watch..."
  ```

- **General URLs**
  ```
  https://example.com/path -> "website example.com at path slash path"
  http://site.org -> "website site dot org"
  ```

- **Web Terms**
  - `.com` → "dot com"
  - `.org` → "dot org"
  - `/` → "slash"
  - `@` → "at"
  - `_` → "underscore"

This makes the audio output more natural when reading documents containing web references.

### Output Organization 📂

Each time you run the program, it creates a new timestamped directory in the `outputs` folder:

```
outputs/
└── run_20240315_143022/          # Timestamped run directory
    ├── text_info.json            # Metadata and original text
    ├── audio.mp3                 # Single audio file (if text is small)
    │   # OR for large texts:
    ├── part_01.mp3              # First chunk of audio
    ├── part_02.mp3              # Second chunk of audio
    ├── part_XX.mp3              # Additional chunks
    └── combined.mp3             # All chunks combined (if multiple parts)
```

#### Metadata File (text_info.json)
Each run's metadata file contains:
- Timestamp of the conversion
- Original text content
- Text length
- List of generated audio files

This organization makes it easy to:
- Keep track of different conversions
- Reference specific audio generations
- Review the original text content
- Access individual parts of long conversions

### Large Text Files
For large text files, the application automatically:
- Splits the text into manageable chunks
- Processes each chunk separately
- Saves individual chunk audio files
- Combines them into a single audio file
- Preserves all files for reference

## Troubleshooting 🔧

- **Missing API Key?** Make sure you have created a `.env` file with your Eleven Labs API key.
- **Audio Not Playing?** Ensure FFmpeg is installed correctly:
  - Windows: Run `install_ffmpeg.ps1` script
  - macOS/Linux: Check if `ffmpeg` is in your PATH
- **File Not Found?** Check that the file path is correct and the file exists.
- **Package Missing?** Run `pip install -r requirements.txt` to install all dependencies.
- **Output Files Missing?** Check if you have write permissions in the project directory.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [Eleven Labs](https://elevenlabs.io/) for their excellent Text-to-Speech API
- [FFmpeg](https://ffmpeg.org/) for audio processing capabilities
- All the open-source libraries that made this project possible 