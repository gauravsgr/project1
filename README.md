# Project 1

## Web Programming with Python and JavaScript

## Objective
In this project, I have build a book review website. Users will be able to register for my website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via my website’s API.

## Requirements
1. Registration: Users should be able to register for my website, providing (at minimum) a username and password.
2. Login: Users, once registered, should be able to log in to my website with their username and password.
3. Logout: Logged in users should be able to log out of the site.
4. Import: Provided in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from my web application, write a program that will take the books and import them into my PostgreSQL database. Decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into my database, and submit this program with the rest of my project code.
5. Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, my website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, my search page should find matches for those as well!
6. Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on my website.
7. Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
8. Goodreads Review Data: On my book page, I should also display (if available) the average rating and number of ratings the work has received from Goodreads.
9. API Access: If users make a GET request to my website’s /api/<isbn> route, where <isbn> is an ISBN number, my website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:


## Steps to install and run:
1. Run pip3 install -r requirements.txt OR install anaconda and run conda install --file requirements.txt
2. Set the environment variable FLASK_APP to be application.py
   export FLASK_APP=application.py
3. Set the DATABASE_URL as an envoirnment variable to hold the postgre database link from Heroku
   export DATABASE_URL=ReallyLongURIthatYouCanFindFromHerokuDashboardinSettingAndViewCredentials
4. [Would not have to do this if you install anaconda] Set the PYTHONPATH as an envoirnment variable to point to the location of all the packages
   export PYTHONPATH=$PYTHONPATH:/home/sgrg/.local/lib/python3.6/site-packages/
5. Set the goodreadskey as an envoirnment variable to hold the key from the Goodreads API dashboard
   export goodreadskey=SomethingNotThatLong
6. Run flask

