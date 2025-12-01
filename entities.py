import pygame

JUMP_FORCE = -5.5
ACCELERATION = 0.03
FRICTION = 0.03
GRAVITY = 0.21
SKID_SENSITIVITY = 0.2


class Entity:
    def __init__(self, pos, assets, action="idle"):
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.vel = pygame.math.Vector2(0, 0)
        self.assets = assets
        self.action = action
        self.frame_index = 0
        self.image = self.assets[self.action][self.frame_index]
        self.flip = False
        self.collisions = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0

    def rect(self):
        return pygame.Rect(
            int(self.pos.x),
            int(self.pos.y),
            self.image.get_width(),
            self.image.get_height(),
        )

    def jump(self):
        self.jump_buffer = 5

    def cancel_jump(self):
        if self.vel.y < -2.0:
            self.vel.y = -2.0
        self.jump_buffer = 0

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.frame_index = 0

    def update(self, keys, collision_rects):
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.coyote_timer > 0:
            self.coyote_timer -= 1

        max_speed = 1.5
        if keys[pygame.K_x]:
            max_speed = 2.5

        input_axis = 0
        if keys[pygame.K_LEFT]:
            input_axis = -1
        if keys[pygame.K_RIGHT]:
            input_axis = 1

        if input_axis != 0:
            if input_axis > 0 > self.vel.x:
                self.vel.x += input_axis * SKID_SENSITIVITY
            if input_axis < 0 < self.vel.x:
                self.vel.x += input_axis * SKID_SENSITIVITY
            else:
                self.vel.x += input_axis * ACCELERATION
        else:
            if self.vel.x > 0:
                self.vel.x = max(0, self.vel.x - FRICTION)
            if self.vel.x < 0:
                self.vel.x = min(0, self.vel.x + FRICTION)

        if self.vel.x > max_speed:
            self.vel.x = max_speed
        if self.vel.x < -max_speed:
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
                if self.vel.x < 0:
                    self.pos.x = block.right
                    self.collisions["left"] = True
                self.vel.x = 0
                entity_rect = self.rect()

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
                    self.coyote_timer = 6
                if self.vel.y < 0:
                    self.pos.y = block.bottom
                    self.collisions["up"] = True
                    self.vel.y = 0
                entity_rect = self.rect()

        if self.jump_buffer > 0 and self.coyote_timer > 0:
            self.vel.y = JUMP_FORCE
            self.jump_buffer = 0
            self.coyote_timer = 0
            self.on_ground = False

        if input_axis > 0:
            self.flip = False
        elif input_axis < 0:
            self.flip = True

        if self.coyote_timer > 0:
            if abs(self.vel.x) > 0.1:
                self.set_action("run")
            else:
                self.set_action("idle")
        else:
            self.set_action("jump")

        if self.action == "run":
            self.frame_index += 0.08
        else:
            self.frame_index += 0.03

        if self.frame_index >= len(self.assets[self.action]):
            self.frame_index = 0

        current_image = self.assets[self.action][int(self.frame_index)]
        self.image = pygame.transform.flip(current_image, self.flip, False)

    def render(self, surf, offset=(0, 0)):
        dest_x = int(self.pos.x - offset[0])
        dest_y = int(self.pos.y - offset[1])
        surf.blit(self.image, (dest_x, dest_y))
