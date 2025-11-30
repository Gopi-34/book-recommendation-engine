from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Inline CSS - No separate file needed!
CSS = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(rgba(44, 85, 48, 0.85), rgba(76, 124, 89, 0.85)),
                url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
    line-height: 1.6;
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 50px 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header h1 {
    font-size: 3.5rem;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #d4af37, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.header p {
    font-size: 1.3rem;
    opacity: 0.9;
    font-style: italic;
}

.search-form {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    margin-bottom: 40px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #2c5530;
    font-size: 1.1rem;
}

.form-group select {
    width: 100%;
    padding: 15px 20px;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 16px;
    transition: all 0.3s ease;
    background: white;
    font-family: inherit;
}

.form-group select:focus {
    outline: none;
    border-color: #d4af37;
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
    transform: translateY(-2px);
}

.btn {
    background: linear-gradient(135deg, #2c5530, #4a7c59);
    color: white;
    padding: 16px 40px;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: inherit;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(44, 85, 48, 0.4);
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.book-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    transition: all 0.4s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #2d3748;
}

.book-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.book-card.popular {
    border-left: 5px solid #e53e3e;
}

.book-card.underrated {
    border-left: 5px solid #d4af37;
}

.book-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2c5530;
    margin-bottom: 10px;
}

.book-author {
    color: #4a7c59;
    font-weight: 600;
    margin-bottom: 15px;
}

.book-rating {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, #fff9e6, #ffedb3);
    padding: 8px 16px;
    border-radius: 25px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #8b6914;
}

