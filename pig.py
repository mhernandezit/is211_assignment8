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
        self.set_name()
        self.type = 'human'
        self.pending_points = 0

    def get_score(self):
        """ Getter to grab the score variable """
        return self.score

    def set_score(self, points):
        """ Score setter method """
        self.score += points

    def get_name(self):
        """ Name getter """
        return self.name

    def set_name(self):
        """ Name setter for humans - should ask player for their name """
        while True:
            try:
                new_name = raw_input('Enter player name: ').strip()
                self.name = new_name
                break
            except ValueError:
                print 'please enter a string'
                continue

    def set_turn(self, turn):
        """ Turn setter """
        self.turn = turn

    def get_turn(self):
        """ Turn getter """
        return self.turn

    def get_type(self):
        """ Return Player type - this will be a human type """
        return self.type

    def set_pending_points(self, points):
        """ Pending points setter """
        self.pending_points += points

    def reset_pending_points(self):
        """ On turn we need to set pending points to 0 """
        self.pending_points = 0

    def get_pending_points(self):
        """ Return active player's pending points """
        return self.pending_points

    def get_choice(self):
        """ Human's choice function, returns true if hold, false if roll """
        while True:
            try:
                player_choice = raw_input("Please enter [h] for hold, or [r] for roll: ").strip()
                if player_choice.lower() == 'h':
                    return True
                elif player_choice.lower() == 'r':
                    return False
            except ValueError:
                print 'Invalid entry, please enter [h] for hold or [r] for roll'

class Computer(Player):
    """ Computer players have the player type of computer """
    def __init__(self):
        Player.__init__(self)
        self.type = 'computer'

    def get_choice(self):
        return int(self.get_pending_points()) >= 25 or (int(self.get_score()) - 100) >= 25

    def set_name(self):
        self.name = 'computer {}'.format(random.randint(1, 30))


class PlayerFactory(object):
    """ Player Factory class - allows us to build players of computer or human types"""
    def player_type(self, ptype):
        """ Two types of players, human or computer """
        if ptype == 'human':
            return Player()
        elif ptype == 'computer':
            return Computer()

class Dice(object):
    """ Each dice object is initialized with a random seed of 0"""
    def __init__(self):
        self.value = random.seed(0)

    def roll(self):
        """ Each dice is six sided and can return integers between 1 and 6 """
        self.value = random.randint(1, 6)
        return self.value

    def get_roll(self):
        """ Getter method to grab the value variable """
        return self.value

