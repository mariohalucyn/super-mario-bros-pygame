import sys
import pygame
from tilemap import Tilemap
from entities import Entity
import helpers

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
        self.scroll = [0, 0]
        self.assets = {
            "small_mario_standing": helpers.load_image("assets/small_mario_standing.png")
        }
        self.player = Entity(self.level.get_spawn_pos("player_spawn"), self.assets["small_mario_standing"])
        self.collision_rects = self.level.get_collision_rects()

    def run(self):
        while True:
            self.display.fill((148, 148, 255))
            self.level.render_visible_layers(self.display, offset=self.scroll)
            self.player.render(self.display, offset=self.scroll)
            relative_player_pos = self.player.rect()[0] - self.scroll[0]
            if self.player.pos.x and relative_player_pos / self.display.get_width() > 1/3:
                self.scroll[0] += self.player.vel.x
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.update(keys, self.collision_rects)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            self.clock.tick(60)


Game().run()
