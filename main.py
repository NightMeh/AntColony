import ant
import pygame
import random

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()
antlist = []
for x in range(20):
    antlist.append(ant.Ant(random.randint(0,SCREENWIDTH),random.randint(0,SCREENHEIGHT)))
    
for y in range(len(antlist)):
    antlist[y].draw(screen)

while playing:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False