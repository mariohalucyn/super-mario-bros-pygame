import pygame
import pytmx


class Tilemap:
    def __init__(self):
        self.tmx_data = None
        self.collision_rects = []

    def load_level(self, path):
        self.tmx_data = pytmx.load_pygame(path)

    def get_collision_rects(self):
        terrain = self.tmx_data.get_layer_by_name("terrain")
        for x, y, gid in terrain:
            if gid != 0:
                rect = pygame.Rect(
                    x * self.tmx_data.tilewidth,
                    y * self.tmx_data.tileheight,
                    self.tmx_data.tilewidth, self.tmx_data.tileheight,
                )
                self.collision_rects.append(rect)
        return self.collision_rects

    def get_spawn_pos(self, name):
        entities = self.tmx_data.get_layer_by_name("entities")
        for obj in entities:
            if obj.name == name:
                return obj.x, obj.y

    def render_visible_layers(self, surf, offset=(0, 0)):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * self.tmx_data.tilewidth - offset[0], y * self.tmx_data.tileheight - offset[1]))
