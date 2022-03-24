import pygame
import math

class Ant:
    def __init__(self,x,y,rotation):
        self.x = x
        self.y = y
        self.speed = 2
        self.rotation = rotation
        self.createtargetlocation()
        print(self.targetx,self.targety)
        
        
    def createtargetlocation(self):
        radius = 100
        self.targetx = radius*math.sin(self.rotation)
        self.targetx = self.x - self.targetx
        self.targety = radius*math.cos(self.rotation)
        self.targety =self.y - self.targety

    def draw(self,screen):
        pygame.draw.circle(screen, [255,0,0], (self.x,self.y), 5)
        pygame.display.flip() #add to end of draw all
        pygame.draw.circle(screen, [0,0,255], (self.targetx,self.targety), 2)

    def findMovePerFrame(self):
        """dx = x - self.x
        dy = y - self.y
        stepx, stepy = dx/60,dy/60
        return stepx, stepy"""
        a = pygame.math.Vector2(self.x,self.y)
        b = pygame.math.Vector2(self.targetx,self.targety)
        c = pygame.math.Vector2.normalize(b)
        c = c*self.speed
        d = a+c
        return d


    def updatePosition(self,vec):
        self.x = vec.x
        self.y = vec.y