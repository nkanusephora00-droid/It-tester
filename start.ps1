# Script de lancement pour IT Access Manager
Write-Host "Lancement de l'application IT Access Manager..." -ForegroundColor Green
Write-Host ""

$env:Path = "C:\Users\Ir Jp Bolombo\AppData\Local\Programs\Python\Python314;" + $env:Path

# Verifier si Python est installe
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python trouve: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python n'est pas installe. Veuillez installer Python 3.12+" -ForegroundColor Red
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

# Aller dans le repertoire backend
Set-Location backend

# Installer les dependances
Write-Host "Installation des dependances..." -ForegroundColor Yellow
pip install -r ../requirements.txt

# Creer les tables (migration)
Write-Host "Creation/mise a jour des tables..." -ForegroundColor Yellow
python ../migrate_settings.py

# Creer l'utilisateur admin
Write-Host "Creation de l'utilisateur admin..." -ForegroundColor Yellow
python ../create_admin.py

# Lancer l'application
Write-Host ""
Write-Host "Demarrage de l'application backend..." -ForegroundColor Green
Write-Host "L'application sera disponible sur: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter l'application" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
