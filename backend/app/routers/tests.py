from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user, get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class TestBase(BaseModel):
    session_id: Optional[int] = None
    application_id: int
    application_nom: Optional[str] = None
    version: Optional[str] = None
    environnement: Optional[str] = None
    fonction: str
    precondition: Optional[str] = None
    etapes: Optional[str] = None
    resultat_attendu: Optional[str] = None
    resultat_obtenu: Optional[str] = None
    statut: str
    commentaires: Optional[str] = None


class TestResponse(TestBase):
    id: int

    class Config:
        from_attributes = True


@router.get("/")
def get_tests(
    session_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if session_id:
        return db.query(models.Test).filter(models.Test.session_id == session_id).all()
    return db.query(models.Test).all()


@router.post("/")
def create_test(test: TestBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if test.application_id and test.application_id != 0:
        db_application = db.query(models.Application).filter(models.Application.id == test.application_id).first()
        if db_application is None:
            raise HTTPException(status_code=404, detail="Application not found")

    if test.session_id:
        db_session = db.query(models.TestSession).filter(models.TestSession.id == test.session_id).first()
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")

    app_id = test.application_id if test.application_id and test.application_id != 0 else None

    db_test = models.Test(
        session_id=test.session_id,
        application_id=app_id,
        application_nom=test.application_nom,
        version=test.version,
        environnement=test.environnement,
        fonction=test.fonction,
        precondition=test.precondition,
        etapes=test.etapes,
        resultat_attendu=test.resultat_attendu,
        resultat_obtenu=test.resultat_obtenu,
        statut=test.statut,
        commentaires=test.commentaires,
        created_by=current_user.id
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


@router.put("/{test_id}")
def update_test(test_id: int, test: TestBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")

    db_test.session_id = test.session_id
    db_test.application_id = test.application_id
    db_test.application_nom = test.application_nom
    db_test.version = test.version
    db_test.environnement = test.environnement
    db_test.fonction = test.fonction
    db_test.precondition = test.precondition
    db_test.etapes = test.etapes
    db_test.resultat_attendu = test.resultat_attendu
    db_test.resultat_obtenu = test.resultat_obtenu
    db_test.statut = test.statut
    db_test.commentaires = test.commentaires

    db.commit()
    db.refresh(db_test)
    return db_test


@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(db_test)
    db.commit()
    return {"message": "Test deleted"}
