import pygame
import math
import random
class Ant:
    def __init__(self,pos):
        self.antimage = pygame.image.load(r'Assets\ant.png').convert_alpha()
        self.maxSpeed = 150
        self.steerStrength = 4
        self.wanderStrength = 0.2
        #self.target = target
        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.desireddir = pygame.math.Vector2(0,0)
        self.targetFoodList = []
        self.targetFood = None
        self.pickupRadius = 10

    def WithinCircle(self,center_x,center_y,radius,x,y):
        square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
        return square_dist <= radius ** 2

    def HandleFood(self,foodList):
        if len(self.targetFoodList) == 0:
            for food in foodList:
                if self.WithinCircle(self.position[0],self.position[1],100,food.pos[0],food.pos[1]):
                    self.targetFoodList.append(food)
            
            if len(self.targetFoodList) > 0:
                self.targetFood = random.choice(self.targetFoodList)
                print(f"{self.targetFood.pos - self.position}food")


                self.desireddir = pygame.math.Vector2.normalize(self.targetFood.pos - self.position)
                #select one of the random food if foodlist > 0
                #get dir to food (foodpos-pos).normalize
                #start targetting food if its in view angle
        else:
            self.desireddir = pygame.math.Vector2.normalize(self.targetFood.pos - self.position)

            if pygame.math.Vector2.length(self.targetFood.pos - self.position) <= self.pickupRadius:
                print("near")
                self.targetFood.AssignParent(self)
                foodList.remove(self.targetFood)
                self.targetFoodList = []
                self.targetFood = None
                



        #else 
        #desireddir = targetfood -pos normal
        #pickup if within close radius
        #set food parent to ant
        #set target food as empty



    def UpdatePosition(self,screen,angle):
        screen.blit(pygame.transform.rotate(self.antimage,-angle),self.position-[16,16])
        #screen.blit(self.antimage,self.position)

    def Update(self,clock,screen,foodList):
        deltaTime = clock.tick(60)/1000
        #self.desireddir = pygame.math.Vector2.normalize(self.target - self.position) #get unit vector for desired direction
        
        angleoffset = math.radians(random.randint(0,360))
        offset = pygame.math.Vector2(math.cos(angleoffset), math.sin(angleoffset))

        self.desireddir = pygame.math.Vector2.normalize(self.desireddir+(offset*self.wanderStrength))
        self.HandleFood(foodList)
        desiredVelocity = self.desireddir * self.maxSpeed #set desired velocity to max speed
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength #set steer based on how fast it is wants to go
        acceleration = desiredSteeringForce / 1
        if pygame.math.Vector2.length(desiredSteeringForce) > self.steerStrength: #make sure its not over the limit
            desiredSteeringForce = pygame.math.Vector2.scale_to_length(desiredSteeringForce,self.steerStrength)
        
        self.velocity = self.velocity+acceleration*deltaTime #set velocity to accel*velocity*time elapsed since last frame
        if pygame.math.Vector2.length(self.velocity+acceleration*deltaTime) > self.maxSpeed: #make sure its not over the limit
            self.velocity = pygame.math.Vector2.scale_to_length(self.velocity,self.maxSpeed)

        self.position += self.velocity*deltaTime #update its pos
        
        angle = math.degrees(math.atan2(self.velocity.y,self.velocity.x)) #get its angle
        
        self.UpdatePosition(screen,angle)

        
        

class Food:
    def __init__(self,location,radius=3):
        self.pos = pygame.math.Vector2(location[0],location[1])
        self.radius = radius
        self.parent = None


    def Update(self,screen):
        
        if self.parent != None:
            pygame.draw.circle(screen,[0,255,0],self.parent.position,self.radius)
        else:
            pygame.draw.circle(screen,[0,255,0],self.pos,self.radius)

    def AssignParent(self,parent):
        self.parent = parent


    
