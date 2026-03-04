from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from .db.session import engine, Base, SessionLocal
from .models import all_models

# Create tables (for testing without alembic initially)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AMEN Platform API",
    description="""
    Backend API for AMEN (Appui aux Ménages et Environnement Naturel).
    
    ### Modules
    * **Auth**: JWT-based authentication with role-based access control (admin / staff).
    * **News**: Management of bilingual articles with auto-translation.
    * **Projects**: Tracking of NGO initiatives and impact stats.
    * **Resources**: Library of reports and guides.
    * **Events**: Community workshops and schedule.
    * **Multimedia**: Photos and videos gallery.
    * **Inquiries**: Contact forms and volunteering.
    * **Live Stats**: Real-time KPI display.
    * **Settings**: Portal-wide configuration (admin only write).
    """,
    version="2.0.0",
    contact={
        "name": "AMEN Platform Support",
        "url": "http://localhost:3000/contact",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "*"  # For development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
upload_dir = os.path.join(static_dir, "images")
for d in [static_dir, upload_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.on_event("startup")
def on_startup():
    """Seed default admin and portal settings on first run."""
    db = SessionLocal()
    try:
        from .crud.user import ensure_default_admin
        from .crud.settings import get_settings
        ensure_default_admin(db)
        get_settings(db)  # ensures singleton settings row exists
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to AMEN Platform API", "status": "running", "version": "2.0.0"}


# Import routers
from .api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")
