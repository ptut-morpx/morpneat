class TicTacToe:
    def __init__(self):
        self.board=[0 for i in range(9)]

    def get(self, x, y):
        return self.board[3*x+y]

    def set(self, x, y, v):
        if self.board[3*x+y]!=0:
            raise KeyError("cell already used")
        self.board[3*x+y]=v
    
    def result(self):
        for i in range(3):
            if self.board[3*i]!=0 and self.board[3*i]==self.board[3*i+1] and self.board[3*i]==self.board[3*i+2]:
                return self.board[3*i]
            if self.board[i]!=0 and self.board[i]==self.board[i+3] and self.board[i]==self.board[i+6]:
                return self.board[i]
            if self.board[0]!=0 and self.board[0]==self.board[4] and self.board[0]==self.board[8]:
                return self.board[0]
            if self.board[2]!=0 and self.board[2]==self.board[4] and self.board[2]==self.board[6]:
                return self.board[2]
        return 0

    def ended(self):
        for i in range(9):
            if self.board[i]==0:
                return False
        return True

