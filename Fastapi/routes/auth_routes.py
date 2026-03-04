from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from schemas.user import UserCreate
from database import users_collection
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


# ---------------------------
# Login Request Schema
# ---------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


# ---------------------------
# Signup Route
# ---------------------------

@router.post("/signup")
async def signup(user: UserCreate):

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }

    users_collection.insert_one(new_user)

    token = create_access_token({"email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------------------
# Login Route
# ---------------------------

@router.post("/login")
async def login(user: LoginRequest):

    existing_user = users_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "email": existing_user["email"],
        "name": existing_user["name"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "name": existing_user["name"]
    }


# ---------------------------
# Logout Route
# ---------------------------

@router.post("/logout")
async def logout():

    return {
        "message": "Logged out successfully. Please remove token from client."
    }