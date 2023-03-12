########################################################################
#############Learning from Youtube video (19 hour) #####################
########https://www.youtube.com/watch?v=0sOvCWFmrtA#####################
####### the demo API is about interacting with social media ############
########################################################################



#create a virtual environment specific to this file in the terminal (NAME IS UNIQUE TO THE FOLDER, SO YOU CAN RE-USE THE SAME NAME VENV AGAIN)
# py -3 -m venv <name of virtual environment>

#change the python interpreter
#view/command pallet/python select interpreter
#enter path for the python.exe in the venv file
# in our case it is .\venv\Scripts\python.exe

###########################
######## STEP 1 ###########
###########################
#then write in the terminal 
#venv\Scripts\activate.bat

#tutorial page from the teacher 
#https://fastapi.tiangolo.com/tutorial/
###########################
#### END OF STEP 1 ########
###########################


#run this in the terminal
#pip install fastapi[all]

#still in terminal, type in the following command to show all packages
#pip freeze
#you can also see them in the Lib folder in the virtual environment

#from typing import Optional, List
from fastapi import FastAPI #, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.params import Body
#from pydantic import BaseModel
#from random import randrange

#import time#
from . import models#, schemas, utils # "." means current app directory

from .database import engine#, get_db
#from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings

# no longer need the command below because we are using Alembic tool now.
# models.Base.metadata.create_all(bind = engine)



app = FastAPI()

#list of all domains that can correspond to our API
origins = ["*"] # we can restrict this list for security purposes

# for a public API, use the following commands as a wild card
# origins = ["*"]


app.add_middleware(
    CORSMiddleware, # this terms is used in most web frameworks
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # we could allow specific request like if we would have a public API, we would maybe put GET as the only allowed request
    allow_headers=["*"],
)



#instead of using a database yet, we create a global variable (array)
#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id":2}]

#basic python language to find a post (before we started to work with databases)
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i # return the index of that specific id

#use the router 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# the teacher says the code below is path operation or route
# the teacher puts a lot of emphasis about the path operations, because utilmately the API is a bunch of path operations
#decorator + HTTP METHOD + PATH (URL) that we have to go to in the url, so if named "/login" then the user would have to go to the page HTTPS.../login to access the API
@app.get("/")
# async is optional and means asynchronous task
#async def root(): 
#function below root is an arbitrary name, we have to have a function as descriptive as possible
def root():
    return {"message": "welcome to my api 123456789!!!"}


###########################
######## STEP 2 ###########
###########################
# Look at the last script #
###########################
# now start the web server, run this in terminal
# uvicorn main:app
# then you'll see your IP address
# copy the IP address and paste it in your web browser, you'll see hello world.. this means that everything works
# each time you make a change to the code, you'll have to restart the server: in the terminal hit CTRL+C and user the uvicorn main:app script again
# if that is annoying, you can run uvicorn main:app --reload 
# reload is good in a development phase, but not for go live (production version) because the code is not going to change
# now that I am looking back to this code from the future, need to add the folder contained in main.py, like this uvicorn app.main:app --reload 
###########################
#### END OF STEP 2 ########
###########################


#the teacher thinks the main.py file is getting too big/cluttered so he wants to break out the file into two files
#the teacher will use routers to organize the code a little bit better



# now the teacher gets into user authentication
# 2 main ways
# 1) session -based 
# 2) JWT Token : stateless, nothing on our back-end or database that keeps track. Stored in the front end (client-side). NOT ENCRYPTED
########### Token consists of header, payload and the signature (signature = payload + header + secret)


# at 8:56:00 the teacher shows us how to make use of environment variables so that we do not have to store confidential information in our code
# step 1: in search bar, search for "environment" and click on "edit the system environment variables"
# step 2: go to "environment variables" under the "advanced" section
# step 3: you'll see two sections, system variables, and user-specific variables. 
# step 4: you can add new
# BUT THE TEACHER SAYS THERE IS ANOTHER WAY TO ADD ENVIRONMENT VARIABLES WITHOUT GOING TO GO THROUGH THIS PROCESS
# the teacher says that with any project, you will have a certain number of environment variables and the number can grow overtime
# the teacher says it is important to perform a validation to make sure all environment variables exist. 
# remember that all environment variables are strings
# This validation is done in our schemas.py file so we can use pygantic to validate this environment variables


# at 11:14:00 the teacher mentions Postman is great, but it is important to understand that the request is sent from local computer and in reality the requests are going to come from multiple devices (a web driver)
# web browsers can generate another behaviour and we need to account for that
# you can test by sending through the CONSOLE (when you inspect a page) and run this command :fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
# Cross Origin Resource Sharing (CORS)
# By default, our API will only allow web browsers running on the same domain as our server to make requests to it
# to allow external servers to be able to run on our API, the teacher starts by pointing us to the documentation : https://fastapi.tiangolo.com/tutorial/cors/?h=cors

