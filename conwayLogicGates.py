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

envWidth = 100
envHeight = 60

cellState = np.zeros((envWidth, envHeight))
# Set the colors


gridSize = 0.01
timeStep = 0.02

aActive = False
bActive = False

showAndGate =  False
showOrGate  = True
showNotGate  = False

def GlidergunLD(x, y):  # LD:=left and down
    cellState[x + 0][y + 2] = 1  # left square
    cellState[x + 0][y + 3] = 1
    cellState[x + 1][y + 2] = 1
    cellState[x + 1][y + 3] = 1
    cellState[x + 34][y + 4] = 1  # right square
    cellState[x + 34][y + 5] = 1
    cellState[x + 35][y + 4] = 1
    cellState[x + 35][y + 5] = 1
    #
    cellState[x + 11][y + 0] = 1
    cellState[x + 11][y + 1] = 1
    cellState[x + 11][y + 5] = 1
    cellState[x + 11][y + 6] = 1
    cellState[x + 13][y + 1] = 1
    cellState[x + 13][y + 5] = 1
    cellState[x + 14][y + 2] = 1
    cellState[x + 14][y + 3] = 1
    cellState[x + 14][y + 4] = 1
    cellState[x + 15][y + 2] = 1
    cellState[x + 15][y + 3] = 1
    cellState[x + 15][y + 4] = 1
    #
    cellState[x + 18][y + 5] = 1
    cellState[x + 19][y + 4] = 1
    cellState[x + 19][y + 5] = 1
    cellState[x + 19][y + 6] = 1
    cellState[x + 20][y + 3] = 1
    cellState[x + 20][y + 7] = 1
    cellState[x + 21][y + 5] = 1
    cellState[x + 22][y + 2] = 1
    cellState[x + 22][y + 8] = 1
    cellState[x + 23][y + 2] = 1
    cellState[x + 23][y + 8] = 1
    cellState[x + 24][y + 3] = 1
    cellState[x + 24][y + 7] = 1
    cellState[x + 25][y + 4] = 1
    cellState[x + 25][y + 5] = 1
    cellState[x + 25][y + 6] = 1


def GlidergunRD(x, y):  # LD:=left and down
    cellState[x + 35 - 0][y + 2] = 1  # left square
    cellState[x + 35 - 0][y + 3] = 1
    cellState[x + 35 - 1][y + 2] = 1
    cellState[x + 35 - 1][y + 3] = 1
    cellState[x + 35 - 34][y + 4] = 1  # right square
    cellState[x + 35 - 34][y + 5] = 1
    cellState[x + 35 - 35][y + 4] = 1
    cellState[x + 35 - 35][y + 5] = 1
    #
    cellState[x + 35 - 11][y + 0] = 1
    cellState[x + 35 - 11][y + 1] = 1
    cellState[x + 35 - 11][y + 5] = 1
    cellState[x + 35 - 11][y + 6] = 1
    cellState[x + 35 - 13][y + 1] = 1
    cellState[x + 35 - 13][y + 5] = 1
    cellState[x + 35 - 14][y + 2] = 1
    cellState[x + 35 - 14][y + 3] = 1
    cellState[x + 35 - 14][y + 4] = 1
    cellState[x + 35 - 15][y + 2] = 1
    cellState[x + 35 - 15][y + 3] = 1
    cellState[x + 35 - 15][y + 4] = 1
    #
    cellState[x + 35 - 18][y + 5] = 1
    cellState[x + 35 - 19][y + 4] = 1
    cellState[x + 35 - 19][y + 5] = 1
    cellState[x + 35 - 19][y + 6] = 1
    cellState[x + 35 - 20][y + 3] = 1
    cellState[x + 35 - 20][y + 7] = 1
    cellState[x + 35 - 21][y + 5] = 1
    cellState[x + 35 - 22][y + 2] = 1
    cellState[x + 35 - 22][y + 8] = 1
    cellState[x + 35 - 23][y + 2] = 1
    cellState[x + 35 - 23][y + 8] = 1
    cellState[x + 35 - 24][y + 3] = 1
    cellState[x + 35 - 24][y + 7] = 1
    cellState[x + 35 - 25][y + 4] = 1
    cellState[x + 35 - 25][y + 5] = 1
    cellState[x + 35 - 25][y + 6] = 1


def GliderRD(x, y):
    cellState[2 + x][0 + y] = 1
    cellState[0 + x][1 + y] = 1
    cellState[2 + x][1 + y] = 1
    cellState[1 + x][2 + y] = 1
    cellState[2 + x][2 + y] = 1

