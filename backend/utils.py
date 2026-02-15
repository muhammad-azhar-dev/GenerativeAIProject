from jose import JWTError, jwt # used for encoding and decoding JSON Web Tokens (JWTs), JWTError is used to handle errors that may occur during the encoding or decoding process, and jwt is used to perform the actual encoding and decoding of JWTs
from fastapi import Depends, HTTPException, status # used for handling dependencies and exceptions in our FastAPI application, Depends is used to declare dependencies for our API endpoints, HTTPException is used to raise HTTP exceptions with specific status codes and messages, and status is used to provide standard HTTP status codes
from fastapi.security import OAuth2PasswordBearer # used for implementing OAuth2 authentication in our FastAPI application, it provides a way to handle token-based authentication using the OAuth2 protocol
from sqlalchemy.orm import Session # used for working with database sessions in SQLAlchemy, it allows us to interact with the database and perform operations such as querying and committing changes
import models
from database import get_db 

SECRET_KEY = "azharshaikh123"
ALGORITHM = "HS256"      
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # create an instance of the OAuth2PasswordBearer class, this will be used to handle token-based authentication in our API endpoints, the tokenUrl parameter specifies the URL where clients can obtain a token for authentication 

def create_token(user_id:int):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM) # create a JWT token by encoding the user_id using the secret key and the specified algorithm

def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) # create an HTTPException that will be raised if the token is invalid or if there is an error during the verification process, it sets the status code to 401 Unauthorized and provides a detail message and a header indicating that the authentication scheme is Bearer

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # decode the JWT token using the secret key and the specified algorithm, this will return the payload contained in the token if it is valid
        user_id: int = payload.get("user_id") # extract the user_id from the payload
        if user_id is None:
            raise credentials_exception 
    except JWTError:
        raise credentials_exception # if there is an error during the decoding process (e.g., invalid token, expired token), raise the credentials_exception defined earlier

    user = db.query(models.User).filter(models.User.id == user_id).first() # query the database to find a user with the extracted user_id
    if user is None:
        raise credentials_exception # if no user is found with the given user_id, raise the credentials_exception defined earlier

    return user # if everything is valid and a user is found, return the user object

