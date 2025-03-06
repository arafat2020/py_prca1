# auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from model.user import User
from schema.user import UserCreate
from db.bd import get_db
from datetime import datetime, timedelta
import jwt
import os

from dotenv import load_dotenv

load_dotenv()

# Initialize the router
router = APIRouter()

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# JWT Token creation function
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Route to get or create a user based on clerkId and return JWT token
@router.post("/user")
def get_or_create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists based on clerkId
    existing_user = db.query(User).filter(User.clerkId == user.clerkId).first()
    
    if existing_user:
        # If user exists, generate token
        user_data = {"clerkId": existing_user.clerkId, "username": existing_user.username}
        token = create_access_token(user_data)
        return {"data": existing_user, "token": token}

    # If user does not exist, create a new one
    new_user = User(clerkId=user.clerkId, username=user.username, pic=user.pic, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create and return the token for the new user
    user_data = {"clerkId": new_user.clerkId, "username": new_user.username}
    token = create_access_token(user_data)
    return {"data": new_user, "token": token}
