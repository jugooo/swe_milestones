from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pandas as pd


#uid = input('UID:')
# Load book data into Pandas DataFrame
#error_bad_lines=False,
ratings = pd.read_csv('BX-CSV-Dump/BX-Book-Ratings.csv', sep=';',on_bad_lines='skip', encoding="latin-1")
# books = pd.read_csv('BX-CSV-Dump/BX-Books.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
# users = pd.read_csv('BX-CSV-Dump/BX-Users.csv', sep=';',on_bad_lines='skip', encoding="latin-1")

# Define the rating scale
reader = Reader(rating_scale=(1, 10))

# Load the data into a Surprise dataset
data = Dataset.load_from_df(ratings[['User-ID', 'ISBN', 'Book-Rating']], reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2)

# Define the SVD algorithm for recommendation
algo = SVD()

# Train the algorithm on the training set
algo.fit(trainset)
# Define a function for recommending books based on user input
def recommend_books(user_id, liked_books=[], disliked_books=[], n=30):
    # Get a list of all book ISBNs
    book_isbns = ratings['ISBN'].unique()

    # Remove books the user disliked from the list
    book_isbns = [isbn for isbn in book_isbns if isbn not in disliked_books]

    # Create a DataFrame with all book ISBNs and ratings predicted by the algorithm
    predictions = []
    for isbn in book_isbns:
        prediction = algo.predict(user_id, isbn)
        predictions.append((prediction.est, prediction.iid))
    predictions_df = pd.DataFrame(predictions, columns=['est_rating', 'ISBN'])
    
    # Sort the DataFrame by predicted rating
    predictions_df = predictions_df.sort_values('est_rating', ascending=False)

    # Remove books the user has already liked from the list
    predictions_df = predictions_df[~predictions_df['ISBN'].isin(liked_books)]

    # Return the top n recommendations
    recommendations = predictions_df['ISBN'].head(n).tolist()
    return recommendations


def get_list_of_books(uid,liked_books=[],disliked_books=[]):
    # User likes the book with ISBN '12345'
#    liked_books = ['12345']

    # User dislikes the book with ISBN '67890'
#    disliked_books = ['67890']
    

    # Get updated recommendations for the user with ID 123
    recommendations = recommend_books(uid, liked_books=liked_books, disliked_books=disliked_books)

    rec_titles = []
    rec_isbn = []
    rec_book_url = []
    rec_book_author = []
    # Print the updated recommendations
    for isbn in recommendations:
      try:
        if not isbn:
          break
        book_title = books.loc[books['ISBN'] == isbn, 'Book-Title'].values[0]
        book_URL = books.loc[books['ISBN'] == isbn, 'Image-URL-L'].values[0]
        book_author = books.loc[books['ISBN'] == isbn, 'Book-Author'].values[0]
#        print(book_URL)
        book_id = isbn #book Id
        rec_titles.append(book_title)
        rec_isbn.append(book_id)
        rec_book_url.append(book_URL)
        rec_book_author.append(book_author)
      except:
#        return get_list_of_books(uid=uid,liked_books=liked_books,disliked_books=disliked_books)
        pass
        
#    rec_titles.pop(0)
#    rec_isbn.pop(0)
    print(rec_titles[1])
    print(rec_isbn[1])
    return rec_titles, rec_isbn,rec_book_url, rec_book_author
