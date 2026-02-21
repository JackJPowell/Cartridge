from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Game, GameCreate, GameUpdate

router = APIRouter()


@router.get("/", response_model=List[Game])
def list_games(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    games = session.exec(select(Game).offset(offset).limit(limit)).all()
    return games


@router.get("/{game_id}", response_model=Game)
def get_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=Game, status_code=201)
def create_game(game: GameCreate, session: Session = Depends(get_session)):
    db_game = Game.model_validate(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


@router.patch("/{game_id}", response_model=Game)
def update_game(
    game_id: int, game_update: GameUpdate, session: Session = Depends(get_session)
):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game_data = game_update.model_dump(exclude_unset=True)
    for key, value in game_data.items():
        setattr(game, key, value)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    session.delete(game)
    session.commit()
