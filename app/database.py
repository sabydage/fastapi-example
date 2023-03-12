from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#structure
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
#bad practice to leave values here because it will be public under github. Also, we set the url to the local machine so creates problem when we go to production environment
#now use environment variables
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()


#create dependency, responsible for talking with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# the below is useful when we want to use raw SQL queries
# while True:
#     # connect to database
#     try:
#         conn = psycopg2.connect(host= 'hostname' , database = 'databasename', user = 'username', password= 'password', cursor_factory=RealDictCursor) #bad practice to hard coded here, better to store them in environment variables
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print("connecting to database failed. the error")
#         print("Error: ", error)
#         time.sleep(2)