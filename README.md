- Clone the Repo
 $ git clone git@github.com:jugooo/milestone-1.git

  run: $ python -m pip install -r requirements.txt

  start local server: python nnguyen-swe-milestone.py

- Link to fly.io
  swe-milestone.fly.dev

- Description:
  I wanted to design this app to randomly select the top 10 movies that are currently trending, so users can get a random movie to watch.
  Often times people have a hard time finding a movie to watch, so the idea of the website is to fix that. 
  However, when you submit a review the page refreshes and the user can not see their review.
  To see the review in the current version of the website you must press "new movie roll"


- Problems:
  - Problem: In logs error message 'Module requests not found'
    - Solution: Add requests and python-dotenv to requirements.txt
    - Resources used: Team Discord
  - Problem: When running $ fly deploy recieved error with ' FLY API TOKEN REQUEST ID' (Not the same as my APIS)
    - Solution: rerun flyctl launch
    - Resources: Googled Error API TOKEN REQUEST ID

    - Milestone 2 Debreif
      Expectations:
        - I thought I was going to be able to setup the database and pull data from it easily because I have done something very similar, but it wasn't as easy as I thought
        - I thought the login/create account steps were going to be easy also, but I since I have never set up a login through this method it wasn't as easy as I thought. I also didn't read the requirements for the project at first, so I was trying to do the password hash and store it into the database.

      Problems:
        - At first I didn't know how to correctly get the Database setup in Fly.io. After Laith released the tips and the demonatration I got a better understanding and was able to easily set it up 
        - I also couldn't figure out how extract the data from the database initally. I googled "pulling data from postgres" and looked at some examples on how they were able to display the data from the review object

- Additional Features
  - Feature: Would like the user to see the list of the top 10 movies trending, allow the user to select, and present user with more useful links 
    such as streaming suggestions, movie theaters showing times, ratings, etc..
    - I orignially had the list of the top 10 movies implemented, but it did not go with the assignment details. 
    - To implement streaming suggestions, find an API or resource that lists legal streaming platforms to display, for illegal streaming I would find 
      reliable websites and discover how they set movie id's to bring the user directly to the movie
    - Ratings and Movie Times in the area, I would need to allow location tracking and get API's for movie theatres and ratings

  - Additional Features as of Thu Nov 10
    Show a menu of 10 movie instead of cycling through the top 10. 