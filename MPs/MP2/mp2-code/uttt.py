from time import sleep
from math import inf
from random import randint


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.maxDepth = 3
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        # self.startBoardIdx=randint(0,8)

        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.cornerMaxUtility = 30

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.cornerMinUtility = -30

        self.expandedNodes = 0
        self.currPlayer = True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]]) + '\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]]) + '\n')

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        score = 0
        # the following score is used to record possible rules
        first_score = 0
        second_score = 0
        third_score = 0

        # the local helper function to find the score
        def score_find(b, t, od):
            s1, s2, s3 = 0, 0, 0
            if od:
                ot = "O"
            else:
                ot = "X"

            # starting with score 1
            
            rowcond = (b[0][0] == t and b[0][1] == t and b[0][2] == t) or (
                        b[1][0] == t and b[1][1] == t and b[1][2] == t) or (
                            b[2][0] == t and b[2][1] == 0 and b[2][2] == t)
            columncond = (b[0][0] == t and b[1][0] == t and b[2][0] == t) or (
                        b[0][1] == t and b[1][1] == t and b[2][1] == t) or (
                            b[0][2] == t and b[1][2] == 0 and b[2][2] == t)
            diagcond = (b[0][0] == t and b[1][1] == t and b[2][2] == t) or (
                        b[2][0] == t and b[1][1] == t and b[0][2] == t)

            if rowcond or columncond or diagcond:
                s1 = 10000
                return s1, s2, s3

            # now starting score 2
            # first row:
            if b[0][0]==t and b[0][1]==t:
                # while attack:
                if b[0][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][0]==t and b[0][2]==t:
                # while attack:
                if b[0][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][1]==t and b[0][2]==t:
                # while attack:
                if b[0][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            # second row
            if b[1][0]==t and b[1][1]==t:
                # while attack:
                if b[1][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][1]==t and b[1][2]==t:
                # while attack:
                if b[1][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][0]==t and b[1][2]==t:
                # while attack:
                if b[1][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            # third row
            if b[2][0]==t and b[2][1]==t:
                # while attack:
                if b[2][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[2][1]==t and b[2][2]==t:
                # while attack:
                if b[2][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[2][0]==t and b[2][2]==t:
                # while attack:
                if b[2][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od

            # first column
            if b[0][0]==t and b[1][0]==t:
                # while attack:
                if b[2][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][0]==t and b[2][0]==t:
                # while attack:
                if b[1][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][0]==t and b[2][0]==t:
                # while attack:
                if b[0][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            # second column
            if b[0][1]==t and b[1][1]==t:
                # while attack:
                if b[2][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][1]==t and b[2][1]==t:
                # while attack:
                if b[1][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][1]==t and b[2][1]==t:
                # while attack:
                if b[0][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            # third column
            if b[0][2]==t and b[1][2]==t:
                # while attack:
                if b[2][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][2]==t and b[2][2]==t:
                # while attack:
                if b[1][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][2]==t and b[2][2]==t:
                # while attack:
                if b[0][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od

            # diag condition
            if b[0][0]==t and b[1][1]==t:
                # while attack:
                if b[2][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][0]==t and b[2][2]==t:
                # while attack:
                if b[1][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[1][1]==t and b[2][2]==t:
                # while attack:
                if b[0][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od

            if b[2][0]==t and b[1][1]==t:
                # while attack:
                if b[0][2] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][2]==t and b[1][1]==t:
                # while attack:
                if b[2][0] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od
            if b[0][2]==t and b[2][0]==t:
                # while attack:
                if b[1][1] == ot:
                    s2 += 500 - 400*od
                else:
                    s2 += 100 + 400*od

            if s2 > 0:
                return 0, s2, 0

            # now starting score 3
            if b[0][0] == t:
                s3 += 30
            if b[0][2] == t:
                s3 += 30
            if b[2][0] == t:
                s3 += 30
            if b[2][2] == t:
                s3 += 30

            return 0, 0, s3

        if isMax:
            target = "X"
            od = 1  # offensive or defensive
        else:
            target = "O"
            od = 0

        for loc_idx in range(len(self.globalIdx)):
            # the offset for global place and get the local board
            ioff, joff = self.globalIdx[loc_idx][0], self.globalIdx[loc_idx][1]
            loc_board = [m[joff:joff+3] for m in self.board[ioff:ioff+3]]
            # print(ioff,joff)
            # print(self.board)
            # print(loc_board)
            temp1, temp2, temp3 = score_find(loc_board, target, od)
            first_score += temp1
            second_score += temp2
            third_score += temp3

            if first_score>0:
                score = temp1
            elif second_score>0:
                score = second_score
            else:
                score = third_score

        return score

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        score = 0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        # YOUR CODE HERE
        movesLeft = False

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '_':
                    movesLeft = True
                    break
            if movesLeft:
                break

        return movesLeft

    def checkWinner(self):
        # Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        # YOUR CODE HERE
        winner = 0

        for i in range(len(self.globalIdx)):
            temp_grade = self.evaluatePredifined(1)
            if temp_grade == 10000:
                return 1

            temp_grade = self.evaluatePredifined(0)
            if temp_grade == 10000:
                return -1

        return winner

    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        self.expandedNodes+=1
        if (depth == self.maxDepth)or (self.checkMovesLeft() == 0) or(self.checkWinner() != 0):
            return self.evaluatePredifined(not isMax)
        a,b=self.globalIdx[currBoardIdx]
        
        if isMax:
            bestValue=self.winnerMinUtility
            for i in range(3):
                for j in range(3):
                    if self.board[a+i][b+j] != '_':
                        continue
                    self.board[a+i][b+j] =self.maxPlayer
                    
                    bestValue=max(bestValue,self.alphabeta(depth+1, 3*j+i, alpha, beta, not isMax),alpha,beta)
                    self.board[a+i][b+j] ='_'
                    if  bestValue>= beta:
                        return bestValue
                    alpha=max(alpha,bestValue)
            # return bestValue
            
        else:
            bestValue=self.winnerMaxUtility
            for i in range(3):
                for j in range(3):
                    if self.board[a+i][b+j] != '_':
                        continue
                    self.board[a+i][b+j] =self.minPlayer
                    
                    bestValue=min(bestValue,self.alphabeta(depth+1, 3*j+i, alpha, beta, not isMax),alpha,beta)
                    self.board[a+i][b+j] ='_'
                    if  bestValue<= alpha:
                        return bestValue
                    beta=min(beta,bestValue)
            # return bestValue
            
            
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        self.expandedNodes+=1
        # YOUR CODE HERE
        if (depth == self.maxDepth)or (self.checkMovesLeft() == 0) or(self.checkWinner() != 0):
            return self.evaluatePredifined(not isMax)
        a,b=self.globalIdx[currBoardIdx]
        
        if isMax:
            bestValue=self.winnerMinUtility
            for i in range(3):
                for j in range(3):
                    if self.board[a+i][b+j] != '_':
                        continue
                    self.board[a+i][b+j] =self.maxPlayer
                    bestValue=max(bestValue,self.minimax(depth+1, 3*i+j, not isMax))
                    self.board[a+i][b+j] ='_'
        else:
            bestValue=self.winnerMaxUtility
            for i in range(3):
                    for j in range(3):
                        if self.board[a+i][b+j] != '_':
                            continue
                        self.board[a+i][b+j] =self.minPlayer
                        bestValue=min(bestValue,self.minimax(depth+1, 3*i+j, not isMax))
                        self.board[a+i][b+j] ='_'
            
                    
        return bestValue

    def playGamePredifinedAgent(self, maxFirst, isMinimaxOffensive, isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes=[]
        currIdx=self.startBoardIdx
        
        winner = 0
        
        self.currPlayer=maxFirst
        beta=self.winnerMaxUtility
        alpha=self.winnerMinUtility
        if self.currPlayer:
                bestvalue=self.winnerMinUtility
        else:
                bestvalue=self.winnerMaxUtility
        
        while(self.checkMovesLeft()==True) and (self.checkWinner()==0) :
        
            a,b=self.globalIdx[currIdx]
            if self.currPlayer:
                bestvalue=self.winnerMinUtility
            else:
                bestvalue=self.winnerMaxUtility
            for i in range(3):
                for j in range(3):
                    currIdx=i*3+j
                    if self.board[i+a][b+j]!='_':
                        continue
                    if self.currPlayer:
                        self.board[a+i][b+j] =self.maxPlayer
                        if isMinimaxOffensive:
                           curvalue=self.minimax(0,currIdx,not self.currPlayer)
                        else:
                           curvalue=self.alphabeta(0,currIdx,alpha,beta,not self.currPlayer)
                        print("curvalue",curvalue)
                        print("bestvalue",bestvalue)
                        if curvalue > bestvalue:
                            bestvalue=curvalue
                            bestmove=(a+i,b+j)
                            bestplayer=self.maxPlayer
                        
                            
                    else:
                        self.board[a+i][b+j] =self.minPlayer
                        if isMinimaxOffensive:
                            curvalue=self.minimax(0,currIdx,not self.currPlayer)
                        else:
                            curvalue=self.alphabeta(0,currIdx,alpha,beta,not self.currPlayer)
                        print("curvalue",curvalue)
                        print("bestvalue",bestvalue)
                        if curvalue < bestvalue:
                            bestvalue=curvalue
                            bestmove=(a+i,b+j)
                            bestplayer=self.minPlayer
                    self.board[a+i][b+j] = '_'
            self.board[bestmove[0]][bestmove[1]]=bestplayer
            gameBoards.append(self.board)
            expandedNodes.append(self.expandedNodes)
            self.expandedNodes=0
            bestMove.append(bestmove)
            bestValue.append(bestvalue)
            currIdx = (bestmove[0]%3)*3 + bestmove[1]%3
            self.currPlayer = not self.currPlayer
        winner = self.checkWinner()
            
        print(gameBoards, bestMove, expandedNodes, bestValue, winner)
        
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        winner = 0
        return gameBoards, bestMove, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        winner = 0
        return gameBoards, bestMove, winner


if __name__ == "__main__":
    uttt = ultimateTicTacToe()
    # feel free to write your own test code
    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(False, True, True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")