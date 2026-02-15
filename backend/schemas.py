from pydantic import BaseModel # used for creating data models that will be used for request and response validation in our API endpoints

class UserCreate(BaseModel):
    username: str # define the username field as a string, this will be used to create a new user in the database
    email: str # define the email field as a string, this will be used to create a new user in the database
    password: str # define the password field as a string, this will be used to create a new user in the database

class UserLogin(BaseModel):
    email: str # define the email field as a string, this will be used for user login
    password: str # define the password field as a string, this will be used for user login

class UserOut(BaseModel):
    id: int # define the id field as an integer, this will be used to represent the user's unique identifier in the database
    username: str # define the username field as a string, this will be used to represent the user's username in the database
    email: str # define the email field as a string, this will be used to represent the user's email in the database

    class Config:
        orm_mode = True # enable ORM mode to allow compatibility with SQLAlchemy models

class ImageCreate(BaseModel):
    prompt: str # define the prompt field as a string, this will be used to create a new generated image in the database
    file_path: str # define the file_path field as a string, this will be used to create a new generated image in the database
    owner_id: int # define the owner_id field as an integer, this will be used to associate the generated image with a specific user in the database

class ImageOut(BaseModel):
    id: int # define the id field as an integer, this will be used to represent the generated image's unique identifier in the database
    prompt: str # define the prompt field as a string, this will be used to represent the generated image's prompt in the database
    file_path: str # define the file_path field as a string, this will be used to represent the generated image's file path in the database
    owner_id: int # define the owner_id field as an integer, this will be used to represent the generated image's associated user in the database

    class Config:
        orm_mode = True # enable ORM mode to allow compatibility with SQLAlchemy models