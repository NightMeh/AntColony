from logging.config import valid_ident
from turtle import position
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
        self.maxSpeed = 7
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
        self.count = 0
        self.foodMode = True  # True for find food, false for find home
        self.home = home
        self.current_chunk = (0, 0)
        self.current_cell = (0, 0)
        self.angle = 0
        self.markerDetectionRange = 25

    def CurrentChunk(self):
        chunkx = (self.position[0] // CHUNKSIZE)
        chunky = (self.position[1] // CHUNKSIZE)
        chunkx = max(0, min(chunkx, (SCREENWIDTH//CHUNKSIZE)-1))
        chunky = max(0, min(chunky, (SCREENHEIGHT//CHUNKSIZE)-1))

        cellx = (self.position[0] - chunkx*CHUNKSIZE)//CELLSIZE
        celly = (self.position[1] - chunky*CHUNKSIZE)//CELLSIZE
        self.current_chunk = (int(chunkx), int(chunky))
        self.current_cell = (int(cellx), int(celly))
    
    def HasItemWithPosition(self,mainList,componant):
        for item in mainList:
            if item.position == componant.position:
                return True
        return False

    def ChunksToCheck(self):
        returnlist = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                chunkchecking = (self.current_chunk[0]+x, self.current_chunk[1]+y)
                if 0 <= chunkchecking[0] <= (SCREENWIDTH//CHUNKSIZE)-1 and 0 <= chunkchecking[1] <= (SCREENHEIGHT//CHUNKSIZE)-1:
                    returnlist.append(chunkchecking)
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
                    print(self.targetFood[1].state)
                    self.targetFoodList = []
                    self.foodMode = False
                except:
                    self.targetFood = None
                    self.targetFoodList = []

    def HandlePheramoneDirection(self, chunks):
        chunksToCheck = self.ChunksToCheck()
        savelist = []
        for chunk in chunksToCheck:
            total_intensity = 0
            for marker in chunks[chunk]:
                if marker.state != MarkerState.NULL:
                    if self.foodMode and marker.state == MarkerState.TOFOOD:
                        markerpos = pygame.math.Vector2(marker.position[0],marker.position[1])
                        tomarker = pygame.math.Vector2(markerpos - self.position)
                        length = pygame.math.Vector2.length(tomarker)
                        m_vecx = math.cos(self.angle)
                        m_vecy = math.sin(self.angle)
                        m_vec = pygame.math.Vector2(m_vecx,m_vecy)
                        point = pygame.math.Vector2(0,0)

                        if length < self.markerDetectionRange:
                            if pygame.math.Vector2.dot(tomarker,m_vec)>0:
                                total_intensity += marker.intensity
                                point += marker.intensity * markerpos
                        tempsave = (total_intensity,point)
                        savelist.append(tempsave)

                    elif not self.foodMode and marker.state == MarkerState.TOHOME:
                        markerpos = pygame.math.Vector2(marker.position[0],marker.position[1])
                        tomarker = pygame.math.Vector2(markerpos - self.position)
                        length = pygame.math.Vector2.length(tomarker)
                        m_vecx = math.cos(self.angle)
                        m_vecy = math.sin(self.angle)
                        m_vec = pygame.math.Vector2(m_vecx,m_vecy)
                        point = pygame.math.Vector2(0,0)

                        if length < self.markerDetectionRange:
                            if pygame.math.Vector2.dot(tomarker,m_vec)>0:
                                total_intensity += marker.intensity
                                point += marker.intensity * markerpos

                        tempsave = (total_intensity,point)
                        savelist.append(tempsave)
        if len(savelist) != 0:
            total_intensitypos = 0

            for x in range(len(savelist)):
                if savelist[x][0] > savelist[total_intensitypos][0]:
                    total_intensitypos = x
            total_intensity = savelist[total_intensitypos][0]
            point = savelist[total_intensitypos][1]

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

    def PlaceMarker(self,chunks,renderqueue):
        index = self.current_cell[0] + self.current_cell[1] * 8
        try:
            if self.foodMode:
                chunks[self.current_chunk][index].state = MarkerState.TOHOME
            else:
                chunks[self.current_chunk][index].state = MarkerState.TOFOOD
            if not self.HasItemWithPosition((renderqueue[self.current_chunk]),(chunks[self.current_chunk][index])):
                renderqueue[self.current_chunk].append(chunks[self.current_chunk][index])
        except:
            pass

    def Update(self, screen, deltaTime, chunks,renderqueue):
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
        self.PlaceMarker(chunks,renderqueue)


class MarkerState(Enum):
    NULL = 0
    TOHOME = 1
    TOFOOD = 2
    FOOD = 3

class Marker(object):
    def __init__(self, position,currentchunk, intensity=100, state=MarkerState.NULL):
        self.state = state
        self.position = position
        self.chunk = currentchunk
        self.defaultintensity = intensity
        self.intensity = intensity
        
        

    def Update(self, deltaTime,renderqueue,chunks):
        self.intensity -= 1.0*deltaTime
        if self.intensity <= 0:
            self.state = MarkerState.NULL
            self.intensity = self.defaultintensity

            renderqueue[self.chunk].remove(self)

    def IsDone(self):
        return self.intensity < 0


class Home:
    def __init__(self, pos, radius):
        self.position = pos
        self.radius = radius

    def Draw(self, screen):
        pygame.draw.circle(screen, [0, 0, 0], self.position, self.radius)
