from logging.config import valid_ident
import pygame
import math
import random
from withinCircle import withinCircle
from constants import *
from enum import Enum

class Ant:
    def __init__(self,pos,home):
        self.antscale = 1
        self.antimage = pygame.image.load(r'Assets\ant.png').convert_alpha()
        self.maxSpeed = 15
        self.steerStrength = 1.7
        self.wanderStrength = 0.1
        self.position = pos
        self.velocity = pygame.math.Vector2(0,0)
        self.desireddir = pygame.math.Vector2(0,0)
        self.targetFoodList = []
        self.targetFood = None
        self.viewrange = 100 *self.antscale
        self.pickupRadius = 15 * self.antscale
        self.forward = pygame.math.Vector2(0,0)
        self.left = pygame.math.Vector2(0,0)
        self.right = pygame.math.Vector2(0,0)
        self.steerConstant = 3
        self.count = 0
        self.sensorSize = 20 * self.antscale
        self.sensorMiddleCentre = (0,0)
        self.sensorLeftCentre = (0,0)
        self.sensorRightCentre = (0,0)
        self.foodMode = True #True for find food, false for find home
        self.home = home
        self.trail = Trail()
        self.current_chunk = (0,0)
        self.angle = 0

    def CurrentChunk(self):
        chunkx = (self.position[0] // 80)
        chunky = (self.position[1] // 80)
        chunkx = max(0,min(chunkx,15))
        chunky = max(0,min(chunky,8))
        return (int(chunkx),int(chunky))

    def ChunksToCheck(self):
        returnlist = []
        x1,y1 = -1,-1
        x2,y2 = 2,2
        itself = False
        if  -22.5 < self.angle < 22.5:
            x1,x2 = 1,2
            itself = True
        elif 22.5 < self.angle < 67.5:
            x1,x2 = 0,2
            y1,y2 = 0,2
        elif -67.5 < self.angle < -22.5:
            x1,x2=0,2
            y1,y2=-1,1
        elif 67.5 < self.angle < 112.5:
            y1,y2 = 1,2
            itself = True
        elif  -112.5 < self.angle < -67.5:
            y1,y2 = -1,0
            itself = True
        elif 112.5 < self.angle < 157.5:
            x1,x2 = -1,1
            y1,y2 = 0,2
        elif -157.5 < self.angle < -112.5:
            x1,x2=-1,1
            y1,y2=-1,1
        elif   self.angle > 157.5 or self.angle < -157.5:
            x1,x2 = -1,0
            itself = True

        for x in range(x1,x2):
            for y in range(y1,y2):
                chunkchecking = (self.current_chunk[0]+x,self.current_chunk[1]+y)
                if  0 <= chunkchecking[0] <= 15 and 0 <= chunkchecking[1] <= 8: 
                    returnlist.append(chunkchecking)
        if itself:
            returnlist.append(self.current_chunk)
        return returnlist

    def RandomMovementOffset(self):
        t = random.random()
        u = random.random()
        x = 1 * math.sqrt(t) * math.cos(2 * math.pi * u)
        y = 1 * math.sqrt(t) * math.sin(2 * math.pi * u)
        return pygame.math.Vector2(x,y)

    def HandleFood(self,foodList,trailList,chunks):
        
        if len(self.targetFoodList) == 0:
            for food in foodList:
                if withinCircle(self.position[0],self.position[1],self.viewrange,food.pos[0],food.pos[1]):
                    self.targetFoodList.append(food)
            
            if len(self.targetFoodList) > 0:
                self.targetFood = random.choice(self.targetFoodList)


                self.desireddir = pygame.math.Vector2.normalize(self.targetFood.pos - self.position)
        else:
            self.desireddir = pygame.math.Vector2.normalize(self.targetFood.pos - self.position)
            if pygame.math.Vector2.length(self.targetFood.pos - self.position) <= self.pickupRadius:
                try:
                    self.targetFood.AssignParent(self)
                    foodList.remove(self.targetFood)
                    self.targetFoodList = []
                    self.trail.ActivateAll(chunks)
                    trailList.append(self.trail)
                    self.foodMode = False
                    self.trail = Trail()
                except:
                    self.targetFood = None
                    self.targetFoodList = []

                
    def HandlePheramoneDirection(self,chunks):
        chunksToCheck = self.ChunksToCheck()
        for chunk in chunksToCheck:
            for marker in chunks[chunk]:
                if marker.value:
                    if self.foodMode and marker.value == Marker.TOFOOD:
                        pass  
                    elif not self.foodMode and marker.value == Marker.TOHOME:
                        pass
                    
        

    def HandleEdgeAvoidance(self):
        if self.sensorLeftCentre[0] > SCREENWIDTH or self.sensorLeftCentre[0] < 0 or self.sensorLeftCentre[1] > SCREENHEIGHT or self.sensorLeftCentre[1] < 0:
            self.desireddir = self.right
        elif self.sensorRightCentre[0] > SCREENWIDTH or self.sensorRightCentre[0] < 0 or self.sensorRightCentre[1] > SCREENHEIGHT or self.sensorRightCentre[1] < 0:
            self.desireddir = self.left
        
        

    def UpdateSensorPosition(self,screen):
        vel = self.velocity
        if pygame.math.Vector2.length(vel) != 0:
            pygame.math.Vector2.scale_to_length(vel,50)
        self.sensorMiddleCentre = self.position + vel
        self.sensorLeftCentre = self.position + pygame.math.Vector2.rotate(vel,-45)
        self.sensorRightCentre = self.position + pygame.math.Vector2.rotate(vel,45)
        
        #pygame.draw.circle(screen,[0,255,0],self.sensorMiddleCentre,self.sensorSize)
        #pygame.draw.circle(screen,[255,255,0],self.sensorLeftCentre,self.sensorSize)
        #pygame.draw.circle(screen,[0,255,255],self.sensorRightCentre,self.sensorSize)


    def UpdatePosition(self,screen):
        screen.blit(pygame.transform.rotate(self.antimage,self.angle),self.position-[16,16])

    

    def Update(self,clock,screen,foodList,deltaTime,chunks,trailList):
        offset = self.RandomMovementOffset() #get a movementoffset for wander
        
        self.desireddir = pygame.math.Vector2.normalize(self.desireddir+(offset*self.wanderStrength))
  
        self.HandlePheramoneDirection(chunks)
        
        if self.foodMode:
            self.HandleFood(foodList,trailList,chunks)

        self.HandleEdgeAvoidance()
        desiredVelocity = self.desireddir * self.maxSpeed #set desired velocity to max speed
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength #set steer based on how fast it is wants to go
        acceleration = desiredSteeringForce / 1
        if pygame.math.Vector2.length(desiredSteeringForce) > self.steerStrength: #make sure its not over the limit
            pygame.math.Vector2.scale_to_length(desiredSteeringForce,self.steerStrength)
        
        self.velocity = self.velocity+acceleration*deltaTime #set velocity to accel+velocity*time elapsed since last frame
        if (pygame.math.Vector2.length(self.velocity)) > self.maxSpeed: #make sure its not over the limit
            pygame.math.Vector2.scale_to_length(self.velocity,self.maxSpeed)
        
        self.position += self.velocity*deltaTime #update its pos
        
        self.angle = -(math.degrees(math.atan2(self.velocity.y,self.velocity.x))) #get its self.angle
        self.UpdateSensorPosition(screen)
        self.UpdatePosition(screen)
        self.current_chunk = self.CurrentChunk()
        self.count += 1
        if self.count == 15:
            pos = [self.position[0],self.position[1]]
            if self.foodMode:
                newPheramone = PheramoneToHome(pos,self.current_chunk,self.trail)
                self.trail.pheramones.append(newPheramone)
            else:
                newPheramone = PheramoneToFood(pos,self.current_chunk,self.trail)
                self.trail.pheramones.append(newPheramone)
            self.count = 0

        
        

class Food:
    def __init__(self,location,radius=3):
        self.pos = pygame.math.Vector2(location[0],location[1])
        self.radius = radius
        self.parent = None


    def Update(self,screen):
        if self.parent == None:
            pygame.draw.circle(screen,[0,255,0],self.pos,self.radius)

    def AssignParent(self,parent):
        self.parent = parent


class Trail:
    def __init__(self,state=False):
        self.pheramones = []
        self.active = state

    def ActivateAll(self,chunks):
        self.pheramones.reverse()
        for index,pheramone in enumerate(self.pheramones):
            pheramone.active = True
            pheramone.strength -= index
            chunks[pheramone.currentChunk].append(pheramone)
        

    def Update(self):
        for pheramone in self.pheramones:
            if pheramone.strength < 0:
                self.pheramones.remove(pheramone)

class MarkerState(Enum):
    NULL = 0
    TOHOME = 1
    TOFOOD = 2


class Marker:
    def __init__(self,intensity=1000,state=MarkerState.NULL):
        self.state = state
        self.intensity = intensity
        self.intensity *= self.value


    def Update(self,deltaTime):
        self.intensity -= 1.0*deltaTime

    def IsDone(self):
        return self.intensity < 0



class Home:
    def __init__(self,pos,radius):
        self.position = pos
        self.radius = radius

    def Draw(self,screen):
        pygame.draw.circle(screen,[0,0,0],self.position,self.radius)

    
