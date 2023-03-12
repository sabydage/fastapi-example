from .. import models, schemas, oauth2 # "." means current app directory
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import  List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", # this allows us not to add this word on every path 
    tags = ['Posts'] # so that the documentation has this group (more organized)
)


# now using ORM instead of raw sql queries
# sqlalchemy is one of the most popular python ORms

#create another path operation
# and always use plural because it is a standard API convention
#@app.get('/posts', response_model= List[schemas.Post])
#@router.get('/', response_model= List[schemas.Post])
#@router.get('/') # removing the response model to see what it looks like temporarily 
@router.get('/', response_model= List[schemas.PostOut])
#def get_posts(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
def get_posts(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 10 , skip: int = 0, 
search: Optional[str] = ""): # now we add a query parameter to the end point to determine the numnber of posts the user wants to fetch. To use this new limit parameter in postman, in the endpoint we add "?limit=10&skip=1&search=welc"
#to mimic a space in the Postman query parameters, add the following "%20"    
    #return {"data":"This is a list of post"}
    
    # RAW SQL 
#def get_posts():
    #cursor.execute(""" SELECT * FROM posts """)
    #posts=cursor.fetchall()
    print(limit)
    #posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # adding the new query variables

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results) # this is to see what the raw SQL query is


    #if you would want to return the posts only for that user, use the query below
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #print(posts)
    #return {"data": posts} #return array to PostMan
    return posts #return array to PostMan
# go to http://127.0.0.1:8000/posts to see the results

#the teacher made us download postman and use this tool instead of the web browser from now on because Postman interface is nice to use and make it easier to test

#@app.post('/posts') #this is bad practice code according to teacher, but will get fixed later
#@app.post('/posts', status_code=201) #add a status code because according to documentation, when we create an object we have to return a 201 code
#@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model= schemas.Post) 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
#def create_posts(payLoad: dict = Body(...)): #add arguments to retrieve body data. Payload is the name of the variable. Take the Body and converting into a python library.
#def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): #automatically validate based on the model defined above
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #add a dependency to validate if user is allowed to post

    #print(payLoad)
    #print(new_post.title) #look how it is easy to access data!
    #print(post.dict()) #convert pydantic model to dictionary. This is a handy tool ! 
    #return {"new_post": f"Title {payLoad['title']} content: {payLoad['content']} "} #how to extract that data and send back in... but in a real application we would store data in a database
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,1000000)
    #my_posts.append(post_dict)
    #return {"data": post_dict}

    # RAW SQL 
    #cursor.execute(""" INSERT INTO posts (title,content, published) VALUES  (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published )) #the %s is sanitizing and prevent SQL injection so this method is good   
    #new_post = cursor.fetchone()
    #conn.commit() #to actually save the change and finalize it


    #new_post=models.Post(title = post.title, content = post.content, published = post.published) #this method is inefficient if we would have 50 fields
    #so use more efficient method that consists in unpacking the dictionary 
    #print(current_user.id)
    #print(current_user.email)

    #new_post=models.Post(**post.dict()) 
    new_post=models.Post(owner_id = current_user.id, **post.dict())  # now adding the user id here so that we create a post 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
#in postman, if you want to send data, do to 'Body' and select 'raw' then select 'JSON' rather than text because it is the most popular one.
#the format in JSON looks like the below 
#{
    #"title":"top beaches in Florida",
    #content":"check out this beach"
# }

#now we'll us pydantic that was automatically installed when all flag pip installfast api
#find it in the lib folder
#this is used to define a schema
#we want the following one
# title str, content str

#@app.get("/posts/{id}", response_model= schemas.Post)
#@router.get("/{id}", response_model= schemas.Post)
@router.get("/{id}", response_model= schemas.PostOut)

#def get_post(id):
def get_post(id: int, response: Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): # here we perform a data validation
    #print(id)
    #post= find_post(int(id)) # convert to int because a string by default

    # RAW SQL
    #cursor.execute("""SELECT * FROM posts where id = %s """, (str(id),)) #make sure you add this comma at the end
    #post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()


    #if you would want to return the posts only for that user, use the query below
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action" )

    #post= find_post(id) 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found"
        )
        #response.status_code = 404 # see http status code for all the avaiable codes
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    #return {"post_detail": f"here is post {id}"}
    return  post

#@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # RAQ SQL 
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post= cursor.fetchone()
    #conn.commit()

    #post = db.query(models.Post).filter(models.Post.id == id)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    #index = find_index_post(id)
    #if index == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exit")
    #my_posts.pop(index)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exit")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action" )

    post_query.delete(synchronize_session=False)
    db.commit()

    #return {"message": "post was sucessfully dleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)



#@app.put("/posts/{id}", response_model= schemas.Post)
@router.put("/{id}", response_model= schemas.Post)

def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # RAW SQL 
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where ID = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()

    #index = find_index_post(id)

    #if index == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exit")



    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exit")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action" )

    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()

    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict

    #return{"data": post_dict}
    return post_query.first()

# fastapi has a built-in support for documentation (swagger UI support). This is practical because we do not have to update the documentation manually
# to see the documentation, go to http://127.0.0.1:8000/docs
# to see the documentation another format of the documentation, go to http://127.0.0.1:8000/redoc

# now the teacher wants to create an app folder so that the file main.py is part of the app folder.
# the way python works is with packages... package = folder so we have created app folder and then created the file named __init__.py to turn this to a proper python package

# stop the terminal using ctrl + C and then use this new commmand to open the main file because it has changed location: uvicorn app.main:app --reload

# now we dive into using a database and we'll use a relational one : POSTGRESQL
# after downloading postgresql, we'll interact with the database using pgadmin so if you search through windows you'll be able to find this


# teacher says there is an alternative using Objet Relational Mapper (ORM) that uses Python language that is converted into SQL after. This is good when you want to avoid SQL.
# the most popular ORM is SQL Alchemy
# I will go through SQL Alchemy because the teacher uses it, but I like SQL so I could avoid using SQL alchemy

# pip freeze commmand is used to see all packages installed 


# at 7:43:00  in the video, the teacher starts to talk about a feature in PostMan called Environments. This allows to go back and forth between prod and dev environments
# we create a new environment to store the variable "URL" with value of my local server "http://127.0.0.1:8000/"
# then when sending a get posts request we changed the value from  "http://127.0.0.1:8000/posts" to "{{URL}}posts"
#
# the other thing the teacher adds to API, is the bearer token integrated faster than just copy the bearer token and passt in the authorization or the body
# the teacher first foes into the login user end point and in the "Tests" section we try to set up an environment variable. In there, there are test snippets of code and we chose "set an environment variable" and the code below came out
# pm.environment.set("variable_key", "variable_value");
# the teacher changed this to that pm.environment.set("JWT", pm.response.json().access_token); 
# then go in the get posts end point and reference the {{JWT}} variable in the authorization section