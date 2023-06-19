import math
from main import envResolution, timeResolution


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.2, speed=1.0):
        self.index = index
        self.target = target
        self.position = position
        self.diameter = diameter
        self.speed = speed

    def collisionAtPoint(self, xNext, yNext, cellStateInternal, environmentInternal, entities):
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
        for neighbour in neighbours:
            if neighbour[1] < (entities[neighbour[0]].diameter + self.diameter) / 2:  # collision with passanger
                collision = True
        if walls[2] < self.diameter * 0.5:  # collision with wall
            collision = True
        return collision

    def nextStep(self, cellStateInternal, environmentInternal, entities):
        xIs = self.position[0]
        yIs = self.position[1]

        xSeat = self.target[0]  # coordinates of target Seat
        ySeat = self.target[1]

        targetVector = (0, 0)  # target direction vector

        if xSeat - 0.5 > xIs:
            targetVector = (self.speed / timeResolution, 0)
        else:
            if ySeat > xIs:
                targetVector = (0, +self.speed / timeResolution)
            if ySeat < xIs:
                targetVector = (0, -self.speed / timeResolution)

        xNext = xIs + targetVector[0]
        yNext = yIs + targetVector[1]

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
