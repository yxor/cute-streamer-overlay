from pynput import keyboard
import queue

class KeyboardListener:
    UP = 0
    DOWN = 1
    SPACE = 2
    ENTER = 3

    def __init__(self, event_queue : queue.Queue):
        self.event_queue : queue.Queue = event_queue

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.event_queue.put(KeyboardListener.SPACE)
        elif key == keyboard.Key.enter:
            self.event_queue.put(KeyboardListener.ENTER)
        else:
            self.event_queue.put(KeyboardListener.DOWN)

    def on_release(self, key):
        self.event_queue.put(KeyboardListener.UP)


    def listen(self):
        self.listener.start()

if __name__=="__main__":
    # just testing the listener
    keyboard_queue = queue.Queue(-1)
    keyboard_listener = KeyboardListener(keyboard_queue)
    keyboard_listener.listen()
    input()
