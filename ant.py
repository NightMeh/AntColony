import pygame
import math

class Ant:
    def __init__(self,x,y,rotation):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.rotation = rotation
        self.targetx,self.targety = self.x,self.y
        
    def createtargetlocation(self):
        rads = math.radians(self.rotation)
        self.targety = self.speed * math.cos(rads)
        self.targety = self.y - self.targety
        self.targetx = self.speed * math.sin(rads)
        self.targetx +=self.x

    def draw(self,screen):
        pygame.draw.circle(screen, [255,0,0], (self.x,self.y), 2)
        pygame.draw.circle(screen, [0,0,255], (self.targetx,self.targety), 1)

    def findMovePerFrame(self):
        """dx = x - self.x
        dy = y - self.y
        stepx, stepy = dx/60,dy/60
        return stepx, stepy"""
        a = pygame.math.Vector2(self.x,self.y)
        b = pygame.math.Vector2(self.targetx,self.targety)
        return b

    def updatePosition(self,vec):
        self.x = vec.x
        self.y = vec.y