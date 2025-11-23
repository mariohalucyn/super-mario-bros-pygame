import sys
import pygame
from tilemap import Tilemap

DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 240
SCALE = 7
SCREEN_WIDTH = DISPLAY_WIDTH * SCALE
SCREEN_HEIGHT = DISPLAY_HEIGHT * SCALE


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Tilemap()
        self.level.load_level("assets/1-1.tmx")

    def run(self):
        while True:
            self.display.fill((148, 148, 255))
            self.level.render_visible_layers(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
