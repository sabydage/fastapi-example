from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])

# post because we want to receive data from user
@router.post('/login', response_model=schemas.Token)
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)): # udpatig this row when started to use oauth credentials
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #starting with oauth documentation in the form of a dictionary, so we have to make somes changes to the below code
    #username 
    #password

    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    # here, instead of using the body arguments (in postman) with "raw", we'll pass them using the "form-data" view which ressembles a tabular format and is different from the Headers section.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    


    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password ):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials") # LET THEM FIGURE OUT IF THE USER OR PASSWORD IS INCORRECT

    # create a tokent 
    # return a token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id}) # here we could provide more data
    #return {"token": "Example token"} 
    return {"access_token" : access_token, "token_type" : "bearer"} 