import pygame
import math
SCREENHEIGHT = 720
SCREENWIDTH = 1280
CHUNKSIZE = 80

class Ant:
    def __init__(self,x,y,rotation):
        self.x = x
        self.y = y
        self.speed = 2
        self.rotation = rotation
        self.antradius = 2
        self.targetx,self.targety = self.x,self.y
        self.currentchunk = self.updatechunk()
        visionarray = []
        
        
    def updatechunk(self):
        return (math.floor(self.x/CHUNKSIZE),math.floor(self.y/CHUNKSIZE))

    def createtargetlocation(self,movementarea):
        count = 0
        rads = math.radians(self.rotation)
        self.targety = self.speed * math.cos(rads)
        self.targety = self.y - self.targety
        self.targetx = self.speed * math.sin(rads)
        self.targetx +=self.x
        
        while movementarea.collidepoint(self.targetx,self.targety) == False:
            if count > 1:
                self.rotation+= 30
            rads = math.radians(self.rotation)
            self.targety = self.speed * math.cos(rads)
            self.targety = self.y - self.targety
            self.targetx = self.speed * math.sin(rads)
            self.targetx +=self.x
            count += 1


    def createvisionpoints(self):
        self.visionarray = []
        for x in range(-45,46,45):
            rads = math.radians(self.rotation+x)
            targety = self.speed * math.cos(rads)
            targety = self.y - self.targety
            targetx = self.speed * math.sin(rads)
            targetx +=self.x
            self.visionarray.append(Visioncone(targetx,targety,10))

    def findpheramones(self,chunkdata):
        highest = 0
        location = 0
        for x in range(len(self.visionarray)):
            vision = self.visionarray[x].detectpheramone(chunkdata,self.currentchunk)
            if vision > highest:
                location = x
        if location == 0:
            self.rotation -= 2
        elif location == 2:
            self.rotation += 2


    def draw(self,screen):
        pygame.draw.circle(screen, [255,0,0], (self.x,self.y), self.antradius)
        pygame.draw.circle(screen, [0,0,255], (self.targetx,self.targety), 1)

    def findMovePerFrame(self):
        """dx = x - self.x
        dy = y - self.y
        stepx, stepy = dx/60,dy/60
        return stepx, stepy"""
        a = pygame.math.Vector2(self.x,self.y)
        b = pygame.math.Vector2(self.targetx,self.targety)
        return b

    def updatePosition(self,vec,chunkdata):
        self.x = vec.x
        self.y = vec.y
        self.currentchunk = self.updatechunk()
        chunkdata[self.currentchunk].append(Pheramone((self.x,self.y),5))

class Visioncone:
    def __init__(self,x,y,width):
        self.x = x
        self.y = y
        self.width = width/2
    
    def detectpheramone(self,chunkdata,currentchunk):
        #loop through pheramones in chunks and adjacent
        #find collisons iwth pheramones
        #find strength
        fulllist = []
        for x in range(-1,2):
            if currentchunk[0]-1 != -1 and currentchunk[1]+x != (SCREENHEIGHT/CHUNKSIZE)-1 and currentchunk[1]+x != -1:
                fulllist += chunkdata[(currentchunk[0]-1,currentchunk[1]+x)]
            if currentchunk[1]+x != -1 and currentchunk[1]+x != (SCREENHEIGHT/CHUNKSIZE)-1 and currentchunk[1]+x != -1:
                fulllist += chunkdata[(currentchunk[0],currentchunk[1]+x)]
            if currentchunk[0]+1 != (SCREENWIDTH/CHUNKSIZE)-1 and currentchunk[1]+x != (SCREENHEIGHT/CHUNKSIZE)-1 and currentchunk[1]+x != -1:    
                fulllist += chunkdata[(currentchunk[0]+1,currentchunk[1]+x)]


        for x in range(len(fulllist)):
            if fulllist[x].rect.collidepoint(self.x,self.y) == True:
                return fulllist[x].strength
        return 0
        


class Pheramone:
    def __init__(self,location,antradius):
        self.x = location[0]
        self.y = location[1]
        self.strength = 100
        self.strengthloss = 2
        self.rect = pygame.Rect(self.x-antradius,self.y+antradius,2*antradius,2*antradius)

    def findchunk(self,chunksize):
        chunkx = math.floor(self.x/chunksize)
        chunky = math.floor(self.y/chunksize)
        return (chunkx,chunky)

    def update(self):
        self.strength-=self.strengthloss



