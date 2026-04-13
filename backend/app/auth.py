from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .security import verify_password, hash_password
from .database import SessionLocal
from . import models
import secrets

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Module-level cache for SECRET_KEY
_SECRET_KEY: str | None = None


def get_secret_key() -> str:
    global _SECRET_KEY
    if _SECRET_KEY is not None:
        return _SECRET_KEY

    db = SessionLocal()
    try:
        setting = db.query(models.Setting).filter(models.Setting.key == "SECRET_KEY").first()
        if setting:
            _SECRET_KEY = setting.value
        else:
            new_key = secrets.token_hex(32)
            new_setting = models.Setting(key="SECRET_KEY", value=new_key)
            db.add(new_setting)
            db.commit()
            _SECRET_KEY = new_key
        return _SECRET_KEY
    finally:
        db.close()


def refresh_secret_key():
    global _SECRET_KEY
    _SECRET_KEY = None
    return get_secret_key()


# Modèle Pydantic pour les données du token
class TokenData(BaseModel):
    username: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_test_user(username: str, email: str, password: str, db: Session):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return existing_user

    hashed_password = hash_password(password)
    user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_demo_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "demo_user"}, expires_delta=access_token_expires
    )
    return access_token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pas assez de permissions"
        )
    return current_user
