import sys
import time
import sounddevice as sd
import soundfile as sf
import numpy as np # required to avoid crashing in assigning the callback input which is a numpy object
import webrtcvad
import queue

# get the default audio input device and its sample rate
device_info = sd.query_devices(None, 'input')
sample_rate = int(device_info['default_samplerate'])

interval_size = 30 # audio interval size in ms
downsample = 1

block_size = sample_rate * interval_size / 1000

# get an instance of webrtc's voice activity detection
vad = webrtcvad.Vad()
vad.set_mode(1)

last_talking_at = time.time()
audio_queue = queue.Queue()

def audio_callback(indata, frames, _, status):
    if status:
        print(F"underlying audio stack warning:{status}", file=sys.stderr)

    assert frames == block_size
    audio_data = indata[::downsample]        # possibly downsample, in a naive way
    audio_data = map(lambda x: (x+1)/2, audio_data)   # normalize from [-1,+1] to [0,1], you might not need it with different microphones/drivers
    audio_data = np.fromiter(audio_data, np.float16)  # adapt to expected float type
    audio_data = audio_data.tobytes()

    detection = vad.is_speech(audio_data, sample_rate)
    if detection == True:
        global last_talking_at
        last_talking_at = time.time()

    global audio_queue
    audio_queue.put(indata.copy())

def record_with_debounce(filename, time_second):
  global last_talking_at
  global audio_queue
  last_talking_at = time.time()
  audio_queue = queue.Queue()
  print(f'\rRecording...', end="")

  with sf.SoundFile(filename, mode='w', samplerate=sample_rate, channels=1, subtype=None) as file:

    with sd.InputStream(
        device=None,  # the default input device
        channels=1,
        samplerate=sample_rate,
        blocksize=int(block_size),
        callback=audio_callback):

        # avoid shutting down for endless processing of input stream audio
        while True:
            now = time.time()
            if now - last_talking_at > 2 and (now - last_talking_at) > time_second:
                break
            time.sleep(0.1)  # intermittently wake up

    while not audio_queue.empty():
        file.write(audio_queue.get())
  
  file.close()

  print(f'\rProcessing...', end="")
