from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from app.routes import base_route
from app.routes.v1.person_route import router
from app.core.config import settings
from app.storages.database_storage import close_db, connect_db


def get_application():
    """Create a new FastAPI application."""
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        debug=False
    )
    _app.include_router(base_route.router)
    _app.include_router(router)
    return _app


def get_complete_application():
    """In production need to start and close db connection and some middleware."""
    _app = get_application()
    _app.add_middleware(GZipMiddleware, minimum_size=1000)
    _app.add_event_handler("startup", connect_db)
    _app.add_event_handler("shutdown", close_db)
    return _app


app = get_complete_application()
