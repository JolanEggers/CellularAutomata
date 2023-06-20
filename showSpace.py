import pygame

screenWidth = 1000
screenHeight = 600
pygame.init()
WINDOW_SIZE = (screenWidth, screenHeight)
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font(None, 20)
gridSize = 0.08
backgroundColor = (255, 255, 255)
lineThickness = 0.00


def showSpace(envWidth, envHeight, envResolution, environment, cellState, entities):
    screen.fill(backgroundColor)
    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):  # loops for environment
            cellColor = (125, 125, 125)
            if environment[x][y] == 1:  # seat
                cellColor = (0, 0, 255)
            if environment[x][y] == 2:  # wall
                cellColor = (125, 0, 0)
            pygame.draw.rect(screen, cellColor, (
                screenWidth * 0.1 + (x + lineThickness) * screenWidth * gridSize / envResolution,
                screenHeight * 0.1 + (y + lineThickness) * screenWidth * gridSize / envResolution,
                screenWidth * gridSize * (1.0 - lineThickness) / envResolution,
                screenWidth * gridSize * (1.0 - lineThickness) / envResolution))

    for x in range(int(envWidth * envResolution)):
        for y in range(int(envHeight * envResolution)):  # loops for entities
            if cellState[x][y] > 0:  # passanger
                cellColor = (245, 245, 220)
                if not entities[int(cellState[x][y]) - 1].luggageStored:
                    cellColor = (180, 225, 225)
                if entities[int(cellState[x][y]) - 1].changeSeatFor >= 0:
                    cellColor = (245, 10, 245)
                if len(entities[int(cellState[x][y]) - 1].awaitingSeatChangeFor) > 0:
                    cellColor = (245, 10, 100)
                diameter = entities[int(cellState[x][y]) - 1].diameter * screenWidth * gridSize * 0.5
                xHighRes = entities[int(cellState[x][y]) - 1].position[0] * envResolution
                yHighRes = entities[int(cellState[x][y]) - 1].position[1] * envResolution
                entityCenterOnScreen = (screenWidth * 0.1 + (xHighRes + 0.5) * screenWidth * gridSize / envResolution,
                                        screenHeight * 0.1 + (yHighRes + 0.5) * screenWidth * gridSize / envResolution)
                pygame.draw.circle(screen, cellColor,
                                   entityCenterOnScreen,
                                   diameter)
                text = font.render(str(int(entities[int(cellState[x][y]) - 1].index)), True, (0, 0, 0))

                screen.blit(text, (entityCenterOnScreen[0]-8,entityCenterOnScreen[1]-6))
    pygame.display.flip()
