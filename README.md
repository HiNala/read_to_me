# Read to Me CLI 🎙️

A powerful command-line tool that converts text to speech using Eleven Labs' Text-to-Speech (TTS) API. Transform any text or document into natural-sounding audio with support for long-form content, web references, and organized output management.

## ✨ Features

### Core Features
- 📝 **Text Input Options**
  - Direct text pasting in terminal
  - File reading (`.txt`, `.md`, `.docx`)
  - Smart handling of web links and URLs
- 🎯 **High-Quality Speech**
  - Powered by Eleven Labs API
  - Natural-sounding voice
  - Configurable voice settings

### Advanced Capabilities
- 📚 **Large Text Support**
  - Automatic content chunking
  - Smart sentence boundary detection
  - Seamless audio combining
- 🔗 **URL Processing**
  - Platform-specific handling (GitHub, YouTube, etc.)
  - Web-friendly term conversion
  - Natural URL narration

### Organization & Management
- 💾 **Structured Output**
  - Timestamped directories
  - Comprehensive metadata
  - Individual and combined audio files
- 🛡️ **Security & Reliability**
  - Secure API key management
  - Robust error handling
  - Detailed logging

## 📋 Prerequisites

### Required Software
- Python 3.8 or higher
- FFmpeg (for audio processing)
- Eleven Labs API key

### Optional Tools
- Git (for cloning repository)
- Text editor (for configuration)

## 🚀 Installation

### 1. Get the Code
```bash
git clone https://github.com/HiNala/read_to_me.git
cd read_to_me
```

### 2. Set Up Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

#### Windows Users
```bash
powershell -ExecutionPolicy Bypass -File install_ffmpeg.ps1
# Restart your terminal after installation
```

#### macOS Users
```bash
brew install ffmpeg
```

#### Linux Users
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### 5. Configure API Key
Create `.env` file in project root:
```env
ELEVEN_LABS_API_KEY=your_api_key_here
```

## 💡 Usage Guide

### Basic Usage
1. Start the application:
   ```bash
   python main.py
   ```

2. Choose input method:
   ```
   1️⃣ Paste text directly
   2️⃣ Provide file path
   ```

3. Listen to the generated audio!

### Advanced Features

#### URL Processing 🔗
The application intelligently processes web references for natural speech:

```
Input:                     Output Speech:
---------------------------------------------------------
github.com/user/repo   →   "GitHub at github dot com slash user slash repo"
example.com/path       →   "website example dot com at path slash path"
user@domain.com        →   "user at domain dot com"
```

Special handling for popular platforms:
- GitHub repositories
- YouTube videos
- LinkedIn profiles
- Twitter/X posts

#### Large Text Processing 📚
For long documents, the application:
1. Splits content into optimal chunks
2. Processes each chunk separately
3. Combines audio seamlessly
4. Preserves all components

### Output Organization 📂

```
outputs/
└── run_20240315_143022/          # Unique run directory
    ├── text_info.json            # Run metadata
    ├── audio.mp3                 # Single file output
    │   # OR for long content:
    ├── part_01.mp3              # Content chunk 1
    ├── part_02.mp3              # Content chunk 2
    └── combined.mp3             # Complete audio
```

#### Metadata Structure
`text_info.json` contains:
```json
{
    "timestamp": "2024-02-15 14:30:22",
    "text_length": 1234,
    "audio_files": ["part_01.mp3", "part_02.mp3", "combined.mp3"],
    "text_content": "Original text content..."
}
```

## 🔧 Troubleshooting

### Common Issues

#### Audio Not Playing
1. Verify FFmpeg installation:
   ```bash
   ffmpeg -version
   ```
2. Check system audio
3. Ensure no other apps are blocking audio

#### API Issues
- Verify API key in `.env`
- Check internet connection
- Confirm API quota availability

#### File Processing
- Ensure file exists
- Check file permissions
- Verify supported format

### Error Messages
- ❌ **API Error**: Check API key and quota
- ❌ **File Not Found**: Verify path and permissions
- ❌ **FFmpeg Error**: Reinstall FFmpeg
- ❌ **Output Error**: Check disk space and permissions

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code:
- Follows existing style
- Includes documentation
- Has appropriate error handling

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Eleven Labs](https://elevenlabs.io/) - State-of-the-art TTS API
- [FFmpeg](https://ffmpeg.org/) - Audio processing capabilities
- Open source community for various libraries
- Contributors and users for feedback and support 