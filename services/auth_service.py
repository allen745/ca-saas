from sqlalchemy.orm import Session
from models.user import CA
from core.security import hash_password, verify_password, create_access_token

def register_ca(db: Session, full_name: str, email: str, password: str, firm_name: str = None):
    existing = db.query(CA).filter(CA.email == email).first()
    if existing:
        return None

    new_ca = CA(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        firm_name=firm_name
    )
    db.add(new_ca)
    db.commit()
    db.refresh(new_ca)
    return new_ca

def login_ca(db: Session, email: str, password: str):
    ca = db.query(CA).filter(CA.email == email).first()
    if not ca or not verify_password(password, ca.hashed_password):
        return None

    token = create_access_token({"sub": str(ca.id), "email": ca.email})
    return token