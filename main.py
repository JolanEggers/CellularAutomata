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
envResolution = 10
timeResolution = 4.0
backgroundColor = (255, 255, 255)
lineThickness = 0.05


class Entity:
    def __init__(self, index=0, target=(0.0, 0.0), position=(0.0, 0.0), diameter=0.3, speed=1.0):
        self.index = index
        self.target = target
        self.position = position
        self.diameter = diameter
        self.speed = speed

    def nextStep(self, cellStateInternal):
        xIs = self.position[0]
        yIs = self.position[1]
        xTarget = self.target[0]
        yTarget = self.target[1]
        collision = False
        for x in range(int(xIs*envResolution - 0.55*envResolution), int(xIs*envResolution + 0.55*envResolution)):
            for y in range(int(yIs*envResolution - 0.55*envResolution), int(yIs*envResolution + 0.55*envResolution)):
                if x != int(xIs*envResolution) or y != int(yIs*envResolution):
                    if cellStateInternal[x][y] != 0:
                        collision = True
                        print(f"collision {x} {y}")

        if not collision:
            if xIs < xTarget:
                self.position = (xIs + self.speed / timeResolution, yIs)


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
    entities.append(Entity(index=1, target=(5.5, 0.5), position=(0.75, 2.25)))
    entitiesToCellState()


def entitiesToCellState():  # writes the index of the entity in the corresponding cell
    global cellState
    cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))  # clear
    for entity in entities:
        cellState[int(entity.position[0] * envResolution)][int(entity.position[1] * envResolution)] = entity.index


def nextStep():  # check for only one step forward possible
    for entity in entities:
        entity.nextStep(cellState)
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
                screenWidth * 0.1 + x * screenWidth * gridSize / envResolution,
                screenHeight * 0.1 + y * screenWidth * gridSize / envResolution,
                screenWidth * gridSize * (1 - lineThickness) / envResolution,
                screenWidth * gridSize * (1 - lineThickness) / envResolution))

    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):  # loops for entities
            if cellState[x][y] > 0:  # passanger
                cellColor = (245, 245, 220)
                diameter = entities[int(cellState[x][y]) - 1].diameter * screenWidth * gridSize * 0.95 * 0.5
                pygame.draw.circle(screen, cellColor,
                                   (screenWidth * 0.1 + (x + 0.5) * screenWidth * gridSize / envResolution,
                                    screenHeight * 0.1 + (y + 0.5) * screenWidth * gridSize / envResolution),
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
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1 / timeResolution:  # 50 steps per second
            start_time = current_time
            if currentStepNumber%4*timeResolution==3*timeResolution:
                entities.append(Entity(index=len(entities)+1, target=(5.5, 0.5), position=(0.75, 2.25)))
                entitiesToCellState()
            nextStep()
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showSpace()


if __name__ == "__main__":
    main()
