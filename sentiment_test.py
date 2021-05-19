import sentiment_mod as s
import webscraper

movies_dictionary = webscraper.get_movies_with_reviews()

for k, v in movies_dictionary.items():
    print('\n'+k)
    for review in v:
        print(review)
        print(s.sentiment(review))
        print("#######################")

