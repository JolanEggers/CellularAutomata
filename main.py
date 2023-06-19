import math
import random
import time
import numpy as np
import pygame

screenWidth = 1000
screenHeight = 600
pygame.init()
WINDOW_SIZE = (screenWidth, screenHeight)
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(None, 36)

envWidth = 7
envHeight = 4.6
envResolution = 20
timeResolution = 20.0
backgroundColor = (255, 255, 255)
lineThickness = 0.00


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.2, speed=1.0):
        self.index = index
        self.target = target
        self.position = position
        self.diameter = diameter
        self.speed = speed

    def collisionAtPoint(self, xNext, yNext, cellStateInternal, environmentInternal):
        neighbours = []  # list of all neighbours in range in format (entityIndex, dist)
        walls = (0, 0, 9999)  # nearest wall in format (x,y,dist)
        for x in range(int(xNext * envResolution - 0.55 * envResolution),
                       int(xNext * envResolution + 0.55 * envResolution)):
            for y in range(int(yNext * envResolution - 0.55 * envResolution),
                           int(yNext * envResolution + 0.55 * envResolution)):
                if cellStateInternal[x][y] != 0 and cellStateInternal[x][y]!=self.index:  # other cell found
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
        if walls[2] < self.diameter * 0.5 :  # collision with wall
            collision = True
        return collision

    def nextStep(self, cellStateInternal, environmentInternal):
        xIs = self.position[0]
        yIs = self.position[1]

        xSeat = self.target[0]  # coordinates of target Seat
        ySeat = self.target[1]

        targetVector = (0, 0)  # target direction vector

        if xSeat > xIs:
            targetVector = (self.speed / timeResolution, 0)

        xNext = xIs + targetVector[0]
        yNext = yIs + targetVector[1]

        collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal)
        if collision:
            targetVector = (0, -self.speed / timeResolution)
            xNext = xIs + targetVector[0]
            yNext = yIs + targetVector[1]
            collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal)
        if collision:
            targetVector = (0, +self.speed / timeResolution)
            xNext = xIs + targetVector[0]
            yNext = yIs + targetVector[1]
            collision = self.collisionAtPoint(xNext, yNext, cellStateInternal, environmentInternal)

        if not collision:
            self.position=(xNext,yNext)



environment = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))
cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))
entities = []

gridSize = 0.08


def initEnv():
    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):
            if int(2 * y / envResolution) != 4:
                if int(2 * x / envResolution) % 2 == 0:
                    environment[x][y] = 1
            if x < 0.5 * envResolution or x > (envWidth - 0.5) * envResolution - 1:
                environment[x][y] = 2
            if y < 0.5 * envResolution or y > (envHeight - 0.5) * envResolution - 1:
                environment[x][y] = 2
    #entities.append(Entity(index=1, target=(3.5, 0.5), position=(0.75, 2.24), diameter=0.32))
    #entitiesToCellState()


def entitiesToCellState():  # writes the index of the entity in the corresponding cell
    global cellState
    cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))  # clear
    for entity in entities:
        cellState[int(entity.position[0] * envResolution)][int(entity.position[1] * envResolution)] = entity.index


def nextStep():  # check for only one step forward possible
    for entity in entities:
        entity.nextStep(cellState, environment)
    entitiesToCellState()


def showSpace():
    screen.fill(backgroundColor)
    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):  # loops for environment
            cellColor = (125, 125, 125)
            if environment[x][y] == 1:  # seat
                cellColor = (0, 0, 255)
            if environment[x][y] == 2:  # wall
                cellColor = (125, 0, 0)
            pygame.draw.rect(screen, cellColor, (
                screenWidth * 0.1 + (x + lineThickness) * screenWidth * gridSize / envResolution,
                screenHeight * 0.1 + (y + lineThickness) * screenWidth * gridSize / envResolution,
                screenWidth * gridSize * (1.0 - lineThickness) / envResolution,
                screenWidth * gridSize * (1.0 - lineThickness) / envResolution))

    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):  # loops for entities
            if cellState[x][y] > 0:  # passanger
                cellColor = (245, 245, 220)
                diameter = entities[int(cellState[x][y]) - 1].diameter * screenWidth * gridSize  * 0.5
                xHighRes = entities[int(cellState[x][y]) - 1].position[0] * envResolution
                yHighRes = entities[int(cellState[x][y]) - 1].position[1] * envResolution
                pygame.draw.circle(screen, cellColor,
                                   (screenWidth * 0.1 + (xHighRes + 0.5) * screenWidth * gridSize / envResolution,
                                    screenHeight * 0.1 + (yHighRes + 0.5) * screenWidth * gridSize / envResolution),
                                   diameter)
    pygame.display.flip()


def main():
    initEnv()
    print("init")
    running = True
    start_time = time.time()
    currentStepNumber = 0
    nextSeatX = 12
    nextSeatY = 1
    nextIndex = 1
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 0.02 :  # 50 steps per second
            start_time = current_time
            nextStep()
            if currentStepNumber % (1 * timeResolution) == 0 and nextSeatY != 4:
                print(nextSeatX)
                entities.append(
                    Entity(index=nextIndex, target=(nextSeatX * 0.5, nextSeatY * 0.5), position=(0.75, 2.4)))
                nextIndex += 1
                nextSeatX = nextSeatX - 2
                if nextSeatX < 1:
                    nextSeatX = 12
                    if nextSeatY < 4:
                        nextSeatY = nextSeatY + 1
                        if nextSeatY == 4:
                            nextSeatY = 7
                    else:
                        nextSeatY = nextSeatY - 1

                entitiesToCellState()
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showSpace()


if __name__ == "__main__":
    main()