from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.exc import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from infrastructure.postgres import postgres_client
from repositories.department_repository import DepartmentRepository
from repositories.faq_repository import FAQRepository
from repositories.group_repository import GroupRepository
from repositories.specialty_repository import SpecialtyRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.department_service import DepartmentService
from services.faq_service import FAQService
from services.group_service import GroupService
from services.specialty_repository import SpecialtyService
from services.user_service import UserService

http_bearer = HTTPBearer()


def get_user_repository(session: AsyncSession = Depends(postgres_client.session_getter)) -> UserRepository:
    return UserRepository(session)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


def get_department_repository(session: AsyncSession = Depends(postgres_client.session_getter)) -> DepartmentRepository:
    return DepartmentRepository(session)


def get_department_service(
        department_repository: DepartmentRepository = Depends(get_department_repository)) -> DepartmentService:
    return DepartmentService(department_repository)


def get_specialty_repository(session: AsyncSession = Depends(postgres_client.session_getter)) -> SpecialtyRepository:
    return SpecialtyRepository(session)


def get_specialty_service(
        specialty_repository: SpecialtyRepository = Depends(get_specialty_repository)) -> SpecialtyService:
    return SpecialtyService(specialty_repository)


def get_group_repository(session: AsyncSession = Depends(postgres_client.session_getter)) -> GroupRepository:
    return GroupRepository(session)


def get_group_service(group_repository: GroupRepository = Depends(get_group_repository)) -> GroupService:
    return GroupService(group_repository)


def get_faq_repository(session: AsyncSession = Depends(postgres_client.session_getter)) -> FAQRepository:
    return FAQRepository(session)


def get_faq_service(faq_repository: FAQRepository = Depends(get_faq_repository)) -> FAQService:
    return FAQService(faq_repository)


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)


def validate_auth_user(
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.verify_token(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )


async def validate_auth_admin(
        payloads=Depends(validate_auth_user),
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_by_username(payloads["sub"])
    if user.role not in ["admin", "system"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions"
        )

    return user
