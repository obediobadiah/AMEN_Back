# AMEN Platform Backend

Backend API for AMEN (Appui aux Ménages et Environnement Naturel), a humanitarian organization focused on community empowerment and sustainable development in the Congo Basin.

## Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Validation**: Pydantic
- **Migrations**: Alembic
- **Translation**: Integrated auto-translation logic for bilingual content (FR/EN) using `deep-translator`

## Setup & Running Locally

1. **Prerequisites**: Python 3.9+
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   Interactive API Documentation: `http://localhost:8000/docs`.

## Project Structure
- `app/api/`: API endpoints organized by version and domain.
- `app/crud/`: CRUD operations logic (Create, Read, Update, Delete).
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic models for request/response validation.
- `app/db/`: Database session and engine configuration.
- `app/static/`: Static files and uploaded assets.

## API Environments
The platform is configured to communicate with the following environments:
- **Local**: `http://localhost:8000`
- **Production**: `http://amen-rdc.org`

## News Management
The News module supports:
- Bilingual content (Auto-translation from source language).
- Image uploads for thumbnails.
- Category-based filtering and status management (Published, Draft, Archived).
