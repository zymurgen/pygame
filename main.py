import pygame
from wave import Wave
import math

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Springy water")

clock = pygame.time.Clock()
is_running = True

wave = Wave()

def on_click(mx, my):
    closest_distance = -1
    closest_point = None
    for p in wave.wave_points:
        distance = math.fabs(mx - p.pos.x)
        if closest_distance == -1:
            closest_point = p
            closest_distance = distance
        elif distance <= closest_distance:
            closest_point = p
            closest_distance = distance

    closest_point.pos.y = my


while is_running:

    dt = clock.tick(FPS) / 1000

    #event handling
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            is_running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            on_click(mx, my)

    screen.fill(pygame.Color("white"))

    wave.update(dt)
    wave.draw(screen)
    pygame.display.update()

pygame.quit()
