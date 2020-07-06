from animation import play_animation
from audioInputListener import AudioInputListener
from keyboardListener import KeyboardListener
from mouseListener import MouseListener

import queue
import yaml

if __name__=="__main__":
    # open the config file and load it as a dict
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # setup the audio listener
    audio_queue = queue.Queue(-1)
    audio_listener = AudioInputListener(audio_queue, config["start_threshold"], config["end_threshold"])
    audio_listener.listen()
    
    # setup the mouse listener
    mouse_queue = queue.Queue(-1)
    mouse_listener = MouseListener(mouse_queue)
    mouse_listener.listen()
    
    # setup the keyboard listener
    keyboard_queue = queue.Queue(-1)
    keyboard_listener = KeyboardListener(keyboard_queue)
    keyboard_listener.listen()

    play_animation(audio_queue, keyboard_queue, mouse_queue)