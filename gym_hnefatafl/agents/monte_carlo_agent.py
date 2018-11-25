import copy
import random
import numpy as np
from gym_hnefatafl.envs import HnefataflEnv
from gym_hnefatafl.envs.board import Outcome, Player

MONTE_CARLO_ITERATIONS = 1000
MIN_NUM_VISITS_INTERNAL = 5 # may have to be much higher go uses 9*9

#################################################################################################################
#################################################################################################################
#################################################################################################################
OUTCOME_BLACK_VALUE = -1
OUTCOME_WHITE_VALUE = 1
OUTCOME_DRAW_VALUE = 0

# An den Werten hier muss bestimmt noch was geändert werden, weil auch die Quadrate davon gespeichert werden!!!
#################################################################################################################
#################################################################################################################
#################################################################################################################


# represents a monte carlo search tree
class Tree(object):
    # board: the current board
    # player: the player that this agent represents
    def __init__(self, board, player):
        self.root = Node(player)
        self.board = board
        self.num_simulations = 0

    # simulates an entire game
    def simulate_game(self):
        # init
        self.num_simulations += 1
        # game history saves all actions done during this simulation
        game_history = []
        board_copy = copy.deepcopy(self.board)
        current_node = self.root

        # simulate actions within the tree until we are no longer at an internal node
        while board_copy.outcome == Outcome.ongoing:
            current_node, action = current_node.choose_and_simulate_action(board_copy)
            game_history.append(action)
            if current_node is None:
                break

        # continue on with external nodes
        while board_copy.outcome == Outcome.ongoing:
            game_history.append(self.__choose_and_simulate_action__())

        # calculate game value
        game_value = OUTCOME_BLACK_VALUE if board_copy.outcome == Outcome.black \
            else OUTCOME_WHITE_VALUE if board_copy.outcome == Outcome.white \
            else OUTCOME_DRAW_VALUE

        # back value up
        # TODO: this part is probably not correct and needs to be changed to the algorithm on page 7 of the paper
        current_node = self.root
        for action in game_history:
            current_node.update_value(game_value)
            current_node = current_node.children[action]
            if current_node is None:
                break

    # chooses an action and simulates it. Then returns the action
    def __choose_and_simulate_action__(self):
        raise NotImplementedError

    # returns the best action found
    def get_best_action(self):
        raise NotImplementedError


# represents a node within the monte carlo search tree (that is actually stored in memory -> see the paper)
class Node(object):
    def __init__(self, player):
        self.children = {}
        self.number_of_visits = 0
        self.sum_of_values = 0
        self.sum_of_squared_values = 0
        self.mean = 0.0
        self.variance = 0.0
        self.player = player
        self.sorted_child_indices = []
        self.action_probabilities = []

    # chooses and simulates an action
    def choose_and_simulate_action(self, board):
        self.number_of_visits += 1
        action = self.__choose_action__(board)
        board.do_action(action, self.player)
        # create child node if this node has already been visited
        if self.number_of_visits > 1 and action not in self.children:
            child_node = Node(other_player(self.player))
            self.children[action] = child_node
            return child_node, action
        else:
            return None, action

    # chooses an action
    def __choose_action__(self, board):
        if self.is_internal():  # do random move based on probability distribution
            return np.random.choice(self.children, 1, self.action_probabilities)
        else:  # do random move for external nodes
            return random.choice(board.get_valid_actions(self.player))

    # updates the internal values
    def update_value(self, value):
        self.sum_of_values += value
        self.sum_of_squared_values += value * value

    def update_action_probabilities(self):
        # sort actions/children descending by mean value of children (or ascending by -mean see paper)
        sorted_children = sorted(self.children.items(), key=lambda ac: ac[1].mean)
        # compute probabilities for each move
        self.action_probabilities = [Node.probability(sorted_children, i) for i in enumerate(sorted_children)]

    def is_internal(self):
        return self.number_of_visits > MIN_NUM_VISITS_INTERNAL

    @staticmethod
    def probability(children, i):
        ai = 0  # just for now
        epsi = (0.1 + pow(2, -i) + ai)/len(children)
        m0 = children[0][1].mean
        mi = children[i][1].mean
        s0 = children[0][1].variance
        si = children[i][1].variance
        return np.exp(-2.4*(m0-mi)/np.sqrt(2*(s0*s0+si*si))) + epsi



# returns the opponent of the given player
def other_player(player):
    return Player.white if player == Player.black else Player.white


class MonteCarloAgent(object):
    # chooses a random move and returns it
    # in order for games to finish in a reasonable amount of time,
    # the agent always sends the king to one of the corners if able
    # (this causes white to win basically all the time)
    def make_move(self, env: HnefataflEnv) -> ((int, int), (int, int)):
        tree = Tree(env.get_board())
        for i in range(MONTE_CARLO_ITERATIONS):
            tree.simulate_game()
        return tree.get_best_action()

    # does nothing in this agent, but is here because other agents need it
    def give_reward(self, reward):
        pass
