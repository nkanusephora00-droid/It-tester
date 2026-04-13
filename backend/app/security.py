# Import du module bcrypt pour gérer le hachage des mots de passe
import bcrypt

# Vérifie un mot de passe en clair contre un hash stocké
def verify_password(plain_password, hashed_password):
    # Convertir le mot de passe en octets UTF-8
    plain_password_bytes = plain_password.encode('utf-8')
    # Convertir le hash stocké en octets si nécessaire
    hashed_password_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    # Vérifier le mot de passe avec bcrypt
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

# Hash un mot de passe pour le stockage sécurisé
def hash_password(password):
    # Convertir le mot de passe en octets UTF-8
    password_bytes = password.encode('utf-8')
    # Générer le sel et hacher le mot de passe
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retourner le hash en chaîne de caractères
    return hashed.decode('utf-8')
