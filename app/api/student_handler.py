from http import HTTPStatus

from fastapi import HTTPException, Depends, APIRouter
from starlette import status

from api.depends import validate_auth_admin

router = APIRouter()


@router.post("", response_model=None, status_code=HTTPStatus.CREATED)
async def create_user(
        #dto: RegisterUserDTO,
        #user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):

    try:
        pass
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=None, status_code=HTTPStatus.OK)
async def get_users(
        #user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):

    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{username}", response_model=None, status_code=HTTPStatus.OK)
async def delete_user(
        #username: str,
        #user_service: UserService = Depends(get_user_service),
        user=Depends(validate_auth_admin)
):

    try:
        pass
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
