import pygame
import pygame.math as pm

class Wavepoint:
    def __init__(self, x: int, y:int):
        self.pos = pm.Vector2(x, y)
        self.mass = 1
        self.spd_y = 0
