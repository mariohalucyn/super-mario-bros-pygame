import pygame


class Entity:
    def __init__(self, pos, image):
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = image

    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, keys):
        '''
        Comparison Table (Mario's Speeds)
        Action	            Internal Speed	Pixels Per Frame	Pixels Per Second
        Walking	            24 subpixels	1.5 px	            ~90 px/s
        Running	            40 subpixels	2.5 px	            ~150 px/s
        Sprinting P-Meter	56 subpixels	3.5 px	            ~210 px/s
        '''
        MAX_SPEED = 2.5 if keys[pygame.K_c] else 1.5
        entity_acc = 0
        if keys[pygame.K_LEFT]:
            entity_acc -= MAX_SPEED
        if keys[pygame.K_RIGHT]:
            entity_acc += MAX_SPEED

        self.pos.x += int(entity_acc)

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.image, (self.pos.x - offset[0], self.pos.y - offset[1]))
