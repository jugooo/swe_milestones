from crypt import methods
import flask
# from custom_classes import get_top_10_weekly_trending_movies,get_wiki_page,open_wiki_page
import custom_classes as cc
from dotenv import load_dotenv
import os

#Set Environment Variables
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

#Initalize App
app = flask.Flask(__name__)

# #Name will be set after /Route added
# @app.route('/<name>')
@app.route('/')
def index_page():
    '''Load Landing Page
        returns: index home page
    '''
    # movie_list = []
    movie_title,movie_overview,movie_genre,movie_poster_path = cc.get_top_10_weekly_trending_movies(TMDB_API_KEY)
    return flask.render_template('index.html',movie_title=movie_title,movie_overview=movie_overview,movie_poster_path=movie_poster_path,movie_genre=movie_genre)

@app.route('/handle_selection', methods=["POST","GET"])
def handle_selection():
    '''Handles which index is selected'''
    movie_selection_data = flask.request.form
    movie_selected = movie_selection_data['movie_title']
    movie_url = cc.get_wiki_page(movie_selected)
    cc.open_wiki_page(movie_url) #Opens Wiki page in a new tab
    return flask.redirect(flask.url_for('index_page'))

if __name__ == "__main__":
    #Run App
    app.run()
