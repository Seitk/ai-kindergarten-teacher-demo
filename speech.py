import subprocess
import tempfile
import sounddevice as sd

from scipy.io import wavfile
from gtts import gTTS
from pydub import AudioSegment

def transcribe_audio_with_cli(filename):
    # Replace this command with the actual Whisper CLI command
    cmd = f"whisper --model tiny.en {filename} --language en --output_format txt --fp16 False  | cut -c 28-"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    
    if result.returncode == 0:
        transcription = result.stdout.strip()
        print("\rYou:", transcription)
        return transcription
    else:
        print("Error:", result.stderr)
        return None
    
# def transcribe_audio_with_openai(filename):

def transcribe(filename):
    return transcribe_audio_with_cli(filename)

def text_to_speech(text):
    print("\rAI:", text)

    # Convert text to speech
    tts = gTTS(text, lang="en")
    
    # Save speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        fp.seek(0)
        
        # Convert MP3 to WAV using pydub
        mp3_audio = AudioSegment.from_file(fp.name, format="mp3")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as wav_fp:
            mp3_audio.export(wav_fp.name, format="wav")
            wav_fp.seek(0)

            # Read audio data from the WAV file
            sample_rate, audio_data = wavfile.read(wav_fp.name)

            # Play the audio
            sd.play(audio_data, sample_rate)
            sd.wait()
