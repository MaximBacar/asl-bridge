from dotenv import load_dotenv
import os

from elevenlabs import stream
from elevenlabs.client import ElevenLabs

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
  api_key=elevenlabs_api_key,
)

def text_to_audio(text):
        audio_stream = client.text_to_speech.convert_as_stream(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb"
        )
        stream(audio_stream)

