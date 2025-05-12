import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import OperationalError
from database import SessionLocal, engine, Base
from models import User

# Carregar env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_password(pw: str, hpw: str) -> bool:
    return pwd_ctx.verify(pw, hpw)

def create_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": sub}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise creds_exc
    except JWTError:
        raise creds_exc

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    if not user:
        raise creds_exc
    return user

def init_db():
    conn = engine.connect(); conn.close()
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso")
            
