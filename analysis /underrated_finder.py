import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class UnderratedBookFinder:
    def __init__(self, books_data):
        self.books_df = pd.DataFrame(books_data)
        
    def find_underrated_gems(self, min_reviews=50):
        """Find books with high ratings but low review counts"""
        # Clean data
        df = self.books_df.copy()
        df = df[df['rating'] != 'N/A']
        df = df[df['review_count'] != 'N/A']
        
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
        df = df.dropna()
        
        # Filter by minimum reviews
        df = df[df['review_count'] >= min_reviews]
        
        if len(df) == 0:
            return pd.DataFrame()
        
        # Normalize metrics
        scaler = MinMaxScaler()
        df[['rating_norm', 'review_count_norm']] = scaler.fit_transform(
            df[['rating', 'review_count']]
        )
        
        # Calculate underrated score (high rating, low reviews)
        df['underrated_score'] = df['rating_norm'] * (1 - df['review_count_norm'])
        
        # Get top underrated books
        underrated_books = df.nlargest(10, 'underrated_score')
        
        return underrated_books[['title', 'author', 'rating', 'review_count', 'underrated_score']]
    
    def find_high_rated_low_popularity(self, rating_threshold=4.0, max_reviews=1000):
        """Find high-rated books with relatively low popularity"""
        df = self.books_df.copy()
        df = df[df['rating'] != 'N/A']
        df = df[df['review_count'] != 'N/A']
        
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
        df = df.dropna()
        
        filtered_books = df[
            (df['rating'] >= rating_threshold) & 
            (df['review_count'] <= max_reviews)
        ]
        
        return filtered_books.nlargest(10, 'rating')
