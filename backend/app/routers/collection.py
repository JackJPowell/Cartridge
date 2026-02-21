from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import CollectionEntry, CollectionEntryCreate, CollectionEntryUpdate

router = APIRouter()


@router.get("/", response_model=List[CollectionEntry])
def list_collection(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    entries = session.exec(select(CollectionEntry).offset(offset).limit(limit)).all()
    return entries


@router.get("/{entry_id}", response_model=CollectionEntry)
def get_entry(entry_id: int, session: Session = Depends(get_session)):
    entry = session.get(CollectionEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Collection entry not found")
    return entry


@router.post("/", response_model=CollectionEntry, status_code=201)
def create_entry(entry: CollectionEntryCreate, session: Session = Depends(get_session)):
    db_entry = CollectionEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry


@router.patch("/{entry_id}", response_model=CollectionEntry)
def update_entry(
    entry_id: int,
    entry_update: CollectionEntryUpdate,
    session: Session = Depends(get_session),
):
    entry = session.get(CollectionEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Collection entry not found")
    entry_data = entry_update.model_dump(exclude_unset=True)
    for key, value in entry_data.items():
        setattr(entry, key, value)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int, session: Session = Depends(get_session)):
    entry = session.get(CollectionEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Collection entry not found")
    session.delete(entry)
    session.commit()
