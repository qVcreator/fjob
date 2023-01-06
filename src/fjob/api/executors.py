from fastapi import APIRouter, Depends, status, HTTPException

from .. import models

from ..services import executors, role
from ..services.executors import ExecutorsService

router = APIRouter(
    prefix="/executors",
    tags=['executors']
)


@router.get(
    '/{executor_id}',
    response_model=models.ExecutorFullInfo,
    status_code=status.HTTP_200_OK
)
def get_executor_by_id(
        executor_id: int,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.ADMIN,
            models.Role.USER,
            models.Role.EXECUTOR
        ])),
        executor_service: ExecutorsService = Depends()):
    return executor_service.get_executor_by_id(executor_id)


@router.post(
    '/',
    response_model=models.Token,
    status_code=status.HTTP_201_CREATED
)
def create_executor(
        executor_data: models.CreateUser,
        executor_service: ExecutorsService = Depends()):
    return executor_service.create_executor(executor_data)


@router.put(
    '/{executor_id}',
    status_code=status.HTTP_204_NO_CONTENT)
def update_executor_information(
        executor_id: int,
        executor_data: models.UpdateExecutor,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.ADMIN,
            models.Role.EXECUTOR
        ])),
        executor_service: ExecutorsService = Depends()):

    if executor_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    executor_service.update_executor_information(executor_data, executor_id)
