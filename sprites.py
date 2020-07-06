import pygame as pg
import os


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
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)



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

    def draw(self, screen, audio_level, dt):
        screen.blit(self.images[audio_level], self.rects[audio_level])


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

    def move_mouse(self, mouse_pos):
        new_pos = (
            int(self.mousepad_origin[0] - self.mousepad_size[0] * mouse_pos[0]),
            int(self.mousepad_origin[1] - self.mousepad_size[1] * mouse_pos[1])
        )
        self.hand_pos = new_pos
        self.mouse.rect = self.mouse.image.get_rect(center=new_pos)

    def draw(self, screen, dt):
        
        pg.draw.circle(screen, (172,107,48), self.starting_pos, 20)
        pg.draw.line(screen, (172,107,48), self.starting_pos, self.hand_pos, 31)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]+3, self.starting_pos[1]+3), self.hand_pos, 30)
        pg.draw.line(screen, (172,107,48), (self.starting_pos[0]-3, self.starting_pos[1]-3), self.hand_pos, 30)
        self.mouse.draw(screen, dt)
        pg.draw.circle(screen, (172,107,48), (self.hand_pos[0] + 9, self.hand_pos[1] - 24), 18)

