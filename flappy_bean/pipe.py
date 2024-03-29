from random import randrange
from pygame.image import load
from pygame.transform import scale
from pygame.mask import from_surface
from .constants import SPEED_ANIMATION, PIPE_DIST, \
                       PIPE_MIN_HGHT, PIPE_MAX_HGHT, \
                       PIPE_WDTH, PIPE_HGHT, \
                       PIPE_PATH_TOP, PIPE_PATH_BASE


class Pipe:
    SPEED = SPEED_ANIMATION
    DIST  = PIPE_DIST
    MIN_HGHT = PIPE_MIN_HGHT
    MAX_HGHT = PIPE_MAX_HGHT

    WDTH = PIPE_WDTH
    HGHT = PIPE_HGHT
    SIZE = WDTH, HGHT
    PATH_TOP  = PIPE_PATH_TOP
    PATH_BASE = PIPE_PATH_BASE

    def __init__(self, x):
        self.x = x
        self.passed = False

        self.pipe_top  = scale(load(self.PATH_TOP), self.SIZE)
        self.pipe_base = scale(load(self.PATH_BASE), self.SIZE)
        self.mask_top  = from_surface(self.pipe_top)
        self.mask_base = from_surface(self.pipe_base)

        self.set_height()

    def set_height(self):
        self.height = randrange(self.MIN_HGHT, self.MAX_HGHT)
        self.pos_top  = self.height - self.HGHT
        self.pos_base = self.height + self.DIST

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.pipe_top, (self.x, self.pos_top))
        screen.blit(self.pipe_base, (self.x, self.pos_base))

    def collide(self, obj):
        mask = obj.mask

        dist_top  = (self.x - obj.x, self.pos_top  - round(obj.y))
        dist_base = (self.x - obj.x, self.pos_base - round(obj.y))

        overlap_top  = mask.overlap(self.mask_top, dist_top)
        overlap_base = mask.overlap(self.mask_base, dist_base)

        return overlap_top or overlap_base

    @property
    def right(self):
        return self.x + self.pipe_top.get_width()

    @property
    def center(self):
        return self.x + (self.WDTH / 2), self.pos_base - (self.DIST / 2)
