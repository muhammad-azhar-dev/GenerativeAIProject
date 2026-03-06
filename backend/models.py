from sqlalchemy import Column, Integer, String, Text, ForeignKey 
from sqlalchemy.orm import relationship 
from database import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String(50), unique=True, index=True) 
    email = Column(String(100), unique=True, index=True) 
    password = Column(String(255)) 
    plan = Column(String, default="free") # added a plan field to track the user's subscription plan
    
    # Relationship to the content they upload
    contents = relationship("UserContent", back_populates="owner") 

class UserContent(Base):
    __tablename__ = "user_contents"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String(500)) 
    file_path = Column(String(255)) # Path to the stored .jpg, .png, or .pdf
    gemini_output = Column(Text)    # Stores the text returned by Gemini 3 Flash
    owner_id = Column(Integer, ForeignKey("users.id")) 

    owner = relationship("User", back_populates="contents")