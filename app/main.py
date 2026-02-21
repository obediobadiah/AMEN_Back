from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from .db.session import engine, Base

# Create tables (for testing without alembic initially)
# In production, use migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AMEN Platform API",
    description="""
    Backend API for AMEN (Appui aux Ménages et Environnement Naturel).
    
    ### Modules
    * **News**: Management of bilingual articles with auto-translation.
    * **Projects**: Tracking of NGO initiatives and impact stats.
    * **Resources**: Library of reports and guides.
    * **Events**: Community workshops and schedule.
    * **Multimedia**: Photos and videos gallery.
    * **Inquiries**: Contact forms and volunteering.
    * **Live Stats**: Real-time KPI display.
    """,
    version="1.0.0",
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
    "*" # For development
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

@app.get("/")
async def root():
    return {"message": "Welcome to AMEN Platform API", "status": "running"}

# Import routers
from .api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")
