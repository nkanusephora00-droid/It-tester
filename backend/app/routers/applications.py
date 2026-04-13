from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user, get_db

router = APIRouter()


@router.get("/")
def get_applications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Application).all()


@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application


@router.post("/")
def create_application(
    nom: str = Form(...),
    description: str = Form(None),
    version: str = Form(None),
    environnement: str = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_application = models.Application(
        nom=nom,
        description=description,
        version=version,
        environnement=environnement,
        created_by=current_user.id
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.put("/{application_id}")
def update_application(
    application_id: int,
    nom: str = Form(...),
    description: str = Form(None),
    version: str = Form(None),
    environnement: str = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    if current_user.role != "admin" and db_application.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this application")

    db_application.nom = nom
    db_application.description = description
    db_application.version = version
    db_application.environnement = environnement
    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    if current_user.role != "admin" and db_application.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this application")

    db.delete(db_application)
    db.commit()
    return {"message": "Application deleted"}
