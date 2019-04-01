""" Pig game - Week 8 Assignment """
import random
import sys
import os
import argparse
import time

class Player(object):
    """ A player object instantiates with a user provided name and score of 0 """
    def __init__(self):
        self.score = 0
        self.turn = False
        self.name = 'player'
        self.type = 'human'
        self.pendingPoints = 0

    def getScore(self):
        """ Getter to grab the score variable """
        return self.score

    def setScore(self, points):
        """ Score setter method """
        self.score += points

    def getName(self):
        """ Name getter """
        return self.name

    def setName(self):
        while True:
            try:
                newName = raw_input('Enter player name: ').strip()
                self.name = newName
            except ValueError:
                print('please enter a string')
                continue

    def setTurn(self, turn):
        """ Turn setter """
        self.turn = turn

    def getTurn(self):
        """ Turn getter """
        return self.turn

    def getType(self):
        return self.type

    def setPendingPoints(self, points):
        self.pendingPoints += points
    
    def resetPendingPoints(self):
        self.pendingPoints = 0

    def getPendingPoints(self):
        return self.pendingPoints

    def getChoice(self):
        while True:
            try:
                playerChoice = raw_input("Please enter [h] for hold, or [r] for roll: ").strip()
                if playerChoice.lower() == 'h':
                    return True
                elif playerChoice.lower() == 'r':
                    return False
            except:
                print('Invalid entry, please enter [h] for hold or [r] for roll')

class Computer(Player):
    """ Computer players have the player type of computer """
    def __init__(self):
        Player.__init__(self)
        self.type = 'computer'
        self.name = 'computer {}'.format(random.randint(1, 6))

    def getChoice(self):
        print self.getPendingPoints() >= 25
        print (int(self.getScore()) - 100) >= 25
        if int(self.getPendingPoints()) >= 25 or (int(self.getScore()) - 100) >= 25:
            return True
        else:
            return False
    


class PlayerFactory(object):
    """ Player Factory class - allows us to build players of computer or human types"""
    def playerType(self, type):
        if type == 'human':
            return Player()
        elif type == 'computer':
            return Computer()                

class Dice(object):
    """ Each dice object is initialized with a random seed of 0"""
    def __init__(self):
        self.value = random.seed(0)

    def roll(self):
        """ Each dice is six sided and can return integers between 1 and 6 """
        self.value = random.randint(1, 6)
        return self.value

    def getCurrentRoll(self):
        """ Getter method to grab the value variable """
        return self.value

