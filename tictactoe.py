
# Tic Tac Toe
# Author: Robert Meyer
# Conctat: (415) 350-0809
# Email: robertnmeyer@hotmail.com
# Date: November 7, 2010

from random import choice


#
# Square is a box on the tic tac toe board.  There are nine per board.
# The class uses internal methods to set an X or O as the square's content.
# Each square's num represents its position on the grid.
#
# @params: none
# @returns: none
#------------------------------------------------------------------------------
class Square():
    num = 0
    content = ' '

    def __init__(self, number):
        self.num = number
        self.content = ' '


    def is_available(self):
        if (self.content == ' '):
            return True
        else:
            return False


    def setX(self):
        if (self.is_available()):
            self.content = 'X'
            return True
        else:
            print '*****That grid is already taken.*****'


    def setO(self):
        if (self.is_available()):
            self.content = 'O'
            return True
        else:
            print '*****That grid is already taken.*****'


    def __repr__(self):
        print str(self.content)
#------------------------------------------------------------------------------   



#
# Board represents the game board, and is comprised of nine grid objects.
#
# @params: none
# @returns: @winner as string ("X" or "O")
#------------------------------------------------------------------------------ 
class Board():
    grid = []
    winningPatterns = ''
    CORNERS = ''
    SIDES = ''    
    CENTER = ''

    def __init__(self,):
        self.winningPatterns = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), \
                                (1,4,7), (2,5,8), (0,4,8), (6,4,2)]
        self.CORNERS = [0,2,6,8]
        self.SIDES = [1,3,5,7]
        self.CENTER = 4
        self.grid = []        
        
        i = 0
        for i in range(0,9):
            self.grid.append(Square(i))


    def display(self,):
        i = 1
        board = ''
                 
        for s in self.grid:
            if (i==1):
                board = '\n' +  ' 0 | 1 | 2 \t'
            elif (i==4):
                board = board + ' 3 | 4 | 5 \t'
            elif (i==7):
                board = board + ' 6 | 7 | 8 \t'
                
            board = board + ' ' + str(s.content) + ' '
            if (i < 8 and i % 3 == 0):
                board = board + '\n' + ('-'*10) + '\t' + ('-'*10) + '\n'
            elif i < 9:
                board= board + '|'

            i = i + 1

        board = board + '\n'
        print board


    def has_winner(self,):
        grid = self.grid
        winner = 'none'

        for pat in self.winningPatterns:
            if(grid[pat[0]].content == 'X' or grid[pat[0]].content =='O'):
                if(grid[pat[0]].content == grid[pat[1]].content and \
                   grid[pat[0]].content == grid[pat[2]].content):
                    winner = grid[pat[0]].content

        return winner
#------------------------------------------------------------------------------ 



