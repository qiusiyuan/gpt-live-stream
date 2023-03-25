from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

google_credentials_file = "PATH_TO_YOUR_GOOGLE_CREDENTIALS_JSON"

# Set the environment variable for Google Text-to-Speech API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_file

# Initialize Google Text-to-Speech API client
tts_client = texttospeech.TextToSpeechClient()
# Function to synthesize text to speech using Google Text-to-Speech API
def synthesize_text(text, language_code="zh-CN"):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content

# Function to play the synthesized audio
def play_audio(audio_data):
    audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
    play(audio)

