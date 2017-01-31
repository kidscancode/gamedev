import pygame as pg
import xml.etree.ElementTree as ET
from os import path
import pytmx
from settings import *
vec = pg.math.Vector2

class SpritesheetWithXML:
    # utility class for loading and parsing spritesheets
    # xml filename should match png filename (Kenney format)
    # TODO: improve to work with other data formats
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename + '.png').convert_alpha()
        # load XML (kenney format) if it exists
        if path.isfile(filename + '.xml'):
            tree = ET.parse(filename + '.xml')
            self.map = {}
            # read through XML and pull out image locations using the following structure:
            # self.map['image name'] = {'x':x, 'y':y, 'w':w, 'h':h}
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['w'] = int(node.attrib.get('width'))
                    self.map[name]['h'] = int(node.attrib.get('height'))

    def get_image_by_rect(self, x, y, w, h):
        r = pg.Rect(x, y, w, h)
        return self.spritesheet.subsurface(r)

    def get_image_by_name(self, name):
        # TODO: error message if no xml exists
        r = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                    self.map[name]['w'], self.map[name]['h'])
        return self.spritesheet.subsurface(r)

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # apply to entity with a rect
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # apply to a given rect
        return rect.move(self.camera.topleft)

    def apply_point(self, pos):
        # apply to a given point
        return pos + vec(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
