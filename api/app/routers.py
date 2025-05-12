from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin, Token
from auth import hash_password, verify_password, create_token, get_current_user
from requests import get

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registrar", status_code=201)
def registrar(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email já cadastrado")
    user = User(
        nome=data.nome,
        email=data.email,
        hashed_password=hash_password(data.senha)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.email)
    return {"jwt": token}

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.senha, user.hashed_password):
        raise HTTPException(401, "Credenciais inválidas")
    token = create_token(user.email)
    return {"jwt": token}

@router.get("/consultar")
def consultar(current_user: User = Depends(get_current_user)):
    resposta = get("https://economia.awesomeapi.com.br/last/USD-BRL", headers={"Authorization": "Bearer " + current_user.token}).json()
    return {"dados": resposta}
