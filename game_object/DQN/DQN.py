#Deep Q-learning Network base on matrix
#
# action: 0 - up,               |   state: 0 - number opponents
#         1 - down,             |          1 - average distance to opponents
#         2 - left,             |          2 - points
#         3 - right,            |          3 - number dodges of player under bullets
#         4 - stay put,         |          4 - number_blocks
#         5 - up + ballet,      |   
#         6 - down + ballet,    |
#         7 - left + ballet,    |   
#         8 - right + ballet,   |
#         9 - stay put + ballet |
#
#
#
#   In matrix_state_action_weight  vertical is states, horizontal is actions
#
#
import math
import random
import copy
import itertools

class DQN:
    def __init__(self, parent, st_op, op):
        self.parent = parent
        self.arr_opponents = itertools.chain(st_op, op)
        self.number_opponents = len(st_op) + len(op) #try minimize
        self.dist_average = 0                      #try minimize
        self.points = 0                            #try maximize
        self.number_dodges = 0                     #try to maximize
        self.number_block = 0
        self.number_state = 5
        self.number_action = 10
        self.matrix_state_action_weight = [[1 for j in range(self.number_action)] for i in range(self.number_state)] #weigth
        self.random_step_probability = 0.25
        self.last_state = None                      #previous data
        self.last_action = None                     #previous move

    def update_state(self, parent, st_op, op, points, dodges, number_block):
        self.parent = parent
        self.arr_opponents = itertools.chain(st_op, op)
        self.number_opponents = len(st_op) + len(op)    #input data
        self.dist_average = self.calc_dist_average()    #input data
        self.points = points                            #input data
        self.number_dodges = dodges                     #input data
        self.number_block = number_block                #input data
        

    def calc_dist_average(self):
        dist = 0
        for op in self.arr_opponents:
            dist += self.distance_in_straight_line(self.parent.pos, op.pos)
        return dist



    def distance_in_straight_line(self, pos1, pos2):
        return (math.sqrt(math.pow((pos1.x - pos2.x), 2) + math.pow((pos1.y - pos2.y), 2)))

    def choosing_action(self):
        if (self.last_state != None):
            #evaluate
            pass
        n = (random.randint(0, 1000) / 100) % self.random_step_probability
        next_action = None
        if n == 0:
            next_action = random.randint(0, 9)
        else:
            next_action = self.generate_action_by_neural_network()
        self.parent.move(next_action)
        self.last_action = next_action
        self.last_state = [None for i in range(self.number_state)]
        self.last_state[0] = self.number_opponents
        self.last_state[1] = self.dist_average
        self.last_state[2] = self.points
        self.last_state[3] = self.number_dodges
        self.last_state[4] = self.number_block

    def generate_action_by_neural_network(self):
        return random.randint(0, 9)
