import random, math, time

class MNode:
    def __init__(self, pos, board, parent, mytile):
        self.child = []
        self.maxchild = 0
        self.win = 0
        self.total = 1#visit time
        self.pos = pos# two elements,movesx and movesy
        self.C = 1.96 
        self.parent=parent
        self.board=board
        self.tile = mytile
        if self.tile == "black":
            self.enemytile = "white"
        if self.tile == "white":
            self.enemytile = "black"
    def Possibility_to_Win(self):
        return self.win/self.total

class MCTS(MNode):

    def __init__(self, pos, board, mytile):
        MNode.__init__(self, pos, board, None, mytile) 
#        self.makeMove(self.board, mytile, pos[0], pos[1])
        self.board=board
        self.optionalmove = self.getValidMoves(self.board, mytile)
        self.maxchild = len(self.optionalmove)
        self.child = []

    def newnode(self,movesx,movesy,parent,mytile):
        newnode=MNode((movesx,movesy), self.getBoardCopy(parent.board), parent,mytile)
        return newnode

    def evaluate(self):
        rootnode=self
        maxscore=65
        for node in rootnode.child:
            score = node.Possibility_to_Win() + rootnode.C * math.sqrt( math.log(rootnode.total) / node.total )
            if score > maxscore or maxscore==65:
                maxscore = score
                nextnode = node
        return nextnode

    def select(self):
        root = self
        while( root.child ):#len(root.child) == root.maxchild
            nextnode = None
            maxscore = -1
            for node in root.child:
                score = node.Possibility_to_Win() + self.C * math.sqrt( math.log(self.total) / node.total )
                if score > maxscore:
                    maxscore = score
                    nextnode = node
            root = nextnode
        # find the next child to do MCTS
        return root


    def expansion(self, node, mytile):#existing problem need to change
        if(self.isGameOver(node.board)==False):
            for (movesx,movesy) in self.optionalmove:
                tempnode=self.newnode(movesx,movesy,node,mytile)
                self.makeMove(tempnode.board,tempnode.tile,tempnode.pos[0],tempnode.pos[1])
                node.child.append(tempnode)
            self.simulation(tempnode)                        
        elif(self.isGameOver(node.board)==True):
            self.simulation(node)

    def simulation(self,node):#makemove here is on the node.board
        j=1
        ready=0
        while(self.isGameOver(node.board)==False):
            tiletype=(j==1 and node.enemytile or node.tile)
            moves=self.getValidMoves(node.board,tiletype)
            if(len(moves)!=0):#last updated,need caution
                i=random.randint(0,len(moves)==0 and len(moves) or len(moves)-1)
                (movesx,movesy)=moves[i]
                tempnode=self.newnode(movesx,movesy,node,tiletype)
                node.child.append(tempnode)
                node=tempnode
                self.makeMove(node.board,tiletype,movesx,movesy)
            if j == 1:
                j=2
                if(len(moves)==0):
                    ready=1
            elif j == 2:
                j=1
                if(len(moves)==0 and ready==1):
                    break
                else:
                    ready=0
        (scorex,scorey)=self.getScoreOfBoard(node.board)#need to update the parentnode here
        if node.tile=='black':#use win to deliver
            win = scorex>scorey and 1 or 0
        else:
            win = scorex>scorey and 0 or 1
        self.backpropagation(win,node)
        #how about joint backpropagation together

    def backpropagation(self,win,node):
        tempnode = node
        while(tempnode.parent!=None):
            tempnode.total+=1
            tempnode.win+=win
            tempnode=tempnode.parent            
        

    def rollout_policy(self, child):
        return child[random.randint(0,len(child)-1)]


    def getValidMoves(self, board, tile):
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    validMoves.append((x,y))
        return validMoves

    def getScoreOfBoard(self,board):
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'black':
                    xscore += 1
                if board[x][y] == 'white':
                    oscore += 1
        return (xscore,oscore)

    def getNewBoard(self):
        board = []
        for i in range(8):
            board.append(['none'] * 8)
        return board


    def getBoardCopy(self, board):
        dupeBoard = self.getNewBoard()

        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]

        return dupeBoard

    def makeMove(self, board, tile, xstart, ystart):
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)
        if tilesToFlip == False:
            return False
        board[xstart][ystart] = tile
        for x, y in tilesToFlip:
            board[x][y] = tile
        return True


    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <=7


    def isGameOver(self, board):
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'none':
                    return False
        return True

    def isValidMove(self, board, tile, xstart, ystart):

        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
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
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                if not self.isOnBoard(x, y):
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

def output(board,tile):
    pos=(0,0)
    root=MCTS(pos,board,tile)
    for (movesx,movesy) in root.optionalmove:
        tempnode=MCTS.newnode(root,movesx,movesy,root,tile)
        root.child.append(tempnode)
    time_starto=time.time()  
    time_endo=time.time()
    while((time_endo-time_starto) < 50):# able to change,depending on the rules
        node=MCTS.select(root)
        MCTS.expansion(root,node,tile)
        time_endo=time.time()
    result=MCTS.evaluate(root)
    (movesx,movesy)=(result.pos[0],result.pos[1])#select problem
    return (movesx,movesy)

        

