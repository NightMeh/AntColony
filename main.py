import ant
import pygame

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
foodList = []
totalfood = []
pheramoneList = []
pheramoneToHomeList = []
antList = []
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()

clock = pygame.time.Clock()
home = ant.Home((600,500),20)
for x in range(10):
    antList.append(ant.Ant((600,350),home))

while playing:
    clock.tick(400)
    
    for x in range(len(antList)):
        antList[x].Update(clock,screen,foodList,pheramoneList,pheramoneToHomeList)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            newfood = ant.Food(pygame.mouse.get_pos(),3)
            foodList.append(newfood)
            totalfood.append(newfood)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                newPheramone = ant.PheramoneToFood(pygame.mouse.get_pos())
                pheramoneList.append(newPheramone)
            if event.key == pygame.K_s:
                newPheramone = ant.PheramoneToHome(pygame.mouse.get_pos())
                pheramoneToHomeList.append(newPheramone)

    for food in totalfood:
        food.Update(screen)

    for pheramone in pheramoneList:
        pheramone.Update(screen,pheramoneList)

    for pheramone in pheramoneToHomeList:
        pheramone.Update(screen,pheramoneToHomeList)

    home.Draw(screen)
    
    pygame.display.flip()
    screen.fill([255, 255, 255])
    