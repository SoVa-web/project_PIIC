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
        

    def distance_in_straight_line(self, pos1, pos2):
        dist = math.sqrt(math.pow((pos1.x - pos2.x), 2)+math.pow((pos1.y - pos2.y), 2))
        return dist

    # arithmetic mean of distances to all opponents, arr_dist - array of distances to all opponents
    def hueristic_alpha_beta(self, pos_players, pos_op):
        sum = 0
        for p in pos_players:
            for op in pos_op:
                sum += self.distance_in_straight_line(p, op)
        if sum != 0:
            sum = sum//(len(pos_op)*len(pos_players))
        return sum

    def minimax(self, players_pos, army_opponent_pos, current_depth, count_op, isMaximizer, alpha, beta):
        if current_depth == self.max_deep:
                return self.hueristic_alpha_beta(players_pos, army_opponent_pos)
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
                if self.field.can_move_to_pos(army_opponent_pos[count_op-1] + move):
                    army_opponent_pos[count_op-1] += move
                value = self.minimax(players_pos, army_opponent_pos, current_depth+1, count_op+1, isMaximizer, alpha, beta)
                bestVal = min( bestVal, value) 
                beta = min( beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal 
