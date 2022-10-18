- Clone the Repo
 $ git clone git@github.com:jugooo/milestone-1.git

  run: $ python -m pip install -r requirements.txt

  start local server: python nnguyen-swe-milestone.py

- Link to fly.io
  frosty-flower-1453.fly.dev

- Problems:
  Problem: In logs error message 'Module requests not found'
    Solution: Add requests and python-dotenv to requirements.txt
    Resources used: Team Discord
  Problem: When running $ fly deploy recieved error with ' FLY API TOKEN REQUEST ID' (Not the same as my APIS)
    Solution: rerun flyctl launch
    Resources: Googled Error API TOKEN REQUEST ID

- Additional Features
  - Feature: Would like the user to see the list of the top 10 movies trending, allow the user to select, and present user with more useful links 
    such as streaming suggestions, movie theaters showing times, ratings, etc..
    - I orignially had the list of the top 10 movies implemented, but it did not go with the assignment details. 
    - To implement streaming suggestions, find an API or resource that lists legal streaming platforms to display, for illegal streaming I would find 
      reliable websites and discover how they set movie id's to bring the user directly to the movie
    - Ratings and Movie Times in the area, I would need to allow location tracking and get API's for movie theatres and ratings