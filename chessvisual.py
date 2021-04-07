import pygame, sys, random
from pygame.locals import *
import MCTS
import time

BACKGROUNDCOLOR = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE=(255,251,240)
YELLOW = (255, 255, 22)
CELLWIDTH = 50
CELLHEIGHT = 50
PIECEWIDTH = 44
PIECEHEIGHT = 44#asd
BOARDX = 0
BOARDY = 0
FPS = 40


def terminate():
    pygame.quit()
    sys.exit()

def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = 'none'

    # Starting pieces:
    board[3][3] = 'black'
    board[3][4] = 'white'
    board[4][3] = 'white'
    board[4][4] = 'black'

def getNewBoard():
    board = []
    for i in range(8):
        board.append(['none'] * 8)

    return board

def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
        return False

    board[xstart][ystart] = tile

    if tile == 'black':
        otherTile = 'white'
    else:
        otherTile = 'black'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = 'none'  # restore the empty space
    if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7

def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'black':
                xscore += 1
            if board[x][y] == 'white':
                oscore += 1
    return {'black': xscore, 'white': oscore}


def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


# belongs to optimization
def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getComputerMove0(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def getComputerMove1(board, computerTile):
        tempboard=getBoardCopy(board)
        (movesx,movesy)=MCTS.output(tempboard,computerTile)
        return (movesx,movesy)
    
def isGameOver(board):
    score = getScoreOfBoard(board)
    if score['black'] == 0 or score['white'] == 0:
        return True
    if timeout==True:
        return True
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'none':
                return False
    return True


if __name__ == '__main__':
    pygame.init()
    mainClock = pygame.time.Clock()
    boardImage = pygame.image.load('board.png')
    boardRect = boardImage.get_rect()
    blackImage = pygame.image.load('black.png')
    blackRect = blackImage.get_rect()
    whiteImage = pygame.image.load('white.png')
    whiteRect = whiteImage.get_rect()
    basicFont = pygame.font.SysFont(None, 48)
    gameoverStr = 'Game Over Score '
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    turn = whoGoesFirst()
    if turn == 'player':
        playerTile = 'black'
        computerTile = 'white'
    else:
        playerTile = 'white'
        computerTile = 'black'

    print('%s first'%turn)
    timeout=False
    windowSurface = pygame.display.set_mode((boardRect.width+4*CELLWIDTH, boardRect.height))
    pygame.display.set_caption('progream test')
    gameOver = False#might exist problem
    #set time preparation
    def set_clock():
        clockcounter=60
        while True:
            time=pygame.time.get_ticks()
            if (time%1000 == 0):
                clockcounter = clockcounter - 1
                clocksurface=myfont.render('%ds remaining'%clockcounter,False,(0,255,0))
                windowSurface.blit(clocksurface,(boardRect.width+1,boardRect.height/2))
                pygame.display.update()
            eventtype=pygame.event.get()
            if eventtype==pygame.MOUSEBUTTONDOWN:
                if clockcounter<=0:
                    timeout=True
                return 1
    #set text preparation
    pygame.font.init()
    roundtag=1
    time_start2=time.time()
    myfont = pygame.font.SysFont(False, 29)
    herfont = pygame.font.SysFont('Comic Sans MS', 19)
    textsurface = myfont.render('echo time:0.0s',False, (0, 0, 255))
    tipssurface1=myfont.render('you are the %s tile'%playerTile,False,(0,0,0))
    thankssurface= herfont.render('dedicated to: Getchar',False,(255,0,0))
#    copyrightsurface=myfont.render('programmed by:PB18000313',False,(255,0,0)) just do it before uploading
    # main part
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                terminate()
            if isGameOver(mainBoard) == False and turn == 'player' and event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:
                if roundtag == 2:
                    time_end2=time.time()
                    movestime=time_end2-time_start2
                    if movestime>=60:
                        timeout=True
                x, y = pygame.mouse.get_pos()
                col = int((x - BOARDX) / CELLWIDTH)
                row = int((y - BOARDY) / CELLHEIGHT)
                if makeMove(mainBoard, playerTile, col, row) == True:
                    if getValidMoves(mainBoard, computerTile) != []:
                        turn = 'computer'

            if event.type == pygame.locals.KEYUP:
                if event.key == pygame.K_q:
                    turn = 'computer'

        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(boardImage, boardRect, boardRect)
        windowSurface.blit(textsurface,(boardRect.width+1,boardRect.height/32))
#        windowSurface.blit(thankssurface,(boardRect.width+1,3*boardRect.height/4))
        windowSurface.blit(tipssurface1,(boardRect.width+1,boardRect.height/14))
        if (isGameOver(mainBoard) == False and turn == 'computer'):
            time_start=time.time()
            (x, y)= getComputerMove1(mainBoard, computerTile)
            time_end=time.time()
            makeMove(mainBoard, computerTile, x, y)#here the computer makes a move
            time_start2=time.time()
            roundtag=2
            savex, savey = x, y
            textsurface = myfont.render('echo time:%fs'%(time_end-time_start),False, (0, 0, 0))
            windowSurface.fill(BACKGROUNDCOLOR)
            windowSurface.blit(boardImage, boardRect, boardRect)
            pygame.display.update()
            if getValidMoves(mainBoard, playerTile) != []:
                turn = 'player'

        score = getScoreOfBoard(mainBoard)
        if score['black'] == 0 or score['white'] == 0 or isGameOver(mainBoard):
            gameOver = True

    #    windowSurface.fill(BACKGROUNDCOLOR)
    #    windowSurface.blit(boardImage, boardRect, boardRect)
        #this part is used to update the tile image
        for x in range(8):
            for y in range(8):
                rectDst = pygame.Rect(BOARDX + x * CELLWIDTH + 2, BOARDY + y * CELLHEIGHT + 2, PIECEWIDTH, PIECEHEIGHT)
                if mainBoard[x][y] == 'black':
                    windowSurface.blit(blackImage, rectDst, blackRect)
                elif mainBoard[x][y] == 'white':
                    windowSurface.blit(whiteImage, rectDst, whiteRect)
        #this part is used to update the score image
        if isGameOver(mainBoard) == True:
            scorePlayer = getScoreOfBoard(mainBoard)[playerTile]
            scoreComputer = getScoreOfBoard(mainBoard)[computerTile]
            if scorePlayer > scoreComputer and timeout == False:
                outputStr = "Win! " + str(scorePlayer) + ":" + str(scoreComputer)
            elif scorePlayer == scoreComputer:
                outputStr = "Tie. " + str(scorePlayer) + ":" + str(scoreComputer)
            else:
                outputStr = "Lose. " + str(scorePlayer) + ":" + str(scoreComputer)
            text = basicFont.render(outputStr, True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.centerx = windowSurface.get_rect().centerx
            textRect.centery = windowSurface.get_rect().centery
            windowSurface.blit(text, textRect)

        pygame.display.update()
        mainClock.tick(FPS)