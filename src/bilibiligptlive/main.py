import os
import time
import requests
import openai
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

# Replace these with your own values
roomid = "YOUR_ROOM_ID"
openai_api_key = "YOUR_OPENAI_API_KEY"
google_credentials_file = "PATH_TO_YOUR_GOOGLE_CREDENTIALS_JSON"

# Set the environment variable for Google Text-to-Speech API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_file

# Initialize OpenAI API
openai.api_key = openai_api_key

# Initialize Google Text-to-Speech API client
tts_client = texttospeech.TextToSpeechClient()

# URL for Bilibili API
url = f"https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={roomid}"

# Function to send a message to ChatGPT and get a response
def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )
    return response.choices[0].text.strip()

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

# Main loop to poll messages and send them to ChatGPT
while True:
    response = requests.get(url)
    data = response.json()

    if data["code"] == 0:
        messages = data["data"]["room"]

        for message in messages:
            message_text = message["text"]
            prompt = f"User: {message_text}\nAI:"
            response_text = chatgpt_response(prompt)
            print(f"User: {message_text}\nAI: {response_text}\n")

            # Synthesize the response text to speech
            audio_data = synthesize_text(response_text, language_code="zh-CN")

            # Play the synthesized audio
            play_audio(audio_data)

    else:
        print("Error fetching messages")

    time.sleep(10)
