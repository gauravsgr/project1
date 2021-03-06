import os
import csv
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    """Read the csv file with the books list and push it to the Postgree DB created at Heroku"""
    f = open("books.csv")
    reader = csv.reader(f)
    count = 0
    for isbn, title, author, year in reader:
        count += 1
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book # {count} Title: {title} Author: {author} year {year}")
    db.commit()

if __name__ == "__main__":
    main()