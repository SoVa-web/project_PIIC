import math
from game_object.vec2 import Vec2
import sys

class MinimaxAlphaBeta:
    def __init__(self, field):
        self.field = field
        self.max_deep = 4
        self.directions = [ 
            Vec2(x=-1, y=0),
            Vec2(x=+1, y=0),
            Vec2(x=0, y=+1),
            Vec2(x=0, y=-1)
        ]
        self.dist = 0
        self.sum = 0
        

    def distance_in_straight_line(self, pos1, pos2):
        self.dist = math.sqrt(math.pow((pos1.x - pos2.x), 2)+math.pow((pos1.y - pos2.y), 2))

    # arithmetic mean of distances to all opponents, arr_dist - array of distances to all opponents
    def hueristic_alpha_beta(self, pos_players, pos_op):
        self.sum = 0
        for p in pos_players:
            for op in pos_op:
                self.distance_in_straight_line(p, op)
                self.sum += self.dist
        if self.sum != 0:
            self.sum = self.sum//(len(pos_op)*len(pos_players))

    def minimax(self, players_pos, army_opponent_pos, current_depth, count_op, isMaximizer, alpha, beta):
        if current_depth == self.max_deep:
            self.hueristic_alpha_beta(players_pos, army_opponent_pos)
            return self.sum
        if isMaximizer :
            bestVal = - 1000
            for move in self.directions:
                players_pos[0] += move
                value = self.minimax(players_pos, army_opponent_pos, current_depth+1, 1, False, alpha, beta)
                bestVal = max( bestVal, value) 
                alpha = max( alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal
        else:
            bestVal = 1000
            if len(army_opponent_pos) == count_op:
                isMaximizer = True
            for  move in self.directions :
                army_opponent_pos[count_op-1] += move
                value = self.minimax(players_pos, army_opponent_pos, current_depth+1, count_op+1, isMaximizer, alpha, beta)
                bestVal = min( bestVal, value) 
                beta = min( beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal 
