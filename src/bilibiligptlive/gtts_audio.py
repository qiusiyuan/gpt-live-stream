from gtts import gTTS
import pygame
import io
# Initialize the pygame mixer
pygame.mixer.init()

def synthesize_text(text, language_code="zh-CN"):
    tts = gTTS(text, lang=language_code)
    
    # Save the synthesized audio to a buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    # Load and play the audio from the buffer
    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__=="__main__":
    text = "你好，我是bilibili ai直播姬。"
    synthesize_text(text)
