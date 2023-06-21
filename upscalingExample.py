import numpy as np
envWidth = 10
envHeight = 7
environment = np.zeros((envWidth, envHeight))
for x in range(envWidth):
    for y in range(envHeight):
        if y != 3:
            if x % 2 == 0:
                environment[x][y] = 1
        if x == 0 or x == envWidth - 1:
            environment[x][y] = 2
        if y == 0 or y == envHeight - 1:
            environment[x][y] = 2
print(np.transpose(environment,axes=None))
environmentUpscale = np.zeros((envWidth*2, envHeight*2))
for x in range(envWidth*2):
    for y in range(envHeight*2):
        environmentUpscale[x][y]=environment[int(x/2)][int(y/2)]
print(np.transpose(environmentUpscale,axes=None))