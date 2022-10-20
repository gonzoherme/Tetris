import math, copy, random

from cmu_112_graphics import *

#################################################
# Tetris
#################################################
def gameDimensions():
    # These values are set to the writeup defaults
    rows = 15
    cols = 10
    cellSize = 40
    margin = 40
    return (rows, cols, cellSize, margin)

def appStarted(app):
    # setting dimensions
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    # creating board full of blue empty Color
    app.emptyColor = 'blue'
    app.board = [[app.emptyColor]*app.cols]
    for _ in range(app.rows-1):
        app.board.extend([[app.emptyColor]*app.cols])


    # Defining our standard individual pieces
    app.iPiece = [
        [  True,  True,  True,  True ]
    ]
    app.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    app.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    app.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    app.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    app.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    app.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    # Putting the pieces into a list
    app.tetrisPieces = [app.iPiece, app.jPiece, app.lPiece, app.oPiece, app.sPiece, app.tPiece, app.zPiece]

    # Defining the colors each piece can be
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]


    # Begin the game by creating a new falling piece
    newFallingPiece(app)

    # timer, speed at which objects fall
    app.timerDelay = 400

    # game over boolean
    app.isGameOver = False

    # score = number of full rows
    app.fullRows = 0

    
def keyPressed(app, event):
    # check if the game is over
    if app.isGameOver == True:
        # restart game
        if event.key == 'r':
            appStarted(app)
        else:
            return
     
    # move left
    if event.key == 'Left':
        drow, dcol = 0, -1
        moveFallingPiece(app, drow, dcol)
    # move Right
    elif event.key == 'Right':
        drow, dcol = 0, +1
        moveFallingPiece(app, drow, dcol)

    # move down
    elif event.key == 'Down':
        drow, dcol = +1, 0
        moveFallingPiece(app, drow, dcol)

    # rotate piece
    elif event.key == 'Up':
        rotateFallingPiece(app)

    # space bar move down instantly
    elif event.key == 'Space':
        counter = 0
        while True:
            if moveFallingPiece(app, counter, 0) == True:
                counter += 1
            else:
                moveFallingPiece(app, counter - 1, 0)
                break
    

    
def placeFallingPiece(app):
    for rowIndex in range(len(app.fallingPiece)):
        for colIndex in range(len(app.fallingPiece[0])):
            if app.fallingPiece[rowIndex][colIndex] == True:
                app.board[app.fallingPieceRow + rowIndex][app.fallingPieceCol + colIndex] = app.fallingPieceColor

    # after placing piece, remove the complete rows
    for row in app.board:
        if row.count(app.emptyColor) == 0:
            app.board.remove(row)
            emptyRow = [app.emptyColor]*app.cols
            app.board.insert(0, emptyRow)
            app.fullRows += 1
    
        
