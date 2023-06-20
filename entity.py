import math

import numpy as np

from main import envResolution, timeResolution, envWidth, envHeight


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.2, speed=1.0, seated=False,
                 changeSeatFor=-1, awaitingSeatChangeFor=None, awaitedSeatChangeFor=None, pleaseMoveX=0, wait=-1,
                 luggageStored=False, state=0):
        if awaitingSeatChangeFor is None:
            awaitingSeatChangeFor = []
        if awaitedSeatChangeFor is None:
            awaitedSeatChangeFor = []
        self.index = index
        self.target = target
        self.position = position
        self.diameter = diameter
        self.speed = speed
        self.seated = seated
        self.changeSeatFor = changeSeatFor
        self.awaitingSeatChangeFor = awaitingSeatChangeFor
        self.awaitedSeatChangeFor = awaitedSeatChangeFor
        self.pleaseMoveX = pleaseMoveX
        self.wait = wait
        self.luggageStored = luggageStored
        self.state = state

    def collisionAtPoint(self, xNext, yNext, cellStateInternal, environmentInternal, entities, giveBackEntity=False):
        neighbours = []  # list of all neighbours in range in format (entityIndex, dist)
        walls = (0, 0, 9999)  # nearest wall in format (x,y,dist)
        for x in range(int(xNext * envResolution - 0.55 * envResolution),
                       int(xNext * envResolution + 0.55 * envResolution)):
            for y in range(int(yNext * envResolution - 0.55 * envResolution),
                           int(yNext * envResolution + 0.55 * envResolution)):
                if cellStateInternal[x][y] != 0 and cellStateInternal[x][y] != self.index:  # other cell found
                    # collision = True
                    nX = entities[int(cellStateInternal[x][y]) - 1].position[0]  # neighbour X
                    nY = entities[int(cellStateInternal[x][y]) - 1].position[1]  # neighbour Y
                    dist = math.sqrt((nX - xNext) * (nX - xNext) + (nY - yNext) * (nY - yNext))
                    neighbours.append((int(cellStateInternal[x][y]) - 1, dist))
                if environmentInternal[x][y] != 0:  # non-empty space
                    eX = x / envResolution
                    eY = y / envResolution
                    dist = math.sqrt((eX - xNext) * (eX - xNext) + (eY - yNext) * (eY - yNext))
                    if dist < walls[2]:
                        walls = (eX, eY, dist)
        # return neighbours, walls
        collision = False
        whichNeighbour = []
        for neighbour in neighbours:
            if neighbour[1] < (entities[neighbour[0]].diameter + self.diameter) / 2:  # collision with passanger
                collision = True
            if neighbour[1] < (entities[neighbour[0]].diameter + self.diameter) * 0.5:
                whichNeighbour.append(neighbour[0])
        if walls[2] < self.diameter * 0.5:  # collision with wall
            collision = True
        if giveBackEntity:
            return whichNeighbour
        return collision

    def isEntityInWay(self, xIs, yIs, xSeat, ySeat, cellStateInternal, environmentInternal, entities):
        EntityInWay = []
        for i in range(6):  # try in 5 steps, if there is someone in the way
            EntityInWay.extend(self.collisionAtPoint(xIs * (i / 5.0) + xSeat * (1 - i / 5.0),
                                                     yIs * (i / 5.0) + ySeat * (1 - i / 5.0),
                                                     cellStateInternal, environmentInternal, entities,
                                                     giveBackEntity=True))
        return list(dict.fromkeys(EntityInWay))  # filter out duplicates

    def nextStep(self, cellStateInternal, environmentInternal, entities):
        if self.state == 0:
            if self.pleaseMoveX != 0:  # asked to move back
                self.moveBack(cellStateInternal, environmentInternal, entities)
            else:
                self.moveToX(cellStateInternal, environmentInternal, entities)

        if self.state == 1:
            self.storeLuggage()

        if self.state == 2:
            if self.moveIfInWay(cellStateInternal, environmentInternal, entities):
                self.state = 4
            else:
                self.state = 3

        if self.state == 3:
            self.takeSeat(cellStateInternal, environmentInternal, entities)
            if self.changeSeatFor >= 0:  # stand up to change seat
                self.state = 10

        if self.state == 100:  # seat taken
            self.tellOthersToStopWaiting(entities)
            if self.changeSeatFor >= 0:  # stand up to change seat
                self.state = 10

        if self.state == 4:
            self.makeWay(cellStateInternal, environmentInternal, entities)
        if self.state == 5:
            self.tellOthersToChangeSeats(cellStateInternal, environmentInternal, entities)
        if self.state == 6:
            self.waitForOthersToGetOutOfWay()
        if self.state == 7:
            self.moveToX2(cellStateInternal, environmentInternal, entities)

        if self.state == 10:
            self.backToAisle(cellStateInternal, environmentInternal, entities)

        if self.state == 11:
            self.moveForwardToChangeSeat(cellStateInternal, environmentInternal, entities)
        if self.state == 12:
            self.retakeSeat(cellStateInternal, environmentInternal, entities)

    def retakeSeat(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[0] - 0.2 - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            if not collision:
                self.position = targetVector
        else:  # next step
            self.state = 1

    def tellOthersToStopWaiting(self, entities):
        if len(self.awaitedSeatChangeFor) > 0:
            for peopleWhichMoved in self.awaitedSeatChangeFor:
                entities[int(peopleWhichMoved)].changeSeatFor = -1
            # print(f"{self.index} {self.awaitedSeatChangeFor}")
            self.awaitedSeatChangeFor = []

    def waitForOthersToGetOutOfWay(self):
        if len(self.awaitingSeatChangeFor) <= 0:
            self.state = 7

    def moveForwardToChangeSeat(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[0] + 0.6 - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            if not collision:
                self.position = targetVector
        if abs(self.target[0] + 0.3 - self.position[0]) < 0.1:  # it's fine, if its only 0.3 m
            entities[int(self.changeSeatFor)].awaitingSeatChangeFor = \
                np.setdiff1d(entities[int(self.changeSeatFor)].awaitingSeatChangeFor, [self.index - 1])
            # remove self from waiting list, since self is out of the way
        if self.changeSeatFor < 0:
            self.state = 12

    def backToAisle(self, cellStateInternal, environmentInternal, entities):
        error = (2.25 - self.position[1]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0], self.position[1] + error * self.speed / timeResolution)
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            if not collision:
                self.position = targetVector
        else:
            self.state = 11

    def tellOthersToChangeSeats(self, cellStateInternal, environmentInternal, entities):
        if len(self.awaitingSeatChangeFor) > 0:
            for needToMove in self.awaitingSeatChangeFor:
                entities[needToMove].changeSeatFor = self.index - 1
        self.state = 6

    def makeWay(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[0] - 0.7 - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            entityInWay = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal,
                                                environmentInternal,
                                                entities, giveBackEntity=True)
            for entity in entityInWay:  # ask other person to step back
                entities[entity].pleaseMoveX = self.position[0] - self.diameter * 2
            if not collision:
                self.position = targetVector
        else:  # next step
            self.state = 5

    def moveBack(self, cellStateInternal, environmentInternal, entities):
        error = (self.pleaseMoveX - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            entityInWay = self.collisionAtPoint(targetVector[0] - self.diameter, targetVector[1], cellStateInternal,
                                                environmentInternal,
                                                entities, giveBackEntity=True)
            for entity in entityInWay:  # ask other person to step back
                entities[entity].pleaseMoveX = self.position[0] - self.diameter * 2
            if not collision:
                self.position = targetVector
            if collision and len(entityInWay) == 0:  # standing against wall
                self.pleaseMoveX = 0
        else:
            self.pleaseMoveX = 0  # continue forward

    def moveToX(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[0] - 0.2 - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            entityInWay = self.collisionAtPoint(targetVector[0] + self.diameter, targetVector[1], cellStateInternal,
                                                environmentInternal,
                                                entities, giveBackEntity=True)
            entityInWay.extend(
                self.collisionAtPoint(targetVector[0] + self.diameter * 2, targetVector[1], cellStateInternal,
                                      environmentInternal,
                                      entities, giveBackEntity=True))
            entityInWay.extend(
                self.collisionAtPoint(targetVector[0] + self.diameter * 3, targetVector[1], cellStateInternal,
                                      environmentInternal,
                                      entities, giveBackEntity=True))
            entityInWay = list(dict.fromkeys(entityInWay))
            collision2 = False
            for entity in entityInWay:
                if entities[entity].state != 0:
                    collision2 = True

            if not collision and not collision2:  # leave enough space
                self.position = targetVector
        else:  # next step
            self.state = 1

    def moveToX2(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[0] - 0.2 - self.position[0]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0] + error * self.speed / timeResolution, self.position[1])
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            if not collision:
                self.position = targetVector
        else:  # next step
            self.state = 1

    def storeLuggage(self):
        if not self.luggageStored:
            if self.wait == -1:
                self.wait = 1
            self.wait -= 1 / timeResolution
            if self.wait <= 0:
                self.luggageStored = True
                self.state = 2
        else:
            self.state = 2

    def takeSeat(self, cellStateInternal, environmentInternal, entities):
        error = (self.target[1] - self.position[1]) * 10  # target
        if abs(error) > 0.1:
            if abs(error) > 1:
                error /= abs(error)
            targetVector = (self.position[0], self.position[1] + error * self.speed / timeResolution)
            collision = self.collisionAtPoint(targetVector[0], targetVector[1], cellStateInternal, environmentInternal,
                                              entities)
            if not collision:
                self.position = targetVector
        else:
            self.state = 100

    def moveIfInWay(self, cellStateInternal, environmentInternal, entities):
        EntityInWay = []
        for i in range(6):  # try in 5 steps, if there is someone in the way
            EntityInWay.extend(self.collisionAtPoint(self.position[0] * (i / 5.0) + self.target[0] * (1 - i / 5.0),
                                                     self.position[1] * (i / 5.0) + self.target[1] * (1 - i / 5.0),
                                                     cellStateInternal, environmentInternal, entities,
                                                     giveBackEntity=True))
        EntityInWay2 = []
        for entity in list(dict.fromkeys(EntityInWay)):  # filter out duplicates
            if entities[entity].state == 100:  # only ask them to change if they are sitting (otherwise turn around...)
                EntityInWay2.append(entity)
        self.awaitingSeatChangeFor = EntityInWay2
        if len(self.awaitingSeatChangeFor) > 0:
            self.awaitedSeatChangeFor.extend(self.awaitingSeatChangeFor)
        if len(self.awaitingSeatChangeFor) > 0:
            return True
        else:
            return False