.rating-high {
    color: #2d7730;
    background: linear-gradient(135deg, #f0fff0, #d4ffd4);
}

.book-genres {
    color: #666;
    font-size: 0.95rem;
    margin-bottom: 15px;
}

.book-description {
    color: #4a5568;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 15px;
}

.section-title {
    font-size: 2.5rem;
    color: white;
    margin: 50px 0 30px 0;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.badge {
    display: inline-flex;
    align-items: center;
    padding: 6px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-left: 10px;
    gap: 5px;
}

.badge-popular {
    background: linear-gradient(135deg, #fed7d7, #feb2b2);
    color: #c53030;
}

.badge-underrated {
    background: linear-gradient(135deg, #fef5e7, #fbd38d);
    color: #744210;
}

.read-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #d4af37, #b8860b);
    color: white;
    padding: 12px 24px;
    text-decoration: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-family: inherit;
}

.read-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(212, 175, 55, 0.4);
    color: white;
    text-decoration: none;
}

.book-cover {
    width: 120px;
    height: 180px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    float: left;
    margin-right: 20px;
    margin-bottom: 10px;
}

@media (max-width: 768px) {
    .books-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .header h1 {
        font-size: 2.5rem;
    }
    
    .book-cover {
        float: none;
        margin: 0 auto 15px;
        display: block;
    }
    
    body {
        padding: 10px;
    }
}
</style>
"""

def get_open_library_books(genre, limit=10):
    """Get real books from Open Library API"""
    try:
        genre_map = {
            'fiction': 'fiction',
            'mystery': 'mystery',
            'fantasy': 'fantasy', 
            'romance': 'romance',
            'science': 'science',
            'history': 'history',
            'biography': 'biography',
            'comedy': 'humor'
        }
        
        open_library_genre = genre_map.get(genre, genre)
        url = f"https://openlibrary.org/subjects/{open_library_genre}.json"
        params = {'limit': limit}
        
        response = requests.get(url, params=params)
        data = response.json()
        
        real_books = []
        for work in data.get('works', []):
            book = {
                'title': work.get('title', 'Unknown Title'),
                'author': ', '.join([author.get('name', '') for author in work.get('authors', [])]),
                'rating': work.get('ratings', {}).get('average', 0),
                'genres': open_library_genre.title(),
                'description': work.get('first_sentence', ['No description available'])[0] if work.get('first_sentence') else 'Check Open Library for details',
                'review_count': work.get('ratings', {}).get('count', 0),
                'published_date': work.get('first_publish_year', ''),
                'cover_id': work.get('cover_id', ''),
                'read_url': f"https://openlibrary.org{work.get('key', '')}",
                'work_key': work.get('key', '').replace('/works/', '')
            }
            real_books.append(book)
        
        return real_books
        
    except Exception as e:
        print(f"API Error: {e}")
        return get_sample_books(genre)

def get_sample_books(genre):
    """Fallback sample data"""
    return [
        {
            'title': f'Great {genre.title()} Novel',
            'author': 'Classic Author',
            'rating': 4.5,
            'genres': f'{genre.title()}, Literature',
            'description': 'A wonderful book that showcases the best of this genre.',
            'review_count': 1500,
            'read_url': 'https://openlibrary.org',
            'cover_id': ''
        },
        {
            'title': f'{genre.title()} Adventure', 
            'author': 'Adventure Writer',
            'rating': 4.2,
            'genres': f'{genre.title()}, Action',
            'description': 'An exciting story full of twists and turns.',
            'review_count': 800,
            'read_url': 'https://openlibrary.org',
            'cover_id': ''
        }
    ]

@app.route('/')
def home():
    return CSS + """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Luxury Book Library</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📖 Luxury Book Library</h1>
                <p>Discover & Read Beautiful Books Online</p>
            </div>

            <form class="search-form" action="/search" method="POST">
                <div class="form-group">
                    <label for="genre">Choose Your Literary Genre:</label>
                    <select id="genre" name="genre">
                        <option value="fiction">Fiction</option>
                        <option value="mystery">Mystery & Thriller</option>
                        <option value="fantasy">Fantasy</option>
                        <option value="romance">Romance</option>
                        <option value="science">Science</option>
                        <option value="history">History</option>
                        <option value="biography">Biography</option>
                        <option value="comedy">Comedy & Humor</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">
                    <span>🔍 Discover Books</span>
                </button>
            </form>

            <div class="features">
                <h2 class="section-title">Why Choose Our Library?</h2>
                <div class="books-grid">
                    <div class="book-card">
                        <h3>🎯 Curated Selection</h3>
                        <p>Hand-picked books across all genres</p>
                    </div>
                    <div class="book-card">
                        <h3>📖 Read Instantly</h3>
                        <p>Direct links to readable editions</p>
                    </div>
                    <div class="book-card">
                        <h3>💎 Hidden Gems</h3>
                        <p>Discover underrated masterpieces</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/search', methods=['POST'])
def search():
    genre = request.form.get('genre', 'fiction')
    books = get_open_library_books(genre, limit=8)
    
    # Separate popular and underrated books
    popular_books = [b for b in books if b['review_count'] > 20]
    underrated_books = [b for b in books if b['review_count'] <= 20]
    
    books_html = f'<h2 class="section-title">📚 Found {len(books)} Books in {genre.title()}</h2>'
    
    if popular_books:
        books_html += "<h3 class='section-title'>🔥 Popular & Acclaimed</h3>"
        for book in popular_books:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book['cover_id'] else ""
            cover_img = f"<img src='{cover_url}' class='book-cover' alt='{book['title']}' onerror='this.style.display=\"none\"'>" if cover_url else ""
            
            books_html += f'''
            <div class="book-card popular">
                {cover_img}
                <div class="book-info">
                    <h3 class="book-title">{book["title"]} <span class="badge badge-popular">Popular</span></h3>
                    <p class="book-author">✍️ {book["author"]}</p>
                    <span class="book-rating rating-high">⭐ {book["rating"]}/5 • {book["review_count"]} reviews</span>
                    <p class="book-genres">{book["genres"]}</p>
                    <p class="book-description">{book["description"]}</p>
                    <p><strong>Published:</strong> {book["published_date"]}</p>
                    <a href="{book['read_url']}" target="_blank" class="read-btn">📖 Read This Book Online</a>
                </div>
                <div style="clear: both;"></div>
            </div>
            '''
    
    if underrated_books:
        books_html += "<h3 class='section-title'>💎 Hidden Literary Gems</h3>"
        for book in underrated_books:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book['cover_id'] else ""
            cover_img = f"<img src='{cover_url}' class='book-cover' alt='{book['title']}' onerror='this.style.display=\"none\"'>" if cover_url else ""
            
            books_html += f'''
            <div class="book-card underrated">
                {cover_img}
                <div class="book-info">
                    <h3 class="book-title">{book["title"]} <span class="badge badge-underrated">Hidden Gem</span></h3>
                    <p class="book-author">✍️ {book["author"]}</p>
                    <span class="book-rating">⭐ {book["rating"]}/5 • {book["review_count"]} reviews</span>
                    <p class="book-genres">{book["genres"]}</p>
                    <p class="book-description">{book["description"]}</p>
                    <p><strong>Published:</strong> {book["published_date"]}</p>
                    <a href="{book['read_url']}" target="_blank" class="read-btn">📖 Read This Book Online</a>
                </div>
                <div style="clear: both;"></div>
            </div>
            '''
    
    return CSS + f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Books in {genre.title()} - Luxury Library</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📖 {genre.title()} Collection</h1>
                <p>Curated selection of {genre} literature</p>
                <a href="/" style="color: #d4af37; text-decoration: none; font-weight: 600; display: inline-block; margin-top: 15px;">← Back to Library</a>
            </div>
            {books_html}
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
