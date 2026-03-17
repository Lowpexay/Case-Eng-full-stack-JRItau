from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import get_current_user
from app.services import game_service

router = APIRouter(prefix="/games", tags=["Jogo"])


@router.post("/start", response_model=schemas.GameStart, status_code=201)
def start_game(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Inicia uma nova partida para o usuário autenticado."""
    game = game_service.start_game(current_user, db)
    return game


@router.post("/{game_id}/attempt")
def submit_attempt(
    game_id: str,
    data: schemas.AttemptIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Submete uma tentativa para a partida especificada.
    Retorna o resultado da tentativa (acertos de posição e cor), 
    sem revelar o código secreto até o fim da partida.
    """
    return game_service.submit_attempt(game_id, data, current_user, db)


@router.get("/{game_id}", response_model=schemas.GameOut)
def get_game(
    game_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retorna o estado atual de uma partida."""
    game = game_service.get_game(game_id, current_user, db)
    game_dict = {
        "id": game.id,
        "user_id": game.user_id,
        "attempts": game.attempts or [],
        "attempt_count": len(game.attempts or []),
        "score": game.score,
        "duration_seconds": game.duration_seconds,
        "started_at": game.started_at,
        "finished_at": game.finished_at,
        "is_won": game.is_won,
        "is_finished": game.is_finished,
    }
    return game_dict


@router.get("/", response_model=List[schemas.GameOut])
def list_games(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Lista as partidas finalizadas do usuário."""
    games = game_service.get_user_games(current_user, db)
    return [
        {
            "id": g.id,
            "user_id": g.user_id,
            "attempts": g.attempts or [],
            "attempt_count": len(g.attempts or []),
            "score": g.score,
            "duration_seconds": g.duration_seconds,
            "started_at": g.started_at,
            "finished_at": g.finished_at,
            "is_won": g.is_won,
            "is_finished": g.is_finished,
        }
        for g in games
    ]
