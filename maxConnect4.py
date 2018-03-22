import sys
from Connect4Game import *
import time

def displayGame(game):
    game.printBoard()
    game.calcScore()
    print('Player 1 Score: ' + str(game.p1Score))
    print('Player 2 Score: ' + str(game.p2Score))

def interactive(game, method, depth):
    game.searchDepth = min(42, game.getPieceCount(game.board) + depth)
    while game.piecesPlayed < 42:
        displayGame(game)
        if game.turn == 1:
            '''
            valid = False
            while not valid:
                play = input('Place Piece(1-7): ')
                valid = game.playPiece(play-1)
                if not valid:
                    print ("Invalid move, pick again!")
            '''
            game.playPieceAI('random', depth)
            game.writeBoardToFile('human.txt')
        else:
            print ("Waiting for AI...")
            game.playPieceAI(method, depth)
            game.writeBoardToFile('computer.txt')
        game.searchDepth = min(42, game.getPieceCount(game.board) + depth)
    displayGame(game)

def main(argv):
    #inputs
    if not len(argv) == 5:
        print("Invalid cmd line arguments")
        print("Use as: python " + argv[0] +\
              " {interactive,one-move} [input_file] [output_file] [depth]")
        sys.exit(-1)
    mode, fin = argv[1], argv[2]
    if mode not in ['interactive','one-move']:
        print("Unrecognized game mode: " + argv[1])
        sys.exit(-1)
    fileExists = False
    try:
        fin = open(fin, 'r')
        fileExists = True
    except IOError:
        print("File could not be opened: " + argv[2])
        if (mode == 'one-move'):
            sys.exit(-1)
        else:
            print('Loading empty board instead')
   
    #setup
    game = Connect4Game()
    data = []
    if fileExists:
        data = [[int(c) for c in line[0:-1]] for line in fin.readlines()]
        game.board = data[:-1]
    game.updatePieceCount()
    game.calcScore()
    depth = int(argv[4])
    
    #interactive game
    if mode == 'interactive':
        if argv[3] not in ['computer-next','human-next']:
            print('Unrecognized player command: ' + argv[3])
            sys.exit(-1)
        game.turn = 1 if argv[3] == 'human-next' else 2
        interactive(game, 'alpha-beta', depth)

    elif mode == 'one-move':
        fout = argv[3]
        game.turn = int(data[-1][0])
        game.searchDepth = min(42, game.getPieceCount(game.board) + depth)
        displayGame(game)
        game.playPieceAI('alpha-beta', depth)
        displayGame(game)
        game.writeBoardToFile(fout)

if __name__ == '__main__':
    main(sys.argv)
