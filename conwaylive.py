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

envWidth = 20
envHeight = 40

cellState = np.zeros((envWidth, envHeight))
# Set the colors


gridSize = 0.04
timeStep = 1


def initEnv():
    cellState[3][1] = 1
    cellState[1][2] = 1
    cellState[3][2] = 1
    cellState[2][3] = 1
    cellState[3][3] = 1


def nextStep():  # check for only one step forward possible
    global cellState
    cellStateCache = cellState.copy()
    for x in range(1, envWidth - 1):
        for y in range(1, envHeight - 1):
            neighbourAliveCount = cellState[x - 1][y + 1] + cellState[x][y + 1] + cellState[x + 1][y + 1] + \
                                  cellState[x - 1][y] + cellState[x + 1][y] + cellState[x - 1][y - 1] + cellState[x][
                                      y - 1] + cellState[x + 1][y - 1]
            if neighbourAliveCount == 3:  # new cell gets born
                cellStateCache[x][y] = 1
            if neighbourAliveCount < 2 or neighbourAliveCount > 3:  # cells dies
                cellStateCache[x][y] = 0
    cellState = cellStateCache.copy()


def showSpace():
    aliveColor = (0, 0, 0)
    deadColor = (255, 255, 255)
    backgroundColor = (125, 125, 125)
    screen.fill(backgroundColor)
    for x in range(envWidth):
        for y in range(envHeight):
            cellColor = deadColor
            if cellState[x][y] == 1:  # entity
                cellColor = aliveColor
            pygame.draw.rect(screen, cellColor, (
                screenWidth * 0.1 + x * screenWidth * gridSize, screenHeight * 0.1 + y * screenWidth * gridSize,
                screenWidth * gridSize * 0.95, screenWidth * gridSize * 0.95))
    pygame.display.flip()


def main():
    initEnv()
    print("init")
    running = True
    start_time = time.time()
    currentStepNumber = 0
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= timeStep:  # 50 steps per second
            start_time = current_time
            nextStep()
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showSpace()


if __name__ == "__main__":
    main()
