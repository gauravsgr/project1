import os
import psycopg2
import requests

from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date

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
@app.route("/index.html")
def index():
    """The home page method"""
    if 'user' in session:
        return render_template("search.html")
    return render_template("index.html")



@app.route("/authenticate", methods=["POST"])
def authenticate():
    """Handles the sign in, sign up part"""
    if 'user' in session:
        render_template("search.html")

    username = request.form.get("username")
    password = request.form.get("passkey")
        
    if request.form.get("auth") == "signin":
        # SIGN IN LOGIC: Check the username and password in the auth table and save username in session   
        authuser = db.execute("SELECT * FROM auth where uname = :username and password = :password", 
                                        {"username": username, "password": password}).fetchone()
        # Checking is the user doesn't exists
        if authuser is None:
            return """<h1> User Not Found </h1> <br> <a href="/">Click here to sign in again!</a>"""        
    else:
        # SIGN UP LOGIC: Save the username and password in a database   
        db.execute("INSERT INTO auth (uname, password) VALUES (:username, :password)",
                {"username": username, "password": password}) 
        db.commit()
        
    session['user'] = username
    return render_template("search.html", user = session['user'])
    #return redirect(url_for('search'))



@app.route("/logout", methods=["POST", "GET"])
def logout():
    """"The Logout clears session and returns to index page"""
    session.clear()
    return redirect(url_for('index'))       



@app.route("/search", methods=["POST", "GET"])
def search():
    """Return the list of books that match the user search query even partially to title, author, isbn or year"""
    bookstr = request.form.get("bookstring")
    # Get all the books that match bookstring
    search_string = "SELECT * FROM books WHERE isbn LIKE " + "'%" + bookstr + "%'" + " OR title LIKE " + "'%" + bookstr + "%'" + " OR author LIKE " + "'%" + bookstr + "%'"
    books = db.execute(search_string).fetchall()
    return render_template("search.html", books=books, user = session['user'])


@app.route("/bookinfo/<string:isbn>", methods=["GET", "POST"])
def get_book_info_page(isbn):
    """Getting the book details based on ISBN and showing to the user"""
    res = requests.get("http://127.0.0.1:5000/api/bookinfo/" + isbn)
    reviews = db.execute("SELECT * FROM reviews where isbn = :isbn", 
                                    {"isbn": isbn}).fetchall()
    bookinfo = []
    bookinfo.append(res.json()["title"])
    bookinfo.append(res.json()["author"])
    bookinfo.append(res.json()["year"])
    bookinfo.append(res.json()["isbn"])
    bookinfo.append(res.json()["review_count"])
    bookinfo.append(res.json()["average_score"])
    bookinfo.append(reviews)
    # session['bookinfo'] = bookinfo
    # return render_template("bookinfo.html", bookinfo = session["bookinfo"]) //Storing bookinfo in session was causing the race condition. 
    return render_template("bookinfo.html", bookinfo = bookinfo)



@app.route("/add_review/<string:isbn>", methods=["POST", "GET"])
def add_review(isbn):
    """Add the review of the book in the database to show to all users"""
    username = session["user"]
    review = request.form.get("review")
    # If user already has a review then do nothing
    preview = db.execute("SELECT * FROM reviews where uname = :username and isbn = :isbn", 
                                    {"username": username, "isbn": isbn}).fetchone()
    # Checking is the user has already posted a review
    if preview is None:
        db.execute("INSERT INTO reviews (isbn, uname, review, date) VALUES (:isbn, :uname, :review, :date)",
                {"isbn": isbn, "uname": username, "review": review, "date": str(date.today())}) 
        db.commit() 
    return redirect(url_for('get_book_info_page', isbn = isbn))       



@app.route("/api/bookinfo/<string:isbn>", methods=["GET", "POST"])
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
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": res.json()["books"][0]["work_reviews_count"],
                "average_score": res.json()["books"][0]["average_rating"]
            })
    return resp



def main():
    """Test function"""
    print(get_book_info('5559609129')) #valid book isbn
    #print(get_book_info('12')) #invalid book isbn



if __name__ == "__main__":
    main()