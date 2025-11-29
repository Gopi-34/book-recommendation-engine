import pandas as pd
import re
from typing import List, Dict

class DataProcessor:
    def __init__(self):
        pass
    
    def clean_book_data(self, books_data: List[Dict]) -> List[Dict]:
        """Clean and normalize book data"""
        cleaned_books = []
        
        for book in books_data:
            cleaned_book = self._clean_single_book(book)
            if cleaned_book:
                cleaned_books.append(cleaned_book)
        
        return cleaned_books
    
    def _clean_single_book(self, book: Dict) -> Dict:
        """Clean individual book record"""
        try:
            # Clean title
            title = book.get('title', '').strip()
            if not title or title == 'N/A':
                return None
            
            # Clean author
            author = book.get('author', '').strip()
            if not author or author == 'N/A':
                author = 'Unknown Author'
            
            # Clean rating
            rating = self._clean_rating(book.get('rating', 0))
            
            # Clean genres
            genres = self._clean_genres(book.get('genres', ''))
            
            # Clean description
            description = self._clean_description(book.get('description', ''))
            
            # Clean review count
            review_count = self._clean_review_count(book.get('review_count', 0))
            
            return {
                'title': title,
                'author': author,
                'rating': rating,
                'genres': genres,
                'description': description,
                'review_count': review_count,
                'similar_books': book.get('similar_books', ''),
                'book_url': book.get('book_url', '')
            }
            
        except Exception as e:
            print(f"Error cleaning book data: {e}")
            return None
    
    def _clean_rating(self, rating) -> float:
        """Convert rating to float between 0-5"""
        try:
            if isinstance(rating, (int, float)):
                return min(max(float(rating), 0), 5)
            elif isinstance(rating, str):
                # Extract numbers from strings like "4.25" or "4.25 avg rating"
                numbers = re.findall(r'\d+\.\d+|\d+', rating)
                if numbers:
                    return min(max(float(numbers[0]), 0), 5)
            return 0.0
        except:
            return 0.0
    
    def _clean_genres(self, genres: str) -> str:
        """Clean and format genres"""
        if not genres or genres == 'N/A':
            return 'Unknown Genre'
        
        # Remove extra spaces and duplicates
        genre_list = [genre.strip() for genre in str(genres).split(',')]
        unique_genres = list(dict.fromkeys(genre_list))  # Preserve order
        return ', '.join(unique_genres[:3])  # Keep only top 3 genres
    
    def _clean_description(self, description: str) -> str:
        """Clean book description"""
        if not description or description == 'N/A':
            return 'No description available'
        
        # Remove extra whitespace and limit length
        cleaned = ' '.join(description.split())
        if len(cleaned) > 300:
            cleaned = cleaned[:297] + '...'
        
        return cleaned
    
    def _clean_review_count(self, review_count) -> int:
        """Convert review count to integer"""
        try:
            if isinstance(review_count, int):
                return max(0, review_count)
            elif isinstance(review_count, str):
                # Extract numbers from strings like "1,234 reviews"
                numbers = re.findall(r'\d+', review_count.replace(',', ''))
                if numbers:
                    return max(0, int(numbers[0]))
            return 0
        except:
            return 0
    
    def filter_books(self, books_data: List[Dict], 
                    min_rating: float = 3.0, 
                    min_reviews: int = 10) -> List[Dict]:
        """Filter books based on criteria"""
        return [
            book for book in books_data 
            if book.get('rating', 0) >= min_rating 
            and book.get('review_count', 0) >= min_reviews
        ]
    
    def export_to_csv(self, books_data: List[Dict], filename: str = 'books_data.csv'):
        """Export book data to CSV"""
        try:
            df = pd.DataFrame(books_data)
            df.to_csv(filename, index=False)
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def export_to_json(self, books_data: List[Dict], filename: str = 'books_data.json'):
        """Export book data to JSON"""
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(books_data, f, indent=2, ensure_ascii=False)
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
