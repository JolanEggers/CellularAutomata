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

envWidth = 12
envHeight = 7
backgroundColor = (25, 25, 25)

environment = np.zeros((envHeight, envWidth))
entity = np.zeros((envHeight, envWidth))
# Set the colors


gridSize = 0.04
timeStep = 1


def initEnv():
    for x in range(envWidth):
        for y in range(envHeight):
            if (y != 3):
                if (x % 2 == 1):
                    environment[y][x] = 1


initEnv()


def nextStep():  # check for only one step forward possible
    global entity
    stepTaken=False
    entityCache = entity.copy()
    for x in range(envWidth - 1):
        for y in range(envHeight):
            if (x > 5):
                if (y > 0):
                    if environment[y - 1][x] == 1 and entity[y][x] == 1 and stepTaken==False:#top seat free
                        entityCache[y-1][x] = 1
                        entityCache[y][x] = 0
                        stepTaken=True
            if y == 3 and entity[y][x] == 1 and stepTaken==False:  # in the middle, move forward
                entityCache[y][x + 1] = 1
                entityCache[y][x] = 0
                stepTaken=True

    entity = entityCache.copy()


def showSpace():
    screen.fill(backgroundColor)
    for x in range(envWidth):
        for y in range(envHeight):
            cellColor = (0, 0, 0)
            if environment[y][x] == 1:  # seat
                cellColor = (0, 0, 255)
            if entity[y][x] == 1:  # entity
                cellColor = (245, 245, 220)
            pygame.draw.rect(screen, cellColor, (
                screenWidth * 0.1 + x * screenWidth * gridSize, screenHeight * 0.1 + y * screenWidth * gridSize,
                screenWidth * gridSize * 0.95, screenWidth * gridSize * 0.95))
    pygame.display.flip()


start_time = time.time()
running = True
currentStepNumber= 0
while running:  # main loop
    # pygame events
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= timeStep:  # 50 steps per second
        start_time = current_time
        nextStep()
        if currentStepNumber%5==0:
            entity[3][0] = 1
        currentStepNumber=currentStepNumber+1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    showSpace()
