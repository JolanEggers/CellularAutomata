import random

import numpy as np
import pandas as pd


def randomSeating():
    availableSeats = []
    for x in range(11):
        for y in range(7):
            if y != 3:
                availableSeats.append((x + 1.9, y * 0.5 + 0.75))
    fillPercentage = 1  # how many of the seats should be filled (0-1)
    entityNumbers = np.zeros(len(availableSeats))
    for i in range(len(entityNumbers)):
        entityNumbers[i] = i

    entityNumbers = random.sample(entityNumbers.tolist(),
                                  int(len(entityNumbers) * fillPercentage))  # shuffel passengers
    return entityNumbers, availableSeats


def steffenPerfect():
    availableSeats = []
    for x in range(11):
        y = 0
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 6
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 0
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 6
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))

    for x in range(11):
        y = 1
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 5
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 1
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 5
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))

    for x in range(11):
        y = 2
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 4
        if x % 2 == 0:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 2
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    for x in range(11):
        y = 4
        if x % 2 == 1:
            availableSeats.append(((10-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers = np.zeros(len(availableSeats))
    for i in range(len(entityNumbers)):
        entityNumbers[i] = i
    return entityNumbers, availableSeats

def backToFront3Groups():
    availableSeats1 = []
    for x in range(4):
        for y in range(7):
            if y != 3:
                availableSeats1.append(((10-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers1 = np.zeros(len(availableSeats1))
    for i in range(len(entityNumbers1)):
        entityNumbers1[i] = i
    entityNumbers1 = random.sample(entityNumbers1.tolist(),
                                   int(len(entityNumbers1)))  # shuffel passengers

    availableSeats2 = []
    for x in range(4):
        for y in range(7):
            if y != 3:
                availableSeats2.append(((6-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers2 = np.zeros(len(availableSeats2))
    for i in range(len(entityNumbers2)):
        entityNumbers2[i] = i + len(entityNumbers1)
    entityNumbers2 = random.sample(entityNumbers2.tolist(),
                                   int(len(entityNumbers2)))  # shuffel passengers

    availableSeats3 = []
    for x in range(3):
        for y in range(7):
            if y != 3:
                availableSeats3.append(((2-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers3 = np.zeros(len(availableSeats3))
    for i in range(len(entityNumbers3)):
        entityNumbers3[i] = i + len(entityNumbers1) + len(entityNumbers2)
    entityNumbers3 = random.sample(entityNumbers3.tolist(),
                                   int(len(entityNumbers3)))  # shuffel passengers


    entityNumbers1=np.concatenate((entityNumbers1,entityNumbers2,entityNumbers3), axis=0)
    availableSeats1=np.concatenate((availableSeats1,availableSeats2,availableSeats3), axis=0)
    return entityNumbers1, availableSeats1

def frontToBack3Groups():
    availableSeats1 = []
    for x in range(4):
        for y in range(7):
            if y != 3:
                availableSeats1.append(((3-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers1 = np.zeros(len(availableSeats1))
    for i in range(len(entityNumbers1)):
        entityNumbers1[i] = i
    entityNumbers1 = random.sample(entityNumbers1.tolist(),
                                   int(len(entityNumbers1)))  # shuffel passengers

    availableSeats2 = []
    for x in range(4):
        for y in range(7):
            if y != 3:
                availableSeats2.append(((7-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers2 = np.zeros(len(availableSeats2))
    for i in range(len(entityNumbers2)):
        entityNumbers2[i] = i + len(entityNumbers1)
    entityNumbers2 = random.sample(entityNumbers2.tolist(),
                                   int(len(entityNumbers2)))  # shuffel passengers

    availableSeats3 = []
    for x in range(3):
        for y in range(7):
            if y != 3:
                availableSeats3.append(((10-x) + 1.9, y * 0.5 + 0.75))
    entityNumbers3 = np.zeros(len(availableSeats3))
    for i in range(len(entityNumbers3)):
        entityNumbers3[i] = i + len(entityNumbers1) + len(entityNumbers2)
    entityNumbers3 = random.sample(entityNumbers3.tolist(),
                                   int(len(entityNumbers3)))  # shuffel passengers


    entityNumbers1=np.concatenate((entityNumbers1,entityNumbers2,entityNumbers3), axis=0)
    availableSeats1=np.concatenate((availableSeats1,availableSeats2,availableSeats3), axis=0)
    return entityNumbers1, availableSeats1

def steffenModified():
    availableSeats1 = []
    for x in range(11):
        for y in range(7):
            if y < 3 and x%2==0:
                availableSeats1.append((x + 1.9, y * 0.5 + 0.75))
    entityNumbers1 = np.zeros(len(availableSeats1))
    for i in range(len(entityNumbers1)):
        entityNumbers1[i] = i
    entityNumbers1 = random.sample(entityNumbers1.tolist(),
                                   int(len(entityNumbers1)))  # shuffel passengers

    availableSeats2 = []
    for x in range(11):
        for y in range(7):
            if y > 3 and x%2==0:
                availableSeats2.append((x + 1.9, y * 0.5 + 0.75))
    entityNumbers2 = np.zeros(len(availableSeats1))
    for i in range(len(entityNumbers2)):
        entityNumbers2[i] = i + len(availableSeats1)
    entityNumbers2 = random.sample(entityNumbers2.tolist(),
                                   int(len(entityNumbers2)))  # shuffel passengers

    availableSeats3 = []
    for x in range(11):
        for y in range(7):
            if y < 3 and x%2==1:
                availableSeats3.append((x + 1.9, y * 0.5 + 0.75))
    entityNumbers3 = np.zeros(len(availableSeats3))
    for i in range(len(entityNumbers3)):
        entityNumbers3[i] = i + len(availableSeats1) + len(availableSeats2)

    availableSeats4 = []
    for x in range(11):
        for y in range(7):
            if y > 3 and x%2==1:
                availableSeats4.append((x + 1.9, y * 0.5 + 0.75))
    entityNumbers4 = np.zeros(len(availableSeats4))
    for i in range(len(entityNumbers4)):
        entityNumbers4[i] = i + len(availableSeats1) + len(availableSeats2) + len(availableSeats3)

    entityNumbers4 = random.sample(entityNumbers4.tolist(),
                                   int(len(entityNumbers4)))  # shuffel passengers



    entityNumbers1=np.concatenate((entityNumbers1,entityNumbers2,entityNumbers3,entityNumbers4), axis=0)
    availableSeats1=np.concatenate((availableSeats1,availableSeats2,availableSeats3,availableSeats4), axis=0)
    return entityNumbers1, availableSeats1

def windowMiddleAisle():
    availableSeats1 = []
    for x in range(11):
        for y in range(7):
            if y == 0 or y == 6:
                availableSeats1.append(((x) + 1.9, y * 0.5 + 0.75))
    entityNumbers1 = np.zeros(len(availableSeats1))
    for i in range(len(entityNumbers1)):
        entityNumbers1[i] = i
    entityNumbers1 = random.sample(entityNumbers1.tolist(),
                                   int(len(entityNumbers1)))  # shuffel passengers

    availableSeats2 = []
    for x in range(11):
        for y in range(7):
            if y == 1 or y == 5:
                availableSeats2.append(((x) + 1.9, y * 0.5 + 0.75))
    entityNumbers2 = np.zeros(len(availableSeats2))
    for i in range(len(entityNumbers2)):
        entityNumbers2[i] = i + len(entityNumbers1)
    entityNumbers2 = random.sample(entityNumbers2.tolist(),
                                   int(len(entityNumbers2)))  # shuffel passengers

    availableSeats3 = []
    for x in range(11):
        for y in range(7):
            if y == 2 or y == 4:
                availableSeats3.append(((x) + 1.9, y * 0.5 + 0.75))
    entityNumbers3 = np.zeros(len(availableSeats3))
    for i in range(len(entityNumbers3)):
        entityNumbers3[i] = i + len(entityNumbers1) + len(entityNumbers2)
    entityNumbers3 = random.sample(entityNumbers3.tolist(),
                                   int(len(entityNumbers3)))  # shuffel passengers


    entityNumbers1=np.concatenate((entityNumbers1,entityNumbers2,entityNumbers3), axis=0)
    availableSeats1=np.concatenate((availableSeats1,availableSeats2,availableSeats3), axis=0)
    return entityNumbers1, availableSeats1

#entityNumbers, availableSeats = randomSeating()
#entityNumbers, availableSeats = steffenPerfect()
#entityNumbers, availableSeats = backToFront3Groups()
entityNumbers, availableSeats = frontToBack3Groups()
#entityNumbers, availableSeats = steffenModified()
#entityNumbers, availableSeats = windowMiddleAisle()

seatPlan = []
for i in range(len(entityNumbers)):
    seatNumber = int(entityNumbers[i])
    targetX = availableSeats[seatNumber][0]
    targetY = availableSeats[seatNumber][1]
    seatPlan.append([(i + 1), targetX, targetY, 0.75, 2.24, 0.3, 1])

df = pd.DataFrame(seatPlan, columns=["index", "targetX", "targetY", "positionX", "positionY", "diameter", "speed"])
df.to_csv('seatingPlan.csv', index=False)
print(df)
