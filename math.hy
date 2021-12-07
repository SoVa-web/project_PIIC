(import math)
(import pandas)
(import numpy)

(setv dataset (pandas.read_csv "result_games.csv"))
(setv duration (get dataset "duration"))
(setv score_player (get dataset "score_player"))

;variance by csore
(setv sample_average (/(.sum score_player) (len score_player)))

(setv sum_pow 0)
(for [value score_player]
    (setv buf (- value sample_average))
    (setv sum_pow (* buf buf))
)

(setv variance (/ sum_pow (- (len score_player) 1)))
(print "Variance:")
(print variance)

;mathematical expectation bu duration
(setv math_exp (/(.sum duration) (len duration)))
(print "Mathematical expectation:")
(print math_exp)
