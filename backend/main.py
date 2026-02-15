from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # used for handling Cross-Origin Resource Sharing (CORS) in our FastAPI application, it allows us to specify which origins are allowed to access our API and what methods and headers are permitted in cross-origin requests
from routers import auth, images # importing the auth and images routers from the routers module, these routers will handle the authentication and image-related endpoints of our API
import models
import database
from dotenv import load_dotenv

load_dotenv() # loads environment variables from a .env file into the environment, this is useful for keeping sensitive information like API keys out of the source code

# create database tables based on the models defined in the models module, this will create the necessary tables in the database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Creative Studio AI")

# CORS middleware ko add karna, isse hum specify kar sakte hain ki kaunse origins humare API ko access kar sakte hain, aur kaunse methods aur headers cross-origin requests mein allowed hain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins to access the API, you can specify specific origins if you want to restrict access
    allow_credentials=True, # allow cookies and other credentials to be included in cross-origin requests
    allow_methods=["*"], # allow all HTTP methods (GET, POST, PUT, DELETE, etc.) in cross-origin requests
    allow_headers=["*"], # allow all headers in cross-origin requests
)

@app.get("/")
def homeroot():
    return {"message": "Welcome to Creative Studio API"}


# Routers ko include karna
app.include_router(auth.router)
app.include_router(images.router)

@app.get("/")
def home():
    return {"message": "Welcome to Creative Studio API"}