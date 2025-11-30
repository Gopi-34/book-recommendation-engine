import pandas as pd

def get_popular_books(books_data, min_reviews=1000):
    df = pd.DataFrame(books_data)
    df = df[df['review_count'] != 'N/A']
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
    df = df.dropna()
    popular_books = df[df['review_count'] >= min_reviews]
    return popular_books.nlargest(10, 'rating')
