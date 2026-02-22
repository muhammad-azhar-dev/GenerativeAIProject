from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from utils import verify_token

rounter = APIRouter(
    prefix="/users",
    tags=["users"]
)

@rounter.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db),
              current_user: models.User = Depends(verify_token) # <--- Security happens here
              ):
    users = db.query(models.User).all()
    return users