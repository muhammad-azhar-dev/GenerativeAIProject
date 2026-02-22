from sqlalchemy import create_engine # used for connecting to the database
from sqlalchemy.ext.declarative import declarative_base # used for creating the base class for our models
from sqlalchemy.orm import sessionmaker # used for creating a session factory that will be used to create sessions for interacting with the database

# XAMPP default is usually root with no password and the database name is creative_studio_db, you can change it according to your setup
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/creative_studio_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base() 

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Database Connection Error")
    finally:
        db.close()