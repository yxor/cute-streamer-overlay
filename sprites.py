import pygame as pg
import os
import random

from keyboardListener import KeyboardListener



class Chair(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(os.path.join('assets', 'chair1.png')).convert_alpha(),
            0,
            0.45
        )
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Keyboard(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(os.path.join('assets', 'keyboard1.png')).convert_alpha(),
            0,
            0.5
        )
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

        self.shaking = False
        self.shaking_counter = 0

    def draw(self, screen, dt):
        if self.shaking:
            new_pos = (self.pos[0] + random.choice([-1, 1]), self.pos[1] + random.choice([-1, 1]))
            screen.blit(self.image, self.image.get_rect(center=new_pos))
            if self.shaking_counter * dt > 20: # 20ms shake animation
                self.shaking = False

            self.shaking_counter += 1
        else:
            screen.blit(self.image, self.rect)


    def shake(self):
        self.shaking = True
        self.shaking_counter = 0


    



class Mousepad(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(os.path.join('assets', 'mousepad1.png')).convert_alpha(),
            0,
            0.6
        )
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Body(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(os.path.join('assets', 'body1.png')).convert_alpha(),
            0,
            0.5
        )
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Eyes(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.blink_counter = 0
        self.blinking = False
        self.images = [
            pg.transform.rotozoom(
                pg.image.load(os.path.join('assets', 'blink1.png')).convert_alpha(),
                0,
                0.8
            ),
            pg.transform.rotozoom(
                pg.image.load(os.path.join('assets', 'blink2.png')).convert_alpha(),
                0,
                0.8
            ),
        ]
        self.rects = [image.get_rect(center=pos) for image in self.images]

    def draw(self, screen, dt):
        blink_progress = self.blink_counter * dt
        self.blink_counter += 1

        if self.blinking and blink_progress > 500:
            self.blinking = False
            self.blink_counter = 0

        if not self.blinking and blink_progress > 4500:
            self.blinking = True
            self.blink_counter = 0


        if self.blinking:
            screen.blit(self.images[0], self.rects[0])
        else:
            screen.blit(self.images[1], self.rects[1])


class Mouth(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.talking_counter = 0
        self.images = [
            pg.transform.rotozoom(
                pg.image.load(os.path.join('assets', f'mouth{image_index}.png')).convert_alpha(),
                0,
                0.9
            ) for image_index in range(4)
        ]
        self.rects = [image.get_rect(center=pos) for image in self.images]
        self.expression = 0
        self.is_expressing = False
        self.expression_counter = 0

    def change_audio_level(self, audio_level):
        self.expression = audio_level
        self.is_expressing = True
        self.expression_counter = 0

    def draw(self, screen, dt):
        screen.blit(self.images[self.expression], self.rects[self.expression])
        expression_progress = self.expression_counter * dt
        if expression_progress > 5: # 5ms
            self.expression = 0
            self.is_expressing = False
        
        self.expression_counter += 1




class Mouse(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(os.path.join('assets', 'mouse1.png')).convert_alpha(),
            13,
            0.5
        )
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen, dt):
        screen.blit(self.image, self.rect)



class MouseHand:

    def __init__(self, mousepad_center, mousepad_size):
        self.starting_pos = (230, 350)
        self.hand_pos = mousepad_center
        self.mouse = Mouse(mousepad_center)
        self.mousepad_size = mousepad_size
        self.mousepad_origin = (mousepad_center[0] + (mousepad_size[0]//2), mousepad_center[1] + (mousepad_size[1]//2)) 
        self.target_pos = mousepad_center


    def update_target(self, mouse_pos):
        self.target_pos = (
            int(self.mousepad_origin[0] - self.mousepad_size[0] * mouse_pos[0]),
            int(self.mousepad_origin[1] - self.mousepad_size[1] * mouse_pos[1])
        )

    def draw(self, screen, dt):


        pg.draw.circle(screen, (172,107,48), self.starting_pos, 20)
        pg.draw.line(screen, (172,107,48), self.starting_pos, self.hand_pos, 31)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]+3, self.starting_pos[1]+3), self.hand_pos, 30)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]-3, self.starting_pos[1]-3), self.hand_pos, 30)
        self.mouse.draw(screen, dt)
        pg.draw.circle(screen, (172,107,48), (self.hand_pos[0] + 9, self.hand_pos[1] - 24), 18)
        
        if not (self.target_pos == self.hand_pos):
            stepx = (self.target_pos[0] - self.hand_pos[0]) /10
            stepy = (self.target_pos[1] - self.hand_pos[1]) /10

            self.hand_pos = (int(self.hand_pos[0] + stepx), int(self.hand_pos[1] + stepy))
            self.mouse.rect = self.mouse.image.get_rect(center=self.hand_pos)


class State:
    IDLE = 0
    CLICKING_A = 1
    CLICKING_B = 2
    CLICKING_SPACE = 3
    CLICKING_ENTER = 4

class KeyboardHand:


    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.starting_pos = (550, 350)
        self.idle_hand_pos = (600, 400)
        self.click_pos_a = (540, 410)
        self.click_pos_b = (650, 400)
        self.click_pos_space = (560, 375)
        self.click_pos_enter = (460, 420)

        # set state to idle at the beginning
        self.hand_pos = self.idle_hand_pos
        self.state = State.IDLE
        self.click_ab_toggle = True

        

    def click_keyboard(self, clicktype):
        clicking = self.state != State.IDLE

        # if its clicking
        if clicking and clicktype == KeyboardListener.DOWN:
            return # keep clicking

        if clicking and clicktype == KeyboardListener.UP:
            self.alter_state(State.IDLE)
            return

        if clicking:
            return
        # if its idle

        if clicktype == KeyboardListener.SPACE:
            self.alter_state(State.CLICKING_SPACE)
        
        if clicktype == KeyboardListener.ENTER:
            self.alter_state(State.CLICKING_ENTER)
        
        if clicktype == KeyboardListener.DOWN:
            if self.click_ab_toggle:
                self.alter_state(State.CLICKING_A)
            else:
                self.alter_state(State.CLICKING_B)

            self.click_ab_toggle = not self.click_ab_toggle
            
        self.keyboard.shake()




    def alter_state(self, new_state):
        if new_state == State.IDLE:
            self.hand_pos = self.idle_hand_pos
        elif new_state == State.CLICKING_A:
            self.hand_pos = self.click_pos_a
        elif new_state == State.CLICKING_B:
            self.hand_pos = self.click_pos_b
        elif new_state == State.CLICKING_SPACE:
            self.hand_pos = self.click_pos_space
        elif new_state == State.CLICKING_ENTER:
            self.hand_pos = self.click_pos_enter
        else:
            return
        
        self.state = new_state


    def draw(self, screen, dt):
        pg.draw.circle(screen, (172,107,48), self.starting_pos, 20)

        pg.draw.line(screen, (172,107,48), self.starting_pos, self.hand_pos, 31)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]+3, self.starting_pos[1]+3), self.hand_pos, 30)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]-3, self.starting_pos[1]-3), self.hand_pos, 30)
        pg.draw.circle(screen, (172,107,48), (self.hand_pos[0], self.hand_pos[1]), 18)


