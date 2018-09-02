# Setting the working directory
from util import *
from settings import *

os.chdir("/home/wesley/asteroid")

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

def launch():

    # Characteristics of the window
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Asteroids')

    # Clock of the update
    clock = pygame.time.Clock()

    # Load music
    pygame.mixer.music.load("audio/scifi.mp3")

    # Play music indefinitely
    pygame.mixer.music.play(-1)

    intro = False
    while not intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = True

        gameDisplay.blit(get_image('imgs/bg_main.jpg'), (0, 0))

        draw_text(gameDisplay, "Asteroids", 150, 350, 160)

        Button(gameDisplay, (120, 470, 150, 60), "Play!", path_font="font/Northwood High.ttf", is_transparent=True)
        Button(gameDisplay, (550, 470, 150, 60), "Quit", path_font="font/Northwood High.ttf", is_transparent=True)

        pygame.display.flip()
        clock.tick(90)
