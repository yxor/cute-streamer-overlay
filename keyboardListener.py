from pynput import keyboard
import queue

class KeyboardListener:
    DOWN = 1
    UP = 0

    def __init__(self, event_queue : queue.Queue):
        self.event_queue : queue.Queue = event_queue

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def on_press(self, key):
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
