import pygame


class Entity:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos[0], pos[1])

    def render(self, image, surf):
        surf.blit(image, (self.pos.x, self.pos.y))
