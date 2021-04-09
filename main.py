from timetracker import TimeTracker
from drawing import Vector2, drawing
from debug import debug
from Sparx import Sparx
from Qix import Qix

import time
import math
import random

import pygame
# import antigravity

running = True
sparx1 = Sparx(0.515, 0, 0.005, False)
sparx2 = Sparx(0.485, 0, -0.005, True)


def checkIfCrossedLineForPoly(playerPosition, lines, linesAllowed):
    for line in lines:
        if (line[0], line[1]) in linesAllowed:
            continue
        if playerPosition[0] >= min(line[1][0], line[0][0]) and playerPosition[0] <= max(line[1][0], line[0][0]):
            if playerPosition[1] >= min(line[1][1], line[0][1]) and playerPosition[1] <= max(line[1][1], line[0][1]):
                return True, line[0], line[1]
    if playerPosition[0] <= 0:
        if not ((0, 0), (0, screenHeight)) in linesAllowed:
            return True, (0, 0), (0, screenHeight)
    if playerPosition[0] >= screenWidth:
        if not ((screenWidth, 0), (screenWidth, screenHeight)) in linesAllowed:
            return True, (screenWidth, 0), (screenWidth, screenHeight)
    if playerPosition[1] <= 0:
        if not ((0, 0), (screenWidth, 0)) in linesAllowed:
            return True, (0, 0), (screenWidth, 0)
    if playerPosition[1] >= screenHeight:
        if not ((0, screenHeight), (screenWidth, screenHeight)) in linesAllowed:
            return True, (0, screenHeight), (screenWidth, screenHeight)

    return False, 0, 0

# Simulates an approach from a starting playerposition in a given direction until it hits a line or the edge
# Returns the distance the player is from a line or the edge and the point at which they connect in that direction


def simulateApproachForPoly(playerPosition, lines, direction, linesAllowed):
    notHitLine = True
    simulateX = playerPosition[0]
    simulateY = playerPosition[1]
    while notHitLine:
        crossedLine, startLine, endLine = checkIfCrossedLineForPoly(
            (simulateX, simulateY), lines, linesAllowed)
        if crossedLine:
            return (simulateX, simulateY), startLine, endLine
        simulateX += direction[0]
        simulateY += direction[1]
    return (simulateX, simulateY), startLine, endLine


def getPolyPoints(points, lines, lastDirection):
    # First get direction of trace
    # Then follow that direction until it hits a line
    # Add point at new spot
    # Turn in new direction
    # Repeat until found first point
    if lastDirection == "up":
        direction = (0, -1)
    elif lastDirection == "down":
        direction = (0, 1)
    elif lastDirection == "right":
        direction = (1, 0)
    elif lastDirection == "left":
        direction = (-1, 0)
    newPoint = (-500, -500)
    linesAllowed = []
    while not newPoint == points[0]:
        newPoint, lineStart, lineEnd = simulateApproachForPoly(
            points[-1], lines, direction, linesAllowed)
        points.append(newPoint)
        if not (lineStart, lineEnd) in linesAllowed:
            linesAllowed.append((lineStart, lineEnd))
        if lineEnd[0] == lineStart[0]:
            if points[0][1] < newPoint[1]:
                direction = (0, -1)
            else:
                direction = (0, 1)
        else:
            if points[0][0] < newPoint[0]:
                direction = (-1, 0)
            else:
                direction = (1, 0)
    return points

# Since the player's x, y is offset by its radius we have to adjust the first and last polygon points


def fixPoints(points):
    newPoints = [0] * len(points)
    for i in range(len(points)):
        # If close to line to left
        direction = (-1, 0)
        distance, intersectPoint = simulateApproach(
            points[i], finalLines, direction)
        if distance == 5:
            newPoints[i] = intersectPoint  # (points[i][0] - 5, points[i][1])
            continue
        # If close to line to right
        direction = (1, 0)
        distance, intersectPoint = simulateApproach(
            points[i], finalLines, direction)
        if distance == 5:
            newPoints[i] = intersectPoint  # (points[i][0] + 5, points[i][1])
            continue
        # If close to line above
        direction = (0, -1)
        distance, intersectPoint = simulateApproach(
            points[i], finalLines, direction)
        if distance == 5:
            newPoints[i] = intersectPoint  # (points[i][0], points[i][1] - 5)
            continue
        # If close to line below
        direction = (0, 1)
        distance, intersectPoint = simulateApproach(
            points[i], finalLines, direction)
        if distance == 5:
            newPoints[i] = intersectPoint  # (points[i][0], points[i][1] + 5)
            continue
        else:
            newPoints[i] = points[i]
    return newPoints
