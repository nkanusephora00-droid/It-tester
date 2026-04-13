from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import applications, comptes, habilitations, tests, auth, users, test_sessions

app = FastAPI(title="IT Access Manager", description="Gestion des accès et mots de passe pour systèmes internes", version="1.0.0")

# Configure CORS for frontend on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(comptes.router, prefix="/comptes", tags=["comptes"])
app.include_router(habilitations.router, prefix="/habilitations", tags=["habilitations"])
app.include_router(tests.router, prefix="/tests", tags=["tests"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(test_sessions.router, prefix="/test-sessions", tags=["test_sessions"])