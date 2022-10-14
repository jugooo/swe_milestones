from crypt import methods
import flask
from custom_classes import get_top_10_weekly_trending_movies
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
    movie_list = get_top_10_weekly_trending_movies(TMDB_API_KEY)
    return flask.render_template('index.html',movies_list= movie_list)

@app.route('/handle_selection', methods=["POST","GET"])
def handle_selection():
    '''Handles which index is selected'''
    movie_selection_data = flask.request.form
    movie_selected = movie_selection_data['movie_title']
    return flask.redirect(flask.url_for('render_movie',movie=movie_selected))


@app.route('/movie_information/<movie>')
def render_movie(movie):
    '''Render Movie Information From Wiki'''
    print(movie)
    return flask.render_template('movie.html')

if __name__ == "__main__":  
    #Run App
    app.run()