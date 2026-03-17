from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, security


def register_user(data: schemas.UserRegister, db: Session) -> models.User:
    if db.query(models.User).filter(models.User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso.")
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="E-mail já está em uso.")

    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=security.hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(data: schemas.UserLogin, db: Session) -> str:
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique seu usuário e senha.",
        )
    token = security.create_access_token(
        {"sub": user.id},
        expires_delta=timedelta(minutes=60),
    )
    return token
