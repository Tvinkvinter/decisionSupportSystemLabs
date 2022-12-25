import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd


def rmse(prediction, ground_truth):
    prediction = np.nan_to_num(prediction)[ground_truth.nonzero()].flatten()
    ground_truth = np.nan_to_num(ground_truth)[ground_truth.nonzero()].flatten()

    mse = mean_squared_error(prediction, ground_truth)
    return sqrt(mse)

cards = pd.read_csv("D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\\answer.csv")
books = cards['book_title'][0]
cards = cards.to_dict()
print()
# k_predict_item = getRecommendation()
# print('RMSE: ', rmse(pred.T, test_data_matrix))
