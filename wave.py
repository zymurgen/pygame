from typing import List

import pygame
import pygame.math as pm
import math
import random

from wavepoint import Wavepoint

class Wave(object):
    def __init__(self):
        self.NUM_POINTS = 80
        self.WIDTH = 600
        self.SPRING_CONSTANT = 0.005
        self.SPRING_CONSTANT_BASEPOINT = 0.005
        self.Y_OFFSET = 200
        self.DAMPING = 0.99
        self.ITERATIONS = 5

        self.offset = 0
        self.NUM_BACKGROUND_WAVES = 7
        self.BACKGROUND_WAVE_MAX_HEIGHT = 6
        self.BACKGROUND_WAVE_COMPRESSION = 1/10

        self.sine_offsets = []
        self.sine_amplitudes = []
        self.sine_stretches = []
        self.offset_stretches = []

        self.wave_points = self.make_wave_points(self.NUM_POINTS)
        self.create_sinuses()

    def create_sinuses(self):
        for i in range(self.NUM_BACKGROUND_WAVES):
            sine_offset = -math.pi + 2 * math.pi * random.uniform(0, 1)
            self.sine_offsets.append(sine_offset)
            sine_amplitude = random.uniform(0, 1) * self.BACKGROUND_WAVE_MAX_HEIGHT
            self.sine_amplitudes.append(sine_amplitude)
            sine_stretch = random.uniform(0,1) * self.BACKGROUND_WAVE_COMPRESSION
            self.sine_stretches.append(sine_stretch)
            offset_stretch = random.uniform(0,1) * self.BACKGROUND_WAVE_COMPRESSION
            self.offset_stretches.append(offset_stretch)


    def overlap_sines(self, x):
        result = 0
        for i in range(self.NUM_BACKGROUND_WAVES-1):
            result = result + self.sine_offsets[i] + self.sine_amplitudes[i] \
                     + math.sin(x * self.sine_stretches[i] + self.offset * self.offset_stretches[i])

        return result


    def make_wave_points(self, numPoints: int):
        t: List[Wavepoint] = []
        for i in range(numPoints):
            x = i / numPoints * self.WIDTH
            y = self.Y_OFFSET
            new_point = Wavepoint(x + 20, y)
            t.append(new_point)
        return t

    def update_wave_points(self, points: List[Wavepoint], dt: float):
        for i in range(self.ITERATIONS):
            for n in range(len(points)):
                p = points[n]
                force = 0

                forceFromLeft = None
                forceFromRight = None

                if n == 0:
                    dy = points[len(points)-1].pos.y - p.pos.y
                    forceFromLeft = self.SPRING_CONSTANT * dy
                else:
                    dy = points[n-1].pos.y - p.pos.y
                    forceFromLeft = self.SPRING_CONSTANT * dy
                if n == len(points)-1:
                    dy = points[0].pos.y - p.pos.y
                    forceFromRight = self.SPRING_CONSTANT * dy
                else:
                    dy = points[n+1].pos.y - p.pos.y
                    forceFromRight = self.SPRING_CONSTANT * dy

                dy = self.Y_OFFSET - p.pos.y
                forceToBaseline = self.SPRING_CONSTANT_BASEPOINT * dy

                force = force + forceFromLeft
                force = force + forceFromRight
                force = force + forceToBaseline

                acceleration = force / p.mass

                p.spd_y = self.DAMPING * p.spd_y + acceleration

                p.pos.y = p.pos.y + p.spd_y

    def draw(self, surf: pygame.Surface):

        #pygame.draw.line(surf, pygame.Color("white"), (0, self.Y_OFFSET), (self.WIDTH, self.Y_OFFSET), 1)

        for i, n in enumerate(self.wave_points):
            #pygame.draw.circle(surf, (124, 124, 124), (n.pos.x, self.Y_OFFSET + self.overlap_sines(n.pos.x)), 5)

            #pygame.draw.circle(surf, (0, 51, 187), (n.pos.x, n.pos.y + self.overlap_sines(n.pos.x)), 5)

            if i > 0:
                leftPoint = self.wave_points[i-1]
                pygame.draw.line(surf, (0,51,187), (leftPoint.pos.x, leftPoint.pos.y + self.overlap_sines(leftPoint.pos.x)),
                                 (n.pos.x, n.pos.y + self.overlap_sines(n.pos.x)), 3)





    def update(self, dt: float):
        self.offset = self.offset + 1
        self.update_wave_points(self.wave_points, dt)