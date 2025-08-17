# Text-to-Speech Converter with Gemini API

This is a Python script to convert text from a file into an audio file using Google's Gemini API.

## Features

- Reads text from a specified input file.
- Converts the text to speech using the `gemini-2.5-pro-preview-tts` model.
- Saves the output as an MP3 or WAV file.
- Command-line interface for specifying input, output, and format.

## Requirements

- Python 3
- `google-generativeai` library
- `pydub` library
- A Google Gemini API Key

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   **Note:** `pydub` requires an audio playback library like `ffmpeg` or `libav`. Please install one if you don't have it already. For example, on Debian/Ubuntu: `sudo apt-get install ffmpeg`

3. Set up your Gemini API Key:
   You need to have a Gemini API key to use this script. You can get one from the [Google AI for Developers](https://ai.google.dev/) website.

   Once you have your key, set it as an environment variable:
   ```bash
   export GEMINI_API_KEY='your-api-key'
   ```

## Usage

Run the `main.py` script from your terminal.

### Default Usage
By default, the script reads from `input.txt` and saves the audio as `output.mp3`:
```bash
python main.py
```

### Specifying Options
You can use command-line arguments to customize the behavior:
- `-i` or `--input`: Path to the input text file.
- `-o` or `--output`: The base name for the output audio file (the extension will be added automatically).
- `-f` or `--format`: The output audio format (`mp3` or `wav`).

### Examples

**Convert `my_story.txt` to `my_audio.wav`:**
```bash
python main.py --input my_story.txt --output my_audio --format wav
```

**Convert `input.txt` to `speech.mp3`:**
```bash
python main.py --output speech --format mp3
```
