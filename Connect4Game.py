import random
import copy as cp

class Connect4Game:
    def __init__(self):
        self.board = [[0 for col in range(7)] for row in range(6)]
        self.turn = 1
        self.p1Score = 0
        self.p2Score = 0
        self.piecesPlayed = 0
        self.gameFile = None
        self.searchDepth = 42
        random.seed()

    def updatePieceCount(self):
        self.piecesPlayed = self.getPieceCount(self.board)

    def printBoard(self):
        print('---------')
        for row in range(6):
            print('|' + ''.join([str(c) for c in self.board[row]]) + '|')
        print('---------')
    
    def writeBoardToFile(self, fout):
        fout = open(fout, 'w')
        for row in range(6):
            fout.write(''.join([str(c) for c in self.board[row]]) + '\n')
        fout.write(str(self.turn))

    def playPiece(self, col, board=None, player = None, searching=False):
        if not board:
            board = self.board
        if not player:
            player = self.turn
        #too many pieces
        if self.getPieceCount(board) == 42:
            if not searching:
                return False
            else:
                return (False, board)
        if col < 0 or col > 6:
            if not searching:
                return False
            else:
                return (False, board)
        #there is an opening
        if board[0][col] == 0:
            row = 5
            while not board[row][col] == 0:
                row -= 1
            board[row][col] = player
            if not searching:
                self.piecesPlayed += 1
                self.turn = 1 if player == 2 else 2
                return True
            else:
                return (True, board)
        #invalid play
        else:
            if not searching:
                return False
            else:
                return (False, board)

    def playPieceAI(self, method='random', depth=None):
        
        if method == 'random':
            possible = [i for i in range(7)]
            col = random.choice(possible)
            
            while not self.playPiece(col):
                possible.remove(col)
                col = random.choice(possible)

            if len(possible) == 0:
                    return False
            return True

        if method == 'minimax':
            search_board = cp.deepcopy(self.board)
            if self.turn == 2:
                best_val = self.find_max(search_board, self.turn, final=True)
            else:
                best_val = self.find_min(search_board, self.turn, final=True)
            self.playPiece(best_val) 
        
        if method == 'alpha-beta':
            search_board = cp.deepcopy(self.board)
            alpha = -float('inf')
            beta = float('inf')
            if self.turn == 2:
                best_val = self.find_max_AB(search_board, self.turn, alpha, beta, final=True)
            else:
                best_val = self.find_min_AB(search_board, self.turn, alpha, beta, final=True)
            self.playPiece(best_val) 

    def find_max_AB(self, board, player, alpha, beta, final=False):
        
        if self.getPieceCount(board) == self.searchDepth:
            scores = self.calcScore(board, searching=True)
            score =  scores[1] - scores[0]
            return score

        best_val = (-1, -float('inf'))
        
        successors = []
        choices = [0,1,2,3,4,5,6]
        random.shuffle(choices)
        for i in choices:
            search_board = cp.deepcopy(board)
            new_state = self.playPiece(i, search_board, player, searching=True)
            if new_state[0]:
                best_val = max(best_val,(i, self.find_min_AB(new_state[1],\
                                                          1 if player == 2 else 2,\
                                                          alpha, beta)),
                                                          key = lambda x: x[1])
                if best_val[1] >= beta:
                    if final:
                        return best_val[0]
                    else:
                        return best_val[1]
          
                alpha = max(alpha, best_val[1])

        if final:
            return best_val[0]
        else:
            return best_val[1]
        
    def find_min_AB(self, board, player, alpha, beta, final=False):

        if self.getPieceCount(board) == self.searchDepth:
            scores = self.calcScore(board, searching=True)
            score = scores[1] - scores[0]
            return score
       
        best_val = (-1, float('inf'))

        successors = []
        choices = [0,1,2,3,4,5,6]
        random.shuffle(choices)
        for i in choices:
            search_board = cp.deepcopy(board)
            new_state = self.playPiece(i, search_board, player, searching=True)
            if new_state[0]:
                best_val = min(best_val,(i, self.find_max_AB(new_state[1],\
                                                          1 if player == 2 else 2,\
                                                          alpha, beta)),
                                                          key = lambda x: x[1])
                if best_val[1] <= alpha:
                    if final:
                        return best_val[0]
                    else:
                        return best_val[1]
          
                beta = min(beta, best_val[1])

        if final:
            return best_val[0]
        else:
            return best_val[1]

    def find_max(self, board, player, final=False):
        
        if self.getPieceCount(board) == self.searchDepth:
            scores = self.calcScore(board, searching=True)
            score =  scores[1] - scores[0]
            return score

        successors = []
        choices = [0,1,2,3,4,5,6]
        random.shuffle(choices)
        for i in choices:
            search_board = cp.deepcopy(board)
            new_state = self.playPiece(i, search_board, player, searching=True)
            if new_state[0]:
                successors.append((i, self.find_min(new_state[1],\
                                                    1 if player == 2 else 2)))
        best_val = max(successors, key=lambda x: x[1])
        
        #print ("MAX: " + str(best_val[1]))
        if final:
            return best_val[0]
        else:
            return best_val[1]
        
    def find_min(self, board, player, final=False):

        if self.getPieceCount(board) == self.searchDepth:
            scores = self.calcScore(board, searching=True)
            score = scores[1] - scores[0]
            return score
    
        successors = []
        choices = [0,1,2,3,4,5,6]
        random.shuffle(choices)
        for i in choices:
            search_board = cp.deepcopy(board)
            new_state = self.playPiece(i, search_board, player, searching=True)
            if new_state[0]:
                successors.append((i, self.find_max(new_state[1],\
                                                    1 if player == 2 else 2)))
        best_val = min(successors, key=lambda x: x[1])
        #print ("Min: " + str(best_val[1]))
        if final:
            return best_val[0]
        else:
            return best_val[1]

    def getPieceCount(self, board):
        p = 0
        for row in range(6):
            for col in range(7):
                if not board[row][col] == 0:
                    p += 1
        return p

    def calcScore(self, board=None, searching=False):
        if not board:
            board = self.board
        score1 = 0
        score2 = 0
        four1 = [1]*4
        four2 = [2]*4
        #horizontal
        for row in board:
            for i in range(4):
                if row[i:i+4] == four1:
                    score1 += 1
                elif row[i:i+4] == four2:
                    score2 += 1
        #vertical
        for j in range(7):
            col = [row[j] for row in board]
            for i in range(3):
                if col[i:i+4] == four1:
                    score1 += 1
                elif col[i:i+4] == four2:
                    score2 += 1
        #diagonal
        for c in range(4):
            for r in range(3):
                bl_tr = [board[r+3-i][c+i] for i in range(4)]
                tl_br = [board[r+i][c+i] for i in range(4)]
                if bl_tr == four1:
                    score1 += 1
                elif bl_tr == four2:
                    score2 += 1
                if tl_br == four1:
                    score1 += 1
                elif tl_br == four2:
                    score2 += 1
        
        if not searching:
            self.p1Score = score1
            self.p2Score = score2
        else:
            return (score1, score2)
