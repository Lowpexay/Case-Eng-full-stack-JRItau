from fastapi import APIRouter, Depends

from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Retorna os dados do usuário autenticado."""
    return current_user
