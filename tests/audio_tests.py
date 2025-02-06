import unittest
from audio import *
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MyTestCase(unittest.TestCase):
    def test_audio_recording(self):
        record_audio("input.wav", duration=5)
        self.assertTrue(True)

    def test_audio_qa(self):
        record_audio("input.wav", duration=5)
        with open("input.wav", "rb") as f:
            audio_file = f.read()
        client = OpenAI(api_key=OPENAI_API_KEY)
        output_wav_bytes = listen_and_answer(client)
        with open("output.wav", "wb") as f:
            f.write(output_wav_bytes)
        self.assertTrue(True)

    def test_audio_dynamic(self):
        record_audio_dynamic(max_duration=10, silence_duration=1.5, fs=44100, threshold=0.01)
        self.assertTrue(True)

    def test_play_io_audio(self):
        play_audio("input.wav")
        play_audio("output.wav")
        self.assertTrue(True)

    def test_full_audio_pipeline(self):
        client = OpenAI(api_key=OPENAI_API_KEY)
        record_audio_dynamic(max_duration=10, silence_duration=1.5, fs=44100, threshold=0.01)
        listen_and_answer(client)
        play_audio("output.wav")


if __name__ == '__main__':
    #unittest.main()
    play_audio("output.wav")