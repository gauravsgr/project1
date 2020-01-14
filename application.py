import os
import psycopg2
import requests

from flask import Flask, session, render_template, jsonify, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO Hello World"


@app.route("/api/bookinfo/<string:isbn>", methods=["GET"])
def get_book_info(isbn):
    """Return details of a single book"""

    book = db.execute("SELECT * FROM books where ISBN = :isbn",
                        {"isbn":isbn}).fetchone()

    # Make sure book exists.    
    if book is None:
        return jsonify({"error": "Invalid book ISBN"}), 422

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("goodreadskey"), "isbns": isbn})
    
    with app.app_context():
        resp =  jsonify({
                "title": book.isbn,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": res.json()["books"][0]["work_reviews_count"],
                "average_score": res.json()["books"][0]["average_rating"]
            })
    return resp

def main():
    print(get_book_info('5559609129')) #valid book isbn
    print(get_book_info('12')) #invalid book isbn

if __name__ == "__main__":
    main()