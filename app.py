from flask import Flask, render_template, request, jsonify
from scraper.goodreads_scraper import GoodreadsScraper
from analysis.underrated_finder import UnderratedBookFinder
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_books():
    genre = request.form.get('genre', 'fiction')
    pages = int(request.form.get('pages', 2))
    
    scraper = GoodreadsScraper()
    books = scraper.scrape_popular_books(genre=genre, pages=pages)
    
    # Find underrated books
    finder = UnderratedBookFinder(books)
    underrated_books = finder.find_underrated_gems()
    
    # Convert to lists for template
    popular_books = books  # All books are considered "popular" for demo
    underrated_list = underrated_books.to_dict('records') if not underrated_books.empty else []
    
    return render_template('results.html', 
                         popular_books=popular_books,
                         underrated_books=underrated_list,
                         genre=genre)

if __name__ == '__main__':
    app.run(debug=True)