#
# ComputerPlayer is the opponent, and always plays O.  The computer can make
# several moves: an opening move, a winning move, a blocking move, a tactical
# move based on scenarios, and random moves.  The various moves are handled
# by the method make_move().
#
# @params: b is the Board which the ComputerPlayer uses to calculate a move
# @returns: @movePiece as string with values 'none' or the grid's index
# 
#------------------------------------------------------------------------------ 
class ComputerPlayer():
    def has_opening(self, b):
        '''
        Opening strategy is take the center grid if possible, else a corner.
        '''
        movePiece = 'none'
        if b.grid[b.CENTER].is_available():
            movePiece = b.grid[b.CENTER].num
        else:
            movePiece = choice(b.CORNERS)

        return movePiece

            
    def has_win(self, b):
        '''
        @b (gameboard) has 8 winning patterns of three squares each.
        If O has two of the squares in any of the patterns, and the third is
        is available, then return the index of the winning square.
        '''
        isMoveFound = False
        movePiece = 'none'
        countO = 0
        
        for pattern in b.winningPatterns:
            if(isMoveFound==False):
                countO = 0
                for index in pattern:
                    if b.grid[index].content == 'O':
                        countO = countO + 1
                        
                if(countO == 2):
                    for index in pattern:
                        if b.grid[index].is_available():
                            movePiece = b.grid[index].num
                            isMoveFound = True

        return movePiece
    
        
    def has_block(self, b):
        '''
        b (gameboard) has 8 winning patterns of three squares each.
        If X (the player) has two of the squares in any of the patterns, and the
        third is available, then return the index of the square to be blocked.
        '''        
        isMoveFound = False
        movePiece = 'none'
        countX = 0

        for pattern in b.winningPatterns:
            if (isMoveFound==False):
                countX = 0
                
                for index in pattern:
                    if (b.grid[index].content == 'X'):
                        countX = countX + 1

                if (countX == 2):
                    for index in pattern:
                        if b.grid[index].is_available():
                            movePiece = b.grid[index].num
                            isMoveFound = True
                            
        return movePiece


    def has_tactic(self, b):
        '''
        has_tactic() looks at three common scenarios that occur in the second
        round that may lead to a player win, and then returns the counter move.
        '''
        isMoveFound = False
        movePiece = 'none'
        corners = {0:0, 2:0, 6:0, 8:0}  # mutable version of grid's corners
        
        '''
        The first tactic to counter is when O has the center and X has two
        corners diagonal from each other.  O must choose a side (non-corner)
        to prevent X from winning in two moves.  The corner pairs to check
        are (0,8) and (6,2).
        '''
        if(isMoveFound==False and b.grid[b.CENTER].content=='O'):
            if ((b.grid[0].content == b.grid[8].content and \
                 b.grid[0].content == 'X') or \
                (b.grid[6].content == b.grid[2].content and \
                 b.grid[6].content == 'X')):
                movePiece = choice(b.SIDES)
                isMoveFound = True

        '''
        The second tactic to counter is when O has the center and there are X's
        in two seperate patterns that share an available corner.  The available
        corner must be filled by O or else X will win in two moves.
        '''
        if(isMoveFound==False and b.grid[b.CENTER].content=='O'):
            activePatterns = []

            '''
            Limit calculations to those with an x but without an o, and add
            them to the list of activePatterns.  
            '''
            for pattern in b.winningPatterns:
                countO = 0
                countX = 0
                for index in pattern:
                    if b.grid[index].content == 'O':
                        countO = countO + 1
                    elif (b.grid[index].content == 'X'):
                        countX = countX + 1

                if (countX >= 1 and countO == 0):
                    activePatterns.append(pattern)

            '''
            Tally the corners to find the corner common to the most patterns
            '''
            for pattern in activePatterns:
                for index in pattern:
                    if index in corners:
                        corners[index] = corners[index] + 1
                        
            '''
            Select the corner that is in at least two patterns and if available.
            '''
            for k,v in corners.items():
                if v > 1:
                    if b.grid[k].is_available():
                        movePiece = k
                        isMoveFound = True

        '''
        The final tactic to counter is when X has the center, O takes a corner,
        and then X takes corner diagonal from O (does not threaten a win).
        O must take a remaining corner to threaten win and then draw.
        '''
        if(isMoveFound==False and b.grid[b.CENTER].content=='X'):
            for c in b.CORNERS:
                if b.grid[c].is_available():
                    movePiece = c
                    isMoveFound = True

        return movePiece

        
    def make_move(self, b, moves):
        '''
        @params: b as the Board, moves as integer for the number of moves made
        @returns: movePiece as integer with value of the Squares index on the grid
        '''
        isChoosingMove = True
        movePiece = ''

        '''
        Opening round
        '''
        if (moves == 2):
            movePiece = self.has_opening(b)
            if(movePiece != 'none'):
                isChoosingMove = False

        '''
        For remaining rounds, check for wins, check for blocks.  Note that the
        method has_tactic is only called during the second round, but is ordered
        after wins and blocks because the computer might have to block immediately
        before countering a more strategic move.
        '''
        if (isChoosingMove):
            movePiece = self.has_win(b)
            if(movePiece != 'none'):
                isChoosingMove = False
                
        if (isChoosingMove):
            movePiece = self.has_block(b)
            if(movePiece != 'none'):
                isChoosingMove = False

        if (isChoosingMove and moves == 4):
            movePiece = self.has_tactic(b)
            if (movePiece != 'none'):
                isChoosingMove = False

        # If no win, block, or tactical move, play a random square
        while (isChoosingMove):
            movePiece= choice([0,1,2,3,4,5,6,7,8])
            if (b.grid[movePiece].is_available()):
                isChoosingMove = False

        return int(movePiece)
        
# end Class ComputerPlayer ---------------------------------------------------- 



#
# Game determines whose turn it is, the number of moves, input from the user,
# input from the computer player, and when the game is over.
#
# @params: none
# @returns: none
#------------------------------------------------------------------------------ 
class Game():
    isPlayersTurn = True
    isGameOver = False
    moves = 1    
    b = ''                                 # gameboard (grid of x's and o's)
    ai = ''
    
    def __init__(self,):
        self.moves = 1
        self.isPlayersTurn = True
        self.isGameOver = False
        self.b = Board()
        self.ai = ComputerPlayer()
                
    def run(self,):
        moves = self.moves
        isPlayersTurn = self.isPlayersTurn
        isGameOver = self.isGameOver
        b = self.b
        ai = self.ai
        
        while(isGameOver != True):
            b.display()
            
            if (isPlayersTurn):
                prompt = 'Player X, Choose a square: '
                command = raw_input(prompt)
            else:
                print 'The computer is making a move...'
            
            if command.lower() == 'q':
                isGameOver = True
                
            else:
                try:
                    if (isPlayersTurn):
                        if(b.grid[int(command)].setX()):
                            isPlayersTurn = False
                            moves = moves + 1
                    else:
                        ai_command = ai.make_move(b, moves)
                        if(b.grid[int(ai_command)].setO()):
                            isPlayersTurn = True
                            moves = moves + 1

                except ValueError:
                    print '\n***Please enter a number between 0 and 8.***'
                except IndexError:
                    print '\n***Please select a square between 0 and 8***'
                finally:
                    pass

            if (moves > 9 or b.has_winner() != 'none'):
                isGameOver = True

        # display game results
        b.display()

        if b.has_winner() == 'none':
            print 'Draw Game.'
        else:
            print 'The winner is Player %s.' % b.has_winner().upper()
#------------------------------------------------------------------------------         



#
# main() activates the game
#------------------------------------------------------------------------------ 
def main():
    QUIT = False
    while (QUIT == False):
        print ('\nWelcome to Tic-Tac-Toe\nEnjoy your game.  Press q to quit.')
        g = Game()
        g.run()

        command = raw_input('\nPlay again (y/n)? ')
        if(command.lower() == 'n' or command.lower() == 'q'):
            QUIT = True
           
#------------------------------------------------------------------------------ 


#---- start tic-tac-toe
            
main()

#---- end...

