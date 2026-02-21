from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class GameBase(SQLModel):
    igdb_id: int
    title: str
    developer: Optional[str] = None
    publisher: Optional[str] = None
    release_date: Optional[date] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    cover_url: Optional[str] = None
    igdb_rating: Optional[float] = None
    summary: Optional[str] = None


class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    igdb_id: int = Field(unique=True)


class GameCreate(GameBase):
    pass


class GameUpdate(SQLModel):
    igdb_id: Optional[int] = None
    title: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    release_date: Optional[date] = None
    genre: Optional[str] = None
    platform: Optional[str] = None
    cover_url: Optional[str] = None
    igdb_rating: Optional[float] = None
    summary: Optional[str] = None


class CollectionEntryBase(SQLModel):
    game_id: int = Field(foreign_key="game.id")
    date_added: date = Field(default_factory=date.today)
    date_played: Optional[date] = None
    my_score: Optional[float] = None  # 1–10
    status: Optional[str] = None  # "completed", "playing", "backlog", "wishlist"
    notes: Optional[str] = None
    physical: bool = True


class CollectionEntry(CollectionEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CollectionEntryCreate(CollectionEntryBase):
    pass


class CollectionEntryUpdate(SQLModel):
    game_id: Optional[int] = None
    date_added: Optional[date] = None
    date_played: Optional[date] = None
    my_score: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    physical: Optional[bool] = None
