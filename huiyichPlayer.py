#Huiyi Chen (huiyich@bu.edu)
#U93791434
#CS440 PA3
#AI Player for Atropos Game
#April 27, 2017


import sys
# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
msg = "Given board " + sys.argv[1] + "\n";
sys.stderr.write(msg);

#parse the input string, i.e., argv[1]
s = sys.argv[1]
#s ="[13][302][1003][30002][100003][3000002][10000003][300000002][12121212]LastPlay:null"
(initBoard, lastPlay) = s.split("LastPlay:")

if lastPlay != "null":
	lastPlay = lastPlay[1:]
	lastPlay = lastPlay[:-1]
	lastPlay = lastPlay.split(",")
	lastPlay = [int(i) for i in lastPlay]
   
board = []
row = []
for char in initBoard:
	if char  == '[':
		row = []
	elif char == ']':
		board.append(row)
	else:
		row.append(int(char))
board.reverse()
		


#perform intelligent search to determine the next move
		
#define colors
UNCOLORED = 0
RED = 1
BLUE = 2
GREEN = 3
 
#define size
SIZE = len(board)-2
          
#define depth
DEPTH = 5

positiveNum = 1000
negativeNum = -1000

#find adjacent position clockwise
def adj(board, lastPlay):
    adj = []
    height = lastPlay[1]
    right = lastPlay[2]
    
    if height > 1:
        adj = [(height+1, right -1), (height+1, right), (height, right+1), (height-1, right+1), (height-1, right), (height, right-1)]
    else:
        adj = [(height+1, right -1), (height+1, right), (height, right+1), (height-1, right), (height-1, right-1), (height, right-1)]

    return adj

#decide whether a move will lose the game            
def gameover(board, move):
    color = move[0]
    adjList = adj(board, move)
    
    for i, (h, r) in enumerate(adjList):
        colors = [color]
        if board[h][r] != 0:
            colors.append(board[h][r])
        (H, R) = adjList[(i+1) % len(adjList)]
        if board[H][R] != 0:
            colors.append(board[H][R])
        if len(set(colors)) == 3:
            return True
    return False

#find all available moves
def availableMoves(board, lastPlay):
    adjList = adj(board, lastPlay)
    avails = []
    for (h, r) in adjList:
        if board[h][r] == 0:
            avails.append((h, r))
    if avails == []:
        for irow, row in enumerate(board):
            for icol, circle in enumerate(row):
                if circle == 0:
                    avails.append((irow, icol))
    return avails

        
#the static evaluator
def evaluator(board, move):
    if (gameover(board, move)):
        return (negativeNum, [])
    
    score = 0
    
    #get 5 points for each adj with color
    #get 2 points for each pair of adj that have the same color
    #subtract 1 points for each adj that have the same color with move itself
    adjList = adj(board, move)
    color = move[0]
    for i,  (h, r) in enumerate(adjList):
        fill = board[h][r]
        if fill != 0:
            score += 10
            if fill == color:
                score -= 1
            (H, R) = adjList[(1+i) % len(adjList)]
            if fill != board[H][R]:
                score += 5
    return (score, move)
    

#use minimax with alpha beta pruning to search best move
def alphaBeta(board, lastPlay, depth, alpha, beta, isMax):
    #if it is the first move, play it in the top of board
    if lastPlay == "null":
        return (0, [3, SIZE, 1, 1])
    
    if depth == 0 or gameover(board, lastPlay):
        return evaluator(board, lastPlay)
    else:
        nodes = availableMoves(board, lastPlay)
        if isMax:
            score = (negativeNum, [])
            for (h, r) in nodes:
                for color in range(1, 4):
                    board[h][r] = color
                    move = [color, h, r, SIZE+2-h-r]
                    nodeScore = alphaBeta(board, move, depth-1, alpha, beta, False)
                    board[h][r] = 0
                    if nodeScore[0] >= score[0]:
                        score = (nodeScore[0], move)
                    if score[0] > alpha:
                        alpha = score[0]
                    if beta <= alpha:
                        break
            
        else:
            score = (positiveNum, [])
            
            for (h, r) in nodes:
                for color in range(1, 4):
                    board[h][r] = color
                    move = [color, h, r, SIZE+2-h-r]
                    nodeScore = alphaBeta(board, move, depth-1, alpha, beta, True)
                    board[h][r] = 0
                    if nodeScore[0] >= score[0]:
                        score = (nodeScore[0], move)
                    if score[0] < beta:
                        beta = score[0]
                    if beta <= alpha:
                        break
            
    return score


#find best move
bestMove = alphaBeta(board, lastPlay, DEPTH, negativeNum, positiveNum, True)
nextMove = map(str, bestMove[1])
makeMove = ",".join(nextMove)
        
        
        
        
        
        
#print to stdout for AtroposGame
sys.stdout.write("(" + makeMove + ")");

