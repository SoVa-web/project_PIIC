(import numpy)
(import random)
(import math)

(setv field [
    [1 0 0 0 1]
    [0 0 0 1 1]
    [0 1 0 1 0]
    [0 0 1 0 0]
    [0 0 0 0 0]
])

;we count from 0
(setv size_matrix 4)
(setv max_deep 2)
(setv directions [
    [1 0]
    [-1 0]
    [0 -1]
    [0 1]
])

;(y, x)
(setv player [0 2])
(setv opponent [3 4])


(defn hueristic_alpha_beta [])


(setv value 1000)
(defn minimax [pos_player pos_opponent current_depth isMaximizer]
    (print "Current depth = " current_depth "; pos player:" pos_player "; pos opponent:" pos_opponent)
   ( if (= current_depth max_deep)
       ( do
       (return (hueristic_alpha_beta pos_player pos_opponent))
       )
   )
   (if (= isMaximizer True)
       (do
        (setv bestVal (- 1000))
        (for [move directions]
            (setv y (+ (get pos_player 0) (get move 0)))
            (setv x (+ (get pos_player 1) (get move 1)))
            (setv g (get field y x))
            (if (or (< y 0)  (< x 0)  (> y size_matrix)  (> x size_matrix) (= (get field y x) 1))
                (do
                   (continue)
                )
            ) 
            (setv value (minimax [y x] pos_opponent (+ current_depth 1) False))
        )
        (return (max bestVal value))
        )
   )
   (if (= isMaximizer False)
       (do
        (setv bestVal 1000)
        (for [move directions]
            (setv y (+ (get pos_opponent 0) (get move 0)))
            (setv x (+ (get pos_opponent 1) (get move 1)))
            (if (or (< y 0)  (< x 0)  (> y size_matrix)  (> x size_matrix) (= (get field y x) 1))
                (do
                    (continue)
                )
            ) 
            (setv value (minimax pos_player [y x] (+ current_depth 1) True))
        )
        (return (min bestVal value))
        )
   )
)


(defn hueristic_alpha_beta [pos1 pos2]
    (setv dist (math.sqrt (+ (* (- (get pos1 0) (get pos2 0)) (- (get pos1 0) (get pos2 0))) (* (- (get pos1 1) (get pos2 1)) (- (get pos1 1) (get pos2 1)))) )
)
    (return dist)
)

(print (minimax player opponent 0 True))
