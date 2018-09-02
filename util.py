import pygame
import os

from settings import *

pygame.init()

# Load all the images at the same time
_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
        _image_library[path] = image
    return image


# Load all the sounds at the same time
_sound_library = {}


def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
        sound.set_volume(.10)
    sound.play()


class Button:

    def __init__(self, surface, rect=None, caption="", bg_color_static=BLUE, bg_color_highlight=LIGHT_BLUE, bg_color_down=BLUE, fgcolor=WHITE, path_font=None, is_transparent=False, visible=True, action=None):

        self.caption = caption
        self.visible = visible
        self.action = action

        self.transparent = is_transparent
        self.path_font = path_font

        self.bg_color_static = bg_color_static
        self.bg_color_highlight = bg_color_highlight
        self.bg_color_down = bg_color_down

        self.fgcolor = fgcolor
        self.surfButton = surface

        if rect is not None:
            self.rect = pg.Rect(rect)
            self.rect.center = (self.rect.x, self.rect.y)

        if path_font is None:
            self.font = pygame.font.SysFont("arial", 16)
        else:
            self.font = pygame.font.Font(path_font, 35)

        if not self.transparent:
            self.surfaceNormal = pg.Surface(self.rect.size).convert_alpha()
            self.surfaceDown = pg.Surface(self.rect.size).convert_alpha()
            self.surfaceHighlight = pg.Surface(self.rect.size).convert_alpha()
        else:
            self.surfaceNormal = pg.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
            self.surfaceDown = pg.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
            self.surfaceHighlight = pg.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()

        self.buttonDown = False
        self.mouseOverButton = False
        self.staticButton = True

        self.update()  # draw the initial button images

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        w = self.rect.width
        h = self.rect.height

        if not self.transparent:
            self.surfaceNormal.fill(self.bg_color_static)
            self.surfaceDown.fill(self.bg_color_down)
            self.surfaceHighlight.fill(self.bg_color_highlight)

        # draw caption text for all buttons
        captionSurf = self.font.render(self.caption, True, self.fgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)

        self.font = pygame.font.Font(self.path_font, 40)
        captionHighlight = self.font.render(self.caption, True, self.fgcolor)

        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)
        self.surfaceHighlight.blit(captionHighlight, captionRect)

        if self.rect.collidepoint(mouse_pos):  # If cursor is over the button
            self.mouseOverButton = True  # Mouse is over button and click was not detected
            self.staticButton = False
            if click[0] == 1:
                self.mouseOverButton = False
                self.buttonDown = True  # Click was detected
                play_sound("audio/air.wav")
        else:
            self.buttonDown = False
            self.mouseOverButton = False
            self.staticButton = True


        self.draw()

    def draw(self):
        # Blit the current button's appearance to the surface object.
        if self.visible:
            if self.buttonDown:
                print "down"
                self.surfButton.blit(self.surfaceDown, self.rect)
            elif self.mouseOverButton:
                print "over"
                self.surfButton.blit(self.surfaceHighlight, self.rect)
            else:
                print "static"
                self.surfButton.blit(self.surfaceNormal, self.rect)


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def draw_text(surf, text, size, x, y):
    font = pg.font.Font("font/Northwood High.ttf", size)
    text_surface, text_rect = text_objects(text, font)
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
