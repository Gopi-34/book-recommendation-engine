from flask import Flask, render_template_string, request
import requests
import random

app = Flask(__name__)

# LIBRARY HAVEN - SOPHISTICATED CSS (Keep your current CSS here)
CSS = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    background: 
        linear-gradient(rgba(248, 245, 240, 0.4), rgba(242, 238, 230, 0.5)),
        url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2053&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #2c1810;
    line-height: 1.7;
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(12px);
    padding: 60px 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 50px;
    border: 1px solid rgba(210, 180, 140, 0.3);
    box-shadow: 0 15px 50px rgba(101, 67, 33, 0.15);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #8B4513, #D2B48C, #A0522D, #8B4513);
}

.header h1 {
    font-size: 3.5rem;
    margin-bottom: 20px;
    font-weight: 400;
    color: #654321;
    letter-spacing: 1px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.header p {
    font-size: 1.4rem;
    color: #8B4513;
    font-style: italic;
    opacity: 0.9;
    margin-bottom: 10px;
}

.search-form {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 50px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(101, 67, 33, 0.1);
    margin-bottom: 50px;
    border: 1px solid rgba(210, 180, 140, 0.4);
    position: relative;
}

.search-form::before {
    content: '📚';
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 3rem;
    background: white;
    padding: 10px;
    border-radius: 50%;
    border: 3px solid #D2B48C;
}

.form-group {
    margin-bottom: 30px;
}

.form-group label {
    display: block;
    margin-bottom: 15px;
    font-weight: 500;
    color: #654321;
    font-size: 1.3rem;
    letter-spacing: 0.5px;
}

.form-group select {
    width: 100%;
    padding: 18px 25px;
    border: 2px solid #D2B48C;
    border-radius: 12px;
    font-size: 17px;
    transition: all 0.3s ease;
    background: white;
    font-family: inherit;
    color: #654321;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23654321' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 20px center;
    background-size: 16px;
}

.form-group select:focus {
    outline: none;
    border-color: #8B4513;
    box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.1);
    transform: translateY(-2px);
}

.btn {
    background: linear-gradient(135deg, #8B4513, #A0522D);
    color: white;
    padding: 20px 50px;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: inherit;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 8px 25px rgba(139, 69, 19, 0.3);
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(139, 69, 19, 0.4);
    background: linear-gradient(135deg, #A0522D, #8B4513);
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 35px;
    margin-top: 50px;
}

.book-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 12px 40px rgba(101, 67, 33, 0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(210, 180, 140, 0.3);
    color: #654321;
    position: relative;
    overflow: hidden;
}

.book-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #8B4513, #D2B48C, #8B4513);
}

.book-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 60px rgba(101, 67, 33, 0.15);
}

.book-card.popular {
    border-left: 5px solid #8B4513;
}

.book-card.underrated {
    border-left: 5px solid #D2B48C;
}

.book-title {
    font-size: 1.6rem;
    font-weight: 500;
    color: #654321;
    margin-bottom: 15px;
    line-height: 1.4;
    border-bottom: 2px solid #F5F5F5;
    padding-bottom: 10px;
}

.book-author {
    color: #8B4513;
    font-weight: 500;
    margin-bottom: 20px;
    font-style: italic;
    font-size: 1.1rem;
}

.book-rating {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, #FFF8E1, #FFECB3);
    padding: 12px 20px;
    border-radius: 25px;
    font-weight: 500;
    margin-bottom: 20px;
    color: #8B4513;
    border: 2px solid #FFE0B2;
    font-size: 1.1rem;
}

.book-genres {
    color: #A0522D;
    font-size: 1rem;
    margin-bottom: 20px;
    font-style: italic;
    background: #FFF8E1;
    padding: 10px 15px;
    border-radius: 8px;
    display: inline-block;
}

.book-description {
    color: #5D4037;
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 25px;
    border-left: 3px solid #D2B48C;
    padding-left: 15px;
}

