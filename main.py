import ant
import pygame
import random
import threading
import numpy

SCREENHEIGHT = 720
SCREENWIDTH = 1280
CHUNKSIZE = 80
offset = 30

playing = True
chunkdata = {}
movementarea = pygame.Rect(offset,offset,SCREENWIDTH-2*offset,SCREENHEIGHT-2*offset)

for chunky in range(int(SCREENHEIGHT/CHUNKSIZE)):
    for chunkx in range(int(SCREENWIDTH/CHUNKSIZE)):
        chunkdata[(chunkx,chunky)] = []

screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()
clock = pygame.time.Clock()

antcount = 40
ants = []

for x in range(int(antcount)):
    ants.append(ant.Ant(250,250,40))

antsplit = numpy.array_split(ants,4)
varience = 30

def updateants(ants,screen):
    for ant in ants:
        ant.createvisionpoints()
        ant.findpheramones(chunkdata)
        ant.createtargetlocation(movementarea)
        stepvec = ant.findMovePerFrame()
        ant.updatePosition(stepvec,chunkdata)
        ant.draw(screen)
        ant.rotation += random.randint(-varience,varience)

while playing:
    clock.tick(60)
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