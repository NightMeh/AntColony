import pygame
import math
import random
class Ant:
    def __init__(self,pos,home):
        self.antscale = 1
        self.antimage = pygame.image.load(r'Assets\ant.png').convert_alpha()
        self.maxSpeed = 5
        self.steerStrength = 1.5
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
        self.sensorMiddleCentre = []
        self.sensorLeftCentre = []
        self.sensorRightCentre = []
        self.foodMode = True #True for find food, false for find home
        self.home = home



    def RandomMovementOffset(self):
        t = random.random()
        u = random.random()
        x = 1 * math.sqrt(t) * math.cos(2 * math.pi * u)
        y = 1 * math.sqrt(t) * math.sin(2 * math.pi * u)
        return pygame.math.Vector2(x,y)

    def WithinCircle(self,center_x,center_y,radius,x,y):
        square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
        return square_dist <= radius ** 2

    def HandleFood(self,foodList):
        if len(self.targetFoodList) == 0:
            for food in foodList:
                if self.WithinCircle(self.position[0],self.position[1],self.viewrange,food.pos[0],food.pos[1]):
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
                    self.foodMode = False
                except:
                    print("nevermind")
                    self.targetFood = None
                    self.targetFoodList = []

    def GetDirections(self):
        self.forward = self.desireddir
        self.left = pygame.math.Vector2.rotate(self.desireddir,-self.steerConstant)
        self.right = pygame.math.Vector2.rotate(self.desireddir,self.steerConstant)

                
    def HandlePheramoneDirection(self,pheramoneList):
        leftTotal = 0
        middleTotal = 0
        rightTotal = 0
        for x in range(len(pheramoneList)):
            if self.WithinCircle(self.sensorLeftCentre[0],self.sensorLeftCentre[1],self.sensorSize,pheramoneList[x].position[0],pheramoneList[x].position[1]):
                leftTotal += pheramoneList[x].strength
            if self.WithinCircle(self.sensorMiddleCentre[0],self.sensorMiddleCentre[1],self.sensorSize,pheramoneList[x].position[0],pheramoneList[x].position[1]):
                middleTotal += pheramoneList[x].strength
            if self.WithinCircle(self.sensorRightCentre[0],self.sensorRightCentre[1],self.sensorSize,pheramoneList[x].position[0],pheramoneList[x].position[1]):
                rightTotal += pheramoneList[x].strength
        
        if leftTotal+rightTotal+middleTotal != 0:
            if max(leftTotal,middleTotal,rightTotal) == leftTotal:
                self.desireddir = self.left
            elif max(leftTotal,middleTotal,rightTotal) == rightTotal:
                self.desireddir = self.right
            elif max(leftTotal,middleTotal,rightTotal) == middleTotal:
                self.desireddir = self.desireddir

    def UpdateSensorPosition(self,screen):
        vel = self.velocity
        if pygame.math.Vector2.length(vel) != 0:
            pygame.math.Vector2.scale_to_length(vel,50)
        self.sensorMiddleCentre = self.position + vel
        self.sensorLeftCentre = self.position + pygame.math.Vector2.rotate(vel,-45)
        self.sensorRightCentre = self.position + pygame.math.Vector2.rotate(vel,45)
        pygame.draw.circle(screen,[0,255,0],self.sensorMiddleCentre,self.sensorSize)
        pygame.draw.circle(screen,[255,255,0],self.sensorLeftCentre,self.sensorSize)
        pygame.draw.circle(screen,[0,255,255],self.sensorRightCentre,self.sensorSize)


    def UpdatePosition(self,screen,angle):
        screen.blit(pygame.transform.rotate(self.antimage,-angle),self.position-[16,16])

    

    def Update(self,clock,screen,foodList,pheramoneList,pheramoneToHomeList):
        deltaTime = clock.tick(400)/10 #get deltatime
        
        offset = self.RandomMovementOffset() #get a movementoffset for wander
        self.GetDirections()
        

        self.desireddir = pygame.math.Vector2.normalize(self.desireddir+(offset*self.wanderStrength))
        if self.foodMode == True:
            self.HandlePheramoneDirection(pheramoneList)
        else:
            print("ww")
            self.HandlePheramoneDirection(pheramoneToHomeList)
        
        if self.foodMode == True:
            self.HandleFood(foodList)
        desiredVelocity = self.desireddir * self.maxSpeed #set desired velocity to max speed
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength #set steer based on how fast it is wants to go
        acceleration = desiredSteeringForce / 1
        if pygame.math.Vector2.length(desiredSteeringForce) > self.steerStrength: #make sure its not over the limit
            pygame.math.Vector2.scale_to_length(desiredSteeringForce,self.steerStrength)
        
        self.velocity = self.velocity+acceleration*deltaTime #set velocity to accel*velocity*time elapsed since last frame
        if (pygame.math.Vector2.length(self.velocity)) > self.maxSpeed: #make sure its not over the limit
            pygame.math.Vector2.scale_to_length(self.velocity,self.maxSpeed)
        
        self.position += self.velocity*deltaTime #update its pos
        
        angle = math.degrees(math.atan2(self.velocity.y,self.velocity.x)) #get its angle
        self.UpdateSensorPosition(screen)
        self.UpdatePosition(screen,angle)
        self.count += 1
        if self.count == 75:
            pos = [self.position[0],self.position[1]]
            if self.foodMode == True:
                newPheramone = PheramoneToHome(pos)
            else:
                newPheramone = PheramoneToFood(pos)
            pheramoneList.append(newPheramone)
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

class PheramoneToFood:
    def __init__(self,position):
        self.position = position
        self.strength = 2000

    def Update(self,screen,pheramoneList):
        pygame.draw.circle(screen,[255,0,0],self.position,3)
        self.strength -= 1
        if self.strength < 0:
            pheramoneList.remove(self)

class PheramoneToHome(PheramoneToFood):
    def __init__(self,pos):
        super().__init__(pos)
        
    def Update(self,screen,pheramoneToHomeList):
        pygame.draw.circle(screen,[0,0,255],self.position,3)
        self.strength -= 1
        if self.strength < 0:
            pheramoneToHomeList.remove(self)

    

class Home:
    def __init__(self,pos,radius):
        self.position = pos
        self.radius = radius

    def Draw(self,screen):
        pygame.draw.circle(screen,[0,0,0],self.position,self.radius)

    
