from fastapi import APIRouter, Depends, status

from .. import models
from ..services import role
from ..services.suggestions import SuggestionsService

router = APIRouter(
    prefix="/suggestions",
    tags=['suggestions']
)


@router.put(
    '/{suggestion_id}',
    status_code=status.HTTP_200_OK
)
def suggestion_reply(
        suggestion_id: int,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.EXECUTOR
        ])),
        suggestions_service: SuggestionsService = Depends()
):
    suggestions_service.suggestion_reply(current_user.id, suggestion_id)


@router.post(
    '/',
    response_model=int,
    status_code=status.HTTP_201_CREATED
)
def create_suggestion(
        suggestion_data: models.SuggestionCreate,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.USER
        ])),
        suggestions_service: SuggestionsService = Depends()
):
    suggestions_service.create_suggestion(suggestion_data)


@router.put(
    '/{suggestion_id}',
    status_code=status.HTTP_200_OK
)
def update_suggestion(
        suggestion_id: int,
        suggestion_data: models.SuggestionUpdate,
        current_user: models.AuthUser = Depends(role.RoleChecker([
            models.Role.USER
        ])),
        suggestions_service: SuggestionsService = Depends()
):
    suggestions_service.update_suggestion(suggestion_id, current_user.id, suggestion_data)


@router.delete('/suggestion_delete')
def delete_suggestion():
    return []
