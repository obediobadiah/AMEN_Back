from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Try to import psycopg2, fall back to basic postgres if not available
try:
    import psycopg2
    PSYCPOPG2_AVAILABLE = True
except ImportError:
    PSYCPOPG2_AVAILABLE = False

load_dotenv()

# Try to get DATABASE_URL first (for production), fall back to individual vars
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    # Use psycopg2 dialect if available, otherwise use basic postgres
    if PSYCPOPG2_AVAILABLE and DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    else:
        SQLALCHEMY_DATABASE_URL = DATABASE_URL
elif os.getenv("POSTGRES_PRISMA_URL"):
    # Use Supabase Prisma URL if available
    prisma_url = os.getenv("POSTGRES_PRISMA_URL")
    if prisma_url.startswith("postgres://"):
        prisma_url = prisma_url.replace("postgres://", "postgresql://", 1)
    if PSYCPOPG2_AVAILABLE and prisma_url.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = prisma_url.replace("postgresql://", "postgresql+psycopg2://")
    else:
        SQLALCHEMY_DATABASE_URL = prisma_url
else:
    # Fallback to individual Supabase environment variables
    DB_USER = os.getenv("POSTGRES_USER") or os.getenv("DB_USER", "amen_user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD", "amen_password")
    DB_NAME = os.getenv("POSTGRES_DATABASE") or os.getenv("DB_NAME", "amen_db")
    DB_HOST = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    if PSYCPOPG2_AVAILABLE:
        SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Handle SSL for production databases
if SQLALCHEMY_DATABASE_URL and ("neon.tech" in SQLALCHEMY_DATABASE_URL or "supabase.co" in SQLALCHEMY_DATABASE_URL):
    if "?" in SQLALCHEMY_DATABASE_URL:
        SQLALCHEMY_DATABASE_URL += "&sslmode=require"
    else:
        SQLALCHEMY_DATABASE_URL += "?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
