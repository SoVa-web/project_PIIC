(import numpy)
(import random)
(import math)

(setv field [
    [1 0 0 0 1]
    [0 0 0 1 1]
    [0 1 0 1 0]
    [0 1 1 0 0]
    [0 0 0 0 0]
])

;we count from 0
(setv size_matrix 4)
(setv max_deep 2)

;(y, x)
(setv player [0 1])
(setv opponent [2 4])


(defn hueristic_alpha_beta [])


(set y 0)
(defn minimax [pos_player pos_opponent current_depth isMaximizer]
   ( if (= current_depth max_deep)
        (return (hueristic_alpha_beta pos_player pos_opponent))
   )
   (if (= isMaximizer True)
       (do
        (setv bestVal (- 1000))
        (for [move directions]
            (setv y (+ (get pos_player 0) (get move 0)))
            (setv x (+ (get pos_player 1) (get move 1)))
            (setv pos_player [y x])
            (setv current_depth (+ current_depth 1))
            (setv value (minimax pos_player pos_opponent current_depth False))
            (return (max bestVal value))
        ))
   )
   (if (= isMaximizer False)
       (do
        (setv bestVal 1000)
        (for [move directions]
            (setv y (+ (get pos_opponent 0) (get move 0)))
            (setv x (+ (get pos_opponent 1) (get move 1)))
            (setv pos_opponent [y x])
            (setv current_depth (+ current_depth 1))
            (setv value (minimax pos_player pos_opponent current_depth True))
            (return (min bestVal value))
        ))
   )
)

