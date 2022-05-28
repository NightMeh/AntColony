import pygame
import math
import random
from withinCircle import withinCircle
from constants import *

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
        self.current_chunk = (-1,-1)

    def CurrentChunk(self):
        chunkx = (self.position[0] // 80)
        chunky = (self.position[1] // 80)
        chunkx = max(0,min(chunkx,15))
        chunky = max(0,min(chunky,8))
        return (int(chunkx),int(chunky))

    def ChunksToCheck(self):
        returnlist = []
        for x in range(-1,2):
            for y in range(-1,2):
                chunkchecking = (self.current_chunk[0]+x,self.current_chunk[1]+y)
                if  0 <= chunkchecking[0] <= 15 and 0 <= chunkchecking[1] <= 8: 
                    returnlist.append(chunkchecking)
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

    def GetDirections(self):
        self.forward = self.desireddir
        self.left = pygame.math.Vector2.rotate(self.desireddir,-self.steerConstant)
        self.right = pygame.math.Vector2.rotate(self.desireddir,self.steerConstant)

                
    def HandlePheramoneDirection(self,chunks):
        leftTotal = 0
        middleTotal = 0
        rightTotal = 0
        chunksToCheck = self.ChunksToCheck()
        for chunk in chunksToCheck:
            for pheramone in chunks[chunk]:
                if self.foodMode and str(type(pheramone))=="<class 'ant.PheramoneToFood'>":
                    if withinCircle(self.sensorLeftCentre[0],self.sensorLeftCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        leftTotal += pheramone.strength
                    if withinCircle(self.sensorMiddleCentre[0],self.sensorMiddleCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        middleTotal += pheramone.strength
                    if withinCircle(self.sensorRightCentre[0],self.sensorRightCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        rightTotal += pheramone.strength
                elif not self.foodMode and str(type(pheramone))=="<class 'ant.PheramoneToHome'>":
                    if withinCircle(self.sensorLeftCentre[0],self.sensorLeftCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        leftTotal += pheramone.strength
                    if withinCircle(self.sensorMiddleCentre[0],self.sensorMiddleCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        middleTotal += pheramone.strength
                    if withinCircle(self.sensorRightCentre[0],self.sensorRightCentre[1],self.sensorSize,pheramone.position[0],pheramone.position[1]):
                        rightTotal += pheramone.strength
        
        if leftTotal+rightTotal+middleTotal != 0:
            if max(leftTotal,middleTotal,rightTotal) == leftTotal:
                self.desireddir = self.left
            elif max(leftTotal,middleTotal,rightTotal) == rightTotal:
                self.desireddir = self.right
            elif max(leftTotal,middleTotal,rightTotal) == middleTotal:
                self.desireddir = self.desireddir

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


    def UpdatePosition(self,screen,angle):
        screen.blit(pygame.transform.rotate(self.antimage,-angle),self.position-[16,16])

    

    def Update(self,clock,screen,foodList,deltaTime,chunks,trailList):
        offset = self.RandomMovementOffset() #get a movementoffset for wander
        self.GetDirections()
        

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
        
        angle = math.degrees(math.atan2(self.velocity.y,self.velocity.x)) #get its angle
        self.UpdateSensorPosition(screen)
        self.UpdatePosition(screen,angle)
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

class PheramoneToFood:
    def __init__(self,position,chunk,trail):
        self.position = position
        self.strength = 750
        self.active = False
        self.currentChunk = chunk
        self.trail = trail

    def __type__(self):
        return "toFood"
    
    def __repr__(self):
        return f"{self.currentChunk}"


    def Update(self,screen,chunks):
        pygame.draw.circle(screen,[255,0,0],self.position,3)
        self.strength -= 1
        if self.strength < 0:
            chunks[self.currentChunk].remove(self)

class PheramoneToHome(PheramoneToFood):
    def __init__(self,pos,chunk,trail):
        super().__init__(pos,chunk,trail)
        
    def __type__(self):
        return "toHome"

    def Update(self,screen,chunks):
        pygame.draw.circle(screen,[0,0,255],self.position,3)
        self.strength -= 1

        if self.strength < 0:
            chunks[self.currentChunk].remove(self)
            self.trail.pheramones.remove(self)
            




    

class Home:
    def __init__(self,pos,radius):
        self.position = pos
        self.radius = radius

    def Draw(self,screen):
        pygame.draw.circle(screen,[0,0,0],self.position,self.radius)

    
