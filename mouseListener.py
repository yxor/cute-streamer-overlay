from pynput import mouse
import queue
import pygame as pg


def limit_norm(norm):
    return 0 if norm < 0 else 1 if norm > 1 else abs(norm)


class MouseListener:
    MOUVEMENT_PERC = 1 # the listerner will only listen to mouvement with this percision

    def __init__(self, event_queue : queue.Queue):
        self.event_queue : queue.Queue = event_queue

        # get screen size
        pg.init()
        infos = pg.display.Info()
        self.window_w, self.window_h = infos.current_w, infos.current_h

        # start in the middle
        self.norm_old_x, self.norm_old_y = 0.5, 0.5

        self.listener = mouse.Listener(on_move=self.on_move)
        

    # Sends an event to the event queue that the mouse moved to a certain direction
    # returns a tuple containing the mouvement vector of the mouse
    def on_move(self, x, y):
        norm_move = (limit_norm(round(x / self.window_w, self.MOUVEMENT_PERC)), limit_norm(round(y / self.window_h, self.MOUVEMENT_PERC)))

        # skip small mouvements
        is_negligable = (norm_move[0] == self.norm_old_x) and (norm_move[1] == self.norm_old_y)
        if is_negligable:
            return
        
        self.norm_old_x, self.norm_old_y = norm_move

        ## add the mouvement to the mouse event queue

        self.event_queue.queue.clear()
        self.event_queue.put(norm_move)

    def listen(self):
        self.listener.start()