# Same reasoning for the lines as with fixing the polygon points


def fixLines(lines):
    newLines = [0] * len(lines)
    counter = 0
    for line in lines:
        points = [line[0], line[1]]
        newPoints = fixPoints(points)
        newStart = newPoints[0]
        newEnd = newPoints[1]
        newLines[counter] = (newStart, newEnd)
        counter += 1
    return newLines


# Checks if player has crossed either a line or the sides of the window
def checkIfCrossedLine(playerPosition, lines):
    for line in lines:
        if playerPosition[0] >= min(line[1][0], line[0][0]) and playerPosition[0] <= max(line[1][0], line[0][0]):
            if playerPosition[1] >= min(line[1][1], line[0][1]) and playerPosition[1] <= max(line[1][1], line[0][1]):
                #print("Found line")
                return True
    if playerPosition[0] <= 0 or playerPosition[0] >= screenWidth:
        return True
    if playerPosition[1] <= 0 or playerPosition[1] >= screenHeight:
        return True

# Simulates an approach from a starting playerposition in a given direction until it hits a line or the edge
# Returns the distance the player is from a line or the edge and the point at which they connect in that direction


def simulateApproach(playerPosition, lines, direction):
    notHitLine = True
    distance = 0
    simulateX = playerPosition[0]
    simulateY = playerPosition[1]
    while notHitLine:
        if checkIfCrossedLine((simulateX, simulateY), lines):
            return distance, (simulateX, simulateY)
        distance += 1
        simulateX += direction[0]
        simulateY += direction[1]
    return distance, (simulateX, simulateY)

# Function that essentially returns whether we are on a wall or not


def distanceToAnyLine(playerPosition, lines):
    distance = [0] * 4
    direction = (-1, 0)
    distance[0], playerPosition = simulateApproach(
        (x, y), finalLines, direction)
    direction = (1, 0)
    distance[1], playerPosition = simulateApproach(
        (x, y), finalLines, direction)

    direction = (0, -1)
    distance[2], playerPosition = simulateApproach(
        (x, y), finalLines, direction)
    direction = (0, 1)
    distance[3], playerPosition = simulateApproach(
        (x, y), finalLines, direction)
    return 5 in distance


# Main
screenWidth = 500
screenHeight = 500

x = 5  # starting x
y = 5  # starting y
playerRadius = 5
velocity = 15
lives = 3
lineStart = (0, 0)  # Used for drawing the first line
lastKeyPressed = None  # Used to check for changing directions
lines = []
polys = []
points = []  # List of points that make up the polygons
finalLines = []
direction = (0, 0)


def bound(pos: Vector2) -> None:
    if pos.x < 0:
        pos.x = 1 - 0
    if pos.x > 1 - 0:
        pos.x = 0
    if pos.y < 0:
        pos.y = 1 - 0
    if pos.y > 1 - 0:
        pos.y = 0


def angle(mov: Vector2) -> float:
    return math.atan2(mov.y, mov.x) * (180 / math.pi)


