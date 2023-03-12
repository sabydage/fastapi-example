from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#create a schema to validate the data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default to true
    #rating: Optional[int] = None #default to nothing and we need to import a library for that

#different models for different requests can be made because each request could have different requirements
# but teacher is using a different method

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default to true
    #do not need to add the user id because we are retrieving it automatically from the token


class PostCreate(PostBase):
    #do not need to add the user id because we are retrieving it automatically from the token
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    #convert to a pygantic because otherwise interferes with alchemy 
    class Config:
        orm_mode = True

# create a new class for the response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # return a pygantic model. and make sure the "UserOut" is declared above in the code
    #convert to a pygantic because otherwise interferes with alchemy 
    class Config:
        orm_mode = True


class PostOut(BaseModel): # this is the mistake made from the teacher!! he was passing PostBase instead of BaseModel
     Post: Post
     votes: int

     class Config:
         orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
