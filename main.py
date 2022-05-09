import ant
import pygame

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
foodList = []
totalfood = []
pheramoneList = []
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()

clock = pygame.time.Clock()

ant1 = ant.Ant((600,350))
ant2 = ant.Ant((500,400))
while playing:
    clock.tick(400)
    
    ant1.Update(clock,screen,foodList,pheramoneList)
    ant2.Update(clock,screen,foodList,pheramoneList)
    
    
    
    #ant1.target = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            newfood = ant.Food(pygame.mouse.get_pos(),3)
            foodList.append(newfood)
            totalfood.append(newfood)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                newPheramone = ant.Pheramone(pygame.mouse.get_pos())
                pheramoneList.append(newPheramone)

    for food in totalfood:
        food.Update(screen)

    for pheramone in pheramoneList:
        pheramone.Update(screen,pheramoneList,clock)
    
    pygame.display.flip()
    screen.fill([255, 255, 255])
    