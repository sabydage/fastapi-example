from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #hashing for password


def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) #the function pwd_context performs the logic of hashing the plain password to compare if it is identitical to the hashed password
    