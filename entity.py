import math
from main import envResolution, timeResolution, envWidth, envHeight


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.2, speed=1.0, seated=False,
                 changeSeat=False, awaitingSeatChange=False):
        self.index = index
        self.target = target
        self.position = position
        self.diameter = diameter
        self.speed = speed
        self.seated = seated
        self.changeSeat = changeSeat
        self.awaitingSeatChange = awaitingSeatChange

    def collisionAtPoint(self, xNext, yNext, cellStateInternal, environmentInternal, entities, giveBackEntity=False):
        #TODO collision not working right anymore, after introducting giveBackEntity
        #TODO give Signal to other entity to make way
        neighbours = []  # list of all neighbours in range in format (entityIndex, dist)
        walls = (0, 0, 9999)  # nearest wall in format (x,y,dist)
        for x in range(int(xNext * envResolution - 0.55 * envResolution),
                       int(xNext * envResolution + 0.55 * envResolution)):
            for y in range(int(yNext * envResolution - 4 * envResolution),
                           int(yNext * envResolution + 4 * envResolution)):
                if 0 <= x < envWidth * envResolution and 0 <= y < envHeight * envResolution:
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
        collisionWithEntity = 0
        for neighbour in neighbours:
            if neighbour[1] < (entities[neighbour[0]].diameter + self.diameter) / 2:  # collision with passanger
                collision = True
                collisionWithEntity = neighbour[0]
        if walls[2] < self.diameter * 0.5:  # collision with wall
            collision = True
        if giveBackEntity:
            return collisionWithEntity
        return collision

    def isEntityInWay(self, xIs, yIs, xSeat, ySeat, cellStateInternal, environmentInternal, entities):
        EntityInWay = False
        for i in range(3):  # try in 5 steps, if there is someone in the way
            EntityInWay = self.collisionAtPoint(xIs * (i / 3.0) + xSeat * (1 - i / 3.0),
                                                yIs * (i / 3.0) + ySeat * (1 - i / 3.0),
                                                cellStateInternal, environmentInternal, entities, giveBackEntity=True)
            if EntityInWay > 0:
                EntityInWay = True

        return EntityInWay

    def nextStep(self, cellStateInternal, environmentInternal, entities):
        xIs = self.position[0]
        yIs = self.position[1]

        xNext = xIs
        yNext = yIs
        xSeat = self.target[0]  # coordinates of target Seat
        ySeat = self.target[1]

        targetVector = (0, 0)  # target direction vector

        if not self.awaitingSeatChange:
            if xSeat - 0.25 > xIs:
                targetVector = (self.speed / timeResolution, 0)
            else:
                if self.isEntityInWay(xIs, yIs, xSeat, ySeat, cellStateInternal, environmentInternal, entities):
                    self.awaitingSeatChange = True
                error = (ySeat - yIs) * 10  # slow down near target
                if abs(error) > 0.1:
                    if abs(error) > 1:
                        error /= abs(error)
                    targetVector = (0, error * self.speed / timeResolution)
                else:
                    self.position = (xSeat, ySeat)  # when near enough "teleport" to seat
                    self.seated = True

            if not self.seated:
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]
        else:
            if xSeat - 0.5 < xIs:
                targetVector = (-self.speed / timeResolution, 0)
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]

        if xNext != xIs or yNext != yIs:
            collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities)
            if collision:
                targetVector = (0, -self.speed / timeResolution)
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]
                collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities)
            if collision:
                targetVector = (0, +self.speed / timeResolution)
                xNext = xIs + targetVector[0]
                yNext = yIs + targetVector[1]
                collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal, entities)

            if not collision:
                self.position = (xNext, yNext)
