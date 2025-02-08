import base64
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import pvporcupine


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
    Record audio until the user stops speaking (silence detected) or until max_duration is reached,
    but skip initial silence and only record after the user starts talking.

    Parameters:
      max_duration (float): Maximum recording time in seconds.
      silence_duration (float): Duration of silence (in seconds) required to stop recording.
      fs (int): Sampling rate.
      threshold (float): Amplitude threshold below which audio is considered silence.
    """
    print("Recording...")
    audio_data = []  # to accumulate audio chunks (only after speech starts)
    silence_start = None  # timestamp when silence started after speech began
    start_time = time.time()  # overall recording start time
    callback_called = False  # flag to indicate if callback has requested to stop
    started_talking = False  # flag indicating if the user has started speaking

    def callback(indata, frames, time_info, status):
        nonlocal silence_start, audio_data, callback_called, started_talking
        if status:
            print(status)

        # Check if speech has started (chunk exceeds threshold)
        if not started_talking:
            if np.max(np.abs(indata)) >= threshold:
                started_talking = True
                # Record this chunk since it contains speech
                audio_data.append(indata.copy())
            # If not started talking, skip this chunk entirely.
            return

        # Once speech has started, record all chunks.
        audio_data.append(indata.copy())

        # Check if the current chunk is silent.
        if np.max(np.abs(indata)) < threshold:
            if silence_start is None:
                silence_start = time.time()  # start the silence timer
        else:
            silence_start = None  # reset silence timer if sound is detected

        # Stop recording if silence persists for longer than silence_duration.
        if silence_start is not None and (time.time() - silence_start) > silence_duration:
            callback_called = True
            raise sd.CallbackStop()

    stream = sd.InputStream(samplerate=fs, channels=1, callback=callback)
    with stream:
        try:
            while time.time() - start_time < max_duration:
                sd.sleep(100)
                if callback_called:
                    print("Silence detected, stopping recording.")
                    break
        except sd.CallbackStop:
            print("Silence detected, stopping recording.")

    if not audio_data:
        print("No audio recorded.")
        return

    # Concatenate the recorded chunks and save to file.
    audio_data = np.concatenate(audio_data, axis=0)
    sf.write("input.wav", audio_data, fs)
    print(f"Saved recording to input.wav")


def listen_for_wake_word(porcupine, timeout=10):
    # Initialize Porcupine with your chosen keyword
    try:
        with sd.RawInputStream(
                samplerate=porcupine.sample_rate,
                blocksize=porcupine.frame_length,
                channels=1,
                dtype="int16"
        ) as stream:
            print("Listening for wake word...")
            start_time = time.time()
            while True:
                pcm = stream.read(porcupine.frame_length)[0]
                pcm = np.frombuffer(pcm, dtype=np.int16)
                if porcupine.process(pcm) >= 0:
                    print("Wake word detected!")
                    return True

                if timeout is not None and time.time() - start_time > timeout:
                    print("Timeout reached, stopping.")
                    return False
    finally:
        porcupine.delete()


def play_audio(filename):
    data, fs = sf.read(filename)
    sd.play(data, fs)
    sd.wait()
    print(f"Played {filename}")
