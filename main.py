import ant
import pygame

SCREENHEIGHT = 720
SCREENWIDTH = 1280

playing = True
foodList = []
totalfood = []
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill([0, 0, 0])
pygame.display.flip()

clock = pygame.time.Clock()

ant1 = ant.Ant((600,350))

while playing:
    clock.tick(100)
    
    ant1.Update(clock,screen,foodList)
    
    
    
    #ant1.target = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            newfood = ant.Food(pygame.mouse.get_pos(),3)
            foodList.append(newfood)
            totalfood.append(newfood)


    for food in totalfood:
        food.Update(screen)
    
    pygame.display.flip()
    screen.fill([255, 255, 255])
    