import pygame
import math

class Ant:
    def __init__(self,x,y,rotation):
        self.x = x
        self.y = y
        self.speed = 2
        self.rotation = rotation
        self.targetx,self.targety = self.x,self.y
        
    def createtargetlocation(self):
        rads = math.radians(self.rotation)
        self.targety = math.cos(rads)
        self.targety = self.y - self.targety
        self.targetx = math.sin(rads)
        self.targetx +=self.x
        print("current pos",self.x,self.y)
        print("target",self.targetx,self.targety)

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
        b = b*self.speed
        d = b-a
        print(d)
        return d

    def updatePosition(self,vec):
        self.x = vec.x
        self.y = vec.y