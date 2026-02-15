from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, utils
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists in the database
    existing_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(user.password)
    
    # Create a new user instance and add it to the database
    new_user = models.User(
        username=user.username, 
        email=user.email, 
        password=hashed_password 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists in the database
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    
    # Verify the password
    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    
    token = utils.create_token(db_user.id) # create a JWT token for the authenticated user using the create_token function defined in the utils module, passing the user's ID as an argument
    
    return {
        "access_token": token, # return the generated token in the response
        "token_type": "bearer", # specify the type of token being returned (in this case, a bearer token)
        "user": {"id": db_user.id, "username": db_user.username, "email": db_user.email} # return the authenticated user's information in the response
    }
