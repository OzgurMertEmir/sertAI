import unittest
from audio import *
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class MyTestCase(unittest.TestCase):
    def test_audio_recording(self):
        record_audio("input.wav", duration=5)
        self.assertTrue(True)

    def test_audio_qa(self):
        record_audio("input.wav", duration=5)
        listen_and_answer(client)
        self.assertTrue(True)

    def test_audio_dynamic(self):
        record_audio_dynamic(max_duration=100, silence_duration=1.5, fs=44100, threshold=0.1)
        self.assertTrue(True)

    def test_play_io_audio(self):
        play_audio("input.wav")
        play_audio("output.wav")
        self.assertTrue(True)

    def test_full_audio_pipeline(self):
        record_audio_dynamic(max_duration=10, silence_duration=1.5, fs=44100, threshold=0.01)
        listen_and_answer(client)
        play_audio("output.wav")

    def test_default_wake_word_detection(self):
        porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=["terminator"])
        listen_for_wake_word(porcupine)

    def test_custom_wake_word_detection(self):
        custom_keyword_path = "../Hey-Sert_en_mac_v3_0_0.ppn"
        porcupine = pvporcupine.create(
            access_key=PORCUPINE_ACCESS_KEY,
            keywords=["Hey Sert"],
            keyword_paths=[custom_keyword_path]
        )
        listen_for_wake_word(porcupine)

    def test_full_audio_pipeline_with_custom_wake_word(self):
        custom_keyword_path = "../Hey-Sert_en_mac_v3_0_0.ppn"
        porcupine = pvporcupine.create(
            access_key=PORCUPINE_ACCESS_KEY,
            keywords=["Hey Sert"],
            keyword_paths=[custom_keyword_path]
        )
        wake_word_detected = listen_for_wake_word(porcupine)
        if wake_word_detected:
            record_audio_dynamic(max_duration=20, silence_duration=1.5, fs=44100, threshold=0.01)
            listen_and_answer(client)
            print("Playing output...")
            play_audio("output.wav")


if __name__ == '__main__':
    # unittest.main()
    play_audio("output.wav")
