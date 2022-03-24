import pygame

class Ant:
    def __init__(self,x,y):
        self.location = (x,y)

    def draw(self,screen):
        pygame.draw.circle(screen, [255,0,0], self.location, 5)
        pygame.display.flip() #add to end of draw all