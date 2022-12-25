import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.metrics.pairwise import pairwise_distances
import time


def processDataSet():
    ratings_df = pd.read_csv("D:\python\Studying\СППР\Lab_2\dataset\Preprocessed_data.csv")
    ratings_df = ratings_df.loc[ratings_df['rating'] > 0]
    ratings_df = ratings_df.loc[ratings_df['Language'] == 'en']
    n = 30000

    card_info = ratings_df[:n][['isbn', 'book_title', 'book_author', 'img_l']]
    card_info = card_info.drop_duplicates()
    card_info.to_csv('D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\card_info.csv',
                     index=False)

    ratings_df = ratings_df[:n][['user_id', 'isbn', 'rating', 'book_title']]

    n_users = len(ratings_df["user_id"].unique())
    n_books = len(ratings_df["isbn"].unique())

    isbns = ratings_df['isbn'].unique()
    user_ids = ratings_df['user_id'].unique()

    def scale_isbn(isbn):
        scaled = np.where(isbns == isbn)[0][0]
        return scaled

    def scale_users(user_id):
        scaled = np.where(user_ids == user_id)[0][0]
        return scaled

    ratings_df['user_id'] = ratings_df['user_id'].apply(scale_users)

    id_isbn = pd.DataFrame(ratings_df['isbn'])
    id_isbn.insert(0, 'book_id', ratings_df['isbn'])
    id_isbn['book_id'] = id_isbn['book_id'].apply(scale_isbn)
    id_isbn = id_isbn.merge(ratings_df[['isbn', 'book_title']], on='isbn')
    id_isbn = id_isbn.drop_duplicates()

    ratings_df['isbn'] = ratings_df['isbn'].apply(scale_isbn)

    train_data = ratings_df  # test_data = model_selection.train_test_split(ratings_df, test_size=0.2)
    train_data_matrix = np.zeros((n_users, n_books))
    for line in train_data.itertuples():
        train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
    # test_data_matrix = np.zeros((n_users, n_books))
    # for line in test_data.itertuples():
    #     test_data_matrix[line[1] - 1, line[2] - 1] = line[3]

    pd.DataFrame(train_data_matrix).to_csv(
        'D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\data_matrix.csv', index=False)
    id_isbn.to_csv('D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\id_isbn.csv',
                   index=False)


def getRecommendation(books):
    id_isbn = pd.read_csv('D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\id_isbn.csv')
    data_matrix = pd.read_csv(
        'D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\data_matrix.csv')
    card_info = pd.read_csv(
        'D:\python\Studying\СППР\Lab_2\\bookRecommender\\recommender\\recommendationCore\card_info.csv')
    books = pd.DataFrame.from_records(books)
    books = books.merge(id_isbn, on='book_title')[['book_id', 'rating']]
    data_matrix.loc[len(data_matrix.index)] = 0
    for i, id in enumerate(books['book_id']):
        data_matrix.iloc[-1][id] = books['rating'][i]
    data_matrix = np.array(data_matrix)

    n_books = len(id_isbn)
    n_users = len(data_matrix)

    item_similarity = pairwise_distances(data_matrix.T, metric='cosine')
    item_similarity = np.abs(item_similarity)
    top = 8
    top_similar = np.zeros((n_books, top))

    for i in range(n_books):
        books_sim = item_similarity[i]
        top_sim_books = books_sim.argsort()[1:top + 1]

        for j in range(top):
            top_similar[i, j] = top_sim_books[j]

    pred = np.zeros((n_books, n_users))

    for i in range(n_books):
        indexes = top_similar[i].astype(int)
        numerator = item_similarity[i][indexes]

        diff_ratings = data_matrix.T[indexes] - data_matrix.T[indexes].mean()
        numerator = numerator.dot(diff_ratings)
        denominator = item_similarity[i][top_similar[i].astype(int)].sum()
        denominator = denominator if denominator != 0 else 1

        mean_rating = np.array([x for x in data_matrix.T[i] if x > 0]).mean()
        mean_rating = 0 if np.isnan(mean_rating) else mean_rating
        pred[i] = mean_rating + numerator / denominator

    rec = pred.T[-1]
    rec = {i: x for i, x in enumerate(rec)}
    rec = sorted(rec, key=rec.get)
    rec.reverse()
    rec = rec[:8]
    answer = []
    for i in rec:
        isbn = np.array(id_isbn.loc[id_isbn['book_id'] == i])[0][1]
        info = np.array(card_info.loc[card_info['isbn'] == isbn])[0]
        info = {'book_title': info[1], 'book_author': info[2], 'photo': info[3]}
        answer.append(info)
    del data_matrix
    return answer

# books1 = [
#     {'book_title': 'Decision in Normandy', 'rating': 8},
#     {'book_title': 'Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It', 'rating': 9},
#     {'book_title': "The Kitchen God's Wife", 'rating': 8},
#     {'book_title': 'PLEADING GUILTY', 'rating': 8},
# ]
#
# books2 = [
#     {'book_title': 'Classical Mythology', 'rating': 8},
#     {'book_title': 'Clara Callan', 'rating': 9},
#     {'book_title': "The Catcher in the Rye", 'rating': 8},
#     {'book_title': 'Midnight in the Garden of Good and Evil: A Savannah Story', 'rating': 8},
# ]
#
# processDataSet()
# begin = time.time()
# rec_books = getRecommendation(books2)
# for book in rec_books:
#     print(book)
# end = time.time()
# print(end - begin)
