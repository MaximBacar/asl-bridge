from dotenv import load_dotenv
import os

from elevenlabs import stream
from elevenlabs.client import ElevenLabs

import openai


class Conversation:

    def __init__(self):
        load_dotenv()
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

        self.client = ElevenLabs( api_key = elevenlabs_api_key)
        openai.api_key = os.getenv("OPEN_AI_KEY")

    def text_to_audio(self, text):
        audio_stream = self.client.text_to_speech.convert_as_stream( text = text, voice_id="JBFqnCBsd6RMkjVDRZzb")
        stream( audio_stream )
    
    def asl_to_text(self, asl):
        prompt = f'The following is in ASL translated literally from hand sign: {asl}. Translate it to readable english. Only give me the translation.'
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role" : "user",
                    "content" : prompt
                }
            ]
        )
        return response['choices'][0]['message']['content']
    