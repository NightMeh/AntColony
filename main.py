import ant
import pygame
import random

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()
clock = pygame.time.Clock()

testant = ant.Ant(400,500,180)
#baseendx = 600
#baseendy = 200
#variance = 400

while playing:
    clock.tick(60)
    stepvec = testant.findMovePerFrame()
    testant.updatePosition(stepvec)
    testant.draw(screen)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False