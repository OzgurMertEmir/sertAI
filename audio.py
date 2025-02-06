import base64
import sounddevice as sd
import soundfile as sf
import numpy as np
import time


def record_audio(filename, duration, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    sf.write(filename, recording, fs)
    print(f"Saved recording to {filename}")


def listen_and_answer(client):
    with open("input.wav", "rb") as f:
        audio_file = f.read()

    # Add preprocessing here in the future

    encoded_string = base64.b64encode(audio_file).decode('utf-8')
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": "wav"
                        }
                    }
                ]
            },
        ]
    )

    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open("output.wav", "wb") as f:
        f.write(wav_bytes)


def record_audio_dynamic(max_duration=10, silence_duration=1.5, fs=44100, threshold=0.01):
    """
    Record audio until the user stops speaking (silence detected) or until max_duration is reached.

    Parameters:
      max_duration (float): Maximum recording time in seconds.
      silence_duration (float): Duration of silence (in seconds) required to stop recording.
      fs (int): Sampling rate.
      threshold (float): Amplitude threshold below which audio is considered silence.
    """
    print("Recording...")
    audio_data = []  # to accumulate audio chunks
    silence_start = None  # timestamp when silence started
    start_time = time.time()  # overall recording start time

    def callback(indata, frames, time_info, status):
        nonlocal silence_start, audio_data

        if status:
            print(status)

        # Append current audio chunk
        audio_data.append(indata.copy())

        # Check if the maximum amplitude in the chunk is below the threshold
        if np.max(np.abs(indata)) < threshold:
            if silence_start is None:
                silence_start = time.time()  # start silence timer
        else:
            silence_start = None  # reset if sound detected

        # If silence has persisted for longer than silence_duration and we have at least 1 second of audio, stop recording
        if silence_start is not None and (time.time() - silence_start) > silence_duration and (
                time.time() - start_time) > 1:
            raise sd.CallbackStop()

    stream = sd.InputStream(samplerate=fs, channels=1, callback=callback)
    with stream:
        try:
            while time.time() - start_time < max_duration:
                sd.sleep(100)  # sleep for a short time to allow the callback to process
        except sd.CallbackStop:
            print("Silence detected, stopping recording.")

    # Concatenate all recorded chunks and write to file
    audio_data = np.concatenate(audio_data, axis=0)
    sf.write("input.wav", audio_data, fs)
    print(f"Saved recording to input.wav")


def play_audio(filename):
    data, fs = sf.read(filename)
    sd.play(data, fs)
    sd.wait()
    print(f"Played {filename}")
