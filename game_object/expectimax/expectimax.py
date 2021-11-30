
from game_object.vec2 import Vec2
import math
class Expectimax:
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
    def hueristic(self, pos_players, pos_op):
        self.sum = 0
        for p in pos_players:
            for op in pos_op:
                self.distance_in_straight_line(p, op)
                self.sum += self.dist
        if self.sum != 0:
            self.sum = self.sum//(len(pos_op)*len(pos_players))

    def expectimax(self, players_pos, army_opponent_pos, current_depth, count_op, isMaximizer):
        if current_depth == self.max_deep:
            self.hueristic(players_pos, army_opponent_pos)
            return self.sum
        if isMaximizer :
            bestVal = - 1000
            for move in self.directions:
                players_pos[0] += move
                value = self.expectimax(players_pos, army_opponent_pos, current_depth+1, 1, False)
                bestVal = max( bestVal, value) 
            return bestVal
        else:
            exp_value = 0
            if len(army_opponent_pos) == count_op:
                isMaximizer = True
            for  move in self.directions :
                army_opponent_pos[count_op-1] += move
                value = self.expectimax(players_pos, army_opponent_pos, current_depth+1, count_op+1, isMaximizer)
                exp_value += value
            return exp_value/len(self.directions)
            