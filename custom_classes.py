from random import randint, random
from urllib import response
import requests
import json
import webbrowser

from hellofly import TMDB_API_KEY

#Retrieve top 10 movies from Movie-API
def get_top_10_weekly_trending_movies(TMDB_API_KEY):
    '''Gets response in JSON and prints the title of top 10 movies
        returns: list of top 10 movies
    '''
    top_10_movie_list = []
    url = "https://api.themoviedb.org/3/trending/movie/week?api_key=" + TMDB_API_KEY
    #Requests
    response = requests.get(url)
    response_json = response.json()

    response_results = response_json['results']

    for x in range(0,10):
        top_10_movie_list.append(response_results[x])

    random_int = randint(0,9)
    random_movie = top_10_movie_list[random_int]
    movie_genres_list = random_movie['genre_ids']
    filtered_genre_list = configure_genre_ids(TMDB_API_KEY,movie_genres_list)
    return random_movie['title'],random_movie['overview'],filtered_genre_list,random_movie['poster_path'] #Returns Title, overview, posterpath

def configure_genre_ids(TMDB_API_KEY,genres_list):
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key="+TMDB_API_KEY+"&language=en-US"
    response = requests.get(url)
    response_json = response.json()
    TMDB_genres = response_json['genres']
    filterd_genre_list = []
    for x in genres_list:
        for y in TMDB_genres:
            if x == y['id']:
                filterd_genre_list.append(y['name'])
    print(filterd_genre_list)
    return filterd_genre_list


def get_wiki_page(movie_title):
    '''Get Wiki Page'''
    session = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    search_page = movie_title

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch":search_page
    }

    response = session.get(url=URL, params=params)
    data = response.json()
    return "https://en.wikipedia.org/w/index.php?curid="+str(data['query']['search'][0]['pageid'])
        

def open_wiki_page(url):
    '''Open Webpage'''
    print(url)
    webbrowser.open_new_tab(url)