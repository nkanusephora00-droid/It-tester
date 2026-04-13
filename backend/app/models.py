from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    description = Column(Text)
    version = Column(String(50))
    environnement = Column(String(50))
    date_creation = Column(TIMESTAMP, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))  # Ajout du champ pour suivre le créateur

    comptes = relationship("Compte", back_populates="application")
    tests = relationship("Test", back_populates="application")

class Compte(Base):
    __tablename__ = "comptes"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    username = Column(String(100), nullable=False)
    code = Column(Text)  # Store password (plain text)
    role = Column(String(50))
    commentaire = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))  # Ajout du champ pour suivre le créateur

    application = relationship("Application", back_populates="comptes")
    habilitations = relationship("Habilitation", back_populates="compte")

class Habilitation(Base):
    __tablename__ = "habilitations"

    id = Column(Integer, primary_key=True, index=True)
    compte_id = Column(Integer, ForeignKey("comptes.id"))
    permission = Column(String(100), nullable=False)

    compte = relationship("Compte", back_populates="habilitations")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"))
    application_id = Column(Integer, ForeignKey("applications.id"))
    application_nom = Column(String(100))  # Nom de l'application (peut être différent de application_id)
    version = Column(String(50))
    environnement = Column(String(50))
    fonction = Column(String(200), nullable=False)
    precondition = Column(Text)
    etapes = Column(Text)
    resultat_attendu = Column(Text)
    resultat_obtenu = Column(Text)
    statut = Column(String(50))  # OK, BUG, EN COURS, BLOQUE
    commentaires = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))  # Ajout du champ pour suivre le créateur

    application = relationship("Application", back_populates="tests")
    session = relationship("TestSession", back_populates="tests")

class TestSession(Base):
    __tablename__ = "test_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(200), nullable=False)
    description = Column(Text)
    application_id = Column(Integer, ForeignKey("applications.id"))  # Application testée
    environnement = Column(String(50))  # Environnement: DEV, RECETTE, PROD, etc.
    version = Column(String(50))  # Version de l'application
    nom_document = Column(String(200))  # Nom du document de test
    date_creation = Column(TIMESTAMP, server_default=func.now())
    statut = Column(String(50), default="En cours")  # En cours, Terminé
    created_by = Column(Integer, ForeignKey("users.id"))  # Ajout du champ pour suivre le créateur
    
    application = relationship("Application")
    tests = relationship("Test", back_populates="session")

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(Text, nullable=False)
    date = Column(TIMESTAMP, server_default=func.now())


class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # admin ou user
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