class Game(object):
    """ The Game object holds the bulk of the work for the Pig game
    gameData holds the player objects
    pendingPoints show how many points are in the bucket to be consumed
    activePlayer is the player name that is currently rolling
    winner boolean determines if there is a winner of the game
    roll is the current roll
    dice is the dice object currently being used
    """
    def __init__(self):
        self.activePlayer = 0
        self.turns = 0
        self.dice = Dice()
        self.scoreData = {}
        self.gameData = []

    def addPlayer(self, ptype=str, index=int):
        """ Adds a new player to the gameData list, also updates the scoreData dictionary"""
        pf = PlayerFactory()
        if ptype == 'computer':
            self.gameData.append(pf.playerType("computer"))
            print index
            print self.gameData
            print self.gameData[index]
            self.scoreData[self.gameData[index].getName()] = self.gameData[index].getScore()
        elif ptype == 'human':
            self.gameData.append(pf.playerType("human"))
            print index
            print self.gameData
            print self.gameData[index]
            self.scoreData[self.gameData[index].getName()] = self.gameData[index].getScore()


    def addPlayersToGame(self, players):
        """ Adds a multiple of players to the game """
        for player in range(players):
            self.addPlayer(player)

    def getActivePlayer(self):
        """ Getter method to pull player objects """
        return self.gameData[self.activePlayer]

    def getWinState(self):
        """
        Checks player scores in the active player objects, if any of the scores are
        above 100, it returns True.
        Otherwise the function returns False.
        The Truth/False values directly correlate to the while statements which run the
        gameLoop
        """
        for player in self.gameData:
            if player.getScore() >= 100:
                return True
        return False

    def getGameStatus(self):
        """ Print functions - builds the game board, prints current status"""
        os.system('cls')
        print('====   Pig Game   ====\n')
        print('{:15} : {:>6}\n').format('Player', 'Score')
        for player in self.gameData:
            print('{:15} : {:6} \n').format(player.getName(), player.getScore())
        print('{} is rolling').format(self.getActivePlayer().getName())
        if self.dice.getCurrentRoll() == 1:
            print('The last roll was {}, next player\'s turn!').format(self.dice.getCurrentRoll())
        else:
            print('The last roll was {}').format(self.dice.getCurrentRoll())
        print('Pending Points: {:>10}').format(self.getActivePlayer().getPendingPoints())

    def playerTurn(self):
        """ Interactive player turn, asks for user input about whether they want
        to roll or hold.
        Depending on the outcome of the roll, the loop will either exit due to
        a player rolling 1 or if the player has over 100 points """
        rolling = self.getActivePlayer()
        rolling.setTurn(True)
        self.getGameStatus()
        while rolling.getTurn() and not self.getWinState():
            rollorhold = rolling.getChoice()
            if rollorhold:
                rolling.setScore(rolling.getPendingPoints())
                rolling.resetPendingPoints()
                rolling.setTurn(False)
            else:
                roll = self.dice.roll()
                if roll == 1:
                    rolling.resetPendingPoints()
                    rolling.setTurn(False)
                rolling.setPendingPoints(roll)
                self.getGameStatus()
                continue

    def gameLoop(self, player1, player2, numPlayers=2):
        """
        The game loop sets up the players in the game, and builds out a turn
        order for the players.  Once the win state is reached, the function allows for
        a game restart with user input.

        Args:
            players (optional): Number of players in the game - defaults to 2
            player1 (string): 
        """
        if numPlayers <= 2:
            print 'in first if'
            print numPlayers
            self.addPlayer(player1, 0)
            self.addPlayer(player2, 1)
            print self.gameData
        elif numPlayers > 2:
            for player in range(2, numPlayers):
                self.addPlayersToGame(player)

        while not self.getWinState():
            for player in self.gameData:
                print 'in for loop'
                self.activePlayer = (self.turns % len(self.gameData))
                self.playerTurn()
                print self.getActivePlayer().getName()
                self.turns += 1

        # New win state formula
        scores=list(self.scoreData.values())
        players=list(self.scoreData.keys())
        topScore = max(scores)
        winner = players[scores.index(max(scores))]
        print('\nWe have a winner! {} is the winner with {}').format(winner, topScore)
        while True:
            try:
                newGame = raw_input("\nPlay again? [y]|[n]: ")
                if newGame == 'y':
                    try:
                        newGamePlayers = int(raw_input("\nEnter number of players in this game: "))
                        self.resetGame()
                        self.gameLoop(newGamePlayers,'human', 'computer')
                    except ValueError:
                        print('Invalid Input, running game with default of 2 players')
                        continue
                    finally:
                        self.resetGame()
                        self.gameLoop(2,'human', 'computer')
                elif newGame == 'n':
                    print('Thanks for playing! Goodbye!')
                    sys.exit()
            finally:
                print('Invalid entry')

    def resetGame(self):
        """ Re-initializes game variables for a fresh start """
        self.activePlayer = 0
        self.turns = 0
        self.dice = Dice()
        self.scoreData = {}
        self.gameData = []


class TimedGameProxy(Game):
    def __init__(self):
        Game.__init__(self)
        self.start_time = time.time()
        self.end_time = time.time() + 60
    
    def getWinState(self):
        if time.time() == self.end_time:
            return True
        for player in self.gameData:
            if player.getScore() >= 100:
                return True
        return False


def main():
    """ Main method to run our game

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--numPlayers',
                        help='Number of players in our game',
                        type=int, required=False, default=2)
    parser.add_argument('--player1', type=str, choices=['human','computer'], default='computer', required=False)
    parser.add_argument('--player2', type=str, choices=['human','computer'], default='computer', required=False)
    parser.add_argument('--timed', help='Determine if the game is timed', required=False, default=False)
    args = parser.parse_args()
    if args.timed == True:
        newGame = TimedGameProxy()
    elif args.timed == False:
        newGame = Game()
    newGame.gameLoop(args.player1, args.player2, args.numPlayers)

if __name__ == '__main__':
    main()
