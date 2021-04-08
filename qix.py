import pygame

#Gets points to make polygons with. This function will be deleted when getPolyPoints works 
def getCorrectPoints(points):
	#Left to right straight across
	if (points[0][0] == 0 and points[-1][0] == screenWidth):
		points.append((screenWidth, screenHeight))
		points.append((0, screenHeight))
		return points
	#Right to left straight across 
	elif (points[0][0] == screenWidth and points[-1][0] == 0):
		points.append((0, screenHeight))
		points.append((screenWidth, screenHeight))
		return points
	#Up to down straight across 
	elif (points[0][1] == 0 and points[-1][1] == screenHeight):
		points.append((screenWidth, screenHeight))
		points.append((screenWidth, 0))
		return points
	#Down to up straight across 
	elif (points[0][1] == screenHeight and points[-1][1] == 0):
		points.append((screenWidth, 0))
		points.append((screenWidth, screenHeight))
		return points
	#Same wall 
	elif points[0][0] == points[-1][0] or points[0][1] == points[-1][1]:
		print("Same")
		#Same wall 
		return points
	#When ended on x side wall (and didn't go into same wall if) on corner
	elif points[-1][0] == 0 or points[-1][0] == screenWidth:
		print("Corner")
		points.append((points[-1][0], points[0][1]))
		return points
	#When ended on y side wall (and didn't go into same wall if) on corner
	elif points[-1][1] == 0 or points[-1][1] == screenHeight:
		points.append((points[0][0], points[-1][1]))
		return points
	else:
		print("this one")
		return []

#def getPolyPoints(points, lines): 
	#First get direction of trace 
	#Then follow that direction until it hits a line
	#Add point at new spot 
	#Turn in new direction 
	#Repeat until found first point 

#Since the player's x, y is offset by its radius we have to adjust the first and last polygon points
def fixPoints(points):
	if points[0][0] == 5:
		points[0] = (points[0][0] - 5, points[0][1])
	elif points[0][0] + playerRadius == screenWidth: 
		points[0] = (points[0][0] + 5, points[0][1])
	elif points[0][1] == 5:
		points[0] = (points[0][0], points[0][1] - 5)
	elif points[0][1] + playerRadius == screenHeight: 
		points[0] = (points[0][0], points[0][1] + 5)

	if points[-1][0] == 5:
		points[-1] = (points[-1][0] - 5, points[-1][1])
	elif points[-1][0] + playerRadius == screenWidth: 
		points[-1] = (points[-1][0] + 5, points[-1][1])
	elif points[-1][1] == 5:
		points[-1] = (points[-1][0], points[-1][1] - 5)
	elif points[-1][1] + playerRadius == screenHeight: 
		points[-1] = (points[-1][0], points[-1][1] + 5)
	return points

#Same reasoning for the lines as with fixing the polygon points
def fixLines(lines):
	newLines = [0] * len(lines)
	counter = 0
	for line in lines:
		points = [line[2], line[3]]
		newPoints = fixPoints(points)
		newStart = newPoints[0]
		newEnd = newPoints[1]
		newLines[counter] = (line[0], line[1], newStart, newEnd)
		counter += 1
	return newLines

#Checks if player has crossed either a line or the sides of the window 
def checkIfCrossedLine(playerPosition, lines):
	for line in lines:
		if playerPosition[0] >= min(line[3][0], line[2][0]) and playerPosition[0] <= max(line[3][0], line[2][0]):
			if playerPosition[1] >= min(line[3][1], line[2][1]) and playerPosition[1] <= max(line[3][1], line[2][1]):
				#print("Found line")
				return True
	if playerPosition[0] <= 0 or playerPosition[0] >= screenWidth:
		return True
	if playerPosition[1] <= 0 or playerPosition[1] >= screenHeight:
		return True

#Simulates an approach from a starting playerposition in a given direction until it hits a line or the edge 
#Returns the distance the player is from a line or the edge and the point at which they connect in that direction
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

#Function that essentially returns whether we are on a wall or not 
def distanceToAnyLine(playerPosition, lines):
	distance = [0] * 4
	direction = (-1, 0)
	distance[0], playerPosition = simulateApproach((x, y), finalLines, direction)
	direction = (1, 0)
	distance[1], playerPosition = simulateApproach((x, y), finalLines, direction)

	direction = (0, -1)
	distance[2], playerPosition = simulateApproach((x, y), finalLines, direction)
	direction = (0, 1)
	distance[3], playerPosition = simulateApproach((x, y), finalLines, direction)
	print(distance)
	return 5 in distance

