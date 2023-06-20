import math
from main import envResolution, timeResolution, envWidth, envHeight


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.2, speed=1.0, seated=False,
                 changeSeatFor=-1, awaitingSeatChangeFor=[], awaitedSeatChangeFor=[], pleaseMoveX=0, wait=0):
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
        xIs = self.position[0]
        yIs = self.position[1]

        xNext = xIs
        yNext = yIs
        xSeat = self.target[0]  # coordinates of target Seat
        ySeat = self.target[1]

        targetVector = (0, 0)  # target direction vector

        if self.pleaseMoveX > 0 and self.changeSeatFor < 0:  # self should move back, if not in SeatChange Process
            self.wait -= timeResolution
            if self.wait <= 0:
                self.pleaseMoveX = 0
            error = (self.pleaseMoveX - xIs) * 10  # target
            if abs(error) > 0.1:  # move down
                if abs(error) > 1:
                    error /= abs(error)
                targetVector = (error * self.speed / timeResolution, 0)
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]

            entitiesInWay = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities,
                                                  giveBackEntity=True)  # backpropagate backing up
            for entityInWay in entitiesInWay:
                entities[int(entityInWay)].pleaseMoveX = xIs - 0.2
                entities[int(entityInWay)].wait = 1

        elif self.changeSeatFor >= 0:
            if self.seated:  # stand up
                self.seated = False
                self.position = (xSeat - 0.15, ySeat)
            error = (2.25 - yIs) * 10  # target
            if abs(error) > 0.1:  # move down
                if abs(error) > 1:
                    error /= abs(error)
                targetVector = (0, error * self.speed / timeResolution)
            else:  # move right
                error = ((xSeat + 0.4) - xIs) * 10
                if abs(error) > 0.1:
                    if abs(error) > 1:
                        error /= abs(error)
                    targetVector = (error * self.speed / timeResolution, 0)
                else:  # tell other entity, seat is free
                    entities[int(self.changeSeatFor)].awaitingSeatChangeFor = []

            xNext = xIs + targetVector[0]
            yNext = yIs + targetVector[1]
            if abs(yNext - yIs) > 0.01:
                entitiesInWay = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities,
                                                      giveBackEntity=True)
                for entityInWay in entitiesInWay:
                    entities[int(entityInWay)].pleaseMoveX = xIs - 0.2
                    entities[int(entityInWay)].wait = 1

        elif len(self.awaitingSeatChangeFor) <= 0:  # not awaiting Seat Change
            error = ((xSeat - 0.25) - xIs) * 10  # slow down near target
            if abs(error) > 0.1:
                if abs(error) > 1:
                    error /= abs(error)
                targetVector = (error * self.speed / timeResolution, 0)
                if targetVector[0] < 0:
                    collision = self.collisionAtPoint(xIs - 0.5, yIs, cellStateInternal, environmentInternal, entities,
                                                      giveBackEntity=True)
                    if len(collision) > 0:
                        entities[collision[0]].pleaseMoveX = xIs - 0.5
                        entities[collision[0]].wait = 1


            else:
                self.awaitingSeatChangeFor = self.isEntityInWay(xIs, yIs, xSeat, ySeat, cellStateInternal,
                                                                environmentInternal, entities)
                if len(self.awaitingSeatChangeFor) > 0:
                    self.awaitedSeatChangeFor = self.awaitingSeatChangeFor
                    for seatChangers in self.awaitingSeatChangeFor:
                        entities[seatChangers].changeSeatFor = self.index - 1
                error = (ySeat - yIs) * 10  # slow down near target
                if abs(error) > 0.1:
                    if abs(error) > 1:
                        error /= abs(error)
                    targetVector = (0, error * self.speed / timeResolution)
                else:
                    if len(self.awaitedSeatChangeFor) > 0:  # other entity can move back into seat
                        for seatChangers in self.awaitedSeatChangeFor:
                            entities[int(seatChangers)].changeSeatFor = -1
                        self.awaitedSeatChangeFor = []
                    self.position = (xSeat, ySeat)  # when near enough "teleport" to seat
                    self.seated = True

            if not self.seated:
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]

        else:  # waiting for someone to get out of seat
            if xSeat - 0.5 < xIs:
                targetVector = (-self.speed / timeResolution, 0)
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]

        if xNext != xIs or yNext != yIs:
            collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities)

            if not collision:
                self.position = (xNext, yNext)
