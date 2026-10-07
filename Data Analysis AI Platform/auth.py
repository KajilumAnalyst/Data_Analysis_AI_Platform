from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserOut, Token
from app.security import hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    return {"id": "user-demo-1", "email": user.email, "name": user.name, "status": "active"}

@router.post("/login", response_model=Token)
async def login():
    token = create_access_token({"sub": "maya@northwind.example", "role": "Admin", "org_id": "org-1"})
    return {"access_token": token, "token_type": "bearer"}
