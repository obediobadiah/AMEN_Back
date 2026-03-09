from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from .db.session import engine, Base, SessionLocal
from .models import all_models

# Create tables (for testing without alembic initially)
# Note: In production, use migrations instead
try:
    # Check if we have production database configured (DATABASE_URL, POSTGRES_URL, or Supabase vars)
    has_prod_db = (
        os.getenv("DATABASE_URL") or 
        os.getenv("POSTGRES_URL") or 
        os.getenv("POSTGRES_PRISMA_URL") or
        (os.getenv("POSTGRES_HOST") and os.getenv("POSTGRES_HOST") != "localhost")
    )
    
    if has_prod_db:
        Base.metadata.create_all(bind=engine)
        print("Database tables created/verified successfully")
    else:
        print("Warning: No production database configured. Skipping table creation.")
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("Continuing without database initialization...")

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
