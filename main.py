from functools import lru_cache
import ant
import pygame
import cProfile
import pstats
import numpy as np
from constants import *
from engine import Engine


engine = Engine()

def testfunc():
    playing = True
    antList = []
    screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
    screen.fill([0, 0, 0])
    chunks = {}

    for chunky in range(SCREENHEIGHT//CHUNKSIZE):
        for chunkx in range(SCREENWIDTH//CHUNKSIZE):
            markers = []
            for cellx in range(CHUNKSIZE//CELLSIZE):
                for celly in range(CHUNKSIZE//CELLSIZE):
                    markers.append(ant.Marker())
            chunks[(chunkx,chunky)] = np.array(markers,dtype=object)

    clock = pygame.time.Clock()
    home = ant.Home((600,500),20)
    for x in range(50):
        antList.append(ant.Ant((600,350),home))


    while playing:
        engine.update_dt()
        pygame.display.set_caption("{:.2f}".format(engine.clock.get_fps()))

        #deltaTime = clock.tick(400)/10
        for x in range(len(antList)):
            antList[x].Update(screen,engine.dt,chunks)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        pass
                    case pygame.K_s:
                        pass

        home.Draw(screen)

        def markerMaths(chunk,index):
            markerx = (CHUNKSIZE*chunk[0])+(index%(CHUNKSIZE/CELLSIZE))*CELLSIZE
            markery = CHUNKSIZE*chunk[1]+(index // (CHUNKSIZE/CELLSIZE))*CELLSIZE
            return markerx,markery

        @lru_cache(maxsize=10)
        def drawStates(screen):
            for chunk in chunks:
                for index,marker in enumerate(chunks[chunk]):
                    markerx,markery = markerMaths(chunk,index)
                    if marker.state == ant.MarkerState.TOHOME:
                        pygame.draw.rect(screen,[0,0,255],pygame.Rect((markerx,markery),(CELLSIZE,CELLSIZE)))
                    if marker.state == ant.MarkerState.TOFOOD:
                        pygame.draw.rect(screen,[0,255,0],pygame.Rect((markerx,markery),(CELLSIZE,CELLSIZE)))

        #drawStates(screen)

        pygame.display.flip()
        screen.fill([255, 255, 255])
        

with cProfile.Profile() as pr:
    testfunc()
    

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
#stats.print_stats()

stats.dump_stats(filename="test.prof")