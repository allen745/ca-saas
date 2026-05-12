from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth_schema import CARegister, CALogin, Token
from services.auth_service import register_ca, login_ca

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: CARegister, db: Session = Depends(get_db)):
    ca = register_ca(db, data.full_name, data.email, data.password, data.firm_name)
    if not ca:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "Registered successfully", "id": ca.id}

@router.post("/login", response_model=Token)
def login(data: CALogin, db: Session = Depends(get_db)):
    token = login_ca(db, data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": token, "token_type": "bearer"}