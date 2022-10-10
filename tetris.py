from tkinter import *
import pygame
from pygame import mixer

###
# Instructions: http://www.krivers.net/CSS-m21/tetris/index.html
###

###
# Did you add any bonus features? List them here!
###

###########################
# customize these functions
###########################

#Background Music



def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return [rows, cols, cellSize, margin]

def getTetrisPieces():
    # Seven "standard" pieces (tetrominoes)

    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    return [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

def init(data):
    # Set up your simulation components here, by setting
    # data.compName = component
    result = gameDimensions()
    data.rows = result[0]
    data.cols = result[1]
    data.cellSize = result[2]
    data.margin = result[3]
    data.emptyColor = "blue"
    data.board = []
    tetrisPieces = getTetrisPieces()
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors
    fallingPieceColor = ""
    data.fallingPieceColor = ""
    data.isGameOver = False
    mixer.init()
    mixer.music.load('tetris.mid')
    mixer.music.play(loops=0)
    for row in range(data.rows):
        data.board.append([data.emptyColor] * data.cols)
# pre-load a few cells with known colors for testing purposes
    newFallingPiece(data)
    data.score = 0
    pass

def newFallingPiece(data):
    import random
    num = random.randint(0 , len(data.tetrisPieces)-1)
    num2 = random.randint(0, len(data.tetrisPieceColors)-1)
    data.fallingPiece = data.tetrisPieces[num]
    data.fallingPieceColor = data.tetrisPieceColors[num2]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols // 2 - len(data.fallingPiece[0]) // 2
    return

def drawFallingPiece(canvas, data):
    for rowz in range(len(data.fallingPiece)):
        for colz in range(len(data.fallingPiece[rowz])):
            if data.fallingPiece[rowz][colz] == True:
                row = data.fallingPieceRow + rowz
                col = data.fallingPieceCol + colz
                drawCell(canvas, data, row, col, data.fallingPieceColor)
    return

def drawCell(canvas, data, row, col, fallingPieceColor):
    top = row * data.cellSize
    bottom = top + data.cellSize
    left = col * data.cellSize
    right = left + data.cellSize
    if fallingPieceColor == "":
        canvas.create_rectangle(left + data.margin, top + data.margin, right + data.margin, bottom + data.margin, fill = data.board[row][col], width = 2)
    else:
        canvas.create_rectangle(left + data.margin, top + data.margin, right + data.margin, bottom + data.margin, fill = data.fallingPieceColor, width = 2)
    return

def drawBoard(canvas, data):
    for row in range(len(data.board)):
        for col in range(len(data.board[row])):
            fallingPieceColor = ''
            drawCell(canvas, data, row, col, fallingPieceColor)
    return

def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow = data.fallingPieceRow + drow
    data.fallingPieceCol = data.fallingPieceCol + dcol
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow = data.fallingPieceRow - drow
        data.fallingPieceCol = data.fallingPieceCol - dcol
        return False
    else:
        return True

def rotateFallingPiece(data):
    rows = len(data.fallingPiece[0])
    cols = len(data.fallingPiece)
    justInCasePiece = data.fallingPiece
    newDimension = []
    for i in range(len(data.fallingPiece[0])):
        r = []
        for x in data.fallingPiece[::-1]:
            r.append(x[i])
        newDimension.append(r)
    data.fallingPiece = newDimension
    #data.fallingPieceRow = data.fallingPieceRow + rows//2 - len(newDimension)//2
    #data.fallingPieceCol = data.fallingPieceCol + cols//2 - len(newDimension[0])//2
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = justInCasePiece
    return

def placeFallingPiece(data):
    for rowz in range(len(data.fallingPiece)):
        for colz in range(len(data.fallingPiece[rowz])):
            if data.fallingPiece[rowz][colz] == True:
                row = data.fallingPieceRow + rowz
                col = data.fallingPieceCol + colz
                data.board[row][col] = data.fallingPieceColor
    removeFullRows(data)
    return

def drawGameOver(canvas, data):
    canvas.create_rectangle(data.margin, data.margin + data.cellSize, data.cols * data.cellSize + data.margin, 3 * data.cellSize + data.margin, fill = "black")
    canvas.create_text((data.cols//2) * data.cellSize + data.margin, 2 * data.cellSize + data.margin, font= 20,text="Game Over!", fill = "yellow")
    return

def removeFullRows(data):
    newBoard = []
    emptyRow = data.board[0]
    fullRows = 0
    for row in range(len(data.board)):
        if data.emptyColor in data.board[row]:
            newBoard.append(data.board[row])
        else:
            fullRow = data.board[row]
            fullRows = fullRows + 1
    new2Board = newBoard
    newBoard = []
    for i in range(fullRows):
        newBoard.append(emptyRow)
    for row in new2Board:
        newBoard.append(row)
    data.board = newBoard
    for i in range(fullRows):
        data.score += 1
    return

def drawScore(canvas, data):
    canvas.create_text((data.cols//2) * data.cellSize + data.margin, data.margin//2, font= 20,text= "Score:" + str(data.score), fill = "blue")
    return

def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                if data.fallingPieceCol < 0:
                    return False
                    Print("False")
                elif (data.fallingPieceCol + len(data.fallingPiece[0])) > data.cols:
                    return False
                elif data.fallingPieceRow < 0:
                    return False
                elif data.fallingPieceRow + len(data.fallingPiece) > data.rows:
                    return False
                elif data.board[data.fallingPieceRow + row][data.fallingPieceCol + col] != data.emptyColor:
                    return False
    return True

def redrawAll(canvas, data):
    # Write your simulation view here, using the Tkinter canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange", width = 0)
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    if data.isGameOver == True:
        drawGameOver(canvas, data)
    drawScore(canvas, data)
    pass

def timerFired(data):
    # Write your simulation rules here, by changing data
    if fallingPieceIsLegal(data) == False:
        data.isGameOver = True
    if data.isGameOver != True:
        if moveFallingPiece(data, 1, 0) != True:
            placeFallingPiece(data)
            newFallingPiece(data)
    pass

def keyPressed(event, data):
    # Use event.char to get the character pressed
    if data.isGameOver == False:
        if event.keysym == "Down":
            moveFallingPiece(data, 1, 0)
        elif event.keysym == "Up":
            rotateFallingPiece(data)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        elif event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
    if event.char == "r":
        init(data)
    pass

def mousePressed(event, data):
    # Use event.x and event.y to get the (x,y) location of the clicked pixel
    pass

##############################################################
# You do not need to be able to write the following functions;
# just modify the five functions above.
##############################################################

def timeLoop(data, canvas):
    timerFired(data)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()

    canvas.after(data.timeRate, timeLoop, data, canvas)


def keyEventHandler(data, canvas, event):
    keyPressed(event, data)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()

def mouseEventHandler(data, canvas, event):
    mousePressed(event, data)

    canvas.delete(ALL)
    redrawAll(canvas, data)
    canvas.update()

class Model:
    pass



def runSimulation(w, h, rate):
    data = Model()
    data.width = w
    data.height = h
    data.timeRate = int(rate * 3000) # call will be in ms
    init(data)

    root = Tk()
    canvas = Canvas(root, width=w, height=h)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    redrawAll(canvas, data)

    canvas.after(data.timeRate, timeLoop, data, canvas)


    root.bind("<Key>", lambda event : keyEventHandler(data, canvas, event))
    root.bind("<Button-1>", lambda event : mouseEventHandler(data, canvas, event))

    root.mainloop()

def playTetris():
    [rows, cols, cellSize, margin] = gameDimensions()
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
    runSimulation(width, height, 0.1)

playTetris()
