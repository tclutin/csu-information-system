from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pygments.lexers import q

from api.auth_handler import router as auth_router
from api.user_handler import router as user_router
from api.department_handler import router as department_router
from api.specialty_handler import router as specialty_router
from api.group_handler import router as group_router
from api.faq_handler import router as faq_router


from config.config import settings
from infrastructure.models import Base

from infrastructure.postgres import postgres_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with postgres_client.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await postgres_client.dispose()

main_app = FastAPI(lifespan=lifespan)


main_app.include_router(auth_router, prefix="/auth", tags=["auth"])
main_app.include_router(user_router, prefix="/users", tags=["user"])
main_app.include_router(faq_router, prefix="/faqs", tags=["faq"])
main_app.include_router(group_router, prefix="/groups", tags=["group"])
main_app.include_router(department_router, prefix="/departments", tags=["department"])
main_app.include_router(specialty_router, prefix="/specialties", tags=["specialty"])

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.http_host,
        port=settings.http_port,
        reload=True
    )
