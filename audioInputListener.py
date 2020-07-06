import sounddevice as sd
import numpy as np
import queue


class AudioInputListener:

    def __init__(self, event_queue : queue.Queue, min_threshold=3, max_threshold=10):
        self.event_queue : queue.Queue = event_queue
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

        self.stream = sd.InputStream(callback=self.on_sound_input)

    def on_sound_input(self, indata, frames, time, status):
        # TODO: figure out a way to only keep frames where its human voice
        volume_norm = np.linalg.norm(indata)
        
        is_ignorable = volume_norm < self.min_threshold or volume_norm > self.max_threshold
        if is_ignorable:
            return
        
        audio_level = 1 + int(3 * (volume_norm - self.min_threshold - 1) / (self.max_threshold - self.min_threshold))
        self.event_queue.put(audio_level)


    def listen(self):
        self.stream.start()
