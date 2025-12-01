#!/usr/bin/env python
import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

from engine import World, Ball, Block

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("blocks.")
    clock = pygame.time.Clock()
    
    world = World()
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <level_file>")
        return 1
    world.load_level(sys.argv[1])

    mpos = None  # Initialisation pour éviter NameError

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mpos = pygame.mouse.get_pos()
                mpos = mpos[0], screen.get_height() - mpos[1]
                pygame.mouse.get_rel()  # Reset relative movement
            elif event.type == MOUSEBUTTONUP and event.button == 1 and mpos is not None:
                ball = Ball(world.space, *mpos, radius=20)
                rel = pygame.mouse.get_rel()
                rel = rel[0] * 2, -rel[1] * 2
                world.append(ball)
                ball.apply_impulse(*rel)
                mpos = None  # Réinitialiser pour éviter réutilisation

        screen.fill(THECOLORS["white"])

        # Step physics
        world.space.step(1/120.0)  # 120 FPS plus raisonnable

        # Draw everything
        world.draw(screen)

        pygame.display.flip()
        clock.tick(120)

    return 0

if __name__ == '__main__':
    sys.exit(main())
