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

envWidth = 14
envHeight = 9
backgroundColor = (255, 255, 255)


class Entity:
    def __init__(self, index=0, target=(0, 0), position=(0, 0)):
        self.index = index
        self.target = target
        self.position = position

    def nextStep(self, cellStateInternal):
        x = self.position[0]
        y = self.position[1]
        if y == self.target[1]:
            if x < self.target[0]:
                self.position = (self.position[0] + 1, self.position[1])
        elif x == self.target[0] - 1:
            if self.target[1] > y:
                self.position = (self.position[0], self.position[1] + 1)
            if self.target[1] < y:
                self.position = (self.position[0], self.position[1] - 1)
        elif cellStateInternal[x + 1][y] == 0 and environment[x + 1][y] != 2:
            self.position = (self.position[0] + 1, self.position[1])


environment = np.zeros((envWidth, envHeight))
cellState = np.zeros((envWidth, envHeight))
entities = []

gridSize = 0.04
timeStep = 0.3


def initEnv():
    for x in range(envWidth):
        for y in range(envHeight):
            if y != 4:
                if x % 2 == 0:
                    environment[x][y] = 1
            if x == 0 or x == envWidth - 1:
                environment[x][y] = 2
            if y == 0 or y == envHeight - 1:
                environment[x][y] = 2
    # entities.append(Entity(index=1, target=(11, 1), position=(1, 4)))
    # entitiesToCellState()


def entitiesToCellState():  # writes the index of the entity in the corresponding cell
    global cellState
    cellState = np.zeros((envWidth, envHeight))  # clear
    for entity in entities:
        cellState[entity.position[0]][entity.position[1]] = entity.index


def nextStep():  # check for only one step forward possible
    for entity in entities:
        entity.nextStep(cellState)
    entitiesToCellState()


def showSpace():
    screen.fill(backgroundColor)
    for x in range(envWidth):
        for y in range(envHeight):
            cellColor = (125, 125, 125)
            if environment[x][y] == 1:  # seat
                cellColor = (0, 0, 255)
            if environment[x][y] == 2:  # wall
                cellColor = (125, 0, 0)
            pygame.draw.rect(screen, cellColor, (
                screenWidth * 0.1 + x * screenWidth * gridSize, screenHeight * 0.1 + y * screenWidth * gridSize,
                screenWidth * gridSize * 0.95, screenWidth * gridSize * 0.95))
            if cellState[x][y] > 0:  # passanger
                cellColor = (245, 245, 220)
                pygame.draw.circle(screen, cellColor, (screenWidth * 0.1 + (x + 0.5) * screenWidth * gridSize,
                                                       screenHeight * 0.1 + (y + 0.5) * screenWidth * gridSize),
                                   screenWidth * gridSize * 0.95 * 0.5)
    pygame.display.flip()


def main():
    initEnv()
    print("init")
    running = True
    start_time = time.time()
    currentStepNumber = 0
    nextSeatX = 12
    nextSeatY = 1
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= timeStep:  # 50 steps per second
            start_time = current_time
            nextStep()
            if currentStepNumber % 3 == 0 and nextSeatY != 4:
                print(nextSeatX)
                entities.append(Entity(index=1, target=(nextSeatX, nextSeatY), position=(1, 4)))
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
