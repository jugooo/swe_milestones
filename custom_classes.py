import requests
import json

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
        top_10_movie_list.append(response_results[x]['title'])

    return top_10_movie_list
