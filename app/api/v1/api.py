from fastapi import APIRouter
from .endpoints import news, project, resource, event, multimedia, governance, inquiry, livestat, publication, album

api_router = APIRouter()
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(project.router, prefix="/projects", tags=["projects"])
api_router.include_router(resource.router, prefix="/resources", tags=["resources"])
api_router.include_router(event.router, prefix="/events", tags=["events"])
api_router.include_router(multimedia.router, prefix="/multimedia", tags=["multimedia"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(inquiry.router, prefix="/inquiries", tags=["inquiries"])
api_router.include_router(livestat.router, prefix="/stats", tags=["stats"])
api_router.include_router(publication.router, prefix="/publications", tags=["publications"])
api_router.include_router(album.router, prefix="/albums", tags=["albums"])
