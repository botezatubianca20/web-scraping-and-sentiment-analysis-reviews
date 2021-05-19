# Import packages and set urls

from requests import get
from bs4 import BeautifulSoup
import pandas as pd

def get_movies_with_reviews():
    base_url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=2020-01-01,2021-05-19&count=10'
    url_header_for_reviews = 'https://www.imdb.com'
    url_tail_for_reviews = 'reviews?ref_=tt_urv'
    base_response = get(base_url)
    html_soup = BeautifulSoup(base_response.text, 'html.parser')

    movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

    result_df = pd.DataFrame()

    # Extract data from individual movie container

    reviews_data = {}
    for container in movie_containers:
    # If the movie has Metascore, then extract:
        if container.find('div', class_ = 'ratings-metascore') is not None:

    # Reviews extracting
            num_reviews = 5
            # Getting last piece of link puzzle for a movie reviews` link
            url_middle_for_reviews = container.find('a')['href']
            # Opening reviews page of a concrete movie
            response_reviews = get(url_header_for_reviews + url_middle_for_reviews + url_tail_for_reviews)
            reviews_soup = BeautifulSoup(response_reviews.text, 'html.parser')
            # Searching all reviews
            reviews_containers = reviews_soup.find_all('div', class_ = 'imdb-user-review')
            # Check if actual number of reviews is less than target one
            if len(reviews_containers) < num_reviews:
                num_reviews = len(reviews_containers)
            # Looping through each review and extracting title and body
            reviews_bodies = []
            for review_index in range(num_reviews):
                review_container = reviews_containers[review_index]
                review_title = review_container.find('a', class_ = 'title').text.strip()
                review_body = review_container.find('div', class_ = 'text').text.strip()
                reviews_bodies.append(review_body)
                reviews_data[container.h3.a.text] = reviews_bodies
    # print(reviews_data)
    return reviews_data


get_movies_with_reviews()
