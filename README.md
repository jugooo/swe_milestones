- Clone the Repo
 $ git clone git@github.com:jugooo/swe_milestones.git

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