# 11:23:00 the teacher mentions that we'll set up GIT as well as a remote repository . this is going to make the whole deployment phase easier 
# watch out GIT checks in all files by default and there are going to be files that you do not want files to uploaded (like personal ones)
# we created a new file called ".gitignore" with the following content inside
#__pycache__
#venv/
#.env
# so important to note that once files are checked in, really hard to delete them.
# teacher mentions that we do not want the ven/ folder containing our virtual environment checked in because 1) heavy and 2) does not make sense because other users would create their own virtual environment
# but if we do not include venv/ a problem arises as in the other user would not know what libraries and version number to use to replicate the API.
# a solution to this is save a copy of those in a file using the following command: pip freeze > requirements.txt
# now if another programmer wants to clone our repository and be able to reproduce, he only needs to run the following command : pip install -r requirements.txt
# now the teacher wants us to install and set up Git on our local machine
# the only special thing we've done is change the path from "master" to "main" because that is new thing to do
# once it is install, test that it is well installed by opening up a new cmd windown and run the following command: git --version
# if it spits out a number, that means it is properly installed.
# after creating an account on Git, this is the list of things that pop up with nice code examples to follow:
""" …or create a new repository on the command line
echo "# fastapi-example" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/sabydage/fastapi-example.git
git push -u origin main

…or push an existing repository from the command line
git remote add origin https://github.com/sabydage/fastapi-example.git
git branch -M main
git push -u origin main

…or import code from another repository
You can initialize this repository with code from a Subversion, Mercurial, or TFS project. """

# after running "git init", it created a folder inside a project documents with the hidden file ".git". Make sure you to select "View" and check "hidden items".
# then we ran "git add --all" and no need to worry about the warning message
# then we ran git commit -m "initial commit"
# if it is the first time you use this account, needs to provide your name like this git config --global user.email "you@example.com"
# and run this command too git config --global user.name "your username on Github"
# then use git branch -M main
# then ran: git remote add origin https://github.com/sabydage/fastapi-example.git
# then ran git push -u origin main
# then we authenticated it worked and we verify that our code was now successfully hosted on Github

# exploring HEROKU as a web platform and apparently it is not free anymore. 
# created an account and dowloaded windows version here:https://devcenter.heroku.com/articles/getting-started-with-python#set-up
# then had to restart all terminals and ran: heroku --version
# then after it spit out a version number we ran: heroku login 
# then just press enter and login using web browser
# then going back to the tutorial. No need to worry about the app because we already have an app
# we ran: heroku create --help
# then we ran the same command with the app name (keep in mind that app name is global so unique): heroku create fastapi-sabydage
# had to add a credit card first 
# then we ran: git remote
# we see that hekoru and origin has been added. so instead of running git push origin main, we'll use:git push heroku main 
# the command above will take some time
# then gave us the url name: https://fastapi-sabydage.herokuapp.com/
# then an error appear on the page and the teacher says it's normal because there needs to be a few things changed before it works.
# the app does not know it has to start. It does know it's an API. so we have to create a file that tells heroku what steps are needed. Procfile created and mentioned in the heroku tutorial
# we pushed the new files to Git hub and then to Heroku using the following commands
# git add --all
# git commit -m "added procfile"
# git push origin main
# git push heroku main
# then the application still does not work, but the teacher know what is wrong 
# anytime the application is not working, heroku has an easy of access logs with the following command: heroku logs -t
# based on the error messages, we see Settings and errors regarding username and password because we did not check in our .env file.
# so we need to add those environment variables through the command line or the dashboard. Before we can do that, we need to set up a postgres database
# heroku provides us with a free postgres instance : https://devcenter.heroku.com/articles/provisioning-heroku-postgres
# then run the following command: heroku addons:create heroku-postgresql:mini --help
# then teacher says we do not need to provide any additional flag so just run this command: heroku addons:create heroku-postgresql:mini
# then back in our Heroku account, we can click on the database and open up settings, view credentials we now see the Host and Database names. Copy this information.
# then go back into main application still on Heroku account. Go into Settings and see the Config Vars. It is where we provide our environment variables to our instance. Heroku calls our instance "dynos"
# right now if you view the config vars, there should only be one "Database_URL"
# the teacher will want to take the environment variable "Database_URL" and break it into smaller components. Basically, we added all variables contained in our .env file
# now we restart our heroku instance using the following command: heroku ps:restart
# then running: heroku logs -t
# if ever you forget the url of your app, you can run this command to get it back: heroku apps:info fastapi-sabydage
# so this works https://fastapi-sabydage.herokuapp.com/
# let's go to our documentation https://fastapi-sabydage.herokuapp.com/docs
# when testing our API and trying to create a user, we get an internal server error
# go back to our logs to check
# teacher says it has to go with our postgres 
# the teacher made us open pgadmin and we register a new server. We selected our name custom and then in the connection tab we used the same parameters as the credentials on Heroku
# then he made us expand databases and there are a ton of databases! can only access your own. You have to search for it manually.
# when you open SChemas/Public/tables, we see that there are no tables. So this is the main reason why our application is not working. This is where alembic is going to come into play
# we ARE GOIN TO RUN this command: alembic upgrade head
# it is important to understand that we NEVER run alembic revision on our PRODUCTION server. we only do that on a DEVELOPMENT SERVER and then we push out our code.
# the teacher now says how are we going to run this command on our production server.
# the teacher refers to this documentation to do that: https://devcenter.heroku.com/articles/getting-started-with-python#start-a-console
# now we run: heroku run "alembic upgrade head"
# then the teacher wants to restart our application just in case we crashed it beforehand: heroku ps:restart
# now go back to docs and try it out. We see that we can successfully created a new user and it appears in pgadmin
# last thing the teacher wants to show us is our to push out changes to our application
# first push out the changes to git hub repository: 
# git add --all
# git commit -m "changing the world"
# git push origin main
# then finally push to our production environment
# git push heroku main
# so that is pushed out now.
# keep in mind that this is the steps you have to do when you change your code, but if you change alembic, same changes but on top of that, we have to do the 
#  heroku run alembic upgrade head so that we push the changes to postgres instance.