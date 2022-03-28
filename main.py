from turtle import update
import ant
import pygame
import random
import threading
import numpy

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()
clock = pygame.time.Clock()

antcount = 400
ants = []

for x in range(int(antcount)):
    ants.append(ant.Ant(250,250,40))

antsplit = numpy.array_split(ants,4)

def updateants(ants,screen):
    for ant in ants:
        ant.createtargetlocation()
        stepvec = ant.findMovePerFrame()
        ant.updatePosition(stepvec)
        ant.draw(screen)
        ant.rotation += random.randint(-30,30)



while playing:
    clock.tick(200)
    t1 = threading.Thread(target=updateants, args=[list(antsplit[0]),screen])
    t2 = threading.Thread(target=updateants, args=[list(antsplit[1]),screen])
    t3 = threading.Thread(target=updateants, args=[list(antsplit[2]),screen])
    t4 = threading.Thread(target=updateants, args=[list(antsplit[3]),screen])
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    pygame.display.update()
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False