import time
import pvporcupine
from audio import *
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
custom_wake_word_path = "./Hey-Sert_en_raspberry-pi_v3_0_0.ppn"
porcupine = pvporcupine.create(
    access_key=PORCUPINE_ACCESS_KEY,
    keywords=["Hey Sert"],
    keyword_paths=[custom_wake_word_path]
)


def run_assistant():
    while True:
        if listen_for_wake_word(porcupine, timeout=None):
            record_audio_dynamic(max_duration=10, silence_duration=1.5, fs=44100, threshold=0.01)
            listen_and_answer(client)
            play_audio("output.wav")


if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("Shutting down assistant...")
    finally:
        porcupine.delete()
