from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

# at 10:31:00, the teacher mentions that there is a limitation with SQLAlchemy. Basically when you want to add/remove columns and the table already exists, the table is not going to change. 
# in other words, it only checks if the table already exists. So the teacher is going to show us a tool to counter that limitation: Alembic. Very powerful. Allow for incremental changes. Database Migrations tools. Allow to roll back our changes at any time. 
# Alembic documentation: https://alembic.sqlalchemy.org/en/latest/
# teacher suggests to follow along in the tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html
# did pip install alembic in the command line (while pressing CLTR+C to stop the API) 
# and can do alembic --help  
# teacher says first thing to do is we have to initialize init                Initialize a new scripts directory. . 
# so we ran "alembic init alembic"
# then go into the new folder and open the file env.py we have to change a few things in there
# then we went into alembic.ini to do one thing is to change the URL 
# then the teacher explains to recreate the tables in posgres using alembic and we'll need to create revision (when we make a change to our database)
# then the teacher indicates we can run "alembic revision --help" and we would only care about -m to create a message associated with each message
# so we run "alembic revision -m "create post table"  "


# running "alembic current" was giving me an authentication error and tried to solve it by changing the value from "scram-sha-256" to "trust" in this file C:\Program Files\PostgreSQL\15\data\pg_hba.conf
# it worked so continuing what the teacher is telling us

# then the teacher made us run "alembic upgrade c891dc50f51d"
# when taking a look at postgres we see that it did add the table posts for us

# now we want to add more columns to that table so we run another revision by running the following command: alembic revision -m "add content column to posts table"

# if you want to downgrade to an earlier version run this command: alembic downgrade earlierVersionName

# you can also upgrade to the latest version using "alembic upgrade head" or use "alembic upgrade +1" to upgrade to the version above

# now the teacher is saying to generate the votes table we'll use alembic's intelligent features which alows automatic generation of columns.... it's going to use our models.py to figure out what's missing and what needs to be added.
# for that we run this command: alembic revision --autogenerate -m "auto-vote"


#SQLalchemy model which is different from the schema
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable =False )
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published= Column(Boolean, server_default = 'True', nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable = False)

    #now the teacher wants to set up a relationship
    owner = relationship("User") # return another class. So that is creates a new owner property. Great part about SQLAlchemy!

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable =False )
    email = Column(String, nullable = False, unique = True)
    password= Column(String, nullable  = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default = text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True)