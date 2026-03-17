from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.security import get_current_user
from app.services import game_service

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("/", response_model=List[schemas.RankingEntry])
def get_ranking(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """Retorna o ranking global ordenado por melhor pontuação."""
    return game_service.get_ranking(db, limit)
