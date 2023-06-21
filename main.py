import time
import numpy as np
import pandas as pd
import pygame
from showSpace import *
from entity import *

envWidth = 13.5
envHeight = 4.6
envResolution = 15
timeResolution = 15.0

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
            if entities[0].collisionAtPoint(nextPosition[0] - entities[0].diameter, nextPosition[1], cellState,
                                            environment, entities):
                doAdd = False
            if entities[0].collisionAtPoint(nextPosition[0] + entities[0].diameter, nextPosition[1], cellState,
                                            environment, entities):
                doAdd = False
        if doAdd:
            entities.append(
                Entity(index=nextIndex, target=nextTarget, position=nextPosition, diameter=nextDiameter,
                       speed=nextSpeed))
            entitiesToCellState()


def initEnv():
    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):
            if int(2 * y / envResolution) != 4 and x > 1 * envResolution:
                if int(2 * x / envResolution) % 2 == 0:
                    environment[x][y] = 1  # seats
            if x < 0.1 * envResolution or x > (envWidth - 0.5) * envResolution - 1:
                environment[x][y] = 2
            if y < 0.5 * envResolution or y > (envHeight - 0.5) * envResolution - 1:
                environment[x][y] = 2


def entitiesToCellState():  # writes the index of the entity in the corresponding cell
    global cellState
    cellState = np.zeros((int(envWidth * envResolution), int(envHeight * envResolution)))  # clear
    for entity in entities:
        cellState[int(entity.position[0] * envResolution)][int(entity.position[1] * envResolution)] = entity.index


def nextStep():  # check for only one step forward possible
    for entity in entities:
        entity.nextStep(cellState, environment, entities)
    entitiesToCellState()


def isOptimal(entitiesCSV):
    isOptimalReturn = True
    if len(entities)==len(entitiesCSV):
        for entity in entities:
            if entity.state != 100:  # check if every entity is seated
                isOptimalReturn = False
    else:
        isOptimalReturn = False
    return isOptimalReturn


def main():
    initEnv()
    print("init")
    running = True
    start_time = time.time()
    currentStepNumber = 0
    entitiesCSV = pd.read_csv("out.csv")
    testC = 0
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 0.0:  # 50 steps per second
            start_time = current_time
            nextStep()
            if isOptimal(entitiesCSV):
                #with open("frontToBack3GroupsResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")
                #with open("backToFront3GroupsResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")
                #with open("randomSeatingResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")
                #with open("steffenModifiedResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")
                #with open("windowMiddleAisleResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")
                #with open("steffenPerfectResult.csv", "a") as myfile:
                #    myfile.write(f",{currentStepNumber}")

                with open("backToFront3GroupsLuggage.csv", "a") as myfile:
                    myfile.write(f"{entities[0].storeLuggageTime},{currentStepNumber}\n")
                running = False
                print(currentStepNumber)
            if currentStepNumber % (timeResolution) == 0:
                if testC == 0:
                    nextEntityFromCSV(entitiesCSV)
            currentStepNumber = currentStepNumber + 1
        for event in pygame.event.get():
            if event.type == 768:
                testC = 1 - testC
            if event.type == pygame.QUIT:
                running = False
        if int(current_time*1000)%1000<10:
            showSpace(envWidth, envHeight, envResolution, environment, cellState, entities)


if __name__ == "__main__":
    main()