def game_update() -> None:
    global qix_pos
    global qix_mov

    global ply_pos
    global ply_mov

    global count

    global sparx1
    global sparx2
    global qix

    global screenWidth
    global screenHeight
    global x
    global y
    global playerRadius
    global velocity
    global lives
    global lineStart
    global lastKeyPressed
    global lines
    global polys
    global points
    global finalLines
    global direction

    drawing.setup_frame()

    if count % 4 == 0:
        #qix_pos = qix_pos + qix_mov
        # bound(qix_pos)

        ply_pos = ply_pos + ply_mov
        bound(ply_pos)

        #qix_mov.rotate_ip(random.randint(0, 20))

    drawing.borders()

    keys = pygame.key.get_pressed()

    # LEFT KEY
    if keys[pygame.K_LEFT]:
        if not lastKeyPressed == "left":
            lineStart = (x, y)
            points.append(fixPoints([(x, y)])[0])
            direction = (-1, 0)
            finalLines += fixLines(lines)
        distance, playerPosition = simulateApproach(
            (x - playerRadius, y), finalLines, direction)
        if distance < velocity:
            x = playerPosition[0]
            points.append(fixPoints([(x, y)])[0])
            x += playerRadius
            print("left blocked")

        else:
            x -= velocity

        # If changing direction start a new line and note that this is a vertix
        lastKeyPressed = "left"

    # RIGHT KEY
    elif keys[pygame.K_RIGHT]:

        if not lastKeyPressed == "right":
            lineStart = (x, y)
            points.append(fixPoints([(x, y)])[0])
            direction = (1, 0)
            finalLines += fixLines(lines)
        distance, playerPosition = simulateApproach(
            (x + playerRadius, y), finalLines, direction)
        if distance < velocity:
            x = playerPosition[0]
            points.append(fixPoints([(x, y)])[0])
            x -= playerRadius
            print("right blocked")

        else:
            x += velocity

        lastKeyPressed = "right"

    # UP KEY
    elif keys[pygame.K_UP]:
        if not lastKeyPressed == "up":
            lineStart = (x, y)
            points.append(fixPoints([(x, y)])[0])
            direction = (0, -1)
            finalLines += fixLines(lines)
        distance, playerPosition = simulateApproach(
            (x, y - playerRadius), finalLines, direction)
        if distance < velocity:
            y = playerPosition[1]
            points.append(fixPoints([(x, y)])[0])
            y += playerRadius
            print("up blocked")

        else:
            y -= velocity

        lastKeyPressed = "up"

    # DOWN KEY
    elif keys[pygame.K_DOWN]:
        if not lastKeyPressed == "down":
            lineStart = (x, y)
            points.append(fixPoints([(x, y)])[0])
            direction = (0, 1)
            finalLines += fixLines(lines)
        distance, playerPosition = simulateApproach(
            (x, y + playerRadius), finalLines, direction)
        if distance < velocity:
            y = playerPosition[1]
            points.append(fixPoints([(x, y)])[0])
            y -= playerRadius
            print("down blocked")
        else:
            y += velocity
        lastKeyPressed = "down"

    # If not on wall append line behind us
    if not distanceToAnyLine((x, y), finalLines):
        try:
            lines.pop()
        except:
            pass
        lines.append((lineStart, (x, y)))
    # Otherwise (if on wall)
    else:
        onWall = True
        if len(points) > 1:
            points.append(fixPoints([(x, y)])[0])
            lines.append((lineStart, (x, y)))
            points = getPolyPoints(points, finalLines, lastKeyPressed)
            #points = getCorrectPoints(points)
            if len(points) > 3:
                polys.append(points)
        points = []

    qix.draw(0.1)
    collided = qix.collision()
    if collided:
        print("collision occurred!")
    qix.move()

    drawing.lines(polys, lines)
    drawing.player((x / 500, y / 500), 0, 0.03)

    sparx1.draw()
    sparx2.draw()
    sparx1.move()
    sparx2.move()

    drawing.end()

    # debug.draw_tps()

    pygame.display.flip()


def main():
    global running

    global qix_pos
    global qix_mov

    global ply_pos
    global ply_mov

    global count
    global qix

    pygame.init()
    pygame.display.set_caption("Qix")
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

    gameUpdate = TimeTracker(time.perf_counter_ns)

    drawing.set_surface(screen)
    debug.set_surface(screen)
    sparx1.set_surface(screen)
    sparx2.set_surface(screen)

    #qix_pos = Vector2(0.25, 0.5)
    #qix_mov = Vector2(0.01, 0.0)
    qix = Qix(Vector2(0.25, 0.5))

    ply_pos = Vector2(0.6, 0.0)
    ply_mov = Vector2(random.uniform(0, 0.01), random.uniform(0, 0.01))

    count = 0

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        #  16666667
        #  16000000
        # 100000000
        gameUpdate.once_after(16666667, game_update)
        gameUpdate.accumulate()


if __name__ == "__main__":
    main()