def timerFired(app):
    # check to see if game is over
    if app.isGameOver == True:
        return

    # we call moving the Piece. If it can't move, then place it
    if moveFallingPiece(app, +1, 0) == False:
        placeFallingPiece(app)
        newFallingPiece(app)

        #check if the new Piece is Legal, if it isn't, then game is over
        if fallingPieceIsLegal(app, 0, 0) == False:
            app.isGameOver = True
        
        

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)

    # set shape and color of the falling piece
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]

    # set position of the falling piece relative to the board
    app.fallingPieceRow = 0
    # set left column of the new fallinc piece, centered
    app.fallingPieceCol = (app.cols//2) - len(app.fallingPiece[0])//2


def moveFallingPiece(app, drow, dcol):
    # check if the movement is legal
    if fallingPieceIsLegal(app, drow, dcol):
        # change the column and row of the top left corner of the falling piece
        app.fallingPieceRow += drow
        app.fallingPieceCol += dcol
        return True

    else: # if the move didn't occur
        return False


        

def rotateFallingPiece(app):
    # store original piece values
    piece = app.fallingPiece
    rowNum = len(piece)
    colNum = len(piece[0])

    rotated = []
    for column in range(len(piece[0])): #for every column index
        currentRow = []
        # get all elements, put into row, and then into rotated
        for row in range(len(piece)):
            currentRow.append(piece[row][column])

        rotated.extend([currentRow])
    rotated.reverse()


    # Computing a centered rotation

    # CENTER ROW COMPUTATION
    #calculate center row of falling piece
    oldCenterRow = app.fallingPieceRow + len(app.fallingPiece)//2
    #calculate center row of rotated piece
    newRow = app.fallingPieceRow
    newCenterRow = newRow + len(rotated)//2

    #set old and new row centers equal
    oldCenterRow = newCenterRow
    newRow = app.fallingPieceRow + len(app.fallingPiece)//2 - len(rotated)//2

    
    # CENTER COLUMN COMPUTATION
    oldCenterCol = app.fallingPieceCol + len(app.fallingPiece[0])//2

    newCol = app.fallingPieceCol
    newCenterCol = newCol + len(rotated[0])//2

    #set old and new col centers equal
    oldCenterCol = newCenterCol
    newCol = app.fallingPieceCol + len(app.fallingPiece[0])//2 - len(rotated[0])//2

    #conserving previous values
    originalFallingPiece = app.fallingPiece
    originalRow = app.fallingPieceRow
    originalCol = app.fallingPieceCol

    # setting the values
    app.fallingPiece = rotated
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol
        
    # revert if not legal
    if not rotatedPieceIsLegal(app):
        print('---------')
        app.fallingPiece = originalFallingPiece
        app.fallingPieceRow = originalRow
        app.fallingPieceCol = originalCol
        
        
def fallingPieceIsLegal(app, drow, dcol):
    # we iterate over every cell (row and col) in the falling piece
    for rowIndex in range(len(app.fallingPiece)):
        for colIndex in range(len(app.fallingPiece[0])):
            if app.fallingPiece[rowIndex][colIndex] == True:
                # 1. Check The cell is in fact on the boar
                if ((app.fallingPieceRow + rowIndex) + drow > app.rows -1 or
                    (app.fallingPieceRow + rowIndex) + drow < 0 or
                    (app.fallingPieceCol + colIndex) + dcol > app.cols -1 or
                    (app.fallingPieceCol + colIndex) + dcol < 0):
                    return False
                # 2. The color at that location of the board is the emptyColor
                if app.board[(app.fallingPieceRow + rowIndex) + drow][(app.fallingPieceCol + colIndex) + dcol] != app.emptyColor:
                    return False

    # if check holds, then return True
    return True


def rotatedPieceIsLegal(app):
    tempLeftCornerRow = app.fallingPieceRow
    tempLeftCornerCol = app.fallingPieceCol
    # we iterate over every cell (row and col) in the falling piece
    for rowIndex in range(len(app.fallingPiece)):
        for colIndex in range(len(app.fallingPiece[0])):
            if app.fallingPiece[rowIndex][colIndex] == True:
                # 1. Check The cell is in fact on the boar
                if ((tempLeftCornerRow + rowIndex) > app.rows -1 or
                    (tempLeftCornerRow + rowIndex) < 0 or
                    (tempLeftCornerCol + colIndex) > app.cols -1 or
                    (tempLeftCornerCol + colIndex) < 0):
                    return False
                # 2. The color at that location of the board is the emptyColor
                if app.board[tempLeftCornerRow + rowIndex][tempLeftCornerCol + colIndex] != app.emptyColor:
                    return False


    return True


def drawCell(app, canvas, row, col, fillColor):
    canvas.create_rectangle(app.margin + (col*app.cellSize),
                            app.margin + ((row)*app.cellSize),
                            app.margin + ((col+1)*app.cellSize),
                            app.margin + ((row+1)*app.cellSize),
                            fill = fillColor,
                            outline = 'black')

    
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])#the last argument passed is the color of the fill

    canvas.create_text((2*app.margin + (app.cols*app.cellSize))/2,
                        app.margin/2,
                        text = f"Score: {app.fullRows}",
                        fill = 'blue',
                        font=('Helvetica','20','bold'))

     
    
def drawFallingPiece(app, canvas):
    for rowIndex in range(len(app.fallingPiece)):
        for colIndex in range(len(app.fallingPiece[0])):
            if app.fallingPiece[rowIndex][colIndex] == True:
                drawCell(app, canvas,
                         rowIndex + app.fallingPieceRow,
                         colIndex + app.fallingPieceCol,
                         app.fallingPieceColor)
            


def redrawAll(app, canvas):
    # draw full orange background
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'orange')
    
    # draw board
    drawBoard(app, canvas)

    # draw falling piece
    drawFallingPiece(app, canvas)

    # game over
    if app.isGameOver == True:
        canvas.create_rectangle(app.margin,
                                app.height/4,
                                (app.margin + app.cols*app.cellSize),
                                app.height/3,
                                fill = 'black')

        canvas.create_text(app.width/2, app.height/3.4, text='    Game over!\n Press r to restart!',
                           font='Arial 20 bold', fill='yellow')

      

def playTetris():
    # Note: Instead of hardcoding width and height, you should call
    # gameDimensions() and calculate the correct width and height values 
    # from rows, cols, cellSize, and margin
    rows, cols, cellSize, margin = gameDimensions()
    height = (2 * margin) + (rows * cellSize)
    width = (2 * margin) + (cols * cellSize)
    runApp(width = width, height = height)


playTetris()
