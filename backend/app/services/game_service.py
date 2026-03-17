import random
import logging
from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings

COLORS = list("ABCDEF")  # 6 possible colors
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

logger = logging.getLogger(__name__)


def _secret_for_log(secret: str) -> str:
    return secret if settings.DEBUG_LOG_SECRETS else "[MASKED]"


def _generate_secret() -> str:
    return "".join(random.choices(COLORS, k=CODE_LENGTH))


def _evaluate(secret: str, guess: str):
    """Return (correct_position, correct_color)."""
    correct_position = sum(s == g for s, g in zip(secret, guess))
    # correct color: count minimum occurrences per color
    correct_color = sum(min(secret.count(c), guess.count(c)) for c in COLORS) - correct_position
    return correct_position, correct_color


def _calculate_score(attempts_count: int, is_won: bool) -> int:
    if not is_won:
        return 0
    return max(0, (MAX_ATTEMPTS - attempts_count + 1) * 100)


def start_game(user: models.User, db: Session) -> models.Game:
    game = models.Game(
        user_id=user.id,
        secret_code=_generate_secret(),
        attempts=[],
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    logger.info(
        "MASTERMIND START | game_id=%s user_id=%s resposta=%s",
        game.id,
        user.id,
        _secret_for_log(game.secret_code),
    )
    return game


def submit_attempt(game_id: str, data: schemas.AttemptIn, user: models.User, db: Session) -> dict:
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    if game.user_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado.")
    if game.is_finished:
        raise HTTPException(status_code=400, detail="Esta partida já foi encerrada.")

    guess = data.guess.upper()
    if len(guess) != CODE_LENGTH or any(c not in COLORS for c in guess):
        raise HTTPException(
            status_code=400,
            detail=f"Tentativa inválida. Use {CODE_LENGTH} letras de A a F.",
        )

    correct_position, correct_color = _evaluate(game.secret_code, guess)

    attempt_entry = {
        "guess": guess,
        "correct_position": correct_position,
        "correct_color": correct_color,
    }

    attempts = list(game.attempts or [])
    attempts.append(attempt_entry)
    game.attempts = attempts

    logger.info(
        "MASTERMIND TRY | game_id=%s user_id=%s tentativa=%s guess=%s resposta=%s pos=%s cor=%s",
        game.id,
        user.id,
        len(attempts),
        guess,
        _secret_for_log(game.secret_code),
        correct_position,
        correct_color,
    )

    is_won = correct_position == CODE_LENGTH
    is_finished = is_won or len(attempts) >= MAX_ATTEMPTS

    if is_finished:
        game.is_finished = True
        game.is_won = is_won
        game.finished_at = datetime.now(timezone.utc)
        # SQLite returns naive datetimes; normalise before subtracting
        finished = game.finished_at.replace(tzinfo=None)
        started = game.started_at.replace(tzinfo=None) if game.started_at.tzinfo else game.started_at
        game.duration_seconds = (finished - started).total_seconds()
        game.score = _calculate_score(len(attempts), is_won)
        logger.info(
            "MASTERMIND END | game_id=%s user_id=%s venceu=%s score=%s resposta=%s tentativas=%s",
            game.id,
            user.id,
            is_won,
            game.score,
            _secret_for_log(game.secret_code),
            len(attempts),
        )

    db.commit()
    db.refresh(game)

    return {
        "attempt": attempt_entry,
        "attempt_number": len(attempts),
        "is_finished": is_finished,
        "is_won": is_won,
        "score": game.score,
        "secret_code": game.secret_code if is_finished else None,
        "remaining_attempts": MAX_ATTEMPTS - len(attempts),
    }


def get_game(game_id: str, user: models.User, db: Session) -> models.Game:
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    if game.user_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado.")
    logger.info(
        "MASTERMIND STATE | game_id=%s user_id=%s resposta=%s tentativas=%s finalizada=%s",
        game.id,
        user.id,
        _secret_for_log(game.secret_code),
        len(game.attempts or []),
        game.is_finished,
    )
    return game


def get_user_games(user: models.User, db: Session) -> List[models.Game]:
    return (
        db.query(models.Game)
        .filter(models.Game.user_id == user.id, models.Game.is_finished == True)
        .order_by(models.Game.finished_at.desc())
        .all()
    )


def get_ranking(db: Session, limit: int = 20) -> List[schemas.RankingEntry]:
    users = db.query(models.User).all()
    entries = []
    for user in users:
        finished_games = [g for g in user.games if g.is_finished]
        if not finished_games:
            continue
        wins = [g for g in finished_games if g.is_won]
        best_score = max((g.score or 0) for g in finished_games)
        entries.append(
            schemas.RankingEntry(
                rank=0,
                user_id=user.id,
                username=user.username,
                best_score=best_score,
                total_games=len(finished_games),
                wins=len(wins),
            )
        )

    entries.sort(key=lambda e: (-e.best_score, -e.wins, e.username))
    for i, entry in enumerate(entries):
        entry.rank = i + 1

    return entries[:limit]