class Game(object):
    """ The Game object holds the bulk of the work for the Pig game
    game_data holds the player objects
    pending_points show how many points are in the bucket to be consumed
    active_player is the player name that is currently rolling
    winner boolean determines if there is a winner of the game
    roll is the current roll
    dice is the dice object currently being used
    """
    def __init__(self):
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []

    def add_player(self, ptype=str, index=int):
        """ Adds a new player to the game_data list, also updates the score_data dictionary"""
        player_factory = PlayerFactory()
        if ptype == 'computer':
            self.game_data.append(player_factory.player_type("computer"))
            self.score_data[self.game_data[index].get_name()] = self.game_data[index].get_score()
        elif ptype == 'human':
            self.game_data.append(player_factory.player_type("human"))
            self.score_data[self.game_data[index].get_name()] = self.game_data[index].get_score()


    def add_players_to_game(self, players):
        """ Adds a multiple of players to the game """
        for player in range(players):
            self.add_player(player)

    def get_active_player(self):
        """ Getter method to pull player objects """
        return self.game_data[self.active_player]

    def get_win_state(self):
        """
        Checks player scores in the active player objects, if any of the scores are
        above 100, it returns True.
        Otherwise the function returns False.
        The Truth/False values directly correlate to the while statements which run the
        game_loop
        """
        for player in self.game_data:
            if player.get_score() >= 100:
                return True
        return False

    def get_game_status(self):
        """ Print functions - builds the game board, prints current status"""
        os.system('cls')
        print '====   Pig Game   ====\n'
        print('{:15} : {:>6}\n').format('Player', 'Score')
        for player in self.game_data:
            print('{:15} : {:6} \n').format(player.get_name(), player.get_score())
        print('{} is rolling').format(self.get_active_player().get_name())
        if self.dice.get_roll() == 1:
            print('The last roll was {}, next player\'s turn!').format(self.dice.get_roll())
        else:
            print('The last roll was {}').format(self.dice.get_roll())
        print('Pending Points: {:>10}').format(self.get_active_player().get_pending_points())

    def player_turn(self):
        """ Interactive player turn, asks for user input about whether they want
        to roll or hold.
        Depending on the outcome of the roll, the loop will either exit due to
        a player rolling 1 or if the player has over 100 points """
        rolling = self.get_active_player()
        rolling.set_turn(True)
        self.get_game_status()
        while rolling.get_turn() and not self.get_win_state():
            rollorhold = rolling.get_choice()
            if rollorhold:
                rolling.set_score(rolling.get_pending_points())
                rolling.reset_pending_points()
                rolling.set_turn(False)
            else:
                roll = self.dice.roll()
                if roll == 1:
                    rolling.reset_pending_points()
                    rolling.set_turn(False)
                rolling.set_pending_points(roll)
                self.get_game_status()
                continue

    def game_loop(self, player1, player2, num_players=2):
        """
        The game loop sets up the players in the game, and builds out a turn
        order for the players.  Once the win state is reached, the function allows for
        a game restart with user input.

        Args:
            players (optional): Number of players in the game - defaults to 2
            player1 (string):
        """
        if num_players <= 2:
            self.add_player(player1, 0)
            self.add_player(player2, 1)
        elif num_players > 2:
            for player in range(2, num_players):
                self.add_players_to_game(player)

        while not self.get_win_state():
            for player in self.game_data:
                self.active_player = (self.turns % len(self.game_data))
                self.player_turn()
                self.turns += 1

        for player in self.game_data:
            self.score_data[player.get_name()] = player.get_score()
        scores = list(self.score_data.values())
        players = list(self.score_data.keys())
        top_score = max(scores)
        winner = players[scores.index(max(scores))]
        print('\nWe have a winner! {} is the winner with {}').format(winner, top_score)
        self.reset_game()

    def reset_game(self):
        """ Re-initializes game variables for a fresh start """
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []


    def restart_game(self, player1, player2, num_players):
        """ Restart function - either builds a new game_loop or exits the game
        Depends on user input """
        while True:
            try:
                new_game = raw_input("\nPlay again? [y]|[n]: ").strip()
                if new_game == 'y':
                    self.game_loop(player1, player2, num_players)
                elif new_game == 'n':
                    print 'Thanks for playing! Goodbye!'
                    sys.exit()
            except ValueError:
                continue


class TimedGameProxy(Game):
    """ A Game class that has a time limit """
    def __init__(self):
        Game.__init__(self)
        self.start_time = time.time()
        self.end_time = time.time() + 60

    def get_win_state(self):
        """ updated win state function which checks time in addtion to score """
        if time.time() >= self.end_time:
            return True
        for player in self.game_data:
            if player.get_score() >= 100:
                return True
        return False

    def get_time_remaining(self):
        """ Returns the time remaining """
        return self.end_time - time.time()

    def get_game_status(self):
        """ Print functions - builds the game board, prints current status"""
        os.system('cls')
        print '====   Pig Game   ====\n'
        print('{:15} : {:>6}\n').format('Player', 'Score')
        for player in self.game_data:
            print('{:15} : {:6} \n').format(player.get_name(), player.get_score())
        print('{} is rolling').format(self.get_active_player().get_name())
        if self.dice.get_roll() == 1:
            print('The last roll was {}, next player\'s turn!').format(self.dice.get_roll())
        else:
            print('The last roll was {}').format(self.dice.get_roll())
        print('Pending Points: {:>10}').format(self.get_active_player().get_pending_points())
        print('Time Remaining: {} seconds').format(round(self.get_time_remaining()))

    def reset_game(self):
        """ Re-initializes game variables for a fresh start """
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []
        self.start_time = time.time()
        self.end_time = time.time() + 60

def main():
    """ Main method to run our game

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_players',
                        help='Number of players in our game',
                        type=int, required=False, default=2)
    parser.add_argument('--player1', type=str,
                        choices=['human', 'computer'], default='human', required=True)
    parser.add_argument('--player2', type=str,
                        choices=['human', 'computer'], default='computer', required=True)
    parser.add_argument('--timed', help='Determine if the game is timed',
                        choices=['yes', 'no'], required=True, default='no')
    args = parser.parse_args()
    if args.timed.lower() == "yes":
        new_game = TimedGameProxy()
    elif args.timed.lower() == "no":
        new_game = Game()
    new_game.game_loop(args.player1, args.player2, args.num_players)
    new_game.restart_game(args.player1, args.player2, args.num_players)


if __name__ == '__main__':
    main()
