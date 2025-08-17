import os
import wave
import argparse
import requests
import base64
from pydub import AudioSegment

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Saves PCM data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

def text_to_speech(input_file, output_file, output_format):
    """
    Converts text from a file to speech using the Gemini API via HTTP requests.
    """
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set the GEMINI_API_KEY environment variable.")
        return

    # Read text from input file
    try:
        with open(input_file, 'r') as file:
            text_to_convert = file.read()
        if not text_to_convert.strip():
            print(f"The file '{input_file}' is empty or contains only whitespace.")
            return
    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    print("Generating speech...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-tts:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{
                "text": text_to_convert
            }]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_json = response.json()

        if 'candidates' not in response_json or not response_json['candidates']:
            print("Error: The API response is missing candidates.")
            print("Response:", response_json)
            return

        b64_data = response_json['candidates'][0]['content']['parts'][0]['inlineData']['data']
        audio_data = base64.b64decode(b64_data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the HTTP request: {e}")
        return
    except (KeyError, IndexError) as e:
        print(f"Error parsing the API response: {e}")
        print("Response:", response.text)
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Process and save the audio file
    temp_wav_file = "temp_output.wav"
    save_wav_file(temp_wav_file, audio_data)

    if output_format.lower() == 'wav':
        os.rename(temp_wav_file, output_file)
        print(f"Successfully created WAV file: {output_file}")
    elif output_format.lower() == 'mp3':
        try:
            audio = AudioSegment.from_wav(temp_wav_file)
            audio.export(output_file, format="mp3")
            print(f"Successfully created MP3 file: {output_file}")
        except Exception as e:
            print(f"Error converting to MP3: {e}")
        finally:
            # Clean up the temporary WAV file
            if os.path.exists(temp_wav_file):
                os.remove(temp_wav_file)
    else:
        print(f"Error: Unsupported output format '{output_format}'. Please use 'wav' or 'mp3'.")
        if os.path.exists(temp_wav_file):
            os.remove(temp_wav_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to speech using the Gemini API.")
    parser.add_argument("-i", "--input", default="input.txt", help="Path to the input text file.")
    parser.add_argument("-o", "--output", default="output", help="Base name for the output audio file (without extension).")
    parser.add_argument("-f", "--format", default="mp3", choices=['mp3', 'wav'], help="Output audio format (mp3 or wav).")

    args = parser.parse_args()

    output_filename = f"{args.output}.{args.format}"

    text_to_speech(args.input, output_filename, args.format)
