from fastapi import APIRouter, Depends, status, HTTPException

from .. import models
from ..services import role
from ..services.comments import CommentsService

router = APIRouter(
    prefix="/comments",
    tags=['comments']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
def create_comment(
        comment_data: models.CreateComment,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.USER,
            models.Role.EXECUTOR
        ])),
        comments_service: CommentsService = Depends()
):
    if current_user.id == comment_data.user_to_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    comments_service.create_comment(comment_data, current_user.role)


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(
        comment_id: int,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.USER,
            models.Role.EXECUTOR
        ])),
        comments_service: CommentsService = Depends()
):
    comments_service.delete_comment(comment_id, current_user.id)
