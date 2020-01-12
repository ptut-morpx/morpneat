def sortedindexes(l):
    x=list(range(len(l)))
    l=[i for i in l]
    s=False
    n=len(l)-1
    while not s:
        s=True
        for i in range(n):
            if l[i]<l[i+1]:
                l[i], l[i+1], x[i], x[i+1]=l[i+1], l[i], x[i+1], x[i]
                s=False
        n-=1
    return x

def getpos(idx):
    x=idx%3
    y=idx//3%3
    x2=idx//9%3
    y2=idx//27
    return x, y, x2, y2

def getNNList(game, player, turn):
    enemy=2 if player==1 else 1

    # AI should know if it's P1 or P2   (2)
    selectedPlayer=[i==player-1 and 1 or 0 for i in range(2)]

    # Tell AI which turn we're on       (81)
    selectedTurn=[i==turn and 1 or 0 for i in range(81)]

    # Tell AI who owns every cell       (162)
    ownedCells=[cell==player and 1 or 0 for cell in game.board]
    enemyCells=[cell==enemy and 1 or 0 for cell in game.board]

    # Tell AI the state of every grid   (27)
    ownedGrids=[grid==player and 1 or 0 for grid in game.grid]
    enemyGrids=[grid==enemy and 1 or 0 for grid in game.grid]
    fullGrids=[grid==-1 and 1 or 0 for grid in game.grid]

    # Tell AI where it can play         (81)
    accessibleCells=[game.canPlay(*getpos(i)) and 1 or 0 for i in range(81)]

    # Merge all the data in a list      (353)
    return selectedPlayer+selectedTurn+ownedCells+enemyCells+ownedGrids+enemyGrids+fullGrids+accessibleCells

class Morpx:
    def __init__(self):
        self.board=[0 for i in range(81)]
        self.grid=[0 for i in range(9)]
        self.used=[0 for i in range(9)]
        self.ended=0
        self.lastX=-1
        self.lastY=-1

    def set(self, x, y, x2, y2, value):
        self.lastX=x2
        self.lastY=y2
        self.board[x+3*y+9*x2+27*y2]=value
        self.used[x+3*y]+=1
        hasBig=False
        if self.get(x, y, 0, y2)==self.get(x, y, 1, y2) and self.get(x, y, 1, y2)==self.get(x, y, 2, y2):
            hasBig=True
        if self.get(x, y, x2, 0)==self.get(x, y, x2, 1) and self.get(x, y, x2, 1)==self.get(x, y, x2, 2):
            hasBig=True
        if x2==y2 and self.get(x, y, 0, 0)==self.get(x, y, 1, 1) and self.get(x, y, 1, 1)==self.get(x, y, 2, 2):
            hasBig=True
        if x2==2-y2 and self.get(x, y, 0, 2)==self.get(x, y, 1, 1) and self.get(x, y, 1, 1)==self.get(x, y, 2, 0):
            hasBig=True
        if hasBig:
            self.setB(x, y, value)
        elif self.used[x+3*y]==9:
            self.grid[x+3*y]=-1
        if self.ended==0:
            ended=True
            for e in self.grid:
                if e==0:
                    ended=False
                    break
            if ended:
                self.ended=-1
    def get(self, x, y, x2, y2):
        return self.board[x+3*y+9*x2+27*y2]
    
    def setB(self, x, y, value):
        self.grid[x+3*y]=value
        hasWin=False
        if self.getB(x, 0)==self.getB(x, 1) and self.getB(x, 1)==self.getB(x, 2):
            hasWin=True
        if self.getB(0, y)==self.getB(1, y) and self.getB(1, y)==self.getB(2, y):
            hasWin=True
        if x==y and self.getB(0, 0)==self.getB(1, 1) and self.getB(1, 1)==self.getB(2, 2):
            hasWin=True
        if x==2-y and self.getB(0, 2)==self.getB(1, 1) and self.getB(1, 1)==self.getB(2, 0):
            hasWin=True
        if hasWin:
            self.ended=value
    def getB(self, x, y):
        return self.board[x+3*y]

    def canPlay(self, x, y, x2, y2):
        if self.lastX==-1:
            return True
        if self.get(x, y, x2, y2):
            return False
        if self.getB(self.lastX, self.lastY)==0:
            return x==self.lastX and y==self.lastY
        return True
    
    @classmethod
    def gamefn(Morpx, n1, n2):
        n1.reset()
        n2.reset()
        game=Morpx()
        player=1
        turn=0
        while game.ended==0:
            net=n1 if player==1 else n2
            rst=net.activate(getNNList(game, player, turn))
            guesses=sortedindexes(rst)
            hasPlayed, i=False, 0
            while not hasPlayed:
                x, y, x2, y2=getpos(guesses[i])
                if game.canPlay(x, y, x2, y2):
                    game.set(x, y, x2, y2, player)
                    hasPlayed=True
                i+=1
            player=2 if player==1 else 1
            turn+=1
        return game.ended
