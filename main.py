import sys
import pygame
from tilemap import Tilemap
from entities import Entity
from goomba import Goomba
import helpers

DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 240
SCALE = 3
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
            "idle": [helpers.load_image("assets/small_mario_standing.png")],
            "run": [
                helpers.load_image("assets/small_mario_run_0.png"),
                helpers.load_image("assets/small_mario_run_1.png"),
                helpers.load_image("assets/small_mario_run_2.png"),
            ],
            "jump": [helpers.load_image("assets/small_mario_jumping.png")],
        }
        self.goomba_assets = {
            "idle": [helpers.load_image("assets/goomba_walk_0.png")],
            "walk": [
                helpers.load_image("assets/goomba_walk_0.png"),
                helpers.load_image("assets/goomba_walk_1.png"),
            ],
            "squashed": [helpers.load_image("assets/goomba_squashed.png")]
        }
        self.player = Entity(self.level.get_spawn_pos("player_spawn"), self.assets)
        self.collision_rects = self.level.get_collision_rects()
        self.enemies = []
        self.pending_enemies = self.level.extract_enemies("goomba")

    def run(self):
        while True:
            self.display.fill((148, 148, 255))

            relative_player_pos = self.player.rect()[0] - self.scroll[0]
            if self.player.pos.x and relative_player_pos / self.display.get_width() > 1/3:
                if self.player.vel.x > 0:
                    self.scroll[0] += self.player.vel.x

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        self.player.cancel_jump()

            keys = pygame.key.get_pressed()
            self.level.render_visible_layers(self.display, offset=self.scroll)

            self.player.update(keys, self.collision_rects)
            self.player.render(self.display, offset=self.scroll)

            for pos in self.pending_enemies[:]:
                dist_x = pos[0] - self.player.pos.x
                if abs(dist_x) < 300:
                    self.enemies.append(Goomba(pos, self.goomba_assets))
                    self.pending_enemies.remove(pos)

            for enemy in self.enemies[:]:
                enemy.update(self.collision_rects)
                enemy.render(self.display, offset=self.scroll)

                if enemy.squashed and enemy.squashed_timer > 60:
                    self.enemies.remove(enemy)
                    continue

                if not enemy.squashed:
                    player_rect = self.player.rect()
                    enemy_rect = enemy.rect()

                    if player_rect.colliderect(enemy_rect):
                        if self.player.vel.y > 0 and player_rect.bottom < enemy_rect.centery:
                            enemy.squashed = True
                            self.player.vel.y = -4
                        else:
                            print("Game Over")
                            self.player = Entity(self.level.get_spawn_pos("player_spawn"), self.assets)
                            self.scroll = [0, 0]

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            self.clock.tick(60)


Game().run()
