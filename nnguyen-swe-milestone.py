import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_user,current_user,login_required
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, select, MetaData, Table, and_
import book_recommendation as br




#Set Environment Variables
load_dotenv()
# TMDB_API_KEY = os.getenv('TMDB_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
# TMDB_API_KEY = ""

#Initalize App
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #silences warning messages
app.config['TEMPLATES_AUTO_RELOAD'] = True
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

# User Details


#https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
#Like and Dislike List
# User_ID Foreign Key
# 0, 1 (Dislike, Like)(Future 3, 4)
# We can query for Dislikes and likes easily by userID if isLike is 1 then its liked
# Book ID
class PersonPreference(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey('person.id',ondelete='CASCADE'))
    book_id = db.Column(db.BigInteger, nullable=True)
    isLike = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self) -> str:
        return '<PersonPreference%r>' % self.id

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




#Get Server to talk to Database
with app.app_context():
    db.create_all()
engine = db.create_engine('postgresql://swe_milestone:jthJxRTUWSUEd0z@localhost:5432')
conn = engine.connect() 

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
    # get form info
    user_input=flask.request.form
    username_input = user_input['username_input']
    email_input = user_input['email_input']
    #create perso \n object
    existing_user = Person.query.filter_by(username=username_input,email=email_input).first()
    
    # print("EXISTING: "+ str(existing_user.id))
    if existing_user:
        uid = existing_user.id
        login_user(existing_user)
        # Set UID On Login
        return flask.redirect(flask.url_for('index_page',uid=uid))
    else:
        flask.flash('Incorrect Credentials')
        return flask.redirect(flask.url_for('login'))


# ------- Login Required -------

@app.route('/index/<uid>',methods=['GET','POST'])
@login_required
def index_page(uid):
    '''Load Landing Page
        returns: index home page
    '''
     

    liked_books = []
    dislike_books =[]
    preferences = PersonPreference.query.filter_by(uid=uid).all()    
    for p in preferences:
        if p.isLike is False:
            dislike_books.append(p.book_id)
        else:
            liked_books.append(p.book_id)
    # print(dislike_books, liked_books)
    
    i = 1
    rec_titles,rec_isbn,rec_book_url,rec_book_author = br.get_list_of_books(uid, liked_books=liked_books,disliked_books=dislike_books)
    
    for isbn in rec_isbn:
        # print(str(int(isbn)) + ":" +str(i))
        try:
            if int(isbn) in liked_books:
                i+=1
            if int(isbn) in dislike_books:
                i+=1
        except:
            i += 1
            # pass
        
    return flask.render_template(
        'index.html',
        uid=uid,
        book_id=rec_isbn[i],
        book_title=rec_titles[i],
        book_def=rec_book_author[i],
        img_path=rec_book_url[i]
        )


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response

@app.route('/handle_dislike_submit', methods=["GET","POST"])
def handle_dislike_submit():
    print("dislike")
    dislike_input = flask.request.form
    dislike_book_id = dislike_input['book_id']
    uid = dislike_input['uid']
    print(uid, dislike_book_id)
    person_preference = PersonPreference(uid=uid,book_id=dislike_book_id,isLike=0)
    db.session.add(person_preference)
    db.session.commit()
    
    return flask.redirect(flask.url_for('index_page',uid=uid))
    
@app.route('/handle_like_submit', methods=["GET","POST"])
def handle_like_submit():
    
    like_input = flask.request.form
    like_book_id = like_input['book_id']
    uid = like_input['uid']
    # print(uid, like_book_id)
    person_preference = PersonPreference(uid=uid,book_id=like_book_id,isLike=1)
    db.session.add(person_preference)
    db.session.commit()
    return flask.redirect(flask.url_for('index_page',uid=uid))
   

if __name__ == "__main__":
#     # Run App
    app.run(debug=True)
