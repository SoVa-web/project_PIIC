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
import json

class DQN:
    def __init__(self, parent, st_op, op):
        self.parent = parent
        self.arr_opponents = itertools.chain(st_op, op)
        self.alpha = 0.6
        self.number_opponents = len(st_op) + len(op) #try minimize
        self.dist_average = 0                      #try minimize
        self.points = 0                            #try maximize
        self.number_dodges = 0                     #try to maximize
        self.number_block = 0
        self.number_state = 5
        self.number_action = 10
        self.matrix_state_action_weight = [[1 for j in range(self.number_action)] for i in range(self.number_state)] #weigth
        self.random_step_probability = 0.04
        self.last_state = None                      #previous data
        self.last_action = None                     #previous move
        self.output = [0 for i in range(self.number_action)] 
        self.input = [0 for i in range(self.number_state)]

        self.obj  = {}

        with open('neural_model.json') as f:
            self.obj = json.load(f)

        self.input = copy.deepcopy(self.obj["input"])
        self.output = copy.deepcopy(self.obj["outputScore"])
        self.matrix_state_action_weight = copy.deepcopy(self.obj["weight"])
        self.last_state =  copy.deepcopy(self.obj["last_state"])
        self.last_action =  copy.deepcopy(self.obj["last_action"])
        

    def update_state(self, parent, st_op, op, points, dodges, number_block):
        self.parent = parent
        self.arr_opponents = itertools.chain(st_op, op)
        self.number_opponents = len(st_op) + len(op)    #input data
        self.dist_average = self.calc_dist_average()    #input data
        self.points = points                            #input data
        self.number_dodges = dodges                     #input data
        self.number_block = number_block                #input data
        self.input[0] = self.number_opponents
        self.input[1] = self.dist_average
        self.input[2] = self.points
        self.input[3] = self.number_dodges
        self.input[4] = self.number_block
        

    def calc_dist_average(self):
        dist = 0
        for op in self.arr_opponents:
            dist += self.distance_in_straight_line(self.parent.pos, op.pos)
        return dist



    def distance_in_straight_line(self, pos1, pos2):
        return (math.sqrt(math.pow((pos1.x - pos2.x), 2) + math.pow((pos1.y - pos2.y), 2)))

    def choosing_action(self):
        if (self.last_state is not None):
            #evaluate
            self.score()
            if self.is_better :
                for i in range(len(self.matrix_state_action_weight)):
                    self.matrix_state_action_weight[i][self.last_action] += 1 * self.last_state[i]
            else:
                for j in range(len(self.matrix_state_action_weight)):
                    self.matrix_state_action_weight[j][self.last_action] -= 1 * self.last_state[j]
        n = (random.randint(0, 4))
        next_action = None
        if n == 0 or self.last_state is None:
            next_action = random.randint(0, 9)
        else:
            next_action = self.choose_action_by_neural_network()
        self.parent.move(next_action)
        self.last_action = next_action
        self.last_state = [None for i in range(self.number_state)]
        self.last_state[0] = self.number_opponents
        self.last_state[1] = self.dist_average
        self.last_state[2] = self.points
        self.last_state[3] = self.number_dodges
        self.last_state[4] = self.number_block

    def choose_action_by_neural_network(self):
        max_score_output = max(self.output)
        next_action = self.output.index(max_score_output)
        return next_action


    def score(self):
        for i in range(self.number_action):
            for j in range(self.number_state):
                if j == 0:
                    self.output[i] -= self.input[j] * self.matrix_state_action_weight[j][i] / 30
                elif j == 1:
                    self.output[i] -= self.input[j] * self.matrix_state_action_weight[j][i] / 20
                elif j == 2:
                    self.output[i] -= self.input[j] * self.matrix_state_action_weight[j][i] * 2
                elif j == 3:
                    self.output[i] += self.input[j] * self.matrix_state_action_weight[j][i] / 10
                else:
                    self.output[i] += self.input[j] * self.matrix_state_action_weight[j][i] / 2
            sum_arr = 0
            for i in range(1, 9):
               sum_arr  += self.output[i]*(pow(self.alpha, i))
            self.output[i] += sum_arr
           

    def is_better(self):
        sum_score = 0
        if self.points >= self.last_state[2]:
            sum_score += 3
        if self.number_opponents < self.last_state[0]:
            sum_score += 20
        if self.dist_average < self.last_state[1]:
            sum_score += 10
        if self.number_dodges >= self.last_state[3]:
            sum_score += 5
        if self.number_block <= self.last_state[4]:
            sum_score += 1
        if sum_score > 9: # points + num_block  + number_doges
            return True
        return False