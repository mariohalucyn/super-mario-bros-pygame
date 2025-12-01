from entities import Entity
from entities import GRAVITY


class Goomba(Entity):
    def __init__(self, pos, assets):
        super().__init__(pos, assets, action="walk")
        self.speed = 0.5
        self.vel.x = -self.speed
        self.squashed = False
        self.squashed_timer = 0

    def update(self, tilemap_rects, player_rect=None):
        if self.squashed:
            if self.action != "squashed":
                old_rect = self.rect()
                self.set_action("squashed")
                self.image = self.assets[self.action][0]
                self.pos.y = old_rect.bottom - self.image.get_height()
            self.squashed_timer += 1
            return

        self.vel.y += GRAVITY
        self.vel.y = min(self.vel.y, 4.0)

        self.pos.x += self.vel.x
        entity_rect = self.rect()
        for block in tilemap_rects:
            if entity_rect.colliderect(block):
                if self.vel.x > 0:
                    self.pos.x = block.left - self.image.get_width()
                    self.vel.x = -self.speed
                elif self.vel.x < 0:
                    self.pos.x = block.right
                    self.vel.x = self.speed
                entity_rect = self.rect()

        self.pos.y += self.vel.y
        entity_rect = self.rect()
        for block in tilemap_rects:
            if entity_rect.colliderect(block):
                if self.vel.y > 0:
                    self.pos.y = block.top - self.image.get_height()
                    self.vel.y = 0
                entity_rect = self.rect()

        self.frame_index += 0.1
        if self.frame_index >= len(self.assets[self.action]):
            self.frame_index = 0
        self.image = self.assets[self.action][int(self.frame_index)]
