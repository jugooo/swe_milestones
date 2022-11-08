import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
# from static.PersonModel import Person
import static.custom_classes as cc
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_user,current_user,login_required


#Set Environment Variables
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
# TMDB_API_KEY = ""

#Initalize App
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #silences warning messages
app.config.update(SECRET_KEY=os.urandom(24))
db = SQLAlchemy(app)

# Person Model 
class Person(UserMixin,db.Model):
    #Every Row in the table is a person; Every Column is a field for the Person
    id = db.Column(db.Integer, primary_key=True) #db.Integer is a SQL integer type
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)

    #Return the Person + username
    def __repr__(self) -> str:
        return '<Person%r>' % self.username

class Review(db.Model):
    '''
    Review Model
    base > Movies (by ID) > Reviews
    Review will be trigger to query database for commits
    '''
    id = db.Column(db.Integer, primary_key=True) #Movie ID to match Movies models
    user = db.Column(db.String(80), unique=False, nullable=False)
    movie_id = db.Column(db.Integer, unique=False,nullable=True)
    rating = db.Column(db.Integer,unique=False,nullable=True)
    comment = db.Column(db.String(120),unique=False,nullable=True)

    def __repr__(self) -> str:
        return '<Review%r>' % self.id

# class Movies(db.Model):
#     '''
#     Movie Model
#     base > Movie (by ID)
#     When a review is submitted, check if the ID is in the database
#     IF NOT add the movie (ID, title) and the review
#     IF EXISTING add review to Movie ID table
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.Integer,unique=True,nullable=False)
#     title = db.Column(db.String(80), unique=True,nullable=False)

#     def __repr__(self) ->str:
#         return '<Movies%r' % self.id


#Get Server to talk to Database
with app.app_context():
    db.create_all()

db.init_app(app=app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))

@app.route('/')
def inital_menu():
    return flask.render_template('inital_menu.html')

@app.route('/create_account',methods=['GET','POST'])
def create_account():
    return flask.render_template('create_account.html')

@app.route('/handle_create_account',methods=['POST'])
def handle_create_account():
    user_input = flask.request.form
    username_input = user_input['username_input']
    email_input = user_input['email_input']
    #Set User Model
    created_user = Person(username=username_input,email=email_input)

    if not register_validate_username(username_input=username_input):
        #The username is already in use
        flask.flash('Email Address already exists')
        return flask.redirect(flask.url_for('create_account'))
    else:
        # Add User to Database
        db.session.add(created_user)
        db.session.commit()
        # If everything is valid redirect to index.html
        return flask.redirect(flask.url_for('index_page'))

#Gets username input, if it exists already return false, 
def register_validate_username(username_input):
    existing_user_username = Person.query.filter_by(
        username=username_input).first()
    if existing_user_username:
        return False
    return True

    
@app.route('/login', methods=['GET','POST'])
def login():
    return flask.render_template('login.html')

@app.route('/handle_login',methods=['GET','POST'])
def handle_login():
    user_input=flask.request.form
    username_input = user_input['username_input']
    email_input = user_input['email_input']
    existing_user = Person.query.filter_by(username=username_input,email=email_input).first()
    if existing_user:
        login_user(existing_user)
        return flask.redirect(flask.url_for('index_page'))
    else:
        flask.flash('Incorrect Credentials')
        return flask.redirect(flask.url_for('login'))


# ------- Login Required -------

@app.route('/index',methods=['GET','POST'])
@login_required
def index_page():
    '''Load Landing Page
        returns: index home page
    '''
    # movie_title,movie_overview,movie_genre,movie_poster_path,movie_id = cc.get_top_10_weekly_trending_movies(TMDB_API_KEY)
    movie_dict = cc.get_top_10_weekly_trending_movies(TMDB_API_KEY)
    movie_wiki_page = cc.get_wiki_page(movie_title=movie_dict['title'])
    # cc.open_wiki_page(movie_wiki_page) #Opens Wiki page in a new tab
    # pull_reviews(movie_dict['id'])
    return flask.render_template(
        'index.html',
        movie_title=movie_dict['title'],
        movie_overview=movie_dict['overview'],
        movie_poster_path=movie_dict['poster_url'],
        movie_genre=movie_dict['genres'],
        wiki_link=movie_wiki_page,movie_id=movie_dict['id'],
        username = current_user.username,
        )
# def pull_reviews(movie_id):
#     reviews = Review.query.filter_by(movie_id=movie_id).all()
#     print("Reviews")
#     for result in reviews:
#         print(type(result))

@login_required
@app.route('/handle_review_submit', methods=['GET','POST'])
def handle_review_submit():
    review_input = flask.request.form
    review_user = review_input['username']
    review_movie_id = review_input['movie_id']
    review_rating = review_input['movie_rating']
    review_comment = review_input['movie_comment']
    # print(review_comment, review_movie_id,review_rating,review_user)
    created_review = Review(movie_id=review_movie_id,rating=review_rating,user=review_user,comment=review_comment)
    db.session.add(created_review)
    db.session.commit()

    flask.flash("Movie review has been submitted")
    return flask.redirect(flask.url_for('index_page'))


if __name__ == "__main__":
#     # Run App
    app.run(debug=True)
