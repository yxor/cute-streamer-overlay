import pygame as pg
import sys
import os
import win32api
import win32con
import win32gui
import queue

from sprites import *
from audioInputListener import AudioInputListener
from mouseListener import MouseListener
from keyboardListener import KeyboardListener

TRANSPARENT_COLOR = (1, 2, 5)  # Transparency color


def set_transparency_color():
    hwnd = pg.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT_COLOR), 0, win32con.LWA_COLORKEY)

class Control:

    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        

        pg.init()
        set_transparency_color()
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        # set Icon
        # pg.display.set_icon(self.icon)
        mousepad_center = (210, 450)
        self.chair = Chair((400, 300))
        self.mousepad = Mousepad(mousepad_center)
        self.keyboard = Keyboard((560, 440))
        self.body = Body((390, 350))
        self.eyes = Eyes((390, 270))
        self.mouth = Mouth((388, 293))

        self.mouse_hand = MouseHand(mousepad_center, (100, 38))
        self.keyboard_hand = KeyboardHand(self.keyboard)

    def update(self, dt):
        # draw the eyes
        self.eyes.draw(self.screen, dt)

        # mouth mouvement
        if not self.audio_queue.empty() and not self.mouth.is_expressing:
            audio_level = self.audio_queue.get()
            self.mouth.change_audio_level(audio_level)

        self.mouth.draw(self.screen, dt)
        
        # mouse mouvement
        if not self.mouse_queue.empty():
            self.mouse_hand.update_target(self.mouse_queue.get())
        
        self.mouse_hand.draw(self.screen, dt)

        # keyboard hand
        if not self.keyboard_queue.empty():
            self.keyboard_hand.click_keyboard(self.keyboard_queue.get())
        self.keyboard_hand.draw(self.screen, dt)


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def game_loop(self):

        while not self.done:
            delta_time = self.clock.tick(self.fps)

            self.event_loop()
            self.screen.fill(TRANSPARENT_COLOR)

            ## draw the chair
            self.chair.draw(self.screen)

            ## draw body
            self.body.draw(self.screen)

            # desk
            pg.draw.rect(self.screen, (200, 200, 200), (0, 380, 800, 380))

            # mousepad
            self.mousepad.draw(self.screen)

            # keyboard
            self.keyboard.draw(self.screen, delta_time)
            self.update(delta_time)
            pg.display.update()


def play_animation(audio_queue, keyboard_queue, mouse_queue):
    settings = {
        'size': (800, 600),
        'fps' : 60,
        'icon': None,
        'audio_queue': audio_queue,
        'mouse_queue': mouse_queue,
        'keyboard_queue': keyboard_queue
    }

    game = Control(**settings)
    game.game_loop()
    pg.quit()
    sys.exit()
