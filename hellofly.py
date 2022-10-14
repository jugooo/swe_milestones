#import flask
from flask import Flask, render_template
from custom_classes import get_top_10_weekly_trending_movies
from dotenv import load_dotenv
import os

#Set Environment Variables
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

#Initalize App
app = Flask(__name__)

# #Name will be set after /Route added
# @app.route('/<name>')
@app.route('/')
def index_page():
    '''Load Landing Page
        returns: index home page
    '''
    movie_list = []
    movie_list = get_top_10_weekly_trending_movies(TMDB_API_KEY)
    print(movie_list)
    return render_template('index.html',movies_list= movie_list)


if __name__ == "__main__":  
    #Run App
    app.run()