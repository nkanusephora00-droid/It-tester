from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user, get_db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pdfplumber
import io

router = APIRouter()


class TestSessionBase(BaseModel):
    nom: str
    description: Optional[str] = None
    application_id: Optional[int] = None
    environnement: Optional[str] = None
    version: Optional[str] = None
    nom_document: Optional[str] = None
    statut: str = "En cours"


class TestSessionResponse(TestSessionBase):
    id: int
    date_creation: datetime

    class Config:
        from_attributes = True


class TestSessionWithTests(TestSessionResponse):
    tests: list = []

    class Config:
        from_attributes = True


@router.get("/")
def get_test_sessions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sessions = db.query(models.TestSession).order_by(models.TestSession.date_creation.desc()).all()
    result = []
    for session in sessions:
        tests = db.query(models.Test).filter(models.Test.session_id == session.id).all()
        application = db.query(models.Application).filter(models.Application.id == session.application_id).first() if session.application_id else None
        result.append({
            "id": session.id,
            "nom": session.nom,
            "description": session.description,
            "application_id": session.application_id,
            "application_nom": application.nom if application else None,
            "environnement": session.environnement,
            "version": session.version,
            "nom_document": session.nom_document,
            "date_creation": session.date_creation,
            "statut": session.statut,
            "created_by": session.created_by,
            "tests": tests,
            "total_tests": len(tests),
            "tests_ok": len([t for t in tests if t.statut == "OK"]),
            "tests_bug": len([t for t in tests if t.statut == "BUG"]),
            "tests_en_cours": len([t for t in tests if t.statut == "EN COURS"])
        })
    return result


@router.get("/{session_id}")
def get_test_session(session_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    session = db.query(models.TestSession).filter(models.TestSession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    tests = db.query(models.Test).filter(models.Test.session_id == session_id).all()
    application = db.query(models.Application).filter(models.Application.id == session.application_id).first() if session.application_id else None
    return {
        "id": session.id,
        "nom": session.nom,
        "description": session.description,
        "application_id": session.application_id,
        "application_nom": application.nom if application else None,
        "environnement": session.environnement,
        "version": session.version,
        "nom_document": session.nom_document,
        "date_creation": session.date_creation,
        "statut": session.statut,
        "created_by": session.created_by,
        "tests": tests,
        "total_tests": len(tests),
        "tests_ok": len([t for t in tests if t.statut == "OK"]),
        "tests_bug": len([t for t in tests if t.statut == "BUG"]),
        "tests_en_cours": len([t for t in tests if t.statut == "EN COURS"])
    }


@router.post("/")
def create_test_session(session: TestSessionBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_session = models.TestSession(
        nom=session.nom,
        description=session.description,
        application_id=session.application_id,
        environnement=session.environnement,
        version=session.version,
        nom_document=session.nom_document,
        statut=session.statut,
        created_by=current_user.id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.put("/{session_id}")
def update_test_session(session_id: int, session: TestSessionBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_session = db.query(models.TestSession).filter(models.TestSession.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    db_session.nom = session.nom
    db_session.description = session.description
    db_session.application_id = session.application_id
    db_session.environnement = session.environnement
    db_session.version = session.version
    db_session.nom_document = session.nom_document
    db_session.statut = session.statut

    db.commit()
    db.refresh(db_session)
    return db_session


@router.delete("/{session_id}")
def delete_test_session(session_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_session = db.query(models.TestSession).filter(models.TestSession.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    db.query(models.Test).filter(models.Test.session_id == session_id).delete()

    db.delete(db_session)
    db.commit()
    return {"message": "Session and all tests deleted"}


@router.post("/{session_id}/import")
def import_tests_from_pdf(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_session = db.query(models.TestSession).filter(models.TestSession.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        contents = file.file.read()
        pdf_file = io.BytesIO(contents)

        imported_tests = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for i, row in enumerate(table):
                        if i == 0 and any('fonction' in str(cell).lower() for cell in row if cell):
                            continue

                        if row and len(row) >= 1 and row[0]:
                            test = models.Test(
                                session_id=session_id,
                                fonction=str(row[0]).strip() if row[0] else '',
                                precondition=str(row[1]).strip() if len(row) > 1 and row[1] else None,
                                etapes=str(row[2]).strip() if len(row) > 2 and row[2] else None,
                                resultat_attendu=str(row[3]).strip() if len(row) > 3 and row[3] else None,
                                resultat_obtenu=str(row[4]).strip() if len(row) > 4 and row[4] else None,
                                statut=str(row[5]).strip() if len(row) > 5 and row[5] else 'Non testé',
                                commentaires=str(row[6]).strip() if len(row) > 6 and row[6] else None,
                                application_id=db_session.application_id,
                                created_by=current_user.id,
                            )
                            db.add(test)
                            imported_tests.append(test)

        db.commit()

        for test in imported_tests:
            db.refresh(test)

        return imported_tests

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