#Main
screenWidth = 500
screenHeight = 500
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Qix")

x = 5 #starting x 
y = 5 #starting y 
playerRadius = 5
velocity = 15
run = True
lives = 3
lineStart = (0, 0) #Used for drawing the first line 
lastKeyPressed = None #Used to check for changing directions 
lines = []
polys = []
points = [] #List of points that make up the polygons 
onWall = True
finalLines = []
while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()

	#LEFT KEY
	if keys[pygame.K_LEFT]:
		if not lastKeyPressed == "left":
			lineStart = (x, y)
			points.append((x, y))
			direction = (-1, 0)
			finalLines += fixLines(lines)
		distance, playerPosition = simulateApproach((x - playerRadius, y), finalLines, direction)
		if distance < velocity:
			x = playerPosition[0] + playerRadius
			print("left blocked")
			onWall = True
			points.append((x, y)) 

		else:
			x -= velocity

		#If changing direction start a new line and note that this is a vertix 
		lastKeyPressed = "left"

	#RIGHT KEY
	elif keys[pygame.K_RIGHT]:

		if not lastKeyPressed == "right":
			lineStart = (x, y)
			points.append((x, y))
			direction = (1, 0)
			finalLines += fixLines(lines)
		distance, playerPosition = simulateApproach((x + playerRadius, y), finalLines, direction)
		if distance < velocity:
			x = playerPosition[0] - playerRadius 
			print("right blocked")
			onWall = True
			points.append((x, y))

		else:
			x += velocity

		#If changing direction start a new line and note that this is a vertix 
		lastKeyPressed = "right"

	#UP KEY
	elif keys[pygame.K_UP]:
		if not lastKeyPressed == "up":
			lineStart = (x, y)
			points.append((x, y))
			direction = (0, -1)
			finalLines += fixLines(lines)
		distance, playerPosition = simulateApproach((x, y - playerRadius), finalLines, direction)
		if distance < velocity:
			y = playerPosition[1] + playerRadius
			print("up blocked")
			onWall = True
			points.append((x, y)) 

		else:
			y -= velocity

		#If changing direction start a new line and note that this is a vertix 
		lastKeyPressed = "up"

	#DOWN KEY
	elif keys[pygame.K_DOWN]:
		if not lastKeyPressed == "down":
			lineStart = (x, y)
			points.append((x, y))
			direction = (0, 1)
			finalLines += fixLines(lines)
		distance, playerPosition = simulateApproach((x, y + playerRadius), finalLines, direction)
		if distance < velocity:
			y = playerPosition[1] - playerRadius 
			print("down blocked")
			onWall = True
			points.append((x, y))
		else:
			y += velocity 
		#If changing direction start a new line and note that this is a vertix 
		lastKeyPressed = "down"

	win.fill((0,0,0))
	pygame.draw.circle(win, (255, 0, 0), (x, y), playerRadius)
	#If not on wall append line behind us
	if not distanceToAnyLine((x, y), finalLines): #Off wall 
		onWall = False
	else: #On wall
		onWall = True
	if not onWall:
		try:
			lines.pop()
		except: 
			pass
		lines.append((win, (255, 255, 255), lineStart, (x, y)))
	#Otherwise (if on wall) 
	else:
		onWall = True
		if len(points) > 1:
			points.append((x, y))
			lines.append((win, (255, 255, 255), lineStart, (x, y)))
			points = fixPoints(points)
			points = getCorrectPoints(points)
			if len(points) > 3:
				polys.append((win, (0, 255, 0), points))
		points = []
	#Draw polygons
	for poly in polys:
		pygame.draw.polygon(poly[0], poly[1], poly[2])
	#Draw the final lines (only ones that are apart of some shape)
	for line in finalLines:
		pygame.draw.line(line[0], line[1], line[2], line[3])
	#Draw intermediate lines
	for line in lines:
		pygame.draw.line(line[0], line[1], line[2], line[3])

	pygame.display.update()

pygame.quit()



