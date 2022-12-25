import pandas as pd
from django.shortcuts import render
from recommender.recommendationCore import recommender


def index(request):
    return render(request, 'recommender/index.html')


def recommendation(request):
    query = []
    cards = []
    if request.method == "POST":
        input_books = []
        for book in request.POST.getlist('book'):
            input_books.append(book)
        input_stars = []
        for star in request.POST.getlist('stars'):
            input_stars.append(star)
        for i in range(len(input_books)):
            query.append(dict(book_title=input_books[i], rating=input_stars[i]))
        recommender.processDataSet()
        cards = recommender.getRecommendation(query)
        print(cards)

    return render(request, 'recommender/recommendation.html', {'info': cards})
