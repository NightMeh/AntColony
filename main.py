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
    renderqueue = {}

    for chunky in range(SCREENHEIGHT//CHUNKSIZE):
        for chunkx in range(SCREENWIDTH//CHUNKSIZE):
            markers = []
            for celly in range(CHUNKSIZE//CELLSIZE):
                for cellx in range(CHUNKSIZE//CELLSIZE):
                    markers.append(ant.Marker((cellx,celly),(chunkx,chunky)))
            chunks[(chunkx,chunky)] = np.array(markers,dtype=object)
            
            renderqueue[(chunkx,chunky)] = []
    
    home = ant.Home((600,500),20)
    for x in range(50):
        antList.append(ant.Ant((600,350),home))

    while playing:
        engine.update_dt()
        pygame.display.set_caption("{:.2f}".format(engine.clock.get_fps()))

        #deltaTime = clock.tick(400)/10
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                chunkx = (position[0] // CHUNKSIZE)
                chunky = (position[1] // CHUNKSIZE)
                chunkx = max(0, min(chunkx, (SCREENWIDTH//CHUNKSIZE)-1))
                chunky = max(0, min(chunky, (SCREENHEIGHT//CHUNKSIZE)-1))
                cellx = (position[0] - chunkx*CHUNKSIZE)//CELLSIZE
                celly = (position[1] - chunky*CHUNKSIZE)//CELLSIZE
                current_chunk = (int(chunkx), int(chunky))
                current_cell = (int(cellx),int(celly))
                index = current_cell[0] + current_cell[1] * 8
                chunks[current_chunk][index].state = ant.MarkerState.FOOD
                renderqueue[current_chunk].append(chunks[current_chunk][index])
                
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        pass
                    case pygame.K_s:
                        pass


        for chunk in renderqueue:
            for marker in renderqueue[chunk]:
                mx = marker.position[0]*CELLSIZE + chunk[0] * CHUNKSIZE
                my = marker.position[1]*CELLSIZE + chunk[1] * CHUNKSIZE
                if marker.state == ant.MarkerState.TOHOME or marker.state == ant.MarkerState.TOFOOD:
                    if marker.state == ant.MarkerState.TOHOME:
                        pygame.draw.rect(screen,[0,0,255],pygame.Rect((mx,my),(CELLSIZE,CELLSIZE)))
                    if marker.state == ant.MarkerState.TOFOOD:
                        pygame.draw.rect(screen,[0,255,0],pygame.Rect((mx,my),(CELLSIZE,CELLSIZE)))
                    marker.Update(engine.dt,renderqueue,chunks)
                if marker.state == ant.MarkerState.FOOD:
                    pygame.draw.rect(screen,[255,0,0],pygame.Rect((mx,my),(CELLSIZE,CELLSIZE)))
                    


        for x in range(len(antList)):
                    antList[x].Update(screen,engine.dt,chunks,renderqueue)

        pygame.display.flip()
        screen.fill([255, 255, 255])
        

with cProfile.Profile() as pr:
    testfunc()
    

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
#stats.print_stats()

stats.dump_stats(filename="test.prof")