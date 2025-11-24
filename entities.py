import pygame


class Entity:
    def __init__(self, pos, image):
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.vel = pygame.math.Vector2(0, 0)
        self.image = image
        self.collisions = {"left": False, "right": False, "up": False, "down": False}
        self.on_ground = False

    def rect(self):
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.image.get_width(), self.image.get_height())

    def update(self, keys, collision_rects):
        ACCELERATION = 0.05
        FRICTION = 0.05
        GRAVITY = 0.22
        JUMP_FORCE = -5.5
        SKID_SENSITIVITY = 0.1

        max_speed = 1.5
        if keys[pygame.K_x]:
            max_speed = 2.5

        input_axis = 0
        if keys[pygame.K_LEFT]:
            input_axis = -1
        elif keys[pygame.K_RIGHT]:
            input_axis = 1

        if input_axis != 0:
            if (input_axis > 0 and self.vel.x < 0) or (input_axis < 0 and self.vel.x > 0):
                self.vel.x += input_axis * SKID_SENSITIVITY
            else:
                self.vel.x += input_axis * ACCELERATION
        else:
            if self.vel.x > 0:
                self.vel.x = max(0, self.vel.x - FRICTION)
            elif self.vel.x < 0:
                self.vel.x = min(0, self.vel.x + FRICTION)

        if self.vel.x > max_speed:
            self.vel.x = max_speed
        elif self.vel.x < -max_speed:
            self.vel.x = -max_speed

        self.pos.x += self.vel.x
        entity_rect = self.rect()
        self.collisions["left"] = False
        self.collisions["right"] = False
        for block in collision_rects:
            if entity_rect.colliderect(block):
                if self.vel.x > 0:
                    self.pos.x = block.left - self.image.get_width()
                    self.collisions["right"] = True
                elif self.vel.x < 0:
                    self.pos.x = block.right
                    self.collisions["left"] = True
                self.vel.x = 0
                entity_rect = self.rect()

        if keys[pygame.K_c]:
            if self.on_ground:
                self.vel.y = JUMP_FORCE
                self.on_ground = False
        if not keys[pygame.K_c]:
            if self.vel.y < -2.0:
                self.vel.y = -2.0

        self.vel.y += GRAVITY
        self.vel.y = min(self.vel.y, 4.0)

        self.pos.y += self.vel.y
        entity_rect = self.rect()
        self.collisions["up"] = False
        self.collisions["down"] = False
        self.on_ground = False

        for block in collision_rects:
            if entity_rect.colliderect(block):
                if self.vel.y > 0:
                    self.pos.y = block.top - self.image.get_height()
                    self.collisions["down"] = True
                    self.on_ground = True
                    self.vel.y = 0
                elif self.vel.y < 0:
                    self.pos.y = block.bottom
                    self.collisions["up"] = True
                    self.vel.y = 0
                entity_rect = self.rect()

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.image, (int(self.pos.x - offset[0]), int(self.pos.y - offset[1])))
