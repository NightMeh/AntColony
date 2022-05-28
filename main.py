import ant
import pygame
import cProfile
import pstats
from constants import *
from engine import Engine


engine = Engine()

def testfunc():
    playing = True
    foodList = []
    totalfood = []
    trailList = []
    antList = []
    screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
    screen.fill([0, 0, 0])
    testtrail = ant.Trail(True)
    trailList.append(testtrail)
    chunks = {}

    for chunky in range(0,9):
        for chunkx in range(0,16):
            chunks[(chunkx,chunky)] = []

    clock = pygame.time.Clock()
    home = ant.Home((600,500),20)
    for x in range(200):
        antList.append(ant.Ant((600,350),home))


    while playing:
        engine.update_dt()
        pygame.display.set_caption("{:.2f}".format(engine.clock.get_fps()))

        #deltaTime = clock.tick(400)/10
        for x in range(len(antList)):
            antList[x].Update(clock,screen,foodList,engine.dt,chunks,trailList)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                newfood = ant.Food(pygame.mouse.get_pos(),3)
                foodList.append(newfood)
                totalfood.append(newfood)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        chunkx = (pygame.mouse.get_pos()[0] // 80)
                        chunky = (pygame.mouse.get_pos()[1] // 80)
                        newPheramone = ant.PheramoneToHome(pygame.mouse.get_pos(),(chunkx,chunky),testtrail)
                        testtrail.pheramones.append(newPheramone)
                        chunks[(chunkx,chunky)].append(newPheramone)
                    case pygame.K_s:
                        chunkx = (pygame.mouse.get_pos()[0] // 80)
                        chunky = (pygame.mouse.get_pos()[1] // 80)
                        newPheramone = ant.PheramoneToFood(pygame.mouse.get_pos(),(chunkx,chunky),testtrail)
                        testtrail.pheramones.append(newPheramone)
                        chunks[(chunkx,chunky)].append(newPheramone)

        for food in totalfood:
            food.Update(screen)

        for trail in trailList:
            trail.Update()
            for pheramone in trail.pheramones:
                pheramone.Update(screen,chunks)


        home.Draw(screen)
        
        pygame.display.flip()
        screen.fill([255, 255, 255])
        

with cProfile.Profile() as pr:
    testfunc()
    

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
#stats.print_stats()

stats.dump_stats(filename="28-5-22.prof")