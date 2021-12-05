(import numpy)
(import [matplotlib [pyplot :as plt]])
(import seaborn)
(import pandas)
(import [sklearn.preprocessing [OrdinalEncoder]])
(import [sklearn.model_selection [train_test_split]])
(import [sklearn.linear_model [LinearRegression]])


(defn divide_dataset [data]
    [(data.drop "score_player" :axis 1) data.score_player])

(defn diagram_win_dependencies[data]
    (setv figure (seaborn.pairplot data :hue "winner" :diag_kind "hist" :height 4))
    (figure.fig.suptitle "Duration, score, algorithm")
    (plt.show)
)

;loading dataset
(setv dataset (pandas.read_csv "result_games.csv" ))
(print "Dataset")
(print (dataset.head))

;train and test dataset
(setv test_dataset(cut dataset 0 5))
(setv train_dataset (cut dataset 5 (len dataset)))

;diagram dependencies win before normalization
(diagram_win_dependencies train_dataset)

;there should be normalization)))))

;diagram dependencies win after normalization
(diagram_win_dependencies train_dataset)

;division into dependent and independent var
(setv x (get (divide_dataset train_dataset) 0))
(setv y (get (divide_dataset train_dataset) 1))

;dividing for train and checking
(setv dataset_shuffle (train_test_split x y :test_size 0.2 :shuffle True))
(setv x_train (get dataset_shuffle 0))
(setv x_valid (get dataset_shuffle 1))
(setv y_train (get dataset_shuffle 2))
(setv y_valid (get dataset_shuffle 3))


(setv columns ["winner" "algorithm"])

(setv encoder (OrdinalEncoder))

(assoc x_train columns (encoder.fit_transform (get x_train columns)))
(assoc x_valid columns (encoder.transform (get x_valid columns)))

;regression
(setv regressionModel (LinearRegression))
(regressionModel.fit x_train y_train)

;prediction
(setv x_test (get (divide_dataset test_dataset) 0))
(setv y_test (get (divide_dataset test_dataset) 1))

(assoc x_test columns (encoder.transform (get x_test columns)))
(setv y_pred (regressionModel.predict x_test))

(print "Prediction:")
(print y_pred)

;comparation
(print "Statistic:")
(print (numpy.abs (- y_test y_pred)))