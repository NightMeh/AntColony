import pygame
import math
import random
class Ant:
    def __init__(self,pos):
        self.antimage = pygame.image.load(r'Assets\ant.png').convert_alpha()
        self.maxSpeed = 100
        self.steerStrength = 4
        self.wanderStrength = 0.2
        #self.target = target
        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.desireddir = pygame.math.Vector2(0,0)

    def HandleFood(self):
        #if no target food
            #get all food with perception radius
            #select one of the random food if foodlist > 0
            #get dir to food (foodpos-pos).normalize
            #start targetting food if its in view angle
        #else 
        #desireddir = targetfood -pos normal
        #pickup if within close radius
        #set food parent to ant
        #set target food as empty

        print("done")


    def UpdatePosition(self,screen,angle):
        #screen.blit(pygame.transform.rotate(self.antimage,-angle),self.position)
        screen.blit(self.antimage,self.position)
        print(angle)
        pygame.display.flip()

    def Update(self,clock,screen):
        deltaTime = clock.tick(60)/1000
        #self.desireddir = pygame.math.Vector2.normalize(self.target - self.position) #get unit vector for desired direction

        angleoffset = math.radians(random.randint(0,360))
        offset = pygame.math.Vector2(math.cos(angleoffset), math.sin(angleoffset))

        self.desireddir = pygame.math.Vector2.normalize(self.desireddir+(offset*self.wanderStrength))

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
        



