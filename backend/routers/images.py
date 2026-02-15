import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.genai import Client
import models, schemas, utils
from database import get_db
from google.genai import types
from IPython.display import display, Markdown
import pathlib
from dotenv import load_dotenv

load_dotenv() # loads environment variables from a .env file into the environment, this is useful for keeping sensitive information like API keys out of the source code


router = APIRouter(prefix="/images", tags=["Images"])

# Naya Client Initialization
apiKey = os.getenv("GOOGLE_API_KEY")
client = Client(api_key=f'{apiKey}')
MODEL_NAME = "gemini-3-flash-preview"

# Loop over all parts and display them either as text or images
def display_response(response):
  for part in response.parts:
    if part.thought: # We don't want to see the thoughts
      continue
    if part.text:
      display(Markdown(part.text))
      print('text displayed ', part.text)
    elif image:= part.as_image():
      image.show()
      print('image displayed working')

# Save the image
# If there are multiple ones, only the last one will be saved
def save_image(response, path):
  for part in response.parts:
    if image:= part.as_image():
      image.save(path)
      print(f'image saved working')

UPLOAD_DIR = "/uploads"

@router.post("/generate", response_model=schemas.ImageOut)
async def generate(
    image_data: schemas.ImageCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(utils.verify_token)
):
    try:


        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=image_data.prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Image'] # response_modalities=['Image'] if you only want the images
            )
        )

        # Check if we actually got an image
        if not response.parts:
            raise HTTPException(status_code=500, detail="Model failed to generate any content.")
        has_image = any(part.as_image() for part in response.parts)
        
        if not has_image:
            raise HTTPException(status_code=500, detail="Model failed to generate an actual image.")

        file_name = f"{uuid.uuid4()}.png"
        save_path = os.path.join("uploads", file_name)
        save_image(response, save_path)


        # 4. MySQL entry
        new_image = models.GeneratedImage(
            prompt=image_data.prompt,
            file_path=f"/uploads/{save_path}", # Web URL path save karein
            owner_id=current_user.id
        )
        
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return new_image

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation Error: {str(e)}")
    
@router.get("/{image_id}", response_model=schemas.ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(utils.verify_token)):
    image = db.query(models.GeneratedImage).filter(models.GeneratedImage.id == image_id, models.GeneratedImage.owner_id == current_user.id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image