from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models.models as models, schemas.schemas as schemas
from database.database import get_db
from utils.utils import verify_token
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db),
              current_user: models.User = Depends(verify_token) # <--- Security happens here
              ):
    users = db.query(models.User).all()
    return users

# Change User Password
@router.put("/change-password")
def change_password(password_data: schemas.ChangePassword, 
                    db: Session = Depends(get_db), 
                    current_user: models.User = Depends(verify_token)):
    # 1. Verify the 'old_password' against the stored hash
    # check_password_hash(hash, plain_text) -> returns True/False
    if not check_password_hash(current_user.password, password_data.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The current password you entered is incorrect."
        )
    # 3. Hash the new password
    # generate_password_hash(plain_text) -> returns hashed string
    new_hashed_password = generate_password_hash(password_data.password)
    
    # 4. Update the MySQL database
    current_user.password = new_hashed_password
    db.commit()
    
    return {"message": "Password updated successfully!"}

# Update User Profile
# Update User Name and Email
@router.put("/update-profile")
def update_profile(
    profile_data: schemas.UpdateProfile, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(verify_token)
):
    # 1. Check if the new email is already taken by another user (if email is being updated)
    if profile_data.email != current_user.email:
        email_exists = db.query(models.User).filter(models.User.email == profile_data.email).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user."
            )

    # 2. Update the user's profile information in the database
    try:
        current_user.username = profile_data.username
        current_user.email = profile_data.email
        
        db.commit()
        db.refresh(current_user) # Updated data user object mein load karne ke liye
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed. Database error."
        )

    return {"message": "Profile updated successfully!", "user": {"name": current_user.username, "email": current_user.email}}