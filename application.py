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
@app.route("/index.html")
def index():
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
    if 'user' in session:
        session.pop('user', None) # delete user info from session
        return render_template("index.html")



@app.route("/search", methods=["POST", "GET"])
def search():
    bookstr = request.form.get("bookstring")
    
    # Get all the books that match bookstring
    # search_string = "SELECT * FROM books WHERE isbn LIKE " + "'\%" + bookstr + "\%'" + " OR WHERE title LIKE " + "'\%" + bookstr + "\%'" + " OR WHERE author LIKE " + "'\%" + bookstr + "\%'"
    search_string = "SELECT * FROM books WHERE author = '" + bookstr +"'"
    books = db.execute(search_string).fetchall()
    
    return render_template("search.html", books=books, user = session['user'])


@app.route("/bookinfo/<string:isbn>", methods=["GET"])
def get_book_info_page(isbn):
    
    res = requests.get("http://127.0.0.1:5000/api/bookinfo/" + isbn)
    title = res.json()["title"]
    author = res.json()["author"]
    year = res.json()["year"]
    isbn = res.json()["isbn"]
    review_count = res.json()["review_count"]
    average_score = res.json()["average_score"]
    #print(title + '|' + author + '|' + year + '|' + isbn + '|' + review_count + '|' + average_score) """
    return render_template("bookinfo.html", title=title, author=author, year=year, isbn=isbn, review_count=review_count, average_score=average_score)



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
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": res.json()["books"][0]["work_reviews_count"],
                "average_score": res.json()["books"][0]["average_rating"]
            })
    return resp


def test():
    print("Hello World")


def main():
    print(get_book_info('5559609129')) #valid book isbn
    #print(get_book_info('12')) #invalid book isbn
    #print(test())


if __name__ == "__main__":
    main()