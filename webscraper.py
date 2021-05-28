from requests import get
from bs4 import BeautifulSoup


def get_movies_with_reviews():
    url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=2020-01-01,2021-05-19&count=10'
    url_first_part_for_reviews = 'https://www.imdb.com'
    url_final_part_for_reviews = 'reviews?ref_=tt_urv'
    base_response = get(url)
    html_soup = BeautifulSoup(base_response.text, 'html.parser')

    movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

    reviews_data = {}
    for container in movie_containers:
        # doar daca filmul are metascore
        if container.find('div', class_ = 'ratings-metascore') is not None:
            num_reviews = 5
            url_middle_for_reviews = container.find('a')['href']
            response_reviews = get(url_first_part_for_reviews + url_middle_for_reviews + url_final_part_for_reviews)
            reviews_soup = BeautifulSoup(response_reviews.text, 'html.parser')
            reviews_containers = reviews_soup.find_all('div', class_ = 'imdb-user-review')
            # sa verific daca nr review-urilor e mai mic de 5. daca da => num_reviews devine numarul lor.
            if len(reviews_containers) < num_reviews:
                num_reviews = len(reviews_containers)
            reviews_bodies = []
            for review_index in range(num_reviews):
                review_container = reviews_containers[review_index]
                review_body = review_container.find('div', class_ = 'text').text.strip()
                reviews_bodies.append(review_body)
                reviews_data[container.h3.a.text] = reviews_bodies
    # print(reviews_data)
    return reviews_data


get_movies_with_reviews()
