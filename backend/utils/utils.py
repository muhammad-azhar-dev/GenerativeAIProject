from jose import JWTError, jwt 
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session 
import models.models as models
from database.database import get_db 

SECRET_KEY = "azharshaikh123"
ALGORITHM = "HS256"      
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def create_token(user_id:int):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM) 

def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        user_id: int = payload.get("user_id") # extract the user_id from the payload
        if user_id is None:
            raise credentials_exception 
    except JWTError:
        raise credentials_exception 

    user = db.query(models.User).filter(models.User.id == user_id).first() # query the database to find a user with the extracted user_id
    if user is None:
        raise credentials_exception # if no user is found with the given user_id, raise the credentials_exception defined earlier

    return user # if everything is valid and a user is found, return the user object

