from PIL import Image
import math
from random import randint


def createLine(startPoint: tuple, endPoint: tuple) -> list:
    dx = int(abs(startPoint[0] - endPoint[0]))
    dy = int(abs(startPoint[1] - endPoint[1]))
    if endPoint[0] > startPoint[0]: #left/right check
        goRight = True
    else:
        goRight = False
    if endPoint[1] > startPoint[1]: #above/below check
        goDown = True
    else:
        goDown = False
    if dx >= dy: # Determine whether to iterate across x or y
        longest = dx
        shortest = dy
    else:
        longest = dy
        shortest = dx
    x = startPoint[0]
    y = startPoint[1]
    output = []
    for i in range(longest+1):
        if (longest != 0):
            percentage = (i+1)/longest
        else:
            percentage = 1
        output.append((x,y))
        if (longest == dx):
            x = addOrSubtract(x, 1, goRight)
            y = addOrSubtract(startPoint[1], round(shortest*percentage), goDown)
        else:
            x = addOrSubtract(startPoint[0], round(shortest*percentage), goRight)
            y = addOrSubtract(y, 1, goDown)
    return output


def addOrSubtract(op1: int, op2: int, boolean: bool) -> int: #CreateLine helper
    if boolean:
        return op1 + op2
    else:
        return op1 - op2


def colorFigure(image, pixelArray: list, color: tuple, scale=1) -> None:
    # pixelArray = scaleFigure(pixelArray, scale)
    for pixel in pixelArray:
        image.putpixel(pixel, color)


def createNodeDistribution(nodeArray: list, origin: tuple, scale: float) -> dict:
    output = {}
    n = len(nodeArray)
    angleBetweenNodes = 2 * math.pi / n
    distanceFromOrigin = origin[1]*(scale/100)
    currentPoint = (origin[0], round(origin[1] - distanceFromOrigin))
    currentAngle = angleBetweenNodes
    for i in range(n):
        currentAngle += 2 * math.pi / n
        currentPoint = (origin[0] - round(distanceFromOrigin * math.sin(currentAngle)), 
                        origin[1] - round(distanceFromOrigin * math.cos(currentAngle)))
        output[nodeArray[i]] = currentPoint
    return output


def organizeByDegree(nodeArray: list, edgeArray: list) -> list:
    count = [0 for _ in range(len(nodeArray))]
    for edge in edgeArray:
        count[edge[0]] += 1
        count[edge[1]] += 1
    output = []
    for i in range(len(nodeArray)):
        index = count.index(max(count))
        output.append(index)
        count[index] = 0
    return output


def createNode(point: tuple) -> list:
    output = []
    x = point[0] - 1
    y = point[1] - 1
    for a in range(3):
        for b in range(3):
            if (a != 1) or (b != 1):
                output.append((x+a, y+b))
    return output


def drawPattern(image, color: tuple) -> None:
    width, height = image.size
    toDraw = createPattern()
    for pixel in toDraw:
        image.putpixel(pixel, color)

def createPattern() -> list:
    output = []
    counter = 1
    for x in range(width):
        counter = counter % 2 + 1
        for y in range(height):
            counter = counter % 2 + 1
            if (counter >= 2):
                output.append((x,y))
    return output

def scaleFigure(figure: list, factor: int) -> list:
    output = []
    for pixel in figure:
        for a in range(-factor, factor+1):
            for b in range(-factor, factor+1):
                output.append((pixel[0]+a, pixel[1]+b))
    return output


def drawGraph(image, 
            nodeArray: list, 
            edgeArray:list, 
            scale: float, 
            nodeColor: tuple, 
            edgeColor:tuple) -> None:
    width, height = image.size
    origin = (math.ceil(width/2), math.ceil(height/2))
    nodePlacements = createNodeDistribution(nodeArray, origin, scale)
    for edge in edgeArray:
        pointA = edge[0]
        pointB = edge[1]
        colorFigure(image,
                createLine(nodePlacements[pointA], nodePlacements[pointB]),
                edgeColor, scale=10)
    for key, node in nodePlacements.items():
        colorFigure(image, createNode(node), nodeColor, scale=10)


def createRandomGraph(sparsityScale: int) -> tuple:
    nodeCount = randint(3, 12)
    nodes = [i for i in range(nodeCount)]
    edges = []
    for u in nodes:
        for v in nodes:
            rand = randint(0,sparsityScale)
            if (rand == 0 and u != v):
                edges.append((u,v))
    return (nodes, edges)


if __name__ == "__main__":
    width = 500
    height = 500
    origin = (math.ceil(width/2), math.ceil(height/2))

    image = Image.new(mode = "RGB", size = (width, height), color = (0, 0, 0))

    drawPattern(image, (20,20,20))
    nodeArray, edgeArray = createRandomGraph(4)
    nodeArray = organizeByDegree(nodeArray, edgeArray)
    drawGraph(image, nodeArray, edgeArray, 75, (255, 255, 255, 255), (0, 255, 0, 255))

    image.save("img.png")
