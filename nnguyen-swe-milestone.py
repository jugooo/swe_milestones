import flask
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
    movie_title,movie_overview,movie_genre,movie_poster_path = cc.get_top_10_weekly_trending_movies(TMDB_API_KEY)
    movie_wiki_page = cc.get_wiki_page(movie_title=movie_title)
    # cc.open_wiki_page(movie_wiki_page) #Opens Wiki page in a new tab
    print(movie_wiki_page)
    return flask.render_template('index.html',movie_title=movie_title,movie_overview=movie_overview,movie_poster_path=movie_poster_path,movie_genre=movie_genre,wiki_link=movie_wiki_page)

# @app.route('/handle_selection', methods=["POST"])
# def handle_selection():
#     '''Handles which index is selected'''
#     movie_selection_data = flask.request.form
#     movie_selected = movie_selection_data['selected_movie_title']
#     print("Selected Movie {movie_selected}")
#     movie_url = cc.get_wiki_page(movie_selected)
#     cc.open_wiki_page(movie_url) #Opens Wiki page in a new tab
#     return 
    # return flask.redirect(flask.url_for('index_page'))

if __name__ == "__main__":
    #Run App
    app.run(debug=True)
