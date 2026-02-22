import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from google import genai
from google.genai import types
from database import get_db
import models, schemas
from utils import verify_token
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()

# 1. Setup Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/generate", response_model=schemas.ContentOut)
async def generate_ai_content(
    owner_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_token) # <--- Security happens here
):
    prompt = "Please analyze the content of the attached file and provide a summary along with any insights you can gather from it."
    # Validate file type
    file_ext = file.filename.split(".")[-1].lower()
    mime_type = "application/pdf" if file_ext == "pdf" else f"image/{file_ext}"
    
    if file_ext not in ["jpg", "jpeg", "png", "pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 2. Save file locally
    file_path = os.path.join(UPLOAD_DIR, f"{owner_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 3. Call Gemini 3 Flash
        # We read the file bytes to send them directly to Gemini
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ]
        )
        
        ai_result = response.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

    # 4. Save everything to MySQL
    new_entry = models.UserContent(
        prompt=prompt,
        file_path=file_path,
        gemini_output=ai_result,
        owner_id=owner_id
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return new_entry

# 2. GET HISTORY (Only Ali sees Ali's stuff)
@router.get("/my-history", response_model=list[schemas.ContentOut])
def get_my_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_token) # <--- Security happens here
):
    # We filter by current_user.id. Ali cannot see anyone else's data.
    contents = db.query(models.UserContent).filter(
        models.UserContent.owner_id == current_user.id
    ).all()
    
    return contents