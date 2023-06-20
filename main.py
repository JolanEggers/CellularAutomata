import time
import numpy as np
import pandas as pd
import pygame
from showSpace import *
from entity import *

envWidth = 7
envHeight = 4.6
envResolution = 20
timeResolution = 20.0

environment = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))
cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))
entities = []


def nextEntityFromCSV(entitiesCSV):
    currentLen = len(entities)
    if currentLen < len(entitiesCSV):
        nextIndex = entitiesCSV.iloc[currentLen]["index"]
        nextTarget = (entitiesCSV.iloc[currentLen]["targetX"], entitiesCSV.iloc[currentLen]["targetY"])
        nextPosition = (entitiesCSV.iloc[currentLen]["positionX"], entitiesCSV.iloc[currentLen]["positionY"])
        nextDiameter = entitiesCSV.iloc[currentLen]["diameter"]
        nextSpeed = entitiesCSV.iloc[currentLen]["speed"]

        doAdd = True  # only add next entity, if there is nothing in the way
        if currentLen > 0:
            if entities[0].collisionAtPoint(nextPosition[0], nextPosition[1], cellState, environment, entities):
                doAdd = False
        if doAdd:
            entities.append(
                Entity(index=nextIndex, target=nextTarget, position=nextPosition, diameter=nextDiameter,
                       speed=nextSpeed))
            entitiesToCellState()


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
    # entities.append(Entity(index=1, target=(3.5, 0.5), position=(0.75, 2.24), diameter=0.32))
    # entitiesToCellState()


def entitiesToCellState():  # writes the index of the entity in the corresponding cell
    global cellState
    cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))  # clear
    for entity in entities:
        cellState[int(entity.position[0] * envResolution)][int(entity.position[1] * envResolution)] = entity.index


def nextStep():  # check for only one step forward possible
    for entity in entities:
        entity.nextStep(cellState, environment, entities)
    entitiesToCellState()


def main():
    initEnv()
    print("init")
    running = True
    start_time = time.time()
    currentStepNumber = 0
    entitiesCSV = pd.read_csv("testBoarding.csv")
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 0.02:  # 50 steps per second
            start_time = current_time
            nextStep()
            if currentStepNumber % (1 * timeResolution) == 0:
                nextEntityFromCSV(entitiesCSV)
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showSpace(envWidth, envHeight, envResolution, environment, cellState, entities)


if __name__ == "__main__":
    main()
