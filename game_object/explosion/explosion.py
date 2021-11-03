import pygame
from typing import TYPE_CHECKING
from game_object import Vec2
from game_object.game_obj import GameObjectSprite
from config import TIMER_EXPLOSION, FIELD_H_SIZE, FIELD_W_SIZE


if TYPE_CHECKING:
    from game_object.field import Field

class ExplosionSprite(GameObjectSprite):
    def __init__(self, pos: Vec2, sprite_filename: str, parent:'Explosion'):
        super().__init__(pos,  sprite_filename)
        self.parent = parent
        self.pos = pos

class Explosion:
    def __init__(self, parent: 'Field', pos: Vec2 = Vec2()):
        self.parent = parent
        self.pos = pos
        self.sprite = ExplosionSprite(self.pos, 'explosion4.png', parent=self)
        self.timer = TIMER_EXPLOSION

    def delete(self, graph, draw_path):
        self.timer -= 1
        if self.timer == 0:
            self.parent.parent.explosions.remove(self)
            self.sprite.kill()
            dir = [Vec2(+1, 0), Vec2(-1, 0), Vec2(0, +1), Vec2(0, -1)]
            for i in dir:
                    if graph.parent.can_draw_edge_graph(self.sprite.pos + i):
                            index_adj = graph.set_nodes.index((self.sprite.pos + i))
                            if graph.parent.can_draw_edge_graph((self.sprite.pos)) and graph.set_nodes.index(self.sprite.pos) != index_adj:
                                graph.matrix_adjacency[graph.set_nodes.index(self.sprite.pos)][index_adj] = graph.matrix_adjacency[index_adj][graph.set_nodes.index(self.sprite.pos)] = 1
                                graph.list_adjacency[graph.set_nodes.index(self.sprite.pos)].append(index_adj)
                                graph.list_adjacency[index_adj].append(graph.set_nodes.index(self.sprite.pos))
            draw_path()