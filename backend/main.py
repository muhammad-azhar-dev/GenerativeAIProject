from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from routers import GeneratedContent, auth, users, payment_gateway
import models.models as models
import database.database as database
from dotenv import load_dotenv

load_dotenv()

# create database tables based on the models defined in the models module, this will create the necessary tables in the database
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"-------Database Connection Error------- \n{str(e)}")

app = FastAPI(title="Document Reader Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # allow all origins to access the API
    allow_credentials=True, # allow cookies and other credentials to be included in cross-origin requests
    allow_methods=["*"], # allow all HTTP methods (GET, POST, PUT, DELETE, etc.) in cross-origin requests
    allow_headers=["*"], # allow all headers in cross-origin requests
)

@app.get("/")
def homeroot():
    return {"message": "Welcome to Document Reader Assistant API"}


# Include Routers
app.include_router(auth.router)
app.include_router(GeneratedContent.router)
app.include_router(users.router)
app.include_router(payment_gateway.router)