# Utiliser l'image officielle Python comme base
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application backend seulement
COPY backend /app/backend

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Créer un groupe et un utilisateur non-root pour des raisons de sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Commande pour démarrer l'application
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
