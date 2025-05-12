from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nome:  str
    email: EmailStr
    senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
