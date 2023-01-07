from fastapi import APIRouter, Depends, status, HTTPException

from .. import models
from ..services import role
from ..services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get(
    '/{user_id}',
    response_model=models.UserAllInfo,
    status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int,
                   current_user: models.AuthUser = Depends(role.RoleChecker([
                       models.Role.ADMIN,
                       models.Role.USER,
                       models.Role.EXECUTOR
                   ])),
                   users_service: UsersService = Depends()
                   ):
    return users_service.get_user_by_id(user_id)


@router.post(
    '/',
    response_model=models.Token,
    status_code=status.HTTP_201_CREATED
)
def create_user(user_data: models.CreateUser,
                users_service: UsersService = Depends()):
    return users_service.create_user(user_data)


@router.put(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int,
                user_data: models.UpdateUser,
                current_user: models.AuthUser = Depends(role.RoleChecker([
                    models.Role.ADMIN,
                    models.Role.USER,
                ])),
                users_service: UsersService = Depends()
                ):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    users_service.update_user_information(user_data, user_id)
