
import requests
import json
import webbrowser

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