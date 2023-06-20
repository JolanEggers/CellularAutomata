import random

import numpy as np
import pandas as pd

availableSeats = pd.read_csv("availableSeats.csv")
fillPercentage = 1  # how many of the seats should be filled
entityNumbers = np.zeros(len(availableSeats))
for i in range(len(entityNumbers)):
    entityNumbers[i] = i

entityNumbers = random.sample(entityNumbers.tolist(), int(len(entityNumbers) * fillPercentage))  # shuffel passengers

seatPlan = []
for i in range(len(entityNumbers)):
    seatNumber=int(entityNumbers[i])

    targetX = availableSeats.iloc[seatNumber]["targetX"]
    targetY = availableSeats.iloc[seatNumber]["targetY"]
    seatPlan.append([(i + 1), targetX, targetY, 0.75, 2.24, 0.3, 1])

df = pd.DataFrame(seatPlan, columns=["index", "targetX", "targetY", "positionX", "positionY", "diameter", "speed"])
df.to_csv('out.csv', index=False)
print(df)
