import pygame


def load_image(path):
    img = pygame.image.load(path)
    img.set_colorkey((146, 144, 255))
    return img
