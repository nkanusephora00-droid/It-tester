from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user, get_db

router = APIRouter()


@router.get("/")
def get_habilitations(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Habilitation).all()


@router.post("/")
def create_habilitation(compte_id: int = Body(...), permission: str = Body(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_compte = db.query(models.Compte).filter(models.Compte.id == compte_id).first()
    if db_compte is None:
        raise HTTPException(status_code=404, detail="Compte not found")
    db_habilitation = models.Habilitation(compte_id=compte_id, permission=permission)
    db.add(db_habilitation)
    db.commit()
    db.refresh(db_habilitation)
    return db_habilitation


@router.delete("/{habilitation_id}")
def delete_habilitation(habilitation_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_habilitation = db.query(models.Habilitation).filter(models.Habilitation.id == habilitation_id).first()
    if db_habilitation is None:
        raise HTTPException(status_code=404, detail="Habilitation not found")
    db.delete(db_habilitation)
    db.commit()
    return {"message": "Habilitation deleted"}