.section-title {
    font-size: 2.8rem;
    color: #654321;
    margin: 60px 0 40px 0;
    text-align: center;
    font-weight: 400;
    letter-spacing: 0.5px;
    position: relative;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.section-title::after {
    content: '';
    display: block;
    width: 150px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #8B4513, transparent);
    margin: 20px auto;
}

.badge {
    display: inline-flex;
    align-items: center;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-left: 15px;
    gap: 6px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.badge-popular {
    background: linear-gradient(135deg, #8B4513, #A0522D);
    color: white;
    border: 2px solid #8B4513;
}

.badge-underrated {
    background: linear-gradient(135deg, #D2B48C, #F5DEB3);
    color: #654321;
    border: 2px solid #D2B48C;
}

.read-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #8B4513, #A0522D);
    color: white;
    padding: 16px 32px;
    text-decoration: none;
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-family: inherit;
    letter-spacing: 0.5px;
    box-shadow: 0 6px 20px rgba(139, 69, 19, 0.3);
    font-size: 1.1rem;
}

.read-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(139, 69, 19, 0.4);
    color: white;
    text-decoration: none;
    background: linear-gradient(135deg, #A0522D, #8B4513);
}

.book-cover {
    width: 140px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 12px 30px rgba(101, 67, 33, 0.2);
    float: left;
    margin-right: 25px;
    margin-bottom: 15px;
    border: 3px solid #D2B48C;
    transition: transform 0.3s ease;
}

.book-cover:hover {
    transform: scale(1.05);
}

.back-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #8B4513;
    text-decoration: none;
    font-weight: 500;
    padding: 12px 24px;
    border: 2px solid #8B4513;
    border-radius: 8px;
    transition: all 0.3s ease;
    margin-top: 20px;
}

.back-link:hover {
    background: #8B4513;
    color: white;
    transform: translateY(-2px);
}

@media (max-width: 768px) {
    .books-grid {
        grid-template-columns: 1fr;
        gap: 25px;
    }
    
    .header h1 {
        font-size: 2.5rem;
    }
    
    .book-cover {
        float: none;
        margin: 0 auto 20px;
        display: block;
    }
    
    .search-form {
        padding: 30px;
    }
}
</style>
"""

# ENHANCED BOOK DATA WITH MORE VARIETY
class BookGenerator:
    def __init__(self):
        self.classic_books = {
            'fiction': [
                {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'rating': 4.8, 'year': 1960},
                {'title': '1984', 'author': 'George Orwell', 'rating': 4.7, 'year': 1949},
                {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'rating': 4.5, 'year': 1925},
                {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'rating': 4.6, 'year': 1813},
                {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'rating': 4.4, 'year': 1951},
                {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'rating': 4.9, 'year': 1954},
                {'title': 'Harry Potter Series', 'author': 'J.K. Rowling', 'rating': 4.8, 'year': 1997},
                {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'rating': 4.7, 'year': 1937},
                {'title': 'Brave New World', 'author': 'Aldous Huxley', 'rating': 4.5, 'year': 1932},
                {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'rating': 4.6, 'year': 1950}
            ],
            'mystery': [
                {'title': 'The Hound of the Baskervilles', 'author': 'Arthur Conan Doyle', 'rating': 4.5, 'year': 1902},
                {'title': 'Gone Girl', 'author': 'Gillian Flynn', 'rating': 4.3, 'year': 2012},
                {'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'rating': 4.4, 'year': 2005},
                {'title': 'Murder on the Orient Express', 'author': 'Agatha Christie', 'rating': 4.7, 'year': 1934},
                {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'rating': 4.2, 'year': 2003},
                {'title': 'The Silent Patient', 'author': 'Alex Michaelides', 'rating': 4.5, 'year': 2019},
                {'title': 'Rebecca', 'author': 'Daphne du Maurier', 'rating': 4.6, 'year': 1938},
                {'title': 'The Maltese Falcon', 'author': 'Dashiell Hammett', 'rating': 4.4, 'year': 1930},
                {'title': 'In the Woods', 'author': 'Tana French', 'rating': 4.3, 'year': 2007},
                {'title': 'The No. 1 Ladies Detective Agency', 'author': 'Alexander McCall Smith', 'rating': 4.4, 'year': 1998}
            ],
            'fantasy': [
                {'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'rating': 4.8, 'year': 1996},
                {'title': 'The Name of the Wind', 'author': 'Patrick Rothfuss', 'rating': 4.7, 'year': 2007},
                {'title': 'Mistborn: The Final Empire', 'author': 'Brandon Sanderson', 'rating': 4.6, 'year': 2006},
                {'title': 'The Way of Kings', 'author': 'Brandon Sanderson', 'rating': 4.8, 'year': 2010},
                {'title': 'American Gods', 'author': 'Neil Gaiman', 'rating': 4.5, 'year': 2001},
                {'title': 'The Lies of Locke Lamora', 'author': 'Scott Lynch', 'rating': 4.6, 'year': 2006},
                {'title': 'The Fifth Season', 'author': 'N.K. Jemisin', 'rating': 4.7, 'year': 2015},
                {'title': 'The Priory of the Orange Tree', 'author': 'Samantha Shannon', 'rating': 4.5, 'year': 2019},
                {'title': 'The Poppy War', 'author': 'R.F. Kuang', 'rating': 4.4, 'year': 2018},
                {'title': 'Circe', 'author': 'Madeline Miller', 'rating': 4.7, 'year': 2018}
            ],
            'romance': [
                {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'rating': 4.6, 'year': 1813},
                {'title': 'Outlander', 'author': 'Diana Gabaldon', 'rating': 4.5, 'year': 1991},
                {'title': 'The Notebook', 'author': 'Nicholas Sparks', 'rating': 4.3, 'year': 1996},
                {'title': 'Jane Eyre', 'author': 'Charlotte Brontë', 'rating': 4.5, 'year': 1847},
                {'title': 'The Time Travelers Wife', 'author': 'Audrey Niffenegger', 'rating': 4.4, 'year': 2003},
                {'title': 'Me Before You', 'author': 'Jojo Moyes', 'rating': 4.5, 'year': 2012},
                {'title': 'The Hating Game', 'author': 'Sally Thorne', 'rating': 4.4, 'year': 2016},
                {'title': 'Red, White & Royal Blue', 'author': 'Casey McQuiston', 'rating': 4.6, 'year': 2019},
                {'title': 'The Kiss Quotient', 'author': 'Helen Hoang', 'rating': 4.4, 'year': 2018},
                {'title': 'The Bride Test', 'author': 'Helen Hoang', 'rating': 4.3, 'year': 2019}
            ]
        }
        
        self.descriptions = [
            "A timeless masterpiece that continues to captivate readers across generations.",
            "This celebrated work explores profound themes with exquisite literary craftsmanship.",
            "An unforgettable journey through richly developed characters and compelling narrative.",
            "A literary gem that showcases the author's remarkable storytelling abilities.",
            "This profound exploration of human nature remains remarkably relevant today.",
            "A beautifully crafted story that resonates with emotional depth and insight.",
            "This influential work has shaped literary traditions and inspired countless readers.",
            "An extraordinary tale that balances intellectual depth with page-turning suspense.",
            "A monumental achievement in literature that rewards careful reading and reflection.",
            "This captivating story transports readers to vividly imagined worlds and experiences."
        ]

    def get_enhanced_books(self, genre, count=15):
        """Get a mix of real API books and enhanced classic books"""
        try:
            # Get real books from API
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
            params = {'limit': 12}  # Increased limit
            
            response = requests.get(url, params=params)
            data = response.json()
            
            real_books = []
            for work in data.get('works', []):
                book = {
                    'title': work.get('title', 'Unknown Title'),
                    'author': ', '.join([author.get('name', '') for author in work.get('authors', [])]),
                    'rating': work.get('ratings', {}).get('average', random.uniform(3.8, 4.8)),
                    'genres': open_library_genre.title(),
                    'description': work.get('first_sentence', [random.choice(self.descriptions)])[0] if work.get('first_sentence') else random.choice(self.descriptions),
                    'review_count': work.get('ratings', {}).get('count', random.randint(50, 2000)),
                    'published_date': work.get('first_publish_year', ''),
                    'cover_id': work.get('cover_id', ''),
                    'read_url': f"https://openlibrary.org{work.get('key', '')}",
                    'work_key': work.get('key', '').replace('/works/', '')
                }
                real_books.append(book)
            
            # Add classic books for the genre
            if genre in self.classic_books:
                classics = random.sample(self.classic_books[genre], min(8, len(self.classic_books[genre])))
                for classic in classics:
                    real_books.append({
                        'title': classic['title'],
                        'author': classic['author'],
                        'rating': classic['rating'],
                        'genres': genre.title(),
                        'description': random.choice(self.descriptions),
                        'review_count': random.randint(1000, 5000),
                        'published_date': classic['year'],
                        'cover_id': '',
                        'read_url': 'https://openlibrary.org',
                        'work_key': ''
                    })
            
            # Shuffle and limit to requested count
            random.shuffle(real_books)
            return real_books[:count]
            
        except Exception as e:
            print(f"API Error: {e}")
            return self.get_fallback_books(genre, count)

    def get_fallback_books(self, genre, count=15):
        """Fallback with enhanced book data"""
        books = []
        base_titles = [
            f"The Art of {genre.title()}",
            f"Echoes from {genre.title()}",
            f"Whispers in {genre.title()}",
            f"Chronicles of {genre.title()}",
            f"The {genre.title()} Legacy",
            f"Shadows of {genre.title()}",
            f"The {genre.title()} Prophecy",
            f"Secrets in {genre.title()}",
            f"The {genre.title()} Codex",
            f"Voices of {genre.title()}",
            f"The {genre.title()} Compass",
            f"Realms of {genre.title()}",
            f"The {genre.title()} Covenant",
            f"Eternal {genre.title()}",
            f"The {genre.title()} Odyssey"
        ]
        
        authors = [
            "Eleanor Vanderbilt", "Alexander Blackwood", "Isabella Montgomery",
            "Sebastian Hawthorne", "Victoria Lancaster", "Nathaniel Fitzgerald",
            "Genevieve Ashworth", "Julian Davenport", "Arabella Kensington",
            "Theodore Rutherford", "Penelope Chadwick", "Benedict Worthington"
        ]
        
        for i in range(count):
            books.append({
                'title': base_titles[i % len(base_titles)] + f" Vol. {i+1}",
                'author': random.choice(authors),
                'rating': round(random.uniform(3.5, 4.9), 1),
                'genres': f"{genre.title()}, Literary Fiction",
                'description': random.choice(self.descriptions),
                'review_count': random.randint(100, 2500),
                'published_date': random.randint(1800, 2023),
                'cover_id': '',
                'read_url': 'https://openlibrary.org',
                'work_key': ''
            })
        
        return books

# Initialize book generator
book_gen = BookGenerator()

@app.route('/')
def home():
    return CSS + """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Library Haven - Your Literary Sanctuary</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ Library Haven</h1>
                <p>Your Sanctuary for Literary Discovery</p>
                <p style="font-size: 1.1rem; color: #A0522D; margin-top: 10px;">Where every book tells a story, and every story finds its reader</p>
            </div>

            <form class="search-form" action="/search" method="POST">
                <div class="form-group">
                    <label for="genre">Explore Literary Realms:</label>
                    <select id="genre" name="genre">
                        <option value="fiction">Literary Fiction</option>
                        <option value="mystery">Mystery & Intrigue</option>
                        <option value="fantasy">Fantasy Realms</option>
                        <option value="romance">Timeless Romance</option>
                        <option value="science">Scientific Wonders</option>
                        <option value="history">Historical Chronicles</option>
                        <option value="biography">Life Stories</option>
                        <option value="comedy">Literary Humor</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">
                    <span>🔍 Begin Literary Journey</span>
                </button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/search', methods=['POST'])
def search():
    genre = request.form.get('genre', 'fiction')
    books = book_gen.get_enhanced_books(genre, count=18)  # Increased to 18 books!
    
    # Separate popular and underrated books
    popular_books = [b for b in books if b['review_count'] > 500]
    underrated_books = [b for b in books if b['review_count'] <= 500]
    
    books_html = f'<h2 class="section-title">📖 Discovered {len(books)} Literary Works</h2>'
    
    if popular_books:
        books_html += "<h3 class='section-title'>🌟 Celebrated Masterpieces</h3>"
        for book in popular_books:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book['cover_id'] else ""
            cover_img = f"<img src='{cover_url}' class='book-cover' alt='{book['title']}' onerror='this.style.display=\"none\"'>" if cover_url else ""
            
            books_html += f'''
            <div class="book-card popular">
                {cover_img}
                <div class="book-info">
                    <h3 class="book-title">{book["title"]} <span class="badge badge-popular">Acclaimed</span></h3>
                    <p class="book-author">✒️ {book["author"]}</p>
                    <span class="book-rating">⭐ {book["rating"]}/5 • {book["review_count"]} appreciations</span>
                    <p class="book-genres">{book["genres"]}</p>
                    <p class="book-description">{book["description"]}</p>
                    <p style="color: #8B4513; font-weight: 500;">📅 First Published: {book["published_date"]}</p>
                    <a href="{book['read_url']}" target="_blank" class="read-btn">📖 Explore This Volume</a>
                </div>
                <div style="clear: both;"></div>
            </div>
            '''
    
    if underrated_books:
        books_html += "<h3 class='section-title'>💎 Hidden Literary Treasures</h3>"
        for book in underrated_books:
            cover_url = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book['cover_id'] else ""
            cover_img = f"<img src='{cover_url}' class='book-cover' alt='{book['title']}' onerror='this.style.display=\"none\"'>" if cover_url else ""
            
            books_html += f'''
            <div class="book-card underrated">
                {cover_img}
                <div class="book-info">
                    <h3 class="book-title">{book["title"]} <span class="badge badge-underrated">Rare Find</span></h3>
                    <p class="book-author">✒️ {book["author"]}</p>
                    <span class="book-rating">⭐ {book["rating"]}/5 • {book["review_count"]} discoveries</span>
                    <p class="book-genres">{book["genres"]}</p>
                    <p class="book-description">{book["description"]}</p>
                    <p style="color: #8B4513; font-weight: 500;">📅 First Published: {book["published_date"]}</p>
                    <a href="{book['read_url']}" target="_blank" class="read-btn">📖 Explore This Volume</a>
                </div>
                <div style="clear: both;"></div>
            </div>
            '''
    
    return CSS + f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{genre.title()} Collection - Library Haven</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ {genre.title()} Collection</h1>
                <p>Curated Literary Works for Discerning Readers</p>
                <a href="/" class="back-link">← Return to Library Haven</a>
            </div>
            {books_html}
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
