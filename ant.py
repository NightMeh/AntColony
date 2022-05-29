from logging.config import valid_ident
import pygame
import math
import random
from withinCircle import withinCircle
from constants import *
from enum import Enum


class Ant:
    def __init__(self, pos, home):
        self.antscale = 1
        self.antimage = pygame.image.load(r'Assets\ant.png').convert_alpha()
        self.maxSpeed = 15
        self.steerStrength = 1.7
        self.wanderStrength = 0.1
        self.position = pos
        self.velocity = pygame.math.Vector2(0, 0)
        self.desireddir = pygame.math.Vector2(0, 0)
        self.targetFoodList = []
        self.targetFood = None
        self.viewrange = 100 * self.antscale
        self.pickupRadius = 15 * self.antscale
        self.forward = pygame.math.Vector2(0, 0)
        self.left = pygame.math.Vector2(0, 0)
        self.right = pygame.math.Vector2(0, 0)
        self.steerConstant = 3
        self.count = 0
        self.sensorSize = 20 * self.antscale
        self.sensorMiddleCentre = (0, 0)
        self.sensorLeftCentre = (0, 0)
        self.sensorRightCentre = (0, 0)
        self.foodMode = True  # True for find food, false for find home
        self.home = home
        self.current_chunk = (0, 0)
        self.current_cell = (0, 0)
        self.angle = 0
        self.markerDetectionRange = 25

    def CurrentChunk(self):
        chunkx = (self.position[0] // CHUNKSIZE)
        chunky = (self.position[1] // CHUNKSIZE)
        chunkx = max(0, min(chunkx, (SCREENWIDTH/CHUNKSIZE)-1))
        chunky = max(0, min(chunky, (SCREENHEIGHT/CHUNKSIZE)-1))

        cellx = (self.position[0] - chunkx*CHUNKSIZE)/CELLSIZE
        celly = (self.position[1] - chunky*CHUNKSIZE)/CELLSIZE
        self.current_chunk = (int(chunkx), int(chunky))
        self.current_cell = (int(cellx), int(celly))

    def ChunksToCheck(self):
        returnlist = []
        x1, y1 = -1, -1
        x2, y2 = 2, 2
        itself = False
        if -22.5 < self.angle < 22.5:
            x1, x2 = 1, 2
            itself = True
        elif 22.5 < self.angle < 67.5:
            x1, x2 = 0, 2
            y1, y2 = 0, 2
        elif -67.5 < self.angle < -22.5:
            x1, x2 = 0, 2
            y1, y2 = -1, 1
        elif 67.5 < self.angle < 112.5:
            y1, y2 = 1, 2
            itself = True
        elif -112.5 < self.angle < -67.5:
            y1, y2 = -1, 0
            itself = True
        elif 112.5 < self.angle < 157.5:
            x1, x2 = -1, 1
            y1, y2 = 0, 2
        elif -157.5 < self.angle < -112.5:
            x1, x2 = -1, 1
            y1, y2 = -1, 1
        elif self.angle > 157.5 or self.angle < -157.5:
            x1, x2 = -1, 0
            itself = True

        for x in range(x1, x2):
            for y in range(y1, y2):
                chunkchecking = (
                    self.current_chunk[0]+x, self.current_chunk[1]+y)
                if 0 <= chunkchecking[0] <= 15 and 0 <= chunkchecking[1] <= 8:
                    returnlist.append(chunkchecking)
        if itself:
            returnlist.append(self.current_chunk)
        return returnlist

    def RandomMovementOffset(self):
        t = random.random()
        u = random.random()
        x = 1 * math.sqrt(t) * math.cos(2 * math.pi * u)
        y = 1 * math.sqrt(t) * math.sin(2 * math.pi * u)
        return pygame.math.Vector2(x, y)

    def HandleFood(self, chunks):
        if len(self.targetFoodList) == 0:
            chunksToCheck = self.ChunksToCheck()
            for chunk in chunksToCheck:
                for index,marker in enumerate(chunks[chunk]):
                    if marker.state == MarkerState.FOOD:
                        markerx = (CHUNKSIZE*chunk[0])+(index%(CHUNKSIZE/CELLSIZE))*CELLSIZE
                        markery = CHUNKSIZE*chunk[1]+(index // (CHUNKSIZE/CELLSIZE))*CELLSIZE
                        self.targetFoodList.append((pygame.math.Vector2(markerx,markery),marker))

            if len(self.targetFoodList) > 0:
                self.targetFood = random.choice(self.targetFoodList)
                self.desireddir = pygame.math.Vector2.normalize(self.targetFood[0] - self.position)
                
        else:
            self.desireddir = pygame.math.Vector2.normalize(self.targetFood[0] - self.position)

            if pygame.math.Vector2.length(self.targetFood[0] - self.position) <= self.pickupRadius:
                try:
                    #set marker to null
                    self.targetFood[1].state = MarkerState.NULL
                    self.targetFoodList = []
                    self.foodMode = False
                except:
                    self.targetFood = None
                    self.targetFoodList = []

    def HandlePheramoneDirection(self, chunks):
        chunksToCheck = self.ChunksToCheck()
        for chunk in chunksToCheck:
            total_intensity = 0
            for index,marker in enumerate(chunks[chunk]):
                if marker.state != MarkerState.NULL:
                    if self.foodMode and marker.state == MarkerState.TOFOOD:
                        markerx = (CHUNKSIZE*chunk[0])+(index%(CHUNKSIZE/CELLSIZE))*CELLSIZE
                        markery = CHUNKSIZE*chunk[1]+(index // (CHUNKSIZE/CELLSIZE))*CELLSIZE
                        markerpos = pygame.math.Vector2(markerx,markery)
                        tomarker = pygame.math.Vector2(markerpos - self.position)
                        length = pygame.math.Vector2.length(tomarker)
                        m_vecx = self.cos(self.angle)
                        m_vecy = self.sin(self.angle)
                        m_vec = pygame.math.Vector2(m_vecx,m_vecy)

                        if length < self.markerDetectionRange:
                            if pygame.math.Vector2.dot(tomarker,m_vec)>0:
                                total_intensity += marker.intensity
                                point += marker.intensity * markerpos

                    elif not self.foodMode and marker.state == MarkerState.TOHOME:
                        markerx = (CHUNKSIZE*chunk[0])+(index%(CHUNKSIZE/CELLSIZE))*CELLSIZE
                        markery = CHUNKSIZE*chunk[1]+(index // (CHUNKSIZE/CELLSIZE))*CELLSIZE
                        markerpos = pygame.math.Vector2(markerx,markery)
                        tomarker = pygame.math.Vector2(markerpos - self.position)
                        length = pygame.math.Vector2.length(tomarker)
                        m_vecx = self.cos(self.angle)
                        m_vecy = self.sin(self.angle)
                        m_vec = pygame.math.Vector2(m_vecx,m_vecy)

                        if length < self.markerDetectionRange:
                            if pygame.math.Vector2.dot(tomarker,m_vec)>0:
                                total_intensity += marker.intensity
                                point += marker.intensity * markerpos

                    if total_intensity:
                            tempvec = pygame.math.Vector2(point / total_intensity - self.position)
                            if tempvec.x > 0:
                                self.desireddir = math.acos(tempvec.x/pygame.math.Vector2.length(tempvec))
                            else:
                                self.desireddir = -(math.acos(tempvec.x/pygame.math.Vector2.length(tempvec)))


    def HandleEdgeAvoidance(self):
        if SCREENWIDTH < self.position[0] or self.position[0] < 0 or SCREENHEIGHT < self.position[1] or self.position[1] < 0:
            self.desireddir *= -1

    def UpdatePosition(self, screen):
        screen.blit(pygame.transform.rotate(self.antimage, self.angle), self.position-[16, 16])

    def PlaceMarker(self,chunks):
        index = ((self.position[0] % CHUNKSIZE) // CELLSIZE) + (((self.position[1] % CHUNKSIZE) // CELLSIZE) * CHUNKSIZE/CELLSIZE)
        index = int(index)
        if self.foodMode:
           chunks[self.current_chunk][index].state = MarkerState.TOHOME
        else:
           chunks[self.current_chunk][index].state = MarkerState.TOFOOD

    def Update(self, screen, deltaTime, chunks):
        offset = self.RandomMovementOffset()  # get a movementoffset for wander

        self.desireddir = pygame.math.Vector2.normalize(self.desireddir+(offset*self.wanderStrength))

        self.HandlePheramoneDirection(chunks)

        if self.foodMode:
            self.HandleFood(chunks)

        self.HandleEdgeAvoidance()
        # set desired velocity to max speed
        desiredVelocity = self.desireddir * self.maxSpeed
        # set steer based on how fast it is wants to go
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength
        acceleration = desiredSteeringForce / 1
        # make sure its not over the limit
        if pygame.math.Vector2.length(desiredSteeringForce) > self.steerStrength:
            pygame.math.Vector2.scale_to_length(desiredSteeringForce, self.steerStrength)

        # set velocity to accel+velocity*time elapsed since last frame
        self.velocity = self.velocity+acceleration*deltaTime

        if (pygame.math.Vector2.length(self.velocity)) > self.maxSpeed:  # make sure its not over the limit pygame.math.Vector2.scale_to_length(self.velocity, self.maxSpeed)
            pygame.math.Vector2.scale_to_length(self.velocity, self.maxSpeed)
        self.position += self.velocity*deltaTime  # update its pos

        # get its self.angle
        self.angle = -(math.degrees(math.atan2(self.velocity.y, self.velocity.x)))
        self.UpdatePosition(screen)
        self.CurrentChunk()
        self.PlaceMarker(chunks)


class MarkerState(Enum):
    NULL = 0
    TOHOME = 1
    TOFOOD = 2
    FOOD = 3

class Marker(object):
    def __init__(self, intensity=1000, state=MarkerState.NULL):
        self.state = state
        if not self.state:
            self.intensity = intensity
        else:
            self.intensity = 0
        

    def Update(self, deltaTime):
        self.intensity -= 1.0*deltaTime

    def IsDone(self):
        return self.intensity < 0


class Home:
    def __init__(self, pos, radius):
        self.position = pos
        self.radius = radius

    def Draw(self, screen):
        pygame.draw.circle(screen, [0, 0, 0], self.position, self.radius)
