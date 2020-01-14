# Project 1

Web Programming with Python and JavaScript

Steps to install and run:
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