def GliderLD(x, y):
    #cellState[0 + x][0 + y] = 1
    #cellState[2 + x][1 + y] = 1
    #cellState[0 + x][1 + y] = 1
    #cellState[1 + x][2 + y] = 1
    #cellState[0 + x][2 + y] = 1

    cellState[0 + x][0 + y] = 1
    cellState[2 + x][0 + y] = 1
    cellState[0 + x][1 + y] = 1
    cellState[1 + x][1 + y] = 1
    cellState[1 + x][2 + y] = 1


def GliderTerminatorRD(x, y):  # Terminates Glider, going in the R-D-Direction
    cellState[x + 2][y + 0] = 1
    cellState[x + 3][y + 0] = 1
    cellState[x + 1][y + 1] = 1
    cellState[x + 3][y + 1] = 1
    cellState[x + 1][y + 2] = 1
    cellState[x + 0][y + 3] = 1
    cellState[x + 1][y + 3] = 1


def GliderTerminatorLD(x, y):  # Terminates Glider, going in the L-D-Direction
    cellState[x + 1][y + 0] = 1
    cellState[x + 0][y + 0] = 1
    cellState[x + 2][y + 1] = 1
    cellState[x + 0][y + 1] = 1
    cellState[x + 2][y + 2] = 1
    cellState[x + 3][y + 3] = 1
    cellState[x + 2][y + 3] = 1


def Reflector1(x, y):
    cellState[x + 1][y + 1] = 1

    cellState[x + 1][y + 2] = 1
    cellState[x + 2][y + 2] = 1
    cellState[x + 3][y + 2] = 1

    cellState[x + 4][y + 3] = 1

    cellState[x + 3][y + 4] = 1
    cellState[x + 4][y + 4] = 1

    cellState[x + 3][y + 14] = 1
    cellState[x + 4][y + 14] = 1
    cellState[x + 8][y + 14] = 1
    cellState[x + 9][y + 14] = 1

    cellState[x + 5][y + 15] = 1
    cellState[x + 6][y + 15] = 1
    cellState[x + 7][y + 15] = 1

    cellState[x + 4][y + 16] = 1
    cellState[x + 8][y + 16] = 1

    cellState[x + 5][y + 17] = 1
    cellState[x + 7][y + 17] = 1

    cellState[x + 6][y + 18] = 1

    cellState[x + 5][y + 22] = 1
    cellState[x + 6][y + 22] = 1
    cellState[x + 5][y + 23] = 1
    cellState[x + 6][y + 23] = 1


isInit = True


def initEnv():
    global isInit
    if showNotGate:
        # Not-Gate
        if isInit:
            isInit = False
            GlidergunLD(15, 2)

            Reflector1(4, 22)

        if aActive:
            GliderRD(4, 5)

    if showOrGate:
        # OR Gate
        if isInit:
            isInit = False
            GlidergunLD(50, 4)
            GlidergunRD(0, 20)

        if aActive:
            GliderRD(40, 4)

        if bActive:
            GliderRD(40, 12)

        GliderTerminatorLD(59, 30)

    if showAndGate:
        #AND Gate
        if isInit:
            isInit = False
            GlidergunLD(18+8, 4)


        if aActive:
            GliderRD(2,12)

        if bActive:
            GliderRD(2 ,4)

        GliderTerminatorRD(10,38)

    '''
    # x = 11 + 8 * 2
    # y = 10
    # cellState[-3 + x][1 + y] = 1
    # cellState[-1 + x][2 + y] = 1
    # cellState[-3 + x][2 + y] = 1
    # cellState[-2 + x][3 + y] = 1
    # cellState[-3 + x][3 + y] = 1

    # x = 32 -8*1
    # y = 31 - 8*2
    # cellState[x + 3 - 2][y + 0] = 1
    # cellState[x + 3 - 3][y + 0] = 1
    # cellState[x + 3 - 1][y + 1] = 1
    # cellState[x + 3 - 3][y + 1] = 1
    # cellState[x + 3 - 1][y + 2] = 1
    # cellState[x + 3 - 0][y + 3] = 1
    # cellState[x + 3 - 1][y + 3] = 1
    '''

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
                screenWidth * 0.0 + x * screenWidth * gridSize, screenHeight * 0.0 + y * screenWidth * gridSize,
                screenWidth * gridSize * 0.95, screenWidth * gridSize * 0.95))
    pygame.display.flip()


def main():
    global aActive, bActive
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
            #pygame.image.save(screen, f"./imgCapture/screenshot{100000+currentStepNumber}.png")
            if currentStepNumber % 30 == 29:
                initEnv()
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == 768:
                if event.key == 97:
                    aActive = not aActive
                if event.key == 98:
                    bActive = not bActive
            if event.type == pygame.QUIT:
                running = False
        showSpace()


if __name__ == "__main__":
    main()