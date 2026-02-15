from sqlalchemy import create_engine # used for connecting to the database
from sqlalchemy.ext.declarative import declarative_base # used for creating the base class for our models
from sqlalchemy.orm import sessionmaker # used for creating a session factory that will be used to create sessions for interacting with the database

# XAMPP default is usually root with no password and the database name is creative_studio_db, you can change it according to your setup
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/creative_studio_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # create an engine that will be used to connect to the database, the URL is passed as an argument to specify the database type and connection details

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a session factory that will be used to create sessions for interacting with the database, autocommit and autoflush are set to False to ensure that changes are not automatically committed or flushed to the database, and bind is set to the engine created earlier to specify the connection details

Base = declarative_base() # create a base class for our models, this will be used to define our database tables and their relationships, it provides a way to define the structure of our database and allows us to create models that can be used to interact with the database

def get_db(): # this function is a generator that will be used to get a database session, it creates a new session using the SessionLocal factory and yields it, allowing us to use it in our API endpoints, and ensures that the session is closed after we are done using it
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()