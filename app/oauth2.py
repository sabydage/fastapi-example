from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm  import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# for this file, the teacher followed the documentation from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


#SECRET_KEY  -- only reside on our server!!1
SECRET_KEY = settings.secret_key

#Algorithm
ALGORITHM = settings.algorithm


#Expiration time - users are not staying logged in forever
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):  # first part is the payload
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # dictionary to update by passing in the expire time

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=  ALGORITHM)

    return encoded_jwt
     
def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id) # here we could validate more parameters than just id
    except JWTError:
        raise credentials_exception
    
    return token_data

# idea is once the verified token is valid, the get current user fetch the correct user from the database
def get_current_user(token: str  = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail = f"Could not validate credentials", 
                                        headers= {"WWW-Authenticate" : "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    #return verify_access_token(token, credentials_exception)
    return user
#in order to use the token, in Postman, use the header section. Under "Key" type in "Authorization" and under "Value" type in "Bearer authkey" where the jebrish is the token value
# alternatively, in POSTMAN, you can go in the Authorization section, select Bearer and just paste in the token. The teacher said to user whatever method we prefer