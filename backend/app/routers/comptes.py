from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from .. import models
from ..security import hash_password
from ..auth import get_current_user, get_db

router = APIRouter()


@router.get("/")
def get_comptes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comptes = db.query(models.Compte).options(joinedload(models.Compte.application)).all()

    result = []
    for compte in comptes:
        compte_dict = {
            "id": compte.id,
            "username": compte.username,
            "role": compte.role,
            "code": compte.code,
            "application_id": compte.application_id,
            "commentaire": compte.commentaire,
            "created_by": compte.created_by,
            "application": {
                "id": compte.application.id if compte.application else None,
                "nom": compte.application.nom if compte.application else None
            } if compte.application else None
        }
        result.append(compte_dict)

    return result


@router.post("/")
def create_compte(application_id: int = Body(...), username: str = Body(...), code: str = Body(None), role: str = Body(None), commentaire: str = Body(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_compte = models.Compte(
        application_id=application_id,
        username=username,
        code=code,
        role=role,
        commentaire=commentaire,
        created_by=current_user.id
    )
    db.add(db_compte)
    db.commit()
    db.refresh(db_compte)
    return db_compte


@router.get("/{compte_id}")
def get_compte(compte_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_compte = db.query(models.Compte).options(joinedload(models.Compte.application)).filter(models.Compte.id == compte_id).first()
    if db_compte is None:
        raise HTTPException(status_code=404, detail="Compte non trouvé")

    compte_dict = {
        "id": db_compte.id,
        "username": db_compte.username,
        "role": db_compte.role,
        "code": db_compte.code,
        "application_id": db_compte.application_id,
        "commentaire": db_compte.commentaire,
        "created_by": db_compte.created_by,
        "application": {
            "id": db_compte.application.id if db_compte.application else None,
            "nom": db_compte.application.nom if db_compte.application else None
        } if db_compte.application else None
    }

    return compte_dict


@router.put("/{compte_id}")
def update_compte(compte_id: int, application_id: int = Body(...), username: str = Body(...), code: str = Body(None), role: str = Body(None), commentaire: str = Body(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_compte = db.query(models.Compte).filter(models.Compte.id == compte_id).first()
    if db_compte is None:
        raise HTTPException(status_code=404, detail="Compte not found")

    if current_user.role != "admin" and db_compte.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this compte")

    db_compte.application_id = application_id
    db_compte.username = username
    if code is not None:
        db_compte.code = code
    db_compte.role = role
    db_compte.commentaire = commentaire
    db.commit()
    db.refresh(db_compte)
    return db_compte


@router.delete("/{compte_id}")
def delete_compte(compte_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_compte = db.query(models.Compte).filter(models.Compte.id == compte_id).first()
    if db_compte is None:
        raise HTTPException(status_code=404, detail="Compte not found")

    if current_user.role != "admin" and db_compte.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this compte")

    db.delete(db_compte)
    db.commit()
    return {"message": "Compte deleted"}
