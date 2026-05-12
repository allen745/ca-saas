from pydantic import BaseModel, EmailStr

class CARegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    firm_name: str | None = None

class CALogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str