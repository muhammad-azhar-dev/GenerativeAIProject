from sqlalchemy import Column, Integer, String, ForeignKey  # used for defining the columns in our database tables, Integer and String are data types for the columns, and ForeignKey is used to define relationships between tables
from sqlalchemy.orm import relationship # used for defining relationships between tables, it allows us to specify how tables are related to each other and how they can be accessed through our models
from database import Base # import the Base class from our database module

class User(Base):
    __tablename__ = "users" # specify the name of the table in the database that this model will represent
    id = Column(Integer, primary_key=True, index=True) # define the id column as an integer, set it as the primary key, and create an index for it to improve query performance
    username = Column(String(50), unique=True, index=True) # define the username column as a string with a maximum length of 50 characters, set it to be unique to prevent duplicate usernames, and create an index for it to improve query performance
    email = Column(String(100), unique=True, index=True) # define the email column as a string with a maximum length of 100 characters, set it to be unique to prevent duplicate emails, and create an index for it to improve query performance
    password = Column(String(255)) # define the password column as a string with a maximum length of 255 characters, this will be used to store the hashed password of the user
    images = relationship("GeneratedImage", back_populates="owner") # define a relationship to the GeneratedImage model, this allows us to access the images associated with a user through the "images" attribute, and back_populates is used to specify the corresponding attribute in the GeneratedImage model that will be used to access the owner of the image

class GeneratedImage(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True) # define the id column as an integer, set it as the primary key, and create an index for it to improve query performance
    prompt = Column(String(500)) # define the prompt column as a string with a maximum length of 500 characters, this will be used to store the text prompt that was used to generate the image
    file_path = Column(String(255)) # define the file_path column as a string with a maximum length of 255 characters, this will be used to store the file path of the generated image on the server
    owner_id = Column(Integer, ForeignKey("users.id")) # define the owner_id column as an integer and set it as a foreign key that references the id column in the users table, this establishes a relationship between the GeneratedImage and User models, allowing us to associate each generated image with a specific user

    owner = relationship("User", back_populates="images") # define a relationship to the User model, this allows us to access the owner of the image through the "owner" attribute, and back_populates is used to specify the corresponding attribute in the User model that will be used to access the images associated with a user